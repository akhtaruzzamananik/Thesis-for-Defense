# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S05 (**STEP-010 complete**: `14` public `2D OPG` candidates audited in `candidates.csv` & `candidate_comparison.md`; `3`-dataset shortlist `CAND0001 UMFIH`, `CAND0002 DENTEX`, `CAND0003 Rahman 2024 Dhaka`; zero raw data downloaded); moving to **STEP-011** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **NOT ASSESSED** | **`STEP-010` complete** (`03_Datasets/candidates.csv`, `reports/candidate_comparison.md`); **`STEP-011`** (`UD03` license/ethics/custody check before any acquisition) next |
| G05–G17 | STEP-015–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-011` (`S05`, `UD03`)**: Resolve actual archive licenses, `ShareAlike`/`NC`/example-disclosure permissions, DIU ethics/waiver determination, and off-Git custody rules (`CAND0001 UMFIH`, `CAND0002 DENTEX`, `CAND0003 Rahman 2024 Dhaka`) in `03_Datasets/licenses/` and `reports/access_decision.md` **before downloading any images**.
2. Retain Telegram/confirmation screenshots for `G01`/`G03` in `01_Project_Management/meetings/`; track `UD21` (defense web demo confirmation & expected defense date) and identify qualified dental reviewer (`UD04/UD06` before `STEP-014`).
3. Maintain strict custody: raw images stay excluded from Git (`raw/` off-Git under `DEC0011`).

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001` & `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
