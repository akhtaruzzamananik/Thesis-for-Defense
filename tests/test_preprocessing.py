"""Unit tests for STEP-019 preprocessing transforms, geometry round-trips, and G07 leakage guards."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import parse_yolo_line, yolo_norm_to_xyxy  # noqa: E402
from opg.preprocessing import (  # noqa: E402
    apply_clahe_rgb,
    autocrop_black_border_with_boxes,
    fit_training_statistics,
    inverse_transform_box,
    load_and_validate_pp_yaml,
    mask_corner_logo_safe,
    prepare_image_and_boxes,
    standardize_channels_rgb,
    validate_pp_config,
)


def test_channel_standardization_and_clahe() -> None:
    gray = np.full((120, 240), 128, dtype=np.uint8)
    rgba = np.zeros((120, 240, 4), dtype=np.uint8)
    rgba[:, :, :3] = 90
    rgba[:, :, 3] = 255

    rgb1 = standardize_channels_rgb(gray)
    rgb2 = standardize_channels_rgb(rgba)
    assert rgb1.shape == (120, 240, 3)
    assert rgb2.shape == (120, 240, 3)

    # Test CLAHE with gradient
    grad = np.tile(np.linspace(10, 230, 240, dtype=np.uint8), (120, 1))
    enhanced = apply_clahe_rgb(grad, clip_limit=2.0, tile_grid_size=(8, 8))
    assert enhanced.shape == (120, 240, 3)
    assert enhanced.dtype == np.uint8


def test_letterbox_and_autocrop_geometry_round_trip() -> None:
    # Create synthetic pediatric OPG with 66% black letterbox framing (like DS0006 1920x1535)
    img = np.zeros((1535, 1920, 3), dtype=np.uint8)
    img[350:1150, 200:1720] = 140  # active radiograph arch interior
    boxes = [
        (0, 480.0, 520.0, 540.0, 590.0),
        (1, 1120.0, 610.0, 1195.0, 685.0),
    ]

    out_img, out_boxes, yolo_lines, ledger = prepare_image_and_boxes(
        img,
        boxes,
        target_size=(640, 640),
        preserve_aspect_ratio=True,
        autocrop_black_border=True,
        clahe_params=(2.0, (8, 8)),
    )
    assert out_img.shape == (640, 640, 3)
    assert len(out_boxes) == 2
    assert len(yolo_lines) == 2
    assert ledger.crop_width < 1920 and ledger.crop_height < 1535

    # Verify forward -> YOLO 6-dec string -> inverse back to original 1920x1535 pixel space!
    for (orig_cid, x0, y0, x1, y1), line in zip(boxes, yolo_lines):
        cid, xc, yc, wn, hn = parse_yolo_line(line)
        assert cid == orig_cid
        px0, py0, px1, py1 = yolo_norm_to_xyxy(xc, yc, wn, hn, 640, 640)
        rx0, ry0, rx1, ry1 = inverse_transform_box((px0, py0, px1, py1), ledger)
        max_err = max(abs(rx0 - x0), abs(ry0 - y0), abs(rx1 - x1), abs(ry1 - y1))
        assert max_err < 0.02


def test_autocrop_never_clips_edge_boxes_and_safe_corner_mask() -> None:
    img = np.zeros((600, 1200, 3), dtype=np.uint8)
    img[100:500, 100:1100] = 120
    # Put a box inside the dark margin near top-left and another in bottom-right corner
    boxes = [(0.0, 20.0, 30.0, 90.0, 95.0), (1.0, 1080.0, 550.0, 1180.0, 590.0)]
    raw_xyxy = [(b[1], b[2], b[3], b[4]) for b in boxes]

    cropped, shifted, (cx0, cy0, cw, ch) = autocrop_black_border_with_boxes(img, raw_xyxy)
    assert cx0 <= 20 and cy0 <= 20
    for sx0, sy0, sx1, sy1 in shifted:
        assert 0.0 <= sx0 < sx1 <= cw
        assert 0.0 <= sy0 < sy1 <= ch

    # Corner mask should refuse to mask bottom_right when box 2 overlaps bottom_right!
    _, masked = mask_corner_logo_safe(img, raw_xyxy, corner="bottom_right")
    assert masked is False
    # But bottom_left is disjoint from both boxes, so it masks safely
    _, masked_bl = mask_corner_logo_safe(img, raw_xyxy, corner="bottom_left")
    assert masked_bl is True


def test_leakage_and_unresolved_config_guards() -> None:
    dummy_img = np.full((64, 64, 3), 100, dtype=np.uint8)
    # 1. Must block fitting before G07 PASS
    with pytest.raises(RuntimeError, match="BLOCKED"):
        fit_training_statistics([dummy_img], g07_split_passed=False, partition_names=["train"])

    # 2. Must block fitting if val or test partition is passed
    with pytest.raises(RuntimeError, match="LEAKAGE VIOLATION"):
        fit_training_statistics([dummy_img, dummy_img], g07_split_passed=True, partition_names=["train", "val"])

    # 3. Valid train-only after G07 PASS succeeds
    stats = fit_training_statistics([dummy_img], g07_split_passed=True, partition_names=["train"])
    assert pytest.approx(stats["mean_intensity_0_1"], abs=1e-4) == 100.0 / 255.0

    # 4. Unresolved config field must fail validation
    bad_cfg = {"preprocessing_id": "PP_BAD", "target_size": None}
    with pytest.raises(ValueError, match="Unresolved or missing"):
        validate_pp_config(bad_cfg)

    # 5. Validate all committed 05_Preprocessing/configs/*.yaml files
    cfg_dir = ROOT / "05_Preprocessing" / "configs"
    if cfg_dir.is_dir():
        yaml_files = sorted(cfg_dir.glob("*.yaml"))
        assert len(yaml_files) >= 4
        for yp in yaml_files:
            loaded = load_and_validate_pp_yaml(yp)
            assert loaded["training_augmentation"]["apply_to_val_or_test"] is False
