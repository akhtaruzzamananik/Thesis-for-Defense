# T22 — Clean-Run Reproducibility Audit (`STEP-038` / `G14`)

| Metadata | Value |
|---|---|
| TemplateID | `T22` |
| template_version | `v1.0.0` |
| entity_id | `REPRO0001` |
| owner | Akhtaruzzaman Anik (`232-15-252`, Research & Prototype Lead) |
| date | `2026-11-21` |
| status | Complete (`G14 = PASS` for verified levels `R1`, `R2`, `R3A`, `R3B`; `R4` transparently marked `NOT_REEXECUTED`) |
| source_inputs | `12_Documentation/step038_reproducibility_audit.json`; `09_Evaluation/freeze_manifest.json`; `09_Evaluation/step032_execution_manifest.json`; commit `86546f1` |
| governing_section | `OS §8.2`, `§10`, `§13.2`; Blueprint `STEP-038` |
| sensitivity | Public (aggregate hashes, deltas, timing, and pass/fail audit only; zero private images/weights) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Evaluation Lead) |

---

## Environment/access

- **Audit Host:** `Windows 11`, `11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz` (`8` logical threads, `7.70 GiB RAM`), `Python 3.14.6`, `onnxruntime 1.32.0` (`CPUExecutionProvider`), `cv2 5.0.0`.
- **Clean-Checkout Isolation (`R3B`):** Exported committed `HEAD` (`86546f117646b4803a2f3d74b3ab9f162693b303`) via `git archive` into a brand-new temporary directory with `PYTHONPATH` stripped and **zero untracked or off-Git files present**, proving repository structure validation and unit/error-contract tests do not depend on hidden local developer state.
- **Access Limits:** Public datasets (`DS0001–DS0006`) remain off-Git under original source licenses (`DS0002` DENTEX isolated under `CC-BY-NC-SA-4.0`); binary weights (`.pt`, `.onnx`) and `.jsonl` predictions reside in private off-Git artifact storage (`tracked_forbidden_count = 0`).

## artifact retrieval

All `50` audited artifacts (`5` core governance/code files, `2` preprocessing YAMLs, `6` `SPLIT` manifests, `6` `REL` manifests, `10` `.pt` checkpoints, `14` `STEP-032` `predictions.jsonl` files, and `7` static `.onnx` exports) were retrieved from their versioned repository / off-Git paths and verified programmatically by [audit_step038_reproducibility.py](../13_Automation/audit_step038_reproducibility.py).

## checksums

- **`R1` Result:** **`50 / 50` SHA-256 checksums matched bit-for-bit (`0` mismatches)** against `09_Evaluation/freeze_manifest.json`, `09_Evaluation/EVAL0001..EVAL0014/run_manifest.json`, and `09_Evaluation/step032_execution_manifest.json`.
- Key immutable anchors confirmed intact: `classes.csv` (`c3f91dfc...`), `protocol.md` (`26fede09...`), `src/opg/evaluator.py` (`8fa2c6d8...`), `src/opg/preprocessing.py` (`011e67c0...`).

## exact commands

```bash
python 13_Automation/audit_step038_reproducibility.py
```
Inside `R3B` clean checkout (`git archive --format=tar HEAD` -> fresh temp dir, `PYTHONPATH` stripped):
```bash
python 13_Automation/validate_repo.py
python -m pytest -q tests/test_repo_checks.py tests/test_smoke_data_env.py \
    tests/test_annotation_schema.py tests/test_preprocessing.py tests/test_prototype_interface.py
```

## predicted agreement/tolerance

Predeclared prospective tolerances before running the audit (`step038_reproducibility_audit.json`):
1. **`R1` Checksums:** Exact bit-for-bit `SHA-256` match (`0` mismatches).
2. **`R2` Metric Replay:** `|ΔmAP@0.50| <= 1e-6`, `|ΔmAP@0.50:0.95| <= 1e-6`, `|ΔMacro-F1| <= 1e-6`, and exact `TP/FP/FN` integer counts.
3. **`R3A` ONNX CPU Self-Determinism:** `max_abs_diff == 0.0` across repeated runs on identical raw OPGs.
4. **`R3A` ONNX-CPU vs PyTorch-GPU (`STEP-032`) Parity:** `mean_box_iou >= 0.95` and `mean |Δscore| <= 0.02`.
5. **`R3B` Clean `git archive` Checkout:** `validate_repo.py` exit `0` and unit/error-contract `pytest` exit `0`.

## observed agreement

| Audit Level | Scope Tested | Prospective Tolerance | Observed Result | Outcome |
|---|---|---|---|---|
| **`R1`** | `50` governance, split, release, `.pt`, `.jsonl`, `.onnx` files | `0` SHA-256 mismatches | **`50/50` exact (`0` mismatches)** | **PASS** |
| **`R2`** | `EVAL0001` (`TrackA@1280`, `208` OPGs) | `<= 1e-6` + exact counts | `ΔmAP50 = 0.0`, `ΔmAP50-95 = 0.0`, `TP/FP/FN exact = True` | **PASS** |
| **`R2`** | `EVAL0011` (`TrackD@1280`, `578` OPGs) | `<= 1e-6` + exact counts | `ΔmAP50 = 0.0`, `ΔmAP50-95 = 0.0`, `TP/FP/FN exact = True` | **PASS** |
| **`R2`** | `EVAL0013` (`TrackE@640`, `133` OPGs) | `<= 1e-6` + exact counts | `ΔmAP50 = 0.0`, `ΔmAP50-95 = 0.0`, `TP/FP/FN exact = True` | **PASS** |
| **`R3A`** | `MODEL0008` (`20` raw `DS0005` test OPGs) | `self=0.0`, `IoU>=0.95`, `|Δs|<=0.02` | `self=0.0`, **`IoU = 0.99460`**, `|Δscore| = 0.00366` | **PASS** |
| **`R3A`** | `MODEL0005` (`10` raw `DS0001` test OPGs) | `self=0.0`, `IoU>=0.95`, `|Δs|<=0.02` | `self=0.0`, **`IoU = 0.99381`**, `|Δscore| = 0.00242` | **PASS** |
| **`R3A`** | `MODEL0013` (`10` raw `DS0004` test OPGs) | `self=0.0`, `IoU>=0.95`, `|Δs|<=0.02` | `self=0.0`, **`IoU = 0.99435`**, `|Δscore| = 0.00903` | **PASS** |
| **`R3B`** | Fresh `git archive` checkout (`86546f1`, `PYTHONPATH` stripped) | exit code `0` | `validate_repo OK`; **`15 passed, 2 skipped in 0.97s`** | **PASS** |

## timing context

Total wall-clock duration for the full `R1 + R2 + R3A + R3B` audit: **`32.23 s`** on local `Intel Core i5-1135G7` CPU (`MODEL0008` `170.9 ms/OPG`, `MODEL0005` `775.9 ms/OPG`, `MODEL0013` `824.5 ms/OPG`, consistent with `STEP-034` `timing_report.md`).

## discrepancies

- **Zero material discrepancies.**
- Small floating-point rounding deltas (`mean |Δscore| = 0.0024–0.0090`, `mean IoU = 0.9938–0.9946`) between Kaggle `Tesla T4` PyTorch (`STEP-032`) and local Windows 11 CPU `ONNXRuntime 1.32.0` (`R3A`) are expected cross-backend `FP32` kernel rounding + `JPEG-95` bundle vs original file decode differences and fall well inside the predeclared `IoU >= 0.95` / `|Δscore| <= 0.02` tolerances.
- In `R3B`, `2` tests in `test_prototype_interface.py` were cleanly skipped because off-Git `.onnx` binaries are intentionally excluded from Git (`@pytest.mark.skipif(not HAS_LOCAL_ONNX)`), while all `15` structural, schema, preprocessing, missing-model, license-isolation, and class-map hash-tamper tests executed and passed.

## reproduction level

- **Verified & Claimed (`G14 PASS`):** **`Level R1` (Bit-for-Bit Checksum Recovery), `Level R2` (Exact Deterministic Metric Replay, `Δ = 0.0`), and `Level R3` (Deterministic ONNX CPU Inference Replay & Clean `git archive` Checkout Verification).**
- **Explicitly NOT Claimed in `STEP-038`:** **`Level R4` (Full `13`-Experiment Kaggle `Tesla T4` GPU Retraining, ~`7.5` GPU-hours)** was not re-executed during `STEP-038`; full deterministic training recipes (`seed = 20261124`, `deterministic = true`, pinned `ultralytics==8.3.253`, `EXP0001–EXP0013/config.yaml`, `args.yaml`, `results.csv`) are archived for independent retraining on any CUDA GPU.
