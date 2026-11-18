"""Turnkey Kaggle GPU Training & Artifact Capture Script for Registered T14 Experiments (STEP-028).

Usage on Kaggle (after uploading EXP0001_REL0001_PP0001_bundle.zip & EXP0001/config.yaml):
    pip install -q ultralytics==8.3.253
    python kaggle_train_exp.py \
        --config EXP0001_config.yaml \
        --data-yaml /kaggle/input/exp0001-rel0001-pp0001-bundle/dataset.yaml \
        --work-dir /kaggle/working/EXP0001_run

If resuming an interrupted run:
    python kaggle_train_exp.py \
        --config EXP0001_config.yaml \
        --data-yaml /kaggle/input/exp0001-rel0001-pp0001-bundle/dataset.yaml \
        --work-dir /kaggle/working/EXP0001_run \
        --resume /kaggle/input/exp0001-ckpt-backup/last.pt
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute registered T14 experiment on Kaggle GPU (STEP-028)")
    parser.add_argument("--config", type=Path, required=True, help="Path to registered EXP####/config.yaml")
    parser.add_argument("--data-yaml", type=Path, required=True, help="Path to dataset.yaml inside Kaggle input")
    parser.add_argument("--work-dir", type=Path, default=Path("/kaggle/working/exp_run"))
    parser.add_argument("--resume", type=Path, default=None, help="Optional last.pt to resume an interrupted run")
    args = parser.parse_args()

    import torch
    import ultralytics
    from ultralytics import YOLO

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    exp_id = cfg["identity"]["experiment_id"]
    expected_pkg = cfg["model"]["package_version"]
    assert ultralytics.__version__ == expected_pkg, (
        f"Environment lock mismatch: expected ultralytics=={expected_pkg}, got {ultralytics.__version__}"
    )

    # Guard against sealed test partition access
    allowed = list(cfg["data"]["allowed_partitions"])
    assert "test" not in allowed and "external_test" not in allowed, "SEALED TEST VIOLATION in config!"
    raw_data_yaml = yaml.safe_load(args.data_yaml.read_text(encoding="utf-8"))
    assert "test" not in raw_data_yaml, "SEALED TEST VIOLATION in dataset.yaml!"

    work_dir = args.work_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    # Point dataset.yaml to the Kaggle read-only input directory
    kaggle_data_yaml = work_dir / "kaggle_dataset.yaml"
    raw_data_yaml["path"] = str(args.data_yaml.resolve().parent)
    kaggle_data_yaml.write_text(yaml.safe_dump(raw_data_yaml, sort_keys=False), encoding="utf-8")

    tr = cfg["training"]
    aug = tr["augmentations"]
    ev = cfg["evaluation"]

    started_utc = datetime.now(timezone.utc).isoformat()
    if args.resume is not None:
        model = YOLO(str(args.resume))
        model.train(resume=True)
        run_mode = f"resumed_from:{args.resume}"
    else:
        weights_name = cfg["model"]["initial_weights"]
        model = YOLO(weights_name)
        model.train(
            data=str(kaggle_data_yaml),
            epochs=int(tr["epochs"]),
            patience=int(tr["patience"]),
            batch=int(tr["batch_size"]),
            imgsz=int(tr["image_size"]),
            seed=int(tr["seed"]),
            deterministic=bool(tr["deterministic"]),
            optimizer=str(tr["optimizer"]),
            lr0=float(tr["lr0"]),
            lrf=float(tr["lrf"]),
            momentum=float(tr["momentum"]),
            weight_decay=float(tr["weight_decay"]),
            warmup_epochs=float(tr["warmup_epochs"]),
            amp=bool(tr["amp"]),
            workers=int(tr["workers"]),
            iou=float(ev["nms_iou"]),
            max_det=int(ev["max_detections"]),
            degrees=float(aug["degrees"]),
            translate=float(aug["translate"]),
            scale=float(aug["scale"]),
            hsv_v=float(aug["hsv_v"]),
            fliplr=float(aug["fliplr"]),
            flipud=float(aug["flipud"]),
            mosaic=float(aug["mosaic"]),
            close_mosaic=int(aug["close_mosaic"]),
            project=str(work_dir),
            name=exp_id,
            exist_ok=True,
        )
        run_mode = "fresh_start"
    finished_utc = datetime.now(timezone.utc).isoformat()

    run_dir = work_dir / exp_id
    weights_dir = run_dir / "weights"
    best_pt = weights_dir / "best.pt"
    last_pt = weights_dir / "last.pt"

    # Package Git-safe metadata separately from off-Git binary weights
    git_export = work_dir / f"{exp_id}_for_git"
    git_export.mkdir(parents=True, exist_ok=True)
    for fname in ("results.csv", "args.yaml"):
        src = run_dir / fname
        if src.exists():
            shutil.copy2(src, git_export / fname)

    ckpt_manifest = {
        "experiment_id": exp_id,
        "run_mode": run_mode,
        "started_utc": started_utc,
        "finished_utc": finished_utc,
        "config_sha256": sha256_file(args.config),
        "ultralytics_version": ultralytics.__version__,
        "torch_version": torch.__version__,
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "checkpoints": {},
    }
    for role, p in (("best", best_pt), ("last", last_pt)):
        if p.exists():
            ckpt_manifest["checkpoints"][role] = {
                "filename": p.name,
                "sha256": sha256_file(p),
                "bytes": p.stat().st_size,
            }

    (git_export / f"{exp_id}_effective_manifest.json").write_text(
        json.dumps(ckpt_manifest, indent=2), encoding="utf-8"
    )
    print(json.dumps(ckpt_manifest, indent=2))


if __name__ == "__main__":
    main()
