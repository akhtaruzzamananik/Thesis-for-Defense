# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-18 |
| Current stage / step | S06 (**STEP-012 & STEP-013 Technical Audit COMPLETE across ALL `6` cohorts (`25,355` files scanned -> `7,789` active OPGs, `17,566` quarantined, `0` errors, `0` cross-cohort matches)**; awaiting **Human/Dental `G04` Sign-Off + Private Drive Backup**; **0 images/archives in Git**) |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **NOT ASSESSED** | **All `6` cohorts acquired & quality-audited (`DS0001–DS0006`, `acquisition_report_STEP-012.md`, `DS####_quality.md`)** — ready for **`G04` review & sign-off** (`G04_dataset_suitability_brief.md` + dental visual review + Private Drive backup) |
| G05–G17 | STEP-015–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Complete **`G04` (`STEP-013` closeout)**: Researchers (`Anik & Mahajub`), Supervisor (`Ms Faiza Feroz`), and dental reviewer complete `G04_dataset_suitability_brief.md` (approving non-merged `6`-track exclusions, duplicate removals, privacy stripping & dental target feasibility) + sync `03_Datasets/raw/DS0001–DS0006` + `*_restricted*` to **Private Google Drive** (`DEC0011`) -> record `G04 PASS`.
2. Proceed upon `G04 PASS` to **`STEP-014` (`S07`)**: Lock visible object ontology (`UD04–UD06` with dental reviewer), starting from reconciled schemas (`DS0001` `0–13` minus `Class 11`, `DS0002` `4` imbalanced diseases, `DS0003` whole-tooth boxes, `DS0004` `PAI 3–5`, `DS0005` `OBB`, `DS0006` pediatric caries).
3. Retain confirmation screenshots (`G01`, `G03`, `UD03 v6`, `G04`) in `01_Project_Management/meetings/`; confirm `UD21` (defense web demo).
4. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0003`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0021` open)
- Gates: `01_Project_Management/gates.csv` (`G01–G03 PASS`; `G04–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
