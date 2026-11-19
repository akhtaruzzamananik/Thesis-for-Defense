# Gate G09 Assessment — Baseline Execution & Checkpoint Recovery Readiness (`STEP-026`)

| Field | Value |
|---|---|
| Gate ID | `G09` (`GA0009`) |
| Step / Stage | `STEP-026` (`S10` — Verify checkpoint recovery and baseline readiness) |
| Outcome | **`PASS`** (`2026-11-19`) |
| Assessors | Akhtaruzzaman Anik (`232-15-252`, Research Lead) & Mahajub Al Shabah (`232-15-900`, Model & Eval Lead) |
| Kaggle Runtime Observed | `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`) |
| Evidence Manifest | [EXP0000_SMOKE_g09_report.json](../../08_Checkpoints/manifests/EXP0000_SMOKE_g09_report.json) |
| Date | `2026-11-19` |

---

## 1. Gate Criteria Verification (All Observed & Passed)

| Mandatory Criterion (`STEP-026` / `OS §13.2`) | Result | Observed Evidence |
|---|---|---|
| **1. Checkpoint policy & honest exact-resume disclosure** | **PASS** | [checkpoint_policy.md](../../08_Checkpoints/checkpoint_policy.md) defines `last`/`best`/`smoke`/`exported_onnx`, immutable naming, off-Git weights boundary, and honest limited exact-resume note (`Restores epoch, model, EMA, and AdamW optimizer state; dataloader RNG is not bit-identical`). |
| **2. Diagnostic `T14` config & leak-free `train/val` bundle** | **PASS** | `EXP0000_SMOKE.yaml` (`CONFIG_VALID`), `32 train + 32 val` (`REL0001` / `PP0001`, `nc=13`, `877` boxes, `0` invalid, `0` `test` entries). |
| **3. Observed interruption & state capture (`epoch 1`)** | **PASS** | `phase1_interrupted_cleanly: true`, `phase1_epoch1_saved_epoch_field: 0`, `phase1_has_optimizer_state: true`, `phase1_has_ema_state: true` on Kaggle `Tesla T4`. |
| **4. Backup copy & retrieval SHA-256 verification** | **PASS** | `phase1_last_pt_sha256 == backup_retrieval_sha256 == 3f4452be644c1e8abcc2fb715d36aa01e83eeae50c635a64cd9e170472661aa4` (`backup_hash_match: true`). |
| **5. Checkpoint restore (`resume=True`) & completion (`epoch 2`)** | **PASS** | Resumed cleanly from backup checkpoint to complete epoch `2/2` (`phase2_completed_epochs_in_results_csv: 2`, `best_pt_sha256: a53dab45a8507162d82095bf6f55ce08eb68a991785eda478ac24ca485d7c756`). |
| **6. Finite validation & timing instrumentation** | **PASS** | `val_map50_finite: 0.0`, `val_map50_95_finite: 0.0` (expected after `2` smoke epochs on `32` images), `smoke_e2e_fps_5imgs: 19.51` (`Tesla T4`), `0` sealed `test` data accessed. |

---

## 2. Decision & Authorization

- **`G09` Outcome:** **`PASS` (`2026-11-19`)**.
- **Unlocks:** Stage **`S11` (`STEP-028` full Kaggle GPU training for `EXP0001`)**.
- **Diagnostic Boundary:** `EXP0000_SMOKE` (`CKPT0001`, `CKPT0002`) is strictly diagnostic and **never reportable** in thesis tables.
