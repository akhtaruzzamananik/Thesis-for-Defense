# Experiment Matrix, Training, Stopping & Selection Plan (`STEP-024` / `UD12`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-024` (`S10` — Approve baseline, experiment and evaluation plans) |
| Record | `07_Experiments/experiment_plan.md` (`v1.0.0`) |
| Owner | Mahajub Al Shabah (`232-15-900`, Model & Evaluation Lead) |
| Co-Reviewer & Approver | Akhtaruzzaman Anik (`232-15-252`, Research Lead) & Ms Faiza Feroz (`Supervisor`) |
| Date | `2026-11-19` |
| Governing Sections | `OS §5.2`, `§5.5`, `§13.2`; Blueprint `STEP-024`; `DEC0012.md` (`UD12`), `DEC0016.md` (`UD16`) |

---

## 1. Training, Stopping & Validation Selection Policy (`UD12` / `DEC0012`)

1. **Controlled Training Hyperparameters (Matched Across Fair Comparisons):**
   - **Optimizer & Schedule:** `AdamW` (`lr0 = 0.001`, `lrf = 0.01` cosine decay, `momentum = 0.937`, `weight_decay = 0.0005`, `warmup_epochs = 3.0`), using `ultralytics==8.3.253` COCO-pretrained weights (`yolo11s.pt`, `yolov8s.pt`, `yolo11m.pt`).
   - **Epochs & Early Stopping (`Stopping Rule`):** Max **`100` epochs** per registered `EXP####` with **`patience = 20` epochs** monitoring **validation `mAP@0.50`** (saving `best.pt` on highest `val mAP@0.50` and `last.pt` every epoch for recovery).
   - **Batch Size & Mixed Precision:** `batch_size = 16` at `640 × 640` (`PP0001–0003`); `batch_size = 4` (or `8` if VRAM allows on `T4`/`P100` `16 GB`) at `1280 × 1280` (`PP0004`), with `amp = true` (`FP16` mixed precision during training).
   - **Determinism & Seed Policy:** Primary fixed seed **`20261124`** (`deterministic = true`) across all baseline and `RQ2` ablation comparisons. Optional `3`-seed sensitivity (`20261124, 20261125, 20261126`) on the primary `Track A` winner if Kaggle GPU quota allows — reporting **all** seeds, never cherry-picking the best seed afterward!
   - **Online Training Augmentation (`OS §4.3`, `PP0001–PP0004`):** Restricted strictly to `train` partition (`degrees=5.0, translate=0.05, scale=0.10, hsv_v=0.10, fliplr=0.0, flipud=0.0, mosaic=0.5, close_mosaic=10`); `val` and `test` receive **zero** stochastic augmentation.
2. **Model Selection Criterion (`Validation-Only`):**
   - Primary selection metric on `val`: **`mAP@0.50`** (tie-breaker: **`mAP@0.50:0.95`**).
   - **`test` and `external_test` partitions remain strictly sealed** until the `G11` freeze (`STEP-031`).

---

## 2. Preregistered Experiment Matrix (`RQ0–RQ3`)

### 2.1 Diagnostic Smoke Experiment (`STEP-026 / G09` — Not Reportable)
- **`EXP0000_SMOKE`:** `TrackA` (`REL0001`, small `32`-train / `16`-val subset), `YOLO11s`, `PP0001` (`640×640`), `2` epochs, `batch=8`, interrupted at epoch `1` and restored to prove checkpoint recovery & finite logs (`G09`).

### 2.2 Primary Baseline & Multi-Track Benchmark Matrix (`RQ0` & `RQ1`)
| `EXP ID` | `RQ` | Dataset / Release (`Track`) | Model (`MC`) | Preprocessing (`PP`) | Controlled Factor / Scientific Comparison |
|---|---|---|---|---|---|
| **`EXP0001`** | `RQ0, RQ1` | `DS0001` / `REL0001` (`TrackA`, `13` cls) | **`YOLO11s`** (`MC0001`) | `PP0001` (`Raw 640`) | **Primary Multi-Class Baseline** on deduplicated `UMFIH`. |
| **`EXP0002`** | `RQ1, RQ3` | `DS0001` / `REL0001` (`TrackA`, `13` cls) | **`YOLOv8s`** (`MC0002`) | `PP0001` (`Raw 640`) | **Cross-Generation Architecture Comparator** vs `EXP0001` (`YOLOv8s` vs `YOLO11s`). |
| **`EXP0003`** | `RQ0, RQ1` | `DS0002` / `REL0002` (`TrackB`, `4` cls) | **`YOLO11s`** (`MC0001`) | `PP0001` (`Raw 640`) | Skewed `4`-class `DENTEX` benchmark (`Caries, Impacted, PA, Deep Caries`). |
| **`EXP0004`** | `RQ0, RQ1` | `DS0003` / `REL0003` (`TrackC`, `6` cls) | **`YOLO11s`** (`MC0001`) | `PP0001` (`Raw 640`) | Bangladeshi handheld-film clinical shift (`5-cls pathology` + `6-cls`). |
| **`EXP0005`** | `RQ0, RQ1` | `DS0004` / `REL0004` (`TrackD`, `3` cls) | **`YOLO11s`** (`MC0001`) | `PP0001` (`Raw 640`) | `PAI 3–5` focal periapical lesion baseline (`3,863` canonical OPGs). |
| **`EXP0006`** | `RQ0, RQ1` | `DS0005` / `REL0005` (`TrackE`, `6` cls) | **`YOLO11s`** (`MC0001`) | `PP0001` (`Raw 640`) | Adult `OBB->AABB` UAE benchmark (`6` tooth/restoration/pathology classes). |
| **`EXP0007`** | `RQ0, RQ1` | `DS0006` / `REL0006` (`TrackF`, `2` cls) | **`YOLO11s`** (`MC0001`) | `PP0001` (`Raw 640` + autocrop) | Pediatric mixed-dentition caries (`Proximal` & `Occlusal`). |

### 2.3 Controlled `RQ2` Preprocessing & Resolution Ablation Matrix (Single-Factor Changes)
| `EXP ID` | `RQ` | Dataset / Release (`Track`) | Model | Preprocessing (`PP`) | Matched Control | Single Changed Factor Tested |
|---|---|---|---|---|---|---|
| **`EXP0008`** | `RQ2` | `DS0001` / `REL0001` (`TrackA`) | `YOLO11s` | **`PP0002` (`CLAHE 2.0, 8×8`)** | `EXP0001` | Moderate `CLAHE` vs raw unenhanced `PP0001`. |
| **`EXP0009`** | `RQ2` | `DS0001` / `REL0001` (`TrackA`) | `YOLO11s` | **`PP0003` (`CLAHE 3.0, 16×16`)** | `EXP0001` | Fine-grid stronger `CLAHE` vs `PP0001` & `PP0002`. |
| **`EXP0010`** | `RQ2, RQ3` | `DS0001` / `REL0001` (`TrackA`) | `YOLO11s` | **`PP0004` (`1280×1280 Raw`)** | `EXP0001` | $2\times$ spatial resolution (`1280` vs `640`) on small lesions + `FPS` tradeoff. |
| **`EXP0011`** | `RQ2, RQ3` | `DS0004` / `REL0004` (`TrackD`) | `YOLO11s` | **`PP0004` (`1280×1280 Raw`)** | `EXP0005` | High-resolution `1280×1280` vs `640×640` on tiny `PAI 3–5` apices. |
| **`EXP0012`** | `RQ2` | `DS0003` / `REL0003` (`TrackC`) | `YOLO11s` | **`PP0002` (`CLAHE 2.0, 8×8`)** | `EXP0004` | Falsifiable test of `P0024` `CLAHE` claim on Dhaka smartphone-photographed OPGs. |
| **`EXP0013`** *(Cond.)* | `RQ1, RQ3` | `DS0001` / `REL0001` (`TrackA`) | **`YOLO11m`** (`MC0003`) | `PP0001` (`Raw 640`) | `EXP0001` | Model scale-up (`YOLO11m` vs `YOLO11s`) if Kaggle weekly GPU quota allows. |

---

## 3. Validity Gates vs Scientific Success Criteria (`UD16` / `DEC0016`)

- **Technical Validity Gates (`G09–G14`):** Pass/fail depends on leak-free splits, deterministic metrics, verified checkpoints, and reproducible code — **never** on achieving an arbitrary inflated `mAP` score (`OS §13.3`).
- **Scientific Success Framing (`UD16` / `DEC0016`):** No arbitrary minimum `mAP` or minimum `FPS` target is invented (`OS §7.2–7.3`, `STEP-024` Common Mistakes). Scientific success is defined by: (1) valid, leak-free quantification of `Precision`, `Recall`, `mAP@0.50`, `mAP@0.50:0.95`, and `FPS_e2e` across all `6` tracks and `HC01–HC05` external bridges, (2) empirical resolution of `RQ2` (`Raw` vs `CLAHE` vs `1280px`), and (3) systematic radiographic error profiling (`T19`).
