"""Thin CLI entry point for STEP-025 pipeline validation, Kaggle bundle export, and training."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.data_loader import export_yolo_dataset_bundle, validate_experiment_config  # noqa: E402
from opg.trainer import train_registered_experiment  # noqa: E402


def _load_track_class_names(track_id: str) -> list[str]:
    classes_csv = ROOT / "04_Annotations" / "classes.csv"
    items: list[tuple[int, str]] = []
    with classes_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            t_idx = row["TrainingIndex"].strip()
            if t_idx.startswith(f"{track_id}:"):
                idx = int(t_idx.split(":", 1)[1])
                items.append((idx, row["Name"].strip()))
    items.sort(key=lambda x: x[0])
    return [name for _, name in items]


def main() -> None:
    parser = argparse.ArgumentParser(description="OPG YOLO Pipeline Thin CLI (STEP-025)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate-config", help="Validate an executable T14 experiment YAML")
    p_val.add_argument("--config", type=Path, required=True)

    p_exp = sub.add_parser("build-kaggle-bundle", help="Export PP####-prepared train/val YOLO bundle for Kaggle")
    p_exp.add_argument("--dataset-id", required=True)
    p_exp.add_argument("--split-id", required=True)
    p_exp.add_argument("--batch-id", required=True)
    p_exp.add_argument("--track-id", required=True)
    p_exp.add_argument("--pp-config", type=Path, required=True)
    p_exp.add_argument("--out-dir", type=Path, required=True)
    p_exp.add_argument("--max-items-per-partition", type=int, default=None)

    p_tr = sub.add_parser("train", help="Launch registered experiment training via Ultralytics")
    p_tr.add_argument("--config", type=Path, required=True)
    p_tr.add_argument("--data-yaml", type=Path, required=True)
    p_tr.add_argument("--out-dir", type=Path, required=True)
    p_tr.add_argument("--resume", type=Path, default=None)

    args = parser.parse_args()
    if args.cmd == "validate-config":
        cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
        validate_experiment_config(cfg, root=ROOT)
        print(f"CONFIG_VALID: {cfg['identity']['experiment_id']}")
    elif args.cmd == "build-kaggle-bundle":
        names = _load_track_class_names(args.track_id)
        manifest = export_yolo_dataset_bundle(
            ROOT,
            dataset_id=args.dataset_id,
            split_id=args.split_id,
            batch_id=args.batch_id,
            track_id=args.track_id,
            pp_config_path=args.pp_config,
            output_dir=args.out_dir,
            class_names=names,
            partitions=("train", "val"),
            allow_test_partition=False,
            max_items_per_partition=args.max_items_per_partition,
        )
        print(json.dumps(manifest, indent=2))
    elif args.cmd == "train":
        cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
        res = train_registered_experiment(
            cfg,
            args.data_yaml,
            args.out_dir,
            root=ROOT,
            resume_checkpoint=args.resume,
        )
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
