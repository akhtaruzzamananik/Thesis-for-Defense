"""Clean-Environment Reproducibility Audit (STEP-038 / T22 / G14).

Verifies three explicit reproduction levels without altering any archived result:
  - R1: Bit-for-bit SHA-256 verification of all 29 freeze hashes, 14 predictions.jsonl, and 7 .onnx files.
  - R2: Exact deterministic metric replay (<= 1e-6 tolerance) via frozen src/opg/evaluator.py on EVAL0001, EVAL0011, EVAL0013.
  - R3: Clean ONNX CPU end-to-end inference replay from raw OPGs (self-determinism + PyTorch-GPU parity) +
        fresh git-archive clean-checkout verification of validate_repo.py & unit tests.
  - R4 (Full 13-EXP GPU retraining): Explicitly marked NOT_REEXECUTED (recipe & seeds locked).

Saves Git-safe JSON evidence to 12_Documentation/step038_reproducibility_audit.json.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import box_iou_xyxy, parse_yolo_line, yolo_norm_to_xyxy  # noqa: E402
from opg.data_loader import load_locked_partition_items  # noqa: E402
from opg.evaluator import DetectionBox, evaluate_predictions  # noqa: E402
from opg.inference_prototype import OPGPrototypeEngine  # noqa: E402

REL_META = {
    "REL0001": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA"),
    "REL0004": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD"),
    "REL0005": ("DS0005", "SPLIT0005", "ANNB0005", "TrackE"),
}
MATCHING_IOUS = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_track_classes() -> dict[str, list[str]]:
    by_track: dict[str, dict[int, str]] = {}
    with (ROOT / "04_Annotations" / "classes.csv").open("r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            ti = r["TrainingIndex"].strip()
            if ":" in ti and ti.startswith("Track"):
                tr, idx = ti.split(":", 1)
                by_track.setdefault(tr, {})[int(idx)] = r["Name"].strip()
    return {t: [d[i] for i in sorted(d)] for t, d in by_track.items()}


def main() -> None:
    t_audit0 = time.perf_counter()
    freeze = json.loads((ROOT / "09_Evaluation" / "freeze_manifest.json").read_text(encoding="utf-8"))
    exec_man = json.loads((ROOT / "09_Evaluation" / "step032_execution_manifest.json").read_text(encoding="utf-8"))
    offgit_root = ROOT / "08_Checkpoints" / "artifacts" / "STEP032_outputs"

    # -------------------------------------------------------------------------
    # LEVEL R1: BIT-FOR-BIT CHECKSUM AUDIT (29 freeze + 14 preds + 7 onnx = 50)
    # -------------------------------------------------------------------------
    gh = freeze["governance_hashes"]
    r1_checks: list[tuple[str, str]] = [
        (gh["class_map_path"], gh["class_map_sha256"]),
        (gh["protocol_path"], gh["protocol_sha256"]),
        (gh["experiment_plan_path"], gh["experiment_plan_sha256"]),
        (gh["evaluator_py_path"], gh["evaluator_py_sha256"]),
        (gh["preprocessing_py_path"], gh["preprocessing_py_sha256"]),
    ]
    for pp_info in gh["pp_configs"].values():
        r1_checks.append((pp_info["path"], pp_info["sha256"]))
    for rid, info in freeze["releases"].items():
        r1_checks.append((f"03_Datasets/splits/{info['split_id']}/manifest.csv", info["split_manifest_csv_sha256"]))
        r1_checks.append((f"05_Preprocessing/processed/{rid}/release_manifest.json", info["release_manifest_sha256"]))
    for fm in freeze["frozen_models"]:
        r1_checks.append((fm["weights_relpath"], fm["weights_sha256"]))
    for ev in freeze["planned_evaluations"]:
        eid = ev["eval_id"]
        rm = json.loads((ROOT / "09_Evaluation" / eid / "run_manifest.json").read_text(encoding="utf-8"))
        r1_checks.append((f"08_Checkpoints/artifacts/STEP032_outputs/evals/{eid}/predictions.jsonl", rm["predictions_sha256"]))
    for mid, ox in exec_man["onnx_exports"].items():
        r1_checks.append((f"08_Checkpoints/artifacts/STEP032_outputs/onnx/{ox['filename']}", ox["sha256"]))

    r1_mismatches = []
    for rel_p, exp_h in r1_checks:
        act_h = sha256_file(ROOT / rel_p)
        if act_h != exp_h:
            r1_mismatches.append({"path": rel_p, "expected": exp_h, "actual": act_h})
    assert not r1_mismatches, f"R1 Checksum failures: {r1_mismatches}"
    print(f"[R1 PASS] {len(r1_checks)}/{len(r1_checks)} artifact SHA-256 checksums verified bit-for-bit.")

    # -------------------------------------------------------------------------
    # LEVEL R2: DETERMINISTIC METRIC REPLAY (<= 1e-6 TOLERANCE)
    # -------------------------------------------------------------------------
    track_classes = load_track_classes()
    r2_targets = [("EVAL0001", "REL0001", "test"), ("EVAL0011", "REL0004", "test"), ("EVAL0013", "REL0005", "test")]
    r2_results: dict[str, Any] = {}
    for eid, rid, part in r2_targets:
        ds_id, sp_id, ba_id, tr_id = REL_META[rid]
        archived = json.loads((ROOT / "09_Evaluation" / eid / "metrics_summary.json").read_text(encoding="utf-8"))
        arch_m = archived["metrics_at_frozen_conf_op"]
        conf_op = float(archived["frozen_conf_op"])

        items = load_locked_partition_items(
            ROOT, dataset_id=ds_id, split_id=sp_id, batch_id=ba_id, track_id=tr_id, partition=part
        )
        exp_dir = ROOT / "04_Annotations" / "exports" / f"{ba_id}_{tr_id}"
        gt_by_img: dict[str, list[DetectionBox]] = {}
        for it in items:
            bs = []
            for ln in (exp_dir / it.label_relpath).read_text(encoding="utf-8").splitlines():
                if ln.strip():
                    c, xc, yc, bw, bh = parse_yolo_line(ln.strip())
                    bs.append(DetectionBox(c, yolo_norm_to_xyxy(xc, yc, bw, bh, it.width, it.height), 1.0))
            gt_by_img[it.image_id] = bs

        pred_by_img: dict[str, list[DetectionBox]] = {}
        with (offgit_root / "evals" / eid / "predictions.jsonl").open("r", encoding="utf-8") as pf:
            for line in pf:
                rec = json.loads(line)
                pred_by_img[rec["image_id"]] = [
                    DetectionBox(int(b[0]), (float(b[2]), float(b[3]), float(b[4]), float(b[5])), float(b[1]))
                    for b in rec["boxes"]
                ]

        replayed = evaluate_predictions(
            gt_by_img,
            pred_by_img,
            track_classes[tr_id],
            matching_ious=MATCHING_IOUS,
            operating_conf=conf_op,
            score_floor=0.001,
            max_detections=300,
        )
        d_m50 = abs(float(replayed["mAP@0.50"]) - float(arch_m["mAP@0.50"]))
        d_m95 = abs(float(replayed["mAP@0.50:0.95"]) - float(arch_m["mAP@0.50:0.95"]))
        d_f1 = abs(float(replayed["macro_f1"]) - float(arch_m["macro_f1"]))
        counts_exact = (
            replayed["total_tp"] == arch_m["total_tp"]
            and replayed["total_fp"] == arch_m["total_fp"]
            and replayed["total_fn"] == arch_m["total_fn"]
        )
        assert d_m50 <= 1e-6 and d_m95 <= 1e-6 and d_f1 <= 1e-6 and counts_exact
        r2_results[eid] = {
            "archived_mAP50": arch_m["mAP@0.50"],
            "replayed_mAP50": replayed["mAP@0.50"],
            "abs_diff_mAP50": d_m50,
            "abs_diff_mAP50_95": d_m95,
            "abs_diff_macro_f1": d_f1,
            "tp_fp_fn_exact_match": counts_exact,
        }
        print(f"[R2 PASS] {eid} metric replay exact: ΔmAP50={d_m50:.1e}, ΔmAP50-95={d_m95:.1e}, TP/FP/FN exact={counts_exact}")

    # -------------------------------------------------------------------------
    # LEVEL R3A: ONNX CPU INFERENCE REPLAY (SELF-DETERMINISM + PYTORCH PARITY)
    # -------------------------------------------------------------------------
    r3_targets = [
        ("MODEL0008", "EVAL0013", "REL0005", 20),
        ("MODEL0005", "EVAL0001", "REL0001", 10),
        ("MODEL0013", "EVAL0011", "REL0004", 10),
    ]
    r3_results: dict[str, Any] = {}
    for mid, eid, rid, n_sample in r3_targets:
        ds_id, sp_id, ba_id, tr_id = REL_META[rid]
        items = load_locked_partition_items(
            ROOT, dataset_id=ds_id, split_id=sp_id, batch_id=ba_id, track_id=tr_id, partition="test"
        )[:n_sample]
        ext_dir = ROOT / "03_Datasets" / "raw" / ds_id / "extracted"
        engine = OPGPrototypeEngine(model_id=mid, repo_root=ROOT)
        conf_op = engine.meta.frozen_conf_op

        pt_preds: dict[str, list[list[float]]] = {}
        with (offgit_root / "evals" / eid / "predictions.jsonl").open("r", encoding="utf-8") as pf:
            for line in pf:
                rec = json.loads(line)
                pt_preds[rec["image_id"]] = [b for b in rec["boxes"] if float(b[1]) >= conf_op]

        max_self_diff = 0.0
        matched_ious: list[float] = []
        matched_score_diffs: list[float] = []
        latencies: list[float] = []

        for idx, it in enumerate(items):
            p_img = ext_dir / it.raw_relpath
            p1, _ = engine.predict_file(p_img)
            latencies.append(float(p1["timing_ms"]["T_e2e_ms"]))
            # Self-determinism replay on first 3 images
            if idx < 3:
                p2, _ = engine.predict_file(p_img)
                assert len(p1["detections"]) == len(p2["detections"])
                for d1, d2 in zip(p1["detections"], p2["detections"]):
                    assert d1["class_id"] == d2["class_id"]
                    max_self_diff = max(max_self_diff, abs(d1["confidence"] - d2["confidence"]))
                    for v1, v2 in zip(d1["bbox_xyxy_px"], d2["bbox_xyxy_px"]):
                        max_self_diff = max(max_self_diff, abs(v1 - v2))

            # Parity vs STEP-032 PyTorch GPU predictions
            for pb in pt_preds.get(it.image_id, []):
                pc, ps, px0, py0, px1, py1 = int(pb[0]), float(pb[1]), float(pb[2]), float(pb[3]), float(pb[4]), float(pb[5])
                best_iou = 0.0
                best_sd = None
                for od in p1["detections"]:
                    if od["class_id"] == pc:
                        iou_v = box_iou_xyxy((px0, py0, px1, py1), tuple(od["bbox_xyxy_px"]))
                        if iou_v > best_iou:
                            best_iou = iou_v
                            best_sd = abs(ps - float(od["confidence"]))
                if best_sd is not None:
                    matched_ious.append(best_iou)
                    matched_score_diffs.append(best_sd)

        mean_iou = round(float(np.mean(matched_ious)), 5) if matched_ious else 0.0
        mean_sd = round(float(np.mean(matched_score_diffs)), 5) if matched_score_diffs else 0.0
        assert max_self_diff == 0.0, f"{mid} non-deterministic CPU replay: {max_self_diff}"
        assert mean_iou >= 0.95 and mean_sd <= 0.02, f"{mid} parity out of tolerance: IoU={mean_iou}, sd={mean_sd}"
        r3_results[mid] = {
            "eval_id": eid,
            "sampled_raw_opgs": n_sample,
            "self_determinism_max_diff": max_self_diff,
            "pytorch_gpu_vs_onnx_cpu_matched_boxes": len(matched_ious),
            "mean_box_iou": mean_iou,
            "mean_abs_score_diff": mean_sd,
            "mean_cpu_e2e_ms": round(float(np.mean(latencies)), 2),
        }
        print(
            f"[R3A PASS] {mid} ({n_sample} raw OPGs): self_diff={max_self_diff}, "
            f"PyTorch-vs-ONNX IoU={mean_iou}, |Δscore|={mean_sd}, CPU T_e2e={r3_results[mid]['mean_cpu_e2e_ms']}ms"
        )

    # -------------------------------------------------------------------------
    # LEVEL R3B: FRESH GIT-ARCHIVE CLEAN CHECKOUT TEST (ZERO UNTRACKED STATE!)
    # -------------------------------------------------------------------------
    head_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip()
    clean_dir = Path(tempfile.mkdtemp(prefix="opg_step038_clean_"))
    try:
        tar_path = clean_dir / "repo.tar"
        subprocess.run(["git", "archive", "--format=tar", "-o", str(tar_path), "HEAD"], cwd=str(ROOT), check=True)
        extract_dir = clean_dir / "checkout"
        extract_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["tar", "-xf", str(tar_path), "-C", str(extract_dir)], check=True)

        clean_env = {k: v for k, v in os.environ.items() if k.upper() != "PYTHONPATH"}
        v_proc = subprocess.run(
            [sys.executable, "13_Automation/validate_repo.py"],
            cwd=str(extract_dir),
            env=clean_env,
            capture_output=True,
            text=True,
            check=False,
        )
        p_proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "tests/test_repo_checks.py",
                "tests/test_smoke_data_env.py",
                "tests/test_annotation_schema.py",
                "tests/test_preprocessing.py",
                "tests/test_prototype_interface.py",
            ],
            cwd=str(extract_dir),
            env=clean_env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert v_proc.returncode == 0, f"Clean checkout validate_repo failed:\n{v_proc.stdout}\n{v_proc.stderr}"
        assert p_proc.returncode == 0, f"Clean checkout pytest failed:\n{p_proc.stdout}\n{p_proc.stderr}"
        clean_checkout_res = {
            "tested_commit": head_sha,
            "clean_env_pythonpath_stripped": True,
            "offgit_data_absent_in_clean_checkout": True,
            "validate_repo_stdout": v_proc.stdout.strip(),
            "pytest_summary": p_proc.stdout.strip().splitlines()[-1] if p_proc.stdout.strip() else "",
            "passed": True,
        }
        print(f"[R3B PASS] Clean git-archive checkout ({head_sha[:7]}): validate_repo OK & {clean_checkout_res['pytest_summary']}")
    finally:
        shutil.rmtree(clean_dir, ignore_errors=True)

    audit_payload = {
        "schema_version": "1.0.0",
        "step": "STEP-038",
        "gate": "G14",
        "audited_utc": datetime.now(timezone.utc).isoformat(),
        "audited_commit": head_sha,
        "duration_sec": round(time.perf_counter() - t_audit0, 2),
        "host_context": {
            "os": f"{platform.system()} {platform.release()}",
            "python": platform.python_version(),
            "cpu_cores_logical": os.cpu_count(),
        },
        "prospective_tolerances": {
            "R1_checksums": "exact_bit_for_bit_sha256",
            "R2_metric_replay": "abs_diff <= 1e-6 and exact TP/FP/FN counts",
            "R3A_onnx_self_determinism": "max_abs_diff == 0.0",
            "R3A_onnx_cpu_vs_pytorch_gpu_parity": "mean_box_iou >= 0.95 and mean_abs_score_diff <= 0.02",
            "R3B_clean_git_archive_checkout": "validate_repo exit 0 and unit/error-contract tests exit 0",
        },
        "reproduction_levels": {
            "R1_artifact_checksums": {"status": "PASS", "verified_count": len(r1_checks), "mismatches": 0},
            "R2_metric_replay": {"status": "PASS", "results": r2_results},
            "R3A_onnx_inference_replay": {"status": "PASS", "results": r3_results},
            "R3B_clean_git_archive_checkout": clean_checkout_res,
            "R4_full_13exp_gpu_retraining": {
                "status": "NOT_REEXECUTED",
                "rationale": "Full 13-EXP Kaggle Tesla T4 retraining (~7.5 GPU-hr) is preserved via locked seeds (20261124), deterministic=true, ultralytics==8.3.253, and committed EXP0001-0013 configs/args/results; not re-executed in STEP-038.",
            },
        },
        "all_verified_levels_passed": True,
    }
    out_path = ROOT / "12_Documentation" / "step038_reproducibility_audit.json"
    out_path.write_text(json.dumps(audit_payload, indent=2) + "\n", encoding="utf-8")
    print(f"\n[ALL DONE] STEP-038 audit complete in {audit_payload['duration_sec']}s -> {out_path}")


if __name__ == "__main__":
    main()
