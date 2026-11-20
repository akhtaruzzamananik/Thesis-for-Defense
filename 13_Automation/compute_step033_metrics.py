"""Compute canonical STEP-033 held-out detection metrics, GroupID cluster bootstrap 95% CIs,
and zero-shot cross-country HC01-HC05 shift metrics using the frozen STEP-031 evaluator.

Verifies frozen evaluator.py, classes.csv, protocol.md, and all predictions.jsonl SHA-256 hashes
against 09_Evaluation/freeze_manifest.json before computing metrics.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import box_iou_xyxy, parse_yolo_line, yolo_norm_to_xyxy  # noqa: E402
from opg.data_loader import load_locked_partition_items  # noqa: E402
from opg.evaluator import DetectionBox, compute_ap_continuous, evaluate_predictions  # noqa: E402

REL_META = {
    "REL0001": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA"),
    "REL0002": ("DS0002", "SPLIT0002", "ANNB0002", "TrackB"),
    "REL0003": ("DS0003", "SPLIT0003", "ANNB0003", "TrackC"),
    "REL0004": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD"),
    "REL0005": ("DS0005", "SPLIT0005", "ANNB0005", "TrackE"),
    "REL0006": ("DS0006", "SPLIT0006", "ANNB0006", "TrackF"),
}

MATCHING_IOUS = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_track_class_names(classes_csv: Path) -> dict[str, list[str]]:
    by_track: dict[str, dict[int, str]] = {}
    with classes_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ti = row["TrainingIndex"].strip()
            if ":" not in ti:
                continue
            track, idx_s = ti.split(":", 1)
            if not track.startswith("Track"):
                continue
            by_track.setdefault(track, {})[int(idx_s)] = row["Name"].strip()
    return {t: [d[i] for i in sorted(d)] for t, d in by_track.items()}


def load_ground_truth(
    release_id: str, partition: str
) -> tuple[dict[str, list[DetectionBox]], dict[str, str]]:
    ds_id, sp_id, ba_id, tr_id = REL_META[release_id]
    items = load_locked_partition_items(
        ROOT,
        dataset_id=ds_id,
        split_id=sp_id,
        batch_id=ba_id,
        track_id=tr_id,
        partition=partition,
        allow_test_partition=False,
    )
    exp_dir = ROOT / "04_Annotations" / "exports" / f"{ba_id}_{tr_id}"
    gt_by_img: dict[str, list[DetectionBox]] = {}
    group_by_img: dict[str, str] = {}
    for it in items:
        group_by_img[it.image_id] = it.group_id
        lbl_path = exp_dir / it.label_relpath
        boxes: list[DetectionBox] = []
        for ln in lbl_path.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            cid, xc, yc, bw, bh = parse_yolo_line(ln)
            x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, it.width, it.height)
            boxes.append(DetectionBox(cid, (x0, y0, x1, y1), score=1.0))
        gt_by_img[it.image_id] = boxes
    return gt_by_img, group_by_img


def load_predictions_jsonl(pred_path: Path, expected_sha256: str) -> dict[str, list[DetectionBox]]:
    actual = sha256_file(pred_path)
    if actual != expected_sha256:
        raise ValueError(f"predictions.jsonl SHA-256 mismatch for {pred_path}: {actual} != {expected_sha256}")
    preds: dict[str, list[DetectionBox]] = {}
    with pred_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            iid = rec["image_id"]
            preds[iid] = [
                DetectionBox(int(b[0]), (float(b[2]), float(b[3]), float(b[4]), float(b[5])), score=float(b[1]))
                for b in rec["boxes"]
            ]
    return preds


def precompute_per_image_matches(
    gt_by_img: dict[str, list[DetectionBox]],
    pred_by_img: dict[str, list[DetectionBox]],
    num_classes: int,
    ious: Sequence[float] = MATCHING_IOUS,
    score_floor: float = 0.001,
    max_det: int = 300,
) -> dict[str, Any]:
    """Precompute exact per-image one-to-one greedy TP/FP flags for fast exact GroupID bootstrap.

    Because greedy matching inside each image depends ONLY on boxes within that image,
    sorting globally by score and computing weighted cumulative TP/FP over resampled images
    is mathematically identical to re-running evaluate_predictions from scratch.
    """
    img_ids = sorted(gt_by_img.keys())
    img_to_idx = {iid: idx for idx, iid in enumerate(img_ids)}
    n_imgs = len(img_ids)

    # Filter & cap predictions per image exactly like evaluate_predictions
    pred_norm: dict[str, list[DetectionBox]] = {}
    for iid in img_ids:
        raw = [p for p in pred_by_img.get(iid, []) if p.score >= score_floor]
        raw.sort(key=lambda p: p.score, reverse=True)
        pred_norm[iid] = raw[:max_det]

    gt_counts = np.zeros((num_classes, n_imgs), dtype=np.int64)
    # Per class: globally sorted arrays of (scores, img_idx, tp_flags[n_ious, n_preds])
    class_data: dict[int, dict[str, Any]] = {}

    for cid in range(num_classes):
        entries: list[tuple[float, int, list[int]]] = []
        for idx, iid in enumerate(img_ids):
            gts = [b.xyxy for b in gt_by_img[iid] if b.class_id == cid]
            gt_counts[cid, idx] = len(gts)
            c_preds = [p for p in pred_norm[iid] if p.class_id == cid]
            c_preds.sort(key=lambda p: p.score, reverse=True)
            if not c_preds:
                continue
            if not gts:
                zeros = [0] * len(ious)
                for p in c_preds:
                    entries.append((p.score, idx, zeros))
                continue

            # Compute IoU matrix once per (img, class)
            n_p = len(c_preds)
            n_g = len(gts)
            iou_mat = np.zeros((n_p, n_g), dtype=np.float64)
            for pi, p in enumerate(c_preds):
                for gi, g in enumerate(gts):
                    iou_mat[pi, gi] = box_iou_xyxy(p.xyxy, g)

            tp_by_iou = [[0] * len(ious) for _ in range(n_p)]
            for t_idx, thr in enumerate(ious):
                used = [False] * n_g
                for pi in range(n_p):
                    best_iou = -1.0
                    best_g = -1
                    for gi in range(n_g):
                        if used[gi]:
                            continue
                        val = float(iou_mat[pi, gi])
                        if val >= thr and val > best_iou:
                            best_iou = val
                            best_g = gi
                    if best_g >= 0:
                        used[best_g] = True
                        tp_by_iou[pi][t_idx] = 1

            for pi, p in enumerate(c_preds):
                entries.append((p.score, idx, tp_by_iou[pi]))

        entries.sort(key=lambda x: x[0], reverse=True)
        if entries:
            scores = np.array([e[0] for e in entries], dtype=np.float64)
            e_img_idx = np.array([e[1] for e in entries], dtype=np.int64)
            tp_mat = np.array([e[2] for e in entries], dtype=np.int8)  # shape (N_p, len(ious))
        else:
            scores = np.zeros(0, dtype=np.float64)
            e_img_idx = np.zeros(0, dtype=np.int64)
            tp_mat = np.zeros((0, len(ious)), dtype=np.int8)
        class_data[cid] = {"scores": scores, "img_idx": e_img_idx, "tp_mat": tp_mat}

    return {
        "img_ids": img_ids,
        "img_to_idx": img_to_idx,
        "gt_counts": gt_counts,
        "class_data": class_data,
        "num_classes": num_classes,
        "ious": tuple(ious),
    }


def eval_weighted_sample(
    pre: dict[str, Any],
    img_weights: np.ndarray,
    operating_conf: float,
    class_subset: Sequence[int] | None = None,
) -> dict[str, float | None]:
    cids = list(range(pre["num_classes"])) if class_subset is None else list(class_subset)
    n_ious = len(pre["ious"])
    ap50_list: list[float] = []
    ap50_95_list: list[float] = []
    macro_p: list[float] = []
    macro_r: list[float] = []
    macro_f1: list[float] = []
    tot_tp = 0
    tot_fp = 0
    tot_fn = 0

    for cid in cids:
        total_gt = int(np.dot(pre["gt_counts"][cid], img_weights))
        cd = pre["class_data"][cid]
        scores: np.ndarray = cd["scores"]
        e_idx: np.ndarray = cd["img_idx"]
        tp_mat: np.ndarray = cd["tp_mat"]

        if scores.size > 0:
            w = img_weights[e_idx]
            active = w > 0
            w_act = w[active]
            sc_act = scores[active]
            tp_act = tp_mat[active]
        else:
            w_act = np.zeros(0, dtype=np.int64)
            sc_act = np.zeros(0, dtype=np.float64)
            tp_act = np.zeros((0, n_ious), dtype=np.int8)

        op_mask = sc_act >= operating_conf
        if total_gt == 0:
            if op_mask.any():
                tot_fp += int(w_act[op_mask].sum())
            continue

        # Operating-point TP/FP/FN at IoU=0.50 (index 0)
        if op_mask.any():
            tp_op = int(np.dot(tp_act[op_mask, 0], w_act[op_mask]))
            fp_op = int(np.dot(1 - tp_act[op_mask, 0], w_act[op_mask]))
        else:
            tp_op = 0
            fp_op = 0
        fn_op = total_gt - tp_op
        tot_tp += tp_op
        tot_fp += fp_op
        tot_fn += fn_op

        rec_op = tp_op / float(total_gt)
        macro_r.append(rec_op)
        if (tp_op + fp_op) > 0:
            prec_op = tp_op / float(tp_op + fp_op)
            macro_p.append(prec_op)
            macro_f1.append((2.0 * prec_op * rec_op / (prec_op + rec_op)) if (prec_op + rec_op) > 0 else 0.0)

        # AP across all IoUs
        if w_act.size == 0:
            ap50_list.append(0.0)
            ap50_95_list.append(0.0)
            continue

        cum_total = np.cumsum(w_act, dtype=np.float64)
        aps_c: list[float] = []
        for t_i in range(n_ious):
            cum_tp = np.cumsum(tp_act[:, t_i] * w_act, dtype=np.float64)
            rec = cum_tp / float(total_gt)
            prec = cum_tp / np.maximum(cum_total, 1e-12)
            mrec = np.concatenate(([0.0], rec, [1.0]))
            mpre = np.concatenate(([1.0], prec, [0.0]))
            mpre = np.maximum.accumulate(mpre[::-1])[::-1]
            idx = np.where(mrec[1:] != mrec[:-1])[0]
            aps_c.append(float(np.sum((mrec[idx + 1] - mrec[idx]) * mpre[idx + 1])))
        ap50_list.append(aps_c[0])
        ap50_95_list.append(float(np.mean(aps_c)))

    micro_p = (tot_tp / float(tot_tp + tot_fp)) if (tot_tp + tot_fp) > 0 else None
    micro_r = (tot_tp / float(tot_tp + tot_fn)) if (tot_tp + tot_fn) > 0 else None
    micro_f1 = (
        (2.0 * micro_p * micro_r / (micro_p + micro_r))
        if (micro_p is not None and micro_r is not None and (micro_p + micro_r) > 0)
        else (0.0 if (micro_p is not None and micro_r is not None) else None)
    )
    return {
        "mAP@0.50": float(np.mean(ap50_list)) if ap50_list else None,
        "mAP@0.50:0.95": float(np.mean(ap50_95_list)) if ap50_95_list else None,
        "macro_precision": float(np.mean(macro_p)) if macro_p else None,
        "macro_recall": float(np.mean(macro_r)) if macro_r else None,
        "macro_f1": float(np.mean(macro_f1)) if macro_f1 else None,
        "micro_f1": micro_f1,
    }


def run_groupid_bootstrap(
    pre: dict[str, Any],
    group_by_img: dict[str, str],
    operating_conf: float,
    *,
    n_resamples: int = 1000,
    seed: int = 20261131,
    class_subset: Sequence[int] | None = None,
) -> dict[str, Any]:
    img_ids = pre["img_ids"]
    groups: dict[str, list[int]] = {}
    for idx, iid in enumerate(img_ids):
        groups.setdefault(group_by_img[iid], []).append(idx)
    group_keys = sorted(groups.keys())
    group_members = [groups[g] for g in group_keys]
    n_groups = len(group_keys)
    n_imgs = len(img_ids)

    rng = np.random.default_rng(seed)
    metrics_keys = ("mAP@0.50", "mAP@0.50:0.95", "macro_precision", "macro_recall", "macro_f1", "micro_f1")
    samples: dict[str, list[float]] = {k: [] for k in metrics_keys}

    for _ in range(n_resamples):
        drawn = rng.integers(0, n_groups, size=n_groups)
        counts = np.bincount(drawn, minlength=n_groups)
        img_w = np.zeros(n_imgs, dtype=np.int64)
        for g_idx, mult in enumerate(counts):
            if mult > 0:
                for m_idx in group_members[g_idx]:
                    img_w[m_idx] += int(mult)
        res = eval_weighted_sample(pre, img_w, operating_conf, class_subset=class_subset)
        for k in metrics_keys:
            if res[k] is not None:
                samples[k].append(float(res[k]))

    ci_out: dict[str, Any] = {
        "n_resamples": n_resamples,
        "n_clusters_GroupID": n_groups,
        "seed": seed,
        "ci_95": {},
    }
    for k in metrics_keys:
        vals = samples[k]
        if vals:
            arr = np.asarray(vals, dtype=np.float64)
            ci_out["ci_95"][k] = {
                "mean": round(float(arr.mean()), 6),
                "std": round(float(arr.std()), 6),
                "lo": round(float(np.percentile(arr, 2.5)), 6),
                "hi": round(float(np.percentile(arr, 97.5)), 6),
            }
        else:
            ci_out["ci_95"][k] = None
    return ci_out


def write_eval_metrics_csv(path: Path, eval_res: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle)
        w.writerow(
            [
                "ClassID",
                "ClassName",
                "GTCount",
                "PredCountFloor",
                "TP_op",
                "FP_op",
                "FN_op",
                "Precision_op",
                "Recall_op",
                "F1_op",
                "AP50",
                "AP50_95",
                "Eligible",
            ]
        )
        for cid in sorted(eval_res["per_class"].keys()):
            c = eval_res["per_class"][cid]
            w.writerow(
                [
                    cid,
                    c["class_name"],
                    c["gt_count"],
                    c["pred_count_total"],
                    c["tp_op"],
                    c["fp_op"],
                    c["fn_op"],
                    "N/A" if c["precision"] is None else f"{c['precision']:.6f}",
                    "N/A" if c["recall"] is None else f"{c['recall']:.6f}",
                    "N/A" if c["f1"] is None else f"{c['f1']:.6f}",
                    "N/A" if c["ap"] is None else f"{c['ap']:.6f}",
                    "N/A" if c.get("ap_50_95") is None else f"{c['ap_50_95']:.6f}",
                    c["eligible"],
                ]
            )
        w.writerow(
            [
                "ALL_MACRO",
                f"Macro ({eval_res['eligible_class_count']}/{eval_res['total_classes']} eligible)",
                sum(c["gt_count"] for c in eval_res["per_class"].values()),
                sum(c["pred_count_total"] for c in eval_res["per_class"].values()),
                eval_res["total_tp"],
                eval_res["total_fp"],
                eval_res["total_fn"],
                "N/A" if eval_res["macro_precision"] is None else f"{eval_res['macro_precision']:.6f}",
                "N/A" if eval_res["macro_recall"] is None else f"{eval_res['macro_recall']:.6f}",
                "N/A" if eval_res["macro_f1"] is None else f"{eval_res['macro_f1']:.6f}",
                "N/A" if eval_res["mAP@0.50"] is None else f"{eval_res['mAP@0.50']:.6f}",
                "N/A" if eval_res["mAP@0.50:0.95"] is None else f"{eval_res['mAP@0.50:0.95']:.6f}",
                True,
            ]
        )
        w.writerow(
            [
                "ALL_MICRO",
                "Micro pooled at frozen conf_op",
                sum(c["gt_count"] for c in eval_res["per_class"].values()),
                sum(c["pred_count_total"] for c in eval_res["per_class"].values()),
                eval_res["total_tp"],
                eval_res["total_fp"],
                eval_res["total_fn"],
                "N/A" if eval_res["micro_precision"] is None else f"{eval_res['micro_precision']:.6f}",
                "N/A" if eval_res["micro_recall"] is None else f"{eval_res['micro_recall']:.6f}",
                "N/A" if eval_res["micro_f1"] is None else f"{eval_res['micro_f1']:.6f}",
                "N/A",
                "N/A",
                True,
            ]
        )


def fmt_opt(v: float | None, nd: int = 4) -> str:
    return "N/A" if v is None else f"{v:.{nd}f}"


def main() -> None:
    freeze_path = ROOT / "09_Evaluation" / "freeze_manifest.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    gh = freeze["governance_hashes"]

    # Strict freeze hash check on evaluator.py, classes.csv, and protocol.md
    for rel_p, exp_h in [
        (gh["class_map_path"], gh["class_map_sha256"]),
        (gh["protocol_path"], gh["protocol_sha256"]),
        (gh["evaluator_py_path"], gh["evaluator_py_sha256"]),
    ]:
        act_h = sha256_file(ROOT / rel_p)
        if act_h != exp_h:
            raise ValueError(f"FREEZE HASH DRIFT on {rel_p}: {act_h} != {exp_h}")
    print("[OK] Frozen evaluator.py, classes.csv, and protocol.md SHA-256 verified bit-for-bit.")

    track_classes = load_track_class_names(ROOT / gh["class_map_path"])
    models_by_id = {m["model_id"]: m for m in freeze["frozen_models"]}
    ev_cfg = freeze["evaluation_settings"]
    score_floor = float(ev_cfg["metric_conf_floor"])
    max_det = int(ev_cfg["max_det"])
    fallback_conf = float(ev_cfg["fallback_reference_conf"])
    n_boot = int(ev_cfg["bootstrap_resamples"])
    boot_seed = int(ev_cfg["bootstrap_seed"])

    offgit_root = ROOT / "08_Checkpoints" / "artifacts" / "STEP032_outputs"

    # Cache loaded GT per (release_id, partition)
    gt_cache: dict[tuple[str, str], tuple[dict[str, list[DetectionBox]], dict[str, str]]] = {}

    def get_gt(rel_id: str, part: str) -> tuple[dict[str, list[DetectionBox]], dict[str, str]]:
        key = (rel_id, part)
        if key not in gt_cache:
            gt_cache[key] = load_ground_truth(rel_id, part)
        return gt_cache[key]

    # -------------------------------------------------------------------------
    # 1. IN-DOMAIN EVALUATIONS (EVAL0001..EVAL0014) + 1000-RESAMPLE BOOTSTRAP
    # -------------------------------------------------------------------------
    eval_summaries: dict[str, Any] = {}
    for ev_idx, ev in enumerate(freeze["planned_evaluations"]):
        ev_id = ev["eval_id"]
        mid = ev["model_id"]
        rel_id = ev["release_id"]
        part = ev["partition"]
        fm = models_by_id[mid]
        tr_id = REL_META[rel_id][3]
        cls_names = track_classes[tr_id]
        conf_op = float(fm["frozen_conf_op"])

        rm = json.loads((ROOT / "09_Evaluation" / ev_id / "run_manifest.json").read_text(encoding="utf-8"))
        gt_by_img, group_by_img = get_gt(rel_id, part)
        pred_by_img = load_predictions_jsonl(offgit_root / "evals" / ev_id / "predictions.jsonl", rm["predictions_sha256"])
        assert set(gt_by_img.keys()) == set(pred_by_img.keys()), f"{ev_id} GT vs pred image key mismatch!"

        # Canonical frozen evaluator at frozen conf_op
        res_op = evaluate_predictions(
            gt_by_img,
            pred_by_img,
            cls_names,
            matching_ious=MATCHING_IOUS,
            operating_conf=conf_op,
            score_floor=score_floor,
            max_detections=max_det,
        )
        # Secondary protocol reference at conf=0.25
        res_025 = evaluate_predictions(
            gt_by_img,
            pred_by_img,
            cls_names,
            matching_ious=(0.50,),
            operating_conf=fallback_conf,
            score_floor=score_floor,
            max_detections=max_det,
        )

        # Verify fast bootstrap engine matches evaluate_predictions to <1e-5 on unit weights!
        pre = precompute_per_image_matches(gt_by_img, pred_by_img, len(cls_names), MATCHING_IOUS, score_floor, max_det)
        unit_check = eval_weighted_sample(pre, np.ones(len(pre["img_ids"]), dtype=np.int64), conf_op)
        assert abs(unit_check["mAP@0.50"] - res_op["mAP@0.50"]) < 1e-5, f"{ev_id} unit bootstrap mismatch on mAP@0.50!"
        assert abs(unit_check["mAP@0.50:0.95"] - res_op["mAP@0.50:0.95"]) < 1e-5, f"{ev_id} unit bootstrap mismatch on mAP50-95!"

        boot_ci = run_groupid_bootstrap(
            pre,
            group_by_img,
            conf_op,
            n_resamples=n_boot,
            seed=boot_seed + ev_idx,
        )

        # TrackC dual reporting: 5-class pathology (0..4) excluding selective Healthy_Tooth (5)
        dual_5cls = None
        if rel_id == "REL0003":
            gt_5 = {iid: [b for b in bs if b.class_id < 5] for iid, bs in gt_by_img.items()}
            pr_5 = {iid: [b for b in bs if b.class_id < 5] for iid, bs in pred_by_img.items()}
            res_5 = evaluate_predictions(
                gt_5,
                pr_5,
                cls_names[:5],
                matching_ious=MATCHING_IOUS,
                operating_conf=conf_op,
                score_floor=score_floor,
                max_detections=max_det,
            )
            boot_5 = run_groupid_bootstrap(pre, group_by_img, conf_op, n_resamples=n_boot, seed=boot_seed + 99, class_subset=[0, 1, 2, 3, 4])
            dual_5cls = {"metrics": res_5, "bootstrap_95ci": boot_5}

        # Persist Git-safe metrics.csv & metrics_summary.json
        out_ev_dir = ROOT / "09_Evaluation" / ev_id
        write_eval_metrics_csv(out_ev_dir / "metrics.csv", res_op)
        summary_payload = {
            "eval_id": ev_id,
            "role": ev["role"],
            "model_id": mid,
            "experiment_id": fm["experiment_id"],
            "architecture": fm["architecture"],
            "imgsz": fm["imgsz"],
            "release_id": rel_id,
            "track_id": tr_id,
            "partition": part,
            "frozen_conf_op": conf_op,
            "val_mAP50_reference": fm["val_mAP50"],
            "val_mAP50_95_reference": fm["val_mAP50_95"],
            "predictions_sha256": rm["predictions_sha256"],
            "metrics_at_frozen_conf_op": res_op,
            "metrics_at_ref_conf_025": {
                "operating_conf": fallback_conf,
                "macro_precision": res_025["macro_precision"],
                "macro_recall": res_025["macro_recall"],
                "macro_f1": res_025["macro_f1"],
                "micro_precision": res_025["micro_precision"],
                "micro_recall": res_025["micro_recall"],
                "micro_f1": res_025["micro_f1"],
                "total_tp": res_025["total_tp"],
                "total_fp": res_025["total_fp"],
                "total_fn": res_025["total_fn"],
            },
            "bootstrap_95ci": boot_ci,
            "trackC_5class_pathology_dual": dual_5cls,
        }
        (out_ev_dir / "metrics_summary.json").write_text(json.dumps(summary_payload, indent=2) + "\n", encoding="utf-8")
        eval_summaries[ev_id] = summary_payload

        ci50 = boot_ci["ci_95"]["mAP@0.50"]
        ci95 = boot_ci["ci_95"]["mAP@0.50:0.95"]
        print(
            f"[EVAL] {ev_id} {mid:9s} ({fm['architecture']}@{fm['imgsz']:4d}) {rel_id}:{part:13s} | "
            f"mAP@50={res_op['mAP@0.50']:.4f} [{ci50['lo']:.4f},{ci50['hi']:.4f}] | "
            f"mAP50-95={res_op['mAP@0.50:0.95']:.4f} [{ci95['lo']:.4f},{ci95['hi']:.4f}] | "
            f"Macro-F1={fmt_opt(res_op['macro_f1'])} (P={fmt_opt(res_op['macro_precision'])}, R={fmt_opt(res_op['macro_recall'])})"
        )

    # -------------------------------------------------------------------------
    # 2. ZERO-SHOT CROSS-COUNTRY SHIFT BRIDGES (12 BRIDGES, HC01-HC05)
    # -------------------------------------------------------------------------
    xshift_rows: list[dict[str, Any]] = []
    for br_idx, br in enumerate(freeze["cross_cohort_bridges"]):
        bid = br["bridge_id"]
        src_mid = br["source_model_id"]
        tgt_rel = br["target_release_id"]
        tgt_part = br["target_partition"]
        fm = models_by_id[src_mid]
        conf_op = float(fm["frozen_conf_op"])
        pass_key = f"{src_mid}_to_{tgt_rel}_{tgt_part}"

        rm_x = json.loads((ROOT / "09_Evaluation" / "xshift" / pass_key / "run_manifest.json").read_text(encoding="utf-8"))
        gt_raw, group_by_img = get_gt(tgt_rel, tgt_part)
        pr_raw = load_predictions_jsonl(offgit_root / "xshift" / pass_key / "predictions.jsonl", rm_x["predictions_sha256"])

        # Group mappings by target harmonized concept:
        # Each unique target GT set gets a harmonized class index 0..K-1
        cmap: dict[str, list[int]] = br["class_map_source_to_target"]
        concepts: list[str] = br["concepts"]

        # Handle both 1-to-1 / 1-to-many (e.g. TrackA:7 -> [0,1,2]) and many-to-1 (e.g. TrackD 0,1,2 -> [7])
        if len(concepts) == 1:
            src_ids = {int(k) for k in cmap.keys()}
            tgt_ids = {int(t) for ts in cmap.values() for t in ts}
            harm_names = [concepts[0]]
            gt_h = {iid: [DetectionBox(0, b.xyxy, 1.0) for b in bs if b.class_id in tgt_ids] for iid, bs in gt_raw.items()}
            pr_h = {iid: [DetectionBox(0, b.xyxy, b.score) for b in bs if b.class_id in src_ids] for iid, bs in pr_raw.items()}
        else:
            # Multi-concept bridge (e.g. HC03, HC04, HC05) in order of cmap items matching concepts list
            harm_names = list(concepts)
            src_to_h: dict[int, int] = {}
            tgt_to_h: dict[int, int] = {}
            for h_idx, (s_str, t_list) in enumerate(cmap.items()):
                src_to_h[int(s_str)] = h_idx
                for t_id in t_list:
                    tgt_to_h[int(t_id)] = h_idx
            gt_h = {
                iid: [DetectionBox(tgt_to_h[b.class_id], b.xyxy, 1.0) for b in bs if b.class_id in tgt_to_h]
                for iid, bs in gt_raw.items()
            }
            pr_h = {
                iid: [DetectionBox(src_to_h[b.class_id], b.xyxy, b.score) for b in bs if b.class_id in src_to_h]
                for iid, bs in pr_raw.items()
            }

        res_h = evaluate_predictions(
            gt_h,
            pr_h,
            harm_names,
            matching_ious=MATCHING_IOUS,
            operating_conf=conf_op,
            score_floor=score_floor,
            max_detections=max_det,
        )
        pre_h = precompute_per_image_matches(gt_h, pr_h, len(harm_names), MATCHING_IOUS, score_floor, max_det)
        boot_h = run_groupid_bootstrap(pre_h, group_by_img, conf_op, n_resamples=n_boot, seed=boot_seed + 500 + br_idx)

        row_rec = {
            "bridge_id": bid,
            "source_model_id": src_mid,
            "source_track": fm["track_id"],
            "target_release_id": tgt_rel,
            "target_track": REL_META[tgt_rel][3],
            "target_partition": tgt_part,
            "concepts": harm_names,
            "frozen_conf_op": conf_op,
            "mAP@0.50": res_h["mAP@0.50"],
            "mAP@0.50_ci95": boot_h["ci_95"]["mAP@0.50"],
            "mAP@0.50:0.95": res_h["mAP@0.50:0.95"],
            "mAP@0.50:0.95_ci95": boot_h["ci_95"]["mAP@0.50:0.95"],
            "macro_f1": res_h["macro_f1"],
            "per_concept": {harm_names[c]: res_h["per_class"][c] for c in sorted(res_h["per_class"].keys())},
        }
        xshift_rows.append(row_rec)
        c_summary = ", ".join(f"{cn}:{fmt_opt(res_h['per_class'][i]['ap'], 3)}" for i, cn in enumerate(harm_names))
        print(
            f"[XSHIFT] {bid:16s} {src_mid}({fm['track_id']})->{tgt_rel}:{tgt_part:13s} "
            f"| mAP@50={fmt_opt(res_h['mAP@0.50'])} | mAP50-95={fmt_opt(res_h['mAP@0.50:0.95'])} | "
            f"concepts={c_summary}"
        )

    (ROOT / "09_Evaluation" / "xshift_metrics_summary.json").write_text(
        json.dumps(xshift_rows, indent=2) + "\n", encoding="utf-8"
    )
    with (ROOT / "09_Evaluation" / "xshift_metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle)
        w.writerow(
            [
                "BridgeID",
                "SourceModel",
                "SourceTrack",
                "TargetRelease",
                "TargetPartition",
                "Concept",
                "GTCount",
                "TP_op",
                "FP_op",
                "FN_op",
                "Precision_op",
                "Recall_op",
                "F1_op",
                "AP50",
                "AP50_95",
            ]
        )
        for xr in xshift_rows:
            for cn, c in xr["per_concept"].items():
                w.writerow(
                    [
                        xr["bridge_id"],
                        xr["source_model_id"],
                        xr["source_track"],
                        xr["target_release_id"],
                        xr["target_partition"],
                        cn,
                        c["gt_count"],
                        c["tp_op"],
                        c["fp_op"],
                        c["fn_op"],
                        fmt_opt(c["precision"], 6),
                        fmt_opt(c["recall"], 6),
                        fmt_opt(c["f1"], 6),
                        fmt_opt(c["ap"], 6),
                        fmt_opt(c.get("ap_50_95"), 6),
                    ]
                )

    # -------------------------------------------------------------------------
    # 3. UPDATE evaluation_registry.csv & WRITE MASTER STEP-033 REPORT
    # -------------------------------------------------------------------------
    reg_path = ROOT / "09_Evaluation" / "evaluation_registry.csv"
    with reg_path.open("r", encoding="utf-8", newline="") as handle:
        reg_rows = list(csv.DictReader(handle))
        fieldnames = list(reg_rows[0].keys())
    for r in reg_rows:
        eid = r["EvaluationID"]
        if eid in eval_summaries:
            r["MetricPath"] = f"09_Evaluation/{eid}/metrics.csv"
            r["ReportPath"] = "09_Evaluation/step033_final_metrics_report.md"
            r["Status"] = "STEP033-Metrics-Computed"
            r["EvidencePath"] = f"09_Evaluation/{eid}/metrics_summary.json"
    with reg_path.open("w", encoding="utf-8", newline="") as handle:
        dw = csv.DictWriter(handle, fieldnames=fieldnames)
        dw.writeheader()
        dw.writerows(reg_rows)

    # Build clean publication-ready Markdown report
    lines = [
        "# `STEP-033` Official Held-Out Final-Test Metrics & Uncertainty Report (`FREEZE0001`)",
        "",
        "| Metadata | Value |",
        "|---|---|",
        "| Step / Protocol | `STEP-033` (`09_Evaluation/protocol.md v1.0.0`, `sha256: 26fede09...`) |",
        "| Evaluator Module | Frozen `src/opg/evaluator.py` (`sha256: 8fa2c6d8...`, all-point continuous AP, class-aware 1-to-1 greedy matching) |",
        "| Fixed Settings | `metric_conf_floor = 0.001`, class-aware `nms_iou = 0.65`, `agnostic_nms = false`, `max_det = 300`, `matching_iou = 0.50` & `[0.50:0.05:0.95]` |",
        "| Operating Threshold | Validation-only frozen `conf_op` (`FREEZE0001`) + protocol fallback `conf = 0.25` reference |",
        "| Uncertainty | `1,000`-resample **`GroupID` cluster bootstrap `95% CI`** (`seed = 20261131`) |",
        "",
        "---",
        "",
        "## 1. Master Held-Out In-Domain & External-Hospital Scoreboard (`EVAL0001–EVAL0014`)",
        "",
        "| `EvalID` | `ModelID` (`Arch@imgsz`) | `Release:Partition` (`N` OPGs) | `conf_op` | `val mAP@50` | **Held-Out `mAP@0.50` (`95% CI`)** | **Held-Out `mAP@0.50:95` (`95% CI`)** | `Macro-P` | `Macro-R` | `Macro-F1` | `Micro-F1` (`@0.25`) |",
        "|---|---|---|---:|---:|---|---|---:|---:|---:|---:|",
    ]
    for ev in freeze["planned_evaluations"]:
        eid = ev["eval_id"]
        s = eval_summaries[eid]
        m = s["metrics_at_frozen_conf_op"]
        m25 = s["metrics_at_ref_conf_025"]
        c50 = s["bootstrap_95ci"]["ci_95"]["mAP@0.50"]
        c95 = s["bootstrap_95ci"]["ci_95"]["mAP@0.50:0.95"]
        bold = "**" if "winner" in s["role"] or s["role"] == "primary_trackA_external" else ""
        lines.append(
            f"| `{eid}` | {bold}`{s['model_id']}`{bold} (`{s['architecture']}@{s['imgsz']}`) | "
            f"`{s['release_id']}:{s['partition']}` (`{m['evaluated_images']}`) | `{s['frozen_conf_op']:.3f}` | "
            f"`{s['val_mAP50_reference']:.4f}` | "
            f"{bold}`{m['mAP@0.50']:.4f}`{bold} (`[{c50['lo']:.4f}, {c50['hi']:.4f}]`) | "
            f"{bold}`{m['mAP@0.50:0.95']:.4f}`{bold} (`[{c95['lo']:.4f}, {c95['hi']:.4f}]`) | "
            f"`{fmt_opt(m['macro_precision'])}` | `{fmt_opt(m['macro_recall'])}` | `{fmt_opt(m['macro_f1'])}` | "
            f"`{fmt_opt(m['micro_f1'])}` (`{fmt_opt(m25['micro_f1'])}`) |"
        )

    # TrackC dual-reporting callout
    s10 = eval_summaries["EVAL0010"]
    d5 = s10["trackC_5class_pathology_dual"]["metrics"]
    b5 = s10["trackC_5class_pathology_dual"]["bootstrap_95ci"]["ci_95"]["mAP@0.50"]
    b5_95 = s10["trackC_5class_pathology_dual"]["bootstrap_95ci"]["ci_95"]["mAP@0.50:0.95"]
    lines.extend(
        [
            "",
            f"> **Track C (`REL0003` Dhaka) Dual Reporting (`DEC0013`):**",
            f"> - **6-Class (`0..5`, incl. selective `Healthy_Tooth`):** `mAP@0.50 = {s10['metrics_at_frozen_conf_op']['mAP@0.50']:.4f}`, `mAP@0.50:0.95 = {s10['metrics_at_frozen_conf_op']['mAP@0.50:0.95']:.4f}`",
            f"> - **5-Class Pathology Only (`0..4`):** `mAP@0.50 = {d5['mAP@0.50']:.4f}` (`95% CI [{b5['lo']:.4f}, {b5['hi']:.4f}]`), `mAP@0.50:0.95 = {d5['mAP@0.50:0.95']:.4f}` (`95% CI [{b5_95['lo']:.4f}, {b5_95['hi']:.4f}]`), `Macro-F1 = {fmt_opt(d5['macro_f1'])}` (note `Fractured_Tooth` has only `GT = {d5['per_class'][3]['gt_count']}` boxes on test).",
            "",
            "---",
            "",
            "## 2. Per-Class Held-Out Breakdown for All `6` Frozen Track Winners",
            "",
        ]
    )

    winner_evals = ["EVAL0001", "EVAL0002", "EVAL0009", "EVAL0010", "EVAL0011", "EVAL0013", "EVAL0014"]
    for eid in winner_evals:
        s = eval_summaries[eid]
        m = s["metrics_at_frozen_conf_op"]
        lines.extend(
            [
                f"### `{eid}` — `{s['model_id']}` (`{s['architecture']}@{s['imgsz']}`, `{s['track_id']}`, `{s['release_id']}:{s['partition']}`, `conf_op={s['frozen_conf_op']:.3f}`)",
                "",
                "| `ID` | Class Name | `GT` | `TP` | `FP` | `FN` | `Precision` | `Recall` | `F1` | **`AP@0.50`** | **`AP@0.50:95`** |",
                "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for cid in sorted(m["per_class"].keys()):
            c = m["per_class"][cid]
            lines.append(
                f"| `{cid}` | `{c['class_name']}` | `{c['gt_count']}` | `{c['tp_op']}` | `{c['fp_op']}` | `{c['fn_op']}` | "
                f"`{fmt_opt(c['precision'])}` | `{fmt_opt(c['recall'])}` | `{fmt_opt(c['f1'])}` | "
                f"**`{fmt_opt(c['ap'])}`** | `{fmt_opt(c.get('ap_50_95'))}` |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 3. Zero-Shot Cross-Country Domain-Shift Bridges (`HC01–HC05`, `UD15` / `RQ1`)",
            "",
            "| `BridgeID` | Source Model (`Track`) | Target `test` Cohort | Harmonized Concept | `GT` Boxes | `Precision` | `Recall` | `F1` | **`AP@0.50`** | **`AP@0.50:95`** |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for xr in xshift_rows:
        for cn, c in xr["per_concept"].items():
            lines.append(
                f"| `{xr['bridge_id']}` | `{xr['source_model_id']}` (`{xr['source_track']}`) | "
                f"`{xr['target_release_id']}:{xr['target_partition']}` (`{xr['target_track']}`) | `{cn}` | `{c['gt_count']}` | "
                f"`{fmt_opt(c['precision'])}` | `{fmt_opt(c['recall'])}` | `{fmt_opt(c['f1'])}` | "
                f"**`{fmt_opt(c['ap'])}`** | `{fmt_opt(c.get('ap_50_95'))}` |"
            )

    (ROOT / "09_Evaluation" / "step033_final_metrics_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n[ALL DONE] STEP-033 complete! Saved 09_Evaluation/step033_final_metrics_report.md & updated evaluation_registry.csv.")


if __name__ == "__main__":
    main()
