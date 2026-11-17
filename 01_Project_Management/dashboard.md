# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S04 (**STEP-009 technical audit & RQ map complete**: `research_questions.md` `v0.9.0`, `DEC0019.md`, `gaps.csv` `v1.1.0`, `claims.csv` `v1.1.0`, `G03_assessment_2026-11-17.md`, `STEP-009_supervisor_brief.md`); **awaiting Supervisor `G03` & `UD19` sign-off** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **NOT ASSESSED** | **STEP-009 technical audit & Supervisor brief complete** (`research_questions.md` `v0.9.0` [`RQ0–RQ3`], `DEC0019.md` [`0` unverified `[1]–[13]` used], `gaps.csv` `v1.1.0`, `claims.csv` `v1.1.0`, `G03_assessment_2026-11-17.md`); awaiting Supervisor Ms Faiza Feroz & Mahajub `UD19` sign-off |
| G04–G17 | STEP-013–049 | **NOT ASSESSED** | Not started (`G04` final dataset selection gated on `G03 PASS`) |

## 2. Immediate priorities & open blockers

1. **Human Sign-Off (`STEP-009 / G03`):** Present `01_Project_Management/meetings/STEP-009_supervisor_brief.md` to Supervisor Ms Faiza Feroz (`RQ0–RQ3` bounded contribution limits & `G03 PASS` authorization) and Literature Lead Mahajub Al Shabah (`DEC0019 / UD19` Option 1 exclusion of deleted report `[1]–[13]` or external supply).
2. Confirm `UD21` (defense web demo confirmation & expected defense date) and identify qualified dental reviewer (`UD04/UD06` before `STEP-014`).
3. Upon **`G03 PASS`**, initiate **`S05` (`STEP-010`)**: inspect candidate public 2D OPG benchmarks (`DENTEX`, `UMFIH`, `Rahman 2024 Dhaka`, deduplicated `Do 2024`, `MD-OPG`, `AU-OPG`, `Tufts`), enforce pre-split deduplication, and verify licenses/splits.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0011`, `DEC0019`, `DEC0021` logged)
- Gates: `01_Project_Management/gates.csv` (`G01–G02 PASS`; `G03` pre-assessed `NOT ASSESSED`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
