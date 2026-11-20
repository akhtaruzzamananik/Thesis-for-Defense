# Model Card — `MODEL0009` (`EXP0012` TrackC Dhaka `CLAHE 2.0` `RQ2` Ablation `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0009` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0012` / `RUN0012` / `CKPT0019` (`best.pt`, epoch `6`, `sha256:b9f0ab61...`, `19,178,394` bytes) |
| Matched Control | `EXP0004` / `MODEL0006` (`REL0003` Raw `PP0001`); single changed factor = `PP0002` (`CLAHE clip=2.0, grid=8×8`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `26` epochs / `101.7 s` [`1.7 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0003` `val`, `34` OPGs — `test` SEALED)
- **Best Epoch (`6` / `26`):** `P = 0.5956`, `R = 0.3478`, `F1 = 0.4391`, `mAP@0.50 = 0.2324` (`0.232` final `BoxPR_curve.png`), `mAP@0.50:0.95 = 0.1315`.
- **Delta vs `EXP0004` (`Raw PP0001`):** **`-0.027 mAP@0.50`** (`0.232` vs `0.259`) and **`-0.0191 mAP@0.50:0.95`** (`0.1315` vs `0.1506`), though `Impacted_Tooth` rose (`0.713 -> 0.776`) while `BDC_BDR` fell sharply (`0.452 -> 0.282`).
- **Scientific Finding (`RQ2`):** Directly refutes blanket `CLAHE` superiority claims on Dhaka smartphone-photographed OPG films (`P0024`).
