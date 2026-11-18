# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-19 |
| Current stage / step | **S08 (`STEP-016` Pilot & `STEP-017` Production Batches `ANNB0001–ANNB0006` COMPLETE: `7,738` canonical `.txt` exports, `44,241` valid boxes, `180` excluded/deduplicated, `240` visual QA overlays)**; ready for **`STEP-018` (`ANN0001–ANN0006` Release Freeze & `G06 = PASS`)** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **PASS** | **Approved (`2026-11-18`):** All `6` cohorts (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined, `0` cross-cohort overlaps) & non-merged `Tracks A–F` approved (`DEC0002.md`, `G04_assessment_2026-11-18.md`) |
| G05 | STEP-015 | **PASS** | **Approved (`2026-11-19`):** Ontology `CLS0001–CLS0041` (`sha256:c3f91dfc...`), canonical YOLO `AABB` export contract (`< 0.002 px` round-trip error across all `6` datasets), and prospective `60`-OPG pilot / `240`-OPG batch QA thresholds frozen (`DEC0004–0006`, `G05_assessment_2026-11-19.md`) |
| G06 | STEP-018 | **NOT ASSESSED** | Ready to execute **`STEP-016` (Pilot QA), `STEP-017` (`ANNB0001–0006` batch conversion & QA), and `STEP-018` (`ANN0001–0006` release freeze)** |
| G07–G17 | STEP-020–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-016`–`STEP-018` (`S08` / `G06`)**:
   - `STEP-016`: Run the `60`-OPG stratified annotation pilot (`10` per dataset, seed `20261119`), generate off-Git overlay review sheets, evaluate agreement/defects against `G05` thresholds (`04_Annotations/reviews/pilot_review.md`).
   - `STEP-017`: Convert all `7,738` labeled active OPGs across `ANNB0001–ANNB0006` into canonical off-Git `04_Annotations/exports/TrackA–TrackF/`, log batch QA (`04_Annotations/reviews/ANNB0001–0006.md`) and adjudications (`04_Annotations/adjudications/`).
   - `STEP-018`: Run whole-release integrity & stratified `240`-OPG visual QA, populate `04_Annotations/annotation_registry.csv` (`ANN0001–ANN0006`), and assess **`G06`**, unlocking **`STEP-019`–`021` (Preprocessing & Split)**.
2. Maintain Private Google Drive sync (`03_Datasets/raw/DS0001–DS0006` + `*_restricted*` per `DEC0011`).
3. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001–DEC0006`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved)
- Gates: `01_Project_Management/gates.csv` (`G01–G05 PASS`; `G06–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
