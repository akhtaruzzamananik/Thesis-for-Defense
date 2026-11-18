# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-19 |
| Current stage / step | **S08 Complete (`STEP-018` / `G06 = PASS` closed: `ANN0001–ANN0006` frozen across `7,738` canonical `.txt` files, `44,241` valid boxes, `0` orphans/invalid/duplicates)**; ready for **`S09` (`STEP-019`–`021`: Preprocessing, Leakage-Safe Split & Prepared Release `REL`)** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **PASS** | **Approved (`2026-11-18`):** All `6` cohorts (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined, `0` cross-cohort overlaps) & non-merged `Tracks A–F` approved (`DEC0002.md`, `G04_assessment_2026-11-18.md`) |
| G05 | STEP-015 | **PASS** | **Approved (`2026-11-19`):** Ontology `CLS0001–CLS0041` (`sha256:c3f91dfc...`), canonical YOLO `AABB` export contract (`< 0.002 px` round-trip error across all `6` datasets), and prospective `60`-OPG pilot / `240`-OPG batch QA thresholds frozen (`DEC0004–0006`, `G05_assessment_2026-11-19.md`) |
| G06 | STEP-018 | **PASS** | **Approved (`2026-11-19`):** Pilot (`60` OPGs) & production batches (`ANNB0001–0006`, `240` visual QA OPGs) accepted; **`ANN0001–ANN0006`** frozen (`7,738` `.txt` files, `44,241` valid boxes, `180` excluded/deduplicated, `0` orphans/invalid, `G06_assessment_2026-11-19.md`) |
| G07–G08 | STEP-020–021 | **NOT ASSESSED** | Ready to start **`S09` (`STEP-019` Preprocessing Design, `STEP-020` Leakage-Safe Split `G07`, `STEP-021` Prepared Release `REL` `G08`)** |
| G09–G17 | STEP-026–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-019` (`S09` — Design preprocessing and coordinate-preserving transforms)**:
   - Draft `05_Preprocessing/specs/pipeline.md`, proposed `05_Preprocessing/configs/` (`Raw` unenhanced baseline vs parameterized `CLAHE` vs resolution/tiling & `DS0006` black-margin autocrop under `RQ2` / `UD09`), and implement coordinate-preserving forward/inverse transform & box-geometry tests in `src/opg/preprocessing.py` + `tests/test_preprocessing.py` (keeping split-dependent fitting blocked until `STEP-020 / G07`).
2. Execute **`STEP-020` (`G07` Leakage-Safe Split)** & **`STEP-021` (`G08` Materialize Prepared Dataset `REL0001–REL0006`)**.
3. Maintain Private Google Drive sync (`03_Datasets/raw/DS0001–DS0006` + `*_restricted*` per `DEC0011`).
4. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001–DEC0006`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved)
- Gates: `01_Project_Management/gates.csv` (`G01–G06 PASS`; `G07–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
