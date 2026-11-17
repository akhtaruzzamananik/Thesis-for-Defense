# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S04 complete (**STEP-009 closed — `G03 PASS`** on `2026-11-17`: `research_questions.md` `v1.0.0`, `DEC0019` resolved Option 1, `gaps.csv` `v1.2.0`, `claims.csv` `v1.2.0`); ready for **STEP-010 (`S05`)** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04–G17 | STEP-013–049 | **NOT ASSESSED** | Not started (`STEP-010` candidate dataset audit now unlocked) |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-010` (`S05`)**: Compare candidate public `2D OPG` datasets (`DENTEX`, `UMFIH`, `Rahman 2024 Dhaka`, deduplicated `Do 2024`, `MD-OPG`, `AU-OPG`, `Tufts`) on provenance, licenses (`UD03`), grouping/duplicates (`UD07`), and `RQ0–RQ3` fit inside `03_Datasets/candidates.csv`.
2. Retain Telegram/confirmation screenshots for `G01`/`G03` in `01_Project_Management/meetings/`; track `UD21` (defense web demo confirmation & expected defense date) and identify qualified dental reviewer (`UD04/UD06` before `STEP-014`).
3. Maintain strict `STEP-011` gate rule: do **not** download/redistribute restricted data until license/ethics checks clear.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001` & `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
