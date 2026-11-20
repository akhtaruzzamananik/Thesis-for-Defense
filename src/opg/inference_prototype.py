"""Bounded Research Inference Prototype Engine for 2D OPG YOLO ONNX Models (STEP-037 / UD18).

This module is the single authoritative inference entry point reused by both the CLI caller
(13_Automation/run_opg_inference.py) and any future web demonstration layer (STEP-047-049).

Design invariants:
  - Reuses frozen src/opg/preprocessing.py (prepare_image_and_boxes, inverse_transform_box) verbatim.
  - Verifies SHA-256 hashes of classes.csv, PP YAML config, and exported .onnx model before inference.
  - Maps all predicted bounding boxes back to original source radiograph pixel coordinates [W, H].
  - Explicitly distinguishes status='OK', status='ZERO_DETECTIONS' (never 'no disease'), and status='ERROR'.
  - Embeds mandatory non-clinical research-only disclaimer in every response and overlay image.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import onnxruntime as ort

from opg.preprocessing import inverse_transform_box, prepare_image_and_boxes

RESEARCH_DISCLAIMER = (
    "RESEARCH PROTOTYPE ONLY — NOT A MEDICAL DEVICE AND NOT FOR CLINICAL DIAGNOSIS OR TREATMENT. "
    "Detection confidence is NOT diagnostic certainty, and zero detections DO NOT exclude dental pathology. "
    "All radiographic interpretations must be performed independently by a qualified dental clinician."
)

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

# Color-blind-friendly BGR palette for optional visual overlays
_OVERLAY_PALETTE_BGR = [
    (66, 133, 244),
    (52, 168, 83),
    (251, 188, 5),
    (234, 67, 53),
    (171, 71, 188),
    (0, 172, 193),
    (255, 112, 67),
    (124, 179, 66),
    (41, 182, 246),
    (236, 64, 122),
    (141, 110, 99),
    (120, 144, 156),
    (38, 166, 154),
]


class PrototypeError(RuntimeError):
    """Base structured error for the OPG research prototype."""

    error_code: str = "PROTOTYPE_ERROR"


class PrototypeModelMissingError(PrototypeError):
    """Raised when a requested model ID or its exported ONNX artifact is unavailable."""

    error_code = "MODEL_MISSING"


class PrototypeHashMismatchError(PrototypeError):
    """Raised when classes.csv, PP config, or ONNX weights fail frozen SHA-256 verification."""

    error_code = "HASH_MISMATCH"


class PrototypeInputError(PrototypeError):
    """Raised when an input image is missing, unsupported, corrupt, or unreadable."""

    error_code = "INVALID_INPUT"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_track_class_names(classes_csv: Path, track_id: str) -> list[str]:
    mapping: dict[int, str] = {}
    with classes_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ti = row["TrainingIndex"].strip()
            if ti.startswith(f"{track_id}:"):
                _, idx_str = ti.split(":", 1)
                mapping[int(idx_str)] = row["Name"].strip()
    if not mapping:
        raise PrototypeError(f"No classes found in {classes_csv} for track {track_id!r}")
    return [mapping[i] for i in sorted(mapping)]


@dataclass(frozen=True)
class LoadedModelMetadata:
    """Immutable provenance record for one verified frozen ONNX model."""

    model_id: str
    experiment_id: str
    checkpoint_id: str
    track_id: str
    release_id: str
    architecture: str
    imgsz: int
    preprocessing_id: str
    pp_config_path: str
    pp_config_sha256: str
    onnx_path: Path
    onnx_sha256: str
    class_map_sha256: str
    freeze_id: str
    frozen_conf_op: float
    nms_iou: float
    max_det: int
    class_names: tuple[str, ...]


class OPGPrototypeEngine:
    """Deterministic single-path 2D OPG object detection prototype backed by frozen ONNX exports."""

    def __init__(
        self,
        model_id: str = "MODEL0008",
        *,
        repo_root: Path | None = None,
        onnx_dir: Path | None = None,
        classes_csv_override: Path | None = None,
        intra_op_num_threads: int | None = None,
    ) -> None:
        self.repo_root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
        freeze_path = self.repo_root / "09_Evaluation" / "freeze_manifest.json"
        exec_path = self.repo_root / "09_Evaluation" / "step032_execution_manifest.json"
        if not freeze_path.is_file() or not exec_path.is_file():
            raise PrototypeModelMissingError("Required freeze_manifest.json or step032_execution_manifest.json missing.")

        freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
        exec_man = json.loads(exec_path.read_text(encoding="utf-8"))
        gh = freeze["governance_hashes"]

        # 1. Verify frozen classes.csv SHA-256
        classes_path = (classes_csv_override or (self.repo_root / gh["class_map_path"])).resolve()
        if not classes_path.is_file():
            raise PrototypeHashMismatchError(f"Class ontology file missing: {classes_path}")
        actual_cls_sha = _sha256_file(classes_path)
        expected_cls_sha = str(gh["class_map_sha256"])
        if actual_cls_sha != expected_cls_sha:
            raise PrototypeHashMismatchError(
                f"Class-map SHA-256 mismatch: got {actual_cls_sha}, expected {expected_cls_sha}"
            )

        # 2. Locate requested frozen model
        fm = next((m for m in freeze["frozen_models"] if m["model_id"] == model_id), None)
        if fm is None:
            raise PrototypeModelMissingError(f"Unknown model_id {model_id!r} not in FREEZE0001 manifest.")
        onnx_info = exec_man.get("onnx_exports", {}).get(model_id)
        if not onnx_info or "filename" not in onnx_info:
            raise PrototypeModelMissingError(
                f"Model {model_id!r} does not have an approved ONNX export (e.g., license-isolated or unexported)."
            )

        # 3. Verify frozen preprocessing config SHA-256
        pp_id = str(fm["preprocessing_id"])
        pp_info = gh["pp_configs"][pp_id]
        pp_path = self.repo_root / pp_info["path"]
        if not pp_path.is_file() or _sha256_file(pp_path) != pp_info["sha256"]:
            raise PrototypeHashMismatchError(f"Preprocessing config SHA-256 mismatch for {pp_id} at {pp_path}")

        # 4. Verify ONNX artifact existence & bit-for-bit SHA-256
        resolved_onnx_dir = (
            onnx_dir or (self.repo_root / "08_Checkpoints" / "artifacts" / "STEP032_outputs" / "onnx")
        ).resolve()
        onnx_path = resolved_onnx_dir / str(onnx_info["filename"])
        if not onnx_path.is_file():
            raise PrototypeModelMissingError(
                f"Exported ONNX artifact not found at {onnx_path}. Restore STEP-032 ONNX artifacts first."
            )
        actual_onnx_sha = _sha256_file(onnx_path)
        expected_onnx_sha = str(onnx_info["sha256"])
        if actual_onnx_sha != expected_onnx_sha:
            raise PrototypeHashMismatchError(
                f"ONNX weight SHA-256 mismatch for {model_id}: got {actual_onnx_sha}, expected {expected_onnx_sha}"
            )

        ev_cfg = freeze["evaluation_settings"]
        cls_names = tuple(_load_track_class_names(classes_path, str(fm["track_id"])))
        self.meta = LoadedModelMetadata(
            model_id=model_id,
            experiment_id=str(fm["experiment_id"]),
            checkpoint_id=str(fm["checkpoint_id"]),
            track_id=str(fm["track_id"]),
            release_id=str(fm["release_id"]),
            architecture=str(fm["architecture"]),
            imgsz=int(fm["imgsz"]),
            preprocessing_id=pp_id,
            pp_config_path=str(pp_info["path"]),
            pp_config_sha256=str(pp_info["sha256"]),
            onnx_path=onnx_path,
            onnx_sha256=actual_onnx_sha,
            class_map_sha256=actual_cls_sha,
            freeze_id=str(freeze["freeze_id"]),
            frozen_conf_op=float(fm["frozen_conf_op"]),
            nms_iou=float(ev_cfg["nms_iou"]),
            max_det=int(ev_cfg["max_det"]),
            class_names=cls_names,
        )

        # 5. Initialize deterministic CPU ONNXRuntime session
        logical_cpus = os.cpu_count() or 4
        threads = intra_op_num_threads or max(1, min(4, logical_cpus // 2 if logical_cpus >= 4 else logical_cpus))
        sess_opts = ort.SessionOptions()
        sess_opts.intra_op_num_threads = int(threads)
        sess_opts.inter_op_num_threads = 1
        sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        t0 = time.perf_counter()
        self.session = ort.InferenceSession(
            str(onnx_path),
            sess_options=sess_opts,
            providers=["CPUExecutionProvider"],
        )
        self.cold_load_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        self.input_name = self.session.get_inputs()[0].name
        self.runtime_label = f"onnxruntime {ort.__version__} (CPUExecutionProvider, threads={threads}, FP32)"

    def _decode_outputs(
        self,
        raw_out: np.ndarray,
        *,
        conf_threshold: float,
        ledger: Any,
    ) -> list[dict[str, Any]]:
        pred = raw_out[0].T
        cls_scores = pred[:, 4:]
        cls_ids = np.argmax(cls_scores, axis=1)
        scores = cls_scores[np.arange(pred.shape[0]), cls_ids]

        keep = scores >= conf_threshold
        if not np.any(keep):
            return []

        boxes_xywh = pred[keep, :4]
        scores_k = scores[keep]
        cls_k = cls_ids[keep]

        x0 = boxes_xywh[:, 0] - 0.5 * boxes_xywh[:, 2]
        y0 = boxes_xywh[:, 1] - 0.5 * boxes_xywh[:, 3]
        bw = boxes_xywh[:, 2]
        bh = boxes_xywh[:, 3]
        bboxes_cv = np.stack([x0, y0, bw, bh], axis=1).tolist()

        idxs = cv2.dnn.NMSBoxesBatched(
            bboxes_cv,
            scores_k.tolist(),
            cls_k.tolist(),
            float(conf_threshold),
            float(self.meta.nms_iou),
        )
        if len(idxs) == 0:
            return []
        idxs_flat = np.asarray(idxs).reshape(-1)
        order = idxs_flat[np.argsort(-scores_k[idxs_flat])][: self.meta.max_det]

        dets: list[dict[str, Any]] = []
        n_cls = len(self.meta.class_names)
        for i in order:
            cid = int(cls_k[i])
            if cid < 0 or cid >= n_cls:
                continue
            bx0 = float(x0[i])
            by0 = float(y0[i])
            bx1 = float(x0[i] + bw[i])
            by1 = float(y0[i] + bh[i])
            sx0, sy0, sx1, sy1 = inverse_transform_box((bx0, by0, bx1, by1), ledger)
            if (sx1 - sx0) <= 1e-4 or (sy1 - sy0) <= 1e-4:
                continue
            dets.append(
                {
                    "class_id": cid,
                    "class_name": self.meta.class_names[cid],
                    "confidence": round(float(scores_k[i]), 6),
                    "bbox_xyxy_px": [round(sx0, 3), round(sy0, 3), round(sx1, 3), round(sy1, 3)],
                }
            )
        return dets

    def predict_bytes(
        self,
        raw_bytes: bytes,
        *,
        source_name: str = "uploaded_image",
        conf_threshold: float | None = None,
    ) -> tuple[dict[str, Any], np.ndarray]:
        """Run deterministic end-to-end inference on raw image bytes; return (structured_payload, decoded_bgr)."""
        if not raw_bytes:
            raise PrototypeInputError("Empty image byte payload.")
        applied_conf = self.meta.frozen_conf_op if conf_threshold is None else float(conf_threshold)
        if not (0.001 <= applied_conf <= 0.999):
            raise PrototypeInputError(f"conf_threshold must be in [0.001, 0.999], got {applied_conf}")

        arr = np.frombuffer(raw_bytes, dtype=np.uint8)
        t0 = time.perf_counter()
        im_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if im_bgr is None or im_bgr.size == 0:
            raise PrototypeInputError(f"Unable to decode image bytes for {source_name!r} (corrupt or unsupported format).")
        src_h, src_w = im_bgr.shape[:2]
        if src_w < 32 or src_h < 32:
            raise PrototypeInputError(f"Image dimensions too small ({src_w}x{src_h}); minimum supported is 32x32.")

        im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
        prep_rgb, _, _, ledger = prepare_image_and_boxes(
            im_rgb,
            [],
            target_size=(self.meta.imgsz, self.meta.imgsz),
            preserve_aspect_ratio=True,
            pad_value=114,
            autocrop_black_border=False,
            clahe_params=None,
        )
        inp = np.ascontiguousarray(prep_rgb.transpose(2, 0, 1), dtype=np.float32) * (1.0 / 255.0)
        inp = inp[None, ...]
        t1 = time.perf_counter()

        raw_out = self.session.run(None, {self.input_name: inp})[0]
        t2 = time.perf_counter()

        dets = self._decode_outputs(raw_out, conf_threshold=applied_conf, ledger=ledger)
        t3 = time.perf_counter()

        status = "OK" if len(dets) > 0 else "ZERO_DETECTIONS"
        status_note = (
            f"{len(dets)} candidate radiographic box(es) detected above confidence {applied_conf:.3f}."
            if dets
            else (
                f"No candidate boxes exceeded confidence {applied_conf:.3f}. "
                "Zero detections DO NOT confirm absence of dental disease."
            )
        )
        payload: dict[str, Any] = {
            "schema_version": "1.0.0",
            "status": status,
            "status_note": status_note,
            "disclaimer": RESEARCH_DISCLAIMER,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "provenance": {
                "freeze_id": self.meta.freeze_id,
                "model_id": self.meta.model_id,
                "experiment_id": self.meta.experiment_id,
                "checkpoint_id": self.meta.checkpoint_id,
                "track_id": self.meta.track_id,
                "release_id": self.meta.release_id,
                "architecture": self.meta.architecture,
                "imgsz": self.meta.imgsz,
                "preprocessing_id": self.meta.preprocessing_id,
                "pp_config_sha256": self.meta.pp_config_sha256,
                "onnx_sha256": self.meta.onnx_sha256,
                "class_map_sha256": self.meta.class_map_sha256,
                "frozen_conf_op": self.meta.frozen_conf_op,
                "applied_conf_threshold": applied_conf,
                "using_frozen_operating_point": abs(applied_conf - self.meta.frozen_conf_op) < 1e-9,
                "nms_iou": self.meta.nms_iou,
                "agnostic_nms": False,
                "max_det": self.meta.max_det,
                "runtime": self.runtime_label,
                "cold_load_ms": self.cold_load_ms,
            },
            "image": {
                "source_name": source_name,
                "src_width": src_w,
                "src_height": src_h,
                "coordinate_space": "original_source_pixels_xyxy",
                "image_sha256": _sha256_bytes(raw_bytes),
            },
            "timing_ms": {
                "T_pre_ms": round((t1 - t0) * 1000.0, 3),
                "T_infer_ms": round((t2 - t1) * 1000.0, 3),
                "T_post_ms": round((t3 - t2) * 1000.0, 3),
                "T_e2e_ms": round((t3 - t0) * 1000.0, 3),
            },
            "detection_count": len(dets),
            "detections": dets,
        }
        return payload, im_bgr

    def predict_file(
        self,
        image_path: Path,
        *,
        conf_threshold: float | None = None,
    ) -> tuple[dict[str, Any], np.ndarray]:
        """Validate path & extension, then run predict_bytes on an image file."""
        p = Path(image_path)
        if not p.is_file():
            raise PrototypeInputError(f"Input file not found: {p}")
        if p.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise PrototypeInputError(
                f"Unsupported image extension {p.suffix!r}; allowed: {sorted(ALLOWED_IMAGE_EXTENSIONS)}"
            )
        return self.predict_bytes(p.read_bytes(), source_name=p.name, conf_threshold=conf_threshold)


def render_overlay_bgr(image_bgr: np.ndarray, payload: dict[str, Any]) -> np.ndarray:
    """Render bounding boxes, class labels, model provenance, and non-clinical banner on a copy of the source image."""
    vis = image_bgr.copy()
    h, w = vis.shape[:2]
    thickness = max(2, int(round(min(h, w) / 450.0)))
    font_scale = max(0.45, min(h, w) / 1800.0)

    for det in payload.get("detections", []):
        cid = int(det["class_id"])
        color = _OVERLAY_PALETTE_BGR[cid % len(_OVERLAY_PALETTE_BGR)]
        x0, y0, x1, y1 = [int(round(v)) for v in det["bbox_xyxy_px"]]
        cv2.rectangle(vis, (x0, y0), (x1, y1), color, thickness)
        short_lbl = str(det["class_name"]).split("_", 1)[-1]
        text = f"{short_lbl} {float(det['confidence']):.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, max(1, thickness - 1))
        ty = max(th + 6, y0 - 4)
        cv2.rectangle(vis, (x0, ty - th - 4), (min(w - 1, x0 + tw + 6), ty + 2), color, -1)
        cv2.putText(vis, text, (x0 + 3, ty - 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), max(1, thickness - 1), cv2.LINE_AA)

    # Prepend clean non-clinical research disclaimer & provenance header bar
    bar_h = max(44, int(round(h * 0.045)))
    canvas = np.zeros((h + bar_h, w, 3), dtype=np.uint8)
    canvas[:bar_h, :] = (28, 30, 36)
    canvas[bar_h:, :] = vis
    prov = payload["provenance"]
    header = (
        f"RESEARCH PROTOTYPE ONLY (NOT CLINICAL) | {prov['model_id']} ({prov['architecture']}@{prov['imgsz']}, "
        f"{prov['preprocessing_id']}, conf={prov['applied_conf_threshold']:.3f}) | "
        f"status={payload['status']} n={payload['detection_count']} T_e2e={payload['timing_ms']['T_e2e_ms']:.1f}ms"
    )
    cv2.putText(
        canvas,
        header,
        (12, int(bar_h * 0.68)),
        cv2.FONT_HERSHEY_SIMPLEX,
        max(0.45, bar_h / 72.0),
        (240, 240, 245),
        1,
        cv2.LINE_AA,
    )
    return canvas


def build_error_payload(exc: Exception, *, model_id: str, source_name: str) -> dict[str, Any]:
    """Return a uniform machine-readable error payload for failed prototype calls."""
    code = getattr(exc, "error_code", "UNEXPECTED_ERROR")
    return {
        "schema_version": "1.0.0",
        "status": "ERROR",
        "error_code": code,
        "error_message": str(exc),
        "disclaimer": RESEARCH_DISCLAIMER,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "requested_model_id": model_id,
        "source_name": source_name,
        "detection_count": 0,
        "detections": [],
    }
