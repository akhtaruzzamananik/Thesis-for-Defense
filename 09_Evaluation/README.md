# `09_Evaluation/`

- **Purpose:** Frozen evaluation/timing protocols, final-test release freeze, Precision/Recall/mAP@0.5/FPS reports, and error review.
- **Owner:** Mahajub Al Shabah (Evaluation Lead); Anik (reviewer)
- **Storage sensitivity:** Aggregate metrics public; raw predictions/private visuals off-Git
- **Inputs:** Validation-selected `MODEL`, `REL`, frozen protocol
- **Allowed contents / outputs:** `evaluation_registry.csv`, `protocol.md`, `freeze.md`, `EVAL####/` reports & `error_review.md`
- **Forbidden:** Test-driven tuning, cherry-picked examples, or selective metric omission
- **Workflow / commands:** Populated in Stage S12-S14 (`STEP-024`, `031`–`036`).
- **Governing handbook:** [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
