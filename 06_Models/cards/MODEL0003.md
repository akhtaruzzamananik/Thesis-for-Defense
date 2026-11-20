# Model Card — `MODEL0003` (`EXP0013` Scale Comparator `YOLO11m` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0003` |
| Candidate / Architecture | `MC0003` (`ultralytics==8.3.253` `YOLO11m`, COCO-pretrained `yolo11m.pt`, `sha256:d5ffc1a6...`) |
| Experiment / Run / Checkpoint | `EXP0013` / `RUN0013` / `CKPT0007` (`best.pt`, epoch `42`, `sha256:a5a89aa4...`, `40,535,276` bytes) |
| Matched Control | `EXP0001` / `MODEL0001` (`YOLO11s` @ `640×640`, identical `REL0001`, `PP0001`, seed `20261124`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `62` epochs / `2,500.7 s`, `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0001` `val`, `214` OPGs — `test` SEALED)
- **Best Epoch (`42` / `62`):** `P = 0.4809`, `R = 0.4324`, `F1 = 0.4553`, `mAP@0.50 = 0.3906` (`0.390` final `BoxPR_curve.png`), `mAP@0.50:0.95 = 0.1583`.
- **Delta vs `EXP0001` (`YOLO11s`):** `+0.009 mAP@0.50` (`0.390` vs `0.381`), `+0.0013 mAP@0.50:0.95`, `+0.0120 Recall`, `+0.0147 Precision`, `+0.0132 F1` at `2.1×` weight size (`40.5 MB` vs `19.2 MB`).
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `Surgical_Device` (`0.899`), `Endodontic_Treatment` (`0.677`), `Impacted_Tooth` (`0.557`), `Prosthetic_Restoration` (`0.544`), `Root_Fragment` (`0.473`), `Obturation` (`0.451`), `Implant` (`0.442`), `Orthodontic_Device` (`0.313`), `Furcation_Lesion` (`0.233`), `Carious_Lesion` (`0.197`), `Apical_Periodontitis` (`0.190`), `Bone_Resorption` (`0.096`), `Apical_Surgery` (`0.002`).
