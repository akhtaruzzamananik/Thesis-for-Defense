# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S05 (**STEP-011 technical & license audit complete**: `03_Datasets/licenses/*.md`, `access_decision.md`, `DEC0003.md`, `.gitignore` hardened; **zero raw datasets downloaded or pushed**); awaiting human **`DEC0003` (`UD03`)** confirmation before `STEP-012` intake |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **NOT ASSESSED** | **`STEP-010`–`011` technical audits complete** (`CAND0001` `1.30 GiB CC BY 4.0`, `CAND0002` `10.32 GiB CC BY 4.0 / NC-SA`, `CAND0003` `197 MB CC BY 4.0 / BY-NC`; `CAND0004–0014` blocked); **awaiting `DEC0003` (`UD03`) human determination before `STEP-012` download** |
| G05–G17 | STEP-015–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. **Human Decision (`STEP-011`, `UD03` / `DEC0003`):** Confirm DIU secondary-research determination + Option 1 (`CAND0001 UMFIH + CAND0003 Rahman Dhaka`, `~1.5 GiB`) vs Option 2 (`+ CAND0002 DENTEX`, `~11.8 GiB`) before downloading raw archives cleanly to **off-Git** `03_Datasets/raw/` + Private Google Drive (`DEC0011`).
2. Retain Telegram/confirmation screenshots for `G01`/`G03` in `01_Project_Management/meetings/`; track `UD21` (defense web demo confirmation & expected defense date) and identify qualified dental reviewer (`UD04/UD06` before `STEP-014`).
3. Maintain strict custody: raw images & `.zip` archives never enter Git (`git ls-files "*.pdf"`, `"*.zip"` must remain empty).

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001` & `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0003` & `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
