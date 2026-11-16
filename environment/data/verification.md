# Minimal data-tool environment verification — STEP-002

| Field | Value |
|---|---|
| Date verified | 2026-11-16 |
| OS | Microsoft Windows 11 Pro (`10.0.26300`, 64-bit) |
| Python | `3.14.6` (`.venv` created from `C:\Users\ASUS\AppData\Local\Programs\Python\Python314\python.exe`) |
| Lockfile | `environment/data/requirements.lock.txt` |
| YOLO / GPU stack | **Deferred to STEP-023** (`OS §10.3`) |

## 1. Installed top-level packages

- `pillow==13.0.0`
- `numpy==2.5.5`
- `PyYAML==6.0.3`
- `pytest==9.2.0`

## 2. Smoke check command and result

Command run:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Observed output (`2026-11-16`):

```text
3 passed in 1.28s
- tests/test_smoke_data_env.py::test_synthetic_image_roundtrip_and_hash PASSED
- tests/test_smoke_data_env.py::test_coordinate_resize_roundtrip PASSED
- tests/test_smoke_data_env.py::test_yaml_and_decisions_csv_readable PASSED
```

*(Replaced an earlier broken `.venv` pointing to `C:\Users\mahaz\AppData\Local\Python\pythoncore-3.15-64\python.exe`.)*
