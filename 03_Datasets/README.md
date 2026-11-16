# `03_Datasets/`

- **Purpose:** Secondary OPG candidate comparison, dataset registry, licenses, raw image custody, quality reports, grouped splits, and prepared releases.
- **Owner:** Akhtaruzzaman Anik (Data Steward); Mahajub (reviewer)
- **Storage sensitivity:** Metadata public; `raw/`, `splits/*linkage*` RESTRICTED (off-Git)
- **Inputs:** Public/secondary dataset terms, raw archives, approved annotations/preprocessing
- **Allowed contents / outputs:** `candidates.csv`, `datasets.csv`, `releases.csv`, `licenses/`, `manifests/`, `reports/`, `splits/`, off-Git `raw/`
- **Forbidden:** Committing raw image bytes to Git; patient-key mappings in shared metadata
- **Workflow / commands:** Populated in Stage S05-S06 & S09 (`STEP-010`–`013`, `020`–`021`).
- **Governing handbook:** [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
