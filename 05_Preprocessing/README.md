# `05_Preprocessing/`

- **Purpose:** Deterministic and training-only fitted preprocessing specs, configs, geometry verification reports.
- **Owner:** Akhtaruzzaman Anik (Preprocessing Lead)
- **Storage sensitivity:** Configs/reports public; `processed/` RESTRICTED (off-Git)
- **Inputs:** Locked `SPLIT` and `ANN` versions
- **Allowed contents / outputs:** `preprocessing_registry.csv`, `specs/`, `configs/`, `reports/`, off-Git `processed/`
- **Forbidden:** Raw image overwrites, test-fitted normalization, or pipeline code outside `src/opg/`
- **Workflow / commands:** Populated in Stage S09 (`STEP-019`, `STEP-021`).
- **Governing handbook:** [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
