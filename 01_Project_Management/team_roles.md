# Team role distribution — Anik & Mahajub

| Field | Value |
|---|---|
| Record | `01_Project_Management/team_roles.md` |
| Version | v0.1.0 (proposed by Anik, 2026-11-16; awaiting Mahajub confirmation) |
| Governing section | OS §11 (Roles and human decisions) |
| Supervisor / Co-supervisor | Ms Faiza Feroz (Lecturer) / Israt Jahan (Senior Lecturer) |

Both teammates share overall project accountability and review each other's outputs. Primary ownership divides the workload ~50/50 and keeps development separated from cross-checking (data splitting vs modeling; modeling vs reproducibility/web parity).

## 1. Primary ownership by teammate

| Teammate | Primary roles | Stages / Steps owned | UD items owned | Cross-review duties |
|---|---|---|---|---|
| **Akhtaruzzaman Anik** (`232-15-252`) | Research Lead (repo/governance), Data Steward & Preprocessing Lead, Prototype & Web Deployment Owner | **S01–S02** (`001–003`), **S05–S06** (`010–013`), **S09** (`019–021`), **S14** (`037`), **S16** (`047–049`), **S15** (`045` archive) | `UD01` (co), `UD02`, `UD03`, `UD07`, `UD08`, `UD09`, `UD11` (co), `UD18`, `UD20`–`UD24` | Review Mahajub's literature claims/citations; review experiment configs & G11/G12 evaluation freezes |
| **Mahajub Al Shabah** (`232-15-900`) | Literature Lead, Annotation QA Lead, Model & Evaluation Lead, Reproducibility Auditor | **S03–S04** (`004–009`), **S07–S08** (`014–018`), **S10–S13** (`022–036`), **S14** (`038` audit) | `UD01` (co), `UD04`–`UD06`, `UD10`, `UD11` (co), `UD12`–`UD16`, `UD19` | Review Anik's split/preprocessing leakage checks; review web demo parity & disclaimer; clean-run audit (`STEP-038`) |
| **Both (shared)** | Co-authors, defense presenters, gate reviewers | **S15** (`039–044`, `046`) and all gate reviews | `UD17`, shared defense prep & offline fallback | Jointly review every gate (`G01–G17`) and thesis/paper chapter |

## 2. Thesis writing split (`S15`)

- **Anik:** Methodology (dataset characterization, grouping/split, preprocessing), Research Prototype & Hosted Web System (`§8.3`), Appendices / Reproducibility package.
- **Mahajub:** Introduction & Objectives, Literature Review & Gap Assessment, Annotation Protocol/QA, Experiments, Results (`Precision`, `Recall`, `mAP@0.5`, `FPS`), Error Analysis & Discussion.
- **Joint:** Abstract, Conclusion, formatting, citation audit, supervisor revision responses, and defense slides.

## 3. External / human sign-offs (cannot be self-approved by teammates)

- **Supervisor (Ms Faiza Feroz) / Co-supervisor (Israt Jahan):** Scope/objectives (`G01`), research questions (`G03`), split/eval/success-criteria sign-offs (`G07`, `G09`, `G11`), error conclusions (`G13`), thesis/paper readiness (`G15`), live demo walkthrough (`G17`), final completion (`G16`).
- **Qualified Dental Reviewer (to be identified before `STEP-014`):** Class ontology & labelability (`G05`), secondary dataset label audit/adjudication (`G06`), clinical wording & sample-image check (`G13`, `UD23`).

## 4. Confirmation record

| Member | Status | Date |
|---|---|---|
| Akhtaruzzaman Anik | Proposed / accepted | 2026-11-16 |
| Mahajub Al Shabah | Pending confirmation | |
