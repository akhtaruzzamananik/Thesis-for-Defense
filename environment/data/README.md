# `environment/data/`

- **Purpose:** Minimal pinned data-tool runtime lock and smoke verification prior to dataset/model work.
- **Owner:** Akhtaruzzaman Anik
- **Storage sensitivity:** Public metadata
- **Inputs:** Python runtime and core data/registry packages
- **Allowed contents / outputs:** Lockfile, `verification.md`
- **Forbidden:** YOLO/GPU training dependencies (deferred to STEP-023)
- **Workflow / commands:** Smoke checks executed in STEP-002 Part 3.
- **Governing handbook:** [OPG Research Operating System](../../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
