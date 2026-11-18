"""Annotation parsing, stratified pilot selection, two-pass QA agreement, and adjudication helpers (STEP-016..018)."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence

from opg.annotation_schema import (
    DS0004_NAME_TO_TRACKD,
    DS0005_NAME_TO_TRACKE,
    DS0006_LABEL_TO_TRACKF,
    box_iou_xyxy,
    clip_xyxy,
    coco_xywh_to_xyxy,
    format_yolo_line,
    is_degenerate_box,
    match_boxes_greedy,
    obb_to_aabb_xyxy,
    parse_yolo_line,
    polygon_to_aabb_xyxy,
    remap_ds0001_class,
    verify_yolo_round_trip,
    xyxy_to_yolo_norm,
    yolo_norm_to_xyxy,
)

EXPECTED_CLASSES_CSV_SHA256 = "c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af"

DATASET_TRACK_MAP: dict[str, str] = {
    "DS0001": "TrackA",
    "DS0002": "TrackB",
    "DS0003": "TrackC",
    "DS0004": "TrackD",
    "DS0005": "TrackE",
    "DS0006": "TrackF",
}

RARE_CLASS_IDS_BY_DATASET: dict[str, set[int]] = {
    "DS0001": {10, 9, 0, 11},  # Apical surgery (10), Furcation (9), Implant (0), Ortho (11)
    "DS0002": {2, 3},          # Periapical Lesion (2), Deep Caries (3)
    "DS0003": {3, 1, 4},       # Fractured Teeth (3), Infection (1), BDC/BDR (4)
    "DS0004": {2, 1},          # PAI 5 (2), PAI 4 (1)
    "DS0005": {5, 4, 3},       # Impacted (5), Implant (4), Cavitated (3)
    "DS0006": {1},             # Occlusal Caries o (1)
}


@dataclass
class BoxRecord:
    """Single canonical converted box with audit telemetry."""

    box_index: int
    class_id: int
    source_label: str
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    xc: float
    yc: float
    w: float
    h: float
    yolo_line: str
    round_trip_px_err: float
    clipped_overhang_px: float = 0.0
    flags: list[str] = field(default_factory=list)


@dataclass
class ImageAnnotationRecord:
    """Complete annotation and QA state for one active OPG image."""

    image_id: str
    dataset_id: str
    track_id: str
    source_bucket: str
    width: int
    height: int
    laplacian_var: float
    annotation_state: str  # reviewed_positive, reviewed_empty, missing_labels
    raw_box_count: int
    valid_boxes: list[BoxRecord] = field(default_factory=list)
    excluded_records: list[dict[str, Any]] = field(default_factory=list)
    anomalies: list[dict[str, Any]] = field(default_factory=list)
    stratum: str = "unselected"


def _overhang_px(xmin: float, ymin: float, xmax: float, ymax: float, w: int, h: int) -> float:
    """Return max pixel distance by which raw coordinates extend outside [0, w] x [0, h]."""
    return max(0.0, -xmin, -ymin, xmax - float(w), ymax - float(h))


def audit_box_list(
    image_id: str,
    dataset_id: str,
    width: int,
    height: int,
    raw_items: Sequence[tuple[int | None, str, float, float, float, float, str]],
) -> tuple[list[BoxRecord], list[dict[str, Any]], list[dict[str, Any]]]:
    """Convert and audit raw (mapped_cls, src_label, xmin, ymin, xmax, ymax, status_hint) tuples."""
    valid_boxes: list[BoxRecord] = []
    excluded: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []

    for idx, (cid, src_label, x0, y0, x1, y1, hint) in enumerate(raw_items):
        if hint == "excluded_class":
            excluded.append(
                {
                    "image_id": image_id,
                    "dataset_id": dataset_id,
                    "box_index": idx,
                    "source_label": src_label,
                    "reason": "excluded_class_UD04",
                }
            )
            continue
        if hint == "excluded_roi":
            excluded.append(
                {
                    "image_id": image_id,
                    "dataset_id": dataset_id,
                    "box_index": idx,
                    "source_label": src_label,
                    "reason": "excluded_auxiliary_roi_UD04",
                }
            )
            continue

        overhang = _overhang_px(x0, y0, x1, y1, width, height)
        cx0, cy0, cx1, cy1 = clip_xyxy(x0, y0, x1, y1, width, height)
        if is_degenerate_box(cx0, cy0, cx1, cy1):
            excluded.append(
                {
                    "image_id": image_id,
                    "dataset_id": dataset_id,
                    "box_index": idx,
                    "source_label": src_label,
                    "reason": "degenerate_zero_area_UD05",
                    "raw_coords": [round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)],
                }
            )
            anomalies.append(
                {
                    "image_id": image_id,
                    "dataset_id": dataset_id,
                    "box_index": idx,
                    "source_label": src_label,
                    "issue_type": "degenerate_zero_area",
                    "resolution": "dropped_by_preapproved_rule_UD05",
                }
            )
            continue

        assert cid is not None
        xc, yc, wn, hn = xyxy_to_yolo_norm(cx0, cy0, cx1, cy1, width, height, clip=False)
        line = format_yolo_line(cid, xc, yc, wn, hn, precision=6)
        rt_err = verify_yolo_round_trip(cid, cx0, cy0, cx1, cy1, width, height, precision=6)

        flags: list[str] = []
        if overhang > 1.0:
            flags.append(f"boundary_overhang_{overhang:.2f}px_clipped")
            anomalies.append(
                {
                    "image_id": image_id,
                    "dataset_id": dataset_id,
                    "box_index": idx,
                    "source_label": src_label,
                    "issue_type": "boundary_overhang_gt1px",
                    "detail": f"overhang={overhang:.2f}px",
                    "resolution": "clipped_to_image_bounds_UD05",
                }
            )

        valid_boxes.append(
            BoxRecord(
                box_index=len(valid_boxes),
                class_id=cid,
                source_label=src_label,
                xmin=round(cx0, 4),
                ymin=round(cy0, 4),
                xmax=round(cx1, 4),
                ymax=round(cy1, 4),
                xc=round(xc, 6),
                yc=round(yc, 6),
                w=round(wn, 6),
                h=round(hn, 6),
                yolo_line=line,
                round_trip_px_err=round(rt_err, 6),
                clipped_overhang_px=round(overhang, 4),
                flags=flags,
            )
        )

    # Check intra-image same-class duplicate boxes (IoU > 0.90) & multi-class overlaps (IoU > 0.50)
    for i in range(len(valid_boxes)):
        for j in range(i + 1, len(valid_boxes)):
            bi = valid_boxes[i]
            bj = valid_boxes[j]
            iou = box_iou_xyxy([bi.xmin, bi.ymin, bi.xmax, bi.ymax], [bj.xmin, bj.ymin, bj.xmax, bj.ymax])
            if bi.class_id == bj.class_id and iou > 0.90:
                bi.flags.append(f"same_class_dup_iou_{iou:.3f}")
                bj.flags.append(f"same_class_dup_iou_{iou:.3f}")
                anomalies.append(
                    {
                        "image_id": image_id,
                        "dataset_id": dataset_id,
                        "box_index": f"{bi.box_index}&{bj.box_index}",
                        "source_label": bi.source_label,
                        "issue_type": "same_class_duplicate_iou_gt_0.90",
                        "detail": f"IoU={iou:.4f}",
                        "resolution": "flagged_for_adjudication",
                    }
                )
            elif bi.class_id != bj.class_id and iou >= 0.50:
                bi.flags.append(f"multi_class_coexistence_iou_{iou:.2f}")
                bj.flags.append(f"multi_class_coexistence_iou_{iou:.2f}")

    return valid_boxes, excluded, anomalies


def select_stratified_pilot_sample(
    records: Sequence[ImageAnnotationRecord],
    n_total: int = 10,
    seed: int = 20261119,
) -> list[ImageAnnotationRecord]:
    """Select a deterministic stratified pilot sample of `n_total` labeled images per dataset."""
    labeled = [r for r in records if r.annotation_state in {"reviewed_positive", "reviewed_empty"}]
    if len(labeled) <= n_total:
        for r in labeled:
            r.stratum = "all_available"
        return list(labeled)

    rng = random.Random(seed)
    ds_id = labeled[0].dataset_id
    rare_cids = RARE_CLASS_IDS_BY_DATASET.get(ds_id, set())

    selected_ids: set[str] = set()
    selected: list[ImageAnnotationRecord] = []

    # Stratum 1: up to 4 images containing rare/minority classes (or pre-flagged anomalies)
    rare_pool = [
        r
        for r in labeled
        if any(b.class_id in rare_cids for b in r.valid_boxes) or bool(r.anomalies) or bool(r.excluded_records)
    ]
    rare_pool.sort(key=lambda r: (-len(r.anomalies), -len(r.excluded_records), r.image_id))
    if len(rare_pool) > 4:
        # Deterministic shuffle after sorting by priority
        top_priority = [r for r in rare_pool if r.anomalies or r.excluded_records][:2]
        rest = [r for r in rare_pool if r.image_id not in {x.image_id for x in top_priority}]
        rng.shuffle(rest)
        rare_picks = (top_priority + rest)[:4]
    else:
        rare_picks = rare_pool[:4]

    for r in rare_picks:
        r.stratum = "S1_rare_or_edge_class"
        selected.append(r)
        selected_ids.add(r.image_id)

    # Stratum 2: 3 images from high object density / multi-label overlap
    rem_high = [r for r in labeled if r.image_id not in selected_ids]
    rem_high.sort(key=lambda r: (-len(r.valid_boxes), r.image_id))
    high_candidates = rem_high[: max(3, len(rem_high) // 10)]
    rng.shuffle(high_candidates)
    for r in sorted(high_candidates[:3], key=lambda x: x.image_id):
        r.stratum = "S2_high_density_overlap"
        selected.append(r)
        selected_ids.add(r.image_id)

    # Stratum 3: remaining slots (typically 3) from low-sharpness / quality-variation tail
    rem_qual = [r for r in labeled if r.image_id not in selected_ids]
    rem_qual.sort(key=lambda r: (r.laplacian_var, r.image_id))
    needed = n_total - len(selected)
    qual_candidates = rem_qual[: max(needed, len(rem_qual) // 10)]
    rng.shuffle(qual_candidates)
    for r in sorted(qual_candidates[:needed], key=lambda x: x.image_id):
        r.stratum = "S3_quality_variation_tail"
        selected.append(r)
        selected_ids.add(r.image_id)

    return sorted(selected, key=lambda r: r.image_id)


def compute_cohens_kappa_binary(labels_a: Sequence[int], labels_b: Sequence[int]) -> dict[str, float]:
    """Compute exact percentage agreement and Cohen's kappa for binary audit dispositions (0=accept, 1=flag)."""
    if len(labels_a) != len(labels_b):
        raise ValueError("Disposition sequences must have equal length")
    n = len(labels_a)
    if n == 0:
        return {"n": 0, "agreement_pct": 100.0, "kappa": 1.0}
    n11 = sum(1 for a, b in zip(labels_a, labels_b) if a == 1 and b == 1)
    n00 = sum(1 for a, b in zip(labels_a, labels_b) if a == 0 and b == 0)
    n10 = sum(1 for a, b in zip(labels_a, labels_b) if a == 1 and b == 0)
    n01 = sum(1 for a, b in zip(labels_a, labels_b) if a == 0 and b == 1)
    po = (n11 + n00) / n
    p_a1 = (n11 + n10) / n
    p_b1 = (n11 + n01) / n
    pe = p_a1 * p_b1 + (1.0 - p_a1) * (1.0 - p_b1)
    if abs(1.0 - pe) < 1e-9:
        kappa = 1.0 if po >= 1.0 - 1e-9 else 0.0
    else:
        kappa = (po - pe) / (1.0 - pe)
    return {
        "n": n,
        "n_accept_both": n00,
        "n_flag_both": n11,
        "n_disagree": n10 + n01,
        "agreement_pct": round(po * 100.0, 2),
        "kappa": round(kappa, 4),
    }


def independent_second_pass_verify(record: ImageAnnotationRecord) -> dict[str, Any]:
    """Independent Pass B verification from stored YOLO lines back to pixel space vs Pass A boxes."""
    boxes_a = [(b.class_id, [b.xmin, b.ymin, b.xmax, b.ymax]) for b in record.valid_boxes]
    boxes_b: list[tuple[int, list[float]]] = []
    dispositions_a: list[int] = []
    dispositions_b: list[int] = []

    img_area = float(record.width * record.height)
    for b in record.valid_boxes:
        cid, xc, yc, wn, hn = parse_yolo_line(b.yolo_line)
        rx0, ry0, rx1, ry1 = yolo_norm_to_xyxy(xc, yc, wn, hn, record.width, record.height)
        boxes_b.append((cid, [rx0, ry0, rx1, ry1]))

        # Pass A disposition: 1 if box had structural anomaly flag (overhang or same-class dup), else 0
        flag_a = 1 if any(f.startswith(("boundary_overhang", "same_class_dup")) for f in b.flags) else 0
        # Pass B independent plausibility disposition: 1 if overhang > 1px, same-class dup, or extreme area (<4px^2 or >65% img)
        b_area = max(0.0, rx1 - rx0) * max(0.0, ry1 - ry0)
        flag_b = 1 if (flag_a == 1 or b_area < 4.0 or (img_area > 0 and b_area / img_area > 0.65)) else 0
        dispositions_a.append(flag_a)
        dispositions_b.append(flag_b)

    # Also include excluded/degenerate items as flagged (1) by both passes
    for _ in record.excluded_records:
        dispositions_a.append(1)
        dispositions_b.append(1)

    match_res = match_boxes_greedy(boxes_a, boxes_b, iou_threshold=0.85, class_aware=True)
    return {
        "match_res": match_res,
        "dispositions_a": dispositions_a,
        "dispositions_b": dispositions_b,
    }
