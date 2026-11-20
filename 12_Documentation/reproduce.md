# Independent Reproduction Guide (`STEP-038` / `G14`)

| Metadata | Value |
|---|---|
| Step / Gate | `STEP-038` (`S13` — Clean-Environment Reproducibility Audit; `G14 = PASS`) |
| Verified Commit | `86546f117646b4803a2f3d74b3ab9f162693b303` (`main`) |
| Audit Evidence | [reproducibility_audit.md](./reproducibility_audit.md) · [step038_reproducibility_audit.json](./step038_reproducibility_audit.json) |
| Owners | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |

---

## 1. Reproduction Levels & Honest Scope (`OS §8.2`)

| Level | Scope | Verified in `STEP-038`? | Expected Runtime & Hardware |
|---|---|---|---:|
| **`R1` (Checksum Recovery)** | Verify all `50/50` SHA-256 digests (`29` freeze + `14` `predictions.jsonl` + `7` `.onnx`) | **VERIFIED (`PASS`)** | `~2 s` (CPU) |
| **`R2` (Metric Replay)** | Recompute held-out `mAP@0.50`, `mAP@0.50:0.95`, `P/R/F1`, `TP/FP/FN` from saved predictions & GT | **VERIFIED (`PASS`, `Δ = 0.0`)** | `~15 s` (CPU) |
| **`R3` (Clean Inference & Clean-Repo Replay)** | Run `OPGPrototypeEngine` (`ONNXRuntime` CPU) on raw held-out OPGs + clean `git archive` tests | **VERIFIED (`PASS`, `self_diff = 0.0`, `IoU >= 0.9938`)** | `~30 s` (CPU) |
| **`R4` (Full `13`-EXP GPU Retraining)** | Re-train `EXP0001–EXP0013` from scratch on Kaggle `Tesla T4` (`seed = 20261124`) | **NOT RE-EXECUTED** *(locked recipe archived)* | `~7.5 hr` (`Tesla T4`) |

---

## 2. Step-by-Step Clean-Environment Setup

### 2.1 Clone Repository & Create Clean Virtual Environment
```bash
git clone https://github.com/akhtaruzzamananik/Thesis-for-Defense.git
cd Thesis-for-Defense
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS:        source .venv/bin/activate
pip install -r environment/data/requirements-data.txt
pip install onnxruntime pytest
```

### 2.2 Verify Repository Structure & Unit Tests (No Off-Git Data Needed)
```bash
python 13_Automation/validate_repo.py
python -m pytest -q tests/test_repo_checks.py tests/test_smoke_data_env.py \
    tests/test_annotation_schema.py tests/test_preprocessing.py tests/test_prototype_interface.py
```

---

## 3. Authorized Off-Git Artifact Retrieval

Raw radiographs (`DS0001–DS0006`), trained weights (`EXP0001–EXP0013/weights/best.pt`), raw prediction logs (`STEP032_outputs/evals/*/predictions.jsonl`), and exported `.onnx` models are strictly excluded from Git (`tracked_forbidden_count = 0`). To run `R1–R3` in full:

1. **Public Source Cohorts (`DS0001–DS0006`):** Obtain directly from the verified primary sources recorded in `03_Datasets/dataset_registry.csv` & `03_Datasets/access_decision.md` under each dataset's original license (`CC-BY-4.0` for `DS0001/0003/0004/0005/0006`; `CC-BY-NC-SA-4.0` non-commercial isolated for `DS0002` DENTEX) and place extracted files under `03_Datasets/raw/DS000X/extracted/`.
2. **Trained Checkpoints, `STEP-032` Predictions & `ONNX` Exports:** Restore from the Private Project Archive (`DEC0011` / `DEC0020`) into:
   - `08_Checkpoints/artifacts/EXP0001..EXP0013/weights/{best.pt, last.pt}`
   - `08_Checkpoints/artifacts/STEP032_outputs/{evals, xshift, timing, onnx}`

---

## 4. Exact Reproduction Commands (`R1–R4`)

### 4.1 Run Full Clean Audit (`R1` Checksums + `R2` Metric Replay + `R3` ONNX Replay & Clean Checkout)
```bash
python 13_Automation/audit_step038_reproducibility.py
```

### 4.2 Recompute All `14` Held-Out Evaluations + `1,000`-Resample `GroupID` `95% CI` + `12` `HC01–HC05` Shift Bridges
```bash
python 13_Automation/compute_step033_metrics.py
python 13_Automation/audit_step035_g12.py
```

### 4.3 Re-run Local CPU `ONNXRuntime` Timing (`UD14`) & Error Taxonomy (`T19`)
```bash
python 13_Automation/benchmark_step034_cpu_onnx.py
python 13_Automation/analyze_step036_errors.py
```

### 4.4 Run Single-Image Research Inference Prototype (`STEP-037`)
```bash
python 13_Automation/run_opg_inference.py \
    --model-id MODEL0008 \
    --input "path/to/deidentified_opg.jpg" \
    --out-json "out.json" \
    --out-overlay "out_overlay.jpg"
```

### 4.5 Full GPU Retraining (`R4` Recipe on Kaggle `Tesla T4`, `ultralytics==8.3.253`)
See `07_Experiments/STEP030_matrix_tracker.md` for the exact 2-cell Kaggle runner invoking `13_Automation/kaggle_train_exp.py` with locked `07_Experiments/EXP0001..EXP0013/config.yaml` (`seed = 20261124`, `deterministic = true`), followed by `09_Evaluation/STEP032_execution_guide.md` for single-pass sealed test inference.
