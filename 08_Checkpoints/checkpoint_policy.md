# Checkpoint Policy, State Capture & Recovery Protocol (`STEP-026` / `G09`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-026` (`S10` — Verify checkpoint recovery and baseline readiness) |
| Record | `08_Checkpoints/checkpoint_policy.md` (`v1.0.0`) |
| Owner | Mahajub Al Shabah (`232-15-900`, Model & Evaluation Lead) |
| Co-Reviewer | Akhtaruzzaman Anik (`232-15-252`, Research Lead) & Ms Faiza Feroz (`Supervisor`) |
| Date | `2026-11-19` |
| Governing Sections | `OS §5.4`, `§7.1`, `§10.2`, `§13.3`; Blueprint `STEP-026`; `DEC0011`, `DEC0012` |

---

## 1. Checkpoint Roles & Immutable Naming

Every training run (`EXP####` / `RUN####`) assigns explicit roles registered in [checkpoint_registry.csv](checkpoint_registry.csv):

| Role | Trigger / Meaning | Reportable? | Retention |
|---|---|---|---|
| `last` | Saved at the end of every epoch (`last.pt`) for interruption recovery | No (recovery only) | Overwritten per epoch during active run; latest epoch backed up at session end |
| `best` | Saved when validation `mAP@0.50` improves (`best.pt`) | **Yes** (primary selection checkpoint per `DEC0012`) | Retained permanently in off-Git artifact tier (`08_Checkpoints/artifacts/<EXP_ID>/`) + backup |
| `smoke` | Diagnostic `EXP0000_SMOKE` checkpoint used solely for `G09` recovery verification | **Never reportable** | Retained off-Git as `G09` audit evidence |
| `exported_onnx` | `FP32` ONNX export from `best.pt` for local CPU deployment (`S16`) | Inference artifact | Retained off-Git + SHA-256 recorded in `08_Checkpoints/manifests/` |

- **Immutable Backup Naming:** `<EXP_ID>_<RUN_ID>_epoch<NNN>_<role>.pt` (e.g., `EXP0001_RUN0001_epoch042_best.pt`).
- **Git Boundary:** Binary weights (`.pt`, `.pth`, `.onnx`, `.engine`, `.safetensors`) are **strictly forbidden in Git** (`.gitignore`). Only `08_Checkpoints/checkpoint_registry.csv`, `08_Checkpoints/manifests/*.json` (SHA-256 + byte size + state inventory), and `<EXP>_effective_config.json` are tracked in Git.

---

## 2. State Capture & Honest Exact-Resume Limitations (`ultralytics==8.3.253`)

1. **What `ultralytics` `last.pt` actually stores:**
   - `model` state dict (`FP16`/`FP32`), `ema` shadow weights, `optimizer` (`AdamW`) state dict, `epoch` index (`last_finished_epoch`), `best_fitness`, `train_args`, and `updates`.
   - **Companion metadata required outside `.pt`:** `<EXP>_effective_config.json` (`source_commit`, resolved `data.yaml`, `hardware_record`, `initial_weights_sha256`), `results.csv`, and SHA-256 checksums.
2. **Honest Exact-Resume Limitation (No Mislabeling):**
   - Calling `YOLO(backup_last_pt).train(resume=True)` restores **epoch counter, model/EMA weights, and optimizer state**, resuming cleanly from `epoch + 1` up to `epochs`.
   - However, because `ultralytics` does **not** serialize Python/PyTorch DataLoader worker RNG states or exact CUDA `amp=True` non-deterministic kernel schedules, a resumed run is **functionally continuous** (not bit-for-bit identical to an uninterrupted run).
   - **Rule:** Weights-only files (or stripped `best.pt` without optimizer/epoch state) must **never** be labeled as `exact_resume`; they are `warm_start` / `eval_only`.

---

## 3. Ephemeral Kaggle Storage & Off-Platform Backup Rule

1. **Ephemeral Compute Warning:** Kaggle `/kaggle/working/` is cleared when a session expires or resets (`12 h` max session / `30 h/week` GPU quota).
2. **Mandatory Backup Procedure:**
   - At the end of every Kaggle session (or interruption point), copy `weights/last.pt`, `weights/best.pt`, `results.csv`, and `<EXP>_effective_config.json` to persistent backup storage (Kaggle Dataset output version and/or private Google Drive / local `08_Checkpoints/artifacts/<EXP_ID>/`).
   - Compute and record `SHA-256` before and after retrieval (`hashlib.sha256`). Any hash mismatch invalidates the restore and triggers re-transfer from backup.
   - Register every retained checkpoint (`CKPT####`) in `08_Checkpoints/checkpoint_registry.csv` before closing the run.
