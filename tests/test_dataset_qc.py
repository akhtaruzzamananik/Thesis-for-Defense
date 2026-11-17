"""Unit tests for STEP-013 image QC metrics, EXIF detection, dHash clustering, and YOLO label audit."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.dataset_qc import audit_yolo_label_dir, find_near_duplicate_pairs, inspect_image_qc  # noqa: E402


def test_qc_detects_exif_tint_and_near_duplicates(tmp_path: Path) -> None:
    """Verify EXIF tagging, RGB tint check, and dHash near-duplicate catching work accurately."""
    img1 = tmp_path / "a.jpg"
    arr = np.tile(np.linspace(20, 220, 128, dtype=np.uint8), (64, 1))
    rgb_arr = np.stack([arr, arr, arr], axis=-1)
    exif = Image.Exif()
    exif[271] = "Samsung"  # Make tag
    Image.fromarray(rgb_arr, mode="RGB").save(img1, exif=exif.tobytes())

    # Re-encoded slightly noisier copy -> different sha256, identical or tiny Hamming dHash
    img2 = tmp_path / "b.png"
    noisy = np.clip(rgb_arr.astype(np.int16) + 2, 0, 255).astype(np.uint8)
    Image.fromarray(noisy, mode="RGB").save(img2)

    # Tinted non-grayscale RGB image with totally different pattern
    img3 = tmp_path / "c.png"
    rng = np.random.default_rng(7)
    tinted = rng.integers(0, 255, size=(64, 128, 3), dtype=np.uint8)
    Image.fromarray(tinted, mode="RGB").save(img3)

    r1 = inspect_image_qc("DS1_IMG_1", img1, "a.jpg", "orig", "sha1")
    r2 = inspect_image_qc("DS1_IMG_2", img2, "b.png", "cls", "sha2")
    r3 = inspect_image_qc("DS1_IMG_3", img3, "c.png", "orig", "sha3")

    assert r1.is_grayscale_identical_rgb is True
    assert "Make" in r1.sensitive_exif_keys
    assert r2.sensitive_exif_keys == ()
    assert r3.is_grayscale_identical_rgb is False

    pairs = find_near_duplicate_pairs(
        [
            (r1.image_id, r1.sha256, r1.dhash64, r1.source_bucket),
            (r2.image_id, r2.sha256, r2.dhash64, r2.source_bucket),
            (r3.image_id, r3.sha256, r3.dhash64, r3.source_bucket),
        ],
        max_hamming=4,
    )
    assert len(pairs) == 1
    assert pairs[0]["id_a"] == "DS1_IMG_1"
    assert pairs[0]["id_b"] == "DS1_IMG_2"
    assert pairs[0]["same_sha256"] is False


def test_audit_yolo_label_dir_catches_oob_and_missing(tmp_path: Path) -> None:
    """Verify YOLO label directory audit reports missing, empty, OOB, and valid counts cleanly."""
    img_dir = tmp_path / "images"
    lbl_dir = tmp_path / "labels"
    img_dir.mkdir()
    lbl_dir.mkdir()

    imgs = [img_dir / "x1.jpg", img_dir / "x2.jpg", img_dir / "x3.jpg"]
    for p in imgs:
        p.write_bytes(b"stub")

    (lbl_dir / "x1.txt").write_text("0 0.5 0.5 0.2 0.1\n1 0.99 0.5 0.1 0.1\n", encoding="utf-8")
    (lbl_dir / "x2.txt").write_text("", encoding="utf-8")
    # x3.txt intentionally missing

    summary = audit_yolo_label_dir(imgs, lbl_dir)
    assert summary["image_count"] == 3
    assert summary["missing_txt"] == 1
    assert summary["empty_txt"] == 1
    assert summary["total_boxes"] == 2
    assert summary["oob_boxes"] == 1
    assert summary["per_class"][0]["count"] == 1
