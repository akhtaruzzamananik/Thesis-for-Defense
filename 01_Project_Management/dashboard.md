# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-17 |
| Current stage / step | S03 (**STEP-008** complete: `42` Core synthesized in `synthesis.md`, `G1–G6` tested in `gap_notes/GAP0001–0006.md` & `gaps.csv`, `12` trace claims in `claims.csv`); moving to **STEP-009** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **NOT ASSESSED** | **STEP-005–008 complete** (`122` screened, `42` Core extracted, `synthesis.md`, `gaps.csv` [`G1=refuted`, `G2–G6=narrowed`], `claims.csv` [`12` trace claims]); **STEP-009** (`RF14` `[1]–[13]`, final RQs, Supervisor `G03` sign-off) next |
| G04–G17 | STEP-013–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **STEP-009**: Verify `RF14` `[1]–[13]` (`UD19` / `DEC0019`), finalize gap-derived RQs in `02_Literature/research_questions.md` (linking `ApprovedRQ` in `gaps.csv` / `gap_notes/`), and submit **G03** for Supervisor sign-off.
2. Confirm `UD21` (defense web demo confirmation & expected defense date) with supervisor when scheduling allows.
3. Upon **G03 PASS**, initiate **`S04` (`STEP-010`)**: inspect candidate public 2D OPG benchmarks (`DENTEX`, `UMFIH`, `Rahman 2024 Dhaka`, deduplicated `Do 2024`, `MD-OPG`, `AU-OPG`, `Tufts`), enforce pre-split deduplication, and verify licenses/splits.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0011`, `DEC0021` logged)
- Gates: `01_Project_Management/gates.csv` (`G01–G17` initialized `NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
