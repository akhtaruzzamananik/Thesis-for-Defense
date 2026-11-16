# `environment/`

- **Purpose:** Chosen environment locks, runtime inventories, and hardware/software records (`environment/data/` and later `environment/model/`).
- **Owner:** Akhtaruzzaman Anik & Mahajub Al Shabah
- **Storage sensitivity:** Public metadata (no secrets)
- **Inputs:** UD11 runtime/hardware decisions
- **Allowed contents / outputs:** Dependency lockfiles, runtime inventory, `verification.md`
- **Forbidden:** Speculative pins advertised as tested; credentials or secrets
- **Workflow / commands:** See `12_Documentation/installation.md` once environment is locked in STEP-002 Part 3.
- **Governing handbook:** [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
