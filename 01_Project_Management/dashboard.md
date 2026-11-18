# Project dashboard

| Field | Value |
|---|---|
| Project | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO |
| Institution | Daffodil International University (CSE) |
| Researchers | Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor), Israt Jahan (Co-supervisor) |
| Last updated | 2026-11-19 |
| Current stage / step | **S09 in progress (`STEP-019` Preprocessing Design & Geometry Contract `PP0001–PP0004` COMPLETE; split-dependent materialization blocked until `G07`)**; ready for **`STEP-020` (`G07` Leakage-Safe Split) and `STEP-021` (`G08` Materialize Prepared Release `REL`)** |

## 1. Stage & gate summary

| Gate | Step | Status | Notes |
|---|---|---|---|
| G01 | STEP-001 | **PASS** | Scope/O1–O3 confirmed via Telegram (Supervisor); no extra feedback; `team_roles.md` v1.0.0 confirmed by Anik & Mahajub (`2026-11-16`) |
| G02 | STEP-003 | **PASS** | Approved by Research Lead Akhtaruzzaman Anik (`2026-11-16`); `validate_repo.py` OK, `pytest` `5 passed` (incl. CSV row-width QA) |
| G03 | STEP-009 | **PASS** | **Approved (`2026-11-17`, reported by A. Anik):** Supervisor Ms Faiza Feroz & Literature Lead Mahajub Al Shabah confirmed `RQ0–RQ3` (`research_questions.md v1.0.0`) & `DEC0019` Option 1 (`G03_assessment_2026-11-17.md`) |
| G04 | STEP-013 | **PASS** | **Approved (`2026-11-18`):** All `6` cohorts (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined, `0` cross-cohort overlaps) & non-merged `Tracks A–F` approved (`DEC0002.md`, `G04_assessment_2026-11-18.md`) |
| G05 | STEP-015 | **PASS** | **Approved (`2026-11-19`):** Ontology `CLS0001–CLS0041` (`sha256:c3f91dfc...`), canonical YOLO `AABB` export contract (`< 0.002 px` round-trip error across all `6` datasets), and prospective `60`-OPG pilot / `240`-OPG batch QA thresholds frozen (`DEC0004–0006`, `G05_assessment_2026-11-19.md`) |
| G06 | STEP-018 | **PASS** | **Approved (`2026-11-19`):** Pilot (`60` OPGs) & production batches (`ANNB0001–0006`, `240` visual QA OPGs) accepted; **`ANN0001–ANN0006`** frozen (`7,738` `.txt` files, `44,241` valid boxes, `180` excluded/deduplicated, `0` orphans/invalid, `G06_assessment_2026-11-19.md`) |
| G07 | STEP-020 | **NOT ASSESSED** | **`STEP-019` preprocessing design (`PP0001–PP0004`) complete** — ready to execute **`STEP-020` (Leakage-Safe Grouped Split `SPLIT0001–SPLIT0006` & `G07`)** |
| G08–G17 | STEP-021–049 | **NOT ASSESSED** | `STEP-021` (`REL0001–REL0006` materialization) awaits `G07 PASS` |

## 2. Immediate priorities & open blockers

1. Execute **`STEP-020` (`S09` — Construct and approve the leakage-safe split / `G07`)**:
   - Build connected-component duplicate/patient grouping graphs from `STEP-013` exact SHA-256 + perceptual (`corr >= 0.95` / `dHash`) duplicate audits (`DS0001–DS0006`), allocate deterministic `70/15/15` grouped partitions (`SPLIT0001–SPLIT0006`) keeping `DS0001` `external_validation` (`178` unique clusters) sealed as an external holdout, verify `0` cross-partition component overlap, resolve `UD07/UD08` (`DEC0007.md`, `DEC0008.md`), and assess **`G07`**.
2. Execute **`STEP-021` (`G08` — Materialize and verify versioned prepared dataset releases `REL0001–REL0006`)**.
3. Maintain Private Google Drive sync (`03_Datasets/raw/DS0001–DS0006` + `*_restricted*` per `DEC0011`).
4. Maintain strict custody: `git ls-files "*.pdf" "*.zip" "*.rar" "*.jpg" "*.png" "*.pt"` stays empty.

## 3. Canonical ledgers

- Decisions: `01_Project_Management/decisions.csv` (`UD01–UD24` registered; `DEC0001–DEC0006`, `DEC0009`, `DEC0019` Resolved, `DEC0011` STEP-002 Resolved)
- Gates: `01_Project_Management/gates.csv` (`G01–G06 PASS`; `G07–G17 NOT ASSESSED`)
- Risks: `01_Project_Management/risk_register.csv` (header-only)
- Role split: `01_Project_Management/team_roles.md`
