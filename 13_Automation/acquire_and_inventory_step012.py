"""Controlled STEP-012 off-Git dataset downloader, verifier, extractor, and inventory CLI."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.dataset_intake import (  # noqa: E402
    compute_file_hashes,
    inventory_raw_dataset,
    write_archive_receipt,
)

RAW_ROOT = ROOT / "03_Datasets" / "raw"
MANIFEST_ROOT = ROOT / "03_Datasets" / "manifests"


@dataclass(frozen=True)
class ArchiveSource:
    """One verified downloadable archive belonging to a dataset."""

    filename: str
    url: str
    expected_md5: str | None = None
    expected_bytes: int | None = None


@dataclass(frozen=True)
class DatasetSpec:
    """Declarative STEP-012 specification for an authorized dataset."""

    dataset_id: str
    candidate_id: str
    kind: str  # "archive" or "huggingface"
    archives: tuple[ArchiveSource, ...] = ()
    hf_repo: str = ""


DATASET_SPECS: dict[str, DatasetSpec] = {
    "DS0001": DatasetSpec(
        dataset_id="DS0001",
        candidate_id="CAND0001",
        kind="archive",
        archives=(
            ArchiveSource(
                filename="panoramic_radiography_yolo_dataset_14_classes.zip",
                url="https://zenodo.org/api/records/15487430/files/panoramic_radiography_yolo_dataset_14_classes.zip/content",
                expected_md5="18d5acaea021f4f3b05b76e9a27fbd42",
                expected_bytes=1397393531,
            ),
        ),
    ),
    "DS0002": DatasetSpec(
        dataset_id="DS0002",
        candidate_id="CAND0002",
        kind="archive",
        archives=(
            ArchiveSource(
                filename="training_data.zip",
                url="https://zenodo.org/api/records/7812323/files/training_data.zip/content",
                expected_md5="eba0c44fa4c6e8ec221db3009eccc1f9",
                expected_bytes=10927391529,
            ),
            ArchiveSource(
                filename="validation_data.zip",
                url="https://zenodo.org/api/records/7812323/files/validation_data.zip/content",
                expected_md5="b2a13267740185e42cb59e968bc3ce83",
                expected_bytes=149512256,
            ),
        ),
    ),
    "DS0003": DatasetSpec(
        dataset_id="DS0003",
        candidate_id="CAND0003",
        kind="archive",
        archives=(
            ArchiveSource(
                filename="c4hhrkxytw-4.zip",
                url="https://data.mendeley.com/public-api/zip/c4hhrkxytw/download/4",
                expected_md5=None,
                expected_bytes=206222368,
            ),
        ),
    ),
    "DS0004": DatasetSpec(
        dataset_id="DS0004",
        candidate_id="CAND0004",
        kind="archive",
        archives=(
            ArchiveSource(
                filename="kx52tk2ddj-3.zip",
                url="https://data.mendeley.com/public-api/zip/kx52tk2ddj/download/3",
                expected_md5=None,
                expected_bytes=8922133584,
            ),
        ),
    ),
    "DS0005": DatasetSpec(
        dataset_id="DS0005",
        candidate_id="CAND0005",
        kind="huggingface",
        hf_repo="YSFF/AU-OPG",
    ),
    "DS0006": DatasetSpec(
        dataset_id="DS0006",
        candidate_id="CAND0007",
        kind="archive",
        archives=(
            ArchiveSource(
                filename="MD_OPG.rar",
                url="https://zenodo.org/api/records/17786082/files/MD_OPG.rar/content",
                expected_md5="5ea31fe4474307f0bdba9591b39574cf",
                expected_bytes=252876370,
            ),
        ),
    ),
}


def _download_with_curl(url: str, dest: Path) -> None:
    """Download a potentially large file using resumable curl.exe."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "curl.exe",
        "-fL",
        "-C",
        "-",
        "--retry",
        "5",
        "--retry-delay",
        "3",
        "--speed-limit",
        "1024",
        "--speed-time",
        "45",
        "-A",
        "Mozilla/5.0 ThesisPhase1-STEP012/1.0",
        "-o",
        str(dest),
        url,
    ]
    print(f"Downloading {dest.name} from {url} ...", flush=True)
    for attempt in range(1, 6):
        proc = subprocess.run(cmd, check=False)
        if proc.returncode == 0:
            return
        print(f"Attempt {attempt}/5 failed (rc={proc.returncode}); resuming {dest.name}...", flush=True)
    raise subprocess.CalledProcessError(proc.returncode, cmd)


def _verify_archive(path: Path, src: ArchiveSource) -> dict[str, object]:
    """Verify size and expected MD5 (when declared), returning immutable archive metadata."""
    hashes = compute_file_hashes(path)
    if src.expected_bytes is not None and hashes["size_bytes"] != src.expected_bytes:
        raise ValueError(
            f"Size mismatch for {path.name}: expected {src.expected_bytes}, got {hashes['size_bytes']}"
        )
    if src.expected_md5 is not None and hashes["md5"] != src.expected_md5:
        raise ValueError(
            f"MD5 mismatch for {path.name}: expected {src.expected_md5}, got {hashes['md5']}"
        )
    return {
        "filename": src.filename,
        "url": src.url,
        "expected_md5": src.expected_md5,
        "expected_bytes": src.expected_bytes,
        "verified_md5": hashes["md5"],
        "verified_sha256": hashes["sha256"],
        "verified_bytes": hashes["size_bytes"],
    }


def _extract_archive(archive_path: Path, target_dir: Path) -> None:
    """Extract .zip via stdlib zipfile or .rar via Windows bsdtar without modifying archive bytes."""
    target_dir.mkdir(parents=True, exist_ok=True)
    suffix = archive_path.suffix.lower()
    if suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(target_dir)
    elif suffix == ".rar":
        subprocess.run(
            ["tar", "-xf", str(archive_path), "-C", str(target_dir)],
            check=True,
        )
    else:
        raise ValueError(f"Unsupported archive format: {archive_path}")


def _acquire_archive_dataset(spec: DatasetSpec) -> list[dict[str, object]]:
    """Download, hash-check, and extract archive-based DS#### datasets cleanly."""
    ds_raw = RAW_ROOT / spec.dataset_id
    archive_dir = ds_raw / "archive"
    extracted_dir = ds_raw / "extracted"
    state_file = ds_raw / ".intake_state.json"

    archive_records: list[dict[str, object]] = []
    for src in spec.archives:
        dest = archive_dir / src.filename
        if dest.is_file():
            try:
                rec = _verify_archive(dest, src)
                print(f"[SKIP-VERIFIED] {spec.dataset_id}/{src.filename}", flush=True)
                archive_records.append(rec)
                continue
            except ValueError as err:
                print(f"[RESUME/REDOWNLOAD] {src.filename}: {err}", flush=True)
        _download_with_curl(src.url, dest)
        rec = _verify_archive(dest, src)
        print(f"[HASH-OK] {spec.dataset_id}/{src.filename}: sha256={rec['verified_sha256']}", flush=True)
        archive_records.append(rec)

    prev_state: dict[str, object] = {}
    if state_file.is_file():
        prev_state = json.loads(state_file.read_text(encoding="utf-8"))
    expected_hashes = [r["verified_sha256"] for r in archive_records]

    if prev_state.get("extracted_for_sha256") != expected_hashes:
        multi_archive = len(spec.archives) > 1
        for src in spec.archives:
            arch_path = archive_dir / src.filename
            out_dir = (extracted_dir / arch_path.stem) if multi_archive else extracted_dir
            print(f"[EXTRACT] {arch_path.name} -> {out_dir}", flush=True)
            _extract_archive(arch_path, out_dir)
        state_file.write_text(
            json.dumps({"extracted_for_sha256": expected_hashes}, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print(f"[SKIP-EXTRACT] {spec.dataset_id} already extracted for matching archive hashes", flush=True)

    return archive_records


def _hf_tree_items(repo: str, subdir: str = "") -> list[dict[str, object]]:
    """List all file entries under a HuggingFace dataset repo path via cursor pagination."""
    suffix = f"/{subdir}" if subdir else ""
    url: str | None = f"https://huggingface.co/api/datasets/{repo}/tree/main{suffix}?limit=1000"
    items: list[dict[str, object]] = []
    while url:
        req = urllib.request.Request(url, headers={"User-Agent": "ThesisPhase1-STEP012/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            items.extend(json.loads(resp.read().decode("utf-8")))
            link = resp.headers.get("Link", "")
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
    return [x for x in items if x.get("type") == "file"]


def _acquire_hf_dataset(spec: DatasetSpec) -> list[dict[str, object]]:
    """Mirror a HuggingFace dataset snapshot into extracted/ with per-file size + SHA-256 verification."""
    ds_raw = RAW_ROOT / spec.dataset_id
    extracted_dir = ds_raw / "extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)

    root_files = _hf_tree_items(spec.hf_repo, "")
    dataset_files = _hf_tree_items(spec.hf_repo, "dataset")
    all_files = root_files + dataset_files
    print(f"[HF] {spec.hf_repo}: {len(all_files)} remote files discovered", flush=True)

    def _fetch_one(entry: dict[str, object]) -> tuple[str, int, str]:
        rel = str(entry["path"])
        expected_size = int(entry["size"])
        lfs_sha = (entry.get("lfs") or {}).get("oid") if isinstance(entry.get("lfs"), dict) else None
        dest = extracted_dir / rel
        if dest.is_file() and dest.stat().st_size == expected_size:
            hashes = compute_file_hashes(dest)
            if not lfs_sha or hashes["sha256"] == lfs_sha:
                return rel, expected_size, str(hashes["sha256"])

        dest.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://huggingface.co/datasets/{spec.hf_repo}/resolve/main/{rel}"
        req = urllib.request.Request(url, headers={"User-Agent": "ThesisPhase1-STEP012/1.0"})
        tmp = dest.with_suffix(dest.suffix + ".part")
        with urllib.request.urlopen(req, timeout=60) as resp, tmp.open("wb") as out:
            while chunk := resp.read(256 * 1024):
                out.write(chunk)
        tmp.replace(dest)

        hashes = compute_file_hashes(dest)
        if hashes["size_bytes"] != expected_size:
            raise ValueError(f"HF size mismatch for {rel}: {hashes['size_bytes']} != {expected_size}")
        if lfs_sha and hashes["sha256"] != lfs_sha:
            raise ValueError(f"HF SHA-256 mismatch for {rel}: {hashes['sha256']} != {lfs_sha}")
        return rel, expected_size, str(hashes["sha256"])

    verified_bytes = 0
    verified_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for _, sz, _ in pool.map(_fetch_one, all_files):
            verified_bytes += sz
            verified_count += 1
            if verified_count % 200 == 0 or verified_count == len(all_files):
                print(f"[HF {spec.dataset_id}] {verified_count}/{len(all_files)} files verified", flush=True)

    return [
        {
            "filename": f"huggingface:{spec.hf_repo}",
            "url": f"https://huggingface.co/datasets/{spec.hf_repo}",
            "expected_md5": None,
            "expected_bytes": verified_bytes,
            "verified_md5": None,
            "verified_sha256": None,
            "verified_bytes": verified_bytes,
            "file_count": verified_count,
        }
    ]


def _build_classifier(spec: DatasetSpec, extracted_dir: Path) -> Callable[[str], tuple[str, str]]:
    """Build deterministic sanitized folder/split bucket classifier per dataset."""
    if spec.dataset_id == "DS0005":
        split_lookup: dict[str, str] = {}
        for split_name, csv_name in (
            ("train_annotated", "train_annotations.csv"),
            ("val_annotated", "val_annotations.csv"),
            ("test_annotated", "test_annotations.csv"),
        ):
            csv_path = extracted_dir / csv_name
            if csv_path.is_file():
                with csv_path.open("r", encoding="utf-8", newline="") as handle:
                    for row in csv.DictReader(handle):
                        img_name = row.get("image", "").strip()
                        if img_name:
                            split_lookup[img_name] = split_name

        def _cls_ds5(relpath: str) -> tuple[str, str]:
            name = Path(relpath).name
            if "/" not in relpath and name == "sample_with_ground_truth.png":
                return "readme_sample_figure", "quarantined-sample-figure"
            if name in split_lookup:
                return split_lookup[name], "acquired-uninspected"
            return "unannotated_extra_in_dataset", "quarantined-unannotated-extra"

        return _cls_ds5

    if spec.dataset_id == "DS0001":
        def _cls_ds1(relpath: str) -> tuple[str, str]:
            low = relpath.lower()
            if low.startswith("test_alte_cabinete/"):
                return "external_validation", "acquired-uninspected"
            if low.startswith("train/"):
                return "internal_train", "acquired-uninspected"
            if low.startswith("valid/"):
                return "internal_valid", "acquired-uninspected"
            if low.startswith("test/"):
                return "internal_test", "acquired-uninspected"
            return "other_raw_folder", "acquired-uninspected"

        return _cls_ds1

    if spec.dataset_id == "DS0003":
        def _cls_ds3(relpath: str) -> tuple[str, str]:
            low = relpath.lower()
            if "dental opg (object detection)/original dataset/" in low:
                return "object_detection_original", "acquired-uninspected"
            if "dental opg (object detection)/augmented dataset/train/" in low:
                return "object_detection_aug_train", "quarantined-pre-augmented"
            if "dental opg (object detection)/augmented dataset/valid/" in low:
                return "object_detection_aug_valid", "quarantined-pre-split-aug"
            if "dental opg (object detection)/augmented dataset/test/" in low:
                return "object_detection_aug_test", "quarantined-pre-split-aug"
            if "dental opg (classification)/" in low:
                return "classification_branch", "quarantined-classification-branch"
            return "other_raw_folder", "acquired-uninspected"

        return _cls_ds3

    if spec.dataset_id == "DS0006":
        def _cls_ds6(relpath: str) -> tuple[str, str]:
            low = relpath.lower()
            if "/opg_image/" in f"/{low}":
                return "opg_original", "acquired-uninspected"
            if "/smile_zone_img/" in f"/{low}":
                return "smile_zone_crop", "quarantined-derived-crop"
            if "/smile_zone_msk/" in f"/{low}":
                return "smile_zone_mask", "quarantined-derived-mask"
            return "other_raw_folder", "acquired-uninspected"

        return _cls_ds6

    if spec.dataset_id == "DS0004":
        def _cls_ds4(relpath: str) -> tuple[str, str]:
            low = relpath.lower()
            if "augment" in low:
                return "augmentation_jpg_folder", "quarantined-pre-augmented"
            if "original" in low:
                return "original_jpg_folder", "acquired-uninspected"
            return "other_raw_folder", "acquired-uninspected"

        return _cls_ds4

    if spec.dataset_id == "DS0002":
        def _cls_ds2(relpath: str) -> tuple[str, str]:
            low = relpath.lower()
            parts = [p.lower() for p in Path(relpath).parts]
            if ".ipynb_checkpoints" in parts:
                return "validation_ipynb_checkpoint", "quarantined-author-checkpoint"
            if "validation_data" in parts:
                return "validation_quadrant_enumeration_disease_no_gt", "acquired-uninspected"
            if "unlabelled" in low or "unlabeled" in low:
                return "training_unlabelled_xrays", "quarantined-unlabeled-pool"
            if "quadrant-enumeration-disease" in low:
                return "training_quadrant_enumeration_disease", "acquired-uninspected"
            if "quadrant_enumeration" in low:
                return "training_quadrant_enumeration_only", "quarantined-no-disease-labels"
            if "/quadrant/" in f"/{low}":
                return "training_quadrant_only", "quarantined-no-disease-labels"
            return "training_other", "acquired-uninspected"

        return _cls_ds2

    def _cls_generic(relpath: str) -> tuple[str, str]:
        low = relpath.lower()
        if "external" in low:
            return "external_cohort", "acquired-uninspected"
        for tag in ("train", "valid", "val", "test", "segmentation", "classification"):
            if f"/{tag}/" in f"/{low}/":
                return tag, "acquired-uninspected"
        return "raw_default", "acquired-uninspected"

    return _cls_generic


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire and inventory STEP-012 datasets safely off-Git.")
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=sorted(DATASET_SPECS.keys()),
        default=sorted(DATASET_SPECS.keys()),
        help="DatasetIDs to process.",
    )
    parser.add_argument(
        "--mode",
        choices=("download", "inventory", "all"),
        default="all",
        help="Download/extract only, inventory only, or both.",
    )
    args = parser.parse_args()

    for ds_id in args.datasets:
        spec = DATASET_SPECS[ds_id]
        extracted_dir = RAW_ROOT / ds_id / "extracted"
        archive_records: list[dict[str, object]] = []

        if args.mode in ("download", "all"):
            if spec.kind == "archive":
                archive_records = _acquire_archive_dataset(spec)
            elif spec.kind == "huggingface":
                archive_records = _acquire_hf_dataset(spec)
            else:
                raise ValueError(f"Unknown dataset kind: {spec.kind}")
            (RAW_ROOT / ds_id / ".archive_records.json").write_text(
                json.dumps(archive_records, indent=2) + "\n", encoding="utf-8"
            )
        elif (RAW_ROOT / ds_id / ".archive_records.json").is_file():
            archive_records = json.loads(
                (RAW_ROOT / ds_id / ".archive_records.json").read_text(encoding="utf-8")
            )

        if args.mode in ("inventory", "all"):
            classifier = _build_classifier(spec, extracted_dir)
            summary = inventory_raw_dataset(
                dataset_id=spec.dataset_id,
                candidate_id=spec.candidate_id,
                extracted_root=extracted_dir,
                manifest_dir=MANIFEST_ROOT,
                classifier=classifier,
            )
            receipt = write_archive_receipt(
                manifest_dir=MANIFEST_ROOT,
                dataset_id=spec.dataset_id,
                candidate_id=spec.candidate_id,
                archives=archive_records,
                summary=summary,
            )
            print(
                f"[INVENTORY {ds_id}] total={summary.total_scanned_images}, "
                f"active={summary.active_raw_count}, quarantined={summary.quarantined_count}, "
                f"errors={summary.decode_error_count}, unique_active_sha256={summary.unique_sha256_active}, "
                f"manifest_sha256={summary.manifest_sha256[:12]}... -> {receipt.name}",
                flush=True,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
