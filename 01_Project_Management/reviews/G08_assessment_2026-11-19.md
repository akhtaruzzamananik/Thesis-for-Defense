# G08 assessment — Preprocessing and prepared dataset release integrity (`STEP-019` & `STEP-021`)

| Metadata | Value |
|---|---|
| TemplateID | T21 |
| template_version | v1.0.0 |
| entity_id | GA0008 (`G08` in `01_Project_Management/gates.csv`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward & Preprocessing Lead) & Mahajub Al Shabah (`232-15-900`, Model & Leakage Reviewer) |
| reviewer | Mahajub Al Shabah, Ms Faiza Feroz (Supervisor) & Clinical/Dental Review Team |
| date | 2026-11-19 |
| status | **`PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/releases.csv` (`REL0001–REL0006`); `05_Preprocessing/preprocessing_registry.csv` (`PP0001–PP0004`); `05_Preprocessing/specs/pipeline.md`; `05_Preprocessing/reports/PP0001.md`–`PP0004.md`; `05_Preprocessing/reports/releases_STEP-021_summary.json`; `src/opg/preprocessing.py`; `tests/test_preprocessing.py`; `13_Automation/materialize_releases_step021.py`; `DEC0009.md` |
| governing_section | OS §4.3, §4.5, §13.1–13.2; Blueprint STEP-019, STEP-021 |
| sensitivity | Public gate audit record (off-Git prepared labels, ledgers & visual QA sheets reside in `05_Preprocessing/processed/REL0001–REL0006/`) |

---

## Gate/entity versions

- **Gate:** `G08` (`GA0008` — *Preprocessing/release integrity*, `STEP-021`)
- **Entity versions assessed:**
  - `REL0001 v1.0.0` (`DS0001 v1.1.0` + `ANN0001 v1.0.0` + `SPLIT0001 v1.0.0` + `PP0001 v1.0.0`, `manifest sha256:40d7db1d4a9a2d87d9d689a16dc784a01a79f6a4df6f84b29f66241990d0ef9c`)
  - `REL0002 v1.0.0` (`DS0002 v1.0.0` + `ANN0002 v1.0.0` + `SPLIT0002 v1.0.0` + `PP0001 v1.0.0`, `manifest sha256:b187d514402a3145ae136127278c125ca563e2d329cdee0bdedd214268ddd8a7`)
  - `REL0003 v1.0.0` (`DS0003 v1.1.0` + `ANN0003 v1.0.0` + `SPLIT0003 v1.0.0` + `PP0001 v1.0.0`, `manifest sha256:5ffe497a21f6ec0a27e04371fa3b8bcb027f5fee224228c64e646c00aee28bb6`)
  - `REL0004 v1.0.0` (`DS0004 v1.0.0` + `ANN0004 v1.0.0` + `SPLIT0004 v1.0.0` + `PP0001 v1.0.0`, `manifest sha256:570f33b421ad415c94055a244ea60b5e9e7afbbe789dec08fc98d1e4e3b08e57`)
  - `REL0005 v1.0.0` (`DS0005 v1.1.0` + `ANN0005 v1.0.0` + `SPLIT0005 v1.0.0` + `PP0001 v1.0.0`, `manifest sha256:1642e409741a5d102a4b0bc8afa45fe2ac6b47ea2ec96794d1b40555a8a35975`)
  - `REL0006 v1.0.0` (`DS0006 v1.1.0` + `ANN0006 v1.0.0` + `SPLIT0006 v1.0.0` + `PP0001 v1.0.0`, `manifest sha256:721126e42e302903d5b9970d3a6c1bc14ccbcafba218fff93d29d10d174cce8f`)
  - `PP0001–PP0004 v1.0.0` (`05_Preprocessing/preprocessing_registry.csv`) & `DEC0009.md` (`UD09`)

---

## each criterion & evidence/hash

| Mandatory Criterion (`OS §13.2` & `STEP-021` Checklist) | Evidence Path & Verified Hash / Record | PASS/FAIL | Corrective Action / Downstream Rule |
|---|---|---|---|
| **1. Raw files unchanged & training-only fitted state (`STEP-021` Checklist #1)** | `05_Preprocessing/reports/releases_STEP-021_summary.json`; `05_Preprocessing/processed/REL0001–REL0006/fit_state_train_only.json`. Every raw `SHA-256` in `DS0001–DS0006_images.csv` verified unchanged; all fitted intensity statistics computed **exclusively** on the `5,106` canonical `train` images (`val_or_test_accessed_for_fit = False`, enforced by `fit_training_statistics` leakage guard). | **PASS** | Enforce `fit_state_train_only_sha256` check in downstream model loaders (`STEP-025`). |
| **2. Coordinate round-trip geometry & target visibility verified (`STEP-021` Checklist #2)** | `05_Preprocessing/reports/PP0001.md`–`PP0004.md`; `05_Preprocessing/processed/REL0001–REL0006/transform_ledger.csv`; `tests/test_preprocessing.py`. Across all `41,103` canonical boxes (`7,457` OPGs), **`0` boxes were dropped or collapsed**, and maximum pixel round-trip error (`raw -> forward letterbox -> YOLO 6-dec -> pixel -> inverse letterbox -> raw`) is **`0.003630 px` at `640×640`** (`PP0001–0003`) and **`0.004068 px` at `1280×1280`** (`PP0004`), well below `< 0.05 px`. Visual QA sheets (`REL0001–0006_pp_comparison_sheet.jpg`, `train/val` only) confirm tight box alignment and clean `DS0006` black-border stripping. | **PASS** | Use `transform_ledger.csv` for inverse mapping of model predictions back to source radiograph coordinates (`STEP-025` / `STEP-037`). |
| **3. Augmentation isolation & release count/hash reconciliation (`STEP-021` Checklist #3–4)** | `03_Datasets/releases.csv` (`REL0001–REL0006`); `05_Preprocessing/specs/pipeline.md` (`§4`). Stochastic augmentation restricted strictly to online `train` (`apply_to_val_or_test = false`). Every release binds exact parent `DatasetManifestSHA256`, `AnnotationExportSHA256`, `ClassMapSHA256` (`c3f91dfc8a...`), `SplitManifestSHA256`, and `PPConfigSHA256`, reconciling `7,457` canonical OPGs (`5,106 train / 1,091 val / 1,082 test / 178 external_test`) and `41,103` canonical boxes (`26,672 train / 5,722 val / 5,784 test / 2,925 external_test`). | **PASS** | Unlocks **`S10` (`STEP-022`–`026`: YOLO implementation selection, runtime environment lock, evaluation protocol & baseline smoke test `G09`)**. |

---

## PASS/FAIL

**`PASS` (`2026-11-19`)**

## missing items

None. All `OS §13.2` `G08` mandatory criteria and `STEP-021` verification checklist items are complete and verified on disk.

## owner/fix

- **Owners:** Akhtaruzzaman Anik (`Data Steward & Preprocessing Lead`) & Mahajub Al Shabah (`Model & Evaluation Lead`).
- **Next Action:** Proceed to **`S10 / STEP-022`** (*Select the YOLO implementation and baseline candidate*).

## assessor/date

- **Assessor:** Akhtaruzzaman Anik & Mahajub Al Shabah (verified via `13_Automation/materialize_releases_step021.py` & `pytest`)
- **Date:** `2026-11-19`

## human approval

- **Approved (`2026-11-19`):** Akhtaruzzaman Anik (Preprocessing Lead), Mahajub Al Shabah (Model Lead), and Ms Faiza Feroz (Supervisor) / Dental Review Team (`2026-11-19`).

## invalidated descendants

None (`G01–G07` remain `PASS`; `G09–G17` are `NOT ASSESSED`).
