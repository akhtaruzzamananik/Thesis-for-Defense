"""Smoke checks for the minimal STEP-002 data-tool runtime.

Uses synthetic in-memory/temporary fixtures only (no medical or patient data).
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import numpy as np
import yaml
from PIL import Image


def test_synthetic_image_roundtrip_and_hash(tmp_path: Path) -> None:
    arr = np.zeros((64, 128), dtype=np.uint8)
    arr[16:48, 32:96] = 200
    img_path = tmp_path / "synthetic_opg.png"
    Image.fromarray(arr, mode="L").save(img_path)

    with Image.open(img_path) as loaded:
        assert loaded.size == (128, 64)
        assert loaded.mode == "L"
        loaded_arr = np.asarray(loaded)
        assert loaded_arr.shape == (64, 128)
        assert int(loaded_arr[24, 64]) == 200

    digest = hashlib.sha256(img_path.read_bytes()).hexdigest()
    assert len(digest) == 64


def test_coordinate_resize_roundtrip() -> None:
    orig_w, orig_h = 200, 100
    new_w, new_h = 100, 50
    box_orig = (20.0, 10.0, 80.0, 60.0)  # x1, y1, x2, y2

    sx, sy = new_w / orig_w, new_h / orig_h
    box_scaled = (box_orig[0] * sx, box_orig[1] * sy, box_orig[2] * sx, box_orig[3] * sy)
    box_back = (box_scaled[0] / sx, box_scaled[1] / sy, box_scaled[2] / sx, box_scaled[3] / sy)

    assert np.allclose(box_orig, box_back, atol=1e-6)


def test_yaml_and_decisions_csv_readable() -> None:
    cfg = yaml.safe_load("ap_iou: 0.50\nsplit: [0.70, 0.15, 0.15]\n")
    assert cfg["ap_iou"] == 0.50

    decisions_path = Path(__file__).resolve().parents[1] / "01_Project_Management" / "decisions.csv"
    with decisions_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 24
    assert rows[0]["DecisionID"] == "DEC0001"
