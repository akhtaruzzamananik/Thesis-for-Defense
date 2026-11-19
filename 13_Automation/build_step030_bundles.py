"""Build unique Kaggle train/val .zip bundles off-Git for STEP-030 (EXP0002-EXP0013).

Usage:
    python 13_Automation/build_step030_bundles.py --bundles REL0001_PP0004 REL0002_PP0001
    python 13_Automation/build_step030_bundles.py --all
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.data_loader import export_yolo_dataset_bundle  # noqa: E402

BUNDLE_SPECS = {
    "REL0001_PP0004": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA", "05_Preprocessing/configs/PP0004_highres_letterbox_1280.yaml"),
    "REL0001_PP0002": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA", "05_Preprocessing/configs/PP0002_clahe_2p0_8x8.yaml"),
    "REL0001_PP0003": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA", "05_Preprocessing/configs/PP0003_clahe_3p0_16x16.yaml"),
    "REL0002_PP0001": ("DS0002", "SPLIT0002", "ANNB0002", "TrackB", "05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml"),
    "REL0003_PP0001": ("DS0003", "SPLIT0003", "ANNB0003", "TrackC", "05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml"),
    "REL0003_PP0002": ("DS0003", "SPLIT0003", "ANNB0003", "TrackC", "05_Preprocessing/configs/PP0002_clahe_2p0_8x8.yaml"),
    "REL0004_PP0001": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD", "05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml"),
    "REL0004_PP0004": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD", "05_Preprocessing/configs/PP0004_highres_letterbox_1280.yaml"),
    "REL0005_PP0001": ("DS0005", "SPLIT0005", "ANNB0005", "TrackE", "05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml"),
    "REL0006_PP0001": ("DS0006", "SPLIT0006", "ANNB0006", "TrackF", "05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml"),
}


def load_track_names(track_id: str) -> list[str]:
    items: list[tuple[int, str]] = []
    with (ROOT / "04_Annotations" / "classes.csv").open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            t_idx = row["TrainingIndex"].strip()
            if t_idx.startswith(f"{track_id}:"):
                items.append((int(t_idx.split(":", 1)[1]), row["Name"].strip()))
    items.sort(key=lambda x: x[0])
    return [name for _, name in items]


def build_one(key: str) -> dict:
    ds_id, split_id, batch_id, track_id, pp_rel = BUNDLE_SPECS[key]
    out_root = ROOT / "08_Checkpoints" / "artifacts" / "kaggle_bundles"
    out_root.mkdir(parents=True, exist_ok=True)
    stage_dir = out_root / f"_stage_{key}"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)

    manifest = export_yolo_dataset_bundle(
        ROOT,
        dataset_id=ds_id,
        split_id=split_id,
        batch_id=batch_id,
        track_id=track_id,
        pp_config_path=ROOT / pp_rel,
        output_dir=stage_dir,
        class_names=load_track_names(track_id),
        partitions=("train", "val"),
        allow_test_partition=False,
    )
    zip_path = out_root / f"{key}_bundle.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(stage_dir.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(stage_dir))
    shutil.rmtree(stage_dir)
    mb = zip_path.stat().st_size / 1e6
    rec = {"bundle": zip_path.name, "zip_mb": round(mb, 2), "partitions": manifest["partitions"]}
    print(f"BUILT_BUNDLE: {json.dumps(rec)}", flush=True)
    return rec


def main() -> None:
    parser = argparse.ArgumentParser(description="Build STEP-030 Kaggle train/val zip bundles")
    parser.add_argument("--bundles", nargs="*", choices=list(BUNDLE_SPECS.keys()))
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    targets = list(BUNDLE_SPECS.keys()) if args.all else (args.bundles or [])
    assert targets, "Specify --all or --bundles <keys>"
    summary = [build_one(k) for k in targets]
    (ROOT / "08_Checkpoints" / "artifacts" / "kaggle_bundles" / "bundles_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
