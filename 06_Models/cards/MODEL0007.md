# Model Card — `MODEL0007` (`EXP0007` TrackF Pediatric MD-OPG Caries Baseline `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0007` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0007` / `RUN0007` / `CKPT0015` (`best.pt`, epoch `36`, `sha256:c725343e...`, `19,179,034` bytes) |
| Data Release & Split | `REL0006` (`DS0006` MD-OPG Pediatric `TrackF`, `SPLIT0006`, `121` train / `25` val; **`24` test SEALED**) |
| Preprocessing | `PP0001` (`640×640` letterbox + black-border autocrop removing `66.17%` frame) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `56` epochs / `157.8 s` [`2.6 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** *(Valid negative/low-performance empirical result retained per OS §13.3)* |

## Validation Performance (`REL0006` `val`, `25` OPGs — `test` SEALED)
- **Best Epoch (`36` / `56`):** `P = 0.2004`, `R = 0.2037`, `F1 = 0.2020`, `mAP@0.50 = 0.0991` (`0.100` final `BoxPR_curve.png`), `mAP@0.50:0.95 = 0.0300`.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `DS0006_Occlusal_Caries` (`0.121`), `DS0006_Proximal_Caries` (`0.079`).
- **Scientific Finding:** Demonstrates severe data-scarcity (`N=121` mixed-dentition pediatric OPGs) + pinpoint interproximal radiolucency visibility limits on full-OPG `640px` detection (`GAP0004` / `P0032`).
