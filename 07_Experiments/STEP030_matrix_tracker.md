# `STEP-030` Controlled Experiment Matrix Tracker & Kaggle Execution Guide

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-030` (`S11` — Execute the approved controlled experiment matrix) |
| Prerequisite | `G09 = PASS` (`Tesla T4`), `G10 = PASS` for `EXP0001` (`MODEL0001`, `val mAP@0.50 = 0.381`) |
| Weekly Kaggle GPU Budget | `30.0 h/week` (`EXP0001` used `0.47 h` / `28 min` on `Tesla T4`) |
| Sealed Test Guard | **All `13` experiments strictly use `["train", "val"]` ONLY (`test`/`external_test` sealed until `G11`)** |
| Last Updated | `2026-11-20` |

---

## 1. Full Matrix Status & Controlled Comparison Map (`EXP0001–EXP0013`)

| Priority | `EXP ID` | `RQ` | Model (`MC`) | Dataset / `PP` (`imgsz`, `BS`) | Matched Control | Kaggle Bundle (`.zip` off-Git) | `val mAP@0.50` | `val mAP@0.50:95` | `G10` Status |
|---|---|---|---|---|---|---|---:|---:|---|
| Done | **`EXP0001`** | `RQ0, RQ1` | `YOLO11s` | `REL0001` / `PP0001` (`640`, `16`) | Primary Anchor | `EXP0001_REL0001_PP0001_bundle.zip` (`94.47 MB`) | **`0.381`** | `0.1570` | **PASS** (`MODEL0001`) |
| **Wave 1** | **`EXP0002`** | `RQ1, RQ3` | **`YOLOv8s`** | `REL0001` / `PP0001` (`640`, `16`) | `EXP0001` | *Reuses `EXP0001` Kaggle dataset!* | **`0.364`** | `0.1523` | **PASS** (`MODEL0002`, `37` ep / `12.1m`) |
| **Wave 1** | **`EXP0013`** | `RQ1, RQ3` | **`YOLO11m`** | `REL0001` / `PP0001` (`640`, `16`) | `EXP0001` | *Reuses `EXP0001` Kaggle dataset!* | **`0.391`** | `0.1583` | **PASS** (`MODEL0003`, `62` ep / `41.7m`) |
| **Wave 1** | **`EXP0010`** | `RQ2, RQ3` | `YOLO11s` | `REL0001` / **`PP0004` (`1280`, `8`)** | `EXP0001` | `kaggle_bundles/REL0001_PP0004_bundle.zip` (`299.46 MB`) | **`0.391`** | **`0.1656`** | **PASS** (`MODEL0005`, `45` ep / `57.8m`) |
| **Wave 2** | **`EXP0003`** | `RQ0, RQ1` | `YOLO11s` | `REL0002` (`DENTEX`) / `PP0001` (`640`, `16`) | TrackB Baseline | `kaggle_bundles/REL0002_PP0001_bundle.zip` (`43.38 MB`) | **`0.444`** *(peak `0.459`)* | **`0.2913`** | **PASS** (`MODEL0004`, `52` ep / `8.9m`) |
| **Wave 2** | **`EXP0004`** | `RQ0, RQ1` | `YOLO11s` | `REL0003` (`Dhaka`) / `PP0001` (`640`, `16`) | TrackC Baseline | `kaggle_bundles/REL0003_PP0001_bundle.zip` (`18.41 MB`) | **`0.259`** *(ep 54: `0.266`)* | `0.1506` | **PASS** (`MODEL0006`, `54` ep / `3.4m`) |
| **Wave 2** | **`EXP0005`** | `RQ0, RQ1` | `YOLO11s` | `REL0004` (`Hanoi PAI`) / `PP0001` (`640`, `16`) | TrackD Baseline | `kaggle_bundles/REL0004_PP0001_bundle.zip` (`230.41 MB`) | `PENDING` | `PENDING` | `READY` |
| **Wave 2** | **`EXP0006`** | `RQ0, RQ1` | `YOLO11s` | `REL0005` (`UAE`) / `PP0001` (`640`, `16`) | TrackE Baseline | `kaggle_bundles/REL0005_PP0001_bundle.zip` (`37.41 MB`) | **`0.858`** *(peak `0.860`)* | **`0.5705`** | **PASS** (`MODEL0008`, `100` ep / `21.1m`) |
| **Wave 2** | **`EXP0007`** | `RQ0, RQ1` | `YOLO11s` | `REL0006` (`Pediatric`) / `PP0001` (`640`, `16`) | TrackF Baseline | `kaggle_bundles/REL0006_PP0001_bundle.zip` (`10.07 MB`) | **`0.100`** | `0.0300` | **PASS** (`MODEL0007`, `56` ep / `2.6m`) |
| **Wave 3** | **`EXP0008`** | `RQ2` | `YOLO11s` | `REL0001` / **`PP0002` (`CLAHE 2.0`)** | `EXP0001` | `kaggle_bundles/REL0001_PP0002_bundle.zip` (`121.17 MB`) | `PENDING` | `PENDING` | `READY` |
| **Wave 3** | **`EXP0009`** | `RQ2` | `YOLO11s` | `REL0001` / **`PP0003` (`CLAHE 3.0`)** | `EXP0001` | `kaggle_bundles/REL0001_PP0003_bundle.zip` (`136.73 MB`) | `PENDING` | `PENDING` | `READY` |
| **Wave 3** | **`EXP0011`** | `RQ2, RQ3` | `YOLO11s` | `REL0004` / **`PP0004` (`1280`, `8`)** | `EXP0005` | `kaggle_bundles/REL0004_PP0004_bundle.zip` (`709.71 MB`) | `PENDING` | `PENDING` | `READY` |
| **Wave 3** | **`EXP0012`** | `RQ2` | `YOLO11s` | `REL0003` / **`PP0002` (`CLAHE 2.0`)** | `EXP0004` | `kaggle_bundles/REL0003_PP0002_bundle.zip` (`21.50 MB`) | `PENDING` | `PENDING` | `READY` |

---

## 2. Universal Kaggle Run Template (Just Change `EXP_ID`!)

On Kaggle GPU (`T4 x2` or `P100`, `Internet: ON`, attach **ONLY** the matching dataset bundle for `EXP_ID`):

**Cell 1:**
```python
!pip install -q ultralytics==8.3.253
!rm -rf /kaggle/working/Thesis-for-Defense
!git clone https://github.com/akhtaruzzamananik/Thesis-for-Defense.git /kaggle/working/Thesis-for-Defense
```

**Cell 2:**
```python
import glob, subprocess, sys

EXP_ID = "EXP0002"  # <-- Change ONLY this ID (EXP0002..EXP0013)
yamls = glob.glob("/kaggle/input/**/dataset.yaml", recursive=True)
print("Found dataset.yaml:", yamls)
assert len(yamls) == 1, f"Attach ONLY 1 dataset bundle! Found: {yamls}"

subprocess.run([
    sys.executable,
    "/kaggle/working/Thesis-for-Defense/13_Automation/kaggle_train_exp.py",
    "--config", f"/kaggle/working/Thesis-for-Defense/07_Experiments/{EXP_ID}/config.yaml",
    "--data-yaml", yamls[0],
    "--work-dir", f"/kaggle/working/{EXP_ID}_run",
], check=True)
```

---

## 3. One-Command Local Ingestion & `G10` Audit

After clicking **Output `⋮` -> Download output** on Kaggle, run locally:
```bash
python 13_Automation/ingest_kaggle_exp.py --exp-id EXP0002 --source "D:\Downloads\results.zip"
```
