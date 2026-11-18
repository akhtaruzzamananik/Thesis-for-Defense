# G04 assessment — Dataset access, relevance, and quality (`STEP-010`–`STEP-013`)

| Metadata | Value |
|---|---|
| TemplateID | T21 |
| template_version | v1.0.0 |
| entity_id | GA0004 (`G04` in `01_Project_Management/gates.csv`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward & Research Lead) |
| reviewer | Mahajub Al Shabah (`232-15-900`) & Ms Faiza Feroz (Supervisor) |
| date | 2026-11-18 |
| status | **`PASS` (`2026-11-18`)** |
| source_inputs | `DEC0002.md`; `DEC0003.md v6`; `03_Datasets/datasets.csv`; `03_Datasets/reports/acquisition_report_STEP-012.md`; `03_Datasets/reports/DS0001–DS0006_card.md`; `03_Datasets/reports/DS0001–DS0006_quality.md`; `03_Datasets/manifests/DS0001–DS0006_qc_summary.json`; `03_Datasets/manifests/cross_dataset_dup_summary.json`; `01_Project_Management/meetings/G04_dataset_suitability_brief.md` |
| governing_section | OS §4.1–4.2, §13.1–13.2; Blueprint STEP-013 |
| sensitivity | Public gate audit record (raw images & restricted linkage/QC maps remain off-Git) |

---

## Gate/entity versions

- **Gate:** `G04` (`GA0004` — *Dataset access/relevance/quality*, `STEP-013`)
- **Entity versions assessed:**
  - `DEC0003.md` (`v6`, `2026-11-17`) & `DEC0002.md` (`v3`, `2026-11-18`)
  - `03_Datasets/datasets.csv` (`DS0001 v1.1.0`, `DS0002 v1.0.0`, `DS0003 v1.1.0`, `DS0004 v1.0.0`, `DS0005 v1.1.0`, `DS0006 v1.1.0`)
  - `03_Datasets/manifests/DS0001_images.csv`–`DS0006_images.csv` (immutable SHA-256 manifests)
  - `03_Datasets/reports/DS0001_card.md`–`DS0006_card.md` & `DS0001_quality.md`–`DS0006_quality.md`
  - Intake & QC tooling: `src/opg/dataset_intake.py`, `src/opg/dataset_qc.py`, `tests/test_dataset_intake.py`, `tests/test_dataset_qc.py` (`8 passed`)

---

## each criterion & evidence/hash

| Mandatory Criterion (`OS §13.2` & `STEP-013` Checklist) | Evidence Path & Verified Hash / Record | PASS/FAIL | Corrective Action / Downstream Binding Rule |
|---|---|---|---|
| **1. Permissions, license & ethics determination (`UD03`)** | `01_Project_Management/decision_log/DEC0003.md` (`v6`, `2026-11-17`); `03_Datasets/licenses/CAND0001–0005,0007*.md`; `03_Datasets/reports/access_decision.md`. Open academic licenses (`CC BY 4.0`, `CC BY-NC 4.0`, `CC-BY-NC-SA-4.0`, `MIT`) and source ethics (`MK-198109`, `D-F-H-6-Mar`, `IR.ZUMS.REC.1404.242`, `UMFIH`, `DENTEX`, `Hanoi`) verified. | **PASS** | Keep `DS0002 DENTEX` (`CC-BY-NC-SA-4.0`) derivatives isolated from pure `CC BY 4.0` tracks. |
| **2. Provenance & immutable archive/manifest hashes (`STEP-012`)** | `03_Datasets/reports/acquisition_report_STEP-012.md`; `03_Datasets/datasets.csv` manifest SHA-256 hashes: `DS0001` (`4f75c64e...`), `DS0002` (`fb268930...`), `DS0003` (`abdc75c9...`), `DS0004` (`b05ad87b...`), `DS0005` (`5a23a5cd...`), `DS0006` (`18678b82...`). Raw files untouched in `03_Datasets/raw/DS0001–DS0006/`. | **PASS** | Sync `03_Datasets/raw/` + `*_restricted*` to Private Google Drive (`DEC0011`) alongside local PC storage. |
| **3. Measured inventory & count reconciliation (`acquired = retained + quarantined`)** | `25,355` total image files scanned across `6` cohorts = **`7,789` active OPGs** (`1,808 + 755 + 231 + 3,924 + 901 + 170`) + **`17,566` quarantined** (`2,899 DS0002` + `1,121 DS0003` + `13,071 DS0004` + `135 DS0005` + `340 DS0006`) + **`0` decode errors**. Every discrepancy vs published papers (`DS0002` `14:1` class skew; `DS0003` `231` vs `232`; `DS0004` `59+2` intra-original duplicates; `DS0005` `6` `train<->val` leaks) reconciled. | **PASS** | Never train on `17,566` quarantined files; collapse `~279` exact/re-encoded duplicate copies into grouped clusters at `STEP-020 / G07`. |
| **4. Image quality, decoding, orientation & burned-in privacy check (`STEP-013`)** | `03_Datasets/reports/DS0001_quality.md`–`DS0006_quality.md`; off-Git `03_Datasets/raw/qc_samples/DS0001–DS0006_qc_sheet.jpg` & `dup_pair_verification.jpg`. `0` corrupted images; `DS0001` `1 RGBA` (`v60.png`) & `DS0005` `17 RGBA` flagged for deterministic `RGB` conversion; `DS0002_IMG_000641` sensor band documented; `DS0003` `30` EXIF/XMP headers + `"PRESCRIPTION POINT"` corner logo flagged for stripping/masking; `DS0006` `66.17%` black letterbox border documented. | **PASS** | Strip EXIF/XMP (`DS0003`), mask clinic corner logos before any thesis figure or `S16` web demo (`UD23`), and apply border-aware preprocessing (`UD09`). |
| **5. Exact & perceptual duplicate screening (intra- and cross-cohort)** | `03_Datasets/manifests/cross_dataset_dup_summary.json` (`0` cross-cohort overlaps across all `6` datasets; max cross pixel correlation `= 0.7793`). Intra-cohort exact SHA-256 and `dHash <= 4` + pixel correlation `>= 0.99` audits completed for all `6` cohorts. | **PASS** | Feed restricted duplicate graphs directly into `STEP-020` (`UD07/UD08` leakage-safe split). |
| **6. Approved dataset selection & track isolation (`UD02` / `DEC0002`)** | `01_Project_Management/decision_log/DEC0002.md` (`v3`, `2026-11-18`) and `01_Project_Management/meetings/G04_dataset_suitability_brief.md` (`Tracks A–F` non-merged architecture). | **PASS** | Proceed to `STEP-014` (`UD04` class ontology definition) and `STEP-015` (`G05` dental reviewer protocol approval). |

---

## PASS/FAIL

**`PASS` (`2026-11-18`)**

## missing items

None for `G04`. *(Note: Formal dental reviewer sign-off on the final trainable class ontology `UD04`, coordinate schema `UD05`, and QA thresholds `UD06` is the explicit purpose of **`G05` (`STEP-014`–`STEP-015`)**, which is now unlocked.)*

## owner/fix

- **Owner:** Akhtaruzzaman Anik (`232-15-252`, Data Steward) & Mahajub Al Shabah (`232-15-900`, Annotation/Model Lead).
- **Ongoing custody action:** Maintain off-Git Private Google Drive mirror of `03_Datasets/raw/DS0001–DS0006/` and `03_Datasets/manifests/*_restricted*` per `DEC0011`.

## assessor/date

- **Assessor:** Akhtaruzzaman Anik & Mahajub Al Shabah (supported by automated `dataset_intake.py` & `dataset_qc.py` verification)
- **Date:** `2026-11-18`

## human approval

- **Approved (`2026-11-18`):** Akhtaruzzaman Anik (Data Steward & Research Lead), Mahajub Al Shabah (Co-researcher), and Ms Faiza Feroz (Supervisor) — confirmed following review of `01_Project_Management/meetings/G04_dataset_suitability_brief.md` (`2026-11-18`).

## invalidated descendants

None (`G01`, `G02`, `G03` remain `PASS`; `G05–G17` were `NOT ASSESSED`).
