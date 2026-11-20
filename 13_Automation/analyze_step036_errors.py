"""Systematic Error Taxonomy (TIDE-style), Size-Bucket Recall, Cross-Class Confusion Matrix,
and Non-Cherry-Picked Case Sampling + Off-Git Visual Review Sheets (STEP-036 / T19 / G13).

Strictly read-only on frozen predictions and ground truth (zero label edits, zero threshold tuning).
Outputs:
  - 09_Evaluation/step036_error_taxonomy.json (Git-safe aggregate counts, confusions, size buckets, sampled case metadata)
  - 08_Checkpoints/artifacts/STEP032_outputs/error_review_sheets/EVAL####_review_sheet.jpg (off-Git visual overlays)
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import box_iou_xyxy, parse_yolo_line, yolo_norm_to_xyxy  # noqa: E402
from opg.data_loader import load_locked_partition_items  # noqa: E402

REL_META = {
    "REL0001": ("DS0001", "SPLIT0001", "ANNB0001", "TrackA"),
    "REL0002": ("DS0002", "SPLIT0002", "ANNB0002", "TrackB"),
    "REL0003": ("DS0003", "SPLIT0003", "ANNB0003", "TrackC"),
    "REL0004": ("DS0004", "SPLIT0004", "ANNB0004", "TrackD"),
    "REL0005": ("DS0005", "SPLIT0005", "ANNB0005", "TrackE"),
    "REL0006": ("DS0006", "SPLIT0006", "ANNB0006", "TrackF"),
}

PRIMARY_EVALS = ["EVAL0001", "EVAL0002", "EVAL0009", "EVAL0010", "EVAL0011", "EVAL0013", "EVAL0014"]


def load_track_classes() -> dict[str, list[str]]:
    by_track: dict[str, dict[int, str]] = {}
    with (ROOT / "04_Annotations" / "classes.csv").open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ti = row["TrainingIndex"].strip()
            if ":" in ti and ti.startswith("Track"):
                tr, idx = ti.split(":", 1)
                by_track.setdefault(tr, {})[int(idx)] = row["Name"].strip()
    return {t: [d[i] for i in sorted(d)] for t, d in by_track.items()}


def size_bucket(x0: float, y0: float, x1: float, y1: float, w: int, h: int) -> str:
    area_frac = ((x1 - x0) * (y1 - y0)) / max(float(w * h), 1.0)
    if area_frac < 0.002:
        return "small(<0.2%)"
    if area_frac < 0.010:
        return "medium(0.2-1.0%)"
    return "large(>=1.0%)"


def draw_case_panel(
    img_bgr: np.ndarray,
    gt_boxes: list[tuple[int, float, float, float, float]],
    pr_boxes: list[tuple[int, float, float, float, float, float]],
    cls_names: list[str],
    title: str,
    panel_w: int = 900,
    panel_h: int = 460,
) -> np.ndarray:
    h, w = img_bgr.shape[:2]
    scale = min(panel_w / float(w), (panel_h - 36) / float(h))
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    resized = cv2.resize(img_bgr, (nw, nh), interpolation=cv2.INTER_AREA)

    canvas = np.full((panel_h, panel_w, 3), 24, dtype=np.uint8)
    ox = (panel_w - nw) // 2
    oy = 36 + ((panel_h - 36 - nh) // 2)
    canvas[oy : oy + nh, ox : ox + nw] = resized

    # Draw GT boxes in GREEN
    for cid, x0, y0, x1, y1 in gt_boxes:
        p0 = (int(round(x0 * scale)) + ox, int(round(y0 * scale)) + oy)
        p1 = (int(round(x1 * scale)) + ox, int(round(y1 * scale)) + oy)
        cv2.rectangle(canvas, p0, p1, (60, 220, 60), 2)

    # Draw Pred boxes at conf_op in RED/ORANGE
    for cid, sc, x0, y0, x1, y1 in pr_boxes:
        p0 = (int(round(x0 * scale)) + ox, int(round(y0 * scale)) + oy)
        p1 = (int(round(x1 * scale)) + ox, int(round(y1 * scale)) + oy)
        cv2.rectangle(canvas, p0, p1, (50, 70, 245), 2)
        short_c = cls_names[cid].split("_", 1)[-1][:10]
        cv2.putText(canvas, f"{short_c}:{sc:.2f}", (p0[0], max(oy + 12, p0[1] - 3)), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (60, 190, 255), 1, cv2.LINE_AA)

    cv2.putText(canvas, title[:110], (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (240, 240, 240), 1, cv2.LINE_AA)
    return canvas


def main() -> None:
    freeze = json.loads((ROOT / "09_Evaluation" / "freeze_manifest.json").read_text(encoding="utf-8"))
    models_by_id = {m["model_id"]: m for m in freeze["frozen_models"]}
    evals_by_id = {e["eval_id"]: e for e in freeze["planned_evaluations"]}
    track_classes = load_track_classes()

    offgit_root = ROOT / "08_Checkpoints" / "artifacts" / "STEP032_outputs"
    sheets_dir = offgit_root / "error_review_sheets"
    sheets_dir.mkdir(parents=True, exist_ok=True)

    full_report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "step": "STEP-036",
        "sampling_policy": "Deterministic non-cherry-picked 4-category selection per primary winner EVAL: (1) Top Success [max TP with 0/min FP+FN], (2) Worst Miss [max FN_Complete_Miss], (3) Worst Background/Mimic FP [max FP_Bkg], (4) Worst Confusion/Localization Error [max FP_Cls + FP_Loc].",
        "evals": {},
    }

    for eid in PRIMARY_EVALS:
        ev = evals_by_id[eid]
        mid = ev["model_id"]
        rel_id = ev["release_id"]
        part = ev["partition"]
        fm = models_by_id[mid]
        conf_op = float(fm["frozen_conf_op"])
        ds_id, sp_id, ba_id, tr_id = REL_META[rel_id]
        cls_names = track_classes[tr_id]

        items = load_locked_partition_items(
            ROOT, dataset_id=ds_id, split_id=sp_id, batch_id=ba_id, track_id=tr_id, partition=part
        )
        items_by_id = {it.image_id: it for it in items}
        exp_dir = ROOT / "04_Annotations" / "exports" / f"{ba_id}_{tr_id}"
        ext_dir = ROOT / "03_Datasets" / "raw" / ds_id / "extracted"

        # Load predictions
        preds_all: dict[str, list[tuple[int, float, float, float, float, float]]] = {}
        with (offgit_root / "evals" / eid / "predictions.jsonl").open("r", encoding="utf-8") as pf:
            for line in pf:
                rec = json.loads(line)
                preds_all[rec["image_id"]] = [
                    (int(b[0]), float(b[1]), float(b[2]), float(b[3]), float(b[4]), float(b[5]))
                    for b in rec["boxes"]
                ]

        fp_counts = Counter()
        fn_counts = Counter()
        confusions = Counter()
        size_stats: dict[str, dict[str, int]] = {
            "small(<0.2%)": {"gt": 0, "tp": 0},
            "medium(0.2-1.0%)": {"gt": 0, "tp": 0},
            "large(>=1.0%)": {"gt": 0, "tp": 0},
        }
        empty_img_stats = {"reviewed_empty_count": 0, "empty_with_fp_op": 0, "total_fp_on_empty": 0}
        per_image_diag: list[dict[str, Any]] = []

        for it in items:
            iid = it.image_id
            gt_boxes: list[tuple[int, float, float, float, float]] = []
            for ln in (exp_dir / it.label_relpath).read_text(encoding="utf-8").splitlines():
                if ln.strip():
                    c, xc, yc, bw, bh = parse_yolo_line(ln.strip())
                    x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, it.width, it.height)
                    gt_boxes.append((c, x0, y0, x1, y1))

            pr_floor = preds_all[iid]
            pr_op = [p for p in pr_floor if p[1] >= conf_op]
            pr_low = [p for p in pr_floor if p[1] < conf_op]

            if len(gt_boxes) == 0:
                empty_img_stats["reviewed_empty_count"] += 1
                if len(pr_op) > 0:
                    empty_img_stats["empty_with_fp_op"] += 1
                    empty_img_stats["total_fp_on_empty"] += len(pr_op)

            # Match class-aware greedy at IoU=0.50 (identical to evaluator.py)
            gt_matched = [False] * len(gt_boxes)
            pr_status: list[str] = []
            pr_sorted = sorted(pr_op, key=lambda x: x[1], reverse=True)

            img_tp = 0
            img_fp_loc = 0
            img_fp_dup = 0
            img_fp_cls = 0
            img_fp_bkg = 0

            for pc, ps, px0, py0, px1, py1 in pr_sorted:
                p_xy = (px0, py0, px1, py1)
                best_iou_same_unmatched = -1.0
                best_gi = -1
                best_iou_same_matched = -1.0
                best_iou_other = -1.0
                best_other_cls = -1

                for gi, (gc, gx0, gy0, gx1, gy1) in enumerate(gt_boxes):
                    iou = box_iou_xyxy(p_xy, (gx0, gy0, gx1, gy1))
                    if gc == pc:
                        if not gt_matched[gi]:
                            if iou > best_iou_same_unmatched:
                                best_iou_same_unmatched = iou
                                best_gi = gi
                        else:
                            if iou > best_iou_same_matched:
                                best_iou_same_matched = iou
                    else:
                        if iou > best_iou_other:
                            best_iou_other = iou
                            best_other_cls = gc

                if best_gi >= 0 and best_iou_same_unmatched >= 0.50:
                    gt_matched[best_gi] = True
                    img_tp += 1
                    pr_status.append("TP")
                elif best_iou_same_matched >= 0.50:
                    fp_counts["FP_Dup"] += 1
                    img_fp_dup += 1
                    pr_status.append("FP_Dup")
                elif best_iou_same_unmatched >= 0.10:
                    fp_counts["FP_Loc"] += 1
                    img_fp_loc += 1
                    pr_status.append("FP_Loc")
                elif best_iou_other >= 0.10:
                    fp_counts["FP_Cls"] += 1
                    img_fp_cls += 1
                    confusions[(cls_names[best_other_cls], cls_names[pc])] += 1
                    pr_status.append("FP_Cls")
                else:
                    fp_counts["FP_Bkg"] += 1
                    img_fp_bkg += 1
                    pr_status.append("FP_Bkg")

            # Classify every GT box (TP vs FN sub-categories + size bucket)
            img_fn_score = 0
            img_fn_loc = 0
            img_fn_cls = 0
            img_fn_miss = 0
            for gi, (gc, gx0, gy0, gx1, gy1) in enumerate(gt_boxes):
                sb = size_bucket(gx0, gy0, gx1, gy1, it.width, it.height)
                size_stats[sb]["gt"] += 1
                if gt_matched[gi]:
                    size_stats[sb]["tp"] += 1
                    continue
                g_xy = (gx0, gy0, gx1, gy1)
                has_low_match = any(pc == gc and box_iou_xyxy((px0, py0, px1, py1), g_xy) >= 0.50 for pc, _, px0, py0, px1, py1 in pr_low)
                has_loc_op = any(pc == gc and box_iou_xyxy((px0, py0, px1, py1), g_xy) >= 0.10 for pc, _, px0, py0, px1, py1 in pr_op)
                has_cls_op = any(pc != gc and box_iou_xyxy((px0, py0, px1, py1), g_xy) >= 0.10 for pc, _, px0, py0, px1, py1 in pr_op)
                if has_loc_op:
                    fn_counts["FN_Loc_Only"] += 1
                    img_fn_loc += 1
                elif has_cls_op:
                    fn_counts["FN_Confused_Cls"] += 1
                    img_fn_cls += 1
                elif has_low_match:
                    fn_counts["FN_Missed_By_Score"] += 1
                    img_fn_score += 1
                else:
                    fn_counts["FN_Complete_Miss"] += 1
                    img_fn_miss += 1

            per_image_diag.append(
                {
                    "image_id": iid,
                    "group_id": it.group_id,
                    "gt": len(gt_boxes),
                    "pred_op": len(pr_op),
                    "tp": img_tp,
                    "fp_total": img_fp_loc + img_fp_dup + img_fp_cls + img_fp_bkg,
                    "fp_loc": img_fp_loc,
                    "fp_dup": img_fp_dup,
                    "fp_cls": img_fp_cls,
                    "fp_bkg": img_fp_bkg,
                    "fn_total": img_fn_score + img_fn_loc + img_fn_cls + img_fn_miss,
                    "fn_miss": img_fn_miss,
                    "fn_score": img_fn_score,
                    "fn_loc": img_fn_loc,
                    "fn_cls": img_fn_cls,
                    "gt_boxes": gt_boxes,
                    "pr_op": pr_sorted,
                }
            )

        # Deterministic non-cherry-picked 4-category case sampling (disjoint where possible)
        chosen: list[tuple[str, dict[str, Any]]] = []
        used_ids: set[str] = set()

        def pick(cat: str, key_fn: Any) -> None:
            cands = [d for d in per_image_diag if d["image_id"] not in used_ids]
            if not cands:
                cands = per_image_diag
            best = max(cands, key=key_fn)
            used_ids.add(best["image_id"])
            chosen.append((cat, best))

        pick("Top_Success", lambda d: (d["tp"] - (d["fp_total"] + d["fn_total"]), d["tp"], -d["fp_total"]))
        pick("Worst_Complete_Miss", lambda d: (d["fn_miss"], d["fn_total"], d["gt"]))
        pick("Worst_Background_Mimic_FP", lambda d: (d["fp_bkg"], d["fp_total"], d["pred_op"]))
        pick("Worst_Class_or_Loc_Error", lambda d: (d["fp_cls"] + d["fp_loc"], d["fp_cls"], d["fp_loc"]))

        # Render 2x2 off-Git diagnostic review sheet for visual verification
        panels = []
        sampled_meta = []
        for cat, d in chosen:
            it = items_by_id[d["image_id"]]
            raw_b = np.fromfile(str(ext_dir / it.raw_relpath), dtype=np.uint8)
            im_bgr = cv2.imdecode(raw_b, cv2.IMREAD_COLOR)
            title = (
                f"{cat} | {d['image_id']} ({it.width}x{it.height}) | "
                f"GT={d['gt']} TP={d['tp']} FP={d['fp_total']}(Bkg={d['fp_bkg']},Loc={d['fp_loc']},Cls={d['fp_cls']},Dup={d['fp_dup']}) "
                f"FN={d['fn_total']}(Miss={d['fn_miss']},Score={d['fn_score']})"
            )
            panels.append(draw_case_panel(im_bgr, d["gt_boxes"], d["pr_op"], cls_names, title))
            sampled_meta.append(
                {
                    "category": cat,
                    "image_id": d["image_id"],
                    "group_id": d["group_id"],
                    "dims": f"{it.width}x{it.height}",
                    "gt": d["gt"],
                    "pred_op": d["pred_op"],
                    "tp": d["tp"],
                    "fp_total": d["fp_total"],
                    "fp_breakdown": {"loc": d["fp_loc"], "dup": d["fp_dup"], "cls": d["fp_cls"], "bkg": d["fp_bkg"]},
                    "fn_total": d["fn_total"],
                    "fn_breakdown": {"complete_miss": d["fn_miss"], "missed_by_score": d["fn_score"], "loc_only": d["fn_loc"], "confused_cls": d["fn_cls"]},
                }
            )
        row1 = np.hstack([panels[0], panels[1]])
        row2 = np.hstack([panels[2], panels[3]])
        sheet = np.vstack([row1, row2])
        cv2.imwrite(str(sheets_dir / f"{eid}_review_sheet.jpg"), sheet, [int(cv2.IMWRITE_JPEG_QUALITY), 88])

        size_recall = {
            k: {
                "gt": v["gt"],
                "tp": v["tp"],
                "recall": round(v["tp"] / float(v["gt"]), 4) if v["gt"] > 0 else None,
            }
            for k, v in size_stats.items()
        }
        top_conf = [{"gt_class": g, "pred_class": p, "count": cnt} for (g, p), cnt in confusions.most_common(8)]
        tot_fp = sum(fp_counts.values())
        tot_fn = sum(fn_counts.values())
        full_report["evals"][eid] = {
            "model_id": mid,
            "track_id": tr_id,
            "release_partition": f"{rel_id}:{part}",
            "frozen_conf_op": conf_op,
            "total_images": len(items),
            "reviewed_empty": empty_img_stats,
            "fp_total": tot_fp,
            "fp_taxonomy": dict(fp_counts),
            "fn_total": tot_fn,
            "fn_taxonomy": dict(fn_counts),
            "size_bucket_recall": size_recall,
            "top_cross_class_confusions": top_conf,
            "sampled_cases": sampled_meta,
            "offgit_review_sheet": f"08_Checkpoints/artifacts/STEP032_outputs/error_review_sheets/{eid}_review_sheet.jpg",
        }
        print(
            f"[T19] {eid} ({mid} {tr_id}:{part}) | FP={tot_fp} (Bkg={fp_counts['FP_Bkg']}, Loc={fp_counts['FP_Loc']}, Cls={fp_counts['FP_Cls']}, Dup={fp_counts['FP_Dup']}) | "
            f"FN={tot_fn} (Miss={fn_counts['FN_Complete_Miss']}, Score={fn_counts['FN_Missed_By_Score']}, Loc={fn_counts['FN_Loc_Only']}, Cls={fn_counts['FN_Confused_Cls']}) | "
            f"SizeRec: S={size_recall['small(<0.2%)']['recall']} M={size_recall['medium(0.2-1.0%)']['recall']} L={size_recall['large(>=1.0%)']['recall']}"
        )

    out_json = ROOT / "09_Evaluation" / "step036_error_taxonomy.json"
    out_json.write_text(json.dumps(full_report, indent=2) + "\n", encoding="utf-8")
    print(f"\n[DONE] Saved {out_json} & 7 off-Git 2x2 visual review sheets.")


if __name__ == "__main__":
    main()
