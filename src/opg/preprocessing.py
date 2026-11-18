"""Coordinate-preserving OPG preprocessing transforms, geometry contracts, and leakage guards (STEP-019)."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np
import yaml

from opg.annotation_schema import clip_xyxy, format_yolo_line, xyxy_to_yolo_norm, yolo_norm_to_xyxy


@dataclass(frozen=True)
class TransformLedger:
    """Invertible affine coordinate mapping from source raw pixels (W_src, H_src) to prepared pixels (W_out, H_out).

    Forward mapping for any pixel (x, y) in source raw image:
        x_cropped = x - crop_x0
        y_cropped = y - crop_y0
        x_out = x_cropped * scale_x + pad_left
        y_out = y_cropped * scale_y + pad_top

    Inverse mapping for any pixel (x_out, y_out) in prepared image:
        x = (x_out - pad_left) / scale_x + crop_x0
        y = (y_out - pad_top) / scale_y + crop_y0
    """

    src_width: int
    src_height: int
    crop_x0: int
    crop_y0: int
    crop_width: int
    crop_height: int
    out_width: int
    out_height: int
    scale_x: float
    scale_y: float
    pad_left: int
    pad_top: int
    pad_right: int
    pad_bottom: int
    pad_value: int = 114


REQUIRED_PP_CONFIG_KEYS = (
    "preprocessing_id",
    "version",
    "purpose",
    "target_size",
    "preserve_aspect_ratio",
    "pad_value",
    "channel_policy",
    "strip_exif_xmp",
    "contrast_enhancement",
    "border_autocrop",
    "privacy_corner_mask",
    "normalization",
    "fit_on_partition",
    "training_augmentation",
)


def compute_config_sha256(config_path: Path) -> str:
    """Return normalized SHA-256 hex digest of a preprocessing YAML config file."""
    raw = config_path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def validate_pp_config(config: dict[str, Any]) -> None:
    """Validate a preprocessing config dict; raise ValueError on missing, null, or invalid settings."""
    for key in REQUIRED_PP_CONFIG_KEYS:
        if key not in config or config[key] is None:
            raise ValueError(f"Unresolved or missing required preprocessing config field: {key!r}")

    target_size = config["target_size"]
    if (
        not isinstance(target_size, (list, tuple))
        or len(target_size) != 2
        or any(v is None or not isinstance(v, int) or v <= 0 for v in target_size)
    ):
        raise ValueError(f"Invalid target_size (must be [width, height] positive ints): {target_size!r}")

    ce = config["contrast_enhancement"]
    if not isinstance(ce, dict) or "method" not in ce or ce["method"] is None:
        raise ValueError("contrast_enhancement.method must be explicitly resolved ('none' or 'clahe')")
    if ce["method"] == "clahe":
        clip_lim = ce.get("clip_limit")
        grid = ce.get("tile_grid_size")
        if clip_lim is None or float(clip_lim) <= 0:
            raise ValueError(f"CLAHE clip_limit must be positive, got {clip_lim!r}")
        if not isinstance(grid, (list, tuple)) or len(grid) != 2 or any(int(g) <= 0 for g in grid):
            raise ValueError(f"CLAHE tile_grid_size must be [gx, gy] positive ints, got {grid!r}")
    elif ce["method"] != "none":
        raise ValueError(f"Unsupported contrast_enhancement.method: {ce['method']!r}")

    fit_part = config["fit_on_partition"]
    if fit_part not in ("none", "train_only"):
        raise ValueError(
            f"Invalid fit_on_partition={fit_part!r}; must be 'none' or 'train_only' (never val/test!)"
        )

    aug = config["training_augmentation"]
    if not isinstance(aug, dict) or aug.get("apply_to_val_or_test") is not False:
        raise ValueError("training_augmentation.apply_to_val_or_test MUST be explicitly False")
    if aug.get("horizontal_flip_allowed_when_laterality_matters", False) is not False:
        raise ValueError("Horizontal flip must remain disabled when left/right quadrant laterality is preserved")


def standardize_channels_rgb(image: np.ndarray) -> np.ndarray:
    """Convert grayscale (H,W), 2-channel, RGB (H,W,3), or RGBA (H,W,4) uint8 array to 3-channel RGB."""
    if image.ndim == 2:
        return np.stack([image, image, image], axis=-1)
    if image.ndim == 3:
        c = image.shape[2]
        if c == 1:
            return np.repeat(image, 3, axis=2)
        if c == 3:
            return image.copy()
        if c == 4:
            # Drop alpha channel deterministically (e.g., DS0001 v60.png RGBA and DS0005 17 RGBA files)
            return image[:, :, :3].copy()
    raise ValueError(f"Unsupported image shape for RGB standardization: {image.shape}")


def apply_clahe_rgb(
    image_rgb: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Apply deterministic CLAHE on luminance/grayscale intensity and return 3-channel uint8 RGB."""
    if clip_limit <= 0:
        raise ValueError(f"clip_limit must be > 0, got {clip_limit}")
    gx, gy = int(tile_grid_size[0]), int(tile_grid_size[1])
    if gx <= 0 or gy <= 0:
        raise ValueError(f"tile_grid_size must be positive, got {tile_grid_size}")

    rgb = standardize_channels_rgb(image_rgb)
    # If all 3 channels are identical grayscale (standard OPG), apply directly to channel 0
    if np.array_equal(rgb[:, :, 0], rgb[:, :, 1]) and np.array_equal(rgb[:, :, 0], rgb[:, :, 2]):
        clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(gx, gy))
        ch = clahe.apply(rgb[:, :, 0])
        return np.stack([ch, ch, ch], axis=-1)

    # Otherwise apply CLAHE to the L channel in LAB color space
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(gx, gy))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def mask_corner_logo_safe(
    image_rgb: np.ndarray,
    boxes_xyxy: Sequence[Sequence[float]],
    corner: str = "bottom_right",
    max_width_frac: float = 0.14,
    max_height_frac: float = 0.10,
) -> tuple[np.ndarray, bool]:
    """Mask corner clinic stamp (e.g., DS0003 'PRESCRIPTION POINT') ONLY if disjoint from all target boxes.

    Never alters or masks any pixel inside a ground-truth bounding box.
    """
    out = standardize_channels_rgb(image_rgb)
    h, w = out.shape[:2]
    mw = int(round(w * max_width_frac))
    mh = int(round(h * max_height_frac))
    if corner == "bottom_right":
        mx0, my0, mx1, my1 = w - mw, h - mh, w, h
    elif corner == "bottom_left":
        mx0, my0, mx1, my1 = 0, h - mh, mw, h
    else:
        raise ValueError(f"Unsupported corner: {corner}")

    # Check if the candidate corner rectangle overlaps any ground-truth box
    for b in boxes_xyxy:
        bx0, by0, bx1, by1 = float(b[0]), float(b[1]), float(b[2]), float(b[3])
        if max(mx0, bx0) < min(mx1, bx1) and max(my0, by0) < min(my1, by1):
            return out, False

    out[my0:my1, mx0:mx1] = 0
    return out, True


def autocrop_black_border_with_boxes(
    image_rgb: np.ndarray,
    boxes_xyxy: Sequence[Sequence[float]],
    black_threshold: int = 8,
    margin_px: int = 8,
) -> tuple[np.ndarray, list[tuple[float, float, float, float]], tuple[int, int, int, int]]:
    """Deterministically crop outer solid-black framing (e.g., DS0006 66% letterbox) while preserving all boxes.

    The crop window is expanded to the union of the non-black pixel bounding box AND all ground-truth boxes
    plus `margin_px`, guaranteeing that ZERO target boxes are ever clipped or dropped.
    """
    rgb = standardize_channels_rgb(image_rgb)
    h, w = rgb.shape[:2]
    gray = np.max(rgb, axis=2)
    ys, xs = np.where(gray > black_threshold)
    if len(xs) == 0 or len(ys) == 0:
        x0, y0, x1, y1 = 0, 0, w, h
    else:
        x0 = max(0, int(xs.min()) - margin_px)
        y0 = max(0, int(ys.min()) - margin_px)
        x1 = min(w, int(xs.max()) + 1 + margin_px)
        y1 = min(h, int(ys.max()) + 1 + margin_px)

    # Guarantee zero box clipping by expanding crop bounds to enclose every ground-truth box
    for b in boxes_xyxy:
        bx0, by0, bx1, by1 = float(b[0]), float(b[1]), float(b[2]), float(b[3])
        x0 = min(x0, max(0, int(math.floor(bx0)) - margin_px))
        y0 = min(y0, max(0, int(math.floor(by0)) - margin_px))
        x1 = max(x1, min(w, int(math.ceil(bx1)) + margin_px))
        y1 = max(y1, min(h, int(math.ceil(by1)) + margin_px))

    cropped = rgb[y0:y1, x0:x1].copy()
    shifted_boxes: list[tuple[float, float, float, float]] = []
    for b in boxes_xyxy:
        sx0 = float(b[0]) - float(x0)
        sy0 = float(b[1]) - float(y0)
        sx1 = float(b[2]) - float(x0)
        sy1 = float(b[3]) - float(y0)
        shifted_boxes.append((sx0, sy0, sx1, sy1))

    return cropped, shifted_boxes, (x0, y0, x1 - x0, y1 - y0)


def forward_transform_box(
    box_xyxy: Sequence[float],
    ledger: TransformLedger,
) -> tuple[float, float, float, float]:
    """Map source raw pixel box [xmin, ymin, xmax, ymax] into prepared output image coordinates."""
    x0, y0, x1, y1 = float(box_xyxy[0]), float(box_xyxy[1]), float(box_xyxy[2]), float(box_xyxy[3])
    ox0 = (x0 - ledger.crop_x0) * ledger.scale_x + ledger.pad_left
    oy0 = (y0 - ledger.crop_y0) * ledger.scale_y + ledger.pad_top
    ox1 = (x1 - ledger.crop_x0) * ledger.scale_x + ledger.pad_left
    oy1 = (y1 - ledger.crop_y0) * ledger.scale_y + ledger.pad_top
    return clip_xyxy(ox0, oy0, ox1, oy1, ledger.out_width, ledger.out_height)


def inverse_transform_box(
    out_box_xyxy: Sequence[float],
    ledger: TransformLedger,
) -> tuple[float, float, float, float]:
    """Map prepared/predicted pixel box [xmin, ymin, xmax, ymax] back to original raw image coordinates."""
    ox0, oy0, ox1, oy1 = (
        float(out_box_xyxy[0]),
        float(out_box_xyxy[1]),
        float(out_box_xyxy[2]),
        float(out_box_xyxy[3]),
    )
    x0 = (ox0 - ledger.pad_left) / ledger.scale_x + ledger.crop_x0
    y0 = (oy0 - ledger.pad_top) / ledger.scale_y + ledger.crop_y0
    x1 = (ox1 - ledger.pad_left) / ledger.scale_x + ledger.crop_x0
    y1 = (oy1 - ledger.pad_top) / ledger.scale_y + ledger.crop_y0
    return clip_xyxy(x0, y0, x1, y1, ledger.src_width, ledger.src_height)


def prepare_image_and_boxes(
    image: np.ndarray,
    boxes_with_classes: Sequence[tuple[int, float, float, float, float]],
    target_size: tuple[int, int] = (640, 640),
    *,
    preserve_aspect_ratio: bool = True,
    pad_value: int = 114,
    autocrop_black_border: bool = False,
    clahe_params: tuple[float, tuple[int, int]] | None = None,
) -> tuple[np.ndarray, list[tuple[int, float, float, float, float]], list[str], TransformLedger]:
    """Apply deterministic coordinate-preserving preparation and return (out_img, out_boxes_xyxy, yolo_lines, ledger).

    Raises ValueError if any input box is silently dropped or becomes degenerate.
    """
    rgb = standardize_channels_rgb(image)
    src_h, src_w = rgb.shape[:2]
    raw_xyxy = [(b[1], b[2], b[3], b[4]) for b in boxes_with_classes]

    if autocrop_black_border:
        work_img, _, (cx0, cy0, cw, ch) = autocrop_black_border_with_boxes(rgb, raw_xyxy)
    else:
        work_img = rgb
        cx0, cy0, cw, ch = 0, 0, src_w, src_h

    if clahe_params is not None:
        clip_lim, grid = clahe_params
        work_img = apply_clahe_rgb(work_img, clip_limit=clip_lim, tile_grid_size=grid)

    out_w, out_h = int(target_size[0]), int(target_size[1])
    if out_w <= 0 or out_h <= 0:
        raise ValueError(f"Invalid target_size: {target_size}")

    if preserve_aspect_ratio:
        scale = min(out_w / float(cw), out_h / float(ch))
        new_w = max(1, int(round(cw * scale)))
        new_h = max(1, int(round(ch * scale)))
        scale_x = new_w / float(cw)
        scale_y = new_h / float(ch)
        pad_w = out_w - new_w
        pad_h = out_h - new_h
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top
        interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        resized = cv2.resize(work_img, (new_w, new_h), interpolation=interp)
        out_img = cv2.copyMakeBorder(
            resized,
            pad_top,
            pad_bottom,
            pad_left,
            pad_right,
            cv2.BORDER_CONSTANT,
            value=(pad_value, pad_value, pad_value),
        )
    else:
        scale_x = out_w / float(cw)
        scale_y = out_h / float(ch)
        pad_left = pad_right = pad_top = pad_bottom = 0
        interp = cv2.INTER_AREA if min(scale_x, scale_y) < 1.0 else cv2.INTER_LINEAR
        out_img = cv2.resize(work_img, (out_w, out_h), interpolation=interp)

    ledger = TransformLedger(
        src_width=src_w,
        src_height=src_h,
        crop_x0=cx0,
        crop_y0=cy0,
        crop_width=cw,
        crop_height=ch,
        out_width=out_w,
        out_height=out_h,
        scale_x=scale_x,
        scale_y=scale_y,
        pad_left=pad_left,
        pad_top=pad_top,
        pad_right=pad_right,
        pad_bottom=pad_bottom,
        pad_value=pad_value,
    )

    out_boxes: list[tuple[int, float, float, float, float]] = []
    yolo_lines: list[str] = []
    for cid, x0, y0, x1, y1 in boxes_with_classes:
        ox0, oy0, ox1, oy1 = forward_transform_box((x0, y0, x1, y1), ledger)
        if (ox1 - ox0) <= 1e-3 or (oy1 - oy0) <= 1e-3:
            raise ValueError(f"Transform collapsed target box to zero area: {(x0, y0, x1, y1)} -> {(ox0, oy0, ox1, oy1)}")
        xc, yc, wn, hn = xyxy_to_yolo_norm(ox0, oy0, ox1, oy1, out_w, out_h, clip=False)
        line = format_yolo_line(cid, xc, yc, wn, hn, precision=6)
        out_boxes.append((cid, ox0, oy0, ox1, oy1))
        yolo_lines.append(line)

    if len(out_boxes) != len(boxes_with_classes):
        raise RuntimeError("Silent drop of target boxes is prohibited (STEP-019 checklist)")

    return out_img, out_boxes, yolo_lines, ledger


def fit_training_statistics(
    train_images_rgb: Sequence[np.ndarray],
    *,
    g07_split_passed: bool,
    partition_names: Sequence[str],
) -> dict[str, float]:
    """Compute intensity mean/std strictly on training images AFTER G07 split approval.

    Raises RuntimeError if G07 is not passed or if any non-training image is included.
    """
    if not g07_split_passed:
        raise RuntimeError(
            "BLOCKED (STEP-019 / OS §4.3): Split-dependent statistics cannot be fitted before STEP-020 / G07 PASS."
        )
    if not train_images_rgb or len(train_images_rgb) != len(partition_names):
        raise ValueError("train_images_rgb and partition_names must be non-empty and equal length")
    if any(p.strip().lower() != "train" for p in partition_names):
        raise RuntimeError("LEAKAGE VIOLATION: fit_training_statistics received non-train partition data!")

    means = [float(np.mean(img) / 255.0) for img in train_images_rgb]
    stds = [float(np.std(img) / 255.0) for img in train_images_rgb]
    return {
        "train_image_count": float(len(train_images_rgb)),
        "mean_intensity_0_1": round(float(np.mean(means)), 6),
        "std_intensity_0_1": round(float(np.mean(stds)), 6),
    }


def load_and_validate_pp_yaml(path: Path) -> dict[str, Any]:
    """Load a preprocessing YAML file and validate all required fields."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    validate_pp_config(data)
    return data
