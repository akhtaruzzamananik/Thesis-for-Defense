# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S05 (**STEP-012 Batch 1 complete (`4/6` acquired & inventoried off-Git)**: `DS0001 UMFIH` [`1,808` active / `1,611` unique SHA-256], `DS0003 Dhaka` [`231` active], `DS0005 AU-OPG` [`901` active], `DS0006 MD-OPG` [`170` active]; **Batch 2 `DS0004` + `DS0002` downloading**; **0 datasets on GitHub**) |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **NOT ASSESSED** | **`STEP-012` Batch 1 complete (`DS0001, DS0003, DS0005, DS0006` in `datasets.csv`, `3,110` active raw OPGs)** — caught `197` exact byte dups (`42` train-valid leaks) + label-order diff in `DS0001`; **`DS0004 + DS0002`** downloading cleanly before full `STEP-013 / G04` |
| G05–G17 | STEP-015–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Complete **`STEP-012` Batch 2**: Finish `DS0004 Do 2024` (`8.30 GiB`) + `DS0002 DENTEX` (`10.32 GiB`) off-Git download & inventory (`03_Datasets/raw/DS0004`, `DS0002`), complete `DS0002_card.md`, `DS0004_card.md`, `acquisition_report_STEP-012.md`, and back up `raw/` to Private Google Drive (`DEC0011`).
2. Prepare **`STEP-013` (`G04`)**: Reconcile `DS0001` `197` exact byte duplicates & `legend.txt` vs `labels (1).txt` order, `DS0003` `231` vs `232` hash diff, `DS0005` `134` unannotated extras, EXIF/border PHI checks, and arrange dental quality review (`UD04/UD06`).
3. Retain confirmation screenshots (`G01`, `G03`, `UD03 v6`) in `01_Project_Management/meetings/`; confirm `UD21` (defense web demo).
4. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0003`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
