# Pipeline architecture, data lineage, and storage policy

> Governing authority: [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md) (`OS §2.3`, `OS §10.2`). This document summarizes the repository's operational storage and lineage contract; it does not replace or alter handbook policy.

## 1. End-to-end data lineage

```text
source → DS version → ANN version → SPLIT → PP → REL → EXP → CKPT/MODEL → EVAL → FIG/TAB → CLAIM → WR → ARCH / DEPLOY
```

- Deterministic viewing/annotation preparation may precede `SPLIT`, with coordinate mappings preserved.
- Fitted normalization/preprocessing and stochastic augmentation happen **only after** `SPLIT` is locked (`OS §4.3`).
- `EVAL` runs on the frozen `MODEL` (`G11` selection on validation only).
- `web/` imports the `STEP-037` inference entry point unchanged and verifies the registered `MODEL` hash at startup (`OS §8.3`).

## 2. Storage tiers (`UD11` — STEP-002 locked in `DEC0011`)

Because `https://github.com/akhtaruzzamananik/Thesis-for-Defense` is **public** (confirmed 2026-11-16), strict tier separation is mandatory:

| Tier | Where it lives | Allowed contents |
|---|---|---|
| **Source (Public Git)** | GitHub (`main`) | Code (`src/opg/`, `web/`), tests, docs, planning records, non-sensitive CSV registries, configs, safe figure/table specs |
| **Restricted data (Off-Git)** | **Local PC** (`03_Datasets/raw/`, active) + **Private Google Drive** (restricted to Anik & Mahajub only, backup/sync) | Raw OPG images (`03_Datasets/raw/`), native/exported annotations (`04_Annotations/native/`, `exports/`), processed images (`05_Preprocessing/processed/`), patient/group linkage keys |
| **Research artifacts (Off-Git)** | **Local PC** (active) + **Private Google Drive** (restricted to Anik & Mahajub only, backup/sync) | Model checkpoints/weights (`.pt`, `.onnx`, `08_Checkpoints/artifacts/`), raw test predictions, private error-review visuals |
| **Release / archive** | `15_Archive/` + approved tier | Immutable snapshots, checksums, submission receipts, `DEPLOY` records (public subset only after license/privacy check) |

## 3. Pre-commit and pre-push checks

- Never commit raw images, linkage keys, weights, `.env`, or `.venv/`.
- Inspect `git status` and `git diff --cached` before every push.
- Record SHA-256 checksums for every external dataset, release, checkpoint, and exported model in the corresponding CSV registry.

## 4. Pipeline Entry Commands (`STEP-025`)

All pipeline logic resides in `src/opg/`; `13_Automation/run_pipeline.py` provides thin CLI entry points:

```powershell
# 1. Validate a resolved T14 experiment YAML (rejects nulls, hash drift, or test access before G11)
python 13_Automation/run_pipeline.py validate-config --config 07_Experiments/EXP0001/config.yaml

# 2. Export a Kaggle-ready PP####-prepared train/val YOLO bundle (test sealed until G11)
python 13_Automation/run_pipeline.py build-kaggle-bundle `
  --dataset-id DS0001 --split-id SPLIT0001 --batch-id ANNB0001 --track-id TrackA `
  --pp-config 05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml `
  --out-dir 05_Preprocessing/processed/kaggle_bundles/REL0001_PP0001

# 3. Launch registered training (Kaggle GPU or authorized runtime)
python 13_Automation/run_pipeline.py train `
  --config 07_Experiments/EXP0001/config.yaml `
  --data-yaml /kaggle/input/rel0001-pp0001/dataset.yaml `
  --out-dir /kaggle/working/runs
```
