"""Ultralytics YOLO training, effective-config capture, and UD14 timing wrapper (STEP-025)."""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Sequence

import numpy as np

from opg.data_loader import validate_experiment_config


def capture_git_revision(root: Path) -> str:
    """Return current 40-char git HEAD commit SHA or 'unknown'."""
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(root), text=True).strip()
    except Exception:
        return "unknown"


def train_registered_experiment(
    config: dict[str, Any],
    data_yaml_path: Path,
    output_dir: Path,
    *,
    root: Path | None = None,
    resume_checkpoint: Path | None = None,
) -> dict[str, Any]:
    """Validate T14 config, capture effective settings, and run Ultralytics YOLO training on train/val only."""
    validate_experiment_config(config, root=root)
    if not data_yaml_path.is_file():
        raise FileNotFoundError(f"Missing dataset.yaml: {data_yaml_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    exp_id = str(config["identity"]["experiment_id"])
    tr = config["training"]
    md = config["model"]

    # Lazy import so CPU-only data/eval tests work without torch/ultralytics installed
    from ultralytics import YOLO  # type: ignore

    weights_target = str(resume_checkpoint) if resume_checkpoint is not None else str(md["initial_weights"])
    model = YOLO(weights_target)

    train_kwargs: dict[str, Any] = {
        "data": str(data_yaml_path),
        "epochs": int(tr["epochs"]),
        "patience": int(tr["patience"]),
        "batch": int(tr["batch_size"]),
        "imgsz": int(tr["image_size"]),
        "optimizer": str(tr["optimizer"]),
        "lr0": float(tr["lr0"]),
        "lrf": float(tr["lrf"]),
        "momentum": float(tr["momentum"]),
        "weight_decay": float(tr["weight_decay"]),
        "warmup_epochs": float(tr["warmup_epochs"]),
        "seed": int(tr["seed"]),
        "deterministic": bool(tr["deterministic"]),
        "amp": bool(tr["amp"]),
        "workers": int(tr["workers"]),
        "degrees": float(tr["augmentations"]["degrees"]),
        "translate": float(tr["augmentations"]["translate"]),
        "scale": float(tr["augmentations"]["scale"]),
        "hsv_v": float(tr["augmentations"]["hsv_v"]),
        "fliplr": float(tr["augmentations"]["fliplr"]),
        "flipud": float(tr["augmentations"]["flipud"]),
        "mosaic": float(tr["augmentations"]["mosaic"]),
        "close_mosaic": int(tr["augmentations"]["close_mosaic"]),
        "project": str(output_dir),
        "name": exp_id,
        "exist_ok": True,
        "resume": resume_checkpoint is not None,
    }

    # Capture requested + effective configuration before launching
    effective_record = {
        "experiment_id": exp_id,
        "source_commit": capture_git_revision(root) if root is not None else config["identity"]["source_commit"],
        "weights_target": weights_target,
        "resume": resume_checkpoint is not None,
        "requested_train_kwargs": train_kwargs,
    }
    (output_dir / f"{exp_id}_effective_config.json").write_text(
        json.dumps(effective_record, indent=2), encoding="utf-8"
    )

    results = model.train(**train_kwargs)
    return {
        "experiment_id": exp_id,
        "save_dir": str(getattr(results, "save_dir", output_dir / exp_id)),
        "effective_config_path": str(output_dir / f"{exp_id}_effective_config.json"),
    }


def benchmark_inference_latency(
    items: Sequence[Any],
    preprocess_fn: Callable[[Any], Any],
    infer_fn: Callable[[Any], Any],
    postprocess_fn: Callable[[Any], Any],
    *,
    warmup_count: int = 10,
    sync_fn: Callable[[], None] | None = None,
) -> dict[str, Any]:
    """Measure serial batch=1 T_pre, T_infer, T_post, T_e2e, and FPS under UD14 protocol."""
    if not items:
        raise ValueError("items cannot be empty for latency benchmark")

    # Warm-up passes (excluded from timed statistics)
    for w_idx in range(min(warmup_count, len(items))):
        x = preprocess_fn(items[w_idx % len(items)])
        if sync_fn is not None:
            sync_fn()
        y = infer_fn(x)
        if sync_fn is not None:
            sync_fn()
        _ = postprocess_fn(y)

    t_pre_ms: list[float] = []
    t_inf_ms: list[float] = []
    t_post_ms: list[float] = []
    t_e2e_ms: list[float] = []

    for item in items:
        t0 = time.perf_counter()
        x = preprocess_fn(item)
        if sync_fn is not None:
            sync_fn()
        t1 = time.perf_counter()
        y = infer_fn(x)
        if sync_fn is not None:
            sync_fn()
        t2 = time.perf_counter()
        _ = postprocess_fn(y)
        t3 = time.perf_counter()

        pre_ms = (t1 - t0) * 1000.0
        inf_ms = (t2 - t1) * 1000.0
        post_ms = (t3 - t2) * 1000.0
        e2e_ms = (t3 - t0) * 1000.0
        t_pre_ms.append(pre_ms)
        t_inf_ms.append(inf_ms)
        t_post_ms.append(post_ms)
        t_e2e_ms.append(e2e_ms)

    def _stats(vals: list[float]) -> dict[str, float]:
        arr = np.asarray(vals, dtype=np.float64)
        return {
            "mean_ms": round(float(arr.mean()), 4),
            "std_ms": round(float(arr.std()), 4),
            "median_ms": round(float(np.median(arr)), 4),
            "iqr_ms": round(float(np.percentile(arr, 75) - np.percentile(arr, 25)), 4),
            "p95_ms": round(float(np.percentile(arr, 95)), 4),
        }

    tot_inf_s = sum(t_inf_ms) / 1000.0
    tot_e2e_s = sum(t_e2e_ms) / 1000.0
    n = len(items)
    return {
        "n_timed_images": n,
        "warmup_count": min(warmup_count, n),
        "T_preprocess": _stats(t_pre_ms),
        "T_infer": _stats(t_inf_ms),
        "T_postprocess": _stats(t_post_ms),
        "T_e2e": _stats(t_e2e_ms),
        "FPS_infer": round(n / tot_inf_s, 2) if tot_inf_s > 0 else None,
        "FPS_e2e": round(n / tot_e2e_s, 2) if tot_e2e_s > 0 else None,
    }
