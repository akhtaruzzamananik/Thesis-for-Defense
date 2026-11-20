# Model Card — `MODEL0013` (`EXP0011` TrackD Hanoi PAI 3–5 `1280×1280` `RQ2` Ablation `YOLO11s`)

| Field | Value |
|---|---|
| Model ID | `MODEL0013` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0011` / `RUN0011` / `CKPT0027` (`best.pt`, epoch `24`, `sha256:ac6dadc9...`, `19,334,554` bytes) |
| Matched Control | `EXP0005` / `MODEL0010` (`REL0004` `640×640` `PP0001`); single changed factor = `PP0004` (`1280×1280`, `batch=8`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `44` epochs / `8,618.9 s` [`143.6 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-21`)** |

## Validation Performance (`REL0004` `val`, `578` OPGs — `test` SEALED)
- **Selected `best.pt` (Epoch `24` / `44`):** **`P = 0.5355`**, **`R = 0.5747`**, **`F1 = 0.5544`**, **`mAP@0.50 = 0.5358`** (`0.536` final `BoxPR_curve.png`; peak `0.5416` at ep `20`), **`mAP@0.50:0.95 = 0.2514`**.
- **Delta vs `EXP0005` (`640×640`):** **`+0.048 mAP@0.50`** (`0.536` vs `0.488`), **`+0.0397 mAP@0.50:0.95`** (**`+18.8%` relative**), **`+0.0813 Recall`** (`57.5%` vs `49.3%`), **`+0.0471 F1`** — outperforming `P0008`'s published full-OPG `YOLO11m` (`0.528`) with half the parameters (`9.4M`).
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `DS0004_PAI_3` (**`0.555`**, `+7.0%`), `DS0004_PAI_4` (**`0.529`**, `+5.2%`), `DS0004_PAI_5` (**`0.522`**, `+2.0%`).
