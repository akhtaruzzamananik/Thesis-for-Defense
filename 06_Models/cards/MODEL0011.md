# Model Card — `MODEL0011` (`EXP0008` TrackA `CLAHE 2.0 8×8` `RQ2` Ablation `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0011` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0008` / `RUN0008` / `CKPT0023` (`best.pt`, epoch `31`, `sha256:4c0c769a...`, `19,186,586` bytes) |
| Matched Control | `EXP0001` / `MODEL0001` (`REL0001` Raw `PP0001`); single changed factor = `PP0002` (`CLAHE clip=2.0, grid=8×8`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `46` epochs / `1,474.9 s` [`24.6 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0001` `val`, `214` OPGs — `test` SEALED)
- **Selected `best.pt` (Epoch `31` / `46`):** `P = 0.4418`, `R = 0.3946`, `F1 = 0.4169`, `mAP@0.50 = 0.3498` (`0.344` final `BoxPR_curve.png`; peak `0.3540` at ep `34`), `mAP@0.50:0.95 = 0.1479`.
- **Delta vs `EXP0001` (`Raw PP0001`):** **`-0.037 mAP@0.50`** (`0.344` vs `0.381`) and **`-0.0091 mAP@0.50:0.95`** (`0.1479` vs `0.1570`), degrading **12 of 13 classes** (including `Carious_Lesion` `0.173 -> 0.122`, `Apical_Periodontitis` `0.198 -> 0.148`, `Impacted_Tooth` `0.643 -> 0.559`).
- **Scientific Finding (`RQ2`):** Replicates `EXP0012` (Dhaka `-0.027`) and confirms `P0011` (`Scarano 2026`): `CLAHE 2.0` consistently degrades YOLO OPG detection across distinct scanners/cohorts.
