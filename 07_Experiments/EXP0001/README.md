# `EXP0001` — Primary Multi-Class Baseline (`TrackA` / `REL0001` / `YOLO11s` / `PP0001`)

| Field | Value |
|---|---|
| Experiment ID | `EXP0001` |
| Research Questions | `RQ0`, `RQ1` |
| Purpose | `primary_baseline` (Anchor for `EXP0002` `YOLOv8s`, `EXP0008–EXP0010` `RQ2` ablations, `EXP0013` `YOLO11m`) |
| Release / Split / Batch | `REL0001` / `SPLIT0001` / `ANNB0001` (`DS0001` `TrackA`, `13` classes) |
| Model / Preprocessing | `MC0001` (`YOLO11s`, `ultralytics==8.3.253`) / `PP0001` (`640×640` raw letterbox) |
| Partitions Allowed | `train` (`994` OPGs) + `val` (`214` OPGs) — **`test` (`208`) & `external_test` (`178`) SEALED** |
| Prelaunch Status | **`READY_TO_LAUNCH_G09_PASS`** *(G09 PASS verified on Kaggle Tesla T4 `2026-11-19`)* |

---

## 1. Scientific Hypothesis & Controlled Factors

- **Hypothesis:** A single-stage anchor-free `YOLO11s` (`MC0001`) trained with raw letterbox `640×640` (`PP0001`) on deduplicated patient-grouped `REL0001` (`TrackA`, `13` classes) establishes a leak-free, reproducible baseline and quantifies small-lesion recall vs common restoration/crown precision (`RQ0`, `RQ1`).
- **Controlled Factors (`DEC0012`):** `seed=20261124`, `deterministic=true`, `AdamW` (`lr0=0.001`, `lrf=0.01`), `epochs=100`, `patience=20` on `val mAP@0.50`, `batch_size=16`, `amp=true`, `fliplr=0.0` (dental left/right laterality preserved).

---

## 2. Resource Estimate (Kaggle GPU)

- **Dataset size:** `994` train + `214` val = `1,208` `640×640` images (`~125–160 MB` zipped off-Git).
- **Estimated Kaggle `T4`/`P100` runtime (`100` max epochs, `batch=16`):** ~`25–45` minutes (early stopping at `patience=20` may finish sooner).

---

## 3. Launch Checklist (`STEP-027` Gate)

- [x] `config.yaml` (`T14`) has zero `null` fields and passes `run_pipeline.py validate-config`.
- [x] All input SHA-256 hashes (`REL0001`, `SPLIT0001`, `classes.csv`, `PP0001`, `protocol.md`) verified.
- [x] `test` and `external_test` partitions excluded from `allowed_partitions` and Kaggle bundle.
- [x] Full `REL0001` `PP0001` Kaggle bundle (`994 train / 214 val`) exported off-Git (`08_Checkpoints/artifacts/EXP0001_REL0001_PP0001_bundle.zip`).
- [x] **`G09 == PASS`** (verified `2026-11-19` on Kaggle `Tesla T4` via `08_Checkpoints/manifests/EXP0000_SMOKE_g09_report.json`).
- [ ] Researcher launches `EXP0001` (`STEP-028`) only after `G09 == PASS`.
