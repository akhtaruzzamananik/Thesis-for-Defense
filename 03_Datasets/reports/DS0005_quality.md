# STEP-013 Quality, Privacy, Duplicate & Label Forensic Audit — `DS0005` (`CAND0005` AU-OPG Ajman UAE)

| Field | Value |
|---|---|
| DatasetID / CandidateID | `DS0005` / `CAND0005` (`AU-OPG` Ajman University Dental Clinic, `YSFF/AU-OPG`, `P0026`) |
| Audit Scope & Count | **`901`** active annotated OPGs (`630` train, `135` val, `136` test); `134` extra unannotated `.jpg`s + `1` README figure quarantined; `0` decode errors |
| Owner / Auditor | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Date | `2026-11-17` |
| Evidence Sources | `03_Datasets/manifests/DS0005_images.csv`, `03_Datasets/manifests/DS0005_qc_summary.json`, off-Git `DS0005_restricted_qc.csv`, `DS0005_restricted_dups.csv`, `qc_samples/DS0005_qc_sheet.jpg`, `dup_pair_verification.jpg` |
| Gate Status | Batch 1 technical audit **complete**; **`G04` remains `NOT ASSESSED`** awaiting Batch 2 (`DS0002`, `DS0004`) + team/dental suitability sign-off |

---

## 1. Decoding, Dimensions, Channels & Photometric Quality

| Metric (`N = 901` active OPGs) | `min` | `p05` | `median` | `p95` | `max` | Finding |
|---|---|---|---|---|---|---|
| **Width (px)** | `2,628` | `3,288` | `3,292` | `3,296` | `3,296` | Very uniform high-res `Cranex` clinical OPGs |
| **Height (px)** | `1,500` | `1,500` | `1,500` | `1,500` | `1,500` | Standardized `1500 px` height (`100%` `>= 2628` wide) |
| **Aspect Ratio (`W/H`)** | `1.75` | `2.19` | `2.19` | `2.20` | `2.20` | `0` aspect-ratio outliers |
| **Mean Luma (`0–255`)** | `57.46` | `88.61` | `113.23` | `136.99` | `157.20` | Consistent exposure range |
| **`%` Black (`<= 3`) / White (`>= 252`)** | `0.89 / 2.59` | `1.91 / 2.79` | `5.15 / 3.00` | `9.99 / 3.31` | `19.42 / 7.34` | Thin uniform scanner frame border (`~3%` white border line) |
| **Sharpness (`Laplacian var` @ 800w)** | `41.19` | `61.92` | `89.42` | `144.65` | `742.22` | Softer gradient texture vs `UMFIH`, clinically clear overall (`DS0005_qc_sheet.jpg`) |

- **Channels / Tint:** `0` non-grayscale tinted images (`R==G==B` across RGB/RGBA images; note `17` files inside full `dataset/` decoded as `RGBA` -> normalize cleanly to `RGB` in pipeline).

---

## 2. Privacy, EXIF & Visual Inspection (`DS0005_qc_sheet.jpg`)

- **EXIF / metadata:** **`0` images** carry sensitive EXIF tags (`Make/Model/Software/DateTime/GPS = 0`).
- **Visual pixel inspection (`DS0005_qc_sheet.jpg`):** Genuine adult clinical `2D OPG`s showing fixation plates, implants, crowns, retained roots, and distorted edge cases intentionally retained by `P0026`. Small `[R]/[L]` bottom-corner badge present; **no hospital/patient text stamps observed in sampled frames**.

---

## 3. Critical Duplicate Leakage Finding (`Despite "Serial OPGs Excluded" Claim!`)

Although `AU-OPG` returned **`0` exact SHA-256 duplicates** (`1,036` distinct files) and `P0026 (p. 4)` stated serial patient radiographs were excluded, pixel-level perceptual screening caught **direct split leakage across the official `train` and `val` CSVs**:

1. **`6` Re-encoded Byte-Changed Identical Images (`corr >= 0.99`, `dHash H=0`) Leaking `train <-> val`:**
   - Verified directly in `dup_pair_verification.jpg` row 1 (`DS0005_IMG_000688 [val]` vs `DS0005_IMG_000932 [train]`, `corr = 1.0000` — identical radiograph with same single lower-right implant saved under two hashes/filenames!).
   - All `6` identical `corr >= 0.99` pairs sit **strictly across `train_annotated <-> val_annotated`** (causing `6 / 135 = 4.4%` validation contamination in the official HF splits).
2. **Additional `0.95–0.99` Pairs & Visual Boundary Clarification:**
   - `2` pairs measure `corr = 0.95–0.99` (`1` inside `test`, `1` inside `train`).
   - Meanwhile, inspecting `corr = 0.90–0.95` pairs on `dup_pair_verification.jpg` row 2 (`DS0005_IMG_000309 [train]` vs `DS0005_IMG_000346 [test]`, `H=3, corr=0.9273`) proved **`0.90–0.95` on standardized `Cranex` frames can be different patients** (2 fused upper-right implants vs 1 upper-midline implant) — demonstrating why **visual confirmation + strict threshold separation (`>= 0.98–0.99` vs exploratory `0.95–0.98`)** prevents false exclusion!
3. **`134` Extra Unannotated `.jpg`s in HF `dataset/`:** **`90 / 134` (`67%`) match annotated splits within `dHash <= 6`**, confirming quarantine of all `134` unannotated extras prevents accidental leakage/unlabeled bias.
4. **Cross-cohort overlap:** `0` true overlaps against `DS0001`, `DS0003`, `DS0006` (`max cross corr = 0.7746`).

---

## 4. Label-Schema Audit (`7,006` CSV OBB Rows Across `901` OPGs)

- Exact row & image match to `P0026 Table 2`:
  - `train`: `4,964` rows (`630` imgs) — `Filled 1,986`, `Crowned 1,009`, `Retained Root 669`, `Cavitated 587`, `Implant 360`, `Impacted 353`
  - `val`: `1,010` rows (`135` imgs) — `Filled 421`, `Crowned 170`, `Retained Root 137`, `Cavitated 117`, `Implant 111`, `Impacted 54`
  - `test`: `1,032` rows (`136` imgs) — `Filled 450`, `Crowned 198`, `Retained Root 135`, `Cavitated 111`, `Implant 73`, `Impacted 65`
- **Geometry:** Rotation `[0.0°, 359.97°]`; `0` rotated-corner bounds `> 5 px` outside image (`1` minor unrotated boundary `> 1 px` in `test`). Sound teeth remain unannotated (`P0026 p. 7`).

---

## 5. Prospective Rules (`G04 / UD05 / UD07`)

1. Retain the **`901` annotated OPGs** (standardizing `RGBA -> RGB`), keep the `134` unannotated extras & `1` sample PNG **quarantined**, and **deduplicate / regroup the `6` `corr >= 0.99` `train<->val` leaks** (plus inspect the `2` `0.95–0.99` pairs) before any split freeze (`G07`).
2. Keep isolated on its dedicated **adult tooth-level `OBB -> AABB` sub-track** unless explicitly reconciled under `UD04–UD05`.
