# Evaluation, Matching, NMS, Timing & Optional-Analysis Protocol (`STEP-024` / `UD13–UD15`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-024` (`S10` — Approve baseline, experiment and evaluation plans) |
| Record | `09_Evaluation/protocol.md` (`v1.0.0`, freezes at `G11 / STEP-031`) |
| Owner | Mahajub Al Shabah (`232-15-900`, Evaluation Lead) |
| Co-Reviewer & Approver | Akhtaruzzaman Anik (`232-15-252`, Research Lead) & Ms Faiza Feroz (`Supervisor`) |
| Date | `2026-11-19` |
| Governing Sections | `OS §7.1–7.4`, `§13.2`; Blueprint `STEP-024`; `DEC0013–DEC0015` |

---

## 1. Detection Matching, AP & NMS Protocol (`UD13` / `DEC0013`)

Every `EVAL####` run evaluates predictions in **authoritative source radiograph pixel coordinates** (after applying `TransformLedger` inverse mapping from `640×640` / `1280×1280` back to original `W × H`), using a deterministic evaluator (`src/opg/evaluator.py`, implemented in `STEP-025`):

1. **Strict Distinction Between NMS IoU and Matching IoU (`OS §7.2`):**
   - **Class-Aware NMS (`agnostic_nms = false`):** `nms_iou = 0.65`, `max_det = 300`. Class-agnostic NMS is **prohibited** because dental pathologies (e.g., `Crown`, `Endodontic treatment`, and `Apical periodontitis`) validly co-exist and overlap on the same tooth (`annotation_protocol_v1.0.0.md`).
   - **Primary Matching IoU (`mAP@0.50`, `RF12`):** `matching_iou = 0.50` using class-aware, confidence-descending **one-to-one greedy matching** (`1` prediction matches at most `1` ground-truth box; duplicate predictions are counted as `FP`, never multiple `TP`).
   - **Strict Localization Complement (`UD15`):** `mAP@0.50:0.95` averaged uniformly over `10` thresholds $\{0.50, 0.55, \dots, 0.95\}$.
2. **Score Floor vs Frozen Deployment Operating Point (`OS §7.2`):**
   - **PR Curve & AP Score Floor:** Retain all predictions down to `metric_conf_floor = 0.001` so full precision-recall curves (`101`-point / all-point continuous trapezoidal integration) are never truncated!
   - **Operating-Point Confidence Threshold (`P`, `R`, `F1`):** Selected **exclusively on the `validation` partition** by maximizing macro-averaged `F1` across active classes (with `0.25` as fallback baseline reference), then **frozen at `G11` (`STEP-031`)** before touching `test` or `external_test`.
3. **Empty Images, Undefined Denominators & Absent-Class Rules (`OS §7.1–7.2`):**
   - **Reviewed-Empty Images (`reviewed_empty`, e.g., `27` OPGs in `DS0002`):** Always retained in image-level evaluation coverage denominators; any predicted box on an empty image counts as `FP`.
   - **Zero-Denominator Rule:** If `TP + FP == 0`, `Precision = N/A`; if `TP + FN == 0`, `Recall = N/A` (never silently set to `1.0` or `0.0`).
   - **Absent Ground-Truth Class Rule:** If a class has `0` ground-truth objects in an evaluated split (`TP + FN == 0`), it is **excluded from `mAP` averaging** for that split, and the exact eligible class count `C_eligible / C_total` is reported explicitly.
   - **Track C (`DS0003`) Dual Reporting:** Report both `5-class pathology (0..4)` and `6-class (0..5)` metrics; flag `Fractured Teeth` (`2` val / `2` test boxes) with explicit support denominators.

---

## 2. Inference Speed & End-to-End Timing Protocol (`UD14` / `DEC0014`)

Per `OS §7.3` and `RQ3`, **no invented minimum `FPS` target is assumed**. Timing is measured separately on **(a) Kaggle GPU (`T4`/`P100`)** and **(b) Local PC CPU (`Windows 11 Pro`, `ONNXRuntime`)**:

1. **Workload & Warm-up:**
   - Serial single-image streaming (`batch_size = 1`, `FP32` standard; `FP16` labeled separately if measured on GPU).
   - **`10` warm-up OPGs** executed and discarded before timing; timed across **`100` consecutive OPGs** (or full `test` set if `< 100`, e.g., `33` in `DS0003` and `24` in `DS0006`).
   - GPU timers call `torch.cuda.synchronize()` immediately before start and stop timestamps.
2. **Explicit Timing Boundaries (`Cold-Start Load & Disk I/O Excluded and Logged Separately`):**
   - **Model-Only Forward Pass (`T_infer`, `FPS_infer`):** Tensor forward pass only (`FPS_infer = N / sum(T_infer)`).
   - **End-to-End Image-to-Box Latency (`T_e2e`, `FPS_e2e`):** `T_preprocess (decode/RGB/autocrop/CLAHE/letterbox) + T_host_to_device + T_infer + T_postprocess (NMS + inverse TransformLedger)`, reporting `mean ± sd`, `median`, `IQR`, `p95` (`ms/OPG`), and `FPS_e2e = N / sum(T_e2e)`.

---

## 3. Optional Analyses Disposition (`UD15` / `DEC0015`)

| Candidate Analysis (`OS §7.4`) | Disposition | Explicit Scientific / Resource Rationale |
|---|---|---|
| **`mAP@0.50:0.95` & Per-Class `AP/P/R/F1`** | **ADOPTED** | Directly resolves `GAP0001`/`GAP0002` (`84.9%` of YOLO literature omits `mAP50-95`, `P0027`). |
| **PR Curves & Class-Aware Error Taxonomy (`T19`)** | **ADOPTED** | Quantifies precision-recall tradeoffs and radiographic mimics/small-lesion misses (`RQ3`). |
| **Controlled `PP0001–PP0004` (`CLAHE` & `1280px`) Ablations** | **ADOPTED** | Core falsifiable test of `RQ2` (`GAP0005`) under matched `SPLIT` & seed. |
| **External `DS0001 external_test` & `HC01–HC05` Shift Tests** | **ADOPTED** | Evaluates cross-hospital and cross-country generalization (`RQ1`, `87.7%` literature gap `P0027`). |
| **Group-Cluster Bootstrap `95% CI` (`1,000` resamples over `GroupID`)** | **ADOPTED** | Properly accounts for intra-OPG box correlation (`P0031` `3.05–6.17×` clustering) without retraining! |
| **Multi-Seed Sensitivity (`3` seeds on `TrackA` winner)** | **CONDITIONAL** | Run on primary `TrackA` winner if Kaggle weekly GPU quota permits (`report all seeds, never best-only`). |
| **Cross-Modality `CBCT`/`BW` Numeric Ranking** | **DECLINED** | Strictly prohibited by `scope.md v1.0.0` (`G01 PASS`) and `GAP0004`. |
| **Full `5`-Seed Training Across All `13` `EXP`s** | **DECLINED** | `65` full training runs exceed free Kaggle GPU quota (`~30 hr/week`); replaced by single-seed matrix + `GroupID` bootstrap `CI` (+ optional `3`-seed `TrackA` check). |
