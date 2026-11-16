# Installation guide — minimal data-tool runtime (STEP-002)

> This covers the minimal STEP-002 environment for registry checks, image inspection, coordinate tests, splitting, and preprocessing (`OS §10.3`). YOLO/GPU dependencies will be pinned separately in `environment/model/` at `STEP-023`.

## 1. Prerequisites

- Python `3.14` (tested with `3.14.6` on Windows 11 Pro 64-bit)
- Git (`2.x`)

## 2. Setup commands (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r environment\data\requirements.lock.txt
```

*(If creating on a fresh machine with a different Python path, recreate `.venv` locally — `.venv/` is excluded from Git by `.gitignore`.)*

## 3. Verify installation

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Expected: all smoke tests in `tests/test_smoke_data_env.py` pass (`3 passed`).
