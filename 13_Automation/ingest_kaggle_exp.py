"""Ingest, verify SHA-256/hyperparameters, and archive any completed Kaggle STEP-030 experiment.

Usage:
    python 13_Automation/ingest_kaggle_exp.py --exp-id EXP0002 --source D:\\Downloads\\results
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify and ingest completed Kaggle experiment outputs")
    parser.add_argument("--exp-id", required=True, help="e.g. EXP0002")
    parser.add_argument("--source", type=Path, required=True, help="Extracted Kaggle output dir or .zip")
    args = parser.parse_args()

    exp_id = args.exp_id
    src = args.source
    temp_dir: Path | None = None
    if src.is_file() and src.suffix.lower() == ".zip":
        temp_dir = ROOT / "08_Checkpoints" / "artifacts" / f"_tmp_extract_{exp_id}"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(temp_dir)
        src = temp_dir

    # Auto-locate <EXP_ID>_run folder
    run_roots = list(src.rglob(f"{exp_id}_effective_manifest.json"))
    assert len(run_roots) == 1, f"Expected 1 {exp_id}_effective_manifest.json under {src}, found {run_roots}"
    git_src = run_roots[0].parent
    run_base = git_src.parent
    yolo_dir = run_base / exp_id

    exp_dir = ROOT / "07_Experiments" / exp_id
    cfg = yaml.safe_load((exp_dir / "config.yaml").read_text(encoding="utf-8"))
    man = json.loads((git_src / f"{exp_id}_effective_manifest.json").read_text(encoding="utf-8"))
    y_args = yaml.safe_load((git_src / "args.yaml").read_text(encoding="utf-8"))

    # 1. Config SHA (accept raw or LF-normalized bytes for Windows CRLF vs Kaggle Linux LF) & hyperparameter reconciliation
    cfg_bytes = (exp_dir / "config.yaml").read_bytes()
    cfg_sha_raw = hashlib.sha256(cfg_bytes).hexdigest()
    cfg_sha_lf = hashlib.sha256(cfg_bytes.replace(b"\r\n", b"\n")).hexdigest()
    assert man["config_sha256"] in {cfg_sha_raw, cfg_sha_lf}, (
        f"config_sha256 mismatch: raw={cfg_sha_raw} lf={cfg_sha_lf} != {man['config_sha256']}"
    )
    tr = cfg["training"]
    aug = tr["augmentations"]
    ev = cfg["evaluation"]
    checks = [
        ("model", y_args["model"], cfg["model"]["initial_weights"]),
        ("epochs", y_args["epochs"], tr["epochs"]),
        ("patience", y_args["patience"], tr["patience"]),
        ("batch", y_args["batch"], tr["batch_size"]),
        ("imgsz", y_args["imgsz"], tr["image_size"]),
        ("seed", y_args["seed"], tr["seed"]),
        ("deterministic", y_args["deterministic"], tr["deterministic"]),
        ("optimizer", y_args["optimizer"], tr["optimizer"]),
        ("lr0", float(y_args["lr0"]), float(tr["lr0"])),
        ("lrf", float(y_args["lrf"]), float(tr["lrf"])),
        ("fliplr", float(y_args["fliplr"]), float(aug["fliplr"])),
        ("flipud", float(y_args["flipud"]), float(aug["flipud"])),
        ("iou", float(y_args["iou"]), float(ev["nms_iou"])),
        ("max_det", y_args["max_det"], ev["max_detections"]),
    ]
    for k, a, b in checks:
        assert a == b, f"Hyperparameter mismatch on {k}: {a} != {b}"

    # 2. Verify & copy checkpoints + plots off-Git
    art_dir = ROOT / "08_Checkpoints" / "artifacts" / exp_id
    (art_dir / "weights").mkdir(parents=True, exist_ok=True)
    (art_dir / "plots").mkdir(parents=True, exist_ok=True)
    for role in ("best", "last"):
        w_src = yolo_dir / "weights" / f"{role}.pt"
        assert w_src.exists(), f"Missing {w_src}"
        w_sha = sha256_file(w_src)
        assert w_sha == man["checkpoints"][role]["sha256"], f"SHA mismatch for {role}.pt"
        shutil.copy2(w_src, art_dir / "weights" / f"{role}.pt")
        print(f"VERIFIED {exp_id} {role}.pt: sha256={w_sha} bytes={w_src.stat().st_size}")

    for ext in ("*.png", "*.jpg"):
        for img in yolo_dir.glob(ext):
            shutil.copy2(img, art_dir / "plots" / img.name)

    # 3. Copy Git-safe metadata
    for fn in ("results.csv", "args.yaml", f"{exp_id}_effective_manifest.json"):
        shutil.copy2(git_src / fn, exp_dir / fn)

    # 4. Parse results.csv
    rows = []
    with (exp_dir / "results.csv").open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = {k.strip(): v.strip() for k, v in r.items()}
            for v in row.values():
                assert math.isfinite(float(v)), f"Non-finite metric in {exp_id} results.csv!"
            rows.append(row)

    best_r = max(rows, key=lambda r: float(r["metrics/mAP50(B)"]))
    p = float(best_r["metrics/precision(B)"])
    rec = float(best_r["metrics/recall(B)"])
    f1 = 2 * p * rec / (p + rec) if (p + rec) > 0 else 0.0
    print(
        f"INGEST_G10_READY {exp_id}: epochs={len(rows)}/{tr['epochs']}, best_ep={best_r['epoch']}, "
        f"P={p:.4f}, R={rec:.4f}, F1={f1:.4f}, mAP50={float(best_r['metrics/mAP50(B)']):.4f}, "
        f"mAP50-95={float(best_r['metrics/mAP50-95(B)']):.4f}, time_s={float(rows[-1]['time']):.1f}"
    )

    if temp_dir is not None and temp_dir.exists():
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
