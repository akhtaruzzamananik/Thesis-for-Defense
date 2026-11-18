"""Canonical annotation coordinate conversion, class-map hashing, and QA matching (STEP-015 / G05)."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class CanonicalBox:
    """Normalized and pixel-space axis-aligned bounding box in canonical top-left (0,0) frame."""

    class_id: int
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    xc_norm: float
    yc_norm: float
    w_norm: float
    h_norm: float
    source_format: str = "yolo_aabb"


# Track A (DS0001 UMFIH): source class 11 (Root resorption, N=5) excluded; 12->11, 13->12
DS0001_SOURCE_TO_TRACKA: dict[int, int | None] = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: None,  # Excluded under UD04 (CLS0012 Root resorption, N=5 in train, 0 in val/test/ext)
    12: 11,
    13: 12,
}

# Track D (DS0004 Do 2024 Hanoi): XML object names ("3"/"4"/"5" or "PAI 3"/"PAI 4"/"PAI 5") -> TrackD index
DS0004_NAME_TO_TRACKD: dict[str, int] = {
    "3": 0,
    "4": 1,
    "5": 2,
    "PAI 3": 0,
    "PAI 4": 1,
    "PAI 5": 2,
}

# Track E (DS0005 AU-OPG): CSV class names -> TrackE index
DS0005_NAME_TO_TRACKE: dict[str, int] = {
    "Filled": 0,
    "Crowned": 1,
    "Retained Root": 2,
    "Cavitated": 3,
    "Implant": 4,
    "Impacted": 5,
}

# Track F (DS0006 MD-OPG): LabelMe JSON labels -> TrackF index (None = auxiliary ROI)
DS0006_LABEL_TO_TRACKF: dict[str, int | None] = {
    "p": 0,
    "o": 1,
    "z": None,  # CLS0036 Smile Zone ROI rectangle (excluded from object detection classes)
}


def compute_class_map_sha256(classes_csv_path: Path) -> str:
    """Return the normalized SHA-256 hex digest of 04_Annotations/classes.csv."""
    raw = classes_csv_path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def remap_ds0001_class(source_class_id: int) -> int | None:
    """Map DS0001 UMFIH source class ID (0..13) to TrackA index (0..12) or None if excluded."""
    if source_class_id not in DS0001_SOURCE_TO_TRACKA:
        raise ValueError(f"Unknown DS0001 source class ID: {source_class_id}")
    return DS0001_SOURCE_TO_TRACKA[source_class_id]


def is_degenerate_box(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    min_side_px: float = 1e-3,
    min_area_px: float = 1.0,
) -> bool:
    """Return True if a pixel-space box has non-finite coordinates, non-positive span, or tiny area."""
    if not all(math.isfinite(v) for v in (xmin, ymin, xmax, ymax)):
        return True
    w = xmax - xmin
    h = ymax - ymin
    if w <= min_side_px or h <= min_side_px:
        return True
    return (w * h) <= min_area_px


def clip_xyxy(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    img_w: int | float,
    img_h: int | float,
) -> tuple[float, float, float, float]:
    """Clip pixel-space [xmin, ymin, xmax, ymax] to [0, img_w] x [0, img_h]."""
    if img_w <= 0 or img_h <= 0:
        raise ValueError(f"Invalid image dimensions: {img_w}x{img_h}")
    x0 = min(max(float(xmin), 0.0), float(img_w))
    y0 = min(max(float(ymin), 0.0), float(img_h))
    x1 = min(max(float(xmax), 0.0), float(img_w))
    y1 = min(max(float(ymax), 0.0), float(img_h))
    return x0, y0, x1, y1


def xyxy_to_yolo_norm(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    img_w: int | float,
    img_h: int | float,
    clip: bool = True,
) -> tuple[float, float, float, float]:
    """Convert pixel-space [xmin, ymin, xmax, ymax] to normalized YOLO (xc, yc, w, h) in [0, 1]."""
    if clip:
        xmin, ymin, xmax, ymax = clip_xyxy(xmin, ymin, xmax, ymax, img_w, img_h)
    w = xmax - xmin
    h = ymax - ymin
    if w <= 0 or h <= 0:
        raise ValueError(f"Non-positive box dimensions after clipping: ({xmin}, {ymin}, {xmax}, {ymax})")
    xc = (xmin + xmax) / (2.0 * float(img_w))
    yc = (ymin + ymax) / (2.0 * float(img_h))
    wn = w / float(img_w)
    hn = h / float(img_h)
    return xc, yc, wn, hn


def yolo_norm_to_xyxy(
    xc: float,
    yc: float,
    w: float,
    h: float,
    img_w: int | float,
    img_h: int | float,
) -> tuple[float, float, float, float]:
    """Convert normalized YOLO (xc, yc, w, h) to pixel-space [xmin, ymin, xmax, ymax]."""
    if img_w <= 0 or img_h <= 0:
        raise ValueError(f"Invalid image dimensions: {img_w}x{img_h}")
    half_w = 0.5 * w * float(img_w)
    half_h = 0.5 * h * float(img_h)
    cx = xc * float(img_w)
    cy = yc * float(img_h)
    return cx - half_w, cy - half_h, cx + half_w, cy + half_h


def coco_xywh_to_xyxy(x: float, y: float, w: float, h: float) -> tuple[float, float, float, float]:
    """Convert COCO top-left [x, y, width, height] to pixel-space [xmin, ymin, xmax, ymax]."""
    return float(x), float(y), float(x) + float(w), float(y) + float(h)


def obb_to_aabb_xyxy(
    x: float,
    y: float,
    w: float,
    h: float,
    rotation_deg: float,
    img_w: int | float,
    img_h: int | float,
    *,
    coords_are_percent: bool = True,
    pivot: str = "top_left",
    clip: bool = True,
) -> tuple[float, float, float, float]:
    """Convert AU-OPG (DS0005) rotated box to tight enclosing pixel-space AABB [xmin, ymin, xmax, ymax].

    In AU-OPG Label Studio CSVs (verified in STEP-013 `inspect_quality_step013.py`), `x, y, width, height`
    are percentages (0..100) of `image_width` and `image_height`, and `rotation` rotates the rectangle
    clockwise around its top-left corner `(px, py)` in image pixel space (`pivot="top_left"`).
    """
    iw = float(img_w)
    ih = float(img_h)
    if coords_are_percent:
        px = float(x) / 100.0 * iw
        py = float(y) / 100.0 * ih
        pw = float(w) / 100.0 * iw
        ph = float(h) / 100.0 * ih
    else:
        px, py, pw, ph = float(x), float(y), float(w), float(h)

    rad = math.radians(float(rotation_deg))
    cos_r = math.cos(rad)
    sin_r = math.sin(rad)

    if pivot == "top_left":
        corners = [(0.0, 0.0), (pw, 0.0), (pw, ph), (0.0, ph)]
        rxs = [px + dx * cos_r - dy * sin_r for dx, dy in corners]
        rys = [py + dx * sin_r + dy * cos_r for dx, dy in corners]
        xmin, xmax = min(rxs), max(rxs)
        ymin, ymax = min(rys), max(rys)
    elif pivot == "center":
        cx = px + 0.5 * pw
        cy = py + 0.5 * ph
        aabb_w = pw * abs(cos_r) + ph * abs(sin_r)
        aabb_h = pw * abs(sin_r) + ph * abs(cos_r)
        xmin, xmax = cx - 0.5 * aabb_w, cx + 0.5 * aabb_w
        ymin, ymax = cy - 0.5 * aabb_h, cy + 0.5 * aabb_h
    else:
        raise ValueError(f"Unsupported OBB pivot mode: {pivot!r}")

    if clip:
        xmin, ymin, xmax, ymax = clip_xyxy(xmin, ymin, xmax, ymax, iw, ih)
    return xmin, ymin, xmax, ymax


def polygon_to_aabb_xyxy(
    points: Sequence[Sequence[float]],
    img_w: int | float | None = None,
    img_h: int | float | None = None,
) -> tuple[float, float, float, float]:
    """Convert LabelMe polygon vertices [[x1, y1], ...] (DS0006 MD-OPG) to tight enclosing AABB."""
    if not points:
        raise ValueError("Polygon points cannot be empty")
    xs = [float(pt[0]) for pt in points]
    ys = [float(pt[1]) for pt in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    if img_w is not None and img_h is not None:
        xmin, ymin, xmax, ymax = clip_xyxy(xmin, ymin, xmax, ymax, img_w, img_h)
    return xmin, ymin, xmax, ymax


def format_yolo_line(class_id: int, xc: float, yc: float, w: float, h: float, precision: int = 6) -> str:
    """Format a single canonical YOLO export line with fixed decimal precision."""
    if class_id < 0:
        raise ValueError(f"class_id must be non-negative, got {class_id}")
    for name, val in (("xc", xc), ("yc", yc), ("w", w), ("h", h)):
        if not math.isfinite(val) or val < -1e-6 or val > 1.0 + 1e-6:
            raise ValueError(f"Normalized coordinate {name}={val} out of bounds [0, 1]")
    xc_c = min(max(xc, 0.0), 1.0)
    yc_c = min(max(yc, 0.0), 1.0)
    w_c = min(max(w, 0.0), 1.0)
    h_c = min(max(h, 0.0), 1.0)
    if w_c <= 0.0 or h_c <= 0.0:
        raise ValueError(f"Normalized width/height must be positive: w={w_c}, h={h_c}")
    fmt = f"{{:.{precision}f}}"
    return f"{class_id} {fmt.format(xc_c)} {fmt.format(yc_c)} {fmt.format(w_c)} {fmt.format(h_c)}"


def parse_yolo_line(line: str) -> tuple[int, float, float, float, float]:
    """Parse and validate a single YOLO annotation line."""
    parts = line.strip().split()
    if len(parts) != 5:
        raise ValueError(f"Expected 5 tokens in YOLO line, got {len(parts)}: {line!r}")
    class_id = int(parts[0])
    xc, yc, w, h = (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
    if class_id < 0:
        raise ValueError(f"Negative class_id: {class_id}")
    if not all(math.isfinite(v) for v in (xc, yc, w, h)):
        raise ValueError(f"Non-finite coordinates in line: {line!r}")
    if w <= 0.0 or h <= 0.0:
        raise ValueError(f"Non-positive width/height in line: {line!r}")
    if any(v < -1e-5 or v > 1.0 + 1e-5 for v in (xc, yc, w, h)):
        raise ValueError(f"Out-of-bounds normalized coordinates in line: {line!r}")
    return class_id, xc, yc, w, h


def verify_yolo_round_trip(
    class_id: int,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    img_w: int,
    img_h: int,
    precision: int = 6,
) -> float:
    """Run pixel -> YOLO string -> pixel round trip and return max absolute pixel error."""
    xc, yc, wn, hn = xyxy_to_yolo_norm(xmin, ymin, xmax, ymax, img_w, img_h, clip=True)
    line = format_yolo_line(class_id, xc, yc, wn, hn, precision=precision)
    cid2, xc2, yc2, wn2, hn2 = parse_yolo_line(line)
    if cid2 != class_id:
        raise ValueError(f"Class ID mismatch in round trip: {cid2} != {class_id}")
    rx0, ry0, rx1, ry1 = yolo_norm_to_xyxy(xc2, yc2, wn2, hn2, img_w, img_h)
    cx0, cy0, cx1, cy1 = clip_xyxy(xmin, ymin, xmax, ymax, img_w, img_h)
    return max(abs(rx0 - cx0), abs(ry0 - cy0), abs(rx1 - cx1), abs(ry1 - cy1))


def box_iou_xyxy(
    box_a: Sequence[float],
    box_b: Sequence[float],
) -> float:
    """Compute exact 2D Intersection-over-Union (IoU) for two [xmin, ymin, xmax, ymax] boxes."""
    ax0, ay0, ax1, ay1 = float(box_a[0]), float(box_a[1]), float(box_a[2]), float(box_a[3])
    bx0, by0, bx1, by1 = float(box_b[0]), float(box_b[1]), float(box_b[2]), float(box_b[3])
    ix0 = max(ax0, bx0)
    iy0 = max(ay0, by0)
    ix1 = min(ax1, bx1)
    iy1 = min(ay1, by1)
    iw = max(0.0, ix1 - ix0)
    ih = max(0.0, iy1 - iy0)
    inter = iw * ih
    if inter <= 0.0:
        return 0.0
    area_a = max(0.0, ax1 - ax0) * max(0.0, ay1 - ay0)
    area_b = max(0.0, bx1 - bx0) * max(0.0, by1 - by0)
    union = area_a + area_b - inter
    return inter / union if union > 0.0 else 0.0


def match_boxes_greedy(
    boxes_a: Iterable[tuple[int, Sequence[float]]],
    boxes_b: Iterable[tuple[int, Sequence[float]]],
    iou_threshold: float = 0.50,
    class_aware: bool = True,
) -> dict[str, float | int]:
    """One-to-one greedy IoU matching for annotation QA pilot/batch agreement (OS §6.3)."""
    list_a = list(boxes_a)
    list_b = list(boxes_b)
    candidates: list[tuple[float, int, int]] = []
    for i, (ca, ba) in enumerate(list_a):
        for j, (cb, bb) in enumerate(list_b):
            if class_aware and ca != cb:
                continue
            iou = box_iou_xyxy(ba, bb)
            if iou >= iou_threshold:
                candidates.append((iou, i, j))
    candidates.sort(key=lambda item: item[0], reverse=True)
    used_a: set[int] = set()
    used_b: set[int] = set()
    matched_ious: list[float] = []
    class_matches = 0
    for iou, i, j in candidates:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        matched_ious.append(iou)
        if list_a[i][0] == list_b[j][0]:
            class_matches += 1
    n_matched = len(matched_ious)
    n_a = len(list_a)
    n_b = len(list_b)
    denom = n_a + n_b
    f1_agreement = (2.0 * n_matched / denom) if denom > 0 else 1.0
    mean_iou = (sum(matched_ious) / n_matched) if n_matched > 0 else 0.0
    return {
        "count_a": n_a,
        "count_b": n_b,
        "matched": n_matched,
        "unmatched_a": n_a - n_matched,
        "unmatched_b": n_b - n_matched,
        "class_matches": class_matches,
        "f1_agreement": f1_agreement,
        "mean_iou": mean_iou,
    }
