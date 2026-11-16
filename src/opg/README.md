# `src/opg/`

- **Purpose:** Reusable Python implementation for registry checks, data validation, annotation conversion, transforms, splitting, training, inference, and evaluation.
- **Owner:** Akhtaruzzaman Anik & Mahajub Al Shabah
- **Storage sensitivity:** Public source
- **Inputs:** Versioned configs and manifests
- **Allowed contents / outputs:** Structured manifests, predictions, metrics, exports
- **Forbidden:** Image datasets, trained weights, hardcoded patient paths, hidden hyperparameters
- **Workflow / commands:** Imported by `tests/`, `13_Automation/`, and `web/`.
- **Governing handbook:** [OPG Research Operating System](../../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
