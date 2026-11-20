# Model Card — `MODEL0004` (`EXP0003` TrackB DENTEX `4`-Class Baseline `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0004` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0003` / `RUN0003` / `CKPT0009` (`best.pt`, epoch `32`, `sha256:33c6453d...`, `19,180,122` bytes) |
| Data Release & Split | `REL0002` (`DS0002` DENTEX `TrackB`, `SPLIT0002`, `493` train / `106` val; **`106` test SEALED**) |
| License | `AGPL-3.0` (`ultralytics`) + **`CC-BY-NC-SA-4.0` (`DS0002` strictly non-commercial / isolated)** |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `52` epochs / `531.3 s`, `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0002` `val`, `106` OPGs — `test` SEALED)
- **Selected `best.pt` (Epoch `32` / `52`):** `P = 0.5079`, `R = 0.4494`, `F1 = 0.4769`, `mAP@0.50 = 0.4438` (`0.443` final `BoxPR_curve.png`; peak `mAP@0.50 = 0.4588` at ep `12`), `mAP@0.50:0.95 = 0.2913`.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `DS0002_Impacted` (**`0.925`**), `DS0002_Deep_Caries` (`0.397`), `DS0002_Caries` (`0.335`), `DS0002_Periapical_Lesion` (`0.117` — `14:1` minority skew, `158` boxes dataset-wide).
