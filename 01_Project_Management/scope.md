# Project scope record — STEP-001

| Field | Value |
|---|---|
| Record | `01_Project_Management/scope.md` |
| Step / gate | STEP-001 / G01 |
| Version | v0.1.0 (draft for supervisor review) |
| Created | 2026-11-16 |
| Status | **DRAFT — awaiting researcher and supervisor approval.** Not an approved scope. G01 NOT ASSESSED. |
| Governing sections | OS §1, §11, §13; Blueprint STEP-001 |
| Linked decisions | DEC0001 (UD01), DEC0021 (UD21); full register in `decisions.csv` |

## 1. Project identity (REPORT FACT, from retained RF ledger)

| Item | Value | Source / evidence |
|---|---|---|
| Approved title | A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO. | RF01 (report p.1). Original PDF deleted at user request; title retained in OS cover |
| Institution | Daffodil International University, Department of CSE | Report cover (retained in OS cover) |
| Report context | FYDP (Title Phase) Evaluation Report; Summer 2026; submitted 13 August 2026 | Report cover |
| Researchers | Akhtaruzzaman Anik (232-15-252); Mahajub Al Shabah (232-15-900) | Report cover |
| Supervisor | Ms Faiza Feroz, Lecturer | Report cover |
| Co-supervisor | Israt Jahan, Senior Lecturer | Report cover |

> The signed title-phase certificate is historical evidence of title approval only. It is **not** approval of this scope record, the operating policies, a dataset, an ethics determination, a class ontology or a clinical study.

**Source availability:** The original report PDF was deleted at the user's request after the plans were written (OS Appendix F). The title above comes from the retained RF ledger. **Verbatim O1–O3 wording is not retained.** See §3.

## 2. Scope (proposed interpretation, from OS §1.3)

**In scope:**

- Collect and characterize 2D OPG (panoramic dental radiograph) images.
- Annotate approved dental objects and selected visible abnormalities with bounding boxes.
- Preprocess and split the data reproducibly and without leakage (Figure 1 proposes 70/15/15 as the starting point).
- Select and train a YOLO detector, tune on validation, and test once on a held-out set.
- Measure Precision, Recall, mAP (with mAP@0.5 required, RF12) and inference speed/FPS.
- Analyze failures; write the thesis and paper documentation.
- Build a research inference prototype.
- **Host the final best model on a website** for the thesis defense. This is a team requirement added after the title report and needs supervisor confirmation (UD21 / DEC0021). It is governed by OS §8.3 and STEP-047–049.

**Out of scope:** 3D CBCT modeling; segmentation as a replacement primary task; image-level classification as a substitute for localization; treatment recommendation; autonomous diagnosis; clinical deployment; claims of proven clinician workload reduction. The hosted website is a research demonstration, not clinical deployment.

**Interpretation limits:**

- Diagram class examples are not a final class list: teeth, impacted tooth, cavities, lesions, restorations (RF09).
- No predicted box does not mean no disease.
- Scores are model scores, not diagnostic probabilities.
- The report's gap claims (G1–G6) are hypotheses to be tested in STEP-004–009.

## 3. Objectives O1–O3

| ID | Report objective (summary from RF06; **not verbatim**) | Operational interpretation (PLANNING RECOMMENDATION) | Evidence needed later |
|---|---|---|---|
| O1 | Design/train YOLO for detection and localization in OPG images | Dataset-to-box-prediction pipeline for approved visible targets | DS/ANN/REL versions, configs, model cards, inference examples |
| O2 | Test detection using Precision, Recall, mAP | Frozen model evaluated on locked held-out partition; explicit matching/AP definitions | Predictions, ground truth, evaluator version, per-class support, metrics |
| O3 | Fast computation / reduced overhead as a secondary aid | Latency and FPS under a stated hardware/workload protocol; no clinical efficiency claim | Timing samples, boundary, hardware/software, failure counts |

> **Unresolved / Human Decision Required (part of UD01):** The checklist item "Exact title and O1–O3 preserved" needs the **verbatim** objective text. A researcher must paste O1–O3 exactly from their retained copy of the title report (or another authorized copy), or the supervisor must confirm the summary wording in writing. Until then, this item stays open.

Candidate primary research question (awaiting G03 at STEP-009, not approved now): *How effectively and efficiently can an approved YOLO detector localize predefined dental objects and selected visible abnormalities in the available 2D OPG dataset under a leakage-controlled evaluation protocol?*

## 4. Feedback status (UD01)

| Item | Status | Evidence |
|---|---|---|
| Title-report feedback form (p.15) | Blank: three empty comment lines; examiner signature and date blank | RF15 |
| Separate supervisor/examiner feedback | **Unknown — confirmation requested** | Ask supervisor (see `meetings/STEP-001_supervisor_brief.md`) |

Only actual comments may be recorded here. No feedback is assumed or invented.

## 5. Decision governance

- Canonical register: `01_Project_Management/decisions.csv` (DEC0001–DEC0024 map one-to-one to UD01–UD24).
- Detailed records: `decision_log/DEC####.md`. Created now for DEC0001 and DEC0021; others are created when their decision is worked on.
- Owners listed in the register are **proposed roles**. Named owners are assigned only when the team/supervisor approve them.
- Later scientific choices (dataset, classes, YOLO version, settings, thresholds) stay **unresolved** until their blocking step. STEP-001 assigns owners and deadlines, not values.

## 6. Approval block (to be completed only with actual evidence)

| Role | Name | Decision (approve / approve with changes / reject) | Date | Evidence (email, signed sheet, meeting note path) |
|---|---|---|---|---|
| Researcher | Akhtaruzzaman Anik | | | |
| Researcher | Mahajub Al Shabah | | | |
| Supervisor | Ms Faiza Feroz | | | |
| Co-supervisor (if required) | Israt Jahan | | | |

## 7. Change history

| Version | Date | Change | Author | Approval |
|---|---|---|---|---|
| v0.1.0 | 2026-11-16 | Initial STEP-001 draft from retained RF ledger and OS v1.2.0 | Research team (AI-assisted draft) | Pending |
