# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S03 complete (**STEP-007** closed: `42/42` Core extracted; `Group A = 23`, `Group B = 19`; CSV schema + row-width QA fixed); moving to **STEP-008** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **NOT ASSESSED** | `STEP-005`–`007` complete (`122` unique screened, `42` Core extracted in `02_Literature/summaries/P0001.md`–`P0042.md`); `STEP-008`–`009` in progress |
| G04–G17 | STEP-013–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **STEP-008**: Test `G1–G6` across the `42` Core `T05` summaries (`23` Group A direct OPG detectors + `19` Group B contextual studies) + `55` Reserve records (`P0043`–`P0097`), author `02_Literature/gap_notes/GAP0001.md`–`GAP0006.md`, `gaps.csv`, `synthesis.md`, and `claims.csv`.
2. Execute **STEP-009**: Verify `RF14` `[1]–[13]` (`UD19` / `DEC0019`), finalize `research_questions.md`, and submit `G03` for Supervisor sign-off.
3. Confirm `UD21` (defense web demo confirmation & expected defense date) with supervisor when scheduling allows.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0011`, `DEC0021` logged)
- Gates: `01_Project_Management/gates.csv` (`G01–G17` initialized `NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
