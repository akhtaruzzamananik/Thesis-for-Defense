# `STEP-034` Inference Speed, End-to-End Timing & `RQ3` Pareto Report (`UD14`)

| Field | Value |
|---|---|
| Step / Protocol | `STEP-034` (`09_Evaluation/protocol.md §2`, `DEC0014`, `FREEZE0001`) |
| Workload & Precision | Serial single-image streaming (`batch_size = 1`, `FP32`), `10` warm-up OPGs discarded + up to `100` consecutive held-out `test` OPGs timed |
| Timing Boundaries | Disk I/O & cold-start session load excluded and logged separately; **`T_e2e = T_pre (decode+RGB+autocrop+letterbox) + T_infer + T_post (NMS+inverse TransformLedger)`** |
| GPU Hardware | Kaggle `NVIDIA Tesla T4` (`torch 2.11.0+cu130`, `ultralytics 8.3.253`, explicit `torch.cuda.synchronize()`) |
| Local CPU Hardware | `11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz` (`7.7 GiB RAM`, `Windows 11`, `Python 3.14.6`, `onnxruntime 1.32.0` `CPUExecutionProvider`, `intra_threads=4`) |
| Failure Count | **`0` failures** across all GPU (`10` models) and CPU (`7` models) timed runs |

---

## 1. Combined GPU (`Tesla T4`) vs Local CPU (`ONNXRuntime`) Speed & Held-Out Accuracy Pareto Table (`RQ3`)

| `ModelID` | Track / Role | Arch `@imgsz` | `.pt` / `.onnx` (MB) | Held-Out `test mAP@50` (`mAP50-95`) | **GPU `T_e2e` mean / p95 (ms)** | **GPU `FPS_e2e`** (`FPS_inf`) | **CPU `T_e2e` mean / p95 (ms)** | **CPU `FPS_e2e`** (`FPS_inf`) | CPU Cold Load (ms) |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| `MODEL0005` | `TrackA` (`track_winner`) | `YOLO11s@1280` | `18.4` / `36.6` | `0.4165` (`0.1741`) | `108.2` / `118.7` | **`9.24`** (`20.20`) | `878.1` / `1224.0` | **`1.14`** (`1.24`) | `237.9` |
| `MODEL0001` | `TrackA` (`rq1_rq3_comparator`) | `YOLO11s@640` | `18.3` / `36.2` | `0.3815` (`0.1577`) | `71.4` / `78.0` | **`14.00`** (`37.63`) | `263.4` / `402.7` | **`3.80`** (`4.92`) | `234.2` |
| `MODEL0002` | `TrackA` (`rq1_rq3_comparator`) | `YOLOv8s@640` | `21.5` / `42.7` | `0.3786` (`0.1578`) | `74.5` / `81.5` | **`13.42`** (`34.12`) | `266.0` / `330.7` | **`3.76`** (`4.62`) | `213.9` |
| `MODEL0003` | `TrackA` (`rq1_rq3_comparator`) | `YOLO11m@640` | `38.7` / `76.7` | `0.3990` (`0.1682`) | `76.1` / `82.6` | **`13.14`** (`32.03`) | `512.4` / `706.0` | **`1.95`** (`2.17`) | `460.8` |
| `MODEL0004` | `TrackB` (`track_winner`) | `YOLO11s@640` | `18.3` / — | `0.4397` (`0.2673`) | `72.6` / `77.9` | **`13.78`** (`36.46`) | *(not exported)* | — | — |
| `MODEL0006` | `TrackC` (`track_winner`) | `YOLO11s@640` | `18.3` / — | `0.2508` (`0.1406`) | `26.2` / `38.8` | **`38.20`** (`70.39`) | *(not exported)* | — | — |
| `MODEL0013` | `TrackD` (`track_winner`) | `YOLO11s@1280` | `18.4` / `36.6` | `0.4868` (`0.2207`) | `90.4` / `93.1` | **`11.06`** (`20.75`) | `847.9` / `1002.0` | **`1.18`** (`1.27`) | `238.4` |
| `MODEL0010` | `TrackD` (`rq2_rq3_comparator`) | `YOLO11s@640` | `18.3` / `36.1` | `0.4419` (`0.1836`) | `56.3` / `58.1` | **`17.77`** (`42.39`) | `181.9` / `215.4` | **`5.50`** (`7.07`) | `222.0` |
| `MODEL0008` | `TrackE` (`track_winner`) | `YOLO11s@640` | `18.3` / `36.1` | `0.8246` (`0.5163`) | `81.4` / `85.6` | **`12.28`** (`35.77`) | `201.6` / `225.5` | **`4.96`** (`7.08`) | `158.8` |
| `MODEL0007` | `TrackF` (`track_winner`) | `YOLO11s@640` | `18.3` / — | `0.0537` (`0.0111`) | `157.4` / `172.2` | **`6.35`** (`35.88`) | *(not exported)* | — | — |

---

## 2. Stage-by-Stage CPU Latency Breakdown & PyTorch-to-ONNX Parity Check (`7` Exported Models)

| `ModelID` | Arch `@imgsz` | `T_pre` mean (ms) | `T_infer` mean ± sd (ms) | `T_post` mean (ms) | `T_e2e` median (IQR) (ms) | Parity Boxes (`5` OPGs) | Mean Box IoU vs PyTorch | Mean `|Δscore|` |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `MODEL0005` | `YOLO11s@1280` | `67.35` | `806.75 ± 172.87` | `3.97` | `815.17` (`178.24`) | `82` | **`0.99234`** | `0.0021` |
| `MODEL0001` | `YOLO11s@640` | `58.95` | `203.10 ± 54.50` | `1.34` | `244.45` (`106.59`) | `98` | **`0.99537`** | `0.00279` |
| `MODEL0002` | `YOLOv8s@640` | `48.11` | `216.70 ± 28.64` | `1.17` | `260.10` (`39.52`) | `80` | **`0.98421`** | `0.00611` |
| `MODEL0003` | `YOLO11m@640` | `51.06` | `460.29 ± 85.23` | `1.09` | `480.63` (`127.10`) | `77` | **`0.99651`** | `0.00157` |
| `MODEL0013` | `YOLO11s@1280` | `56.62` | `789.69 ± 82.26` | `1.57` | `827.35` (`119.57`) | `13` | **`0.99406`** | `0.01135` |
| `MODEL0010` | `YOLO11s@640` | `39.94` | `141.37 ± 14.29` | `0.56` | `178.36` (`19.50`) | `7` | **`0.9829`** | `0.00705` |
| `MODEL0008` | `YOLO11s@640` | `59.58` | `141.24 ± 17.72` | `0.77` | `201.42` (`18.84`) | `46` | **`0.99416`** | `0.00229` |

---

## 3. Honest Deployment & `RQ3` Interpretation Notes (`OS §7.3`)

1. **Model-Only vs End-to-End Gap:** Across all `10` models on `Tesla T4`, pure model+NMS `FPS_infer` (`20.2–70.4 FPS`) is `1.8×–5.6×` higher than true end-to-end `FPS_e2e` (`6.35–38.20 FPS`) because full-resolution OPG decoding (`~2000×1000 px`), letterboxing, and `DS0006` black-border autocrop consume `15–130 ms/OPG` on CPU. Reporting model-only FPS without end-to-end boundaries overstates operational throughput.
2. **Resolution vs Scale Pareto Frontier (`TrackA`):** Upgrading `YOLO11s` from `640px` (`MODEL0001`) to `1280px` (`MODEL0005`) gained **`+0.0350` internal `test mAP@0.50`** (`+0.0622` on `external_test`) while reducing GPU `FPS_e2e` from `14.00` to `9.24 FPS` (`~0.11 s/OPG`) and increasing CPU `T_e2e` (`~4×` input pixels). By contrast, doubling parameters at `640px` (`YOLO11m` `MODEL0003`, `80.4 MB` ONNX) yielded smaller internal test gains (`+0.0175`) at `2.1×` memory footprint.
3. **CPU Feasibility for `S16` Web Research Showcase:** On a standard laptop CPU (`Intel i5-1135G7`, no GPU), `MODEL0008` (`TrackE UAE@640`, `mAP@0.50 = 0.8246`) runs interactive single-OPG inference well under `0.5 s/OPG`, and even `1280px` `MODEL0005` / `MODEL0013` complete single-radiograph research showcase inference in `~0.5–1.0 s/OPG` — suitable for an interactive non-clinical web demonstration on free CPU tiers without claiming real-time video throughput or clinical workflow clearance.
4. **Variability & Non-Clinical Boundary:** Single-machine CPU latencies reflect background OS scheduling and thermal scaling (`IQR` & `p95` reported transparently above; raw `100`-image samples archived in `09_Evaluation/timing/*_cpu_raw_samples.csv`). No clinical throughput claim is made.
