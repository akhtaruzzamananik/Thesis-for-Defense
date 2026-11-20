# Model Card — `MODEL0012` (`EXP0009` TrackA `CLAHE 3.0 16×16` `RQ2` Ablation `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0012` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0009` / `RUN0009` / `CKPT0025` (`best.pt`, epoch `30`, `sha256:ef03d631...`, `19,187,098` bytes) |
| Matched Control | `EXP0001` / `MODEL0001` (`REL0001` Raw `PP0001`); single changed factor = `PP0003` (`CLAHE clip=3.0, grid=16×16`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `50` epochs / `1,052.3 s` [`17.5 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0001` `val`, `214` OPGs — `test` SEALED)
- **Best Epoch (`30` / `50`):** `P = 0.5441`, `R = 0.3867`, `F1 = 0.4521`, `mAP@0.50 = 0.3628` (`0.363` final `BoxPR_curve.png`), `mAP@0.50:0.95 = 0.1472`.
- **Delta vs `EXP0001` (`Raw PP0001`):** **`-0.018 mAP@0.50`** (`0.363` vs `0.381`) and **`-0.0098 mAP@0.50:0.95`** (`0.1472` vs `0.1570`); degrades all radiolucent lesion classes (`Carious_Lesion` `0.173 -> 0.116`, `Bone_Resorption` `0.094 -> 0.054`, `Furcation_Lesion` `0.150 -> 0.113`, `Apical_Periodontitis` `0.198 -> 0.174`).
- **Scientific Finding (`RQ2`):** Completes the `3/3` consistent `CLAHE` ablation (`EXP0008`, `EXP0009`, `EXP0012`): unenhanced raw OPG outperforms both `CLAHE 2.0 (8×8)` and `CLAHE 3.0 (16×16)`.
