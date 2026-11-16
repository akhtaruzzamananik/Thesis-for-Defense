# Changelog

All notable changes to the project governance, plans, and repository structure are recorded here.

## [Unreleased] — STEP-004 Protocol Approved

- Promoted `02_Literature/searches/protocol.md` to `v1.0.0` (Research Lead Akhtaruzzaman Anik approved 2026-11-16).

## [Unreleased] — G02 PASS Recorded

- Recorded Research Lead (Akhtaruzzaman Anik) approval of `G02` (`PASS`) in `01_Project_Management/reviews/G02_assessment_2026-11-16.md`, `gates.csv`, and `dashboard.md`.

## [Unreleased] — STEP-004 Draft (Literature Search Protocol & Provisional RQs)

- Drafted `02_Literature/searches/protocol.md` (queries `Q1–Q3` testing `G1–G6`, inclusion/exclusion codes, deduplication, and quality criteria), `02_Literature/searches/search_log_template.md`, and `02_Literature/research_questions.md` (provisional `RQ1–RQ3` bounded by `O1–O3`).
- Logged `01_Project_Management/diary/2026-11-16_STEP-004.md`; kept `G01` and `G02` as `NOT ASSESSED` pending human sign-off before executing `STEP-005` searches.

## [Unreleased] — STEP-003 Part 2 (Templates, Validator, and G02 Readiness Review)

- Installed all 30 blank operational templates (`T01–T30`) and `templates_index.md` under `14_Templates_Prompts/`.
- Added `src/opg/repo_validator.py`, `13_Automation/validate_repo.py`, and `tests/test_repo_checks.py` (`4 passed in 0.40s`).
- Created `01_Project_Management/reviews/G02_assessment_2026-11-16.md` and `01_Project_Management/diary/2026-11-16_STEP-003.md` (awaiting Research Lead sign-off for `G02 PASS`).

## [Unreleased] — STEP-003 Part 1 (Canonical CSV Registries, Dashboard, Timeline)

- Created all 21 remaining Appendix B CSV registries (header-only, zero dummy data; `gates.csv` initialized with `G01–G17` as `NOT ASSESSED`).
- Added `01_Project_Management/dashboard.md` and `01_Project_Management/timeline.md`.

## [Unreleased] — STEP-002 Complete (UD11 Storage Lock)

- Confirmed off-Git storage policy (`DEC0011.md`): Local PC (active) + Private Google Drive (restricted to Anik & Mahajub for backup/sync), paired with public GitHub (`main`) for source/metadata only.
- Recorded `01_Project_Management/diary/2026-11-16_STEP-002.md`.

## [Unreleased] — STEP-002 Part 3 (Minimal Data-Tool Runtime & Smoke Check)

- Recreated local `.venv` on Python `3.14.6` (excluded from Git) and locked minimal data-tool dependencies (`pillow==13.0.0`, `numpy==2.5.5`, `PyYAML==6.0.3`, `pytest==9.2.0`) in `environment/data/requirements.lock.txt`.
- Added synthetic smoke checks in `tests/test_smoke_data_env.py` (`3 passed in 1.28s`) and recorded evidence in `environment/data/verification.md` and `12_Documentation/installation.md`.

## [Unreleased] — STEP-002 Part 2 (Repository Skeleton & Inventory)

- Materialized OS §2.1 domain folders (`02_Literature/`–`16_Web_Demo/`, `environment/data/`, `src/opg/`, `tests/`, `web/`) with contract `README.md` files.
- Added `src/opg/__init__.py`, `12_Documentation/pipeline.md` (storage tiers & data lineage), and `01_Project_Management/reviews/source_inventory_2026-11-16.md` (SHA-256 inventory and historical deletion record).

## [Unreleased] — STEP-002 Part 1 (Repository Initialization & Governance)

- Connected local workspace directly to `origin/main` (`Thesis-for-Defense`).
- Added `.gitignore` and `.gitattributes` to enforce off-Git protection for OPG images, patient linkage keys, model weights, secrets, and virtual environments.
- Replaced unrelated template `README.md` with the OPG YOLO thesis `README.md`; added `CHANGELOG.md` and `CONTRIBUTING.md`.

## [v1.2.0] — 2026-11-16 (STEP-001 Draft & Hosted Best-Model Web Plan)

- Updated `OPG_RESEARCH_OPERATING_SYSTEM.md` and `OPG_PROJECT_EXECUTION_BLUEPRINT.md` to add Stage S16 (`STEP-047–049`, `G17`, `UD21–UD24`, `T29–T30`, `web/`, `16_Web_Demo/`) for hosting the validation-selected final best model at the thesis defense.
- Created `01_Project_Management/` STEP-001 records (`scope.md`, `decisions.csv`, `DEC0001.md`, `DEC0021.md`, `team_roles.md`, supervisor brief, `G01` pre-assessment, session diary).
- Recorded supervisor Ms Faiza Feroz's Telegram confirmation on scope/O1–O3, confirmation of no extra defense feedback, secondary-dataset intention, and public GitHub repository policy.

## [v1.1.0] — 2026-11-16

- Recorded user-directed deletion of initial template/source files in `OS Appendix F`, added two-phase environment readiness (`STEP-002` / `STEP-023`), and separated `G15` thesis vs. paper readiness.

## [v1.0.0] — 2026-11-16

- Initial source-grounded OPG Research Operating System and Project Execution Blueprint.
