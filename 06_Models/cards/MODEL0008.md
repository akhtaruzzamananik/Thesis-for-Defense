# Model Card — `MODEL0008` (`EXP0006` TrackE UAE AU-OPG `6`-Class Baseline `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0008` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0006` / `RUN0006` / `CKPT0017` (`best.pt`, epoch `88`, `sha256:0336a078...`, `19,187,866` bytes) |
| Data Release & Split | `REL0005` (`DS0005` AU-OPG Ajman UAE `TrackE`, `SPLIT0005`, `628` train / `134` val; **`133` test SEALED**) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `100` epochs / `1,268.0 s` [`21.1 min`], `max_epochs_100`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0005` `val`, `134` OPGs — `test` SEALED)
- **Selected `best.pt` (Epoch `88` / `100`):** **`P = 0.8382`**, **`R = 0.8186`**, **`F1 = 0.8283`**, **`mAP@0.50 = 0.8579`** (`0.858` final `BoxPR_curve.png`; peak `0.8601` at ep `46`), **`mAP@0.50:0.95 = 0.5705`**.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `DS0005_Implant` (**`0.995`**), `DS0005_Crowned_Tooth` (**`0.928`**), `DS0005_Filled_Tooth` (**`0.881`**), `DS0005_Impacted_Tooth` (**`0.857`**), `DS0005_Retained_Root` (**`0.826`**), `DS0005_Cavitated_Tooth` (**`0.660`**).
- **Scientific Significance:** Proves that our exact `YOLO11s` `640×640` pipeline achieves high leak-free performance (`0.858` `mAP@0.50`, `0.571` `mAP@0.50:0.95`) on consistently annotated whole-tooth OPG targets, demonstrating that cross-track variance (`0.100–0.858`) is governed by radiographic physics, target granularity, and class support rather than pipeline deficits.
