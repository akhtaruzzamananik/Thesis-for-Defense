# A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO

**Institution:** Daffodil International University, Department of Computer Science and Engineering  
**Context:** FYDP (Summer 2026 title phase → ongoing execution)  
**Researchers:** Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`)  
**Supervisors:** Ms Faiza Feroz (Lecturer), Israt Jahan (Senior Lecturer)

> **Research disclaimer:** This repository is for an academic research prototype studying automated 2D OPG dental object localization using YOLO. It is **not** a clinically validated diagnostic tool and must not be used for medical diagnosis or treatment decisions.

---

## Current Project Status (as of 2026-11-16)

- **Planning documents:** Complete (`v1.2.0`) — see [OPG Research Operating System](./OPG_RESEARCH_OPERATING_SYSTEM.md) and [OPG Project Execution Blueprint](./OPG_PROJECT_EXECUTION_BLUEPRINT.md).
- **Execution state:** **STEP-001 in progress / STEP-002 initialization.**
- **Quality gates:** All scientific and operational gates (`G01–G17`) remain **NOT ASSESSED** until their required evidence and sign-offs are recorded.
  - Scope & O1–O3 interpretation confirmed via Telegram by Supervisor Ms Faiza Feroz (reported 2026-11-16).
  - Team role split (`team_roles.md`) drafted and awaiting Mahajub Al Shabah's confirmation to close `G01`.
  - Dataset selection, dental ontology, YOLO variant, and training/evaluation configurations remain unresolved until their owning steps.

---

## Scope & Core Objectives

- **Task:** Bounding-box object detection in **2D Orthopantomogram (OPG)** dental radiographs using **YOLO** (using a secondary/public OPG dataset to be selected and licensed at Stage S05).
- **Objectives (O1–O3):**
  1. **O1:** Design and train a YOLO object-detection and localization pipeline for approved visible dental targets.
  2. **O2:** Evaluate detection performance on a leakage-controlled, locked held-out test partition using **Precision**, **Recall**, and **mAP** (with **mAP@0.5** required).
  3. **O3:** Measure inference speed (**FPS** / latency) and computational overhead as a secondary aid.
- **Defense deliverable (S16):** Host the validation-selected, frozen **final best model** on a thin web demonstration site for the thesis defense (backed by an offline fallback), calling the same frozen inference entry point.

---

## Repository Governance & Public-Repo Safety Rules

This repository is **public** (`https://github.com/akhtaruzzamananik/Thesis-for-Defense`). Strict storage separation (`OS §10.2`) applies at all times:

- **Tracked in Git:** Planning documents, Python source code (`src/opg/`, `web/`), tests, non-sensitive CSV registries, configs, documentation, and small permitted figure/table assets.
- **NEVER committed to Git (blocked by `.gitignore`):** Raw or processed OPG images, native/exported medical annotations, patient/group linkage keys, trained model checkpoints/weights (`.pt`, `.onnx`, etc.), credentials, `.env` files, or `.venv/`.

---

## Governing Documents & Initial Records

- [OPG_RESEARCH_OPERATING_SYSTEM.md](./OPG_RESEARCH_OPERATING_SYSTEM.md) — Project constitution, storage tiers, YOLO/evaluation/web-demo policies, quality gates (`G01–G17`), and registry schemas (`v1.2.0`)
- [OPG_PROJECT_EXECUTION_BLUEPRINT.md](./OPG_PROJECT_EXECUTION_BLUEPRINT.md) — 16-stage, 49-step sequential execution roadmap (`v1.2.0`)
- [01_Project_Management/scope.md](./01_Project_Management/scope.md) — Project scope draft and approval record
- [01_Project_Management/team_roles.md](./01_Project_Management/team_roles.md) — Anik & Mahajub 50/50 workload & cross-review distribution
- [01_Project_Management/decisions.csv](./01_Project_Management/decisions.csv) — Unresolved decision register (`UD01–UD24`)

*(Note: This README replaces an earlier unrelated template placeholder README from initial repository creation.)*
