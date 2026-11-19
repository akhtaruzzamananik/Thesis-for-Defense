# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-19 |
| Current stage / step | **S10 COMPLETE (`G09 = PASS` on Kaggle `Tesla T4`, `2026-11-19`)**; **S11 (`STEP-028`) UNLOCKED** — ready to launch **`EXP0001`** (`94.47 MB` bundle) on Kaggle GPU |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **PASS** | **Approved (`2026-11-18`):** All `6` cohorts (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined, `0` cross-cohort overlaps) & non-merged `Tracks A–F` approved (`DEC0002.md`, `G04_assessment_2026-11-18.md`) |
| G05 | STEP-015 | **PASS** | **Approved (`2026-11-19`):** Ontology `CLS0001–CLS0041` (`sha256:c3f91dfc...`), canonical YOLO `AABB` export contract (`< 0.002 px` round-trip error across all `6` datasets), and prospective `60`-OPG pilot / `240`-OPG batch QA thresholds frozen (`DEC0004–0006`, `G05_assessment_2026-11-19.md`) |
| G06 | STEP-018 | **PASS** | **Approved (`2026-11-19`):** Pilot (`60` OPGs) & production batches (`ANNB0001–0006`, `240` visual QA OPGs) accepted; **`ANN0001–ANN0006`** frozen (`7,738` `.txt` files, `44,241` valid boxes, `180` excluded/deduplicated, `0` orphans/invalid, `G06_assessment_2026-11-19.md`) |
| G07 | STEP-020 | **PASS** | **Approved (`2026-11-19`):** Connected-component grouped-stratified `70/15/15` splits **`SPLIT0001–SPLIT0006`** locked (`7,457` canonical OPGs [`5,106 train / 1,091 val / 1,082 test / 178 external_test`], `281` redundant copies deduplicated, `0` cross-partition leaks, `DEC0007–0008`, `G07_assessment_2026-11-19.md`) |
| G08 | STEP-021 | **PASS** | **Approved (`2026-11-19`):** Prepared dataset releases **`REL0001–REL0006`** & **`PP0001–PP0004`** verified (`7,457` canonical OPGs, `41,103` boxes, `0` dropped boxes, `max_rt_err = 0.003630 px @ 640 / 0.004068 px @ 1280`, train-only fit on `5,106` train OPGs, `G08_assessment_2026-11-19.md`) |
| G09 | STEP-026 | **PASS** | **Verified (`2026-11-19` on Kaggle `Tesla T4`, `torch 2.11.0+cu130`, `ultralytics 8.3.253`):** `EXP0000_SMOKE` epoch-1 interrupt (`optimizer`+`EMA` saved), backup SHA-256 match (`3f4452be...`), clean `resume=True` to epoch `2/2`, `19.51 FPS_e2e` (`G09_assessment_2026-11-19.md`) |
| G10–G17 | STEP-029–049 | **NOT ASSESSED** | Not started |

## 2. Immediate priorities & open blockers

1. Execute **`S10` (`STEP-022`–`026` — Baseline Readiness & `G09`)**:
   - `STEP-022`: Compare documented YOLO candidate implementations/scales in `06_Models/candidates.csv`, record baseline choice & weight provenance in `06_Models/baseline_plan.md` and `DEC0010.md` (`UD10`).
   - `STEP-023`: Pin and verify the model execution environment (`environment/model/` + `DEC0011` YOLO compute resolution).
   - `STEP-024`: Approve baseline, experiment matrix, and evaluation/timing plans (`07_Experiments/experiment_plan.md`, `09_Evaluation/protocol.md`, `DEC0012–DEC0016`).
   - `STEP-025` & `STEP-026`: Implement data loader/trainer/evaluator adapters (`src/opg/`), run smoke & checkpoint recovery verification, and assess **`G09`**.
2. Maintain Private Google Drive sync (`03_Datasets/raw/DS0001–DS0006` + `05_Preprocessing/processed/REL0001–REL0006` per `DEC0011`).
3. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001–DEC0009`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved)
- Gates: `01_Project_Management/gates.csv` (`G01–G07 PASS`; `G08–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
