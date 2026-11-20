"""Functional, Error-Contract, Hash-Guard, and PyTorch-Parity Tests for STEP-037 Research Prototype."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_schema import box_iou_xyxy  # noqa: E402
from opg.data_loader import load_locked_partition_items  # noqa: E402
from opg.inference_prototype import (  # noqa: E402
    OPGPrototypeEngine,
    PrototypeHashMismatchError,
    PrototypeInputError,
    PrototypeModelMissingError,
    render_overlay_bgr,
)

ONNX_DIR = ROOT / "08_Checkpoints" / "artifacts" / "STEP032_outputs" / "onnx"
HAS_LOCAL_ONNX = (ONNX_DIR / "MODEL0008.onnx").is_file()


def test_prototype_rejects_missing_model_and_license_isolated_model(tmp_path: Path) -> None:
    # 1. Unknown model ID
    with pytest.raises(PrototypeModelMissingError):
        OPGPrototypeEngine(model_id="MODEL9999", repo_root=ROOT)

    # 2. License-isolated DENTEX model (not exported to ONNX)
    with pytest.raises(PrototypeModelMissingError):
        OPGPrototypeEngine(model_id="MODEL0004", repo_root=ROOT)

    # 3. Valid model ID but missing ONNX file in custom dir
    with pytest.raises(PrototypeModelMissingError):
        OPGPrototypeEngine(model_id="MODEL0008", repo_root=ROOT, onnx_dir=tmp_path)


def test_prototype_rejects_class_map_hash_mismatch(tmp_path: Path) -> None:
    tampered_csv = tmp_path / "classes.csv"
    tampered_csv.write_text("ClassID,Name,TrainingIndex\nCLS0001,Fake,TrackE:0\n", encoding="utf-8")
    with pytest.raises(PrototypeHashMismatchError, match="Class-map SHA-256 mismatch"):
        OPGPrototypeEngine(model_id="MODEL0008", repo_root=ROOT, classes_csv_override=tampered_csv)


@pytest.mark.skipif(not HAS_LOCAL_ONNX, reason="Off-Git STEP-032 ONNX artifacts not present in this checkout")
def test_prototype_zero_detections_and_corrupt_inputs(tmp_path: Path) -> None:
    engine = OPGPrototypeEngine(model_id="MODEL0008", repo_root=ROOT)

    # 1. Zero-detection synthetic blank image -> MUST return ZERO_DETECTIONS (not ERROR!)
    blank = np.zeros((600, 1200, 3), dtype=np.uint8)
    ok, enc = cv2.imencode(".png", blank)
    assert ok
    payload, bgr = engine.predict_bytes(enc.tobytes(), source_name="blank_zero_det.png")
    assert payload["status"] == "ZERO_DETECTIONS"
    assert payload["detection_count"] == 0
    assert "DO NOT exclude" in payload["disclaimer"]
    assert payload["image"]["src_width"] == 1200 and payload["image"]["src_height"] == 600
    assert payload["provenance"]["using_frozen_operating_point"] is True

    # Overlay renders cleanly even for zero detections
    overlay = render_overlay_bgr(bgr, payload)
    assert overlay.shape[0] > bgr.shape[0] and overlay.shape[1] == bgr.shape[1]

    # 2. Corrupt image bytes -> PrototypeInputError
    with pytest.raises(PrototypeInputError):
        engine.predict_bytes(b"not-a-valid-image-file", source_name="corrupt.jpg")

    # 3. Unsupported extension -> PrototypeInputError
    bad_ext = tmp_path / "radiograph.txt"
    bad_ext.write_text("hello", encoding="utf-8")
    with pytest.raises(PrototypeInputError, match="Unsupported image extension"):
        engine.predict_file(bad_ext)


@pytest.mark.skipif(not HAS_LOCAL_ONNX, reason="Off-Git STEP-032 ONNX artifacts not present in this checkout")
def test_prototype_valid_opg_parity_and_cli_entry(tmp_path: Path) -> None:
    # Load 1 canonical held-out DS0005 test image & verify box bounds + PyTorch-vs-ONNX parity
    items = load_locked_partition_items(
        ROOT, dataset_id="DS0005", split_id="SPLIT0005", batch_id="ANNB0005", track_id="TrackE", partition="test"
    )
    sample = items[0]
    raw_img = ROOT / "03_Datasets" / "raw" / "DS0005" / "extracted" / sample.raw_relpath
    assert raw_img.is_file()

    out_json = tmp_path / "pred.json"
    out_ov = tmp_path / "overlay.jpg"
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "13_Automation" / "run_opg_inference.py"),
            "--model-id",
            "MODEL0008",
            "--input",
            str(raw_img),
            "--out-json",
            str(out_json),
            "--out-overlay",
            str(out_ov),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, f"CLI failed: {proc.stderr}\n{proc.stdout}"
    assert out_json.is_file() and out_ov.is_file()

    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["status"] in ("OK", "ZERO_DETECTIONS")
    assert payload["provenance"]["model_id"] == "MODEL0008"
    assert payload["image"]["src_width"] == sample.width
    assert payload["image"]["src_height"] == sample.height

    # Verify all predicted boxes lie strictly within original source image pixel dimensions
    for det in payload["detections"]:
        x0, y0, x1, y1 = det["bbox_xyxy_px"]
        assert 0.0 <= x0 < x1 <= sample.width + 1e-3
        assert 0.0 <= y0 < y1 <= sample.height + 1e-3

    # Verify parity against STEP-032 PyTorch predictions.jsonl for the exact same image
    pt_jsonl = ROOT / "08_Checkpoints" / "artifacts" / "STEP032_outputs" / "evals" / "EVAL0013" / "predictions.jsonl"
    if pt_jsonl.is_file():
        conf_op = payload["provenance"]["frozen_conf_op"]
        pt_boxes = []
        with pt_jsonl.open("r", encoding="utf-8") as pf:
            for line in pf:
                rec = json.loads(line)
                if rec["image_id"] == sample.image_id:
                    pt_boxes = [b for b in rec["boxes"] if float(b[1]) >= conf_op]
                    break
        if pt_boxes:
            ious = []
            for pb in pt_boxes:
                best = max(
                    (
                        box_iou_xyxy((pb[2], pb[3], pb[4], pb[5]), tuple(d["bbox_xyxy_px"]))
                        for d in payload["detections"]
                        if d["class_id"] == int(pb[0])
                    ),
                    default=0.0,
                )
                ious.append(best)
            assert float(np.mean(ious)) >= 0.95, f"ONNX parity IoU too low: {ious}"
