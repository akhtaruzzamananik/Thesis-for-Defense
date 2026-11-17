# T08 — Dataset Card: `DS0001` (`CAND0001` — UMFIH Dental Pathology + Multi-Center External)

| Metadata | Value |
|---|---|
| TemplateID | T08 |
| template_version | v1.0.0 |
| entity_id | DS0001 |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-17 |
| status | Technical Quality Audited (`STEP-013` Batch 1 complete; `G04` review awaiting Batch 2 & dental check) |
| source_inputs | `https://zenodo.org/records/15487430` (`doi:10.5281/zenodo.15487429`); `03_Datasets/licenses/CAND0001_UMFIH_CC-BY-4.0.md`; `03_Datasets/manifests/DS0001_images.csv`; `03_Datasets/reports/DS0001_quality.md` |
| governing_section | OS §4.1–4.2; Blueprint STEP-012 |
| sensitivity | Public metadata card (`raw/` & `DS0001_restricted_linkage.csv` strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`) |

## Origin/version

- **Archive:** `panoramic_radiography_yolo_dataset_14_classes.zip` (`Zenodo record 15487430`, published `2025-05-22`, Concept DOI `10.5281/zenodo.15487429`).
- **Accompanying papers:** Mureșanu et al. (2024, `P0023`), Eftimie et al. (2025, `P0015`).

## access/license/ethics

- **Permission record:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`, `2026-11-17`).
- **License:** **`CC BY 4.0`** (`Creative Commons Attribution 4.0 International`).
- **Ethics:** Retrospective de-identified clinical collection from UMFIH Cluj-Napoca (`2021–2023`, `P0023 pp. 2, 10`) + external multi-center clinics; DIU secondary-research track confirmation recorded in `DEC0003`.

## modality

- `2D OPG` (panoramic dental radiographs; Vatech `PCH-2500` internal + external clinical centers).

## population known/unknown

- Adult clinical dental patients (`UMFIH Cluj-Napoca, Romania` + multi-center external clinics); age/sex per-image distributions `not reported` at file level.

## collection

- Pre-partitioned archive structure observed upon extraction (`2026-11-17`):
  - `internal_train`: `1,375` images
  - `internal_valid`: `153` images
  - `internal_test`: `100` images (`1,628` internal total)
  - `external_validation` (`test_alte_cabinete`): `180` images (`180` external total)
- **Formats decoded (`STEP-012`):** `1,807` `.jpg` (`RGB`) + `1` `.png` (`RGBA`, inside `internal_test`), **`0` decode errors**.

## patient/image/object counts

- **Total scanned / active raw images:** **`1,808`** (`1,808` active + `0` quarantined + `0` errors).
- **Unique SHA-256 hashes:** **`1,611`** (`187` duplicate SHA-256 groups accounting for **`197` exact byte-for-byte duplicate files**).
- **Patient count:** Unknown (`patient IDs not reported` in public archive).
- **Object / label inspection:** Deferred to `STEP-013` *(archive includes `1,808` per-image `.txt` files + `legend.txt` [`14` classes `0–13`] + `labels (1).txt` [`13` classes; critical index-order divergence flagged for `STEP-013`!])*.

## quality/exclusions

- Audited in `03_Datasets/reports/DS0001_quality.md`: `0` decode errors (`804–5538` px wide, `0` aspect outliers, median Laplacian `1,210.25`), `0` sensitive EXIF tags, Vatech bottom exposure footers + `1 RGBA` PNG (`v60.png`), `3` zero-area boxes, and `Class 11` (`5` boxes total) flagged for `UD04` exclusion. Empirically verified `external_validation` uses `legend.txt` (`0–13`).

## duplicates/grouping

- Audited in `DS0001_quality.md` (`DS0001_restricted_dups.csv`): `197` exact SHA-256 duplicates (**`42` leaking `train <-> valid` = `27.5%` of `valid`**) PLUS **`18` re-encoded exact visual pairs (`corr >= 0.99`)** and `2` pairs at `0.95–0.99`. Zero true cross-cohort matches against `DS0003/0005/0006`. Pre-supplied splits **MUST** be replaced (`G07`).

## annotations

- **Label files detected:** YOLO normalized `.txt` files plus conflicting root `legend.txt` (`14` entries `0–13`, includes `Root resorption`) vs `test_alte_cabinete/labels (1).txt` (`13` entries, different class ordering for `obturation`/`prosthetic restoration` and `impacted tooth`/`bone resorption`). Must be reconciled empirically in `STEP-013` and `UD04–UD05` before any modeling.

## biases

- Contains metal/orthodontic artifacts (`P0023`); exact byte duplicates inside `internal_train/valid`; diffuse `Bone resorbtion` and rare `Furcation`/`Apical surgery` classes flagged in literature (`GAP0003`).

## intended use

- Primary adult multi-class `2D OPG` benchmark cohort (`RQ0–RQ3`) after strict SHA-256 + near-duplicate cleaning, external label-index verification, and patient/image-safe grouped splitting (`UD07–UD08`).

## access/retention

- **Restricted storage:** `03_Datasets/raw/DS0001/` (`archive/` + `extracted/`, `.gitignore`-excluded) + Private Google Drive (`Anik & Mahajub`).
- **Restricted linkage:** `03_Datasets/manifests/DS0001_restricted_linkage.csv` (`.gitignore`-excluded).

## hashes

- **Archive (`panoramic_radiography_yolo_dataset_14_classes.zip`):** `1,397,393,531` bytes, `md5:18d5acaea021f4f3b05b76e9a27fbd42` (matches Zenodo API!), `sha256:cebc49f18944ad21951088d77f1ce83296c9336d6c1244ab1792b91db50b598a`.
- **Public manifest (`DS0001_images.csv`):** `sha256:4f75c64e9a295553a5c2753e73d0c39122e8274a94e2c883794b5c6b0cae6179`.
