# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-21 |
| Current stage / step | **`STEP-044` COMPLETE (Concise IMRaD paper package `11_Writing/paper/manuscript_draft.{md,v1.0.0.html}` `WRIT0009–0013` drafted, compiled with inline SVGs & IEEE refs, and audited `PASS` [`17/17` claims, `12/12` assets, `25/25` metric checks]; `paper_disposition.md` & `GA0018` `G15 / paper` recorded honestly as `DEFERRED` under `UD17`)**; **ready for `STEP-047`–`049` (Live Hosted Web Showcase `G17`) or `STEP-045`–`046` (Archival Release & Completion Audit `G16`)** |

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
| G10 | STEP-029–030 | **PASS** *(`13/13`)* | **ALL `13/13` experiments (`EXP0001–EXP0013` / `MODEL0001–MODEL0013`) PASSED (`2026-11-21`):** TrackE UAE **`0.858`**, TrackD Hanoi 1280 **`0.536`** (`+4.8%` vs 640 `0.488`), TrackB DENTEX **`0.444`**, TrackA UMFIH 1280 **`0.391`** (`0.1656` mAP50-95), TrackC Dhaka **`0.259`**, TrackF Pediatric **`0.100`**; `3/3` CLAHE ablations degraded `mAP@0.50` (`STEP030_matrix_tracker.md`) |
| G11 | STEP-031 | **PASS** | **Frozen (`2026-11-21`):** `FREEZE0001` locked (`6` track winners: `MODEL0005/0004/0006/0013/0008/0007` + `4` `RQ1`/`RQ3` comparators: `MODEL0001/0002/0003/0010`; `3/3` CLAHE excluded; `val`-only `conf_op`; `0` prior test access; `09_Evaluation/freeze_manifest.json`, `G11_assessment_2026-11-21.md`) |
| G12 | STEP-035 | **PASS** | **Verified (`2026-11-21`):** Programmatic audit (`g12_reconciliation_audit.json`) reconciled `14/14` EVALs, `128/128` per-class `TP+FN==GT` rows, `12/12` `HC01–HC05` shift bridges, `10` GPU + `7` CPU ONNX timing logs (`0` errors), `G11 < STEP-032` custody, and `CLAIM0013–CLAIM0017` (`final_evaluation_report.md`, `G12_assessment_2026-11-21.md`) |
| G13 | STEP-036 | **PASS** | **Verified (`2026-11-21`):** Exhaustive FP/FN taxonomy (`6,718` GT boxes), size-bucket recall (`Small 30.9% -> Large 80.3%`), `28` non-cherry-picked cases visually reviewed (`7` off-Git overlay sheets), source-label incompleteness & ordinal boundary uncertainty documented, and strict non-clinical limits frozen (`error_review.md`, `limitations.md`, `G13_assessment_2026-11-21.md`) |
| G14 | STEP-038 | **PASS** | **Verified (`2026-11-21`):** `OPGPrototypeEngine` + `REPRO0001`: **`R1`** `50/50` checksums, **`R2`** exact `0.0` metric replay (`EVAL0001/0011/0013`), **`R3A`** `0.0` self-diff & `0.994` ONNX-PyTorch IoU parity on `40` raw OPGs, **`R3B`** clean `git archive` checkout passing (`reproduce.md`, `reproducibility_audit.md`, `G14_assessment_2026-11-21.md`; `R4` GPU retraining transparently archived) |
| G15 | STEP-042 | **HOLD** *(Tech `PASS`)* | **Assembled & Audited (`2026-11-21`):** `DIU_CSE_Thesis_Assembled_v1.0.0.{md,html}` (`6` inline SVGs, `40` IEEE refs), `defense_slides.md` (`17` slides), `STEP-041` audit `PASS`; **`HOLD` strictly awaiting actual Ms Faiza Feroz supervisor sign-off & `UD17` defense date** (`G15_thesis_readiness_2026-11-21.md`) |
| G16–G17 | STEP-043–049 | **NOT ASSESSED** | Ready for **`STEP-043` (Submission Record once `G15 PASS`)**, **`STEP-044` (Concise Paper Package `WRIT0009–0013`)**, **`S15` (`STEP-045`–`046` Archive -> `G16`)**, & **`S16` (`STEP-047`–`049` Live Web Showcase -> `G17`)** |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-042`–`STEP-044`** (`S14` — Assemble complete thesis document + supervisor review checklist & DIU defense slide deck `WRIT0014` -> **`G15`**, preserve immutable thesis submission record, and prepare optional concise paper draft `WRIT0009–0013` / disposition).
2. Execute **`STEP-045`–`STEP-046`** (Final Archival Release & Zenodo/Git Tag -> **`G16 PASS`**) and **`STEP-047`–`STEP-049`** (Live Hosted Web Showcase reusing `OPGPrototypeEngine` -> **`G17 PASS`**).
3. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt" "*.onnx"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001–DEC0016`, `DEC0018`, `DEC0019` Resolved/Frozen; `DEC0017`, `DEC0020–0024` open for `S14–S16`)
- Gates: `01_Project_Management/gates.csv` (`G01–G14 PASS`; `G15–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
