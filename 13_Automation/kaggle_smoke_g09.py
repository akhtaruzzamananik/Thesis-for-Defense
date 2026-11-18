"""Kaggle GPU G09 Smoke & Checkpoint Recovery Verification Script (STEP-026).

Usage on Kaggle (after uploading EXP0000_SMOKE_bundle.zip as a Kaggle Dataset):
    pip install -q ultralytics==8.3.253
    python kaggle_smoke_g09.py --data-yaml /kaggle/input/exp0000-smoke-bundle/dataset.yaml --work-dir /kaggle/working/g09_smoke

Outputs a JSON audit report (`EXP0000_SMOKE_g09_report.json`) and backup checkpoint
hashes to bring back into `08_Checkpoints/manifests/` for G09 sign-off.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import time
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP0000_SMOKE G09 recovery check on Kaggle GPU")
    parser.add_argument("--data-yaml", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, default=Path("/kaggle/working/g09_smoke"))
    parser.add_argument("--weights", default="yolo11s.pt")
    args = parser.parse_args()

    import torch
    import ultralytics
    from ultralytics import YOLO

    assert ultralytics.__version__ == "8.3.253", f"Expected ultralytics==8.3.253, got {ultralytics.__version__}"
    work_dir = args.work_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    backup_dir = work_dir / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Fix dataset.yaml path for Kaggle read-only input directory
    data_root = args.data_yaml.resolve().parent
    kaggle_data_yaml = work_dir / "kaggle_dataset.yaml"
    raw_yaml = args.data_yaml.read_text(encoding="utf-8")
    lines = [ln if not ln.startswith("path:") else f"path: {data_root}" for ln in raw_yaml.splitlines()]
    kaggle_data_yaml.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Phase 1: Run 1 epoch, simulate interruption, capture state & backup hash
    run_dir = work_dir / "exp0000_smoke"
    if run_dir.exists():
        shutil.rmtree(run_dir)

    def stop_after_epoch_1(trainer) -> None:
        if trainer.epoch == 0:
            # Epoch 0 (1st epoch) just finished and saved last.pt
            trainer.stop = True

    m1 = YOLO(args.weights)
    m1.add_callback("on_fit_epoch_end", stop_after_epoch_1)
    m1.train(
        data=str(kaggle_data_yaml),
        epochs=2,
        imgsz=640,
        batch=8,
        seed=20261124,
        deterministic=True,
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.01,
        amp=True,
        workers=2,
        project=str(work_dir),
        name="exp0000_smoke",
        exist_ok=True,
    )

    last_pt = run_dir / "weights" / "last.pt"
    assert last_pt.exists(), f"Missing {last_pt}"
    ckpt_ep1 = torch.load(last_pt, map_location="cpu", weights_only=False)
    ep1_epoch_val = int(ckpt_ep1.get("epoch", -999))
    has_optimizer = ckpt_ep1.get("optimizer") is not None
    has_ema = ckpt_ep1.get("ema") is not None
    last_sha_orig = sha256_file(last_pt)

    # Backup copy + retrieval hash check
    backup_pt = backup_dir / "EXP0000_SMOKE_RUN0001_epoch001_last.pt"
    shutil.copy2(last_pt, backup_pt)
    backup_sha = sha256_file(backup_pt)
    assert last_sha_orig == backup_sha, "Backup SHA-256 mismatch!"

    # Phase 2: Restore from backup checkpoint & resume to epoch 2
    restored_pt = work_dir / "restored_last.pt"
    shutil.copy2(backup_pt, restored_pt)
    assert sha256_file(restored_pt) == backup_sha

    m2 = YOLO(str(restored_pt))
    m2.train(resume=True)

    final_last = run_dir / "weights" / "last.pt"
    final_best = run_dir / "weights" / "best.pt"
    ckpt_ep2 = torch.load(final_last, map_location="cpu", weights_only=False)

    # Phase 3: Validation + single-image serial latency smoke check
    val_res = YOLO(str(final_best if final_best.exists() else final_last)).val(
        data=str(kaggle_data_yaml), imgsz=640, batch=8, conf=0.001, iou=0.65, max_det=300
    )
    map50 = float(val_res.box.map50)
    map50_95 = float(val_res.box.map)
    assert math.isfinite(map50) and math.isfinite(map50_95), "Non-finite validation metrics!"

    val_imgs = sorted((data_root / "images" / "val").glob("*"))[:5]
    eval_model = YOLO(str(final_best if final_best.exists() else final_last))
    t0 = time.perf_counter()
    for p in val_imgs:
        eval_model.predict(source=str(p), imgsz=640, conf=0.25, iou=0.65, verbose=False)
    elapsed = time.perf_counter() - t0

    report = {
        "experiment_id": "EXP0000_SMOKE",
        "purpose": "diagnostic_smoke_G09_not_reportable",
        "ultralytics_version": ultralytics.__version__,
        "torch_version": torch.__version__,
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "phase1_epoch1_saved_epoch_field": ep1_epoch_val,
        "phase1_has_optimizer_state": has_optimizer,
        "phase1_has_ema_state": has_ema,
        "phase1_last_pt_sha256": last_sha_orig,
        "backup_retrieval_sha256": backup_sha,
        "backup_hash_match": last_sha_orig == backup_sha,
        "phase2_resumed_final_epoch_field": int(ckpt_ep2.get("epoch", -999)),
        "val_map50_finite": map50,
        "val_map50_95_finite": map50_95,
        "smoke_e2e_fps_5imgs": round(len(val_imgs) / max(elapsed, 1e-9), 2),
        "best_pt_sha256": sha256_file(final_best) if final_best.exists() else None,
        "exact_resume_note": "Restores epoch, model, EMA, and AdamW optimizer state; dataloader RNG is not bit-identical.",
    }
    report_path = work_dir / "EXP0000_SMOKE_g09_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
