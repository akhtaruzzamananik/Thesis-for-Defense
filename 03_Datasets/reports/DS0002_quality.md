# STEP-013 Quality, Privacy, Duplicate & Label Forensic Audit — `DS0002` (`CAND0002` DENTEX)

| Field | Value |
|---|---|
| DatasetID / CandidateID | `DS0002` / `CAND0002` (`DENTEX MICCAI 2023`) |
| Audit Scope & Count | **`755`** active PNGs (`705` labeled train + `50` unlabeled challenge validation); `2,899` quarantined (`quadrant_only`, `enum_only`, `unlabelled`, `.ipynb_checkpoints`); `0` decode errors |
| Owner / Auditor | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Date | `2026-11-18` |
| Evidence Sources | `03_Datasets/manifests/DS0002_images.csv`, `03_Datasets/manifests/DS0002_qc_summary.json`, off-Git `DS0002_restricted_qc.csv`, `DS0002_restricted_dups.csv`, `qc_samples/DS0002_qc_sheet.jpg` |
| Gate Status | **`G04 PASS` (`2026-11-18`, `G04_assessment_2026-11-18.md`)** |

---

## 1. Decoding, Dimensions, Sensor Artifact & Photometric Quality

| Metric (`N = 755` active PNGs) | `min` | `p05` | `median` | `p95` | `max` | Finding |
|---|---|---|---|---|---|---|
| **Width (px)** | `1,976` | `2,512` | `2,872` | `2,983.3` | `3,139` | `0` images `< 800` px; consistently high diagnostic resolution |
| **Height (px)** | `976` | `1,316` | `1,316` | `1,504` | `1,536` | High vertical fidelity |
| **Aspect Ratio (`W/H`)** | `1.60` | `1.91` | `2.13` | `2.26` | `2.33` | `0` aspect outliers (`< 1.3` or `> 2.8`) |
| **Mean Luma (`0–255`)** | `53.85` | `94.86` | `113.07` | `125.88` | `145.86` | Balanced exposure spread |
| **`%` Black (`<= 3`) / White (`>= 252`)** | `0.55 / 0.06` | `1.40 / 0.15` | `1.87 / 1.39` | `5.21 / 1.74` | `39.43 / 3.22` | `DS0002_IMG_003635` has dark margins (`39.4%` black) |
| **Sharpness (`Laplacian var` @ 800w)** | `91.74` | `124.74` | `260.06` | `665.30` | `2,247.54` | High spike caused by **`DS0002_IMG_000641` sensor-banding artifact**! |

- **Visual Artifact Finding (`DS0002_qc_sheet.jpg` top-right):** **`DS0002_IMG_000641`** exhibits a severe vertical/horizontal readout **sensor streak band obscuring the entire left `~22%` of the frame (right mandibular ramus)**. Keep documented explicitly under `STEP-013` clinical/technical artifact policy rather than silently omitting.
- **Channels / Tint:** `0` non-grayscale tinted images (`100%` clean grayscale-channel RGB).

---

## 2. Privacy, License File & Duplicate Integrity

- **EXIF / PNG Metadata:** **`0` sensitive EXIF tags** (`0` PNG text chunks). Minor `"VistaPano"` device mark and `"R/L"` laterality corner tags visible (`DS0002_qc_sheet.jpg`); no patient names or hospital IDs observed.
- **In-Archive License Check:** Neither `.zip` contains an embedded `LICENSE` or `README` file; therefore conservative **`CC-BY-NC-SA-4.0`** attribution/ShareAlike tracking remains in effect alongside Zenodo `CC BY 4.0` metadata.
- **Duplicates Within `755` Active PNGs:**
  - **`0` exact SHA-256 duplicates** (`unique_active = 755`).
  - **`0` true near-duplicates:** All `25` non-exact `dHash <= 4` pairs (`20` within train, `5` `train<->val`) measured **`pixel correlation < 0.90`**, confirming clean distinct images across the `705 + 50` subset!
  - *(Author `.ipynb_checkpoints` copy inside `validation_data.zip` overlapped `1` active SHA-256 and was quarantined at `STEP-012`.)*

---

## 3. COCO Label Audit & Critical Literature Count Correction (`train_quadrant_enumeration_disease.json`)

- **Schema & bounds:** `705` images, `3,529` annotations, `0` OOB boxes (`> 1 px`), `0` zero-area boxes; **`validation_data.zip` contains `0` public ground-truth labels**.
- **CRITICAL CLASS-BALANCE CORRECTION (`P0014` myth vs measured JSON):**
  - Earlier literature summaries (`CAND0002` citing `P0014`) listed `[799, 942, 823, 965]` as disease box counts, making `DENTEX` appear nearly balanced (`~800–965/class`).
  - Direct parsing of `train_quadrant_enumeration_disease.json` proves **`[823, 799, 965, 942]` are actually `categories_1` (`Quadrant 1–4`) counts**, whereas actual **`categories_3` (disease classes)** are **strongly skewed (`14:1` imbalance!)**:
    - **`Caries` (`id=1`): `2,189` boxes (`62.0%`)**
    - **`Impacted` (`id=0`): `604` boxes (`17.1%`)**
    - **`Deep Caries` (`id=3`): `578` boxes (`16.4%`)**
    - **`Periapical Lesion` (`id=2`): `158` boxes (`4.5%`)**
  - **Impact on `UD04 / UD08`:** Because `validation_data` (`50` PNGs) has no public labels AND `Periapical Lesion` only has `158` boxes across `705` labeled OPGs, evaluating `DENTEX` requires splitting the **`705` labeled OPGs** (`~24` PA test boxes at `15%` test) + dental reviewer QA check (`G05/G06`) because labeler `κ`/credentials remain undisclosed (`P0014 p. 3`).
