# Model Card — `MODEL0005` (`EXP0010` High-Res `1280×1280` `YOLO11s` `RQ2` Ablation)

| Field | Value |
|---|---|
| Model ID | `MODEL0005` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0010` / `RUN0010` / `CKPT0011` (`best.pt`, epoch `25`, `sha256:6a845f99...`, `19,342,746` bytes) |
| Matched Control | `EXP0001` / `MODEL0001` (`YOLO11s` @ `640×640` `PP0001`); single changed factor = `PP0004` (`1280×1280`, `batch=8`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `45` epochs / `3,467.9 s` [`57.8 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0001` `val`, `214` OPGs — `test` SEALED)
- **Best Epoch (`25` / `45`):** `P = 0.4859`, `R = 0.4150`, `F1 = 0.4477`, **`mAP@0.50 = 0.3906`** (`0.391` final `BoxPR_curve.png`), **`mAP@0.50:0.95 = 0.1656`** *(highest `mAP@0.50:0.95` among all TrackA runs)*.
- **Delta vs `EXP0001` (`640×640`):** `+0.010 mAP@0.50` (`0.391` vs `0.381`), `+0.0086 mAP@0.50:0.95` (`+5.5%` relative), matching `EXP0013` (`YOLO11m` `640px`, `0.391`) while outperforming it on tight `mAP@0.50:0.95` (`0.1656` vs `0.1583`) at half the model size (`19.3 MB` vs `40.5 MB`).
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `Surgical_Device` (`0.886`), `Endodontic_Treatment` (`0.667`), `Impacted_Tooth` (`0.618`), `Prosthetic_Restoration` (`0.535`), `Root_Fragment` (`0.453`), `Implant` (`0.427`), `Obturation` (`0.424`), `Orthodontic_Device` (**`0.389`** vs `0.265` @640), `Carious_Lesion` (`0.198` vs `0.173`), `Apical_Periodontitis` (`0.180`), `Furcation_Lesion` (`0.180` vs `0.150`), `Bone_Resorption` (`0.069`), `Apical_Surgery` (`0.054` vs `0.010`).
