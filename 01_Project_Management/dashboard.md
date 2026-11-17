# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S06 (**STEP-013 Batch 1 Quality & Forensic Audit complete (`DS0001, DS0003, DS0005, DS0006`: `3,110` active OPGs)**: `DS0001` label-index proved + `42` `train-valid` SHA dups + `18` re-encoded dups; `DS0005` `6` `train-val` re-encoded dups; `DS0003` film re-shoot/EXIF/`231 vs 232` solved; `DS0006` `66%` black padding caught; **Batch 2 `DS0004 + DS0002` downloading (`task-2333`)**) |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **NOT ASSESSED** | **`STEP-013` Batch 1 forensic quality reports (`DS0001, DS0003, DS0005, DS0006` `*_quality.md`) complete** (`0` cross-cohort matches); awaiting Batch 2 (`DS0004 + DS0002`) download/audit + team/dental visual suitability review |
| G05–G17 | STEP-015–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Complete **`STEP-012/013` Batch 2 (`task-2333`)**: Finish `DS0004 Do 2024` (`8.30 GiB`) + `DS0002 DENTEX` (`10.32 GiB`) download, hash inventory (`DS0002_images.csv`, `DS0004_images.csv`), quality audits (`DS0002_quality.md`, `DS0004_quality.md`), cards, and full **`G04` assessment** (after dental/human review).
2. Prepare **`STEP-014` (`UD04/UD06` dental reviewer)**: Arrange qualified dental reviewer confirmation for target visibility/suitability (`G04` -> `G05`).
3. Keep off-Git backups synced to **Private Google Drive** (`Anik & Mahajub`); retain confirmation screenshots (`G01`, `G03`, `UD03 v6`) in `01_Project_Management/meetings/`.
4. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0003`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
