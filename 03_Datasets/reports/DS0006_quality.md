# STEP-013 Quality, Privacy, Duplicate & Label Forensic Audit — `DS0006` (`CAND0007` MD-OPG Pediatric Cohort)

| Field | Value |
|---|---|
| DatasetID / CandidateID | `DS0006` / `CAND0007` (`MD-OPG` Pediatric Mixed Dentition Caries Dataset, `Zenodo 17786082`, `P0010`) |
| Audit Scope & Count | **`170`** active full pediatric `OPG_Image` PNGs (`340` derived `Smile_Zone_IMG` & `Smile_Zone_MSK` quarantined); `0` decode errors |
| Owner / Auditor | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Date | `2026-11-17` |
| Evidence Sources | `03_Datasets/manifests/DS0006_images.csv`, `03_Datasets/manifests/DS0006_qc_summary.json`, off-Git `DS0006_restricted_qc.csv`, `qc_samples/DS0006_qc_sheet.jpg` |
| Gate Status | **`G04 PASS` (`2026-11-18`, `G04_assessment_2026-11-18.md`)** |

---

## 1. Decoding, Dimensions, Letterbox Padding & Photometric Quality

| Metric (`N = 170` active PNGs) | `min` | `p05` | `median` | `p95` | `max` | Visual / Forensic Explanation |
|---|---|---|---|---|---|---|
| **Width (px)** | `1,343` | `1,920` | `1,920` | `1,920` | `1,920` | `167/170` are `1920 × 1535`; `2` are `1440 × 1151`; `1` is `1343 × 1074` |
| **Height (px)** | `1,074` | `1,535` | `1,535` | `1,535` | `1,535` | — |
| **Aspect Ratio (`W/H`)** | `1.25` | `1.25` | `1.25` | `1.25` | `1.25` | **Visual explanation (`DS0006_qc_sheet.jpg`):** Not an anatomical square! Every PNG is **padded inside massive solid black letterbox margins (`~66.17%` black pixels `<= 3`)** framing a central thin white border box! |
| **Mean Luma (`0–255`)** | `30.17` | `33.43` | `40.99` | `63.14` | `69.59` | Artificially depressed by `48.7%–71.4%` solid black margin padding |
| **`%` Black (`<= 3`)** | `48.73%` | `50.11%` | **`66.17%`** | `68.96%` | `71.40%` | **Mandatory `UD09` insight:** autocrop solid black margins (shifting polygon coords) OR use `Smile Zone` ROI to prevent severe tooth minification at `640 × 640`! |
| **Sharpness (`Laplacian var` @ 800w)** | `269.40` | `304.26` | `499.87` | `846.77` | `1,012.33` | Clean, crisp pediatric mixed-dentition films inside inner white border |

- **Channels (`170 non-identical RGB`?):** Saved as `RGB` PNGs with `icc_profile` metadata (`0` sensitive EXIF tags); subtle RGB channel variations in padded exports require deterministic grayscale/RGB normalization.

---

## 2. Privacy, Visual & Duplicate Screening (`DS0006_qc_sheet.jpg`)

- **EXIF tags:** `0` sensitive EXIF tags (`0` `DateTime/Software/GPS`). Note each `OPG_Annotation/P_###_Ann_.json` embeds base64 `imageData` (never copy raw JSONs containing `imageData` to public Git!).
- **Visual check (`DS0006_qc_sheet.jpg`):** Clear pediatric mixed-dentition `2D OPG` radiographs (`ages 3–12`) with unerupted permanent tooth buds, primary molars/restorations, small `[R/L]` marker, and a thin white perimeter rectangle surrounded by solid black padding. **Zero burned-in patient names/IDs observed.**
- **Duplicates:** `0` exact SHA-256 duplicates. *(Note: raw whole-image `dHash` reported `724` pairs because `66%` identical solid-black border dominates the `8×9` downsample! Visual spot-check confirms diverse pediatric dentition across samples; re-run `dHash` on border-cropped interior in `UD07` before splitting.)*

---

## 3. Label-Schema Audit (`170` LabelMe JSONs)

- Exact match to `P0010 Table 1`:
  - `json_count = 170`, `empty_annotation_files = 0`, `oob_shapes_gt1px = 0`.
  - Shapes: **`p` (Proximal caries) = `716` polygons**, **`o` (Occlusal caries) = `179` polygons**, **`z` (Smile Zone ROI) = `170` rectangles**.
  - **Defect caught:** **`1` zero-area shape (`zero_area_shapes = 1`)** detected in JSON shapes — must drop/repair deterministically during polygon-to-AABB export (`UD05`).

---

## 4. Prospective Inclusion & Exclusion Rules

1. **Retain all `170` full pediatric `OPG_Image` PNGs** strictly on a **separate pediatric caries sub-track** (`mixed dentition ages 3–12` must NOT confound adult models).
2. **Keep `340` `Smile_Zone_IMG` / `Smile_Zone_MSK` files quarantined** to avoid double-counting.
3. **Require border-cropped interior `dHash` check (`UD07`)** + black-margin autocrop / coordinate-shift validation (`UD09`) + clean removal of the `1` zero-area shape and embedded `imageData` before any export.
