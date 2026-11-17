"""Read-only dataset intake, archive verification, and pseudonymous manifest tooling (STEP-012)."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from PIL import Image, UnidentifiedImageError

IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"})

PUBLIC_MANIFEST_COLUMNS = (
    "ImageID",
    "DatasetID",
    "CandidateID",
    "sha256",
    "md5",
    "file_size_bytes",
    "file_ext",
    "width",
    "height",
    "mode",
    "channels",
    "decode_status",
    "source_bucket",
    "intake_status",
    "error_message",
)

RESTRICTED_LINKAGE_COLUMNS = (
    "ImageID",
    "DatasetID",
    "original_relpath",
    "sha256",
    "intake_status",
)

MODE_CHANNELS = {
    "1": 1,
    "L": 1,
    "P": 1,
    "I": 1,
    "F": 1,
    "I;16": 1,
    "LA": 2,
    "RGB": 3,
    "YCbCr": 3,
    "LAB": 3,
    "HSV": 3,
    "RGBA": 4,
    "CMYK": 4,
}


@dataclass(frozen=True)
class InventorySummary:
    """Measured counts and digest for one STEP-012 dataset manifest."""

    dataset_id: str
    candidate_id: str
    total_scanned_images: int
    active_raw_count: int
    quarantined_count: int
    decode_error_count: int
    unique_sha256_all: int
    unique_sha256_active: int
    manifest_sha256: str
    manifest_path: str
    restricted_linkage_path: str


def compute_file_hashes(path: Path, chunk_size: int = 1024 * 1024) -> dict[str, int | str]:
    """Stream-compute SHA-256, MD5, and byte size for a file without modifying bytes."""
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            sha256.update(chunk)
            md5.update(chunk)
            size += len(chunk)
    return {
        "sha256": sha256.hexdigest(),
        "md5": md5.hexdigest(),
        "size_bytes": size,
    }


def _inspect_image_header(path: Path) -> tuple[int | str, int | str, str, int | str, str, str]:
    """Safely inspect image dimensions and decode health; emit explicit errors on failure."""
    try:
        with Image.open(path) as img:
            width, height = img.size
            mode = img.mode
            channels: int | str = MODE_CHANNELS.get(mode, len(img.getbands()))
            img.load()
        return width, height, mode, channels, "ok", ""
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        sanitized = str(exc).replace(str(path), "<image>").replace(path.name, "<image>")
        return "", "", "", "", "error", f"{type(exc).__name__}: {sanitized}"


def default_classifier(relpath: str) -> tuple[str, str]:
    """Classify a non-filtered raw image file into active uninspected inventory."""
    _ = relpath
    return "raw_default", "acquired-uninspected"


def inventory_raw_dataset(
    *,
    dataset_id: str,
    candidate_id: str,
    extracted_root: Path,
    manifest_dir: Path,
    classifier: Callable[[str], tuple[str, str]] | None = None,
) -> InventorySummary:
    """Walk extracted raw files read-only and emit public + restricted STEP-012 manifests.

    Every image file under ``extracted_root`` is hashed and decoded deterministically.
    Unreadable images are preserved with ``decode_status='error'`` rather than skipped.
    """
    classify_fn = classifier or default_classifier
    image_paths = sorted(
        (
            p
            for p in extracted_root.rglob("*")
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        ),
        key=lambda p: p.relative_to(extracted_root).as_posix().lower(),
    )

    manifest_dir.mkdir(parents=True, exist_ok=True)
    public_path = manifest_dir / f"{dataset_id}_images.csv"
    restricted_path = manifest_dir / f"{dataset_id}_restricted_linkage.csv"

    public_rows: list[list[object]] = []
    restricted_rows: list[list[object]] = []
    active_hashes: set[str] = set()
    all_hashes: set[str] = set()
    active_count = 0
    quarantined_count = 0
    decode_error_count = 0

    for idx, img_path in enumerate(image_paths, start=1):
        relpath = img_path.relative_to(extracted_root).as_posix()
        image_id = f"{dataset_id}_IMG_{idx:06d}"
        hashes = compute_file_hashes(img_path)
        sha256_hex = str(hashes["sha256"])
        all_hashes.add(sha256_hex)

        width, height, mode, channels, decode_status, error_msg = _inspect_image_header(img_path)
        source_bucket, intake_status = classify_fn(relpath)

        if decode_status != "ok":
            decode_error_count += 1
            intake_status = "decode-error"
        elif intake_status.startswith("quarantined"):
            quarantined_count += 1
        else:
            active_count += 1
            active_hashes.add(sha256_hex)

        public_rows.append(
            [
                image_id,
                dataset_id,
                candidate_id,
                sha256_hex,
                hashes["md5"],
                hashes["size_bytes"],
                img_path.suffix.lower(),
                width,
                height,
                mode,
                channels,
                decode_status,
                source_bucket,
                intake_status,
                error_msg,
            ]
        )
        restricted_rows.append([image_id, dataset_id, relpath, sha256_hex, intake_status])

    with public_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(PUBLIC_MANIFEST_COLUMNS)
        writer.writerows(public_rows)

    with restricted_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(RESTRICTED_LINKAGE_COLUMNS)
        writer.writerows(restricted_rows)

    total_scanned = len(image_paths)
    if active_count + quarantined_count + decode_error_count != total_scanned:
        raise RuntimeError(f"Inventory count mismatch for {dataset_id}")

    manifest_sha = str(compute_file_hashes(public_path)["sha256"])
    return InventorySummary(
        dataset_id=dataset_id,
        candidate_id=candidate_id,
        total_scanned_images=total_scanned,
        active_raw_count=active_count,
        quarantined_count=quarantined_count,
        decode_error_count=decode_error_count,
        unique_sha256_all=len(all_hashes),
        unique_sha256_active=len(active_hashes),
        manifest_sha256=manifest_sha,
        manifest_path=public_path.as_posix(),
        restricted_linkage_path=restricted_path.as_posix(),
    )


def write_archive_receipt(
    *,
    manifest_dir: Path,
    dataset_id: str,
    candidate_id: str,
    archives: list[dict[str, object]],
    summary: InventorySummary,
    notes: str = "",
) -> Path:
    """Write deterministic JSON intake receipt linking archives to the DS#### manifest hash."""
    receipt_path = manifest_dir / f"{dataset_id}_archive_hashes.json"
    payload = {
        "dataset_id": dataset_id,
        "candidate_id": candidate_id,
        "recorded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archives": archives,
        "inventory": {
            "total_scanned_images": summary.total_scanned_images,
            "active_raw_count": summary.active_raw_count,
            "quarantined_count": summary.quarantined_count,
            "decode_error_count": summary.decode_error_count,
            "unique_sha256_all": summary.unique_sha256_all,
            "unique_sha256_active": summary.unique_sha256_active,
            "manifest_sha256": summary.manifest_sha256,
        },
        "notes": notes,
    }
    receipt_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return receipt_path
