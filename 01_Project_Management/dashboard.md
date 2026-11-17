# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S05 (**STEP-011 closed — `DEC0003 v6` 6-Dataset Portfolio authorized**: `CAND0001 UMFIH` + `CAND0002 DENTEX` + `CAND0003 Rahman Dhaka` + `CAND0004 Do2024` + `CAND0005 AU-OPG` + `CAND0007 MD-OPG` [`reported 2026-11-17`; `CAND0007` replaces unpublished `CAND0006 OPG-233`]; **0 datasets on GitHub**); ready for **STEP-012** (`off-Git raw/` download + SHA-256 inventory) |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **NOT ASSESSED** | **`STEP-010`–`011` complete (`DEC0003 v6` 6-dataset clearance `2026-11-17`)** — `CAND0001–0005` + `CAND0007` cleared for off-Git non-merged intake (`CAND0006` unpublished placeholder + `CAND0008–0014` blocked); **`STEP-012`** next before `STEP-013 / G04` |
| G05–G17 | STEP-015–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-012` (`S05`)**: Download the `6` authorized cohorts (`CAND0001 UMFIH`, `CAND0002 DENTEX`, `CAND0003 Rahman Dhaka`, `CAND0004 Do2024`, `CAND0005 AU-OPG`, `CAND0007 MD-OPG`) strictly to **off-Git** `03_Datasets/raw/DS####/` + Private Google Drive backup (`DEC0011`), verify MD5/SHA-256 checksums, isolate pre-aug duplicates (`CAND0003`, `CAND0004`), and build deterministic non-identifying manifests in `03_Datasets/manifests/` (**never push raw images or `.zip`/`.rar`s to GitHub**).
2. Retain confirmation screenshots (`G01`, `G03`, `UD03`) in `01_Project_Management/meetings/`; confirm `UD21` (defense web demo) & identify qualified dental reviewer (`UD04/UD06` before `STEP-014`).
3. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0003`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
