# Installation & Runtime Setup Guide (`STEP-002` Data Runtime + `STEP-023` Model Runtime)

> **Two-Environment Policy (`STEP-023` / `OS §10.3`):** `environment/data/` governs the Local PC Python `3.14.6` data/preprocessing/registry runtime and is **preserved unchanged**. `environment/model/` governs the Kaggle GPU training runtime and Local PC ONNX-CPU inference runtime.

---

## Part A — Local PC Minimal Data-Tool Runtime (`environment/data/`, `STEP-002`)

### 1. Prerequisites
- Python `3.14` (tested with `3.14.6` on Windows 11 Pro 64-bit, `8` CPUs, `7,880 MB` RAM)
- Git (`2.x`)

### 2. Setup commands (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r environment\data\requirements.lock.txt
```
*(If creating on a fresh machine with a different Python path, recreate `.venv` locally — `.venv/` is excluded from Git by `.gitignore`.)*

### 3. Verify data-tool installation
```powershell
python 13_Automation/validate_repo.py
python -m pytest -q
```

---

## Part B — Kaggle GPU Model Training Runtime (`environment/model/`, `STEP-023`)

Use a **Kaggle Notebook** with **Accelerator: `GPU T4 x2` or `GPU P100`** and **Persistence: `Files only`** (and attach only **Private** Kaggle Datasets for `REL0001–REL0006` `train`/`val` partitions).

### 1. Cell 1 — Clone repo & install pinned YOLO package
```bash
!git clone https://github.com/akhtaruzzamananik/Thesis-for-Defense.git /kaggle/working/repo
%cd /kaggle/working/repo
!pip install -q --no-deps ultralytics==8.3.253
!pip install -q thop>=0.1.1 ultralytics-thop>=2.0.18
```
*(If any transitive ultralytics dependency is missing in a future Kaggle image, run `pip install -q -r environment/model/requirements-kaggle.txt`.)*

### 2. Cell 2 — Capture exact observed GPU, CUDA, PyTorch & Ultralytics inventory (`STEP-023`)
```bash
!python 13_Automation/verify_runtime_step023.py | tee /kaggle/working/runtime_kaggle.json
```
Verify that the printed JSON shows:
- `"cuda_available": true`
- `"ultralytics_import_ok": true` (`8.3.253`)
- `"torch_tensor_smoke_ok": true`
- `"write_permission_ok": true`

Download `/kaggle/working/runtime_kaggle.json` and save it alongside the `STEP-026` smoke record so every `EXP####` logs observed hardware and driver versions (`OS §5.2`, `STEP-023` checklist).
