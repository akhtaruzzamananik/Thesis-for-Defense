# `STEP-032` Final-Test Prediction Generation & Integrity Validation Report

- **Freeze ID:** `FREEZE0001` (`freeze_manifest_sha256: d6147ffe5a0e6173da4440185c7cddacc2296aaf71908f0388e7aecf9e234ba1`)
- **Hardware / Runtime:** `Tesla T4` | `torch 2.11.0+cu130` | `ultralytics 8.3.253`
- **Execution Window (UTC):** `2026-11-20T20:24:27.148500+00:00` -> `2026-11-20T20:34:42.065854+00:00`
- **Total Errors Across All Runs:** `0`

## 1. In-Domain Held-Out Evaluations (`EVAL0001–EVAL0014`)

| `EvalID` | `ModelID` | `Release:Partition` | Coverage | Zero-Det `@op` | Boxes `@op` | Invalid Boxes/Cls | `predictions_sha256` |
|---|---|---|---:|---:|---:|---:|---|
| `EVAL0001` | `MODEL0005` | `REL0001:test` | `208/208` (`100%`) | `1` | `2545` | `1` filtered (`0` persisted) / `0` | `65c8ec253213...` |
| `EVAL0002` | `MODEL0005` | `REL0001:external_test` | `178/178` (`100%`) | `1` | `2299` | `0` filtered (`0` persisted) / `0` | `a731236c1c99...` |
| `EVAL0003` | `MODEL0001` | `REL0001:test` | `208/208` (`100%`) | `0` | `2622` | `0` filtered (`0` persisted) / `0` | `36901051eb67...` |
| `EVAL0004` | `MODEL0001` | `REL0001:external_test` | `178/178` (`100%`) | `1` | `2026` | `0` filtered (`0` persisted) / `0` | `8917852ad619...` |
| `EVAL0005` | `MODEL0002` | `REL0001:test` | `208/208` (`100%`) | `2` | `2596` | `0` filtered (`0` persisted) / `0` | `ef211446d59a...` |
| `EVAL0006` | `MODEL0002` | `REL0001:external_test` | `178/178` (`100%`) | `1` | `2218` | `0` filtered (`0` persisted) / `0` | `571628957902...` |
| `EVAL0007` | `MODEL0003` | `REL0001:test` | `208/208` (`100%`) | `2` | `2486` | `1` filtered (`0` persisted) / `0` | `c816271ae854...` |
| `EVAL0008` | `MODEL0003` | `REL0001:external_test` | `178/178` (`100%`) | `1` | `2157` | `0` filtered (`0` persisted) / `0` | `d4954a78971d...` |
| `EVAL0009` | `MODEL0004` | `REL0002:test` | `106/106` (`100%`) | `2` | `690` | `0` filtered (`0` persisted) / `0` | `560671ee4618...` |
| `EVAL0010` | `MODEL0006` | `REL0003:test` | `33/33` (`100%`) | `0` | `256` | `0` filtered (`0` persisted) / `0` | `2f651a49d18d...` |
| `EVAL0011` | `MODEL0013` | `REL0004:test` | `578/578` (`100%`) | `57` | `1073` | `0` filtered (`0` persisted) / `0` | `52458d3592ba...` |
| `EVAL0012` | `MODEL0010` | `REL0004:test` | `578/578` (`100%`) | `90` | `917` | `0` filtered (`0` persisted) / `0` | `8749eea37392...` |
| `EVAL0013` | `MODEL0008` | `REL0005:test` | `133/133` (`100%`) | `1` | `1008` | `0` filtered (`0` persisted) / `0` | `7ac32d8cdf75...` |
| `EVAL0014` | `MODEL0007` | `REL0006:test` | `24/24` (`100%`) | `1` | `99` | `0` filtered (`0` persisted) / `0` | `4475e578f56d...` |

## 2. Cross-Country Zero-Shot Shift Passes (`HC01–HC05`)

| Pass Key | Bridges | Coverage | Boxes `@op` | `predictions_sha256` |
|---|---|---:|---:|---|
| `MODEL0005_to_REL0005_test` | `XSHIFT01` | `133/133` | `1278` | `761bb5d33c52...` |
| `MODEL0005_to_REL0003_test` | `XSHIFT03_A` | `33/33` | `302` | `fd89fca9091d...` |
| `MODEL0005_to_REL0002_test` | `XSHIFT04_A` | `106/106` | `783` | `06eb72b1ec7c...` |
| `MODEL0005_to_REL0004_test` | `XSHIFT05_A2D` | `578/578` | `3787` | `0b993485e336...` |
| `MODEL0013_to_REL0001_test` | `XSHIFT05_D2A_INT` | `208/208` | `292` | `924a7b6b340c...` |
| `MODEL0013_to_REL0001_external_test` | `XSHIFT05_D2A_EXT` | `178/178` | `267` | `a6fa7bfb3157...` |
| `MODEL0008_to_REL0001_test` | `XSHIFT02_INT` | `208/208` | `1830` | `b74de4bf5f8d...` |
| `MODEL0008_to_REL0001_external_test` | `XSHIFT02_EXT` | `178/178` | `1517` | `4309ca4618c0...` |
| `MODEL0008_to_REL0003_test` | `XSHIFT03_E, XSHIFT06_E2C` | `33/33` | `187` | `afff555dfe0d...` |
| `MODEL0008_to_REL0002_test` | `XSHIFT04_E, XSHIFT06_E2B` | `106/106` | `595` | `0188e6e452ef...` |

## 3. GPU Timing (`UD14`, Serial `BS=1`, `FP32`, CUDA-Synced) & `ONNX` Exports

| `ModelID` | Arch / `imgsz` | `T_pre` (ms) | `T_infer+NMS` (ms) | `T_e2e` (ms) | `FPS_e2e` | `ONNX` Export (Off-Git) |
|---|---|---:|---:|---:|---:|---|
| `MODEL0005` | `YOLO11s@1280` | `58.21` | `49.52` | `108.25` | **`9.24`** | `36.6 MB` (`03a28f1553...`) |
| `MODEL0001` | `YOLO11s@640` | `44.49` | `26.57` | `71.44` | **`14.00`** | `36.2 MB` (`5455598718...`) |
| `MODEL0002` | `YOLOv8s@640` | `44.77` | `29.31` | `74.52` | **`13.42`** | `42.7 MB` (`b93fbf20fd...`) |
| `MODEL0003` | `YOLO11m@640` | `44.48` | `31.22` | `76.13` | **`13.14`** | `76.7 MB` (`4344e19e50...`) |
| `MODEL0004` | `YOLO11s@640` | `44.94` | `27.42` | `72.55` | **`13.78`** | Not requested |
| `MODEL0006` | `YOLO11s@640` | `11.79` | `14.21` | `26.18` | **`38.20`** | Not requested |
| `MODEL0013` | `YOLO11s@1280` | `42.07` | `48.18` | `90.43` | **`11.06`** | `36.6 MB` (`cc0a331657...`) |
| `MODEL0010` | `YOLO11s@640` | `32.52` | `23.59` | `56.29` | **`17.77`** | `36.1 MB` (`e74c46f2f3...`) |
| `MODEL0008` | `YOLO11s@640` | `53.29` | `27.95` | `81.41` | **`12.28`** | `36.1 MB` (`b26b436734...`) |
| `MODEL0007` | `YOLO11s@640` | `129.32` | `27.87` | `157.41` | **`6.35`** | Not requested |
