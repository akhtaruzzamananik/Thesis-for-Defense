# STEP-013 Quality, Privacy, Duplicate & Label Forensic Audit — `DS0003` (`CAND0003` Rahman 2024 Dhaka)

| Field | Value |
|---|---|
| DatasetID / CandidateID | `DS0003` / `CAND0003` (`Dental OPG X-RAY Dataset` — Dhaka, Bangladesh) |
| Audit Scope & Count | **`231`** active original OPGs (`1,121` aug/classification copies strictly quarantined out of `1,352` archive files); `0` decode errors |
| Owner / Auditor | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Date | `2026-11-17` |
| Evidence Sources | `03_Datasets/manifests/DS0003_images.csv`, `03_Datasets/manifests/DS0003_qc_summary.json`, off-Git `DS0003_restricted_qc.csv`, `DS0003_restricted_dups.csv`, `qc_samples/DS0003_qc_sheet.jpg`, `dup_pair_verification.jpg` |
| Gate Status | Batch 1 technical audit **complete**; **`G04` remains `NOT ASSESSED`** awaiting Batch 2 (`DS0002`, `DS0004`) + team/dental suitability sign-off |

---

## 1. Decoding, Dimensions, Channels & Photometric Quality

| Metric (`N = 231` active originals) | `min` | `p05` | `median` | `p95` | `max` | Finding |
|---|---|---|---|---|---|---|
| **Width (px)** | `497` | `844` | `1,176` | `1,871` | `1,988` | **`7` low-res OPGs (`< 800` px wide)** from tight manual smartphone cropping |
| **Height (px)** | `259` | `408.5` | `601` | `910.5` | `1,260` | Handheld `Samsung Galaxy A52` film-photograph resolution jitter |
| **Aspect Ratio (`W/H`)** | `1.32` | `1.63` | `1.98` | `2.35` | `2.56` | `0` severe aspect outliers (`< 1.3` or `> 2.8`) |
| **Mean Luma (`0–255`)** | `92.10` | `110.52` | `129.35` | `140.37` | `154.53` | Moderate illumination shifts from clinic light-boxes |
| **Std Luma** | `36.14` | `48.67` | `58.32` | `68.27` | `73.73` | — |
| **`%` Black (`<= 3`) / White (`>= 252`)** | `0.0 / 0.0` | `0.0 / 0.0` | `0.02 / 0.17` | `0.13 / 1.19` | `7.13 / 1.98` | Minimal margin padding |
| **Sharpness (`Laplacian var` @ 800w)** | `22.15` | `121.64` | `395.91` | `1,640.15` | `2,706.58` | Huge sharpness gap: `22.15` motion blur (`DS0003_IMG_001216`) vs `2706.58` moiré grain (`DS0003_IMG_001156`) |

- **Channels / Tint:** `0` non-grayscale tinted images among `231` active originals (`R==G==B` when `RGB` or grayscale `L`).

---

## 2. Privacy, EXIF & Visual Burned-In Inspection (`DS0003_qc_sheet.jpg`)

- **EXIF / XMP Metadata Flagged (`30 / 231` JPGs):**
  - `30` active JPGs carry `EXIF` and `XMP` headers (`Software: Windows Photo Editor 10.0.10011.16384`, `DateTime: 2024:08:04–08:05`, `ExifOffset`). No patient names or GPS coordinates were found in EXIF, **but mandatory EXIF/XMP stripping MUST occur in preprocessing / export (`UD09`, `UD23`)**.
- **Visual inspection (`DS0003_qc_sheet.jpg` & `dup_pair_verification.jpg` row 3):**
  - **Clinic corner logo & `"R / OPG"` markings visible:** Sample `DS0003_IMG_001156` (and duplicate pair `DS0003_IMG_001153/1321`) visibly displays **`"OPG"` and partial corner clinic logo (`"PRESCRIPTION POINT"`)** from photographed hard-copy X-ray films, plus horizontal lightbox glare bands and tight vertical jaw cropping (`DS0003_IMG_001289`).
  - **Disclosure Rule (`OS §1.5`, `UD23`):** All `DS0003` images used in thesis figures or `S16` hosted defense demo MUST be corner-masked/inspected for `"PRESCRIPTION POINT"` or clinic logos beforehand.

---

## 3. Count Reconciliation (`231` vs `232`) & Near-Duplicate Film Catch

1. **Resolved `231` vs `232` discrepancy:**
   - `Original Dataset/` contains **`231`** images (`230` with `.txt` labels; **`DS0003_IMG_001202` is missing a paired `.txt` label file!**).
   - Forensic SHA-256 + `dHash` comparison against `Dental OPG (Classification)/` (`232` unique SHA-256s, `517` multi-folder copies) revealed:
     - `230` exact SHA-256 matches;
     - `DS0003_IMG_000070` (Classification) matches `DS0003_IMG_001146` (Original) at `dHash Hamming = 1` (re-saved copy);
     - **`DS0003_IMG_000023` (Classification only) has `min_dHash = 16` against all originals** — proving the **`232nd`** unique OPG exists only inside `Classification/` without an object-detection `.txt` label!
2. **Same-film smartphone re-shoot duplicate caught inside `Original Dataset`:**
   - **`4`** non-exact pairs had `dHash <= 4`, and visual inspection on **`dup_pair_verification.jpg` row 3 (`DS0003_IMG_001153 <-> DS0003_IMG_001321`, `dHash H=1`, `corr = 0.8625`)** confirmed they are **two separate handheld photos of the exact same radiographic film** (identical lower-left molar restoration, identical missing upper molar, slight phone shift). Must be grouped together (`UD07`) before any split!
3. **Cross-cohort overlap:** `0` true overlaps against `DS0001`, `DS0005`, `DS0006`.

---

## 4. Label-Schema Audit (`Original Dataset` `230` `.txt` files)

- **`1,189` boxes total** (`vs 1,204` claimed in `P0024`; `0` malformed, `0` OOB, `0` zero-area; `1` image `DS0003_IMG_001202` has no `.txt`):
  - Class `0`: `194` boxes (`mean_w=0.0705, mean_h=0.2212`)
  - Class `1`: `37` boxes (`mean_w=0.0894, mean_h=0.2447`)
  - Class `2`: `196` boxes (`mean_w=0.0805, mean_h=0.1764`)
  - Class `3`: `14` boxes (`mean_w=0.0628, mean_h=0.2298`)
  - Class `4`: `97` boxes (`mean_w=0.0524, mean_h=0.1910`)
  - Class `5`: `651` boxes (`mean_w=0.0617, mean_h=0.2459`) — notice tall `mean_h ~ 0.18–0.25` reflects **whole-tooth-bounding-boxes (`Healthy Teeth` + pathologic teeth)** rather than tight apical lesion boxes (`CAND0001`), requiring careful ontology reconciliation (`UD04`) before cross-cohort testing!

---

## 5. Prospective Inclusion & Exclusion Rules

1. **Keep quarantined (`DO NOT train on`):** All `604` Roboflow pre-split augmented images (`558` train + `23` valid + `23` test) and `517` `Classification` files.
2. **Retain `230` labeled active OPGs (`+ quarantine/review unlabeled DS0003_IMG_001202` and group duplicate re-shoots `DS0003_IMG_001153/1321` under `UD07`).**
3. **Strip EXIF/XMP cleanly** in preprocessing and verify clinic logos cropped/masked on public outputs.
