"""Unit and round-trip tests for STEP-015 annotation schema and conversion contract (G05)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import (  # noqa: E402
    box_iou_xyxy,
    coco_xywh_to_xyxy,
    compute_class_map_sha256,
    format_yolo_line,
    is_degenerate_box,
    match_boxes_greedy,
    obb_to_aabb_xyxy,
    parse_yolo_line,
    polygon_to_aabb_xyxy,
    remap_ds0001_class,
    verify_yolo_round_trip,
)


def test_class_map_sha256_and_ds0001_remap() -> None:
    root = Path(__file__).resolve().parents[1]
    classes_csv = root / "04_Annotations" / "classes.csv"
    digest = compute_class_map_sha256(classes_csv)
    assert len(digest) == 64
    # DS0001 class 11 (Root resorption, N=5) excluded -> None; 12->11, 13->12
    assert remap_ds0001_class(0) == 0
    assert remap_ds0001_class(10) == 10
    assert remap_ds0001_class(11) is None
    assert remap_ds0001_class(12) == 11
    assert remap_ds0001_class(13) == 12
    with pytest.raises(ValueError):
        remap_ds0001_class(14)


def test_coordinate_conversions_and_round_trip() -> None:
    # 1. Standard pixel -> YOLO -> pixel round trip on OPG resolution (2652 x 1536)
    max_err = verify_yolo_round_trip(4, 512.0, 340.0, 648.0, 488.0, 2652, 1536, precision=6)
    assert max_err < 0.01

    # 2. COCO [x, y, w, h] -> xyxy -> YOLO round trip (DS0002 DENTEX)
    x0, y0, x1, y1 = coco_xywh_to_xyxy(420.0, 610.0, 180.0, 290.0)
    assert (x0, y0, x1, y1) == (420.0, 610.0, 600.0, 900.0)
    assert verify_yolo_round_trip(1, x0, y0, x1, y1, 2872, 1316) < 0.01

    # 3. Rotated OBB -> AABB (DS0005 AU-OPG Label Studio percent top-left pivot & pixel center pivot)
    ox0, oy0, ox1, oy1 = obb_to_aabb_xyxy(
        10.0, 20.0, 5.0, 10.0, 0.0, 2000, 1000, coords_are_percent=True, pivot="top_left"
    )
    assert pytest.approx((ox0, oy0, ox1, oy1), abs=1e-6) == (200.0, 200.0, 300.0, 300.0)
    rx0, ry0, rx1, ry1 = obb_to_aabb_xyxy(
        100.0, 200.0, 80.0, 160.0, 90.0, 3292, 1500, coords_are_percent=False, pivot="center"
    )
    assert pytest.approx((rx0, ry0, rx1, ry1), abs=1e-5) == (60.0, 240.0, 220.0, 320.0)

    # 4. LabelMe Polygon -> AABB (DS0006 MD-OPG)
    pts = [[720.5, 640.0], [745.2, 638.5], [748.0, 672.0], [718.0, 670.0]]
    px0, py0, px1, py1 = polygon_to_aabb_xyxy(pts, 1920, 1535)
    assert (px0, py0, px1, py1) == (718.0, 638.5, 748.0, 672.0)
    assert verify_yolo_round_trip(0, px0, py0, px1, py1, 1920, 1535) < 0.01


def test_degenerate_and_invalid_yolo_lines() -> None:
    assert is_degenerate_box(10.0, 20.0, 10.0, 50.0) is True
    assert is_degenerate_box(10.0, 20.0, 40.0, 50.0) is False
    line = format_yolo_line(2, 0.5, 0.5, 0.1, 0.2)
    assert parse_yolo_line(line) == (2, 0.5, 0.5, 0.1, 0.2)
    with pytest.raises(ValueError):
        format_yolo_line(0, 0.5, 0.5, 0.0, 0.2)
    with pytest.raises(ValueError):
        parse_yolo_line("0 0.5 0.5 -0.1 0.2")


def test_greedy_qa_matching() -> None:
    boxes_a = [(0, [100.0, 100.0, 200.0, 200.0]), (1, [300.0, 300.0, 400.0, 400.0])]
    boxes_b = [(0, [105.0, 100.0, 205.0, 200.0]), (2, [300.0, 300.0, 400.0, 400.0])]
    assert box_iou_xyxy([100, 100, 200, 200], [100, 100, 200, 200]) == 1.0
    res_aware = match_boxes_greedy(boxes_a, boxes_b, iou_threshold=0.50, class_aware=True)
    assert res_aware["matched"] == 1
    assert res_aware["unmatched_a"] == 1
    assert res_aware["unmatched_b"] == 1
    assert res_aware["mean_iou"] > 0.80
