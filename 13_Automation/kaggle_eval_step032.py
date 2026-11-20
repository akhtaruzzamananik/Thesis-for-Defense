"""Single-Pass Sealed Final-Test Inference, GPU Timing (UD14), and ONNX Export on Kaggle GPU (STEP-032).

Strictly verifies every hash in 09_Evaluation/freeze_manifest.json before running inference.
Produces:
  - evals/EVAL0001..EVAL0014/{predictions.jsonl, coverage.csv, eval_run_manifest.json}
  - xshift/<bridge_pass_key>/{predictions.jsonl, coverage.csv, xshift_run_manifest.json}
  - timing/MODEL####_gpu_timing.json (serial BS=1, FP32, 10 warmup + up to 100 timed OPGs, CUDA sync)
  - onnx/MODEL####.onnx (static opset=17 exports for local CPU timing & S16 demo)
  - step032_execution_manifest.json (complete provenance & SHA-256 checksums)
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_lf_normalized(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def verify_hash_accept_crlf(path: Path, expected: str, label: str) -> None:
    raw_h = sha256_file(path)
    lf_h = sha256_lf_normalized(path)
    if raw_h != expected and lf_h != expected:
        raise ValueError(f"FREEZE HASH MISMATCH [{label}] {path}: raw={raw_h}, lf={lf_h}, expected={expected}")


def compute_stats(vals_ms: list[float]) -> dict[str, float]:
    arr = np.asarray(vals_ms, dtype=np.float64)
    return {
        "mean_ms": round(float(arr.mean()), 4),
        "std_ms": round(float(arr.std()), 4),
        "median_ms": round(float(np.median(arr)), 4),
        "iqr_ms": round(float(np.percentile(arr, 75) - np.percentile(arr, 25)), 4),
        "p95_ms": round(float(np.percentile(arr, 95)), 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute frozen STEP-032 final-test evaluation on Kaggle GPU")
    parser.add_argument("--repo-root", type=Path, required=True, help="Cloned Thesis-for-Defense repo root")
    parser.add_argument("--bundle-dir", type=Path, required=True, help="Kaggle input directory containing bundle_index.json")
    parser.add_argument("--work-dir", type=Path, default=Path("/kaggle/working/STEP032_outputs"))
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    bundle_dir = args.bundle_dir.resolve()
    work_dir = args.work_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))

    from opg.preprocessing import inverse_transform_box, prepare_image_and_boxes  # noqa: E402
    import torch  # noqa: E402
    import ultralytics  # noqa: E402
    from ultralytics import YOLO  # noqa: E402

    assert ultralytics.__version__ == "8.3.253", f"Expected ultralytics==8.3.253, got {ultralytics.__version__}"
    device = 0 if torch.cuda.is_available() else "cpu"
    use_cuda = torch.cuda.is_available()
    cuda_name = torch.cuda.get_device_name(0) if use_cuda else "cpu"
    print(f"[ENV] ultralytics={ultralytics.__version__}, torch={torch.__version__}, device={cuda_name}")

    # -------------------------------------------------------------------------
    # 1. STRICT FREEZE VERIFICATION GATE (abort on any mismatch)
    # -------------------------------------------------------------------------
    repo_freeze_path = repo_root / "09_Evaluation" / "freeze_manifest.json"
    bundle_freeze_path = bundle_dir / "freeze_manifest.json"
    repo_freeze_lf = sha256_lf_normalized(repo_freeze_path)
    bundle_freeze_lf = sha256_lf_normalized(bundle_freeze_path)
    if repo_freeze_lf != bundle_freeze_lf:
        raise ValueError(f"freeze_manifest.json mismatch between repo ({repo_freeze_lf}) and bundle ({bundle_freeze_lf})")

    freeze = json.loads(repo_freeze_path.read_text(encoding="utf-8"))
    bundle_index = json.loads((bundle_dir / "bundle_index.json").read_text(encoding="utf-8"))
    assert bundle_index.get("labels_included") is False, "Blind inference bundle MUST NOT include labels!"

    gh = freeze["governance_hashes"]
    verify_hash_accept_crlf(repo_root / gh["class_map_path"], gh["class_map_sha256"], "classes.csv")
    verify_hash_accept_crlf(repo_root / gh["protocol_path"], gh["protocol_sha256"], "protocol.md")
    verify_hash_accept_crlf(repo_root / gh["experiment_plan_path"], gh["experiment_plan_sha256"], "experiment_plan.md")
    verify_hash_accept_crlf(repo_root / gh["evaluator_py_path"], gh["evaluator_py_sha256"], "evaluator.py")
    verify_hash_accept_crlf(repo_root / gh["preprocessing_py_path"], gh["preprocessing_py_sha256"], "preprocessing.py")
    for pp_id, pp_info in gh["pp_configs"].items():
        verify_hash_accept_crlf(repo_root / pp_info["path"], pp_info["sha256"], pp_id)

    models_by_id: dict[str, dict[str, Any]] = {}
    for fm in freeze["frozen_models"]:
        mid = fm["model_id"]
        w_path = bundle_dir / bundle_index["weights"][mid]["arcname"]
        actual_w_sha = sha256_file(w_path)
        if actual_w_sha != fm["weights_sha256"]:
            raise ValueError(f"WEIGHT SHA-256 MISMATCH for {mid}: {actual_w_sha} != {fm['weights_sha256']}")
        fm_copy = dict(fm)
        fm_copy["bundle_weight_path"] = w_path
        models_by_id[mid] = fm_copy
    print(f"[OK] Freeze gate PASSED: governance files + {len(models_by_id)}/10 model checkpoints verified bit-for-bit.")

    ev_cfg = freeze["evaluation_settings"]
    conf_floor = float(ev_cfg["metric_conf_floor"])
    nms_iou = float(ev_cfg["nms_iou"])
    agnostic_nms = bool(ev_cfg["agnostic_nms"])
    max_det = int(ev_cfg["max_det"])
    fallback_conf = float(ev_cfg["fallback_reference_conf"])

    timing_cfg = freeze["timing_settings"]
    warmup_n = int(timing_cfg["warmup_images"])
    timed_max_n = int(timing_cfg["timed_images_max"])

    # Helper to run single-pass blind inference for one (model, release, partition)
    def run_inference_pass(
        model: YOLO,
        fm: dict[str, Any],
        target_release: str,
        target_partition: str,
        out_subdir: Path,
        run_label: str,
    ) -> dict[str, Any]:
        out_subdir.mkdir(parents=True, exist_ok=True)
        part_key = f"{target_release}:{target_partition}"
        records = bundle_index["partitions"][part_key]
        imgsz = int(fm["imgsz"])
        conf_op = float(fm["frozen_conf_op"])
        model_nc = int(freeze["releases"][fm["release_id"]]["num_classes"])
        use_autocrop = target_release == "REL0006"

        pred_path = out_subdir / "predictions.jsonl"
        cov_path = out_subdir / "coverage.csv"

        ok_cnt = 0
        err_cnt = 0
        zero_floor_cnt = 0
        zero_op_cnt = 0
        total_boxes_floor = 0
        total_boxes_op = 0
        invalid_box_cnt = 0
        invalid_cls_cnt = 0

        t_start = datetime.now(timezone.utc).isoformat()
        with pred_path.open("w", encoding="utf-8") as pf, cov_path.open("w", encoding="utf-8", newline="") as cf:
            cw = csv.writer(cf)
            cw.writerow(
                [
                    "ImageID",
                    "GroupID",
                    "ReleaseID",
                    "Partition",
                    "SrcWidth",
                    "SrcHeight",
                    "Status",
                    "NPredFloor",
                    "NPredOp",
                    "NPred025",
                    "ErrorMsg",
                ]
            )
            for rec in records:
                iid = rec["image_id"]
                src_w = int(rec["src_width"])
                src_h = int(rec["src_height"])
                img_path = bundle_dir / rec["bundle_img_relpath"]
                try:
                    raw_b = np.fromfile(str(img_path), dtype=np.uint8)
                    im_bgr = cv2.imdecode(raw_b, cv2.IMREAD_COLOR)
                    if im_bgr is None:
                        raise RuntimeError(f"cv2.imdecode returned None for {img_path}")
                    im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
                    if (im_rgb.shape[1], im_rgb.shape[0]) != (src_w, src_h):
                        raise ValueError(f"Shape mismatch: {im_rgb.shape[:2]} vs {(src_h, src_w)}")

                    prep_rgb, _, _, ledger = prepare_image_and_boxes(
                        im_rgb,
                        [],
                        target_size=(imgsz, imgsz),
                        preserve_aspect_ratio=True,
                        pad_value=114,
                        autocrop_black_border=use_autocrop,
                        clahe_params=None,
                    )
                    prep_bgr = cv2.cvtColor(prep_rgb, cv2.COLOR_RGB2BGR)

                    res_list = model.predict(
                        source=prep_bgr,
                        imgsz=imgsz,
                        conf=conf_floor,
                        iou=nms_iou,
                        agnostic_nms=agnostic_nms,
                        max_det=max_det,
                        device=device,
                        half=False,
                        verbose=False,
                    )
                    r0 = res_list[0]
                    boxes_out: list[list[float]] = []
                    if r0.boxes is not None and len(r0.boxes) > 0:
                        xyxy_np = r0.boxes.xyxy.detach().cpu().numpy()
                        conf_np = r0.boxes.conf.detach().cpu().numpy()
                        cls_np = r0.boxes.cls.detach().cpu().numpy()
                        for b_xyxy, sc, c_raw in zip(xyxy_np, conf_np, cls_np):
                            cid = int(round(float(c_raw)))
                            score = float(sc)
                            if cid < 0 or cid >= model_nc:
                                invalid_cls_cnt += 1
                                continue
                            if not np.all(np.isfinite(b_xyxy)) or not np.isfinite(score):
                                invalid_box_cnt += 1
                                continue
                            sx0, sy0, sx1, sy1 = inverse_transform_box(b_xyxy.tolist(), ledger)
                            if (sx1 - sx0) <= 1e-4 or (sy1 - sy0) <= 1e-4:
                                invalid_box_cnt += 1
                                continue
                            boxes_out.append(
                                [
                                    cid,
                                    round(score, 6),
                                    round(sx0, 3),
                                    round(sy0, 3),
                                    round(sx1, 3),
                                    round(sy1, 3),
                                ]
                            )
                    # Deterministic descending sort by score
                    boxes_out.sort(key=lambda x: x[1], reverse=True)
                    boxes_out = boxes_out[:max_det]

                    n_floor = len(boxes_out)
                    n_op = sum(1 for b in boxes_out if b[1] >= conf_op)
                    n_025 = sum(1 for b in boxes_out if b[1] >= fallback_conf)
                    if n_floor == 0:
                        zero_floor_cnt += 1
                    if n_op == 0:
                        zero_op_cnt += 1
                    total_boxes_floor += n_floor
                    total_boxes_op += n_op
                    ok_cnt += 1

                    pf.write(
                        json.dumps(
                            {
                                "image_id": iid,
                                "group_id": rec["group_id"],
                                "src_width": src_w,
                                "src_height": src_h,
                                "boxes": boxes_out,
                            }
                        )
                        + "\n"
                    )
                    cw.writerow([iid, rec["group_id"], target_release, target_partition, src_w, src_h, "OK", n_floor, n_op, n_025, ""])
                except Exception as exc:  # noqa: BLE001
                    err_cnt += 1
                    pf.write(
                        json.dumps(
                            {
                                "image_id": iid,
                                "group_id": rec["group_id"],
                                "src_width": src_w,
                                "src_height": src_h,
                                "boxes": [],
                                "error": str(exc),
                            }
                        )
                        + "\n"
                    )
                    cw.writerow([iid, rec["group_id"], target_release, target_partition, src_w, src_h, "ERROR", 0, 0, 0, str(exc)])

        t_end = datetime.now(timezone.utc).isoformat()
        run_manifest = {
            "run_label": run_label,
            "model_id": fm["model_id"],
            "experiment_id": fm["experiment_id"],
            "checkpoint_id": fm["checkpoint_id"],
            "weights_sha256": fm["weights_sha256"],
            "model_release_id": fm["release_id"],
            "target_release_id": target_release,
            "target_partition": target_partition,
            "imgsz": imgsz,
            "preprocessing_id": fm["preprocessing_id"],
            "frozen_conf_op": conf_op,
            "metric_conf_floor": conf_floor,
            "nms_iou": nms_iou,
            "agnostic_nms": agnostic_nms,
            "max_det": max_det,
            "started_utc": t_start,
            "finished_utc": t_end,
            "total_intended_images": len(records),
            "ok_images": ok_cnt,
            "error_images": err_cnt,
            "coverage_pct": round(100.0 * ok_cnt / max(len(records), 1), 4),
            "zero_det_floor_images": zero_floor_cnt,
            "zero_det_op_images": zero_op_cnt,
            "total_boxes_floor": total_boxes_floor,
            "total_boxes_op": total_boxes_op,
            "invalid_box_count": invalid_box_cnt,
            "invalid_class_count": invalid_cls_cnt,
            "predictions_sha256": sha256_file(pred_path),
            "coverage_sha256": sha256_file(cov_path),
        }
        (out_subdir / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n", encoding="utf-8")
        print(
            f"[DONE] {run_label}: {fm['model_id']} -> {target_release}:{target_partition} | "
            f"OK={ok_cnt}/{len(records)} err={err_cnt} boxes@op={total_boxes_op} zero@op={zero_op_cnt}"
        )
        return run_manifest

    # Helper for UD14 GPU timing benchmark
    def run_gpu_timing(model: YOLO, fm: dict[str, Any], target_release: str, out_path: Path) -> dict[str, Any]:
        records = bundle_index["partitions"][f"{target_release}:test"]
        imgsz = int(fm["imgsz"])
        use_autocrop = target_release == "REL0006"
        timed_records = records[: min(timed_max_n, len(records))]

        # Pre-read file bytes into RAM so disk I/O is excluded per DEC0014 while JPEG decode + RGB + letterbox IS timed in T_pre
        raw_blobs = [np.fromfile(str(bundle_dir / r["bundle_img_relpath"]), dtype=np.uint8) for r in timed_records]

        def _one_step(blob: np.ndarray) -> tuple[float, float, float, float]:
            t0 = time.perf_counter()
            im_bgr = cv2.imdecode(blob, cv2.IMREAD_COLOR)
            im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
            prep_rgb, _, _, ledger = prepare_image_and_boxes(
                im_rgb,
                [],
                target_size=(imgsz, imgsz),
                preserve_aspect_ratio=True,
                pad_value=114,
                autocrop_black_border=use_autocrop,
                clahe_params=None,
            )
            prep_bgr = cv2.cvtColor(prep_rgb, cv2.COLOR_RGB2BGR)
            if use_cuda:
                torch.cuda.synchronize()
            t1 = time.perf_counter()

            res_list = model.predict(
                source=prep_bgr,
                imgsz=imgsz,
                conf=conf_floor,
                iou=nms_iou,
                agnostic_nms=agnostic_nms,
                max_det=max_det,
                device=device,
                half=False,
                verbose=False,
            )
            if use_cuda:
                torch.cuda.synchronize()
            t2 = time.perf_counter()

            r0 = res_list[0]
            if r0.boxes is not None and len(r0.boxes) > 0:
                xyxy_np = r0.boxes.xyxy.detach().cpu().numpy()
                for b_xyxy in xyxy_np:
                    _ = inverse_transform_box(b_xyxy.tolist(), ledger)
            t3 = time.perf_counter()
            return (t1 - t0) * 1000.0, (t2 - t1) * 1000.0, (t3 - t2) * 1000.0, (t3 - t0) * 1000.0

        # Warm-up passes (discarded)
        for wi in range(warmup_n):
            _one_step(raw_blobs[wi % len(raw_blobs)])

        pre_ms, inf_ms, post_ms, e2e_ms = [], [], [], []
        for blob in raw_blobs:
            p, i, po, e = _one_step(blob)
            pre_ms.append(p)
            inf_ms.append(i)
            post_ms.append(po)
            e2e_ms.append(e)

        n = len(raw_blobs)
        tot_inf_s = sum(inf_ms) / 1000.0
        tot_e2e_s = sum(e2e_ms) / 1000.0
        payload = {
            "model_id": fm["model_id"],
            "architecture": fm["architecture"],
            "imgsz": imgsz,
            "release_id": target_release,
            "hardware": cuda_name,
            "precision": "FP32",
            "batch_size": 1,
            "warmup_images": warmup_n,
            "timed_images": n,
            "cuda_synchronized": use_cuda,
            "T_pre_ms": compute_stats(pre_ms),
            "T_infer_with_ultralytics_nms_ms": compute_stats(inf_ms),
            "T_post_inv_ledger_ms": compute_stats(post_ms),
            "T_e2e_ms": compute_stats(e2e_ms),
            "FPS_infer": round(n / tot_inf_s, 3) if tot_inf_s > 0 else 0.0,
            "FPS_e2e": round(n / tot_e2e_s, 3) if tot_e2e_s > 0 else 0.0,
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(
            f"[TIMING] {fm['model_id']} ({fm['architecture']}@{imgsz}): "
            f"T_e2e={payload['T_e2e_ms']['mean_ms']:.2f} ms -> FPS_e2e={payload['FPS_e2e']:.2f} | "
            f"FPS_infer={payload['FPS_infer']:.2f}"
        )
        return payload

    # -------------------------------------------------------------------------
    # 2. EXECUTE ALL 14 PLANNED EVALS, 10 UNIQUE XSHIFT PASSES, TIMING & ONNX
    # -------------------------------------------------------------------------
    started_utc = datetime.now(timezone.utc).isoformat()
    exec_manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "step": "STEP-032",
        "freeze_id": freeze["freeze_id"],
        "freeze_manifest_sha256": repo_freeze_lf,
        "started_utc": started_utc,
        "ultralytics_version": ultralytics.__version__,
        "torch_version": torch.__version__,
        "hardware": cuda_name,
        "evals": {},
        "xshift_passes": {},
        "gpu_timing": {},
        "onnx_exports": {},
    }

    # Group work by model_id so each model is loaded onto GPU exactly once
    evals_by_model: dict[str, list[dict[str, Any]]] = {}
    for ev in freeze["planned_evaluations"]:
        evals_by_model.setdefault(ev["model_id"], []).append(ev)

    # Deduplicate cross-cohort inference passes by (source_model_id, target_release_id, target_partition)
    xshift_by_model: dict[str, dict[tuple[str, str], list[str]]] = {}
    for br in freeze["cross_cohort_bridges"]:
        mid = br["source_model_id"]
        key = (br["target_release_id"], br["target_partition"])
        xshift_by_model.setdefault(mid, {}).setdefault(key, []).append(br["bridge_id"])

    onnx_dir = work_dir / "onnx"
    onnx_dir.mkdir(parents=True, exist_ok=True)

    for fm in freeze["frozen_models"]:
        mid = fm["model_id"]
        print(f"\n================ Loading {mid} ({fm['architecture']}@{fm['imgsz']}) ================")
        model = YOLO(str(fm["bundle_weight_path"]))

        # 2a. In-domain planned evaluations
        for ev in evals_by_model.get(mid, []):
            ev_id = ev["eval_id"]
            res_m = run_inference_pass(
                model,
                fm,
                ev["release_id"],
                ev["partition"],
                work_dir / "evals" / ev_id,
                ev_id,
            )
            exec_manifest["evals"][ev_id] = res_m

        # 2b. Unique zero-shot cross-country passes
        for (tgt_rel, tgt_part), bridge_ids in xshift_by_model.get(mid, {}).items():
            pass_key = f"{mid}_to_{tgt_rel}_{tgt_part}"
            res_x = run_inference_pass(
                model,
                fm,
                tgt_rel,
                tgt_part,
                work_dir / "xshift" / pass_key,
                pass_key,
            )
            res_x["bridge_ids"] = bridge_ids
            exec_manifest["xshift_passes"][pass_key] = res_x

        # 2c. UD14 GPU serial BS=1 timing on model's primary test partition
        timing_res = run_gpu_timing(model, fm, fm["release_id"], work_dir / "timing" / f"{mid}_gpu_timing.json")
        exec_manifest["gpu_timing"][mid] = timing_res

        # 2d. Static ONNX export for selected models (opset=17, simplify=False)
        if fm.get("export_onnx", False):
            # Copy weight to work temp so export writes cleanly to /kaggle/working (input dir is read-only!)
            tmp_pt = work_dir / "_tmp_export" / f"{mid}.pt"
            tmp_pt.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fm["bundle_weight_path"], tmp_pt)
            try:
                exp_model = YOLO(str(tmp_pt))
                exported_path = Path(
                    exp_model.export(
                        format="onnx",
                        imgsz=int(fm["imgsz"]),
                        opset=17,
                        simplify=False,
                        dynamic=False,
                        half=False,
                    )
                )
                dst_onnx = onnx_dir / f"{mid}.onnx"
                shutil.move(str(exported_path), str(dst_onnx))
                exec_manifest["onnx_exports"][mid] = {
                    "filename": dst_onnx.name,
                    "imgsz": int(fm["imgsz"]),
                    "opset": 17,
                    "sha256": sha256_file(dst_onnx),
                    "bytes": dst_onnx.stat().st_size,
                }
                print(f"[ONNX] Exported {dst_onnx.name} ({dst_onnx.stat().st_size / (1024*1024):.2f} MB)")
            except Exception as exc:  # noqa: BLE001
                exec_manifest["onnx_exports"][mid] = {"error": str(exc)}
                print(f"[ONNX WARN] Export failed for {mid} (predictions & timing unaffected): {exc}")
            finally:
                tmp_pt.unlink(missing_ok=True)

        del model
        if use_cuda:
            torch.cuda.empty_cache()

    shutil.rmtree(work_dir / "_tmp_export", ignore_errors=True)
    exec_manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
    all_eval_errors = sum(v["error_images"] for v in exec_manifest["evals"].values())
    all_xs_errors = sum(v["error_images"] for v in exec_manifest["xshift_passes"].values())
    exec_manifest["total_errors"] = all_eval_errors + all_xs_errors
    exec_manifest["all_checks_passed"] = (exec_manifest["total_errors"] == 0)

    out_manifest_path = work_dir / "step032_execution_manifest.json"
    out_manifest_path.write_text(json.dumps(exec_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\n[ALL DONE] STEP-032 complete! Total errors={exec_manifest['total_errors']} | Manifest: {out_manifest_path}")


if __name__ == "__main__":
    main()
