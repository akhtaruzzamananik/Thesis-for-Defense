"""Thin CLI Entry Point for the Bounded 2D OPG Research Inference Prototype (STEP-037).

Example:
    python 13_Automation/run_opg_inference.py \
        --model-id MODEL0008 \
        --input "path/to/opg.jpg" \
        --out-json "output.json" \
        --out-overlay "output_overlay.jpg"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.inference_prototype import (  # noqa: E402
    OPGPrototypeEngine,
    PrototypeError,
    build_error_payload,
    render_overlay_bgr,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run bounded research 2D OPG object detection using a frozen ONNX model (STEP-037)."
    )
    parser.add_argument(
        "--model-id",
        default="MODEL0008",
        help="Frozen exported ONNX model ID (default: MODEL0008 [TrackE UAE@640]; also MODEL0005, MODEL0013, MODEL0001-0003, MODEL0010).",
    )
    parser.add_argument("--input", type=Path, required=True, help="Path to a single 2D OPG radiograph (.jpg/.png/.bmp/.tif).")
    parser.add_argument("--out-json", type=Path, default=None, help="Optional output path to save structured JSON result.")
    parser.add_argument("--out-overlay", type=Path, default=None, help="Optional output path to save annotated overlay image.")
    parser.add_argument(
        "--conf",
        type=float,
        default=None,
        help="Optional display confidence threshold override (defaults to the model's G11 frozen validation conf_op).",
    )
    parser.add_argument("--onnx-dir", type=Path, default=None, help="Optional custom directory containing exported MODEL####.onnx files.")
    args = parser.parse_args()

    try:
        engine = OPGPrototypeEngine(model_id=args.model_id, repo_root=ROOT, onnx_dir=args.onnx_dir)
        payload, im_bgr = engine.predict_file(args.input, conf_threshold=args.conf)
        if args.out_json is not None:
            args.out_json.parent.mkdir(parents=True, exist_ok=True)
            args.out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        if args.out_overlay is not None:
            args.out_overlay.parent.mkdir(parents=True, exist_ok=True)
            overlay = render_overlay_bgr(im_bgr, payload)
            cv2.imwrite(str(args.out_overlay), overlay)
        print(json.dumps(payload, indent=2))
        sys.exit(0)
    except PrototypeError as exc:
        err = build_error_payload(exc, model_id=args.model_id, source_name=args.input.name)
        if args.out_json is not None:
            args.out_json.parent.mkdir(parents=True, exist_ok=True)
            args.out_json.write_text(json.dumps(err, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(err, indent=2))
        sys.exit(2)


if __name__ == "__main__":
    main()
