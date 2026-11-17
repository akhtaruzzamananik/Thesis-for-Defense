"""Unit tests for STEP-012 read-only dataset hashing, manifest separation, and error logging."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.dataset_intake import compute_file_hashes, inventory_raw_dataset  # noqa: E402


def test_inventory_preserves_errors_and_separates_linkage(tmp_path: Path) -> None:
    """Ensure corrupted images emit explicit errors and raw filenames stay out of public CSV."""
    extracted = tmp_path / "raw" / "extracted"
    orig_dir = extracted / "Original_Images"
    aug_dir = extracted / "Augmentation_Images"
    orig_dir.mkdir(parents=True)
    aug_dir.mkdir(parents=True)

    img1 = orig_dir / "patient_alpha_001.png"
    Image.new("L", (64, 32), color=128).save(img1)

    img2 = aug_dir / "aug_flip_001.jpg"
    Image.new("RGB", (80, 40), color=(10, 20, 30)).save(img2)

    bad_img = orig_dir / "corrupt_scan.jpg"
    bad_img.write_bytes(b"not-a-valid-jpeg-stream")

    manifests = tmp_path / "manifests"

    def _classify(relpath: str) -> tuple[str, str]:
        if "Augmentation" in relpath:
            return "pre_augmented", "quarantined-pre-augmented"
        return "original", "acquired-uninspected"

    summary = inventory_raw_dataset(
        dataset_id="DS9999",
        candidate_id="CAND9999",
        extracted_root=extracted,
        manifest_dir=manifests,
        classifier=_classify,
    )

    assert summary.total_scanned_images == 3
    assert summary.active_raw_count == 1
    assert summary.quarantined_count == 1
    assert summary.decode_error_count == 1
    assert compute_file_hashes(Path(summary.manifest_path))["sha256"] == summary.manifest_sha256

    public_text = Path(summary.manifest_path).read_text(encoding="utf-8")
    assert "patient_alpha_001" not in public_text
    assert "corrupt_scan" not in public_text
    assert "aug_flip_001" not in public_text

    with Path(summary.manifest_path).open("r", encoding="utf-8", newline="") as handle:
        pub_rows = list(csv.DictReader(handle))
    by_status = {r["intake_status"]: r for r in pub_rows}
    assert by_status["acquired-uninspected"]["width"] == "64"
    assert by_status["acquired-uninspected"]["channels"] == "1"
    assert by_status["quarantined-pre-augmented"]["channels"] == "3"
    assert by_status["decode-error"]["decode_status"] == "error"
    assert by_status["decode-error"]["error_message"] != ""

    with Path(summary.restricted_linkage_path).open("r", encoding="utf-8", newline="") as handle:
        link_rows = list(csv.DictReader(handle))
    relpaths = {r["original_relpath"] for r in link_rows}
    assert "Original_Images/patient_alpha_001.png" in relpaths
    assert "Original_Images/corrupt_scan.jpg" in relpaths
