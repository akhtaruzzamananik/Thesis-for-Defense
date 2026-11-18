# OPG Preprocessing Pipeline, Coordinate Geometry Contract & Leakage Isolation Specification (`STEP-019`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-019` (`S09` — Design preprocessing and coordinate-preserving transforms) |
| Record | `05_Preprocessing/specs/pipeline.md` (`v1.0.0`) |
| Owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward & Preprocessing Lead) |
| Co-Reviewer & Clinical Sign-Off | Mahajub Al Shabah (`232-15-900`, Reproducibility & Leakage Reviewer), Ms Faiza Feroz (`Supervisor`) & Clinical/Dental Review Team |
| Date | `2026-11-19` |
| Governing Sections | `OS §4.3`, `§6.1–6.2`, `§13.2`; Blueprint `STEP-019`; `02_Literature/research_questions.md` (`RQ2`, `GAP0005`); `DEC0009.md` (`UD09`) |
| Registered Configurations | `PP0001` (`Raw 640×640 Letterbox Baseline`), `PP0002` (`CLAHE 2.0 8×8 @ 640`), `PP0003` (`CLAHE 3.0 16×16 @ 640`), `PP0004` (`Raw 1280×1280 High-Res Letterbox`) |
| Implementation & Tests | `src/opg/preprocessing.py` & `tests/test_preprocessing.py` |
| Split-Dependent Materialization Status | **STRICTLY BLOCKED UNTIL `STEP-020 / G07 PASS`** (enforced programmatically by `fit_training_statistics(..., g07_split_passed=...)`) |

---

## 1. Grounded Rationale & Separation of Operations (`STEP-019` Procedure #1 & #3)

The deleted report's Figure 1 listed five generic candidate operations (*contrast enhancement, noise reduction, resizing, normalization, filtering*) without parameters or evidence that filtering improves `2D OPG` detection (`OS §1.3 RF08`, `OS §4.3`). Our literature synthesis (`02_Literature/synthesis.md`, `GAP0005`, `CLAIM0008–0009`) and `STEP-013` forensic quality audits across `DS0001–DS0006` (`7,789` active OPGs) established two critical empirical facts:
1. **Unverified Filtering Can Erase Small Radiolucent Targets (`GAP0005`):** While `P0004` (`mAP50 +3.4%`) and `P0024` (`DS0003`) advocated `CLAHE`, four controlled studies (`P0011`, `P0029`, `P0038`, `P0041`) reported **null or negative effects** when aggressive contrast enhancement or smoothing amplified trabecular bone noise and blurred subtle periapical (`PAI 3`) and interproximal caries boundaries.
2. **Cohort-Specific Structural Artifacts Observed in `STEP-013`:**
   - **`DS0001` (`UMFIH`) & `DS0005` (`AU-OPG`):** Contain `1` (`v60.png`) and `17` `RGBA` 4-channel PNG/JPG files alongside 3-channel grayscale-consistent `RGB` images.
   - **`DS0003` (`Rahman Dhaka`):** Contains `30` JPGs with `Windows Photo Editor` `DateTime/Software` EXIF/XMP headers and burned-in bottom-corner clinic stamps (`"PRESCRIPTION POINT"`).
   - **`DS0006` (`MD-OPG` Pediatric Cohort):** Every image (`1920 × 1535`) is framed inside a massive **solid-black letterbox border (`66.17%` median black pixels $\le 3$)**, which severely minifies pediatric caries boxes (`p, o`) if naively downscaled to `640 × 640` without first cropping the outer solid-black frame.
   - **`DS0004` (`Do 2024 Hanoi`):** Contains `6,741` tiny focal `PAI 3–5` apical boxes (`mean_w = 0.025, mean_h = 0.038`) sensitive to downsampling minification.

Therefore, in compliance with `OS §4.3` (*"begin with the minimum preparation necessary for the selected YOLO implementation, preserve aspect ratio where feasible, and evaluate any additional enhancement as an explicit controlled factor"*), we separate operations into three distinct phases and reject arbitrary blurring/denoising filters:

| Phase | Operations Included | Partition Scope & Determinism | Fitted Cross-Image State? |
|---|---|---|---|
| **Phase A: Fixed Per-Image Hygiene & Reference Sanitization** | 1. Strip all EXIF/XMP/ICC metadata tags on export;<br>2. Standardize channel format (`L` / `RGBA` $\to$ 3-channel grayscale-consistent `RGB uint8`);<br>3. `DS0006` outer solid-black border autocrop (`black_threshold = 8`, `margin_px = 8`) expanded to guarantee `100%` box inclusion;<br>4. `DS0003` safe corner-logo mask (`bottom_right` $14\% \times 10\%$, applied **only** when disjoint from all target boxes for public figures/`S16` demo). | Deterministic across all partitions (`train`, `val`, `test`) | **`None`** (`fit_on_partition = none`) |
| **Phase B: Controlled Model-Input Preparation (`PP0001–PP0004`)** | 1. Optional deterministic Luma `CLAHE` (`PP0001/PP0004`: `none`; `PP0002`: `clip=2.0, grid=8×8`; `PP0003`: `clip=3.0, grid=16×16`);<br>2. Aspect-ratio-preserving letterbox resize to `target_size` (`640×640` for `PP0001–0003`; `1280×1280` for `PP0004`) with constant neutral gray padding (`pad_value = 114`);<br>3. Pixel intensity scaling to `[0.0, 1.0]` (`float32 = uint8 / 255.0`). | Deterministic across `train`, `val`, `test` (`matched to deployment inference`) | **`None`** (`0` validation/test statistics used) |
| **Phase C: Stochastic Training-Only Augmentation** | Online minor rotation ($\pm 5^\circ$), scale jitter ($[0.90, 1.10]$), translation ($\pm 5\%$), and mild brightness/contrast jitter ($\pm 10\%$) with synchronized box transformation. | **`train` partition ONLY** (strictly disabled on `val` and `test`: `apply_to_val_or_test = false`) | **`None`** (online stochastic during training only, **after** `STEP-020` split lock) |

### Explicit Non-Adoption of Arbitrary Denoising / Median / Gaussian Blur (`OS §4.3`)
- **Decision (`UD09`):** Gaussian/median/bilateral smoothing filters are **explicitly not adopted** in baseline or primary tracks because `STEP-013` sharpness audits (`Laplacian var`) and literature evidence (`P0011`, `P0032`) show low-pass filtering blurs fine lamina dura discontinuities (`PAI 3`) and incipient carious cavitation margins.

---

## 2. Exact Forward & Inverse Box Coordinate Geometry Contract (`STEP-019` Procedure #2)

Implemented in `src/opg/preprocessing.py` (`TransformLedger`, `forward_transform_box`, `inverse_transform_box`, `prepare_image_and_boxes`) and verified in `tests/test_preprocessing.py`:

1. **Step 1 — Optional Outer Black-Border Autocrop (`DS0006` only):**
   - Given raw image dimensions $(W_{\text{src}}, H_{\text{src}})$ and crop window $(x_{\text{crop}}, y_{\text{crop}}, W_{\text{crop}}, H_{\text{crop}})$ (where $x_{\text{crop}} = y_{\text{crop}} = 0, W_{\text{crop}} = W_{\text{src}}, H_{\text{crop}} = H_{\text{src}}$ when autocrop is disabled):
     $$x' = x - x_{\text{crop}}, \quad y' = y - y_{\text{crop}}$$
   - **Safety Invariant:** `autocrop_black_border_with_boxes` expands $(x_{\text{crop}}, y_{\text{crop}}, W_{\text{crop}}, H_{\text{crop}})$ to enclose the union of non-black pixels ($I > 8$) **and** every ground-truth box plus an `8 px` margin, mathematically guaranteeing **zero clipped or dropped boxes**.
2. **Step 2 — Aspect-Preserving Letterbox Resize to $(W_{\text{out}}, H_{\text{out}})$:**
   - Compute isotropic scale factor:
     $$s = \min\left(\frac{W_{\text{out}}}{W_{\text{crop}}}, \frac{H_{\text{out}}}{H_{\text{crop}}}\right), \quad W_{\text{new}} = \text{round}(W_{\text{crop}} \cdot s), \quad H_{\text{new}} = \text{round}(H_{\text{crop}} \cdot s)$$
   - Effective axis scales and symmetric integer padding:
     $$s_x = \frac{W_{\text{new}}}{W_{\text{crop}}}, \quad s_y = \frac{H_{\text{new}}}{H_{\text{crop}}}, \quad p_{\text{left}} = \left\lfloor \frac{W_{\text{out}} - W_{\text{new}}}{2} \right\rfloor, \quad p_{\text{top}} = \left\lfloor \frac{H_{\text{out}} - H_{\text{new}}}{2} \right\rfloor$$
   - **Forward Box Mapping (`Source Raw Pixels -> Prepared Output Pixels`):**
     $$x_{\text{out}} = (x - x_{\text{crop}}) \cdot s_x + p_{\text{left}}, \quad y_{\text{out}} = (y - y_{\text{crop}}) \cdot s_y + p_{\text{top}}$$
   - **Inverse Box Mapping (`Prepared Output / Predicted Pixels -> Source Raw Pixels`):**
     $$x = \frac{x_{\text{out}} - p_{\text{left}}}{s_x} + x_{\text{crop}}, \quad y = \frac{y_{\text{out}} - p_{\text{top}}}{s_y} + y_{\text{crop}}$$
3. **Round-Trip Error Tolerance (`UD09`):**
   - Across `pixel -> forward letterbox -> normalized 6-decimal YOLO .txt -> pixel -> inverse letterbox`, maximum round-trip coordinate error back on the original radiograph must satisfy **$\max |\Delta_{\text{px}}| < 0.05\text{ px}$** (measured $< 0.02\text{ px}$ in `tests/test_preprocessing.py`).
   - Any transform that collapses a valid box to zero area or drops a box raises a `ValueError` / `RuntimeError` immediately.

---

## 3. Registered Preprocessing Configurations (`PP0001–PP0004`, `RQ2` Controlled Matrix)

All four YAML files in `05_Preprocessing/configs/` are schema-validated by `load_and_validate_pp_yaml`:

| `PreprocessingID` | Config Path | Config `SHA-256` | Target Size | Contrast Method & Params | Scientific Role (`RQ1` / `RQ2`) |
|---|---|---|---|---|---|
| **`PP0001`** | `05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml` | `04493e1e2bcdfcadbef5b044b392bf7091822439381e158d85c144d420e0b93b` | `640 × 640` | `none` (unenhanced raw intensity) | **Primary Baseline (`RQ1` & `RQ2` control)** across all tracks (`Tracks A–F`). |
| **`PP0002`** | `05_Preprocessing/configs/PP0002_clahe_2p0_8x8.yaml` | `7482eac3c347664672f287781aba8f5b952bfc219059bc5fdd2570d539eedfbf` | `640 × 640` | `clahe` (`clip_limit=2.0`, `tile_grid_size=[8, 8]`) | **`RQ2` Controlled Factor 1:** Standard moderate `CLAHE` ablation vs `PP0001` under identical split & seed (`DS0001`, `DS0003`, `DS0004`). |
| **`PP0003`** | `05_Preprocessing/configs/PP0003_clahe_3p0_16x16.yaml` | `65b7ffd170ce05d5e2ae9f8acbd1f401acaf430e69754ba86caaedc64166c64e` | `640 × 640` | `clahe` (`clip_limit=3.0`, `tile_grid_size=[16, 16]`) | **`RQ2` Controlled Factor 2:** Fine-grid higher-clip `CLAHE` testing local lesion contrast vs noise false positives. |
| **`PP0004`** | `05_Preprocessing/configs/PP0004_highres_letterbox_1280.yaml` | `08fd22b42f9fa31465eedc092251d92d7b5338b76de4fc7d321a7c77741dd2de` | `1280 × 1280` | `none` (unenhanced raw intensity) | **`RQ2` Controlled Factor 3:** High-resolution spatial preservation for small radiolucent targets (`PAI 3–5` & focal caries). |

---

## 4. Training-Only Fit Rules, Augmentation Limits & Leakage Guards (`STEP-019` Procedure #4)

1. **Block on Pre-Split Fitting & Materialization (`STEP-019` DoD):**
   - `fit_training_statistics` in `src/opg/preprocessing.py` requires `g07_split_passed=True` and `partition_names == ["train", ...]`; calling it before `STEP-020 / G07 PASS` or passing any `"val"` / `"test"` record raises a `RuntimeError`.
   - No prepared dataset release (`05_Preprocessing/processed/REL####/`) may be materialized until `STEP-020` (`G07 PASS`) locks the leakage-safe grouped split (`SPLIT0001–SPLIT0006`).
2. **Prohibited Augmentation Effects (`OS §4.3`, `§6.1`):**
   - **No pre-split offline augmentation:** Augmenting before splitting was the root cause of the `+30.4%` leakage inflation in `P0011` (`DS0004`) and `DS0003` Roboflow folders.
   - **No vertical flips (`vertical_flip` prohibited):** Inverts maxillary vs mandibular anatomy into non-physiological orientation.
   - **No horizontal flips when quadrant/laterality is evaluated (`horizontal_flip_allowed_when_laterality_matters = false`):** Prevents swapping left (`Q2/Q3`) and right (`Q1/Q4`) anatomical quadrants.
   - **No random cropping that drops or truncates target boxes.**
   - **Zero augmentation on `validation` or `test` partitions (`apply_to_val_or_test = false`).**
