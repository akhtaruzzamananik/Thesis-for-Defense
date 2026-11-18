# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-18 |
| Current stage / step | **S07 (`STEP-013` / `G04 = PASS` closed; `STEP-014` Dental Object Ontology `CLS0001–CLS0041` complete)**; ready for **`STEP-015` (`G05` protocol, schema & QA threshold approval)** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **PASS** | **Approved (`2026-11-18`):** All `6` cohorts (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined, `0` cross-cohort overlaps) & non-merged `Tracks A–F` approved (`DEC0002.md`, `G04_assessment_2026-11-18.md`) |
| G05 | STEP-015 | **NOT ASSESSED** | **`STEP-014` ontology proposal complete (`04_Annotations/classes.csv` `CLS0001–CLS0041`, `protocols/class_definitions.md`, `DEC0004.md`)** — ready for `STEP-015` protocol freeze & `G05` sign-off (`STEP-014_UD04_ontology_brief.md`) |
| G06–G17 | STEP-018–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Complete **`STEP-015` (`G05` approval)**: Confirm `UD04–UD06` in `01_Project_Management/meetings/STEP-014_UD04_ontology_brief.md` (approve `CLS0001–CLS0041` ontology, normalized YOLO `AABB` export contract + round-trip converter, and stratified secondary-dataset pilot/batch QA thresholds) -> freeze `04_Annotations/protocols/annotation_protocol_v1.0.0.md` and assess `G05`.
2. Execute **`STEP-016`–`STEP-018` (`S08` / `G06`)**: Run the stratified pilot (`60` OPGs) and full batch integrity/conversion QA (`ANNB0001–ANNB0006` across `7,789` active OPGs) to freeze `ANN0001–ANN0006` (`G06 PASS`), unlocking **`STEP-019`–`021` (Preprocessing & Split)**.
3. Maintain Private Google Drive sync (`03_Datasets/raw/DS0001–DS0006` + `*_restricted*` per `DEC0011`) and retain confirmation screenshots in `01_Project_Management/meetings/`.
4. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001`, `DEC0002`, `DEC0003`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved, `DEC0004` STEP-014 draft complete)
- Gates: `01_Project_Management/gates.csv` (`G01–G04 PASS`; `G05–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
