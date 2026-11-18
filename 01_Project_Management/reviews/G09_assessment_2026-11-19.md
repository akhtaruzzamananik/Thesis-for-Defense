# Gate G09 Assessment — Baseline Execution & Checkpoint Recovery Readiness (`STEP-026`)

| Field | Value |
|---|---|
| Gate ID | `G09` (`GA0009`) |
| Step / Stage | `STEP-026` (`S10` — Verify checkpoint recovery and baseline readiness) |
| Outcome | **`PENDING_KAGGLE_SMOKE`** *(Local readiness verified; Kaggle GPU execution & human sign-off pending)* |
| Assessors | Mahajub Al Shabah (`232-15-900`, Model & Eval Lead) & Akhtaruzzaman Anik (`232-15-252`, Research Lead) |
| Date | `2026-11-19` |

---

## 1. Local Readiness Verification (Completed & Observed)

| Check | Result | Evidence |
|---|---|---|
| Checkpoint & recovery policy | **PASS** | [checkpoint_policy.md](../../08_Checkpoints/checkpoint_policy.md) defines `last`/`best`/`smoke`/`exported_onnx` roles, immutable naming, off-Git binary boundary, and honest `ultralytics==8.3.253` exact-resume limitations. |
| Diagnostic `T14` config validation | **PASS** | `python 13_Automation/run_pipeline.py validate-config --config 07_Experiments/configs/EXP0000_SMOKE.yaml` -> `CONFIG_VALID: EXP0000_SMOKE` (`allowed_partitions: ["train", "val"]`, `test` blocked). |
| Kaggle `EXP0000_SMOKE` bundle export | **PASS** | Built via `run_pipeline.py build-kaggle-bundle` (`DS0001` / `SPLIT0001` / `ANNB0001` / `TrackA` / `PP0001`, `--max-items-per-partition 32`): `32` train + `32` val images, `nc=13`, `877` boxes, `0` invalid boxes, `0` `test` entries, zipped to `08_Checkpoints/artifacts/EXP0000_SMOKE_bundle.zip` (`5.14 MB`, off-Git). |
| Kaggle GPU recovery script | **READY** | [kaggle_smoke_g09.py](../../13_Automation/kaggle_smoke_g09.py) tests `1`-epoch interrupt -> backup SHA-256 verification -> `resume=True` restore to epoch `2` -> finite `val` `mAP@0.50` / `mAP@0.50:0.95` + `FPS_e2e`. |
| Repo & unit tests | **PASS** | `validate_repo.py` + `pytest` (`22 passed`) verified in `STEP-025`/`026`. |

---

## 2. Pending Kaggle GPU Evidence Required to Flip `G09` -> `PASS`

Because `torch` / `ultralytics` GPU execution runs on **Kaggle GPU** (`DEC0011`), `G09` cannot be marked `PASS` until the user executes [kaggle_smoke_g09.py](../../13_Automation/kaggle_smoke_g09.py) on Kaggle with `EXP0000_SMOKE_bundle.zip` and returns `EXP0000_SMOKE_g09_report.json` confirming:
1. `phase1_has_optimizer_state == true` and `phase1_has_ema_state == true`;
2. `backup_hash_match == true` (`last.pt` SHA-256 == backup retrieval SHA-256);
3. `phase2_resumed_final_epoch_field == 1` (`0`-indexed epoch `2/2` completed after `resume=True`);
4. Finite `val_map50_finite` and `val_map50_95_finite` and `smoke_e2e_fps_5imgs > 0`;
5. Researcher / Supervisor acceptance of `G09` (including honest limited exact-resume policy).
