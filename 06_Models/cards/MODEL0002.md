# Model Card — `MODEL0002` (`EXP0002` Cross-Generation Comparator `YOLOv8s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0002` |
| Candidate / Architecture | `MC0002` (`ultralytics==8.3.253` `YOLOv8s`, COCO-pretrained `yolov8s.pt`, `sha256:1f47a78b...`) |
| Experiment / Run / Checkpoint | `EXP0002` / `RUN0002` / `CKPT0005` (`best.pt`, epoch `17`, `sha256:2f4b5b27...`, `22,527,018` bytes) |
| Matched Control | `EXP0001` / `MODEL0001` (`YOLO11s` @ `640×640`, identical `REL0001`, `PP0001`, seed `20261124`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `37` epochs / `727.7 s`, `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0001` `val`, `214` OPGs — `test` SEALED)
- **Best Epoch (`17` / `37`):** `P = 0.5261`, `R = 0.3993`, `F1 = 0.4540`, `mAP@0.50 = 0.3637` (`0.364` final `BoxPR_curve.png`), `mAP@0.50:0.95 = 0.1523`.
- **Delta vs `EXP0001` (`YOLO11s`):** `-0.017 mAP@0.50` (`0.364` vs `0.381`), `-0.0047 mAP@0.50:0.95`, `-0.0211 Recall`, `+0.0599 Precision`.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `Surgical_Device` (`0.891`), `Endodontic_Treatment` (`0.633`), `Impacted_Tooth` (`0.558`), `Prosthetic_Restoration` (`0.478`), `Implant` (`0.466`), `Obturation` (`0.420`), `Root_Fragment` (`0.389`), `Orthodontic_Device` (`0.365`), `Apical_Periodontitis` (`0.180`), `Carious_Lesion` (`0.136`), `Furcation_Lesion` (`0.111`), `Bone_Resorption` (`0.094`), `Apical_Surgery` (`0.004`).
