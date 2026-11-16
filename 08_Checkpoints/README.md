# `08_Checkpoints/`

- **Purpose:** Checkpoint policy, manifests, SHA-256 checksums, off-Git artifact pointers, and restore verification.
- **Owner:** Mahajub Al Shabah (Experiment Lead)
- **Storage sensitivity:** Checksums/manifests public; binary weights RESTRICTED/off-Git
- **Inputs:** Training runs (`EXP`/`RUN`)
- **Allowed contents / outputs:** `checkpoint_registry.csv`, `checkpoint_policy.md`, `manifests/`, off-Git `artifacts/`
- **Forbidden:** Weight binaries (`.pt`, `.onnx`, etc.) committed to ordinary Git
- **Workflow / commands:** Populated in Stage S10-S11 (`STEP-026`, `028`–`030`).
- **Governing handbook:** [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
