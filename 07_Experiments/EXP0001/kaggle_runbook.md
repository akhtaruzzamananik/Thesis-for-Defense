# `EXP0001` Kaggle GPU Launch & Recovery Runbook (`STEP-028`)

| Field | Value |
|---|---|
| Experiment ID | `EXP0001` (`Primary Multi-Class Baseline — TrackA / REL0001 / YOLO11s / PP0001`) |
| Registered Config | [config.yaml](config.yaml) (`sha256: 3a168d88bc04d6c6a0258c40a0e6896661bf4c890a92c89f3020cb860c40b1f6`) |
| Off-Git Bundle | `08_Checkpoints/artifacts/EXP0001_REL0001_PP0001_bundle.zip` (`94.47 MB`, `994 train / 214 val`) |
| Runner Script | [kaggle_train_exp.py](../../13_Automation/kaggle_train_exp.py) |
| Prerequisite | **`G09 == PASS`** via `EXP0000_SMOKE` (`kaggle_smoke_g09.py`) before launching `EXP0001` |

---

## 1. Exact Kaggle Execution Steps

### Step A — Verify `G09` Smoke First (One-Time Gate)
1. Upload `08_Checkpoints/artifacts/EXP0000_SMOKE_bundle.zip` (`5.14 MB`) + `13_Automation/kaggle_smoke_g09.py` to a Kaggle GPU notebook (`T4 x2` or `P100`).
2. Run:
   ```bash
   pip install -q ultralytics==8.3.253
   python kaggle_smoke_g09.py --data-yaml /kaggle/input/exp0000-smoke-bundle/dataset.yaml --work-dir /kaggle/working/g09_smoke
   ```
3. Save `EXP0000_SMOKE_g09_report.json` to flip **`G09 -> PASS`**.

### Step B — Launch `EXP0001` (`100` Epochs, `patience=20`)
1. Upload `08_Checkpoints/artifacts/EXP0001_REL0001_PP0001_bundle.zip` (`94.47 MB`), `07_Experiments/EXP0001/config.yaml` (rename or pass path), and `13_Automation/kaggle_train_exp.py`.
2. Run:
   ```bash
   pip install -q ultralytics==8.3.253
   python kaggle_train_exp.py \
     --config /kaggle/input/exp0001-config/config.yaml \
     --data-yaml /kaggle/input/exp0001-rel0001-pp0001-bundle/dataset.yaml \
     --work-dir /kaggle/working/EXP0001_run
   ```

---

## 2. Monitored Anomalies & Permitted Interventions (`STEP-028`)

| Condition | Permitted Action | Forbidden Action |
|---|---|---|
| Kaggle `12 h` timeout / preemption | Save `last.pt` + `results.csv`, re-launch with `--resume <backup_last.pt>`, record interruption in `observations.md` | Never reconstruct missing epochs or hide interruptions |
| `NaN`/`Inf` loss or CUDA OOM | Stop run, preserve failure logs, record in `observations.md`, open a **new** `EXP####` if `batch_size`/`lr0` must change | **Never** silently change `batch_size`, `seed`, or `lr0` under `EXP0001` |
| `val mAP@0.50` plateaus for `20` epochs | Automatic `patience=20` early stop (`StoppingReason: early_stop_patience_20`) | Never touch `test` or `external_test` during training |

---

## 3. Artifacts to Bring Back Before Closing Kaggle Session

1. **Git-safe metadata** (from `/kaggle/working/EXP0001_run/EXP0001_for_git/` -> commit into `07_Experiments/EXP0001/`):
   - `results.csv`
   - `args.yaml`
   - `EXP0001_effective_manifest.json`
2. **Off-Git binary weights** (save to Private Google Drive & local `08_Checkpoints/artifacts/EXP0001/`):
   - `weights/best.pt`
   - `weights/last.pt`
