# T08 — Dataset Card: `DS0003` (`CAND0003` — Rahman et al. 2024 Dhaka OPG Cohort)

| Metadata | Value |
|---|---|
| TemplateID | T08 |
| template_version | v1.0.0 |
| entity_id | DS0003 |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-17 |
| status | Technical Quality Audited (`STEP-013` Batch 1 complete; `G04` review awaiting Batch 2 & dental check) |
| source_inputs | `https://doi.org/10.17632/c4hhrkxytw.4` (Mendeley Data V4); `03_Datasets/licenses/CAND0003_Rahman_Dhaka_CC-BY-4.0.md`; `03_Datasets/manifests/DS0003_images.csv`; `03_Datasets/reports/DS0003_quality.md` |
| governing_section | OS §4.1–4.2; Blueprint STEP-012 |
| sensitivity | Public metadata card (`raw/` & `DS0003_restricted_linkage.csv` strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`) |

## Origin/version

- **Archive:** `c4hhrkxytw-4.zip` (`doi:10.17632/c4hhrkxytw.4`, Mendeley Data Version 4, published `2024-08-27`, `Rahman et al. 2024` *Data in Brief* 57, 110970 `P0024`).

## access/license/ethics

- **Permission record:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`, `2026-11-17`).
- **License:** Mendeley API **`CC BY 4.0`** vs *Data in Brief* article **`CC BY-NC 4.0`** (conservatively treated as non-commercial academic `CC BY-NC 4.0` + `CC BY 4.0` attribution).
- **Ethics:** **Bangladesh Dental College & Hospital (`Protocol No: MK-198109`)** (`P0024 p. 13`), clinical films collected across 3 centers in Banani & Dhanmondi, Dhaka (`Prescription Point`, `LabAid`, `Ibn Sina`).

## modality

- `2D OPG` (re-photographed dental panoramic X-ray films captured via handheld `Samsung Galaxy A52` camera; `.jpg` images across grayscale `L` and `RGB` modes).

## population known/unknown

- Bangladeshi dental clinic patients in Dhaka (`exact age/sex breakdown not reported` in archive).

## collection

- **Total scanned images inside `c4hhrkxytw-4.zip`:** **`1,352`** `.jpg` files (`0` decode errors), cleanly partitioned at `STEP-012`:
  - `object_detection_original` (`Original Dataset`): **`231`** images + `231` YOLO `.txt` labels (**`acquired-uninspected`**)
  - `object_detection_aug_train` (`Augmented Dataset/train`): `558` images (**`quarantined-pre-augmented`**)
  - `object_detection_aug_valid` (`Augmented Dataset/valid`): `23` images (**`quarantined-pre-split-aug`**)
  - `object_detection_aug_test` (`Augmented Dataset/test`): `23` images (**`quarantined-pre-split-aug`**)
  - `classification_branch` (`Dental OPG (Classification)`): `517` multi-folder images (**`quarantined-classification-branch`** — forensic SHA-256 check confirms these are multi-class duplicates of **`232` unique OPGs**, overlapping `230/231` of `Original Dataset`!).

## patient/image/object counts

- **Total scanned:** `1,352` (`231` active object-detection originals + `1,121` quarantined pre-split/augmented/classification copies + `0` errors).
- **Important count reconciliation finding (`STEP-012`):** `P0024` reports `232` original OPGs (`1,204` boxes), whereas Mendeley V4 `Original Dataset/` contains **`231` `.jpg`s + `231` `.txt`s** while `Classification/` spans **`232` unique SHA-256s** (`2` unique classification hashes differ from `Original Dataset`, while `1` in `Original Dataset` is absent or altered in `Classification`). Exact mismatch must be inspected in `STEP-013` (perceptual hash vs valid/test folders).
- **Patient count:** Unknown (`patient IDs not reported`).

## quality/exclusions

- Audited in `03_Datasets/reports/DS0003_quality.md`: `231` active originals (`497–1988` px, `7 < 800` px wide, median Laplacian `395.91`); `30/231` carry Windows Photo Editor `DateTime/Software` EXIF/XMP; `"OPG"` / partial `"PRESCRIPTION POINT"` corner stamps visible on filmed sheets -> strip EXIF + verify crops (`UD23`). `DS0003_IMG_001202` lacks `.txt` (`230` `.txt`s = `1,189` boxes); `232nd` image exists only in `Classification/`.

## duplicates/grouping

- Quarantined `604` Roboflow aug + `517` classification files. Visually confirmed **`DS0003_IMG_001153 <-> DS0003_IMG_001321` (`dHash H=1, corr=0.8625`) are two handheld photos of the same OPG film** inside `Original Dataset/` (`dup_pair_verification.jpg` row 3) — group together under `UD07`.

## annotations

- YOLO `.txt` label files alongside `Original Dataset` across `6` reported classes (`Healthy Teeth, Caries, Impacted Teeth, BDC/BDR, Infection, Fractured Teeth`, 2-tier CVAT review without `κ` in `P0024`).

## biases

- Handheld smartphone film re-photography (glare, resolution jitter, keystone tilt) and extreme minority imbalance (`13` Fractured, `23` Infection). Unsuitable as standalone multi-class training set; ideal external Bangladeshi shift & `RQ2 CLAHE` testbed.

## intended use

- Dedicated Bangladeshi cross-cohort shift & `RQ2 CLAHE` contrast-ablation dataset (or grouped small-cohort benchmark subject to `STEP-013` and `UD04–UD08`).

## access/retention

- **Restricted storage:** `03_Datasets/raw/DS0003/` (`archive/` + `extracted/`, `.gitignore`-excluded) + Private Google Drive (`Anik & Mahajub`).
- **Restricted linkage:** `03_Datasets/manifests/DS0003_restricted_linkage.csv` (`.gitignore`-excluded).

## hashes

- **Archive (`c4hhrkxytw-4.zip`):** `206,222,368` bytes (`~196.67 MiB`), `md5:6213283c6de1063a07858470443b84ca`, `sha256:f11eaa3379ffe221adb74f141a5dcd0f8748f00a3d52cbbe462699cc75da7726`.
- **Public manifest (`DS0003_images.csv`):** `sha256:abdc75c9198840331d802f5a0e2d178e9d2944ef8e188b20ac081858a035edec`.
