# OPG RESEARCH OPERATING SYSTEM

## Cover page

**Approved research title:** A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO.

| Field | Value |
|---|---|
| Document | OPG_RESEARCH_OPERATING_SYSTEM.md |
| Type | Project-specific research governance and operational handbook |
| Version / date | v1.1.0 / 2026-11-16 |
| Status | Complete planning document; proposed operating policies awaiting human ratification; research execution NOT VERIFIED |
| Institution | Daffodil International University, Department of Computer Science and Engineering (report cover) |
| Report context | FYDP (Title Phase) Evaluation Report; reporting period Summer 2026; submission date 13 August 2026 |
| Researchers | Akhtaruzzaman Anik, ID 232-15-252; Mahajub Al Shabah, ID 232-15-900 (report cover) |
| Supervisor | Ms Faiza Feroz, Lecturer (report cover) |
| Co-supervisor | Israt Jahan, Senior Lecturer (report cover) |
| Operational owner | Research team; named task owners and qualified dental reviewer remain to be assigned |
| Scientific authority | Title evaluation report (reviewed during v1.0.0 authoring; subsequently removed at the user’s request; see [source status](#source-status)), interpreted within the user's binding approved scope |
| Execution companion | [OPG Project Execution Blueprint](./OPG_PROJECT_EXECUTION_BLUEPRINT.md) |
| Intended output | Research prototype for dental object localization in 2D OPG images; supplementary aid, not validated clinical diagnosis |

The cover's signed certificate is part of the supplied title-phase record. It does not establish approval of the new policies, a clinical study, a dataset license, or an annotation ontology. No such approval is inferred here.

## Version history

| Version | Date | Change | Approval state |
|---|---|---|---|
| v1.0.0 | 2026-11-16 | Initial source-grounded OPG handbook and aligned 46-step execution architecture | Proposed; no execution gates passed |
| v1.1.0 | 2026-11-16 | Recorded user-directed source deletion; added early data-tool environment readiness; separated thesis and paper submission-readiness assessments | Editorial/workflow correction authorized; scientific execution gates remain NOT ASSESSED |

Record subsequent changes with author, reason, affected decisions, affected steps, and approval evidence. A title or scope change requires formal supervisor review; a typographical correction does not silently change scientific commitments.

## Table of contents

1. [Executive summary](#executive-summary)
2. [1. Project constitution and source authority](#os-01)
3. [2. Repository architecture and folder contracts](#os-02)
4. [3. Literature and research-question workflow](#os-03)
5. [4. Dataset, preprocessing, and split operating system](#os-04)
6. [5. YOLO model and experiment operating system](#os-05)
7. [6. Annotation governance and quality assurance](#os-06)
8. [7. Evaluation protocol](#os-07)
9. [8. Research prototype and reproducibility](#os-08)
10. [9. Writing and submission operating system](#os-09)
11. [10. Version control and artifact storage](#os-10)
12. [11. Roles and human decisions](#os-11)
13. [12. Daily research operations](#os-12)
14. [13. Quality gates and completion](#os-13)
15. [14. Template library](#os-14)
16. [Appendix A. Canonical definitions](#appendix-a)
17. [Appendix B. Registry catalog and schemas](#appendix-b)
18. [Appendix C. Stage map and dependency chain](#appendix-c)
19. [Appendix D. Glossary](#appendix-d)
20. [Appendix E. Acronyms](#appendix-e)
21. [Appendix F. Source coverage and self-review](#appendix-f)

<a id="executive-summary"></a>
## Executive summary

This handbook governs collection, preprocessing, annotation, preparation, YOLO training, validation, testing, and evaluation of 2D panoramic dental radiographs. Predictions are bounding boxes and approved class labels for predefined dental objects and selected visible abnormalities. The required metrics are Precision, Recall, mAP, and inference speed. The report's Figure 1 additionally proposes mAP@0.5, FPS, and a 70% training / 15% validation / 15% testing allocation. Those details are preserved, not replaced by assumed defaults.

The research contribution is a focused, reproducible detection workflow and an honestly evaluated prototype. The report's gap analysis is a proposal to investigate. It does not establish that no OPG detection system exists, that YOLO is superior, or that this project is novel. Literature review must test those propositions against direct and contradictory evidence.

The architecture follows the management discipline of the two supplied Markdown templates: canonical artifact homes, stable identifiers, source-backed claims, explicit human decisions, immutable experiment records, recovery procedures, and evidence-based gates. Its scientific methods, computing platform, and implementation library must be chosen for this project. No platform-specific development arrangement is inherited from the templates.

This is a plan, not an account of completed research. All G01-G16 gates initially have status **NOT ASSESSED**, which blocks dependent work just as a failed gate does. Empty registries, proposed checks, and this document's self-review are not evidence that experiments or scientific gates have passed.

<a id="os-01"></a>
# 1. Project constitution and source authority

## 1.1 Authority and evidence labels

Use the following labels in decisions, drafts, and reports:

- **REPORT FACT:** content explicitly present in the supplied report, with physical PDF page and section/figure/table locator. A report statement about another paper is a fact about what the report says, not independent verification of that paper.
- **PLANNING RECOMMENDATION:** a proposed method or operational rule introduced here. It becomes an adopted project policy only when the responsible human records approval; it never becomes a fact attributed to the report.
- **Unresolved / Human Decision Required:** missing, ambiguous, unverified, or source-dependent information that needs a named decision owner and evidence.

Authority order: approved project scope and report; recorded supervisor-approved clarifications within that scope; this handbook; the companion blueprint; implementation configurations. The former master handbook and execution template were structural references only; both were subsequently deleted at the user’s request. Their removal does not remove the approved scientific scope. If an implementation conflicts with a governing policy, stop the dependent work, record the conflict, and correct or formally revise the policy. Do not reinterpret historical results to fit a new policy.

## 1.2 Source-grounded facts ledger

Page numbers below are physical PDF pages, starting with the photographic cover as page 1; the report's section numbering is not sequential.

| ID | REPORT FACT | Locator | Operational implication |
|---|---|---|---|
| RF01 | Exact approved title appears on the cover | p.1, Project Identification I | Preserve title verbatim in research records |
| RF02 | Project concerns detection in 2D OPG images using YOLO | pp.2-3, Abstract and Introduction | Detection/localization is the primary task |
| RF03 | Predefined dental objects and selected visible anomalies are to receive boxes and class labels | pp.2-3, pp.8-10 | An approved class ontology is required before production annotation |
| RF04 | Workflow includes collection, preprocessing, annotation, dataset preparation, training, validation, testing, evaluation | pp.10-11, Proposed diagram and Figure 1 | Preserve this scientific lifecycle |
| RF05 | Required evaluation uses Precision, Recall, mAP, inference speed | p.2 Abstract; p.3; p.9 G6; pp.10-11 | Report all four, including unfavorable outcomes |
| RF06 | Three objectives concern YOLO detection/localization, detection metrics, and fast computation/reduced overhead as a secondary aid | p.10, Objectives | Translate into measurable research questions without claiming achieved clinical utility |
| RF07 | Figure 1 lists hospitals, clinics, or public datasets as collection possibilities | p.11, box 1 | These are source categories, not obtained datasets or permissions |
| RF08 | Figure 1 lists contrast enhancement, noise reduction, resizing, normalization, filtering | p.11, box 2 | Specify and assess operations; no parameter values or proven benefit are supplied |
| RF09 | Figure 1 gives examples: teeth, impacted tooth, cavities, lesions, restorations, etc. | p.11, box 3 | Examples are not a final exhaustive ontology, numeric class map, or proof of radiographic labelability |
| RF10 | Figure 1 proposes 70% training, 15% validation, 15% testing | p.11, box 4 | Start split design from these proposed proportions; grouping and actual counts require evidence |
| RF11 | Figure 1 tunes learning rate, batch size, epochs, etc. on validation and selects the best-performing model before unseen-image testing | p.11, boxes 5-7 | Freeze selection and thresholds before final test access |
| RF12 | Figure 1 explicitly lists mAP@0.5 and inference speed (FPS) | p.11, box 8 | Primary detection AP setting is IoU 0.50; FPS requires a defined timing boundary |
| RF13 | Final diagram output is detected objects with bounding boxes and class labels | p.11, box 9 | Preserve coordinate and class provenance in prototype output |
| RF14 | Table 1 summarizes 13 cited studies; Table 2 proposes six gap themes G1-G6 | pp.4-9; references pp.12-14 | Treat bibliography and gap themes as leads requiring source verification |
| RF15 | Supervisor feedback has three blank comment lines; examiner signature and date are blank | p.15 | No substantive feedback is available to implement or quote |
| RF16 | CO1 maps to PO1, CO2 to PO2, CO3 to PO4, covering problem identification, analysis, and literature-based goals | p.2, CO/PO table | Preserve institutional context; do not invent assessment outcomes |

## 1.3 Binding scope and exclusions

**In scope:** 2D OPG image collection and characterization; approved dental object/visible-abnormality box annotation; reproducible preprocessing and splitting; YOLO model selection and training; validation; held-out testing; detection metrics and timing; failure analysis; thesis/paper documentation; a research inference prototype.

**Outside the present approved study:** 3D CBCT modeling, segmentation as a replacement primary task, image-level disease classification as a substitute for localization, treatment recommendations, autonomous diagnosis, clinical deployment, or proven reductions in clinician workload. Other methods can be reviewed as related literature. A new task or clinical validation study requires a separately justified scope amendment.

Avoid interpreting an absence of a predicted box as absence of disease. Detection scores are model scores, not calibrated diagnostic probabilities. A reviewer may conclude that some diagram examples are unsuitable for reliable box labeling on the available OPG images. That decision must be documented, not hidden behind an ambiguous umbrella class.

## 1.4 Objectives and candidate research questions

The three report objectives are preserved as O1-O3:

| Objective | Operational interpretation (PLANNING RECOMMENDATION) | Evidence needed |
|---|---|---|
| O1: design/train YOLO detection and localization | Build a dataset-to-box-prediction pipeline for approved visible targets | Dataset/annotation versions, training configs, model cards, inference examples |
| O2: test detection with Precision, Recall, mAP | Evaluate a frozen model on a locked held-out partition with explicit matching and AP definitions | Predictions, ground truth, evaluator version, counts, metrics, per-class support |
| O3: fast computation and reduced overhead for a secondary aid | Measure inference latency and FPS under a stated hardware/workload protocol | Timing samples, boundaries, hardware/software, failure counts; no clinical efficiency conclusion without a separate study |

Candidate primary question, awaiting G03 approval: **How effectively and efficiently can an approved YOLO detector localize predefined dental objects and selected visible abnormalities in the available 2D OPG dataset under a leakage-controlled evaluation protocol?**

Candidate subordinate questions: RQ1, detection performance overall and per approved class; RQ2, the effect of a justified preprocessing or training factor on validation performance under controlled comparison; RQ3, measured speed and observed failure patterns under documented inference conditions. These are recommendations, not report quotations. Assign stable RQ identifiers on approval; do not promise a favorable answer.

## 1.5 Research principles and ethics

1. Plan and review the protocol before implementation or expensive training.
2. Trace every result to data, labels, split, configuration, source revision, and model checksum.
3. Preserve failed, interrupted, null, and negative experiments and all attempted comparisons.
4. Keep raw data immutable; corrections create derived versions with provenance.
5. Use validation for development; keep final test data inaccessible to tuning.
6. Protect patient privacy in pixels, metadata, logs, figures, filenames, and backups.
7. Respect data access terms, consent/waiver determinations, institutional ethics decisions, software licenses, and pretrained-weight terms independently.
8. Record actual uncertainty. Never invent citations, annotation agreement, sample sizes, dates, approvals, performance targets, or outcomes.
9. Distinguish technical validity from high performance. A valid low-performing experiment can be scientifically complete.
10. Keep human dental interpretation and methodological sign-off with qualified reviewers and supervisors.

Obtain the institution's determination on ethics review and permitted use before restricted acquisition or annotation. Do not presume public availability means unrestricted medical-data use. Use a restricted linkage store for patient identifiers; analytical manifests use pseudonymous grouping IDs. A de-identified image can still be sensitive. Public examples require permission and a separate disclosure review.

## 1.6 Unresolved decision register at initialization

Every row below is **Unresolved / Human Decision Required**. The canonical future record is `01_Project_Management/decisions.csv`; detailed resolutions use `decision_log/DEC####.md`. Decisions can remain open until their blocking milestone. Step 001 approves owners and deadlines, not arbitrary scientific values.

| ID | Decision / missing evidence | Owner role | Resolve before | Required resolution evidence |
|---|---|---|---|---|
| UD01 | Confirm scope interpretation, operational owners, and whether further title-defense feedback exists | Researchers + supervisor | G01 / STEP-001 | Scope record; actual feedback or confirmation that none is supplied |
| UD02 | Source dataset(s), access route, provenance, sample size, population, acquisition sites | Researchers + data custodian | G04 / STEP-013 | Candidate comparison, source records, measured counts |
| UD03 | Data license, permitted processing/sharing, ethics/consent/waiver requirements, retention | Institution + custodian | Before acquisition; G04 | Written terms and institutional determination |
| UD04 | Exact class inventory, clinical definitions, labelability, overlap and target granularity | Dental reviewer + supervisor | G05 / STEP-015 | Approved class table and examples; no invented final classes |
| UD05 | Annotation tool, native/export format, coordinate convention and box geometry | Annotation lead + dental reviewer | G05 | Versioned schema, tested export plan; axis-aligned boxes are only a recommendation |
| UD06 | Annotator credentials, review sample, agreement measures, acceptance thresholds, adjudication | Dental reviewer + researchers | Pilot STEP-016 | Prospective QA plan and named adjudicator |
| UD07 | Patient/study/source grouping availability, duplicates, supplied split reliability | Custodian + researchers | G07 / STEP-020 | Grouping metadata or conservative alternative and stated limitations |
| UD08 | Operational split algorithm, seed, rounding, class support, use of proposed 70/15/15 | Researchers + supervisor | G07 | Reproducible group-level manifest and approval of any departure |
| UD09 | Preprocessing algorithms/parameters, annotation reference image, augmentation limits | Researchers + dental reviewer | G08 / STEP-021 | Geometry/visibility validation and fit-on-training rules |
| UD10 | YOLO implementation, release/commit, architecture/scale, pretrained weights and licenses | Researchers + supervisor | G09 / STEP-026 | Candidate review, provenance and baseline decision |
| UD11 | Compute platform, hardware, dependency versions, storage, backup and access controls | Researchers + institution | G02 storage and minimal data-tool runtime; G09 YOLO runtime | Feasibility/access decision and executable environment lock |
| UD12 | Training settings, seed/repeat policy, budgets, stopping rules, comparison factors | Researchers + supervisor | G09; each STEP-027 | Approved experiment plan with resolved configurations |
| UD13 | Precision/Recall operating point, AP implementation, NMS, matching, maximum detections, averaging, missing-class rules | Evaluation lead + supervisor | G09; freeze at G11 | Protocol preserving report mAP@0.5; separate NMS and matching IoU |
| UD14 | Timing boundary, batch size, precision mode, warm-up/repetitions, hardware and target if any | Evaluation lead | G09; freeze at G11 | Timing protocol; no invented minimum FPS |
| UD15 | Additional analyses: AP across IoUs, uncertainty, repeats, external data, subgroups, robustness | Researchers + supervisor | G09; freeze at G11 | Feasible preregistered scope or explicit non-adoption reasons |
| UD16 | Numeric scientific success criteria, if required by supervisor | Supervisor + researchers | G09 | Rationale grounded in task/data; distinct from gate validity |
| UD17 | Thesis format, dates, authorship, acknowledgements, paper venue and submission obligations | Researchers + supervisor | Writing plan; G15 | Actual institutional/venue instructions and author agreement |
| UD18 | Prototype interface and permitted demonstration material | Researchers + dental reviewer | STEP-037 | Minimal approved inference interface and disclosure review |
| UD19 | Report bibliography metadata/content verification, including typographic/encoding issues | Literature lead | G03 / STEP-009 | Original sources checked; unresolved sources excluded from supporting claims |
| UD20 | Release license, archival access/retention, artifact host and post-project ownership | Researchers + custodian | STEP-045; permissions before any upload | Tiered release/retention agreement and restore evidence |

New uncertainties receive new UD numbers. The blueprint references this register rather than creating divergent assumptions. A blocking unknown remains a blocker even if a software library has a default for it.

<a id="os-02"></a>
# 2. Repository architecture and folder contracts

## 2.1 Proposed repository layout

Only the two requested planning documents are created at this planning stage. The following is a **future architecture**, to be instantiated by STEP-002/003. The three original source files were deleted after initial authoring at the user’s explicit request; they are not current repository contents. Listed future paths are contracts, not assertions that files currently exist.

```text
workspace/
  OPG_RESEARCH_OPERATING_SYSTEM.md
  OPG_PROJECT_EXECUTION_BLUEPRINT.md
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  LICENSE                                    # only after license decision
  .gitignore
  .gitattributes
  environment/                               # chosen dependency lock + hardware record
  src/opg/                                   # reusable implementation; thin entry points
  tests/                                     # fixtures must be synthetic or permitted
  01_Project_Management/
  02_Literature/
  03_Datasets/
  04_Annotations/
  05_Preprocessing/
  06_Models/
  07_Experiments/
  08_Checkpoints/
  09_Evaluation/
  10_Figures_Tables/
  11_Writing/
  12_Documentation/
  13_Automation/
  14_Templates_Prompts/
  15_Archive/
```

## 2.2 Folder contracts

Every materialized domain folder has a README covering purpose, allowed contents, owner, inputs, outputs, storage sensitivity, commands/workflow, and links to this handbook. Do not create unused implementation frameworks merely to fill the tree.

| Home | Writes / reads | Allowed contents and contract | Forbidden / validation |
|---|---|---|---|
| `environment/` | Implementer / all executors | Chosen environment lock, runtime inventory, installation instructions; hardware/software record | No speculative pins advertised as tested; no credentials |
| `src/opg/` | Implementer / pipeline users | Data validation, annotation conversion, transforms, splitting, training, inference, evaluation modules | No image datasets, trained weights, hardcoded patient paths or hidden hyperparameters |
| `tests/` | Implementer / reviewer | Geometry, schema, split, metric, checkpoint, inference tests and permitted tiny fixtures | No unlicensed or identifiable patient fixtures |
| `01_Project_Management/` | Researchers / all roles | `decisions.csv`, `decision_log/`, `risk_register.csv`, `gates.csv`, `reviews/`, `diary/`, `meetings/`, `scope.md`, `dashboard.md`, `timeline.md` | No fabricated approval or raw clinical linkage data |
| `02_Literature/` | Literature lead / modeling and writing | `searches/`, `papers.csv`, `screening.csv`, permitted `papers/`, `summaries/`, `gaps.csv`, `claims.csv`, `references.bib`, `synthesis.md`, `research_questions.md` | No redistributing restricted PDFs; no source-free summaries |
| `03_Datasets/` | Data steward / annotation and modeling | `candidates.csv`, `datasets.csv`, `releases.csv`, `licenses/`, restricted `raw/`, `manifests/`, `reports/`, `splits/` | Raw bytes immutable and excluded from Git; no patient-key mapping in shared metadata |
| `04_Annotations/` | Annotation lead / dataset pipeline | `classes.csv`, `protocols/`, `annotation_registry.csv`, restricted `native/`, `exports/`, `reviews/`, `adjudications/` | No implicit class ordering, silent label replacement, or unreviewed labels called ground truth |
| `05_Preprocessing/` | Implementer / annotation and training | `preprocessing_registry.csv`, `specs/`, versioned `configs/`, `reports/`; restricted `processed/` | Reusable code belongs in `src/opg/`; no raw overwrites or test-fitted parameters |
| `06_Models/` | Model lead / evaluation and inference | `candidates.csv`, `model_registry.csv`, `baseline_plan.md`, `cards/`; pointers to weights | No anonymous checkpoints or unverified pretrained source |
| `07_Experiments/` | Experiment lead / evaluation and writing | `experiment_registry.csv`, `experiment_plan.md`, `EXP####/config.yaml`, `run_manifest.json`, logs, observations, conclusions, failure reports | Do not edit a launched config or merge distinct runs into one result |
| `08_Checkpoints/` | Experiment lead / recovery and inference | `checkpoint_registry.csv`, `checkpoint_policy.md`, checksums and restricted artifact pointers | Weight binaries live in approved artifact tier, not ordinary Git |
| `09_Evaluation/` | Evaluation lead / writing | `evaluation_registry.csv`, `protocol.md`, `freeze.md`, `EVAL####/` predictions, manifests, metrics, timing, analysis, reports | Sensitive outputs remain restricted; no test-driven tuning |
| `10_Figures_Tables/` | Analysts / writing | `assets.csv`, `specs/`, `data/`, `rendered/`, captions; generation commands reference scripts | No fabricated chart values, unlabeled axes, or identifying example images |
| `11_Writing/` | Authors / reviewers | `writing_registry.csv`, `thesis/`, `paper/`, `reviews/`, submission records; bibliography derived from canonical literature source | No unsupported novelty/clinical claims; no parallel conflicting citation databases |
| `12_Documentation/` | Implementer and researchers / new user | `installation.md`, `pipeline.md`, `prototype_guide.md`, `reproduce.md`, `reproducibility_audit.md`, data-access instructions | No duplicated scientific policy or promises unsupported by tests |
| `13_Automation/` | Implementer / all roles | Thin commands for registry checks, artifact verification, figure generation and orchestration | No independent hidden pipeline logic or automated scientific approval |
| `14_Templates_Prompts/` | Researchers / all roles | Approved blank templates, planning/implementation/review prompts, version log | Filled instances live in owning domain; prompts contain no patient data or secrets |
| `15_Archive/` | Release owner / authorized readers | Immutable release snapshots, `archive_manifest.csv`, receipts and retention instructions | No active drafts or overwriting released records |

## 2.3 Artifact placement and integration contracts

Code is centralized in `src/opg/`; domain folders contain specs, configurations, records, and outputs. Notebooks are optional thin callers in the relevant experiment or analysis folder. A local command-line or script-based prototype is sufficient unless UD18 chooses another minimal interface. No separate product architecture is required by the report.

Maintain this data lineage: `source → DS version → ANN version → SPLIT → PP → REL → EXP → CKPT/MODEL → EVAL → FIG/TAB → CLAIM → WR → release`. Deterministic pre-annotation preparation may occur before splitting, but fitted preprocessing and stochastic augmentation must occur only after split locking under Section 4. The split maps source identities so all derived images inherit their original partition.

Each conversion consumes explicit input manifests and emits a manifest containing parent identifiers, hashes, dimensions, coordinate mappings, and software/configuration versions. A downstream consumer rejects mismatched class maps, split IDs, or manifest hashes. An artifact pointer contains a stable object version and checksum, not a temporary signed URL as its only locator.

<a id="os-03"></a>
# 3. Literature and research-question workflow

## 3.1 Search design

PLANNING RECOMMENDATION: search both dental/medical and computer-vision sources. Candidate sources include PubMed, IEEE Xplore, Scopus or Web of Science if accessible, Google Scholar, publisher sites, and original repositories. Availability is unresolved; use accessible equivalents and document limitations. Do not require arbitrary paper counts or use citation popularity as a scientific-quality filter.

Seed query, to adapt and log per database:

```text
(orthopantomogram OR orthopantomography OR OPG OR "panoramic radiograph")
AND (dental OR tooth OR teeth)
AND ("object detection" OR localization OR localisation OR YOLO)
```

Run complementary queries for image quality, annotations, dental abnormalities, and terms discovered during reading. Search directly for existing YOLO OPG detectors, not only classification/segmentation papers. Record exact syntax, database, date, coverage window, language restrictions, filters, retrieved counts, exports, deduplication rules, and reasons for exclusions. Do not infer that an inaccessible source contains supporting evidence.

## 3.2 Intake, screening, and extraction

1. Register a record before summarizing it. Deduplicate DOI, normalized title, and linked preprint/final versions. Link duplicate versions; do not count them as independent studies.
2. Screen title/abstract, then full text, using prospectively approved inclusion and exclusion criteria. Record one explicit reason per full-text exclusion. Separate direct 2D OPG box-detection evidence from contextual studies using other tasks or modalities.
3. Retrieve legal full text and verify bibliographic metadata against the publisher/original paper. The report's references [1]-[13] are seed records, not automatically verified sources. The document-generation task has not conducted that external verification.
4. Extract the unit of analysis, patient/image counts as reported, dataset provenance, classes, annotation expertise, split level, possible leakage, detector/version, preprocessing, training settings, IoU definitions, AP implementation, speed hardware/boundary, uncertainty, code access, and limitations. Write `not reported` rather than filling gaps from familiarity with a library.
5. Inspect methods, tables, figures, supplements, and results before making a numerical claim. Keep a page/table locator for every extracted numerical result. Distinguish author-stated limitations from reviewer inference.
6. Reconcile disagreements through human review; preserve initial extraction and correction history. Update the claim ledger and synthesis together.

## 3.3 Research-gap verification

Retain the report's G1-G6 labels as source labels; project gap records use GAP#### and a `ReportGap` field to avoid confusion with project gates G01-G16.

| Report proposal | What the review must test | Possible honest outcome |
|---|---|---|
| G1: task-specific studies | Which dental classes and combinations existing OPG detectors actually cover | Broad coverage may already exist; narrow contribution to a justified reproducible comparison |
| G2: classification lacks spatial localization | Whether directly relevant literature supplies boxes, and under what conditions | Distinguish task differences without asserting all prior work is classification |
| G3: segmentation versus detection needs | Whether bounding boxes satisfy this project's approved use case | Task suitability, not a universal superiority claim |
| G4: CBCT versus OPG | Which evidence uses 3D/CBCT versus genuinely comparable 2D OPG data | Keep modality boundaries and avoid cross-modality performance rankings |
| G5: image-quality influence | Evidence for image quality effects and specific preprocessing benefits/harms | Treat enhancement as a testable factor, not an automatic improvement |
| G6: condition-specific detection and efficiency | Existing multi-object methods and their speed measurement protocols | Report contextual limits and any remaining feasible question |

For each gap record list supporting and contradicting papers, exact claim boundaries, search coverage, evidence quality, feasibility, and status: `proposed`, `supported-within-search`, `narrowed`, `refuted`, or `unresolved`. Multiple citations alone do not prove novelty. Never convert failure to find a paper into proof of absence. If the report's strongest novelty statement is refuted, retain the approved topic and seek a defensible narrower objective with the supervisor.

## 3.4 Question approval and living review

At STEP-009, connect each RQ to O1-O3, GAP records, dataset requirements, experiment factors, metrics, and intended claim limits. G03 requires a defensible objective and transparent gap assessment; it does not require proving that every proposed gap is true. Revisit the review before model selection, before manuscript submission, and after relevant new findings. Record search cutoff dates in writing.

**Literature acceptance:** reproducible search and screening, verified sources for used claims, extraction coverage, contradictory evidence, an approved RQ-to-evaluation mapping, and no unsupported novelty statement. **Failure handling:** quarantine unsupported claims, reacquire unreadable sources where lawful, revise the synthesis, and reassess G03. Do not silently delete a refuted hypothesis from the record.

<a id="os-04"></a>
# 4. Dataset, preprocessing, and split operating system

## 4.1 Lifecycle and permissions

`Discovery → access/ethics determination → controlled intake → raw integrity → quality inspection → class/protocol approval → annotation → label QA → preprocessing design → grouped split approval → derived release → training readiness`.

This operational ordering elaborates the report's workflow without test leakage: a fixed, reversible viewing/preparation transform can precede annotation, consistent with Figure 1; any statistics learned from images and all training augmentation follow split locking. Preserve source coordinates and the transform ledger across both phases.

Evaluate candidates on actual 2D OPG relevance, licensing, class label availability, annotation quality, patient grouping, provenance, image quality, population/site coverage, access stability, and computational feasibility. Record unknowns instead of scoring them as favorable. A popular repository is not the data owner. Do not merge mirrors as separate datasets or assume a downloadable archive grants redistribution rights.

The data card records collection purpose, modality, acquisition/source information when supplied, inclusion/exclusion, dates when known, population, measured patient/study/image/object counts, formats, de-identification, permissions, annotations, intended use, known missing metadata, biases, and access instructions. Do not infer demographics from images.

## 4.2 Intake and raw integrity

Verify source URLs/access receipts and archive hashes; extract to a new DS version in restricted storage. Inventory every file, including unreadable or excluded records. Record `ImageID`, source-relative locator, SHA-256, dimensions, file type, acquisition group where authorized, duplicate group, inclusion status, and exclusion reason. Keep the linkage to original filenames restricted if identifying.

Check image decoding, bit depth, grayscale/color interpretation, orientation, aspect ratio, corruption, overlays, identifiers burned into pixels, missing anatomy, blur, contrast, exposure, artifacts, and annotation compatibility. Use deterministic checks plus a documented dental/human visual sample. A decoder success alone does not establish relevance or diagnostic visibility. Do not establish filters after seeing which images the model gets wrong.

Counts must reconcile: acquired = retained + excluded + quarantined, with no double counting. Report patient count as unknown if it is unavailable. Store exact and near-duplicate findings separately; near matches need human review and group linkage. Repeated examinations of the same patient, different exports, crops, or contrast variants must not be treated as independent split units.

## 4.3 Preprocessing contract

For each PP#### record specify rationale, inputs, order, implementation version, every effective parameter, output dimensions/channel interpretation, deterministic or stochastic behavior, fitted state, geometry mapping, and verification. The diagram's contrast enhancement, noise reduction, resizing, normalization, and filtering are proposed operations, not mandates to apply arbitrary filters to every image.

PLANNING RECOMMENDATION: begin with the minimum preparation necessary for the selected YOLO implementation, preserve aspect ratio where feasible, and evaluate any additional enhancement as an explicit controlled factor. Do not erase small visible targets, distort morphology, alter left/right semantics, or silently discard boxes during cropping. Geometric augmentation must transform boxes identically and respect the class protocol. Record clipped/dropped boxes with approved rules and counts.

Learn any normalization statistics or data-dependent preprocessing on training data only; serialize that fitted state and apply it unchanged to validation/test. Fixed per-image operations do not use cross-partition statistics, but still require approval and versioning. Augmentation is training-only; never augment then randomly split the derived images. Validation/test processing is deterministic and matched to deployment inference.

Verification includes coordinate round trips, box overlays before/after transforms, bounds and positive areas, class preservation, aspect ratio/padding checks, and raw hash comparison. A threshold for acceptable geometry error belongs in UD09. If a transform damages target visibility or box alignment, freeze the bad derivative, create a corrected PP version, and invalidate affected releases and experiments.

## 4.4 Leakage-safe splitting

Start from the report's proposed **70/15/15** allocation. Apply grouping before image allocation: patient, study/examination, duplicate/near-duplicate family, and all derivatives of each source image. If multiple grouping relations overlap, use connected groups so a duplicate cannot bridge partitions. Patient-level grouping is preferred where metadata permits; a site holdout is a separate, justified generalization design, not a default requirement.

Record the split algorithm, actual seed, input manifest hash, grouping keys, target and actual counts/proportions, rounding, class/object/patient support, and exclusions. Grouping may prevent exact percentages. Explain discrepancies and obtain supervisor approval instead of breaking a group to force percentages. If a class has inadequate evaluation support, revise the feasible ontology or study design before freezing; never manufacture a minimum count.

A supplied benchmark split is not assumed safe. Audit its overlap and record comparability consequences before changing it. If patient IDs are unavailable, seek custodian grouping or conservative study/duplicate grouping, and document that patient independence cannot be fully established. G07 must not certify patient-safe evaluation without evidence; a revised, explicitly limited split claim requires supervisor approval. Unresolved material overlap blocks training.

Keep the final test partition sealed from model development: no hyperparameter choices, image-quality threshold tuning, checkpoint selection, class redefinition, or error-driven preprocessing based on test results. A data steward may audit test-label integrity using the preapproved protocol without revealing model-specific test performance. Log access. Train/validation inspection is allowed under the protocol; test access for final evaluation starts only after G11.

## 4.5 Versioned release and change control

A REL#### release manifest binds DS version, ANN version, class-map hash, SPLIT, PP configuration/fitted-state hash, image/label inventories, code revision, schema, and restricted storage locations. It records which objects were excluded and why. No derived release overwrites another.

| Change | Required action |
|---|---|
| Label correction | New ANN version; affected image IDs and justification; new REL; invalidate dependent comparisons as needed |
| Class definition or class-map change | New protocol/class-map version; review old labels; reassess G05-G08 and downstream results |
| Grouping or split change | New SPLIT and REL; reassess G07 onward; previous test observations remain disclosed |
| Preprocessing change | New PP/REL; rerun geometry checks; new EXP for a scientific comparison |
| Newly discovered unauthorized data | Stop use; restrict access; notify responsible human; follow institutional remediation and invalidate affected claims |
| Documentation typo | Patch with history; do not relabel data or rerun valid science unnecessarily |

**Dataset DoD:** authorized access, immutable inventory, reviewed quality, approved annotations, evidenced grouping, reproducible split, verified transforms, release linkage, and G04-G08 PASS for the relevant versions. **Recovery:** return to the earliest invalid parent artifact and regenerate descendants; retain superseded manifests and findings.

<a id="os-05"></a>
# 5. YOLO model and experiment operating system

## 5.1 Discovery and baseline policy

The report specifies the YOLO family, not a version, package, architecture scale, pretrained checkpoint, optimizer, image size, or training schedule. Discover candidates from verified original papers, official implementation documentation, and maintainable repositories. Record release/commit, detection task support, license, weight provenance, supported environments, configuration exposure, evaluator behavior, checkpoint support, resource needs, and limitations. Do not equate a library's name with the exact model implementation.

Choose a feasible, documented YOLO detection baseline after the class map and release exist. PLANNING RECOMMENDATION: establish one minimal, reproducible baseline before adding variations. Pretraining may be used if approved and licensed; record the source dataset/task and any known overlap risk. Do not claim a new architecture merely because a model was fine-tuned on OPG images.

Fair comparison invariants: same approved class definitions, reference labels, held-out split, metric implementation, comparison hardware/timing boundary, and evaluation policy. Match budgets and seed policy where relevant. If preprocessing or resolution is the intended factor, record that deliberate difference and keep the rest controlled. Comparisons with published studies using different data or AP conventions belong in a contextual table, not a numerical ranking of superiority.

## 5.2 Configuration contract

Every executable experiment configuration must resolve all required fields. Templates can contain nulls; launched configurations cannot. Capture both requested and effective library settings, including defaults and automatically altered batch/image sizes.

Required groups:

- Identity: EXP ID, research question, purpose, parent/comparison ID, source commit, timestamp, plan approval.
- Data: REL, DS/ANN/PP/SPLIT IDs, manifest and class-map hashes, partition paths, loader/conversion version.
- Model: exact YOLO implementation version/commit, architecture/scale, weight origin/hash/license, class count and mapping.
- Training: seed(s), determinism options, epochs or stopping budget, batch and image size, optimizer, learning-rate schedule, loss settings, warm-up, freeze/fine-tuning policy, augmentation settings, precision mode, workers, early-stopping rule and selection metric.
- Runtime: OS, language/runtime version, framework, acceleration library/driver, device, memory, distributed settings if used, dependency lock.
- Outputs: logs, checkpoints, retention/backup policy, prediction schema, model export settings, permitted storage destination.
- Evaluation: protocol hash, validation frequency, matching/AP settings, confidence/NMS settings, maximum detections, metric averaging and class-support handling.

The configuration validator checks required fields, numeric ranges, existing parent records, checksum agreement, permitted partition use, class-map consistency, storage availability, and unresolved placeholders. The evaluator must not quietly substitute a different default. Configuration changes after launch receive a new EXP ID; corrected descriptions can be appended without changing the original configuration.

## 5.3 Training lifecycle

`Register plan → verify gates and artifacts → validate effective config → load training/validation only → train → save checkpoints and logs → validate → preserve outputs → register model → review completion`.

The first end-to-end smoke test uses an approved training subset and validation sample. Confirm images and labels load correctly, losses and metrics are finite where defined, boxes align, checkpoints reload, and predictions serialize. A tiny-subset overfit check may diagnose pipeline defects; it is not a reportable generalization result. Do not access final test data for smoke testing.

Each EXP has one immutable scientific configuration. Each RUN is an execution attempt within that EXP. An exact resume of the same configuration can use another RUN ID linked to the prior checkpoint. Restarting from initial weights with a changed seed or budget is a new EXP unless a preapproved multi-run design explicitly groups those seeds and stores each complete configuration. Prefer separate EXP IDs per seed for straightforward traceability.

Log epoch, step, training and validation losses, evaluation settings, learning rate, timing, device/memory, warnings, errors, resource interruptions, and checkpoint events. Preserve all attempted runs, including OOM failures and diverged runs. A low validation metric does not justify deletion or retroactive reclassification as a smoke test.

## 5.4 Checkpoint and interruption management

Define immutable CKPT IDs and filenames including EXP, RUN, epoch/step, and role. `best` and `last` are pointers to immutable objects, not overwritten sole copies. Store hashes, file sizes, artifact locations, model/config hashes, epoch/step, monitored validation value, and available training-state components.

For exact-resume support, capture weights, optimizer, scheduler, precision scaler where applicable, epoch/step, random-number states, and implementation-specific state. Verify what the selected implementation actually saves. If it cannot restore full state, document the limitation and classify continuation as a restart/fine-tuning experiment rather than asserting exact resume.

Before a long run, simulate interruption on a small approved run, restore into the same environment, verify identity/state and continued logging, and confirm the backup can be fetched and hash-checked. Checkpoint frequency and retention are UD12/UD11 choices driven by time limits and storage. Keep best, final, and sufficient recovery artifacts according to the approved policy; retention decisions are logged and must preserve evidence needed for reported claims.

On corruption: quarantine the bad object; verify an independent backup; otherwise fall back to the last verified checkpoint and document lost work. Never reconstruct missing losses, epochs, or metric values. Never fabricate a completed run to keep a schedule.

## 5.5 Experiment matrix, model registry, and completion

For each planned comparison specify the RQ, one intended factor, controlled factors, budget, seed/repetition policy, validation selection criterion, anticipated failure modes, and interpretation of positive/null/negative outcomes. A hypothesis is an expected relationship, not a promised score. Choose any repeat count and statistical analysis before results, according to resources and inferential need.

Model records link to the exact EXP/RUN and CKPT, architecture/configuration, class-map and preprocessing dependencies, licenses, export/runtime, evaluation IDs, and intended use. Register exports separately if precision or inference backend changes predictions. Test exported versus source-model predictions within a prospectively chosen tolerance before using export timing as the reported model's speed.

G10 is assessed for each qualifying run, not just the first baseline. An interrupted or invalid run remains documented but does not become eligible for final model selection. An approved early-stopped run can be complete if its stopping rule, logs, and checkpoint evidence are intact. STEP-030 repeats STEP-027-029 for approved experiments; do not duplicate steps or recycle IDs.

<a id="os-06"></a>
# 6. Annotation governance and quality assurance

## 6.1 Class ontology and responsibility

The report's examples (teeth, impacted tooth, cavities, lesions, restorations) establish candidate concepts only. UD04 must settle the final set and whether each can be reliably identified and localized on the available 2D images by the approved annotators. No numeric class IDs, tooth-numbering scheme, lesion taxonomy, or diagnosis is preassigned here.

For every accepted class define: stable class ID and display name; target concept and visible evidence; unit of annotation; inclusion and exclusion; box boundary convention; partial visibility; overlap/nesting; multiple objects; ambiguity; minimum visibility/quality; out-of-scope appearances; positive, negative, and borderline examples; reviewer qualification; source and approval version. If tooth numbering or laterality is adopted, specify the convention and transform constraints explicitly.

Distinguish a visible feature from a clinical diagnosis requiring information not available in OPG. Do not label an uncertain region as a disease merely because a model or unqualified annotator suggests it. Record `uncertain` or `needs_adjudication` as review states, not automatically as trainable object classes. A negative image is negative only for the approved annotated targets after complete review.

## 6.2 Annotation protocol and data representation

Choose and version the tool, native representation, export representation, coordinate origin, units, box geometry, edge inclusivity, rounding, clipping, and class ordering. YOLO-compatible normalized center-width-height text is a possible export, **not a format specified by the report**. If adopted, document how source pixel coordinates map to normalized values and back; pin parser and exporter versions. Native editable annotations must be retained independently of a training export.

The protocol must resolve:

1. Which image version annotators view and which coordinate system is authoritative.
2. Whether overlapping boxes and a normal structure with an associated abnormality can coexist, and how the evaluator treats them.
3. Treatment of truncated, obscured, tiny, ambiguous, artifact-covered, and out-of-scope targets.
4. Whether the dataset is exhaustively annotated for all classes; how unassessed regions/images are quarantined or ignored in a supported, documented evaluator.
5. Definitions of missing labels, reviewed empty labels, invalid labels, and excluded images.
6. Adjudication roles, disagreement logging, and rules for correcting an already released annotation.
7. Access controls and a prohibition on uploading medical images to unapproved annotation services.

## 6.3 Pilot, production, and review

Before production, independently annotate a prospectively selected pilot covering available classes, image-quality variation, overlap, and ambiguous cases. The sample size and coverage criterion are UD06, not invented here. Compare object presence, class agreement, matched-box IoU distribution, missed/extra objects, and disagreement types under a defined matching rule. High box IoU alone does not prove correct or complete clinical labeling.

The qualified reviewer adjudicates discrepancies, refines the protocol, and determines whether the pilot meets prospectively approved thresholds. If the protocol changes, recheck previously labeled pilot items against the new version. Record examples and reasons. Production annotation begins only after documented pilot acceptance and G05 still applies to the current protocol.

Production batches receive ANNB#### identifiers and are tracked with assigned images, annotator, protocol/tool version, completion/review state, QA sample membership, and timestamps. Model-assisted labels, if approved, require independent review and recorded assistance provenance; pseudo-labels are not silently treated as reference ground truth. Review both positive and negative images to detect systematic omissions.

## 6.4 Integrity and release checks

Automated checks: expected image-label correspondence, unique identifiers, permitted class IDs, finite coordinates, positive area, in-bounds geometry, duplicate boxes, orphan labels, reviewed-empty status, and export round-trip consistency. Visual QA checks tightness, target identity, completeness, transformed alignment, ambiguity handling, and class-map interpretation.

Use class/quality-stratified review and document its sampling frame, random seed where used, coverage, observed error rates, agreement measures, and adjudication counts. Sampling cannot prove all labels correct; state residual uncertainty. The QA threshold and escalation rule must be approved before assessing production batches. Do not lower the threshold after seeing poor agreement.

G06 requires all material annotation issues resolved or excluded under a preapproved rule, no invalid training/evaluation labels, an immutable ANN release, and independent review evidence. Where clinical annotation support is unavailable, mark **Unresolved / Human Decision Required** and stop production labeling of those targets. Do not substitute AI assurance for qualified review.

**Recovery:** quarantine affected batches, find the earliest faulty rule/tool version, reannotate or adjudicate, issue a new ANN version, regenerate exports, rerun integrity checks, and invalidate dependent releases. A test-label correction after testing must be disclosed, with a new evaluation ID and unchanged frozen model; it cannot justify retraining and pretending the test remained unseen.

<a id="os-07"></a>
# 7. Evaluation protocol

## 7.1 Protocol before training; freeze before testing

Draft the evaluation protocol with the baseline plan, resolve required settings at G09, and freeze final model/checkpoint, PP, class map, thresholds, metric code, and planned analyses at G11. The freeze record contains hashes and decision evidence. Training/evaluation leads confirm no final-test feedback influenced selection. Tuning ends before final-test predictions are produced.

Use one EVAL#### per model/partition/protocol execution. Store image-level coverage separately from object-level detections: an image with zero predicted boxes still needs an evaluated-image record. Record failures explicitly; do not silently omit unreadable or failed images from denominators. Follow the preapproved failure/exclusion rule and report counts.

Prediction schema includes ImageID, MODEL/CKPT/EVAL IDs, class ID, score, box coordinates in a documented reference frame, preprocessing/inverse mapping, and runtime metadata. Ground truth links to the exact ANN/REL. Validate IDs, class map, finite scores and boxes, coverage, hashes, and inverse geometry before computing metrics.

## 7.2 Required detection metrics

Define IoU as intersection area divided by union area of predicted and reference boxes, using the chosen coordinate convention. For an agreed class-aware, confidence-ordered one-to-one matching procedure, a detection can match at most one eligible ground-truth object and each ground-truth object at most one detection at a given IoU threshold. An unmatched prediction is FP; an unmatched eligible ground-truth object is FN. Duplicate detections are not multiple true positives. Ignored/uncertain regions need an explicit compatible rule.

| Required measure | Definition / primary reporting | Settings that must accompany it |
|---|---|---|
| Precision | TP / (TP + FP), at the frozen operating point | Confidence cutoff, matching IoU, NMS settings, class/overall aggregation, denominators |
| Recall | TP / (TP + FN), at the same frozen operating point | Same settings and eligible ground-truth support |
| mAP@0.5 | Mean across eligible approved classes of AP at matching IoU = 0.50, as proposed in report Figure 1 | Evaluator/version, AP integration/interpolation, class set, score floor, maximum detections, NMS, ignore policy |
| Inference speed | FPS plus measured latency under the specified runtime and boundary | Device, runtime, precision, batch/image size, warm-up, repetitions, inclusion of processing/transfers/NMS/I/O |

AP uses a precision-recall curve formed by ranking predictions over confidence thresholds, not merely the Precision/Recall pair at a single deployment cutoff. Retain the predictions needed for that curve. Do not discard low-score predictions at an aggressive display threshold and then report the truncated curve as standard AP. State the metric collection score floor separately from the selected operating-point threshold.

Matching IoU for AP, matching IoU for operating-point Precision/Recall, and suppression IoU for NMS are different settings. Only AP@0.50 is explicitly supplied by the diagram; resolve other values in UD13. Do not label a generic library field `mAP` without confirming exactly what it computes.

Report per-class AP/Precision/Recall, target/object support, number of images, number of patients/groups when known, and aggregate rules. If TP+FP is zero, Precision is mathematically undefined; if TP+FN is zero, Recall is undefined. Record N/A and the denominator plus the software's aggregation convention. For absent ground-truth classes, state the AP/mAP eligibility rule, excluded classes, and resulting class count; never silently assign a favorable zero or omit a hard class. Do not aggregate incompatible class ontologies.

## 7.3 Timing protocol

PLANNING RECOMMENDATION: report both model-only execution and end-to-end image-to-box latency if feasible, with separate labels. At minimum, the chosen boundary must be explicit and the report's FPS measure must be reproducible. Include or exclude decoding, resize/normalization, host-device transfer, model forward pass, NMS/postprocessing, drawing, disk I/O, and model-loading time explicitly. Report cold-start loading separately if measured.

Use the actual recorded hardware; specify CPU/GPU, memory, OS, framework, driver/accelerator, device power/settings if controlled, backend, precision, image size, batch size, and concurrency. Perform a predeclared warm-up and repeated timed measurements. Synchronize asynchronous accelerator work at timing boundaries using the chosen framework's appropriate mechanism. Record raw elapsed times, processed image counts, failures, and run order.

Compute throughput as successfully processed images divided by the corresponding measured duration, with failures disclosed. Single-image FPS can be derived from latency only under the stated serial single-image workload; batch throughput is not interchangeable with patient-facing latency. Report mean and median latency and a tail statistic if the sample supports it; specify variability and units. No FPS target or clinical real-time claim is set by the report.

## 7.4 Recommended analyses, not report requirements

These require explicit adoption under UD15 and an analysis plan before final testing:

- **mAP@0.50:0.95:** mean AP over IoU thresholds 0.50, 0.55, ..., 0.95 with implementation convention stated; complements rather than replaces required mAP@0.5.
- **PR curves and class-aware error counts:** identify confidence tradeoffs and localization/classification failures. Any threshold choice uses validation only.
- **Uncertainty estimates:** patient/group bootstrap where grouping exists, rerunning metric computation per resample; disclose unit, repetitions, interval method, seed, and small-sample limitations. Image-level independence cannot be asserted when patients repeat.
- **Repeat-seed sensitivity:** report every planned seed and aggregate variation, not the best seed alone. Separate training variability from uncertainty due to the finite test sample.
- **Controlled preprocessing or resolution ablations:** predefine changed factors and matched comparison protocol; no post-test search for improvements.
- **Quality/source subgroups or external evaluation:** only where metadata, compatible annotations, permissions, and sufficient support exist. An internal split does not demonstrate cross-hospital generalization.

Do not transplant classification-specific statistical tests without checking their assumptions for correlated multi-object detections. Superiority claims need an appropriate paired design, effect size, uncertainty, and adjustment/qualification for multiple comparisons. If data or resources do not support inferential claims, present descriptive results honestly.

## 7.5 Error analysis and limitations

Use a prospectively defined sampling strategy that includes successes, missed targets, spurious boxes, duplicate detections, incorrect classes, and localization errors. Record EVAL/ImageID/target identifiers, error category, observable image features, reviewer, and possible explanations. Assess small or overlapping targets, low contrast, blur, dental materials/artifacts, truncation, ambiguous labels, and source variation only when observed. Never turn an error category into an established causal mechanism without evidence.

Discuss label uncertainty, dataset selection and size, class imbalance/support, missing patient metadata, single-site or hardware limits, preprocessing effects, restricted external validity, and retrospective research design as applicable. Distinguish measured limitations from untested risks. The report's proposed supplementary use remains an aspiration; detection metrics alone cannot validate diagnosis, treatment benefit, reduced workload, or clinician replacement.

## 7.6 Evaluation failure and correction

If prediction coverage or evaluator tests fail, mark the evaluation invalid and repair the implementation before reporting. Preserve original outputs and issue a new EVAL linked to the correction. Disclose whether the correction was methodological or a software bug. If test results prompt a new model, treat the old test as development-exposed: obtain a genuinely untouched approved test source or clearly report the new analysis as exploratory. Reassessment cannot erase exposure history.

G12 requires all four required metrics under a complete protocol, failure counts, frozen-model traceability, and adopted analyses or documented deviations. It does not require a high score. G13 requires supported error analysis and appropriately bounded conclusions.

<a id="os-08"></a>
# 8. Research prototype and reproducibility

## 8.1 Minimal prototype contract

Implement only a research inference path that accepts an approved 2D OPG input, validates it, applies the registered deterministic preprocessing, loads a registered model, produces class-labeled boxes with scores, maps boxes to the original reference image, and exports a structured result. A script or command-line entry point with optional box overlay is a sufficient recommendation. The report does not require a hosted application.

Outputs include model/checkpoint and preprocessing versions, class-map version, source revision, input identifier, timing boundary, and processing status. Explain zero detections, unsupported input, corrupted input, missing model, invalid class map, and resource failure clearly. Zero detections is a valid technical outcome, not a negative diagnosis. Avoid retaining patient inputs beyond approved research policy.

A model export is accepted only after reload and output compatibility checks. If changing precision/backend changes outputs beyond the approved tolerance, register it as a different evaluated inference artifact. A visually convincing demonstration is not a substitute for held-out metrics.

## 8.2 Reproducibility levels and audit

Distinguish: (a) reloading the archived model and reproducing predictions/metrics; (b) retraining from the recorded initial state/configuration; and (c) reproducing conclusions under expected nondeterminism. Declare which levels were attempted and what agreement tolerance was prospectively accepted. Do not promise bitwise training determinism across hardware that was not tested.

The audit in STEP-038 uses a clean authorized environment or a demonstrably fresh environment, retrieves artifacts by manifest, verifies checksums, follows written commands, regenerates metrics and representative figures, and compares results under documented tolerances. Recheck the release class map, split, training configuration, evaluator, and inference timing setup. Reproduction cannot depend on unrecorded notebook state or a private chat history.

If data cannot be shared, provide lawful access instructions and restricted audit evidence. Restricted access is not an excuse to fabricate public reproducibility; state what an external reader can and cannot reproduce. G14 fails on missing essential artifacts or unexplained disagreement. Repairs generate new artifact/evaluation versions and appropriate downstream review.

<a id="os-09"></a>
# 9. Writing and submission operating system

## 9.1 Evidence-first writing

Maintain one claim ledger at `02_Literature/claims.csv` and one writing registry at `11_Writing/writing_registry.csv`. Claims can be literature-supported, experiment-supported, decision-based descriptions, proposed, contradicted, or unresolved. Every substantive factual sentence must be traceable to a source location or artifact; purely connective prose does not need an artificial citation.

Draft background and planned methods while experiments proceed, labeling them as plans. Write realized methods from actual configurations and results only after the relevant evidence exists. Clearly separate planned, performed, and exploratory analyses. Do not write plausible-looking result tables as placeholders. Use `Evidence pending` during drafting and resolve or remove it before submission.

## 9.2 Thesis and paper structure

PLANNING RECOMMENDATION, subject to institutional format: Introduction and objectives; Literature review and gap assessment; Dataset and annotation; Methodology and implementation; Experiments and evaluation; Results; Discussion and limitations; Conclusion and future work; References and appendices. Combine chapters if required, while retaining evidence coverage.

| Writing unit | Required input | Completion condition |
|---|---|---|
| Introduction / gap | Approved O1-O3/RQs, verified literature, GAP records | Bounded motivation; no unsupported claim that prior OPG detectors do not exist |
| Dataset / annotation | DS/ANN/REL cards, permissions, quality and split audits | Counts reconcile, definitions and reviewer roles are clear, missing metadata disclosed |
| Methods | Actual code/configuration, PP/model/selection protocol | Another researcher can reconstruct the procedure; defaults and deviations explicit |
| Results | Valid EVAL records and traceable figures/tables | Required metrics, supports, uncertainty if adopted, failures and negative comparisons included |
| Discussion | Results, error review, comparison limits | Observations separated from hypotheses; no unwarranted clinical utility claim |
| Conclusion | Approved objectives and realized evidence | States what was learned, including limitations; no new results |
| Appendices / supplements | Locks, schemas, protocols, access instructions | Lawful, sufficient reproducibility detail and no identifying leakage |

A paper uses the same frozen evidence base in a more concise, venue-appropriate form. Paper destination, timeline, authorship, and requirement are UD17. Prepare the pathway; do not make project completion depend on journal acceptance. If paper submission is not required or is deferred, record the approved disposition rather than claiming submission occurred.

## 9.3 Figures, tables, and citations

Assign FIG#### and TAB#### IDs to specs and assets. Record source EVAL/EXP/data hash, generating script/version/command, units, aggregation, caption, permissions, and manuscript location. Generate plots from recorded values, inspect rendered outputs, and keep scripts and source data. Human reviewers validate interpretation and any medical examples. There is no requirement that all figures be manually rendered.

Verify every citation against the original source and canonical bibliography. Preserve report reference numbers as `ReportRef` metadata, not as permanent thesis numbering. Correct metadata only with evidence. The report has textual/encoding irregularities and an escaped publisher string in its references; do not silently copy them as verified metadata. Do not invent a DOI or claim that a source was read when only its abstract was available.

## 9.4 Revision and submission

Run technical review, evidence/claim review, citation verification, terminology/numbering consistency, formatting, grammar, and supervisor review. Track each comment with source, date, exact comment, interpretation, action, changed location, evidence, response, owner, and status. The supplied blank feedback page generates no invented action items.

Before submission confirm actual institutional/venue requirements, approvals, authorship, disclosures, similarity policy if applicable, figure permissions, availability statements, final document rendering, and required supplementary artifacts. Retain approved final file hashes and submission receipts. A prepared file is not a submitted file; a submitted manuscript is not an accepted one.

Post-review experiments reenter the relevant gated steps with new IDs. Archive every submitted version, response, and revision without overwriting earlier records. G15 is assessed separately for each document: `G15 / thesis` at STEP-042 blocks thesis submission at STEP-043; `G15 / paper` at STEP-044 blocks paper submission within that step. Thesis readiness never depends on a paper not yet drafted. Paper readiness checks that manuscript, its supplements, verified claims/citations/figures, venue requirements and author/supervisor approval. If paper submission is explicitly not required or deferred, record its approved disposition instead of asserting a paper-readiness PASS. G16 requires thesis readiness/submission plus either paper readiness/submission when required or the approved paper disposition. Store distinct AssessmentIDs, using EntityVersions to identify the document/version.

<a id="os-10"></a>
# 10. Version control and artifact storage

## 10.1 Right-sized source control

PLANNING RECOMMENDATION: use Git for source, text configurations, non-sensitive registries, documentation, small approved aggregate metrics, figure/table specifications, and artifact pointers. Select the remote and access level under UD11; no particular cloud provider is mandated. For a small team, a protected main branch with short-lived task branches and review is sufficient; an integration branch is optional.

Commit a coherent unit with a meaningful prefix such as `docs:`, `research:`, `data:`, `annotation:`, `experiment:`, `evaluation:`, `writing:`, or `fix:` and the relevant entity/step ID. Record source revision before execution. Avoid a self-referential requirement that a config contain the hash of the commit which first contains that config: use the code revision plus a separate configuration hash and run manifest.

Review diffs for identifiers, images, restricted metadata, secrets, licenses, and large binaries before any push. Ignore rules do not protect files already tracked. Never upload medical data or sensitive predictions to a public remote simply because a template recommends synchronization. A source-control commit does not replace an artifact backup.

## 10.2 Storage tiers

| Tier | Contents | Policy |
|---|---|---|
| Source | Code, permitted text records, config, documentation | Git with approved remote/access; review before sync |
| Restricted data | Raw/derived images, native/export labels, patient grouping/linkage | Institutionally approved encrypted/access-controlled storage; separate linkage permissions; no ordinary Git |
| Research artifacts | Checkpoints, models, full predictions, timing samples, private visual examples | Approved versioned artifact store; classify sensitivity; hashes and authorized backup |
| Release/archive | Submission files, source snapshot, permitted aggregates, artifact manifest | Immutable snapshot; public subset only after license/privacy approval |

`.gitignore` should cover restricted raw/processed/annotation exports, binary checkpoints, environment directories, caches, logs that may contain identifiers, notebook outputs, credentials, and private linkage files. Use explicit controlled exceptions for safe small records; do not broadly ignore all evaluation evidence and then lose it. An artifact manager or LFS can be adopted if useful and permitted; neither is a requirement of the report.

## 10.3 Environment readiness in two phases

STEP-002 establishes and tests a minimal environment for registry checks, read-only image inspection, annotation conversion, splitting and preprocessing before those tools are executed. Record actual runtime/package/tool versions, installation commands and a dependency lock under `environment/data/`, plus smoke checks on synthetic or permitted fixtures in `environment/data/verification.md`. Do not select a YOLO version or GPU stack here. G02 requires this basic tooling evidence. Add dependencies only when needed; pin and test them before their first use and retain each environment revision.

STEP-023 creates the model-specific training/inference/evaluation environment under `environment/model/` after YOLO selection. Preserve the earlier data-tool lock and each PP/REL’s recorded environment hash; do not silently overwrite it. If consolidation or upgrades change preprocessing outputs, recheck geometry, hashes and counts, create new PP/REL versions where scientifically material, and reassess G08 before training. This separates early executable data work from later model-stack hardening without adding or renumbering steps.

## 10.4 Synchronization and recovery

Before remote compute: verify source/config revision, authorized data access, input hashes, environment, output location, disk budget, and checkpoint retrieval. During compute: persist logs/checkpoints to the approved store. After compute: verify uploaded artifact hashes and a retrieval sample, then update registries and source metadata. Ephemeral runtimes are never the sole copy.

Back up each storage tier according to approved retention and access policy. Test restoration at checkpoint smoke testing, reproducibility audit, and archival. If a credential or patient record leaks, stop distribution, involve the authorized institutional owner, rotate affected credentials where applicable, and perform controlled remediation. History rewriting or deletion of research evidence requires a specific remediation plan; do not erase failed work to clean the repository.

<a id="os-11"></a>
# 11. Roles and human decisions

Roles describe responsibilities; they do not require a separate person or autonomous agent for every row. A small team can hold multiple roles, but scientific approval and annotation adjudication must be explicit. AI assistance does not supply clinical qualifications or independent validation by itself.

| Role | Responsibility | Decision boundary |
|---|---|---|
| Researchers | Plans, registries, code, experiments, writing, coordination | Propose scientific decisions; record actual approvals |
| Supervisor / co-supervisor | Scope, objectives, feasibility, methodological and submission review | Ratify scientific changes and contribution claims |
| Data custodian / ethics authority | Access, linkage, consent/waiver, storage and sharing | Approve lawful medical-data use; no assumption of approval |
| Qualified dental reviewer | Class labelability, annotation examples, disagreements, clinical wording | Approve annotation protocol and adjudicate ambiguous targets |
| Implementer | Build reviewed data/model/evaluation functions | Cannot silently change classes, splits, or evaluation protocol |
| Evaluation reviewer | Freeze checks, evaluator validity, evidence review | Cannot tune against final-test results |
| Writing/release owner | Claim/citation audit, final files, receipts, archives | Cannot assert submission or acceptance without evidence |

Human-task handoff: state the question, why evidence is needed, options and consequences, responsible person, blocking step/gate, required record/path, and verification method. Stop only dependent work; continue independent literature/documentation where allowed. Preserve a decision once authorized unless new evidence invalidates it. Never repeatedly ask for the same approval without a changed basis.

AI-assisted task contract: objective, source inputs, allowed paths, prohibited changes, output schema, tests/checklist, uncertainty labels, human boundary, and recovery. Verify generated citations, code, labels, and prose against sources. Do not place patient data in prompts to unapproved services. Repository records, not transient conversations, carry durable project decisions.

<a id="os-12"></a>
# 12. Daily research operations

**Start:** read dashboard, last session note, current gate statuses, pending decisions, artifact availability, and Git status. Choose one bounded work unit from the blueprint whose prerequisites are evidenced. Record its inputs and success criteria before starting.

**Work:** plan/review, execute, inspect results, document anomalies, and update the owning registry. For repetitive annotation, reading, or training, use dated batches or RUN records under the existing step rather than pretending a large activity is one short session.

**Close:** save verifiable output, run the relevant checks, preserve failed attempts, update decisions/risks/gates, synchronize only permitted material, and record the next unblocked action. If nothing completed, record the blocker and evidence; do not invent progress to satisfy a productivity target.

Weekly review covers RQ alignment, literature changes, data/annotation coverage, compute budget, invalidated artifacts, open UD items, gate blockers, writing evidence, and backup health. Milestone review updates provisional estimates using actual annotation throughput, run duration, review turnaround, and external deadlines. No fixed project completion date is asserted here.

Initial risk themes: unavailable permissions; insufficient labelability or reviewer time; missing patient grouping; small/imbalanced class support; corrupted data; preprocessing damage; compute interruption; test exposure; citation errors; overstated clinical claims; artifact loss. Record probability/impact assessments only when the team evaluates them, with owner, trigger, mitigation, contingency, and next review date.

<a id="os-13"></a>
# 13. Quality gates and completion

## 13.1 Assessment semantics

Every gate is **PASS or FAIL when assessed**. Initial state `NOT ASSESSED` and invalidated state `STALE` are not passes and block dependent work. PASS requires all mandatory criteria, evidence paths/hashes, assessor/date, affected entity versions, and human sign-off where specified. Missing evidence is FAIL, not conditional PASS. Optional analyses may be explicitly not adopted before execution; mandatory report metrics cannot be waived as optional.

Store assessments in `01_Project_Management/gates.csv` and detailed `reviews/G##_assessment_<date>.md`. A checklist below describes a future assessment, not a checked result. Reassess the gate whenever a material parent artifact changes; mark descendants STALE. A writing-quality audit never certifies scientific validity on its own.

## 13.2 Canonical gate matrix

| Gate / owning step | PASS evidence and mandatory criteria | FAIL / blocked transition | Human reviewer |
|---|---|---|---|
| G01 Scope and objectives / 001 | Exact title; report facts separated from proposals; scope/O1-O3 recorded; UD owners and deadlines; actual feedback status | Scope drift or invented approval; blocks repository policy adoption and research protocol work | Supervisor + researchers |
| G02 Repository readiness / 003 | Folder/registry/template contracts, source-availability history, ignore/access policy, identifier checks, storage decision, tested minimal data-tool environment | Missing canonical homes or unsafe storage; blocks operational artifact production | Research lead |
| G03 Literature and gap / 009 | Logged search/screening; original-source verification for used claims; supporting/contradicting evidence; approved RQs and bounded gap conclusion | Unsupported novelty or missing required sources; blocks dataset selection as a final scientific decision | Supervisor |
| G04 Dataset access/relevance/quality / 013 | Permissions/ethics determination, provenance, immutable hashes, measured inventory, quality report, exclusions and approved selection | Unauthorized use, irreconcilable inventory or unsuitable images; blocks production annotation | Custodian + researchers |
| G05 Classes and protocol / 015 | Approved ontology, visibility/ambiguity/negative rules, coordinate/export contract, reviewer roles, prospective QA thresholds | Undefined targets or absent competent review; blocks pilot/production protocol use | Dental reviewer + supervisor |
| G06 Annotation quality/integrity / 018 | Accepted pilot, reviewed production batches, structural/visual QA, adjudications, frozen ANN/class-map hashes | Unresolved material labels/omissions or failed thresholds; blocks derived release | Dental reviewer |
| G07 Leakage-safe split / 020 | Audited grouping/duplicates, deterministic manifest, target/actual proportions, class support, test custody; approved handling of metadata limits | Material cross-partition overlap or unsupported independence claim; blocks release/training | Supervisor + data lead |
| G08 Preprocessing/release integrity / 021 | Raw unchanged, geometry/visibility checks, training-only fitted state, augmentation isolation, REL manifest/checksums | Damaged boxes/targets, test-fitted processing, mismatched labels; blocks baseline use | Data/model leads |
| G09 Baseline readiness / 026 | Approved YOLO/weights/licenses; pinned tested runtime; baseline/evaluation/timing plan; resolved configs; smoke and checkpoint restore evidence | Missing settings, invalid loader/evaluator, no recovery evidence; blocks full training | Researchers + method reviewer |
| G10 Experiment completion/checkpoints / 029, repeated at 030 | Valid stopping, complete logs/config, verified checkpoints and exports, registry/model card, all attempts preserved | Missing state, invalid training or silent loss; blocks candidate eligibility | Experiment reviewer |
| G11 Final-test release / 031 | Completed comparison matrix, validation-only selection, model/protocol/threshold hashes frozen, test-access history reviewed | Test-informed selection or unfrozen analysis; blocks final-test execution | Supervisor + evaluation reviewer |
| G12 Final evaluation/metrics / 035 | Valid coverage and matching; Precision/Recall/mAP@0.5/FPS with settings/supports; timing samples/hardware; adopted analyses and deviations; traceable report | Missing required metric, ambiguous IoU, selective omission or invalid evaluator; blocks final result claims | Evaluation reviewer |
| G13 Errors and limitations / 036 | Systematic case review, label/error distinctions, reviewer evidence, bounded limitations and clinical wording | Cherry-picked examples, unsupported causes or utility claims; blocks final conclusions | Dental reviewer + supervisor |
| G14 Reproducibility / 038 | Fresh-environment evidence; artifact retrieval/checksums; predictions/metrics regenerated; declared training reproducibility level; documented tolerances and limits | Missing artifacts, unrecorded state or unexplained discrepancy; blocks submission readiness | Reproduction reviewer |
| G15 Document-specific submission readiness / 042 thesis; 044 paper if submitting | Complete relevant document and supplements; citation/claim/figure checks; actual institution or venue requirements; review responses and author/supervisor approval, separately evidenced for each document/version | Missing evidence blocks only that document’s submission; thesis does not await paper drafting. Approved paper deferral is a disposition, not a PASS | Supervisor + authors |
| G16 Project completion / 046 | All applicable prior gates current; thesis receipt, paper disposition, source/artifact archive, access/retention and restore proof, deliverable inventory | Missing required submission/evidence/archive; blocks completion declaration | Researchers + supervisor |

## 13.3 Gate failure and recovery

Record failed item, evidence, affected artifacts, corrective action, owner, and retest. Return to the earliest responsible step, not automatically to the start of the project. Preserve the failed assessment and append a new assessment. A low score is not gate failure unless a prospectively approved scientific success target applies; even then report the valid negative result and discuss objective attainment honestly.

Project completion means documented fulfillment of the approved deliverables and honest conclusions, not a positive hypothesis or publication acceptance. Final deliverables: source and environment record; authorized dataset/annotation/preprocessing/split pipeline and manifests; complete experiment and checkpoint records; registered models; valid evaluation and error reports; reproducibility and prototype guide; thesis submission; paper package/submission or approved disposition; immutable archive and recoverable backups.

<a id="os-14"></a>
# 14. Template library

## 14.1 Template contract and use

The following templates are usable field specifications, to be materialized in `14_Templates_Prompts/` by STEP-003. They are deliberately unfilled. Each includes a common header: `TemplateID, template_version, entity_id, owner, date, status, source_inputs, governing_section, sensitivity, reviewer`. Use `Unresolved / Human Decision Required` for unresolved choices and `not reported` for missing source information. Empty example fields are not approvals or observations.

Instances belong to their domain folder; templates remain blank and versioned. Required fields must be completed or explicitly justified as not applicable. Registry-backed fields must match Appendix B. Scientific decision, annotation, and gate templates require the named human review; mechanical validation alone is insufficient.

## 14.2 Operational templates

| ID / template | Purpose / instance location | Required body fields | Verification / common mistake |
|---|---|---|---|
| T01 `readme.md` | Explain a folder / each materialized folder | Purpose; owner; inputs; contents; workflow/commands; outputs; sensitivity; related paths; governing section | Matches actual contents; avoid duplicating this handbook |
| T02 `decision.md` | Resolve a UD/scientific choice / `01_Project_Management/decision_log/DEC####.md` | UD reference; question; source facts; options; evidence; tradeoffs; recommendation; actual human decision; date; approver; rejected options; affected artifacts/gates; review trigger | No invented decision; preserve superseded entries |
| T03 `session.md` | Daily plan and closeout / `01_Project_Management/diary/` | Step/batch; objective; prerequisites; intended outputs; actual outputs; checks; blockers; decisions; artifact sync; next action | Actual work separated from plan |
| T04 `search.md` | Repeatable search / `02_Literature/searches/` | Database; exact query; date; coverage; filters; counts; export/pointer; dedup; supplementary search; limitations | Reproduce retrieval strategy, not an assumed result count |
| T05 `paper_summary.md` | Grounded extraction / `02_Literature/summaries/P####.md` | Verified citation; question/task/modality; data/counts; annotation; split; model; preprocessing; training; metrics/IoU; timing/hardware; results with locators; limitations; critique; reuse; conflicts; unresolved fields | Source-read evidence and locators; no result guessed from abstract |
| T06 `gap.md` | Test a proposal / `02_Literature/gap_notes/GAP####.md` | ReportGap; proposed statement; search coverage; supporting and contradicting P IDs; independence; feasibility; narrower interpretation; status; approved RQ links | Search absence is not proof of novelty |
| T07 `claim.md` | Trace scientific assertions / `02_Literature/claim_notes/CLAIM####.md` | Exact statement; scope; evidence IDs/locators; contradictions; uncertainty; permitted wording; verification; writing locations | Do not cite a proposed experiment as evidence of its result |
| T08 `dataset_card.md` | Document source and limitations / `03_Datasets/reports/DS####_card.md` | Origin/version; access/license/ethics; modality; population known/unknown; collection; patient/image/object counts; quality/exclusions; duplicates/grouping; annotations; biases; intended use; access/retention; hashes | Measured counts and permission evidence; no assumed patient independence |
| T09 `class_protocol.md` | Govern annotation / `04_Annotations/protocols/` | Class table; reference image; geometry/schema; visibility and negative rules; overlap; ambiguity; examples; tool/export; qualifications; pilot/QA sampling and thresholds; adjudication; version | Final class list approved, not copied from diagram examples |
| T10 `annotation_batch.md` | Track labels / `04_Annotations/reviews/ANNB####.md` | Image membership; annotator; tool/protocol; assistance; start/end; native/export hashes; QA selection; agreement/errors; adjudication; acceptance | No batch accepted without required review |
| T11 `preprocessing.md` | Specify/reproduce a PP / `05_Preprocessing/reports/PP####.md` | Rationale; ordered transforms; parameters; fit partition/state; geometry; data dependencies; output counts/hashes; test results; visual QA; limitations | No test-fitted normalization or unlabeled dropped boxes |
| T12 `split.md` | Approve partition / `03_Datasets/splits/SPLIT####/report.md` | Input hash; grouping; duplicate graph; algorithm/seed; proposed 70/15/15; actual counts; class support; overlap checks; unknown identity limits; custody/access; approval | No exact-ratio requirement that breaks patient groups |
| T13 `experiment.md` | Plan and report a run / `07_Experiments/EXP####/README.md` | RQ/hypothesis; comparison; inputs/hashes; config; budget/stopping; preregistered metrics; RUN IDs; observations; failures; actual result; conclusion; next action | Planned outcome never prefilled as observed |
| T14 `config.yaml` | Machine-readable configuration / `07_Experiments/EXP####/config.yaml` | All Section 5.2 groups; resolved effective settings before launch | Validator rejects nulls/unknowns for executable fields |
| T15 `failure.md` | Preserve unsuccessful work / owning entity `failure_report.md` | Symptoms/time; affected IDs; known facts; suspected cause; logs; impact; recovery; lost work; prevention; verification; status | Hypothesis about cause clearly labeled |
| T16 `checkpoint.md` | Recover and verify / `08_Checkpoints/manifests/` | CKPT/EXP/RUN; role/epoch; state components; config/model hashes; artifact/hash/size; backup; restore test; limitations | Weights-only file is not automatically exact-resumable |
| T17 `model_card.md` | Bound model claims / `06_Models/cards/MODEL####.md` | Architecture/source/weights/licenses; EXP/CKPT/REL; classes/preprocessing; evaluation IDs; intended research use; exclusions; bias/limitations; export verification | No clinical approval inferred from mAP |
| T18 `evaluation.md` | Audit metrics / `09_Evaluation/EVAL####/report.md` | Freeze/model/data hashes; partition; coverage; matching; AP/IoU; thresholds/NMS; supports; P/R/mAP; timing/FPS; optional analyses; deviations; errors; conclusions | All reported numbers trace to raw records |
| T19 `error_review.md` | Systematic qualitative analysis / `09_Evaluation/EVAL####/error_review.md` | Selection method; ImageID/object; prediction/reference; error category; observed quality; label issue; reviewer; possible cause; limitation; example permission | No cherry-picked montage presented as representative |
| T20 `figure_table.md` | Reproducible asset / `10_Figures_Tables/specs/FIG####.md` or `TAB####.md` | Purpose; evidence IDs/hash; command/script; axes/units/aggregation; caption; output path; permission; visual review; writing references | Do not hand-edit values to improve appearance |
| T21 `gate_audit.md` | Explicit PASS/FAIL / `01_Project_Management/reviews/` | Gate/entity versions; each criterion; evidence/hash; PASS/FAIL; missing items; owner/fix; assessor/date; human approval; invalidated descendants | No prechecked template or conditional mandatory pass |
| T22 `reproduce.md` | Clean-run audit / `12_Documentation/` | Environment/access; artifact retrieval; checksums; exact commands; predicted agreement/tolerance; observed agreement; timing context; discrepancies; reproduction level | Distinguish inference replay from retraining |
| T23 `writing_unit.md` | Evidence-based chapter/section / `11_Writing/` | WR ID; audience/purpose; RQs; claims; P/EXP/EVAL/FIG/TAB links; draft; limitations; unresolved evidence; review/version | No fabricated filler for missing results |
| T24 `review_response.md` | Supervisor/reviewer response / `11_Writing/reviews/` | Original comment/date; issue; action; changed location; evidence; response; reviewer disposition; status | Blank feedback is not a request for invented improvements |
| T25 `submission.md` | Ready/submitted distinction / `11_Writing/` | Destination; actual instructions; files/hashes; authors; approvals; disclosures; readiness checks; submitted date; receipt; pending items | No claimed submission without receipt |
| T26 `archive.md` | Immutable handover / `15_Archive/` | Release ID; files/artifact versions/hashes; source tag; storage/access; licenses; exclusions; retention; restore proof; owner; receipts | Do not publicly package restricted images |
| T27 `prompt.md` | Repeatable assistance / `14_Templates_Prompts/` | Role; objective; context; inputs; allowed outputs/paths; prohibited changes; uncertainty rules; checks; human boundary; version | No sensitive content or hidden assumed state |
| T28 `risk_meeting.md` | Risk and milestone review / `01_Project_Management/meetings/` | Participants; progress/evidence; risks/triggers; options; actual feedback; decisions; actions/owners/dates; milestone forecast | Forecasts provisional; no fabricated meeting or signatures |

## 14.3 Copy-ready decision, gate, and configuration skeletons

```markdown
# DEC#### — [decision question]
Status: Unresolved / Human Decision Required
Owner / approver / due step:
UD reference:
Report facts and locators:
Planning options and evidence:
Recommendation and rejected alternatives:
Actual human decision / date / approval evidence:
Affected versions, steps, gates, and claims:
Reassessment trigger and rollback/recovery:
```

```markdown
# G## assessment — [entity/version]
Initial status: NOT ASSESSED
Assessor / date / human reviewer:
| Mandatory criterion | Evidence path and hash | PASS/FAIL | Corrective action |
|---|---|---|---|
Overall outcome: [PASS only if all required evidence is present; otherwise FAIL]
Invalidated downstream work:
Reassessment record:
```

```yaml
# Planning template only. Null values prohibit launch.
experiment_id: null
research_question_id: null
approval_record: null
source_commit: null
release_id: null
manifest_sha256: null
class_map_sha256: null
model:
  implementation: null
  version_or_commit: null
  architecture: null
  initial_weights_sha256: null
  license_record: null
training:
  seed: null
  image_size: null
  batch_size: null
  epochs_or_budget: null
  optimizer_and_schedule: null
  augmentations: null
  stopping_and_selection: null
runtime:
  environment_lock: null
  hardware_record: null
evaluation:
  protocol_sha256: null
  ap_iou: 0.50  # Report Figure 1 proposal; evaluator still must be specified.
  precision_recall_operating_point: null
  nms_and_max_detections: null
checkpoint_policy: null
artifact_destination: null
```

This skeleton is not a package-specific runnable YOLO configuration. STEP-024/025 must expand it to the chosen implementation's complete effective settings and validator schema. Do not mistake its brevity for permission to omit Section 5.2 fields.

<a id="appendix-a"></a>
# Appendix A. Canonical definitions

## A.1 Identifiers and naming

Use stable, zero-padded IDs. Never reuse an assigned ID; mark retired or superseded records instead. IDs shown here are format examples, not actual datasets/models/results. STEP-001 through STEP-046, G01 through G16, UD01 through UD20, RF01 through RF16, and T01 through T28 are planning identifiers defined now.

| Entity | ID pattern | Canonical record |
|---|---|---|
| Paper / screening record | P#### / SCR#### | Papers / Screening registries |
| Gap / claim | GAP#### / CLAIM#### | Research Gap / Claim registries |
| Decision / risk | DEC#### / RISK#### | Decision / Risk registries |
| Dataset candidate / source | CAND#### / DS#### | Dataset Candidates / Dataset registries |
| Annotation release / batch | ANN#### / ANNB#### | Annotation Registry; batch review files |
| Class | CLS#### (human-approved mapping) | Class Registry; numeric training index stored separately |
| Split / preprocessing / prepared release | SPLIT#### / PP#### / REL#### | Split manifests / Preprocessing / Release registries |
| Model candidate / trained model | MC#### / MODEL#### | Model Candidates / Model Registry |
| Experiment / execution attempt / checkpoint | EXP#### / RUN#### / CKPT#### | Experiment Registry, per-EXP run manifest, Checkpoint Registry |
| Evaluation / image | EVAL#### / IMG######## | Evaluation Registry / restricted image manifest |
| Figure / table / writing unit | FIG#### / TAB#### / WR#### | Asset / Writing registries |
| Archived release | ARCH#### | Archive manifest |

General filenames use `snake_case`; canonical document names and ID prefixes retain case. Raw source filenames are preserved in restricted storage. Never put direct patient identifiers in shared filenames. Timestamps use ISO 8601 with timezone where relevant. Checksums use SHA-256. Units and coordinate frames are explicit.

## A.2 Versioning and immutability

Documents/schemas use `vMAJOR.MINOR.PATCH`: breaking structure/meaning, compatible addition, nonsemantic correction. Dataset and annotation releases use explicit versions and immutable hashes. Methodologically meaningful data/label/config changes require new scientific entity versions/IDs even if a document edit looks small. A failed run's record remains addressable.

Registries may update status and pointers with Git history; historical configs, predictions, metrics, labels, and source artifacts are not edited in place. Corrections link old and new entities, reason, date, author, impact, and affected claims/gates. Do not conflate editing a registry description with permission to alter scientific evidence.

## A.3 Universal Definition of Done

A step is Done only when: objective and specified outputs are met; inputs and procedure are recorded; verification has evidence; applicable gates are current PASS; required human decisions are recorded; owning registries/docs are updated; permitted source/artifact copies are durable and recoverable; and the next researcher can follow the handoff. Preserve available evidence and its provenance; record authorized removals explicitly. The planning-source deletion is recorded in Appendix F and is not an unresolved hash-integrity failure. If remote sync is blocked, preserve an authorized local backup and mark sync pending; do not misstate completion of a remote-sync requirement.

This is a checklist for future execution, not an assertion that current research is reproducible. STEP-001 can save its scope/decision record before the full repository bootstrap; STEP-002 brings that record into source control. No circular dependency on a future folder gate is intended.

## A.4 Registry conventions

UTF-8 CSV with one header row and documented types; quote fields containing commas/newlines. Use explicit common fields `Owner,Version,Status,Created,Updated,EvidencePath`. Each registry has one canonical path and role owner. Linked IDs must resolve; multi-ID fields use a documented semicolon separator. Zero means measured zero; `not reported`, `unknown`, and `Unresolved / Human Decision Required` are not numeric zeros. Initial registries are header-only except actual decisions/facts with evidence. Never insert dummy experiments or citations.

<a id="appendix-b"></a>
# Appendix B. Registry catalog and schemas

The common fields in A.4 are appended once to every schema below. These are future canonical paths, used identically by the blueprint. Additional per-entity detail lives in the linked report, not a competing ledger.

| Registry / canonical path | Key / owner | Required domain columns beyond key and common fields |
|---|---|---|
| Decisions — `01_Project_Management/decisions.csv` | DEC / research lead | UD,Question,Decision,Approver,ApprovalDate,BlocksStep,OptionsEvidence,Supersedes,AffectedGates |
| Risks — `01_Project_Management/risk_register.csv` | RISK / research lead | Description,Trigger,Probability,Impact,Mitigation,Contingency,ReviewDate |
| Gates — `01_Project_Management/gates.csv` | AssessmentID / reviewer | GateID,EntityVersions,Outcome,CriteriaReport,Assessor,Approval,AssessmentDate,Supersedes,Invalidates |
| Papers — `02_Literature/papers.csv` | P / literature lead | ReportRef,Title,Authors,Year,Venue,DOI,SourceURL,SourceVersion,Access,FullTextPath,MetadataVerified,ReadingStatus,Task,Modality,Dataset,Model,Limitations,CitationKey |
| Screening — `02_Literature/screening.csv` | SCR / literature lead | PaperID,SearchRecord,Stage,Decision,Reason,Reviewer,ConflictResolution,DuplicateOf |
| Research Gaps — `02_Literature/gaps.csv` | GAP / literature lead | ReportGap,Statement,SupportingPapers,ContradictingPapers,SearchCoverage,Feasibility,ApprovedRQ,DecisionRecord |
| Claims — `02_Literature/claims.csv` | CLAIM / writing lead | Statement,Scope,PaperIDs,SourceLocators,ExperimentIDs,EvaluationIDs,AssetIDs,Contradictions,Uncertainty,Verification,WritingIDs |
| Dataset Candidates — `03_Datasets/candidates.csv` | CAND / data lead | Name,SourceURL,Modality,Access,LicenseEvidence,ClassesAsReported,GroupingAvailable,Relevance,QualityEvidence,DuplicateOf,SelectionDecision |
| Datasets — `03_Datasets/datasets.csv` | DS / data steward | CandidateID,SourceVersion,Provenance,PermissionRecord,EthicsRecord,LicenseRecord,ManifestHash,ImageCount,PatientCount,CountEvidence,CardPath,RestrictedLocation |
| Prepared Releases — `03_Datasets/releases.csv` | REL / data lead | DatasetID,DatasetVersion,AnnotationID,ClassMapHash,SplitID,PreprocessingID,ManifestHash,ImageCount,ObjectCount,RestrictedLocation,ParentRelease,ChangeReason |
| Classes — `04_Annotations/classes.csv` | CLS / annotation lead | Name,TrainingIndex,Definition,Inclusion,Exclusion,BoxRule,VisibilityRule,OverlapRule,Examples,ProtocolVersion,Approver |
| Annotation Registry — `04_Annotations/annotation_registry.csv` | ANN / annotation lead | DatasetID,ProtocolVersion,ClassMapHash,BatchIDs,Annotators,Reviewer,ToolVersion,NativeSchema,ExportSchema,NativeHash,ExportHash,QAReport,AdjudicationRecord,ParentVersion |
| Preprocessing — `05_Preprocessing/preprocessing_registry.csv` | PP / implementer | InputManifest,Operations,ConfigPath,ConfigHash,FitPartition,FitStateHash,GeometryContract,CodeRevision,ValidationReport,OutputManifest |
| Model Candidates — `06_Models/candidates.csv` | MC / model lead | Implementation,SourceURL,Version,Architecture,WeightOrigin,License,ResourceEvidence,Compatibility,Limitations,SelectionDecision |
| Models — `06_Models/model_registry.csv` | MODEL / model lead | CandidateID,ExperimentID,RunID,CheckpointID,ReleaseID,ClassMapHash,PreprocessingID,ExportFormat,ExportHash,ArtifactLocation,CardPath,EvaluationIDs,IntendedUse |
| Experiments — `07_Experiments/experiment_registry.csv` | EXP / experiment lead | RQ,Purpose,ParentComparison,ReleaseID,ModelCandidate,ConfigPath,ConfigHash,SourceCommit,Seed,RunIDs,Start,End,StoppingReason,ValidationEvaluationIDs,FailureReport,Conclusion |
| Checkpoints — `08_Checkpoints/checkpoint_registry.csv` | CKPT / experiment lead | ExperimentID,RunID,EpochStep,Role,StateComponents,ConfigHash,ModelHash,ArtifactPath,SHA256,Bytes,BackupPath,RestoreEvidence |
| Evaluations — `09_Evaluation/evaluation_registry.csv` | EVAL / evaluation lead | ExperimentID,ModelID,CheckpointID,ReleaseID,Partition,ProtocolHash,PredictionHash,MetricPath,TimingPath,CoverageReport,ReportPath,FreezeRecord,Deviations,ParentEvaluation |
| Assets — `10_Figures_Tables/assets.csv` | FIG or TAB / analyst | Kind,SourceIDs,DataHash,SpecPath,GeneratorCommand,CodeRevision,OutputPath,Caption,Units,Permission,VisualReview,WritingIDs |
| Writing — `11_Writing/writing_registry.csv` | WR / author | Document,Section,Topic,ClaimIDs,PaperIDs,EvaluationIDs,AssetIDs,DraftPath,Reviewer,ReviewState,Revision,MissingEvidence |
| Archive — `15_Archive/archive_manifest.csv` | ArchiveItemID / release owner | ArchiveID,ReleaseTag,ItemType,SourcePath,StoredLocation,Version,SHA256,Bytes,Sensitivity,License,Retention,RestoreEvidence,SubmissionReceipt |

Split manifests reside at `03_Datasets/splits/SPLIT####/manifest.csv` with `ImageID,GroupID,Partition,SourceHash,DuplicateGroup,AssignmentReason`, plus a versioned report and algorithm/configuration. GroupID is pseudonymous and potentially sensitive; classify storage accordingly. The REL row references the SPLIT ID and hash. Per-EXP run manifests include RUN, attempt/start/end, continuation checkpoint, environment, status and log pointers. These subordinate manifests are not duplicate master registries.

Traceability checks: every REL resolves its DS/ANN/SPLIT/PP; each EXP resolves REL and config/code; each MODEL resolves CKPT/EXP; each EVAL resolves MODEL/REL/protocol; each asset resolves data; each empirical claim resolves EVAL; each writing unit resolves its claims. An unresolved foreign key is a verification failure, not a harmless typo.

<a id="appendix-c"></a>
# Appendix C. Stage map and dependency chain

This map is canonical. The [blueprint](./OPG_PROJECT_EXECUTION_BLUEPRINT.md#stage-map) repeats it for navigation; step details live there.

| Stage | Steps | Governing sections | Exit gate(s) |
|---|---|---|---|
| S01 Foundation and unresolved-decision approval | 001 | 1, 11 | G01 |
| S02 Repository, documentation and registries | 002-003 | 2, 10, 14, A-B | G02 |
| S03 Literature search, screening and extraction | 004-007 | 3 | Feeds G03 |
| S04 Gap, objectives and RQ validation | 008-009 | 1, 3 | G03 |
| S05 Dataset discovery, permissions and intake | 010-012 | 4, 10 | Permission check before intake; feeds G04 |
| S06 Image inspection and quality | 013 | 4 | G04 |
| S07 Class and annotation-protocol approval | 014-015 | 6 | G05 |
| S08 Annotation pilot, production and QA | 016-018 | 6 | G06 |
| S09 Preprocessing and leakage-safe release | 019-021 | 4 | G07, G08 |
| S10 YOLO baseline, environment and pipeline | 022-026 | 5, 7, 10 | G09 |
| S11 Experiments, training and checkpoints | 027-030 | 5 | G10 per qualifying experiment |
| S12 Validation selection and final testing | 031-032 | 7 | G11 before testing |
| S13 Detection metrics and speed reporting | 033-035 | 7 | G12 |
| S14 Error analysis, prototype and reproducibility | 036-038 | 7-8 | G13, G14 |
| S15 Writing, submission and archive | 039-046 | 9, 10, 13 | G15, G16 |

```text
001/G01 → 002–003/G02 → 004–009/G03
→ 010–013/G04 → 014–015/G05 → 016–018/G06
→ 019–020/G07 → 021/G08 → 022–026/G09
→ [027 → 028 → 029/G10] → 030 (repeat approved experiment loop)
→ 031/G11 → 032 → [033 metrics + 034 timing] → 035/G12
→ 036/G13 → 037 prototype → 038/G14
→ 039–042/G15(thesis) → 043 thesis → 044 [G15(paper) before submission OR approved disposition]
→ 045 archive → 046/G16
```

The default path is sequential. Limited parallelism is permitted only where a blueprint step explicitly names independent work and no unmet gate is crossed. Earlier literature updates and documentation may continue during approved training. Final-test analysis cannot loop back into model selection without disclosing exposure and redesigning evaluation. Corrections return to the earliest affected parent step with new versions, then reassess downstream gates.

<a id="appendix-d"></a>
# Appendix D. Glossary

- **OPG:** a two-dimensional panoramic dental radiograph in this project.
- **Object detection:** prediction of target category and spatial bounding box; distinct from image-level classification and pixel-level segmentation.
- **Visible abnormality:** an approved radiographically observable target under the annotation protocol; not automatically a definitive diagnosis.
- **Ontology:** versioned class definitions, relationships, exclusions, and labeling rules.
- **Reference annotation:** reviewed labels used for training/evaluation; imperfect and subject to documented uncertainty.
- **Negative image:** fully reviewed image containing no approved targets under the protocol, not a declaration of dental health.
- **IoU:** overlap ratio used for a specified localization/matching or suppression purpose.
- **AP / mAP:** area under an implementation-defined precision-recall curve / mean of AP over the stated eligible classes and, where specified, IoUs.
- **Leakage:** information shared across intended independent partitions or obtained from test results that influences development.
- **Release:** an immutable, manifest-defined combination of data, labels, preprocessing and partition assignment.
- **Baseline:** the approved reference experiment against which controlled changes are interpreted.
- **Validation:** development partition used for selection/tuning under the protocol.
- **Final test:** locked partition used after selection/freeze to estimate held-out performance.
- **Checkpoint:** serialized model and, where supported, training state tied to a run and hash.
- **Gate:** evidence-based permission to proceed for specific versions; not an aspiration or score target.
- **Research prototype:** an experimental tool demonstrating the pipeline, without an implied clinical deployment authorization.

<a id="appendix-e"></a>
# Appendix E. Acronyms

| Acronym | Meaning |
|---|---|
| OPG | Orthopantomogram |
| YOLO | You Only Look Once |
| AP / mAP | Average Precision / mean Average Precision |
| IoU | Intersection over Union |
| FPS | Frames per second; images per second in the stated OPG workload |
| TP / FP / FN | True positive / false positive / false negative |
| NMS | Non-maximum suppression |
| QA / QC | Quality assurance / quality control |
| RQ / DoD | Research question / Definition of Done |
| CO / PO | Course outcome / program outcome |
| FYDP | Final year design project |
| CBCT | Cone-beam computed tomography; contextual modality, outside primary scope |
| GPU / CPU | Graphics processing unit / central processing unit |
| CSV / YAML | Comma-separated values / YAML configuration format |
| DOI | Digital object identifier |
| CI | Confidence interval |
| OOM | Out of memory |

<a id="appendix-f"></a>
# Appendix F. Source coverage and self-review

## F.1 Reading and historical source record

<a id="source-status"></a>
### Current source availability — 2026-11-16

After v1.0.0 was completed and its source hashes verified, the user explicitly requested deletion of the two original Markdown templates and the evaluation PDF. All three were deleted; only the two OPG plans remain in the workspace. The reading record, RF ledger, page locators and hashes below describe the original authoring event, not current file availability or a retained full copy. No backup is claimed. Historical source names/hashes are retained for provenance, without broken file links.

STEP-001 may proceed using the retained RF ledger and researcher/supervisor confirmation of scope. The obsolete templates are not execution prerequisites. If an ambiguity or decision needs the original PDF, obtain an authorized copy and verify it against the recorded hash, or obtain a documented supervisor clarification; block only the dependent decision until that evidence exists. The RF summary is not a substitute for the original report for independent source verification. Likewise, the summarized bibliography is not a substitute for reading the original studies.


All three supplied sources were read before drafting. The PDF was text-extracted in memory and all 15 pages were rendered and visually inspected, including the photographic cover, all table continuations, Figure 1 and blank feedback form. Temporary page renders were used only for inspection; no extracted-text file or additional report was added to the workspace.

| PDF pages | Material reviewed | Treatment in this handbook |
|---|---|---|
| 1 | Identity, reporting period, names, title, submission and certificate | Cover; RF01; no inference of new study approval |
| 2-3 | CO/PO table, Abstract, Introduction | Scope, objectives, metrics, supplementary-use limits |
| 4-7 | Background and Table 1, all 13 entries | Literature verification workflow; no independent verification claimed |
| 7-9 | Gap prose and Table 2 G1-G6 | Explicitly provisional gap hypotheses |
| 10 | Objectives and workflow introduction | O1-O3 and scientific lifecycle |
| 11 | Figure 1 and caption | Source categories; preparation operations; class examples; 70/15/15; validation-before-test; mAP@0.5/FPS |
| 12-14 | References [1]-[13] | Seed bibliography to verify under UD19; no invented citations added |
| 15 | Blank feedback/comment lines and blank examiner fields | No substantive supervisor/examiner feedback supplied; UD01 |

The Markdown references informed organization, canonical registries, templates, dependencies, session fields, gates, and recovery discipline. Project-specific scientific content and platform mandates were not inherited. Source SHA-256 values recorded before authoring:

```text
MASTER_RESEARCH_OPERATING_SYSTEM.md
EA84F1DAB9AFE1A081244065695137B241FC68CF5E284679A055A77B21505FF2
PROJECT_EXECUTION_BLUEPRINT.md
53CB45252AB8F2ECFF0E1BFE576C6639870D6F72AD7564FB2F8BD4BE375AF082
Title Evaluation Report (1).pdf
300EA7E2BA7A1A1388A1C4036E7C402D4A3243F3C0907E725D56D96B590DA556
```

## F.2 Planning-document self-review

Revision v1.1.0 corrects current source availability, establishes a tested minimal data-tool environment before early scripts, and separates G15 assessments for thesis and paper. These are document/workflow corrections, not evidence of passed execution gates.

Review scope: the two planning documents, their source fidelity, structure, internal references and executable instructions. This is **not** G01-G16 research execution evidence.

| Check | Planning disposition |
|---|---|
| Approved title and detection scope | Preserved verbatim; 2D OPG/YOLO/boxes and supplementary use maintained |
| Source versus recommendations versus unknowns | RF ledger, explicit recommendation policy, and UD01-UD20 register |
| Diagram-only details | Preserved; class examples not promoted to approved ontology |
| Feedback | Blank source fields acknowledged; no comments invented |
| Shared architecture | Sections, 15 stages, 46 steps, 16 gates, schemas and template IDs aligned |
| Leakage and test independence | Grouping, training-only fits, deterministic evaluation, final freeze, exposure recovery specified |
| Annotation uncertainty | Human protocol/pilot/adjudication and versioned correction specified |
| Failed/negative results | Preserved with immutable records and interpretation rules |
| Scientific conclusions | None invented; no dataset/model/configuration/results claimed as selected or completed |
| Completion versus plan quality | All research gates remain NOT ASSESSED; human ratification remains outstanding |

**Initial project state:** two complete planning deliverables; no research execution inferred. Begin with [STEP-001](./OPG_PROJECT_EXECUTION_BLUEPRINT.md#step-001). Do not mark a gate PASS simply because its checklist has been written.

*End of OPG Research Operating System — v1.1.0.*
