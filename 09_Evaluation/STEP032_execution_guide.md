# `STEP-032` Sealed Final-Test Execution Guide (Single Kaggle GPU Run)

| Field | Value |
|---|---|
| Step / Prerequisite | `STEP-032` (`G11 = PASS`, `FREEZE0001` committed at `6282385`) |
| Off-Git Kaggle Bundle | `08_Checkpoints/artifacts/kaggle_bundles/STEP032_SEALED_TEST_BUNDLE.zip` |
| Scope | All `14` held-out runs (`EVAL0001–EVAL0014`), `10` unique `HC01–HC05` zero-shot cross-country passes, `10` `UD14` GPU `BS=1` timing benchmarks, and `7` static `ONNX` (`opset=17`) exports |
| Blind Inference Guard | Zero ground-truth labels inside bundle; every weight & protocol hash verified bit-for-bit against `09_Evaluation/freeze_manifest.json` |

---

## 1. Upload Bundle to Kaggle Dataset

1. Go to Kaggle -> **Datasets -> New Dataset**.
2. Upload **`e:\Thesis Phase 1\08_Checkpoints\artifacts\kaggle_bundles\STEP032_SEALED_TEST_BUNDLE.zip`** as a **Private** dataset (e.g., `opg-step032-sealed-test`).
3. Create a Kaggle Notebook with **Accelerator: GPU T4 x2 (or P100)**, **Internet: ON**, and attach **ONLY** that dataset.

---

## 2. Two-Cell Execution on Kaggle (`~5–8` min total)

**Cell 1:**
```python
!pip install -q ultralytics==8.3.253 onnx onnxscript
!rm -rf /kaggle/working/Thesis-for-Defense /kaggle/working/STEP032_outputs
!git clone https://github.com/akhtaruzzamananik/Thesis-for-Defense.git /kaggle/working/Thesis-for-Defense
```

**Cell 2:**
```python
import glob, subprocess, sys
from pathlib import Path

idxs = glob.glob("/kaggle/input/**/bundle_index.json", recursive=True)
print("Found bundle_index.json:", idxs)
assert len(idxs) == 1, f"Attach ONLY the STEP032 bundle! Found: {idxs}"
bundle_dir = str(Path(idxs[0]).parent)

subprocess.run([
    sys.executable,
    "/kaggle/working/Thesis-for-Defense/13_Automation/kaggle_eval_step032.py",
    "--repo-root", "/kaggle/working/Thesis-for-Defense",
    "--bundle-dir", bundle_dir,
    "--work-dir", "/kaggle/working/STEP032_outputs",
], check=True)
```

---

## 3. Download Output & Run One-Command Local Ingestion

1. After Cell 2 prints `[ALL DONE] STEP-032 complete! Total errors=0`, click **Output `⋮` -> Download output** (`STEP032_outputs` zip).
2. Locally run:
```bash
python 13_Automation/ingest_step032_results.py --source "D:\Downloads\results.zip"
```
(Replace with your downloaded zip path — or just tell Antigravity `"step 32 downloaded"`!)
