# Model Card — `MODEL0006` (`EXP0004` TrackC Dhaka Bangladeshi Handheld OPG Baseline `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0006` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0004` / `RUN0004` / `CKPT0013` (`best.pt`, epoch `34`, `sha256:966d9abc...`, `19,181,978` bytes) |
| Data Release & Split | `REL0003` (`DS0003` Rahman 2024 Dhaka `TrackC`, `SPLIT0003`, `163` train / `34` val; **`33` test SEALED**) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `54` epochs / `202.6 s` [`3.4 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0003` `val`, `34` OPGs — `test` SEALED)
- **Selected `best.pt` (Epoch `34` / `54`):** `P = 0.4343`, `R = 0.3022`, `F1 = 0.3564`, `mAP@0.50 = 0.2588` (`0.259` final `BoxPR_curve.png`; `0.2660` at ep `54`), `mAP@0.50:0.95 = 0.1506`.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `DS0003_Impacted_Tooth` (**`0.713`**), `DS0003_BDC_BDR` (`0.452`), `DS0003_Healthy_Tooth` (`0.210` — selective annotation artifact), `DS0003_Caries_Tooth` (`0.160`), `DS0003_Infection_Tooth` (`0.019`, ultra-rare `N=37`), `DS0003_Fractured_Tooth` (`0.000`, ultra-rare `N=14`).
- **Matched Ablation Control:** Serves as the unenhanced `PP0001` anchor for **`EXP0012`** (`PP0002` `CLAHE 2.0 8×8` falsifiable test of `P0024`).
