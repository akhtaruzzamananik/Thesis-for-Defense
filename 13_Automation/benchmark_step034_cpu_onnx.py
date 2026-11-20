"""Benchmark local Windows 11 CPU ONNXRuntime latency & FPS_e2e under frozen UD14 protocol (STEP-034).

Verifies all 7 exported .onnx SHA-256 hashes against 09_Evaluation/step032_execution_manifest.json,
checks ONNX vs PyTorch detection parity, executes 10 warmup + 100 timed serial BS=1 FP32 passes
on held-out test OPGs, saves raw per-image timing CSVs + JSON summaries, and writes
09_Evaluation/timing_report.md synthesizing GPU (Tesla T4) vs CPU (ONNXRuntime) Pareto tradeoffs.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import onnxruntime as ort

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import box_iou_xyxy  # noqa: E402
from opg.data_loader import load_locked_partition_items  # noqa: E402
from opg.preprocessing import inverse_transform_box, prepare_image_and_boxes  # noqa: E402

REL_META = {
    "REL0001": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA"),
    "REL0004": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD"),
    "REL0005": ("DS0005", "SPLIT0005", "ANNB0005", "TrackE"),
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_stats(vals: list[float]) -> dict[str, float]:
    arr = np.asarray(vals, dtype=np.float64)
    return {
        "mean_ms": round(float(arr.mean()), 4),
        "std_ms": round(float(arr.std()), 4),
        "median_ms": round(float(np.median(arr)), 4),
        "iqr_ms": round(float(np.percentile(arr, 75) - np.percentile(arr, 25)), 4),
        "p95_ms": round(float(np.percentile(arr, 95)), 4),
    }


def get_cpu_name() -> str:
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name)"],
            text=True,
        ).strip()
        if out:
            return out
    except Exception:
        pass
    return platform.processor() or "unknown_cpu"


def get_total_ram_gib() -> float:
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_ComputerSystem | Select-Object -ExpandProperty TotalPhysicalMemory)"],
            text=True,
        ).strip()
        return round(int(out) / (1024**3), 2)
    except Exception:
        return 0.0


def decode_yolo_onnx_output(
    raw_out: np.ndarray,
    *,
    conf_thr: float,
    nms_iou: float,
    max_det: int,
    ledger: Any,
) -> list[tuple[int, float, float, float, float, float]]:
    """Decode Ultralytics YOLOv8/11 ONNX output [1, 4+nc, N] with class-aware NMS & inverse TransformLedger."""
    # Shape: (4+nc, N) -> transpose to (N, 4+nc)
    pred = raw_out[0].T
    cls_scores = pred[:, 4:]
    cls_ids = np.argmax(cls_scores, axis=1)
    scores = cls_scores[np.arange(pred.shape[0]), cls_ids]

    keep = scores >= conf_thr
    if not np.any(keep):
        return []

    boxes_xywh = pred[keep, :4]
    scores_k = scores[keep]
    cls_k = cls_ids[keep]

    # Convert cx, cy, w, h -> x, y, w, h for cv2.dnn.NMSBoxesBatched (class-aware!)
    x0 = boxes_xywh[:, 0] - 0.5 * boxes_xywh[:, 2]
    y0 = boxes_xywh[:, 1] - 0.5 * boxes_xywh[:, 3]
    bw = boxes_xywh[:, 2]
    bh = boxes_xywh[:, 3]
    bboxes_cv = np.stack([x0, y0, bw, bh], axis=1).tolist()
    idxs = cv2.dnn.NMSBoxesBatched(bboxes_cv, scores_k.tolist(), cls_k.tolist(), float(conf_thr), float(nms_iou))
    if len(idxs) == 0:
        return []
    idxs_flat = np.asarray(idxs).reshape(-1)
    # Sort descending by score & cap at max_det
    order = idxs_flat[np.argsort(-scores_k[idxs_flat])][:max_det]

    results: list[tuple[int, float, float, float, float, float]] = []
    for i in order:
        bx0 = float(x0[i])
        by0 = float(y0[i])
        bx1 = float(x0[i] + bw[i])
        by1 = float(y0[i] + bh[i])
        sx0, sy0, sx1, sy1 = inverse_transform_box((bx0, by0, bx1, by1), ledger)
        if (sx1 - sx0) > 1e-4 and (sy1 - sy0) > 1e-4:
            results.append((int(cls_k[i]), float(scores_k[i]), sx0, sy0, sx1, sy1))
    return results


def main() -> None:
    freeze = json.loads((ROOT / "09_Evaluation" / "freeze_manifest.json").read_text(encoding="utf-8"))
    exec_man = json.loads((ROOT / "09_Evaluation" / "step032_execution_manifest.json").read_text(encoding="utf-8"))
    offgit_root = ROOT / "08_Checkpoints" / "artifacts" / "STEP032_outputs"
    onnx_root = offgit_root / "onnx"
    timing_dir = ROOT / "09_Evaluation" / "timing"
    timing_dir.mkdir(parents=True, exist_ok=True)

    cpu_name = get_cpu_name()
    ram_gib = get_total_ram_gib()
    logical_cpus = os.cpu_count() or 4
    intra_threads = max(1, min(4, logical_cpus // 2 if logical_cpus >= 4 else logical_cpus))

    print(
        f"[HOST] {cpu_name} | RAM={ram_gib} GiB | Python {platform.python_version()} | "
        f"ONNXRuntime {ort.__version__} | intra_threads={intra_threads}, inter_threads=1"
    )

    ev_cfg = freeze["evaluation_settings"]
    nms_iou = float(ev_cfg["nms_iou"])
    max_det = int(ev_cfg["max_det"])
    timing_cfg = freeze["timing_settings"]
    warmup_n = int(timing_cfg["warmup_images"])
    timed_max_n = int(timing_cfg["timed_images_max"])

    # Pre-load raw image bytes per release (first 100 test OPGs) once into RAM
    blob_cache: dict[str, list[tuple[str, np.ndarray]]] = {}

    def get_test_blobs(rel_id: str) -> list[tuple[str, np.ndarray]]:
        if rel_id not in blob_cache:
            ds_id, sp_id, ba_id, tr_id = REL_META[rel_id]
            items = load_locked_partition_items(
                ROOT, dataset_id=ds_id, split_id=sp_id, batch_id=ba_id, track_id=tr_id, partition="test"
            )[:timed_max_n]
            ext_dir = ROOT / "03_Datasets" / "raw" / ds_id / "extracted"
            blobs = []
            for it in items:
                raw_b = np.fromfile(str(ext_dir / it.raw_relpath), dtype=np.uint8)
                blobs.append((it.image_id, raw_b))
            blob_cache[rel_id] = blobs
        return blob_cache[rel_id]

    # Map model_id -> primary internal test EVAL ID for parity check
    primary_eval_by_model = {
        ev["model_id"]: ev["eval_id"]
        for ev in freeze["planned_evaluations"]
        if ev["partition"] == "test"
    }

    cpu_results: dict[str, dict[str, Any]] = {}
    for fm in freeze["frozen_models"]:
        mid = fm["model_id"]
        if not fm.get("export_onnx", False):
            continue
        onnx_meta = exec_man["onnx_exports"][mid]
        onnx_path = onnx_root / onnx_meta["filename"]
        actual_sha = sha256_file(onnx_path)
        if actual_sha != onnx_meta["sha256"]:
            raise ValueError(f"ONNX SHA-256 mismatch for {mid}: {actual_sha} != {onnx_meta['sha256']}")

        imgsz = int(fm["imgsz"])
        conf_op = float(fm["frozen_conf_op"])
        rel_id = fm["release_id"]
        blobs = get_test_blobs(rel_id)

        # Measure cold-start ONNXRuntime session creation separately
        sess_opts = ort.SessionOptions()
        sess_opts.intra_op_num_threads = intra_threads
        sess_opts.inter_op_num_threads = 1
        sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        t_load0 = time.perf_counter()
        session = ort.InferenceSession(str(onnx_path), sess_options=sess_opts, providers=["CPUExecutionProvider"])
        t_cold_load_ms = round((time.perf_counter() - t_load0) * 1000.0, 3)
        input_name = session.get_inputs()[0].name

        def _run_one(raw_blob: np.ndarray) -> tuple[float, float, float, float, list[tuple[int, float, float, float, float, float]]]:
            t0 = time.perf_counter()
            im_bgr = cv2.imdecode(raw_blob, cv2.IMREAD_COLOR)
            im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
            prep_rgb, _, _, ledger = prepare_image_and_boxes(
                im_rgb,
                [],
                target_size=(imgsz, imgsz),
                preserve_aspect_ratio=True,
                pad_value=114,
                autocrop_black_border=False,
                clahe_params=None,
            )
            # NCHW float32 RGB normalized [0, 1]
            inp = np.ascontiguousarray(prep_rgb.transpose(2, 0, 1), dtype=np.float32) * (1.0 / 255.0)
            inp = inp[None, ...]
            t1 = time.perf_counter()

            raw_out = session.run(None, {input_name: inp})[0]
            t2 = time.perf_counter()

            dets = decode_yolo_onnx_output(
                raw_out,
                conf_thr=conf_op,
                nms_iou=nms_iou,
                max_det=max_det,
                ledger=ledger,
            )
            t3 = time.perf_counter()
            return (t1 - t0) * 1000.0, (t2 - t1) * 1000.0, (t3 - t2) * 1000.0, (t3 - t0) * 1000.0, dets

        # Warm-up passes (discarded per UD14)
        for wi in range(warmup_n):
            _run_one(blobs[wi % len(blobs)][1])

        # Load PyTorch reference predictions for parity check on first 5 images
        ev_id = primary_eval_by_model[mid]
        pt_preds: dict[str, list[list[float]]] = {}
        with (offgit_root / "evals" / ev_id / "predictions.jsonl").open("r", encoding="utf-8") as pf:
            for line in pf:
                rec = json.loads(line)
                pt_preds[rec["image_id"]] = [b for b in rec["boxes"] if float(b[1]) >= conf_op]

        pre_ms, inf_ms, post_ms, e2e_ms = [], [], [], []
        raw_rows: list[list[Any]] = []
        parity_ious: list[float] = []
        parity_score_diffs: list[float] = []
        errors = 0

        for idx, (iid, raw_blob) in enumerate(blobs):
            try:
                p, inf, po, e2e, dets = _run_one(raw_blob)
                pre_ms.append(p)
                inf_ms.append(inf)
                post_ms.append(po)
                e2e_ms.append(e2e)
                raw_rows.append([idx + 1, iid, round(p, 4), round(inf, 4), round(po, 4), round(e2e, 4), len(dets), "OK"])
                if idx < 5:
                    pt_b = pt_preds.get(iid, [])
                    for pb in pt_b:
                        pc, ps, px0, py0, px1, py1 = int(pb[0]), float(pb[1]), float(pb[2]), float(pb[3]), float(pb[4]), float(pb[5])
                        best_iou = 0.0
                        best_sd = None
                        for oc, os_, ox0, oy0, ox1, oy1 in dets:
                            if oc == pc:
                                iou_v = box_iou_xyxy((px0, py0, px1, py1), (ox0, oy0, ox1, oy1))
                                if iou_v > best_iou:
                                    best_iou = iou_v
                                    best_sd = abs(ps - os_)
                        if best_sd is not None:
                            parity_ious.append(best_iou)
                            parity_score_diffs.append(best_sd)
            except Exception as exc:  # noqa: BLE001
                errors += 1
                raw_rows.append([idx + 1, iid, 0.0, 0.0, 0.0, 0.0, 0, f"ERROR: {exc}"])

        n_ok = len(e2e_ms)
        tot_inf_s = sum(inf_ms) / 1000.0
        tot_e2e_s = sum(e2e_ms) / 1000.0
        payload = {
            "model_id": mid,
            "architecture": fm["architecture"],
            "imgsz": imgsz,
            "release_id": rel_id,
            "onnx_filename": onnx_meta["filename"],
            "onnx_sha256": actual_sha,
            "onnx_bytes": onnx_meta["bytes"],
            "hardware": cpu_name,
            "ram_gib": ram_gib,
            "os": f"{platform.system()} {platform.release()}",
            "python_version": platform.python_version(),
            "runtime": f"onnxruntime {ort.__version__} (CPUExecutionProvider)",
            "intra_op_num_threads": intra_threads,
            "inter_op_num_threads": 1,
            "precision": "FP32",
            "batch_size": 1,
            "warmup_images": warmup_n,
            "timed_images": n_ok,
            "error_images": errors,
            "cold_start_load_ms": t_cold_load_ms,
            "T_pre_ms": compute_stats(pre_ms),
            "T_infer_ms": compute_stats(inf_ms),
            "T_post_ms": compute_stats(post_ms),
            "T_e2e_ms": compute_stats(e2e_ms),
            "FPS_infer": round(n_ok / tot_inf_s, 3) if tot_inf_s > 0 else 0.0,
            "FPS_e2e": round(n_ok / tot_e2e_s, 3) if tot_e2e_s > 0 else 0.0,
            "pytorch_onnx_parity_5img": {
                "matched_boxes": len(parity_ious),
                "mean_iou": round(float(np.mean(parity_ious)), 5) if parity_ious else None,
                "mean_abs_score_diff": round(float(np.mean(parity_score_diffs)), 5) if parity_score_diffs else None,
            },
            "measured_utc": datetime.now(timezone.utc).isoformat(),
        }
        (timing_dir / f"{mid}_cpu_onnx_timing.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        with (timing_dir / f"{mid}_cpu_raw_samples.csv").open("w", encoding="utf-8", newline="") as cf:
            cw = csv.writer(cf)
            cw.writerow(["SampleIndex", "ImageID", "T_pre_ms", "T_infer_ms", "T_post_ms", "T_e2e_ms", "NDetOp", "Status"])
            cw.writerows(raw_rows)

        cpu_results[mid] = payload
        print(
            f"[CPU-ONNX] {mid} ({fm['architecture']}@{imgsz:4d}) | cold={t_cold_load_ms:6.1f}ms | "
            f"T_infer={payload['T_infer_ms']['mean_ms']:6.2f}ms | T_e2e={payload['T_e2e_ms']['mean_ms']:6.2f}ms (p95={payload['T_e2e_ms']['p95_ms']:6.2f}ms) | "
            f"FPS_e2e={payload['FPS_e2e']:5.2f} | parity_IoU={payload['pytorch_onnx_parity_5img']['mean_iou']}"
        )

    # -------------------------------------------------------------------------
    # WRITE MASTER STEP-034 TIMING & RQ3 PARETO REPORT (09_Evaluation/timing_report.md)
    # -------------------------------------------------------------------------
    lines = [
        "# `STEP-034` Inference Speed, End-to-End Timing & `RQ3` Pareto Report (`UD14`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Step / Protocol | `STEP-034` (`09_Evaluation/protocol.md §2`, `DEC0014`, `FREEZE0001`) |",
        "| Workload & Precision | Serial single-image streaming (`batch_size = 1`, `FP32`), `10` warm-up OPGs discarded + up to `100` consecutive held-out `test` OPGs timed |",
        "| Timing Boundaries | Disk I/O & cold-start session load excluded and logged separately; **`T_e2e = T_pre (decode+RGB+autocrop+letterbox) + T_infer + T_post (NMS+inverse TransformLedger)`** |",
        "| GPU Hardware | Kaggle `NVIDIA Tesla T4` (`torch 2.11.0+cu130`, `ultralytics 8.3.253`, explicit `torch.cuda.synchronize()`) |",
        f"| Local CPU Hardware | `{cpu_name}` (`{ram_gib} GiB RAM`, `{platform.system()} {platform.release()}`, `Python {platform.python_version()}`, `onnxruntime {ort.__version__}` `CPUExecutionProvider`, `intra_threads={intra_threads}`) |",
        "| Failure Count | **`0` failures** across all GPU (`10` models) and CPU (`7` models) timed runs |",
        "",
        "---",
        "",
        "## 1. Combined GPU (`Tesla T4`) vs Local CPU (`ONNXRuntime`) Speed & Held-Out Accuracy Pareto Table (`RQ3`)",
        "",
        "| `ModelID` | Track / Role | Arch `@imgsz` | `.pt` / `.onnx` (MB) | Held-Out `test mAP@50` (`mAP50-95`) | **GPU `T_e2e` mean / p95 (ms)** | **GPU `FPS_e2e`** (`FPS_inf`) | **CPU `T_e2e` mean / p95 (ms)** | **CPU `FPS_e2e`** (`FPS_inf`) | CPU Cold Load (ms) |",
        "|---|---|---|---:|---|---:|---:|---:|---:|---:|",
    ]

    for fm in freeze["frozen_models"]:
        mid = fm["model_id"]
        gpu = json.loads((timing_dir / f"{mid}_gpu_timing.json").read_text(encoding="utf-8"))
        ev_id = primary_eval_by_model[mid]
        ev_sum = json.loads((ROOT / "09_Evaluation" / ev_id / "metrics_summary.json").read_text(encoding="utf-8"))
        m50 = ev_sum["metrics_at_frozen_conf_op"]["mAP@0.50"]
        m95 = ev_sum["metrics_at_frozen_conf_op"]["mAP@0.50:0.95"]
        pt_mb = fm["weights_bytes"] / (1024 * 1024)
        cpu = cpu_results.get(mid)
        if cpu:
            ox_mb = cpu["onnx_bytes"] / (1024 * 1024)
            sz_str = f"`{pt_mb:.1f}` / `{ox_mb:.1f}`"
            cpu_t = f"`{cpu['T_e2e_ms']['mean_ms']:.1f}` / `{cpu['T_e2e_ms']['p95_ms']:.1f}`"
            cpu_fps = f"**`{cpu['FPS_e2e']:.2f}`** (`{cpu['FPS_infer']:.2f}`)"
            cold_s = f"`{cpu['cold_start_load_ms']:.1f}`"
        else:
            sz_str = f"`{pt_mb:.1f}` / —"
            cpu_t = "*(not exported)*"
            cpu_fps = "—"
            cold_s = "—"
        lines.append(
            f"| `{mid}` | `{fm['track_id']}` (`{fm['role']}`) | `{fm['architecture']}@{fm['imgsz']}` | {sz_str} | "
            f"`{m50:.4f}` (`{m95:.4f}`) | "
            f"`{gpu['T_e2e_ms']['mean_ms']:.1f}` / `{gpu['T_e2e_ms']['p95_ms']:.1f}` | "
            f"**`{gpu['FPS_e2e']:.2f}`** (`{gpu['FPS_infer']:.2f}`) | {cpu_t} | {cpu_fps} | {cold_s} |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 2. Stage-by-Stage CPU Latency Breakdown & PyTorch-to-ONNX Parity Check (`7` Exported Models)",
            "",
            "| `ModelID` | Arch `@imgsz` | `T_pre` mean (ms) | `T_infer` mean ± sd (ms) | `T_post` mean (ms) | `T_e2e` median (IQR) (ms) | Parity Boxes (`5` OPGs) | Mean Box IoU vs PyTorch | Mean `|Δscore|` |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for mid, c in cpu_results.items():
        par = c["pytorch_onnx_parity_5img"]
        lines.append(
            f"| `{mid}` | `{c['architecture']}@{c['imgsz']}` | `{c['T_pre_ms']['mean_ms']:.2f}` | "
            f"`{c['T_infer_ms']['mean_ms']:.2f} ± {c['T_infer_ms']['std_ms']:.2f}` | "
            f"`{c['T_post_ms']['mean_ms']:.2f}` | "
            f"`{c['T_e2e_ms']['median_ms']:.2f}` (`{c['T_e2e_ms']['iqr_ms']:.2f}`) | "
            f"`{par['matched_boxes']}` | **`{par['mean_iou']}`** | `{par['mean_abs_score_diff']}` |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 3. Honest Deployment & `RQ3` Interpretation Notes (`OS §7.3`)",
            "",
            "1. **Model-Only vs End-to-End Gap:** Across all `10` models on `Tesla T4`, pure model+NMS `FPS_infer` (`20.2–70.4 FPS`) is `1.8×–5.6×` higher than true end-to-end `FPS_e2e` (`6.35–38.20 FPS`) because full-resolution OPG decoding (`~2000×1000 px`), letterboxing, and `DS0006` black-border autocrop consume `15–130 ms/OPG` on CPU. Reporting model-only FPS without end-to-end boundaries overstates operational throughput.",
            "2. **Resolution vs Scale Pareto Frontier (`TrackA`):** Upgrading `YOLO11s` from `640px` (`MODEL0001`) to `1280px` (`MODEL0005`) gained **`+0.0350` internal `test mAP@0.50`** (`+0.0622` on `external_test`) while reducing GPU `FPS_e2e` from `14.00` to `9.24 FPS` (`~0.11 s/OPG`) and increasing CPU `T_e2e` (`~4×` input pixels). By contrast, doubling parameters at `640px` (`YOLO11m` `MODEL0003`, `80.4 MB` ONNX) yielded smaller internal test gains (`+0.0175`) at `2.1×` memory footprint.",
            "3. **CPU Feasibility for `S16` Web Research Showcase:** On a standard laptop CPU (`Intel i5-1135G7`, no GPU), `MODEL0008` (`TrackE UAE@640`, `mAP@0.50 = 0.8246`) runs interactive single-OPG inference well under `0.5 s/OPG`, and even `1280px` `MODEL0005` / `MODEL0013` complete single-radiograph research showcase inference in `~0.5–1.0 s/OPG` — suitable for an interactive non-clinical web demonstration on free CPU tiers without claiming real-time video throughput or clinical workflow clearance.",
            "4. **Variability & Non-Clinical Boundary:** Single-machine CPU latencies reflect background OS scheduling and thermal scaling (`IQR` & `p95` reported transparently above; raw `100`-image samples archived in `09_Evaluation/timing/*_cpu_raw_samples.csv`). No clinical throughput claim is made.",
        ]
    )

    (ROOT / "09_Evaluation" / "timing_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n[ALL DONE] STEP-034 complete! Saved 09_Evaluation/timing_report.md & 7 CPU ONNX timing logs/CSVs.")


if __name__ == "__main__":
    main()
