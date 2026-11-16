# `web/`

- **Purpose:** Thin web front end and API calling the frozen `src/opg/` inference entry point, plus container/deployment config and web tests.
- **Owner:** Akhtaruzzaman Anik (Deployment Owner); Mahajub (parity reviewer)
- **Storage sensitivity:** Public source (secrets in host secret store only)
- **Inputs:** STEP-037 inference entry point, registered best `MODEL` pointer/hash
- **Allowed contents / outputs:** Web app, `Dockerfile`, web tests
- **Forbidden:** Reimplemented preprocessing/thresholds/class maps, model weights, patient images, or secrets in Git
- **Workflow / commands:** Built and parity-tested in Stage S16 (`STEP-048`).
- **Governing handbook:** [OPG Research Operating System](../OPG_RESEARCH_OPERATING_SYSTEM.md#os-02) · [Execution Blueprint](../OPG_PROJECT_EXECUTION_BLUEPRINT.md)
