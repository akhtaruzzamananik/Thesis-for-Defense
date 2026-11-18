"""Protocol-controlled deterministic detection evaluator (STEP-025 / OS §7.2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np

from opg.annotation_schema import box_iou_xyxy


@dataclass(frozen=True)
class DetectionBox:
    """Ground-truth or predicted detection box in common pixel coordinates."""

    class_id: int
    xyxy: tuple[float, float, float, float]
    score: float = 1.0


def compute_ap_continuous(recalls: Sequence[float], precisions: Sequence[float]) -> float:
    """Compute exact all-point continuous precision-recall envelope area (COCO/VOC2010 standard)."""
    if not recalls:
        return 0.0
    mrec = np.concatenate(([0.0], np.asarray(recalls, dtype=np.float64), [1.0]))
    mpre = np.concatenate(([1.0], np.asarray(precisions, dtype=np.float64), [0.0]))
    for i in range(len(mpre) - 2, -1, -1):
        mpre[i] = max(mpre[i], mpre[i + 1])
    idx = np.where(mrec[1:] != mrec[:-1])[0]
    return float(np.sum((mrec[idx + 1] - mrec[idx]) * mpre[idx + 1]))


def _evaluate_class_at_iou(
    gt_by_img: dict[str, list[DetectionBox]],
    pred_by_img: dict[str, list[DetectionBox]],
    class_id: int,
    iou_threshold: float,
    operating_conf: float,
) -> dict[str, Any]:
    """Evaluate one class across all covered images at a single IoU threshold."""
    gt_per_img: dict[str, list[tuple[float, float, float, float]]] = {}
    total_gt = 0
    for img_id, boxes in gt_by_img.items():
        cls_boxes = [b.xyxy for b in boxes if b.class_id == class_id]
        gt_per_img[img_id] = cls_boxes
        total_gt += len(cls_boxes)

    # Gather predictions across ALL covered images (including reviewed_empty images!)
    preds: list[tuple[float, str, tuple[float, float, float, float]]] = []
    for img_id in gt_by_img:
        for pb in pred_by_img.get(img_id, []):
            if pb.class_id == class_id:
                preds.append((pb.score, img_id, pb.xyxy))
    preds.sort(key=lambda x: x[0], reverse=True)

    # Absent ground-truth class rule (OS §7.2): exclude from mAP averaging, disclose FP count if any
    if total_gt == 0:
        fp_op = sum(1 for sc, _, _ in preds if sc >= operating_conf)
        return {
            "class_id": class_id,
            "gt_count": 0,
            "pred_count_total": len(preds),
            "tp_op": 0,
            "fp_op": fp_op,
            "fn_op": 0,
            "precision": 0.0 if fp_op > 0 else None,
            "recall": None,
            "f1": None,
            "ap": None,
            "eligible": False,
        }

    used_gt: dict[str, list[bool]] = {img_id: [False] * len(b_list) for img_id, b_list in gt_per_img.items()}
    tp_flags = np.zeros(len(preds), dtype=np.float64)
    fp_flags = np.zeros(len(preds), dtype=np.float64)
    scores_arr = np.zeros(len(preds), dtype=np.float64)

    for idx, (score, img_id, p_xyxy) in enumerate(preds):
        scores_arr[idx] = score
        gt_list = gt_per_img.get(img_id, [])
        best_iou = -1.0
        best_gt_idx = -1
        for g_idx, g_xyxy in enumerate(gt_list):
            if used_gt[img_id][g_idx]:
                continue
            iou = box_iou_xyxy(p_xyxy, g_xyxy)
            if iou >= iou_threshold and iou > best_iou:
                best_iou = iou
                best_gt_idx = g_idx
        if best_gt_idx >= 0:
            used_gt[img_id][best_gt_idx] = True
            tp_flags[idx] = 1.0
        else:
            fp_flags[idx] = 1.0

    cum_tp = np.cumsum(tp_flags)
    cum_fp = np.cumsum(fp_flags)
    recalls = cum_tp / float(total_gt)
    precisions = cum_tp / np.maximum(cum_tp + cum_fp, 1e-12)
    ap = compute_ap_continuous(recalls.tolist(), precisions.tolist())

    # Operating-point counts (score >= operating_conf)
    op_mask = scores_arr >= operating_conf
    tp_op = int(tp_flags[op_mask].sum())
    fp_op = int(fp_flags[op_mask].sum())
    fn_op = int(total_gt - tp_op)
    prec_op = (tp_op / float(tp_op + fp_op)) if (tp_op + fp_op) > 0 else None
    rec_op = tp_op / float(total_gt)
    f1_op = (
        (2.0 * prec_op * rec_op / (prec_op + rec_op))
        if (prec_op is not None and (prec_op + rec_op) > 0.0)
        else (0.0 if prec_op is not None else None)
    )

    return {
        "class_id": class_id,
        "gt_count": total_gt,
        "pred_count_total": len(preds),
        "tp_op": tp_op,
        "fp_op": fp_op,
        "fn_op": fn_op,
        "precision": round(prec_op, 6) if prec_op is not None else None,
        "recall": round(rec_op, 6),
        "f1": round(f1_op, 6) if f1_op is not None else None,
        "ap": round(ap, 6),
        "eligible": True,
    }


def evaluate_predictions(
    ground_truths_by_image: dict[str, Sequence[DetectionBox]],
    predictions_by_image: dict[str, Sequence[DetectionBox]],
    class_names: Sequence[str],
    *,
    matching_ious: Sequence[float] = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95),
    operating_conf: float = 0.25,
    score_floor: float = 0.001,
    max_detections: int = 300,
) -> dict[str, Any]:
    """Evaluate predictions under protocol 09_Evaluation/protocol.md retaining empty images and absent classes."""
    if not ground_truths_by_image:
        raise ValueError("ground_truths_by_image cannot be empty")

    gt_norm: dict[str, list[DetectionBox]] = {img_id: list(boxes) for img_id, boxes in ground_truths_by_image.items()}
    pred_norm: dict[str, list[DetectionBox]] = {}
    empty_images_count = sum(1 for boxes in gt_norm.values() if len(boxes) == 0)

    for img_id in gt_norm:
        raw_preds = [p for p in predictions_by_image.get(img_id, []) if p.score >= score_floor]
        raw_preds.sort(key=lambda p: p.score, reverse=True)
        pred_norm[img_id] = raw_preds[:max_detections]

    per_class_50: dict[int, dict[str, Any]] = {}
    ap_by_class_ious: dict[int, list[float]] = {}
    eligible_classes: list[int] = []
    absent_classes: list[int] = []

    for cid in range(len(class_names)):
        res_50 = _evaluate_class_at_iou(gt_norm, pred_norm, cid, 0.50, operating_conf)
        res_50["class_name"] = class_names[cid]
        per_class_50[cid] = res_50
        if not res_50["eligible"]:
            absent_classes.append(cid)
            continue
        eligible_classes.append(cid)
        aps: list[float] = []
        for iou_thr in matching_ious:
            if abs(iou_thr - 0.50) < 1e-9:
                aps.append(float(res_50["ap"]))
            else:
                r_iou = _evaluate_class_at_iou(gt_norm, pred_norm, cid, float(iou_thr), operating_conf)
                aps.append(float(r_iou["ap"]))
        ap_by_class_ious[cid] = aps
        res_50["ap_50_95"] = round(float(np.mean(aps)), 6) if aps else None

    map50 = (
        round(float(np.mean([per_class_50[c]["ap"] for c in eligible_classes])), 6) if eligible_classes else None
    )
    map50_95 = (
        round(float(np.mean([per_class_50[c]["ap_50_95"] for c in eligible_classes])), 6)
        if eligible_classes
        else None
    )

    # Micro & macro P/R/F1 at operating_conf
    total_tp = sum(int(per_class_50[c]["tp_op"]) for c in range(len(class_names)))
    total_fp = sum(int(per_class_50[c]["fp_op"]) for c in range(len(class_names)))
    total_fn = sum(int(per_class_50[c]["fn_op"]) for c in range(len(class_names)))
    micro_p = (total_tp / float(total_tp + total_fp)) if (total_tp + total_fp) > 0 else None
    micro_r = (total_tp / float(total_tp + total_fn)) if (total_tp + total_fn) > 0 else None
    micro_f1 = (
        (2.0 * micro_p * micro_r / (micro_p + micro_r))
        if (micro_p is not None and micro_r is not None and (micro_p + micro_r) > 0.0)
        else (0.0 if (micro_p is not None and micro_r is not None) else None)
    )

    macro_p_vals = [per_class_50[c]["precision"] for c in eligible_classes if per_class_50[c]["precision"] is not None]
    macro_r_vals = [per_class_50[c]["recall"] for c in eligible_classes if per_class_50[c]["recall"] is not None]
    macro_f1_vals = [per_class_50[c]["f1"] for c in eligible_classes if per_class_50[c]["f1"] is not None]

    return {
        "evaluated_images": len(gt_norm),
        "reviewed_empty_images": empty_images_count,
        "total_classes": len(class_names),
        "eligible_class_count": len(eligible_classes),
        "absent_class_ids": absent_classes,
        "operating_conf": operating_conf,
        "score_floor": score_floor,
        "max_detections": max_detections,
        "mAP@0.50": map50,
        "mAP@0.50:0.95": map50_95,
        "micro_precision": round(micro_p, 6) if micro_p is not None else None,
        "micro_recall": round(micro_r, 6) if micro_r is not None else None,
        "micro_f1": round(micro_f1, 6) if micro_f1 is not None else None,
        "macro_precision": round(float(np.mean(macro_p_vals)), 6) if macro_p_vals else None,
        "macro_recall": round(float(np.mean(macro_r_vals)), 6) if macro_r_vals else None,
        "macro_f1": round(float(np.mean(macro_f1_vals)), 6) if macro_f1_vals else None,
        "total_tp": total_tp,
        "total_fp": total_fp,
        "total_fn": total_fn,
        "per_class": per_class_50,
    }


def find_optimal_operating_conf(
    ground_truths_by_image: dict[str, Sequence[DetectionBox]],
    predictions_by_image: dict[str, Sequence[DetectionBox]],
    class_names: Sequence[str],
    candidates: Sequence[float] = (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70),
) -> tuple[float, float]:
    """Select optimal operating confidence on validation split only by maximizing macro-F1."""
    best_conf = 0.25
    best_f1 = -1.0
    for conf in candidates:
        res = evaluate_predictions(
            ground_truths_by_image,
            predictions_by_image,
            class_names,
            matching_ious=(0.50,),
            operating_conf=float(conf),
        )
        f1 = res["macro_f1"] if res["macro_f1"] is not None else 0.0
        if f1 > best_f1:
            best_f1 = f1
            best_conf = float(conf)
    return best_conf, round(best_f1, 6)
