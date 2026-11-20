"""Build the single sealed final-test Kaggle bundle for STEP-032 after G11 PASS.

Verifies all 29 SHA-256 hashes in 09_Evaluation/freeze_manifest.json and G11=PASS,
then packages:
  - freeze_manifest.json
  - weights/MODEL####_best.pt (all 10 frozen checkpoints, bit-for-bit verified)
  - images/REL000X/{test,external_test}/{ImageID}.jpg (1,260 EXIF-stripped full-res OPGs, NO labels!)
  - bundle_index.json (image metadata & SHA-256 checksums for 100% blind coverage verification)

Output (off-Git): 08_Checkpoints/artifacts/kaggle_bundles/STEP032_SEALED_TEST_BUNDLE.zip
Git-safe ledger:  09_Evaluation/step032_bundle_manifest.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.data_loader import _is_g11_passed, load_locked_partition_items  # noqa: E402
from opg.preprocessing import standardize_channels_rgb  # noqa: E402


REL_META = {
    "REL0001": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA", ("test", "external_test")),
    "REL0002": ("DS0002", "SPLIT0002", "ANNB0002", "TrackB", ("test",)),
    "REL0003": ("DS0003", "SPLIT0003", "ANNB0003", "TrackC", ("test",)),
    "REL0004": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD", ("test",)),
    "REL0005": ("DS0005", "SPLIT0005", "ANNB0005", "TrackE", ("test",)),
    "REL0006": ("DS0006", "SPLIT0006", "ANNB0006", "TrackF", ("test",)),
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_freeze_manifest(manifest: dict[str, Any]) -> None:
    if not _is_g11_passed(ROOT):
        raise PermissionError("BLOCKED: G11 is NOT PASS in 01_Project_Management/gates.csv!")
    gh = manifest["governance_hashes"]
    checks = [
        (gh["class_map_path"], gh["class_map_sha256"]),
        (gh["protocol_path"], gh["protocol_sha256"]),
        (gh["experiment_plan_path"], gh["experiment_plan_sha256"]),
        (gh["evaluator_py_path"], gh["evaluator_py_sha256"]),
        (gh["preprocessing_py_path"], gh["preprocessing_py_sha256"]),
    ]
    for pp_info in gh["pp_configs"].values():
        checks.append((pp_info["path"], pp_info["sha256"]))
    for rid, info in manifest["releases"].items():
        checks.append((f"03_Datasets/splits/{info['split_id']}/manifest.csv", info["split_manifest_csv_sha256"]))
        checks.append((f"05_Preprocessing/processed/{rid}/release_manifest.json", info["release_manifest_sha256"]))
    for fm in manifest["frozen_models"]:
        checks.append((fm["weights_relpath"], fm["weights_sha256"]))

    for rel_path, expected in checks:
        actual = sha256_file(ROOT / rel_path)
        if actual != expected:
            raise ValueError(f"FREEZE SHA-256 MISMATCH for {rel_path}: {actual} != {expected}")
    print(f"[OK] Verified {len(checks)}/{len(checks)} freeze_manifest.json SHA-256 hashes bit-for-bit.")


def main() -> None:
    freeze_path = ROOT / "09_Evaluation" / "freeze_manifest.json"
    manifest = json.loads(freeze_path.read_text(encoding="utf-8"))
    verify_freeze_manifest(manifest)

    out_dir = ROOT / "08_Checkpoints" / "artifacts" / "kaggle_bundles"
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / "STEP032_SEALED_TEST_BUNDLE.zip"

    bundle_index: dict[str, Any] = {
        "schema_version": "1.0.0",
        "freeze_id": manifest["freeze_id"],
        "freeze_manifest_sha256": sha256_file(freeze_path),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "blind_inference_only": True,
        "labels_included": False,
        "weights": {},
        "partitions": {},
    }

    total_images = 0
    # Use ZIP_STORED because .pt (zip) and .jpg are already compressed -> fast & clean
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_STORED) as zf:
        zf.write(freeze_path, arcname="freeze_manifest.json")

        # 1. Pack all 10 frozen best.pt weights
        for fm in manifest["frozen_models"]:
            mid = fm["model_id"]
            src_w = ROOT / fm["weights_relpath"]
            arc_w = f"weights/{mid}_best.pt"
            zf.write(src_w, arcname=arc_w)
            bundle_index["weights"][mid] = {
                "arcname": arc_w,
                "sha256": fm["weights_sha256"],
                "bytes": fm["weights_bytes"],
                "experiment_id": fm["experiment_id"],
                "checkpoint_id": fm["checkpoint_id"],
            }
        print(f"[OK] Packed {len(manifest['frozen_models'])} frozen model checkpoints.")

        # 2. Pack all 1,260 EXIF-stripped full-resolution test & external_test images (NO labels!)
        for rid, (ds_id, sp_id, ba_id, tr_id, parts) in REL_META.items():
            ext_dir = ROOT / "03_Datasets" / "raw" / ds_id / "extracted"
            for part in parts:
                items = load_locked_partition_items(
                    ROOT,
                    dataset_id=ds_id,
                    split_id=sp_id,
                    batch_id=ba_id,
                    track_id=tr_id,
                    partition=part,
                    allow_test_partition=False,  # Enforces live G11=PASS check
                )
                expected_n = (
                    manifest["releases"][rid]["test_images"]
                    if part == "test"
                    else manifest["releases"][rid]["external_test_images"]
                )
                if len(items) != expected_n:
                    raise RuntimeError(f"Count mismatch for {rid}/{part}: {len(items)} != {expected_n}")

                key = f"{rid}:{part}"
                records = []
                for it in items:
                    raw_path = ext_dir / it.raw_relpath
                    raw_bytes = np.fromfile(str(raw_path), dtype=np.uint8)
                    im_bgr = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
                    if im_bgr is None:
                        raise RuntimeError(f"Failed to decode {raw_path}")
                    im_rgb = standardize_channels_rgb(cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB))
                    h, w = im_rgb.shape[:2]
                    if (w, h) != (it.width, it.height):
                        raise ValueError(f"Dimension mismatch for {it.image_id}: {(w, h)} != {(it.width, it.height)}")

                    # Re-encode clean EXIF/XMP-free full-resolution JPEG-95
                    ok, enc = cv2.imencode(
                        ".jpg",
                        cv2.cvtColor(im_rgb, cv2.COLOR_RGB2BGR),
                        [int(cv2.IMWRITE_JPEG_QUALITY), 95],
                    )
                    if not ok:
                        raise RuntimeError(f"JPEG encode failed for {it.image_id}")
                    jpg_bytes = enc.tobytes()
                    arc_img = f"images/{rid}/{part}/{it.image_id}.jpg"
                    zf.writestr(arc_img, jpg_bytes)
                    records.append(
                        {
                            "image_id": it.image_id,
                            "dataset_id": ds_id,
                            "release_id": rid,
                            "split_id": sp_id,
                            "group_id": it.group_id,
                            "partition": part,
                            "src_width": it.width,
                            "src_height": it.height,
                            "raw_sha256": it.sha256,
                            "bundle_img_relpath": arc_img,
                            "bundle_img_sha256": sha256_bytes(jpg_bytes),
                        }
                    )
                    total_images += 1
                bundle_index["partitions"][key] = records
                print(f"[OK] Packed {rid} {part}: {len(records)} EXIF-free full-res OPGs.")

        idx_bytes = json.dumps(bundle_index, indent=2).encode("utf-8")
        zf.writestr("bundle_index.json", idx_bytes)

    zip_sha = sha256_file(zip_path)
    zip_mb = round(zip_path.stat().st_size / (1024 * 1024), 2)

    git_manifest = {
        "schema_version": "1.0.0",
        "step": "STEP-032",
        "freeze_id": manifest["freeze_id"],
        "freeze_manifest_sha256": bundle_index["freeze_manifest_sha256"],
        "created_utc": bundle_index["created_utc"],
        "off_git_bundle_path": "08_Checkpoints/artifacts/kaggle_bundles/STEP032_SEALED_TEST_BUNDLE.zip",
        "bundle_sha256": zip_sha,
        "bundle_bytes": zip_path.stat().st_size,
        "bundle_mb": zip_mb,
        "blind_inference_only": True,
        "labels_included": False,
        "total_frozen_models": len(manifest["frozen_models"]),
        "total_test_images": sum(
            len(v) for k, v in bundle_index["partitions"].items() if k.endswith(":test")
        ),
        "total_external_test_images": sum(
            len(v) for k, v in bundle_index["partitions"].items() if k.endswith(":external_test")
        ),
        "partition_counts": {k: len(v) for k, v in bundle_index["partitions"].items()},
    }
    git_manifest_path = ROOT / "09_Evaluation" / "step032_bundle_manifest.json"
    git_manifest_path.write_text(json.dumps(git_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\n[DONE] Bundle written: {zip_path} ({zip_mb} MB, sha256={zip_sha[:16]}...)")
    print(f"[DONE] Total images packed: {total_images} (1082 test + 178 external_test)")
    print(f"[DONE] Git manifest saved: {git_manifest_path}")


if __name__ == "__main__":
    main()
