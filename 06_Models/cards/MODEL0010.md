# Model Card — `MODEL0010` (`EXP0005` TrackD Hanoi PAI 3–5 `640×640` Baseline `YOLO11s`)

| Field | Value |
|---|---|
| Model ID | `MODEL0010` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0005` / `RUN0005` / `CKPT0021` (`best.pt`, epoch `25`, `sha256:305d279c...`, `19,178,394` bytes) |
| Data Release & Split | `REL0004` (`DS0004` Do 2024 Hanoi PAI 3–5 `TrackD`, `SPLIT0004`, `2,707` train / `578` val; **`578` test SEALED**) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `45` epochs / `2,491.6 s` [`41.5 min`], `early_stop_patience_20`) |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

## Validation Performance (`REL0004` `val`, `578` OPGs — `test` SEALED)
- **Best Epoch (`25` / `45`):** `P = 0.5221`, `R = 0.4934`, `F1 = 0.5073`, **`mAP@0.50 = 0.4878`** (`0.488` final `BoxPR_curve.png`), **`mAP@0.50:0.95 = 0.2117`**.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):** `DS0004_PAI_5` (**`0.502`**), `DS0004_PAI_3` (**`0.485`**), `DS0004_PAI_4` (**`0.477`**) — balanced across all 3 ordinal severity grades.
- **Matched Ablation Control:** Serves as the `640×640` `PP0001` anchor for **`EXP0011`** (`1280×1280` `PP0004` high-resolution test on tiny periapical apices).
