# Bounded 2D OPG Research Inference Prototype Guide (`STEP-037` / `UD18`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-037` (`S13` — Package the research inference prototype and guide) |
| Decision Record | [DEC0018.md](../01_Project_Management/decision_log/DEC0018.md) (`UD18`) |
| Single Inference Entry Point | [inference_prototype.py](../src/opg/inference_prototype.py) (`OPGPrototypeEngine`) |
| CLI Caller | [run_opg_inference.py](../13_Automation/run_opg_inference.py) |
| Automated Test Suite | [test_prototype_interface.py](../tests/test_prototype_interface.py) |
| Owner | Akhtaruzzaman Anik (`232-15-252`, Prototype Lead) |

> [!CAUTION]
> **NON-CLINICAL RESEARCH PROTOTYPE ONLY:** This software is a bounded academic research prototype for reproducible 2D OPG object-detection demonstration. It is **NOT** a medical device, has **NOT** undergone clinical regulatory clearance, and **MUST NOT** be used for diagnosis, triage, or treatment planning. Confidence scores are not diagnostic probabilities, and **`ZERO_DETECTIONS` NEVER confirms the absence of dental disease**.

---

## 1. Architecture & Single-Path Invariance (`STEP-037` / `STEP-047`)

To guarantee that demonstrations reproduce the exact evaluated models from `FREEZE0001` (`G11–G13 PASS`):

1. **Frozen Preprocessing Reuse:** `OPGPrototypeEngine` calls `src/opg/preprocessing.py` (`prepare_image_and_boxes` + `inverse_transform_box`, `sha256: 011e67c0...`) directly — zero separate demo resizing, zero undocumented contrast/CLAHE filters.
2. **Bit-for-Bit Startup Hash Gate:** Before accepting any image, `OPGPrototypeEngine` verifies the `SHA-256` digests of `04_Annotations/classes.csv`, `05_Preprocessing/configs/PP0001|PP0004*.yaml`, and the exported `MODEL####.onnx` artifact against `09_Evaluation/freeze_manifest.json` and `09_Evaluation/step032_execution_manifest.json`. Any tampering raises `PrototypeHashMismatchError`.
3. **Reusable Across CLI & Future Web Demo (`STEP-047–049`):** Any web showcase (e.g., FastAPI/web frontend in `16_Web_Demo/`) MUST import and invoke `OPGPrototypeEngine` directly rather than re-implementing YOLO preprocessing or NMS.

---

## 2. Supported Evaluated `ONNX` Models (`CPUExecutionProvider`, `FP32`, `BS=1`)

All `7` models below were exported to static `ONNX` (`opset=17`) in `STEP-032` and verified for `0.983–0.997` mean box IoU parity against PyTorch in `STEP-034`:

| `ModelID` | Track / Target Scope | Arch `@imgsz` | Frozen `conf_op` | Held-Out `test mAP@0.50` | CPU `T_e2e` (`i5-1135G7`) | License Isolation |
|---|---|---|---:|---:|---:|---|
| **`MODEL0008`** *(Default)* | `TrackE` UAE (`6` tooth-level classes: Filled, Crowned, Retained Root, Cavitated, Implant, Impacted) | `YOLO11s@640` | `0.379` | **`0.8246`** | **`201.6 ms`** (`4.96 FPS`) | `CC-BY-4.0` cohort |
| **`MODEL0005`** | `TrackA` Romania (`13` focal pathology & hardware classes) | `YOLO11s@1280` | `0.227` | **`0.4165`** *(ext `0.4338`)* | **`878.1 ms`** (`1.14 FPS`) | `CC-BY-4.0` cohort |
| **`MODEL0013`** | `TrackD` Hanoi (`3` periapical severity grades: `PAI 3/4/5`) | `YOLO11s@1280` | `0.201` | **`0.4868`** | **`847.9 ms`** (`1.18 FPS`) | `CC-BY-4.0` cohort |
| `MODEL0001` | `TrackA` `640px` baseline reference | `YOLO11s@640` | `0.238` | `0.3815` | `263.4 ms` (`3.80 FPS`) | `CC-BY-4.0` cohort |
| `MODEL0002` | `TrackA` `YOLOv8s` cross-generation reference | `YOLOv8s@640` | `0.197` | `0.3786` | `266.0 ms` (`3.76 FPS`) | `CC-BY-4.0` cohort |
| `MODEL0003` | `TrackA` `YOLO11m` scale reference | `YOLO11m@640` | `0.253` | `0.3990` | `512.4 ms` (`1.95 FPS`) | `CC-BY-4.0` cohort |
| `MODEL0010` | `TrackD` `640px` baseline reference | `YOLO11s@640` | `0.205` | `0.4419` | `181.9 ms` (`5.50 FPS`) | `CC-BY-4.0` cohort |

*(Note: `MODEL0004` `TrackB` DENTEX is strictly excluded from prototype exports to preserve `CC-BY-NC-SA-4.0` non-commercial isolation.)*

---

## 3. Usage Examples

### 3.1 Command-Line Interface (`13_Automation/run_opg_inference.py`)

```bash
# Default fast 6-class model (MODEL0008, TrackE UAE@640)
python 13_Automation/run_opg_inference.py \
    --model-id MODEL0008 \
    --input "path/to/deidentified_opg.jpg" \
    --out-json "scratch/pred_model0008.json" \
    --out-overlay "scratch/pred_model0008_overlay.jpg"

# Comprehensive 13-class high-resolution model (MODEL0005, TrackA@1280)
python 13_Automation/run_opg_inference.py \
    --model-id MODEL0005 \
    --input "path/to/deidentified_opg.jpg" \
    --out-json "scratch/pred_model0005.json" \
    --out-overlay "scratch/pred_model0005_overlay.jpg"
```

### 3.2 Python API (Used by `STEP-047` Web Showcase)

```python
from pathlib import Path
from opg.inference_prototype import OPGPrototypeEngine, render_overlay_bgr

engine = OPGPrototypeEngine(model_id="MODEL0008")
payload, bgr = engine.predict_file(Path("path/to/deidentified_opg.jpg"))
overlay_bgr = render_overlay_bgr(bgr, payload)
```

---

## 4. Structured Output & Error Contract

- **`status = "OK"`:** One or more boxes passed `applied_conf_threshold` and class-aware NMS (`nms_iou = 0.65`, `max_det = 300`). Each detection returns `class_id`, `class_name`, `confidence`, and `bbox_xyxy_px` in **authoritative original source radiograph pixels `[0..W, 0..H]`**, alongside `provenance` (all SHA-256 digests) and `timing_ms` (`T_pre_ms`, `T_infer_ms`, `T_post_ms`, `T_e2e_ms`).
- **`status = "ZERO_DETECTIONS"`:** Image decoded and processed cleanly with `0` boxes above threshold; exit code `0`. Explicitly warns that zero detections do NOT exclude pathology.
- **`status = "ERROR"`:** Structured JSON error (`error_code`: `MODEL_MISSING`, `HASH_MISMATCH`, or `INVALID_INPUT`) with non-zero CLI exit code `2`.

---

## 5. Permitted Demonstration Material & Dependencies

- **Dependencies:** `Python 3.14+`, `numpy`, `opencv-python`, `onnxruntime>=1.20` (no GPU or PyTorch required for CPU prototype execution).
- **Off-Git Artifacts Required:** Place the `STEP-032` exported `.onnx` models under `08_Checkpoints/artifacts/STEP032_outputs/onnx/` (or pass `--onnx-dir`).
- **Permitted Demo Inputs:** Strictly de-identified `CC-BY-4.0` radiographs (`DS0001`, `DS0004`, `DS0005`) retained off-Git; never upload unconsented patient radiographs with burned-in PII.
- **Known Limitations:** See [limitations.md](../09_Evaluation/limitations.md) and [error_review.md](../09_Evaluation/error_review.md) (small `< 0.2%` lesion recall ceiling, cervical spine ghost superimposition, ordinal grading ambiguity, and cross-country radiolucency domain shift).
