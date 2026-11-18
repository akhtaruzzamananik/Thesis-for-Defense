# Model & Execution Runtime Inventory (`STEP-023` / `UD11`)

| Field | Value |
|---|---|
| Step / Stage | `STEP-023` (`S10` — Pin and verify the execution environment) |
| Owner | Mahajub Al Shabah (`232-15-900`, Model Lead) & Akhtaruzzaman Anik (`232-15-252`, Research Lead) |
| Date | `2026-11-19` |
| Governing Sections | `OS §5`, `§8`, `§10`; Blueprint `STEP-023`; `DEC0011.md` (`UD11`) |
| Preserved Data Lock | `environment/data/requirements.lock.txt` & `environment/data/verification.md` (**preserved unchanged**, `G08` unaffected) |
| Model Lock File | `environment/model/requirements-kaggle.txt` (`ultralytics==8.3.253`, excluding PyPI `8.3.41/42/45/46`) |
| Verification Script | `13_Automation/verify_runtime_step023.py` |

---

## 1. Two-Tier Compute Architecture (`DEC0011` / `UD11`)

Per `DEC0011`, the project uses a **two-tier execution split** matching the actual hardware available to the team:

1. **Local PC (`CPU` Data, Preprocessing, Verification & `CPU` ONNX Inference Tier):**
   - Handles all `STEP-002`–`021` data governance, quality audits, grouped splitting, `PP0001–PP0004` preprocessing, `S14` CPU `FPS`/prototype checks, and `S16` local fallback inference.
2. **Kaggle Cloud GPU (`Tesla T4 16 GB` / `P100 16 GB`, Linux x86_64 — Training & GPU `FPS` Tier):**
   - Authorized cloud GPU destination for `STEP-026` smoke & checkpoint-recovery verification, `STEP-028`–`030` YOLO training (`YOLO11s`, `YOLOv8s`, `YOLO11m`), and `RQ3` GPU inference latency benchmarking.
   - **Data Privacy Compliance (`OS §1.5`, `STEP-023` Checklist #4):** Only **Private** Kaggle Datasets (`REL0001–REL0006` containing de-identified `DS0001–DS0006` public-license cohorts with `DS0003` EXIF stripped) may be attached; public Kaggle dataset visibility is strictly prohibited, and `test` / `external_test` partitions remain sealed until `STEP-031` (`G11`).

---

## 2. Observed Local Runtime Inventory (`2026-11-18T19:37:36Z`)

Captured directly by `python 13_Automation/verify_runtime_step023.py` (observed, not assumed):

| Property | Observed Local Value |
|---|---|
| **OS / Architecture** | `Windows-11-10.0.26300-SP0` (`AMD64`, `8` logical CPUs, `7,880 MB` RAM) |
| **Python** | `3.14.6` |
| **NVIDIA CUDA GPU** | **None locally (`nvidia-smi` absent; `cuda_available = false`)** — confirms cloud GPU (Kaggle) is required for training |
| **Verified Installed Packages** | `numpy==2.5.1`, `pillow==12.3.0`, `opencv-python==5.0.0.93`, `PyYAML==6.0.3`, `pytest==9.1.1`, `onnxruntime==1.32.0` (`CPUExecutionProvider`) |
| **Local `torch` / `ultralytics`** | `not-installed` (kept isolated in `environment/model/requirements-kaggle.txt` so `environment/data/` stays intact) |
| **Write Permission Smoke Check** | `write_permission_ok = true`, `onnxruntime_import_ok = true` |

---

## 3. Kaggle GPU Runtime Pin & Pending Live Session Capture (`Before G09`)

- **Pinned Package Specification (`environment/model/requirements-kaggle.txt`):**
  - `ultralytics==8.3.253` (safe `8.3.x` release supporting `YOLO11s`, `YOLOv8s`, and `YOLO11m`, explicitly avoiding compromised `8.3.41/42/45/46`)
  - `PyYAML>=6.0.2`, `onnx>=1.16.0`, `onnxruntime>=1.18.0`
  - Kaggle's preinstalled CUDA-matched `torch` and `torchvision` are preserved without blind wheel overwrites.
- **Exact GPU/Driver Capture Rule (`STEP-023` -> `STEP-026 / G09`):**
  - Because Kaggle's exact Linux kernel, CUDA driver, `torch`, and `Tesla T4`/`P100` VRAM values can only be observed inside the live Kaggle session, **no Kaggle `torch`/CUDA version is guessed here**.
  - On launching the first Kaggle GPU session (`STEP-026` smoke test), run `python 13_Automation/verify_runtime_step023.py > runtime_kaggle.json` and append the exact observed `torch`, `torchvision`, `cuda`, `cudnn`, and GPU device strings to `environment/model/` and `07_Experiments/EXP0000_SMOKE/run_manifest.json` before assessing **`G09`**.
