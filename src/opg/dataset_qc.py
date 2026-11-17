"""Read-only STEP-013 image quality, EXIF privacy, dHash duplicate, and label integrity checks."""

from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
from PIL import ExifTags, Image

EXIF_TAG_NAMES = {k: str(v) for k, v in ExifTags.TAGS.items()}
SENSITIVE_EXIF_TAGS = frozenset(
    {
        "Make",
        "Model",
        "Software",
        "DateTime",
        "DateTimeOriginal",
        "DateTimeDigitized",
        "Artist",
        "Copyright",
        "UserComment",
        "ImageDescription",
        "GPSInfo",
        "HostComputer",
        "OwnerName",
        "CameraOwnerName",
    }
)


@dataclass(frozen=True)
class ImageQCRecord:
    """Measured pixel, EXIF, blur, contrast, and perceptual hash metrics for one image."""

    image_id: str
    relpath: str
    source_bucket: str
    sha256: str
    dhash64: str
    width: int
    height: int
    aspect_ratio: float
    mode: str
    is_grayscale_identical_rgb: bool
    mean_luma: float
    std_luma: float
    p05_luma: float
    p95_luma: float
    pct_black_le_3: float
    pct_white_ge_252: float
    laplacian_var: float
    exif_tag_count: int
    sensitive_exif_keys: tuple[str, ...]
    png_text_keys: tuple[str, ...]


def compute_dhash64(gray: np.ndarray) -> str:
    """Compute a 64-bit difference hash (8 rows x 9 cols) formatted as 16 hex chars."""
    resized = cv2.resize(gray, (9, 8), interpolation=cv2.INTER_AREA)
    diff = resized[:, 1:] > resized[:, :-1]
    bits = 0
    for val in diff.flatten():
        bits = (bits << 1) | int(bool(val))
    return f"{bits:016x}"


def hamming_distance_hex(h1: str, h2: str) -> int:
    """Return Hamming bit distance between two equal-length hex hash strings."""
    return (int(h1, 16) ^ int(h2, 16)).bit_count()


def inspect_image_qc(image_id: str, path: Path, relpath: str, source_bucket: str, sha256: str) -> ImageQCRecord:
    """Run read-only PIL EXIF/info inspection plus OpenCV grayscale QC metrics on one image."""
    with Image.open(path) as img:
        mode = img.mode
        width, height = img.size
        exif_raw = img.getexif()
        exif_keys = sorted(
            EXIF_TAG_NAMES.get(int(tag_id), f"Tag_{tag_id}") for tag_id in exif_raw.keys()
        )
        sensitive_keys = tuple(k for k in exif_keys if k in SENSITIVE_EXIF_TAGS)
        png_keys = tuple(
            sorted(
                str(k)
                for k in img.info.keys()
                if str(k).lower() not in {"dpi", "jfif", "jfif_version", "jfif_unit", "jfif_density", "adobe", "adobe_transform"}
            )
        )
        arr = np.asarray(img)

    if arr.ndim == 2:
        gray = arr
        is_gray_rgb = True
    elif arr.ndim == 3 and arr.shape[2] >= 3:
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        is_gray_rgb = bool(np.array_equal(r, g) and np.array_equal(g, b))
        gray = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2GRAY)
    else:
        gray = arr[:, :, 0]
        is_gray_rgb = True

    if gray.dtype != np.uint8:
        gray_u8 = np.clip(gray / (256.0 if gray.max() > 255 else 1.0), 0, 255).astype(np.uint8)
    else:
        gray_u8 = gray

    # Compute Laplacian variance at normalized width=800 to compare focus fairly across resolutions.
    scale_h = max(16, int(round(800 * (gray_u8.shape[0] / max(1, gray_u8.shape[1])))))
    norm_gray = cv2.resize(gray_u8, (800, scale_h), interpolation=cv2.INTER_AREA)
    lap_var = float(cv2.Laplacian(norm_gray, cv2.CV_64F).var())

    p05, p95 = np.percentile(gray_u8, [5, 95])
    total_px = float(gray_u8.size)
    return ImageQCRecord(
        image_id=image_id,
        relpath=relpath,
        source_bucket=source_bucket,
        sha256=sha256,
        dhash64=compute_dhash64(gray_u8),
        width=width,
        height=height,
        aspect_ratio=round(width / max(1, height), 4),
        mode=mode,
        is_grayscale_identical_rgb=is_gray_rgb,
        mean_luma=round(float(gray_u8.mean()), 2),
        std_luma=round(float(gray_u8.std()), 2),
        p05_luma=round(float(p05), 1),
        p95_luma=round(float(p95), 1),
        pct_black_le_3=round(100.0 * float((gray_u8 <= 3).sum()) / total_px, 2),
        pct_white_ge_252=round(100.0 * float((gray_u8 >= 252).sum()) / total_px, 2),
        laplacian_var=round(lap_var, 2),
        exif_tag_count=len(exif_keys),
        sensitive_exif_keys=sensitive_keys,
        png_text_keys=png_keys,
    )


def find_near_duplicate_pairs(
    records: Iterable[tuple[str, str, str, str]],
    *,
    max_hamming: int = 4,
) -> list[dict[str, object]]:
    """Find near-duplicate pairs (sha256 different or identical, dHash Hamming <= max_hamming).

    Each item is ``(image_id, sha256, dhash64, bucket)``.
    """
    items = list(records)
    ints = [int(item[2], 16) for item in items]
    pairs: list[dict[str, object]] = []
    n = len(items)
    for i in range(n):
        id_a, sha_a, d_a, b_a = items[i]
        int_a = ints[i]
        for j in range(i + 1, n):
            dist = (int_a ^ ints[j]).bit_count()
            if dist <= max_hamming:
                id_b, sha_b, d_b, b_b = items[j]
                pairs.append(
                    {
                        "id_a": id_a,
                        "id_b": id_b,
                        "bucket_a": b_a,
                        "bucket_b": b_b,
                        "same_sha256": sha_a == sha_b,
                        "hamming": dist,
                        "dhash_a": d_a,
                        "dhash_b": d_b,
                    }
                )
    return pairs


def audit_yolo_label_dir(image_paths: list[Path], label_dir: Path) -> dict[str, object]:
    """Audit YOLO normalized label files paired with image stems without altering files."""
    class_counts: Counter[int] = Counter()
    box_widths: dict[int, list[float]] = {}
    box_heights: dict[int, list[float]] = {}
    missing_txt = 0
    empty_txt = 0
    malformed_lines = 0
    oob_boxes = 0
    zero_area = 0
    total_boxes = 0

    for img_path in image_paths:
        lbl = label_dir / f"{img_path.stem}.txt"
        if not lbl.is_file():
            missing_txt += 1
            continue
        lines = [ln.strip() for ln in lbl.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
        if not lines:
            empty_txt += 1
            continue
        for ln in lines:
            parts = ln.split()
            if len(parts) < 5:
                malformed_lines += 1
                continue
            try:
                cls_id = int(float(parts[0]))
                xc, yc, w, h = (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
            except ValueError:
                malformed_lines += 1
                continue
            total_boxes += 1
            class_counts[cls_id] += 1
            box_widths.setdefault(cls_id, []).append(w)
            box_heights.setdefault(cls_id, []).append(h)
            if w <= 0 or h <= 0:
                zero_area += 1
            x1, y1 = xc - w / 2.0, yc - h / 2.0
            x2, y2 = xc + w / 2.0, yc + h / 2.0
            if x1 < -1e-4 or y1 < -1e-4 or x2 > 1.0001 or y2 > 1.0001:
                oob_boxes += 1

    per_class_geom = {
        cls_id: {
            "count": class_counts[cls_id],
            "mean_w": round(float(np.mean(box_widths[cls_id])), 4),
            "mean_h": round(float(np.mean(box_heights[cls_id])), 4),
        }
        for cls_id in sorted(class_counts)
    }
    return {
        "image_count": len(image_paths),
        "missing_txt": missing_txt,
        "empty_txt": empty_txt,
        "total_boxes": total_boxes,
        "malformed_lines": malformed_lines,
        "oob_boxes": oob_boxes,
        "zero_area": zero_area,
        "per_class": per_class_geom,
    }


def sha256_bytes(data: bytes) -> str:
    """Return hex SHA-256 digest of a byte buffer."""
    return hashlib.sha256(data).hexdigest()
