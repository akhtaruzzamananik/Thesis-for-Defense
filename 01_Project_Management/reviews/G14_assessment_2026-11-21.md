# Gate G14 Assessment — Prototype Integrity & Clean-Run Reproducibility (`STEP-038`)

| Field | Value |
|---|---|
| Gate ID | `G14` (`GA0014`) |
| Step / Stage | `STEP-038` (`S13` — Perform a clean-environment reproducibility audit) |
| Entity Versions Assessed | `OPGPrototypeEngine v1.0.0` (`src/opg/inference_prototype.py`), `run_opg_inference.py`, `DEC0018`, `prototype_guide.md`, `reproduce.md`, `reproducibility_audit.md` (`REPRO0001 v1.0.0`) |
| Outcome | **`PASS` (`2026-11-21`)** |
| Assessors | Akhtaruzzaman Anik (`232-15-252`, Research & Prototype Lead) & Mahajub Al Shabah (`232-15-900`, Evaluation Lead) |
| Audit Evidence | [step038_reproducibility_audit.json](../../12_Documentation/step038_reproducibility_audit.json) & [reproducibility_audit.md](../../12_Documentation/reproducibility_audit.md) |

---

## 1. Mandatory `G14` Criteria Audit (`STEP-037–038` / `OS §8`, `§10`, `§13.2`)

| Criterion | Result | Observed Verification |
|---|---|---|
| **1. Prototype stability, single inference path & safety contract (`STEP-037`)** | **PASS** | `OPGPrototypeEngine` reuses frozen `src/opg/preprocessing.py` verbatim, enforces startup SHA-256 checks (`classes.csv`, `PP`, `.onnx`), maps boxes to original source pixels, isolates `CC-BY-NC-SA` `MODEL0004`, distinguishes `OK` / `ZERO_DETECTIONS` / `ERROR`, and embeds mandatory non-clinical disclaimers (`test_prototype_interface.py` `4/4` passing). |
| **2. Artifact checksum recovery (`Level R1`)** | **PASS** | **`50 / 50` SHA-256 digests** (`29` freeze + `14` `predictions.jsonl` + `7` `.onnx`) matched bit-for-bit (`0` mismatches). |
| **3. Exact deterministic metric replay (`Level R2`)** | **PASS** | `EVAL0001` (`TrackA`), `EVAL0011` (`TrackD`), and `EVAL0013` (`TrackE`) replayed via frozen `src/opg/evaluator.py` with **`ΔmAP@0.50 = 0.0`**, **`ΔmAP@0.50:0.95 = 0.0`**, and **`TP/FP/FN exact = True`**. |
| **4. Clean inference replay & fresh checkout isolation (`Level R3A/R3B`)** | **PASS** | `40` raw held-out OPGs replayed via CPU `ONNXRuntime` achieved **`self_diff = 0.0`** and **`IoU = 0.9938–0.9946`** (`|Δscore| = 0.0024–0.0090`) vs Kaggle PyTorch GPU; fresh `git archive` checkout (`86546f1`, `PYTHONPATH` stripped, zero off-Git files) passed `validate_repo.py` and `15 passed, 2 skipped in 0.97s`. |
| **5. Honest disclosure of verified reproduction level** | **PASS** | Explicitly certifies **`R1–R3 PASS`** and transparently discloses that **`R4` (full `13`-EXP GPU retraining)** was not re-executed in `STEP-038` (full deterministic training recipes archived). |

---

## 2. Decision & Next Step

- **`G14` Outcome:** **`PASS` (`2026-11-21`)** — Stage **`S13` (Research Prototype & Clean-Environment Reproducibility)** is 100% COMPLETE (`14/17` gates passed!).
- **Unlocks:** **`S14` (`STEP-039`–`STEP-044`)** (*Publication Figures/Tables, Full Thesis Manuscript & Defense Writing -> `G15`*) and parallel **`S16` (`STEP-047`–`STEP-049`)** (*Live Hosted Web Showcase -> `G17`*).
