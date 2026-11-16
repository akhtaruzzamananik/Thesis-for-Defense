# OPG PROJECT EXECUTION BLUEPRINT

## Cover page

**Approved research title:** A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO.

| Field | Value |
|---|---|
| Document | OPG_PROJECT_EXECUTION_BLUEPRINT.md |
| Version / date | v1.1.0 / 2026-11-16 |
| Type | Sequential research execution manual |
| Governing handbook | [OPG Research Operating System](./OPG_RESEARCH_OPERATING_SYSTEM.md), v1.1.0 |
| Primary scientific authority | Title evaluation report (reviewed during original authoring; subsequently removed at the user’s request; see [source status](./OPG_RESEARCH_OPERATING_SYSTEM.md#source-status)) |
| Status | Complete planning document; execution NOT VERIFIED; all gates NOT ASSESSED |
| Coverage | 15 stages; 46 focused step types, with repeatable paper, annotation, experiment and writing sessions |
| Owners | Research team, supervisor and named reviewers; assignments recorded at STEP-001 |
| Intended system | YOLO-based 2D OPG object-localization research prototype and supplementary aid |

## Version history

| Version | Date | Change | Approval |
|---|---|---|---|
| v1.0.0 | 2026-11-16 | Initial source-grounded execution roadmap aligned to the OPG handbook | Proposed; human adoption pending |
| v1.1.0 | 2026-11-16 | Recorded user-directed source deletion; added early data-tool environment readiness; separated thesis and paper submission-readiness assessments | Editorial/workflow correction authorized; scientific execution gates remain NOT ASSESSED |

## How to use this blueprint

1. Read the [source facts and unresolved decisions](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01). REPORT FACT, PLANNING RECOMMENDATION, and **Unresolved / Human Decision Required** have the same meanings in both documents. The report's gap claims remain hypotheses to verify.
2. Start at the earliest unfinished step with evidenced prerequisites. All steps start NOT STARTED; unchecked boxes below are future verification tasks, not completed work. All research gates G01-G16 start NOT ASSESSED.
3. The handbook defines policy; this document sequences it. Its [repository contracts](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-02), [registry schemas](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-b), [templates](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-14), and [universal DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a) apply to every step.
4. For each work session, record the step ID plus a dated batch or RUN identifier. Repeated reading, annotation, training and writing steps are bounded sessions repeated until their coverage criteria are met. Time estimates below are **provisional planning estimates**, not promises or reported project dates. Human review/access delays and compute duration are additional unless stated.
5. Parallelizable means independent work after all its prerequisites exist. It does not authorize crossing a failed/unassessed gate or simultaneous conflicting registry edits. Assign IDs and merge canonical registry changes serially.
6. Use planning/review prompts before implementation prompts. Prompts are ready to adapt to the actual entity IDs and approved inputs, not permission to invent missing scientific settings. A human-only decision remains blocked until recorded; independent work may continue.
7. A gate PASS requires a dated evidence-based assessment for the exact versions. FAIL, NOT ASSESSED, and STALE all block dependent steps. The gate matrix is [Section 13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13). Low performance does not automatically invalidate an otherwise valid experiment.
8. Only the two planning files are created by the present task. Future artifact paths below are intended execution outputs. The supplied PDF and two Markdown references were subsequently deleted at the user’s request. Their historical provenance and current availability are recorded in [OS Appendix F](./OPG_RESEARCH_OPERATING_SYSTEM.md#source-status).

## Source-specific execution constraints

- The report's Figure 1 proposes **70% training / 15% validation / 15% testing**. Preserve that starting design, but document actual grouped proportions and obtain approval for necessary departures. Never split a patient/duplicate group to force exact percentages.
- Figure 1 explicitly lists **mAP@0.5** and **FPS**. Use matching IoU 0.50 for this required AP measure and specify the evaluator. Precision/Recall operating points, NMS IoU, AP implementation, timing boundary, hardware and repetition counts still require decisions.
- Teeth, impacted tooth, cavities, lesions and restorations are diagram examples, not an approved exhaustive class map. Classes, annotation geometry/format and qualified reviewer arrangements remain unresolved.
- No dataset name/count, YOLO release, training settings, score target, or experimental result is supplied as a finalized decision. Do not fill these from convenient library defaults without recording and reviewing them.
- The report's feedback form is blank. Ask whether separate feedback exists, but never invent comments, examiner signatures or dates.
- Final-test access follows validation selection and freeze. Published or internal test observations cannot be erased by renaming a split.

<a id="stage-map"></a>
## Stage-to-step map and contents

| Stage | Steps / navigation | Governing handbook | Exit gates |
|---|---|---|---|
| S01 Foundation and unresolved-decision approval | [001](#step-001) | §1, §11 | G01 |
| S02 Repository, documentation and registries | [002](#step-002)-[003](#step-003) | §2, §10, §14, A-B | G02 |
| S03 Literature search, screening and extraction | [004](#step-004)-[007](#step-007) | §3 | Feeds G03 |
| S04 Gap, objectives and RQ validation | [008](#step-008)-[009](#step-009) | §1, §3 | G03 |
| S05 Dataset discovery, permissions and intake | [010](#step-010)-[012](#step-012) | §4, §10 | Permissions before intake; feeds G04 |
| S06 Image inspection and quality | [013](#step-013) | §4 | G04 |
| S07 Class and annotation-protocol approval | [014](#step-014)-[015](#step-015) | §6 | G05 |
| S08 Annotation pilot, production and QA | [016](#step-016)-[018](#step-018) | §6 | G06 |
| S09 Preprocessing and leakage-safe release | [019](#step-019)-[021](#step-021) | §4 | G07, G08 |
| S10 YOLO baseline, environment and pipeline | [022](#step-022)-[026](#step-026) | §5, §7, §10 | G09 |
| S11 Experiments, training and checkpoints | [027](#step-027)-[030](#step-030) | §5 | G10 per qualifying experiment |
| S12 Validation selection and final testing | [031](#step-031)-[032](#step-032) | §7 | G11 |
| S13 Detection metrics and speed reporting | [033](#step-033)-[035](#step-035) | §7 | G12 |
| S14 Error analysis, prototype and reproducibility | [036](#step-036)-[038](#step-038) | §7-8 | G13, G14 |
| S15 Writing, submission and archive | [039](#step-039)-[046](#step-046) | §9, §10, §13 | G15, G16 |

## Master dependency chain

```text
001/G01 → 002–003/G02 → 004–009/G03 → 010–013/G04
→ 014–015/G05 → 016–018/G06 → 019–020/G07 → 021/G08
→ 022–026/G09 → [027 → 028 → 029/G10] → 030 approved repeats
→ 031/G11 → 032 → [033 metrics + 034 speed] → 035/G12
→ 036/G13 → 037 → 038/G14 → 039–042/G15(thesis)
→ 043 thesis → 044 [G15(paper) before submission OR approved disposition] → 045 archive → 046/G16
```

Repository bootstrapping and a tested minimal data-tool environment (STEP-002, verified at G02) precede operational scripts. Model-specific environment locking follows YOLO selection at STEP-023; the data-tool environment remains versioned separately. Deterministic annotation preparation may precede split assignment, but fitted preprocessing and augmentation never do. Test predictions are deliberately absent from the experiment loop. STEP-030 repeats STEP-027-029 under new IDs; it does not open the final test set.

## Universal session and artifact expectations

All steps inherit the [universal DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a). Record actual inputs/hashes, actions, outputs, verification, decisions, deviations and next action in the session note. Source-control expectations below apply to non-sensitive metadata only. Images, native labels, linkage keys, full predictions and checkpoints use their approved restricted/data/artifact tier; review before syncing. Document artifact hash and recoverable location. No named cloud provider or local-versus-cloud execution policy is assumed.

For all planning prompts: read the governing sections and current registries, distinguish source facts from proposals, list unresolved blockers, and never claim work performed without evidence. For implementation prompts: use the approved plan, preserve raw/source artifacts, fail explicitly on missing scientific settings, record exact code/configuration versions, and produce verification evidence. These standing constraints are part of every prompt below.

---

<a id="step-001"></a>
## STEP-001 — Confirm the mandate and assign unresolved decisions

**Objective:** Establish the approved scope and a decision process without prematurely selecting unknown scientific details.

**Why this step exists:** The report approves a topic and proposed workflow; it does not settle data, classes, implementation, or new operational policies.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §11](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** Both OPG plans and retained RF/source-history records available; researcher/supervisor confirmation of scope. Deleted templates are not required. Obtain an authorized report copy or documented clarification only where a source-dependent uncertainty needs it; no research completion assumed.

**Estimated difficulty and time (provisional):** Moderate; 2–3 hours plus supervisor response.

**Parallelizable:** No for scope approval; source indexing can be prepared independently.

**Inputs:** Retained RF01-RF16 and UD01-UD20, historical report locators and source-status record; researcher/supervisor confirmations and any authorized source copy or clarification subsequently obtained.

**Expected outputs:** Approved scope/O1-O3 interpretation, named decision owners, blocking deadlines, feedback-status record, G01 assessment.

**Repository/file changes:** Create `01_Project_Management/scope.md`, `decisions.csv`, `decision_log/DEC####.md`, and `reviews/G01_assessment_<date>.md`; these limited records may precede the full skeleton.

**Execution procedure:**

1. Review the retained title, names and report locators with the researcher; record source availability and seek original evidence or supervisor clarification for any disputed detail. Separate historical certificate evidence from approval of this new plan.
2. Review all UD rows; assign an owner and latest decision step, keeping later scientific choices unresolved.
3. Confirm whether separate supervisor/examiner feedback exists; record only actual comments.
4. Obtain scope/policy adoption and assess G01 against evidence, retaining unresolved later-stage decisions.

**Planning/review prompt:**

> Compare the OPG plans against the report. Prepare a scope-and-decision brief that preserves the diagram details and identifies only decisions needed now. Do not select unknown datasets or classes.

**Implementation prompt:**

> Documentation only: save the reviewed scope and actual decision records. Leave unapproved fields explicitly unresolved and do not premark any gate PASS.

**Human-only actions and decisions:** Supervisor/researchers approve scope interpretation and owners; confirm actual feedback availability (UD01).

**Version-control/artifact expectations:** Preserve the source-history/RF records and any authorized source copy subsequently obtained; do not recreate deleted originals from summaries. Save initial records durably; bring them into Git in STEP-002. No raw data acquisition.

**Documentation updates:** Cover approval state only if actually adopted; decision register, scope and dashboard baseline.

**Verification checklist:**

- [ ] Exact title and O1-O3 preserved.
- [ ] All UD items have owners and blocking milestones.
- [ ] No feedback invented; no research execution claimed.
- [ ] G01 has actual approval evidence.

**Common mistakes:** Calling all unknowns resolved; treating the signed cover as dataset or clinical approval.

**Recovery procedure:** Correct the record through a superseding DEC, retain earlier wording, and reassess G01 before dependent work.

**Definition of Done:** Scope and decision governance approved; G01 PASS with actual evidence. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-002](#step-002)

---

<a id="step-002"></a>
## STEP-002 — Create the repository skeleton and storage policy

**Objective:** Give every future artifact a canonical home and protect sensitive material before intake.

**Why this step exists:** Registries and outputs need stable paths; medical-data handling cannot be an afterthought.

**Governing section references:** [OS §2](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-001 complete; G01 PASS; UD11 storage/access decisions sufficient for repository setup.

**Estimated difficulty and time (provisional):** Moderate; 4–6 hours including minimal runtime verification.

**Parallelizable:** Folder README drafting may be divided; repository initialization and settings changes are serialized.

**Inputs:** OS folder contracts, current OPG plans, source-deletion history and approved access/storage decision.

**Expected outputs:** Canonical skeleton, README/CHANGELOG/CONTRIBUTING, ignore rules, chosen source-control workflow, storage-tier policy and tested minimal data-tool environment.

**Repository/file changes:** Create the Section 2 folders, root governance files, `.gitignore` and `.gitattributes`; add LICENSE only after its actual approval. Create `environment/data/` with the chosen dependency lock, runtime inventory and `verification.md`; record installation commands in `12_Documentation/installation.md`.

**Execution procedure:**

1. Inventory current files and hashes; record the authorized deletion of the historical references. Preserve any available evidence without claiming the deleted files remain present.
2. Create documented domain folders and minimal source/tests/environment homes, without choosing a model stack.
3. Define approved Git remote/access if available and restricted data/artifact storage separately.
4. Establish a minimal pinned runtime for registry/data tools, test basic imports/file access and image/coordinate operations on synthetic or permitted fixtures, and record actual versions. Add and test later data dependencies before first use; defer the YOLO stack.
5. Test ignore rules with safe dummy paths and inspect the staged inventory for sensitive or large content.

**Planning/review prompt:**

> Translate OS Section 2 into an exact creation checklist and storage policy. Identify which metadata may be sensitive and specify ignore checks before any acquisition.

**Implementation prompt:**

> Create the approved skeleton, governance files and minimal data-tool environment. Record a tested dependency lock and installation/smoke evidence before downstream scripts run; defer model-specific dependencies. Preserve existing evidence, test ignore behavior and report actual source-control state.

**Human-only actions and decisions:** Approve remote/access and storage arrangements; approve any project code license independently of dataset licenses.

**Version-control/artifact expectations:** First coherent source commit may include STEP-001 records. Do not initialize a public remote or publish records without the approved access policy.

**Documentation updates:** Root README, storage/access policy within `12_Documentation/pipeline.md`, folder contracts and CHANGELOG.

**Verification checklist:**

- [ ] Folder names match OS Section 2.
- [ ] Current-file inventory and historical source-deletion record agree; any recovered source copy has verified provenance.
- [ ] Restricted images, labels, secrets and checkpoints excluded from ordinary Git.
- [ ] Actual repository/access state documented.
- [ ] Minimal data-tool environment is pinned and smoke-tested; dependency additions must be tested before use.

**Common mistakes:** Copying template platform mandates; assuming ignore rules sanitize already tracked files.

**Recovery procedure:** Inspect staged/tracked files, correct placement and ignores, involve the owner for any disclosure, and verify the clean inventory.

**Definition of Done:** Repository and safe artifact homes exist with verified documentation; ready for registry bootstrap. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-003](#step-003)

---

<a id="step-003"></a>
## STEP-003 — Install templates, registries and repository checks

**Objective:** Create one canonical ledger per entity and pass repository readiness.

**Why this step exists:** Later evidence loses traceability if each session invents its own schemas or IDs.

**Governing section references:** [OS §2](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-14); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-002 complete; storage/access policy and tested minimal data-tool environment recorded.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours, split into schema and verification sessions if needed.

**Parallelizable:** Template files can be drafted independently; registry headers and ID assignment use one reviewer.

**Inputs:** T01-T28, Appendix B schemas, common registry columns, actual STEP-001 decisions.

**Expected outputs:** Blank templates, correct registry headers, populated actual decision records, dashboard and G02 assessment.

**Repository/file changes:** Create `14_Templates_Prompts/` templates/prompts and all Appendix B CSV paths; create `01_Project_Management/gates.csv`, `dashboard.md`, `timeline.md` and the G02 review.

**Execution procedure:**

1. Materialize field-complete blank templates; retain human approval boundaries.
2. Create headers from Appendix B with governance columns once, without dummy scientific rows.
3. Record G01-G16 as NOT ASSESSED except any evidenced G01 assessment; create actual decisions only.
4. Verify the minimal data-tool environment evidence, then validate unique headers/IDs, links, folder READMEs and restricted-tier rules; assess G02.

**Planning/review prompt:**

> Audit the proposed registry and template inventory against the handbook. Identify missing fields, duplicate sources of truth and any status that falsely implies completed science.

**Implementation prompt:**

> Save the approved templates and schemas. Add a lightweight registry/link validator under `13_Automation/` if useful, using only empty or permitted sample records; do not fabricate dataset or experiment rows.

**Human-only actions and decisions:** Research lead confirms G02 and schema ownership.

**Version-control/artifact expectations:** Commit non-sensitive schemas/templates and audit as `docs: initialize OPG registries and templates`; approved remote sync only.

**Documentation updates:** Template index, registry owner/path index, dashboard and repository readiness report.

**Verification checklist:**

- [ ] All canonical schemas match Appendix B.
- [ ] T01-T28 are usable and unfilled.
- [ ] No dummy scientific evidence or prechecked gates.
- [ ] G02 mandatory criteria evidenced.

**Common mistakes:** Two experiment ledgers; initial PASS flags; confusing an authorized, recorded source removal with undocumented evidence loss.

**Recovery procedure:** Reconcile duplicate paths into the canonical ledger with history; remove clearly marked dummy records before research intake, then rerun G02.

**Definition of Done:** G02 PASS and every downstream artifact has a documented schema/home. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-004](#step-004)

---

<a id="step-004"></a>
## STEP-004 — Approve the literature search and screening protocol

**Objective:** Define a reproducible search that can challenge the report's gap proposals.

**Why this step exists:** Searching only supportive work creates a biased novelty argument.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-003 complete; G01-G02 PASS; provisional RQs bounded by O1-O3.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours.

**Parallelizable:** Database-specific syntax can be drafted independently after shared eligibility criteria exist.

**Inputs:** Report references [1]-[13], G1-G6, candidate RQs and accessible literature services.

**Expected outputs:** Search protocol, database-specific strings, eligibility rules, extraction form and update schedule.

**Repository/file changes:** Create `02_Literature/searches/protocol.md` and search-log templates; document provisional RQs in `research_questions.md`.

**Execution procedure:**

1. Include direct YOLO/OPG detection queries and complementary annotation/image-quality searches.
2. Set modality/task relevance groups, date/language coverage, deduplication and full-text exclusion rules.
3. Specify quality appraisal based on methods, labels, splitting, metrics and reproducibility, not citation popularity.
4. Review feasibility and approve search/screening procedure before claiming coverage.

**Planning/review prompt:**

> Design a search capable of refuting G1-G6. Separate direct 2D OPG box-detection studies from contextual work and specify complete logs and screening reasons.

**Implementation prompt:**

> Documentation only: save approved strings and forms without inventing search counts or citations. Record inaccessible databases as limitations.

**Human-only actions and decisions:** Research lead/supervisor reviews eligibility and scope; resolve access constraints.

**Version-control/artifact expectations:** Commit protocol and versioned prompts as research planning records; no copyrighted bulk full text in public Git.

**Documentation updates:** Search protocol, screening instructions and unresolved access notes.

**Verification checklist:**

- [ ] Exact queries and coverage fields defined.
- [ ] Direct existing OPG detectors are actively sought.
- [ ] Exclusion and duplicate rules set before screening.
- [ ] No search reported as executed yet.

**Common mistakes:** Using the report's table as the complete review; arbitrary paper quotas.

**Recovery procedure:** Revise biased or infeasible queries with a logged reason; rerun affected searches under the revised protocol.

**Definition of Done:** Approved reproducible search/screening protocol ready for execution. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-005](#step-005)

---

<a id="step-005"></a>
## STEP-005 — Execute searches and register candidate papers

**Objective:** Build an auditable literature intake from actual retrieved records.

**Why this step exists:** Source provenance and duplicate control are prerequisites to defensible synthesis.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-004 approved; database access available.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per search batch, repeated to protocol coverage.

**Parallelizable:** Yes across independent sources; serialize P-ID allocation and deduplication.

**Inputs:** Approved queries, report bibliography leads, legal retrieval access.

**Expected outputs:** Search logs, deduplicated paper records, available full-text pointers and bibliography candidates.

**Repository/file changes:** Update `02_Literature/searches/`, `papers.csv`, `references.bib` and permitted `papers/P####.pdf` or restricted pointers.

**Execution procedure:**

1. Run each exact query and log date, filters, counts and export location.
2. Match DOI/title/version before assigning P IDs; link report reference numbers without adopting their metadata unchecked.
3. Retrieve lawful full texts where available and preserve bibliographic source evidence.
4. Record unavailable material, duplicate families and retrieval limits explicitly.

**Planning/review prompt:**

> Review each search export and report-reference lead. Produce a deduplicated intake with evidence-backed metadata and retrieval limitations; do not summarize unread papers.

**Implementation prompt:**

> Register actual retrieved records and preserve search logs. Keep unverified bibliographic fields marked unknown; save PDFs only where access terms permit.

**Human-only actions and decisions:** Use institutional access and approve any paid/access requests; do not bypass restrictions.

**Version-control/artifact expectations:** Commit logs/metadata and lawful pointers. Restrict PDFs where redistribution is not permitted.

**Documentation updates:** Papers Registry, canonical bibliography verification state and search coverage log.

**Verification checklist:**

- [ ] Every record links to a search or seed source.
- [ ] Duplicate versions are linked, not counted independently.
- [ ] No invented DOI/title/author data.
- [ ] Access and metadata verification states explicit.

**Common mistakes:** Treating a repository mirror as original provenance; marking inaccessible full text as read.

**Recovery procedure:** Correct metadata against sources, retain duplicate links, and repeat unlogged searches if reproducibility is missing.

**Definition of Done:** Planned search batch logged and registered with known coverage and access limitations. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-006](#step-006)

---

<a id="step-006"></a>
## STEP-006 — Screen records and document eligibility

**Objective:** Create a defensible set of included studies and contextual references.

**Why this step exists:** An exclusion trail prevents selective selection of convenient studies.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-005 batch registered; approved criteria from STEP-004.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per screening batch; total depends on retrieval volume.

**Parallelizable:** Yes for assigned records; reconcile disagreements before final inclusion.

**Inputs:** Registered titles/abstracts, accessible full text and screening criteria.

**Expected outputs:** Title/abstract and full-text decisions, reasons, conflict resolutions and reconciled flow counts.

**Repository/file changes:** Update `02_Literature/screening.csv`, paper reading states and `searches/screening_summary.md`.

**Execution procedure:**

1. Screen title/abstract using the approved rule set, preserving uncertain cases for full-text review.
2. Screen full text and label direct detection relevance versus contextual evidence.
3. Record explicit exclusion reasons and identify multiple reports of the same study.
4. Reconcile reviewer disagreements and count retrieved, duplicate, screened, excluded and included records.

**Planning/review prompt:**

> Audit screening decisions for consistency with the protocol. Identify any exclusion that suppresses contrary evidence or confuses CBCT, segmentation and 2D detection.

**Implementation prompt:**

> Save actual screening decisions and generate reconciled counts from the ledger. Do not infer eligibility from an unverified report summary.

**Human-only actions and decisions:** Resolve methodological disagreements and inaccessible key-source decisions.

**Version-control/artifact expectations:** Commit decision ledger and aggregate flow counts; retain restricted full-text storage.

**Documentation updates:** Screening summary, exclusions and search limitations.

**Verification checklist:**

- [ ] All screened records have stage and reason.
- [ ] Counts reconcile without duplicate studies.
- [ ] Contradictory eligible evidence retained.
- [ ] Reviewer disagreements explicitly resolved.

**Common mistakes:** Excluding strong competing methods because they weaken novelty; mixing task types in one comparator set.

**Recovery procedure:** Reopen affected records, document corrected criteria application and regenerate counts; update included set transparently.

**Definition of Done:** Current search batch screened with reproducible eligibility and exclusion evidence. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-007](#step-007)

---

<a id="step-007"></a>
## STEP-007 — Read, extract and verify included studies

**Objective:** Build detailed evidence records from original papers and their tables/figures.

**Why this step exists:** Metric names alone hide differences in data, labels, splits and evaluation settings.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-006 inclusion decisions; readable sources or explicit access limitations.

**Estimated difficulty and time (provisional):** Hard; 1–3 hours per paper provisionally; repeat for required evidence coverage.

**Parallelizable:** Yes by paper; cross-check critical numerical claims with a reviewer.

**Inputs:** Included full texts/supplements, T05, report seed-reference mapping.

**Expected outputs:** Structured summaries, verified metadata, extraction/comparison data and claim candidates with locators.

**Repository/file changes:** Create `02_Literature/summaries/P####.md`; update `papers.csv`, `references.bib`, `claims.csv` and source-linked extraction records.

**Execution procedure:**

1. Read methods, tables, figures and relevant supplements, not just abstracts.
2. Extract data unit/counts, class ontology, annotation expertise, split level, YOLO/version, preprocessing and training as reported.
3. Capture IoU/AP/threshold/timing conventions and limitations; mark missing fields not reported.
4. Verify each used result and citation; distinguish author statements from your critique and record contradictions.

**Planning/review prompt:**

> Extract this paper using T05. Give page/table locations for each scientific statement and assess whether its detection metrics and speed are comparable to this project.

**Implementation prompt:**

> Save grounded extraction and bibliography corrections only. Do not fill unreported configurations from knowledge of a model family; preserve verification notes.

**Human-only actions and decisions:** Review high-impact/ambiguous evidence and bibliographic discrepancies under UD19.

**Version-control/artifact expectations:** Commit permitted summaries and extraction metadata; keep original PDFs unaltered.

**Documentation updates:** Paper reading state, source locators, claims verification and comparison evidence.

**Verification checklist:**

- [ ] All used numerical statements have locators.
- [ ] Task/modality/split and AP settings explicit or not reported.
- [ ] Metadata verified for sources used to support claims.
- [ ] No unobserved result represented as fact.

**Common mistakes:** Copying report paraphrases as verified findings; comparing mAP with different IoUs or class sets.

**Recovery procedure:** Downgrade affected claims, return to original sources, correct extraction with history and flag downstream synthesis for review.

**Definition of Done:** Required included studies have source-grounded summaries and verified evidence for intended claims. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-008](#step-008)

---

<a id="step-008"></a>
## STEP-008 — Synthesize evidence and test proposed research gaps

**Objective:** Determine which report gap statements remain defensible within the documented search.

**Why this step exists:** The project's novelty must be investigated rather than assumed from a title proposal.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-007 evidence coverage sufficient to assess all report G1-G6 themes; unresolved sources labeled.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per synthesis cycle.

**Parallelizable:** Thematic drafts can be prepared separately; final interpretation is jointly reviewed.

**Inputs:** Summaries, screening coverage, comparison data, report Table 2 and claim ledger.

**Expected outputs:** Gap records with supporting/contradicting evidence, bounded synthesis and contribution options.

**Repository/file changes:** Update `02_Literature/gaps.csv`, `gap_notes/GAP####.md`, `synthesis.md` and `claims.csv`.

**Execution procedure:**

1. Map G1-G6 to actual studies, task/modality distinctions and measurable open questions.
2. Look explicitly for existing broad OPG/YOLO detection systems and incompatible novelty claims.
3. Classify each proposal as supported-within-search, narrowed, refuted or unresolved.
4. Draft feasible contribution options while preserving the approved detection title and negative evidence.

**Planning/review prompt:**

> Challenge each proposed gap using the extracted evidence. State search limitations, contradictory findings and a narrower contribution if the broad absence claim fails.

**Implementation prompt:**

> Documentation only: save the reviewed synthesis and gap/claim records with source IDs. Retain refuted hypotheses instead of erasing them.

**Human-only actions and decisions:** Supervisor judges defensible contribution framing and any needed scope clarification.

**Version-control/artifact expectations:** Commit synthesis and gap history; no scientific record deleted because it weakens the narrative.

**Documentation updates:** Research Gap Registry, claim wording, limitations and RQ candidates.

**Verification checklist:**

- [ ] Every gap has source coverage and counterevidence fields.
- [ ] No claim that no OPG detector exists without defensible support.
- [ ] No cross-modality numerical superiority argument.
- [ ] Feasible options map to O1-O3.

**Common mistakes:** Counting citations as proof of novelty; treating segmentation/detection differences as universal superiority.

**Recovery procedure:** Narrow or withdraw unsupported wording, extend targeted searches where needed and repeat synthesis before G03.

**Definition of Done:** Evidence-backed gap assessment ready for objective/RQ approval. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-009](#step-009)

---

<a id="step-009"></a>
## STEP-009 — Approve research questions and pass the literature gate

**Objective:** Lock a feasible RQ-to-objective-to-evaluation map and pass G03.

**Why this step exists:** Dataset and experiment choices must answer explicit approved questions.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-008 synthesis and STEP-004-007 search/screening/extraction evidence; G01-G02 current.

**Estimated difficulty and time (provisional):** Moderate; 2–3 hours plus supervisor review.

**Parallelizable:** No for scientific approval; literature updates can continue after the gate.

**Inputs:** O1-O3, candidate RQs, GAP/CLAIM records, feasibility options.

**Expected outputs:** Approved RQs/contribution limits, literature audit and G03 decision.

**Repository/file changes:** Finalize `02_Literature/research_questions.md`; update `decisions.csv`, `claims.csv`, `gates.csv`, and G03 assessment.

**Execution procedure:**

1. Map each question to data/class requirements, experiment factor, required metrics and intended claim.
2. Resolve UD19 for sources used in supporting arguments; exclude unverified sources from evidential support.
3. Approve a bounded contribution even if some proposal gaps were refuted.
4. Audit search transparency, source traceability and contradictory evidence; record actual G03 outcome.

**Planning/review prompt:**

> Review the complete literature evidence and propose the final RQ map. Make objective attainment measurable without inventing data counts, score targets or model settings.

**Implementation prompt:**

> Save only the actual approved questions and audit outcome. Update cross-references and mark unresolved downstream methodological choices with their UD IDs.

**Human-only actions and decisions:** Supervisor approves questions and contribution limits; researcher records the decision.

**Version-control/artifact expectations:** Commit the approved map, synthesis version and gate evidence as a research milestone.

**Documentation updates:** Scope cross-reference, question map, dashboard, literature cutoff date and G03 review.

**Verification checklist:**

- [ ] All RQs map to O1-O3 and evidence.
- [ ] No unverified novelty claim survives.
- [ ] Search/screening/source verification evidence complete for used claims.
- [ ] G03 assessment signed/dated as required.

**Common mistakes:** Demanding every report gap be confirmed; choosing questions based on expected favorable results.

**Recovery procedure:** Return to extraction/synthesis for unsupported claims; revise RQs within scope and reassess G03.

**Definition of Done:** G03 PASS; approved RQs guide dataset selection and experiment design. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-010](#step-010)

---

<a id="step-010"></a>
## STEP-010 — Discover and compare OPG dataset candidates

**Objective:** Find feasible 2D OPG sources suited to the approved questions.

**Why this step exists:** Hospitals, clinics and public datasets are possibilities in the report, not confirmed acquisitions.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-009 complete; G03 PASS.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours per discovery batch.

**Parallelizable:** Yes by source; consolidate duplicates and original provenance.

**Inputs:** Approved RQs, literature dataset references, report collection categories.

**Expected outputs:** Evidence-based candidate comparison with access, relevance, class/grouping and quality unknowns.

**Repository/file changes:** Populate `03_Datasets/candidates.csv` and `reports/candidate_comparison.md`.

**Execution procedure:**

1. Find original data owners and distinguish mirrors from independent collections.
2. Record modality, available labels/classes, source population and grouping information only when documented.
3. Compare access/license constraints, relevance and likely annotation burden; mark unknown counts explicitly.
4. Shortlist conditional candidates and identify permission questions before downloading restricted data.

**Planning/review prompt:**

> Compare actual OPG candidates against the RQs. Provide provenance and objective selection criteria; do not invent dataset sizes or treat publicly downloadable as legally reusable.

**Implementation prompt:**

> Save source-backed candidate records and a comparison memo. No medical-data download or upload until STEP-011 permissions are resolved.

**Human-only actions and decisions:** Researchers/supervisor select a conditional shortlist; custodian clarifies unknown source terms.

**Version-control/artifact expectations:** Commit safe metadata/pointers only; preserve candidate rejection reasons.

**Documentation updates:** Candidate ledger, feasibility comparison and UD02/UD03 status.

**Verification checklist:**

- [ ] Every candidate has an original source or explicit provenance gap.
- [ ] 2D OPG relevance distinguished from other modalities.
- [ ] License/access and grouping unknowns visible.
- [ ] No dataset represented as acquired or approved prematurely.

**Common mistakes:** Selecting by image count alone; counting mirrors as independent external validation.

**Recovery procedure:** Seek original provenance, exclude unsuitable candidates and expand discovery if access or relevance fails.

**Definition of Done:** A documented shortlist is ready for lawful access decisions. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-011](#step-011)

---

<a id="step-011"></a>
## STEP-011 — Resolve access, licensing, ethics and custody

**Objective:** Establish lawful acquisition, annotation, storage and reporting permissions.

**Why this step exists:** Medical-image access and derivative sharing cannot be inferred from research intent.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-11); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-010 shortlist; source-specific terms and institutional contact route available.

**Estimated difficulty and time (provisional):** Hard; 2–4 hours of preparation plus external approval turnaround, unknown.

**Parallelizable:** Permission requests for independent sources can proceed separately; no dependent intake before authorization.

**Inputs:** Candidate source terms, intended operations, storage plan and institutional requirements.

**Expected outputs:** Permission/ethics determination records, license copies or controlled pointers, retention/sharing rules and approved acquisition decision.

**Repository/file changes:** Create `03_Datasets/licenses/` records and `reports/access_decision.md`; update Decisions and candidate states.

**Execution procedure:**

1. Check use, annotation, derivative, model-weight, publication-example and redistribution rights separately.
2. Obtain institutional ethics/consent/waiver determination appropriate to the actual source.
3. Agree custody, pseudonymization/linkage, access roles, retention and allowed compute destinations.
4. Document the exact authorized source/version and acquisition route; leave denied/pending sources blocked.

**Planning/review prompt:**

> Prepare a source-specific permission checklist grounded in actual terms. Identify unmet rights and institutional determinations without offering legal or ethics approval yourself.

**Implementation prompt:**

> Documentation only: save actual permission evidence and restrictions securely, with safe metadata in Git. Do not manufacture approval language or signatures.

**Human-only actions and decisions:** Custodian/institution provides permission and ethics determination; researchers approve lawful source use (UD03).

**Version-control/artifact expectations:** Keep signed/private agreements restricted; Git stores permitted summaries and controlled references, never credentials.

**Documentation updates:** Access matrix, retention policy, candidate decision and unresolved restrictions.

**Verification checklist:**

- [ ] Acquisition and intended processing explicitly permitted.
- [ ] Ethics/consent determination recorded, not assumed.
- [ ] Compute/sharing destinations comply with terms.
- [ ] Pending/denied sources cannot proceed.

**Common mistakes:** Treating an open repository license as image consent; uploading to a convenient unapproved cloud.

**Recovery procedure:** Stop dependent use, request clarification or choose another source; preserve the denied decision and return to STEP-010 if needed.

**Definition of Done:** Written authorization is sufficient for the specific intake; unresolved restrictions remain explicit. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-012](#step-012)

---

<a id="step-012"></a>
## STEP-012 — Acquire, register and lock raw images

**Objective:** Create an immutable source inventory with verified provenance.

**Why this step exists:** Every label, split and model must trace to the exact acquired image version.

**Governing section references:** [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-011 permissions complete for selected source; approved restricted storage and G02 current.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per batch plus transfer duration.

**Parallelizable:** Yes per authorized source; DS IDs and manifests merged serially.

**Inputs:** Approved source/version, transfer method, storage permissions and checksum tools.

**Expected outputs:** DS record, source/individual file hashes, raw inventory, acquisition receipt and restricted location.

**Repository/file changes:** Populate restricted `03_Datasets/raw/DS####/`; update `datasets.csv`, `manifests/DS####_images.csv`, and acquisition reports.

**Execution procedure:**

1. Acquire exactly the authorized version and record origin/time plus archive hashes.
2. Extract into a new restricted raw location without modifying original bytes or filenames.
3. Assign pseudonymous ImageIDs and record source mapping, dimensions/hash/status; restrict identifying mappings.
4. Verify transferred counts/hashes, raw read-only practice and a recoverable backup.

**Planning/review prompt:**

> Specify a safe intake and hashing plan for the authorized source. List inventory reconciliation checks and private linkage handling.

**Implementation prompt:**

> Implement or run read-only inventory/checksum tooling. Preserve all raw files, including unreadable ones, and emit explicit errors rather than silently skipping.

**Human-only actions and decisions:** Custodian/researcher handles restricted access credentials and confirms authorized receipt.

**Version-control/artifact expectations:** No image bytes or identifying filenames in ordinary Git. Commit permitted manifests/pointers; back up data in its approved tier.

**Documentation updates:** Dataset Registry, acquisition record, source version and integrity report.

**Verification checklist:**

- [ ] Archive/file hashes and measured counts recorded.
- [ ] Raw bytes unchanged after inventory.
- [ ] Restricted linkage separate from shareable metadata.
- [ ] Backup retrieval and provenance recorded.

**Common mistakes:** Renaming raw images to make tooling convenient; assuming downloaded count equals usable count.

**Recovery procedure:** Quarantine incomplete intake, reacquire authorized originals, compare hashes and retain transfer-failure evidence.

**Definition of Done:** Immutable DS inventory acquired, registered and recoverable; no usability claim yet. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-013](#step-013)

---

<a id="step-013"></a>
## STEP-013 — Inspect image quality and approve the dataset

**Objective:** Establish actual OPG relevance, quality and feasible labeling conditions; pass G04.

**Why this step exists:** Readable files can still be unsuitable, identifying or impossible to label reliably.

**Governing section references:** [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-012 raw inventory; permissions current; dental/human review arranged for quality relevance.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per inspection batch plus review time.

**Parallelizable:** Automated integrity and visual review can proceed independently on assigned batches.

**Inputs:** Raw inventory, source metadata, candidate class concepts and approved access.

**Expected outputs:** Quality/integrity reports, duplicate candidates, exclusions/quarantine ledger, dataset card and G04 assessment.

**Repository/file changes:** Write `03_Datasets/reports/DS####_quality.md`, integrity data and `DS####_card.md`; update Dataset Registry and G04 review.

**Execution procedure:**

1. Check decoding, dimensions, channels/bit depth, orientation, corruption and burned-in identifiers.
2. Review available image variation, coverage, blur/contrast/artifacts and visibility with qualified input.
3. Identify exact/near duplicates and repeated studies; inspect any fixed viewing transform before annotation and preserve its mapping.
4. Reconcile retained/excluded/quarantined counts, approve suitability and record G04.

**Planning/review prompt:**

> Assess actual image quality and source relevance. Propose documented inclusion rules and flag targets that may not be visible; do not assign diagnosis or assume class counts.

**Implementation prompt:**

> Run read-only QC and duplicate screening; generate measured statistics and review samples within permissions. Preserve raw data and record every exclusion reason.

**Human-only actions and decisions:** Researchers/custodian approve source suitability; dental reviewer assesses visible-target feasibility.

**Version-control/artifact expectations:** Store private visual samples and duplicate maps in restricted storage; commit only approved aggregate reports and pointers.

**Documentation updates:** Data card, limitations, UD02/UD07/UD09 evidence and gate ledger.

**Verification checklist:**

- [ ] Counts reconcile and raw hashes remain unchanged.
- [ ] Privacy and OPG relevance checked.
- [ ] Quality exclusions use explicit rules.
- [ ] G04 permission/relevance/quality criteria evidenced.

**Common mistakes:** Filtering difficult images after model results; assuming unrecorded demographic attributes.

**Recovery procedure:** Correct QC errors, quarantine problematic inputs or seek another source; reassess G04 before annotation.

**Definition of Done:** G04 PASS for the selected DS version with explicit quality and metadata limitations. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-014](#step-014)

---

<a id="step-014"></a>
## STEP-014 — Define and review the dental object ontology

**Objective:** Turn report examples into a defensible proposed class specification.

**Why this step exists:** An example list is insufficient to define reproducible annotation or evaluation.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-013 complete; G04 PASS; qualified dental reviewer available.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus expert review.

**Parallelizable:** Individual class drafts can be prepared separately; overlap/granularity decisions require joint review.

**Inputs:** Report Figure 1 examples, literature, actual dataset quality and RQs.

**Expected outputs:** Proposed class table, inclusion/exclusion/visibility rules, ambiguity cases and approval questions.

**Repository/file changes:** Draft `04_Annotations/classes.csv` and `protocols/class_definitions.md`; link approved or pending DEC records.

**Execution procedure:**

1. Evaluate whether each proposed concept is visible and localizable on the selected OPG images.
2. Define object granularity, box target, negative examples and overlap/nested-label policies.
3. Separate radiographic observations from diagnoses requiring unavailable information.
4. Assign stable class identities and a proposed training-index map only for reviewer-approved candidates.

**Planning/review prompt:**

> Draft an ontology from source examples and actual visibility evidence. Explain inclusion/exclusion and ambiguous cases; label every unapproved class decision unresolved.

**Implementation prompt:**

> Documentation only: save definitions and permitted examples with source references. Do not create production labels or silently merge clinically different concepts.

**Human-only actions and decisions:** Dental reviewer/supervisor decides final targets, granularity and clinical terminology (UD04).

**Version-control/artifact expectations:** Commit allowed definitions; restrict patient examples. Class-map changes are versioned, never silently reordered.

**Documentation updates:** Class definitions, reviewer questions, RQ coverage and decision evidence.

**Verification checklist:**

- [ ] Each proposed class has operational boundaries.
- [ ] Examples not mistaken for a mandatory exhaustive class list.
- [ ] Ambiguous/overlapping cases explicitly covered.
- [ ] Qualified review and approval status recorded.

**Common mistakes:** Using broad lesion labels without rules; accepting AI-generated class suggestions as clinical truth.

**Recovery procedure:** Narrow or remove poorly labelable targets with supervisor approval, document the effect on objectives and revise definitions.

**Definition of Done:** A complete, evidence-based class proposal is ready for protocol approval. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-015](#step-015)

---

<a id="step-015"></a>
## STEP-015 — Approve annotation format, protocol and QA thresholds

**Objective:** Freeze a usable annotation protocol and pass G05.

**Why this step exists:** Consistent labels require agreed geometry, review rules and acceptance criteria before annotating.

**Governing section references:** [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-14); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-014 reviewed ontology; actual tool/export feasibility and qualified adjudicator identified.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus human approval.

**Parallelizable:** Tool/schema testing can accompany protocol drafting; approval is serialized.

**Inputs:** Class definitions, dataset viewing/reference images, tool candidates, T09 and UD05/UD06.

**Expected outputs:** Approved ontology/protocol, exact coordinate/export contract, pilot/production QA plan and G05 assessment.

**Repository/file changes:** Finalize `04_Annotations/protocols/annotation_protocol_v1.0.0.md`, `classes.csv`; save G05 review and decision records.

**Execution procedure:**

1. Specify native and training-export schemas, units/origin/geometry, class ordering and conversion rules.
2. Define uncertain, partially visible, empty, missing and ignored annotation states.
3. Set pilot coverage, double-review/adjudication, agreement measures and acceptance thresholds prospectively.
4. Test a permitted example's export round trip, then obtain approval and assess G05.

**Planning/review prompt:**

> Review the protocol for reproducibility, completeness and OPG labelability. Identify every rule needed to distinguish a reviewed negative from an unannotated image.

**Implementation prompt:**

> Save the approved protocol; implement a tiny export-schema check if needed using permitted examples. Do not choose a format merely because it is common for YOLO.

**Human-only actions and decisions:** Dental reviewer and supervisor approve class map, schema, annotator roles and QA criteria (UD04-UD06).

**Version-control/artifact expectations:** Version protocol and class-map hash; retain native examples securely and avoid publishing clinical images.

**Documentation updates:** Protocol, tool/version record, QA plan, class map and G05 review.

**Verification checklist:**

- [ ] Class map and all ambiguity rules approved.
- [ ] Coordinates/native/export formats fully specified.
- [ ] QA sampling and thresholds set before results.
- [ ] G05 PASS supported by named reviewers.

**Common mistakes:** Treating missing labels as background; picking an agreement threshold after seeing poor results.

**Recovery procedure:** Revise ambiguous rules, rerun example conversion and obtain renewed approval before pilot use.

**Definition of Done:** G05 PASS for a specific protocol and class map. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-016](#step-016)

---

<a id="step-016"></a>
## STEP-016 — Run and adjudicate the annotation pilot

**Objective:** Test whether annotators can apply the approved protocol consistently.

**Why this step exists:** A written protocol may fail on real overlap, visibility and quality variation.

**Governing section references:** [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-015 complete; G05 PASS; authorized pilot sample and reviewers assigned.

**Estimated difficulty and time (provisional):** Hard; 2–4 hours per pilot session plus independent annotation/review; total data-dependent.

**Parallelizable:** Independent annotators work separately before reconciliation; do not share initial labels.

**Inputs:** Prospective sample/QA criteria, protocol, actual images and chosen tool.

**Expected outputs:** Independent pilot labels, disagreement report, adjudication and accepted pilot or corrective plan.

**Repository/file changes:** Store restricted pilot native/exports and `04_Annotations/reviews/pilot_review.md`; update protocol/decision records if needed.

**Execution procedure:**

1. Select the approved coverage sample and preserve its selection evidence.
2. Annotate independently and compare target presence, class agreement and matched-box localization.
3. Have the qualified reviewer adjudicate misses, extra boxes, disagreement and uncertain cases.
4. Apply prospective criteria; revise and repeat the pilot if needed, reapproving changed protocol under G05.

**Planning/review prompt:**

> Evaluate the pilot against the predeclared criteria. Separate structural validity, object completeness, class correctness and box agreement; do not equate high IoU with clinical validity.

**Implementation prompt:**

> Compute approved agreement summaries and schema checks from actual pilot labels. Preserve independent originals and adjudicated versions separately.

**Human-only actions and decisions:** Qualified reviewer adjudicates and approves pilot readiness; supervisor resolves scope-changing labelability problems.

**Version-control/artifact expectations:** Retain original annotations and adjudications in restricted versioned storage; commit safe summary and protocol history.

**Documentation updates:** Pilot review, agreement/error summaries, examples and annotator training notes.

**Verification checklist:**

- [ ] Pilot sample follows approved coverage.
- [ ] Independent originals retained.
- [ ] All material disagreements adjudicated.
- [ ] Pilot accepted by criteria or explicitly failed; changed protocol reapproved.

**Common mistakes:** Calibrating annotators by copying one person's boxes before measuring agreement; hiding difficult cases.

**Recovery procedure:** Clarify rules, retrain annotators, reannotate affected pilot records and repeat assessment without lowering thresholds post hoc.

**Definition of Done:** Pilot accepted under the current G05-approved protocol; production permitted. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-017](#step-017)

---

<a id="step-017"></a>
## STEP-017 — Annotate production batches with review tracking

**Objective:** Produce complete, auditable labels in manageable batches.

**Why this step exists:** Untracked annotation work causes omissions, class drift and unrecoverable corrections.

**Governing section references:** [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-016 accepted pilot; G04-G05 current; batch assignments and access authorized.

**Estimated difficulty and time (provisional):** Hard; 2–4 hours per annotation/review session; total estimated from observed pilot throughput.

**Parallelizable:** Yes across disjoint assigned batches; independent QA allocation and ID merges remain controlled.

**Inputs:** Approved protocol/class map, accepted annotators, image membership and QA schedule.

**Expected outputs:** Native and exported labels per ANNB batch, reviewed-empty states, uncertainty queue and review records.

**Repository/file changes:** Populate restricted `04_Annotations/native/`, `exports/`, `reviews/ANNB####.md` and `adjudications/`; prepare ANN registry release metadata.

**Execution procedure:**

1. Assign nonoverlapping image batches and record annotator/tool/protocol versions.
2. Annotate all eligible targets and explicitly mark reviewed negatives; quarantine unassessed images.
3. Queue ambiguous objects for adjudication and record any approved model assistance.
4. Apply batch QA and preserve original/corrected labels and review coverage before closing each batch.

**Planning/review prompt:**

> Prepare this batch assignment and quality-review checklist using the current protocol. Identify workload and review bottlenecks from measured pilot throughput, without inventing completion dates.

**Implementation prompt:**

> Use approved annotation tools and validation helpers only. Track every assigned image and export status; never autoaccept model proposals as ground truth.

**Human-only actions and decisions:** Annotators provide qualified labels; dental reviewer adjudicates uncertainty and approves reviewed batches.

**Version-control/artifact expectations:** Back up native editable labels and exports in approved storage; commit only safe batch metadata and aggregate progress.

**Documentation updates:** Batch records, uncertainty/adjudication log, throughput estimate and annotation progress.

**Verification checklist:**

- [ ] Every assigned image has a completion/review state.
- [ ] Class/tool/protocol versions recorded.
- [ ] Reviewed negatives distinguish missing labels.
- [ ] Corrections and model assistance, if any, traceable.

**Common mistakes:** Saving only training exports; counting boxes as proof annotation is complete.

**Recovery procedure:** Reopen incomplete batches, restore native backups, resolve uncertainty, and rerun review before release.

**Definition of Done:** All required production batches completed and reviewed, ready for whole-release QA. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-018](#step-018)

---

<a id="step-018"></a>
## STEP-018 — Audit annotations and freeze the annotation release

**Objective:** Establish a verified ANN release and pass G06.

**Why this step exists:** Training and test metrics are invalid if reference labels are incomplete or misaligned.

**Governing section references:** [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-017 complete; pilot/batch review and adjudication records available; G05 current.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus stratified visual review.

**Parallelizable:** Structural and visual QA can run independently; release approval waits for both.

**Inputs:** All native/export labels, image inventory, class map, approved QA thresholds.

**Expected outputs:** Whole-release integrity/QA report, accepted ANN version and hashes, G06 assessment.

**Repository/file changes:** Update `04_Annotations/annotation_registry.csv`, `reviews/annotation_release_audit.md`, restricted manifests and G06 review.

**Execution procedure:**

1. Validate all image-label pairs, class indices, finite in-bounds boxes, area and duplicate/orphan records.
2. Reconcile reviewed empty, excluded and missing labels and object/image totals.
3. Conduct the approved class/quality-stratified visual review and confirm adjudication closure.
4. Freeze native/export/class-map hashes and assess G06 with qualified reviewer evidence.

**Planning/review prompt:**

> Audit annotation completeness and correctness against the prospective protocol. Report actual errors and residual uncertainty; do not certify unseen labels as perfect.

**Implementation prompt:**

> Run schema and correspondence checks, generate reconciled counts and immutable manifests. Do not silently repair coordinates or relabel objects; queue corrections for review.

**Human-only actions and decisions:** Dental reviewer accepts annotation quality and adjudications; data lead confirms inventory integrity.

**Version-control/artifact expectations:** Archive immutable ANN versions in restricted storage; safe metadata/hashes in source control.

**Documentation updates:** Annotation Registry, QA report, class-map version, corrected-batch lineage and gate ledger.

**Verification checklist:**

- [ ] No unresolved invalid/orphan training or evaluation labels.
- [ ] QA criteria met with actual sample evidence.
- [ ] Adjudications and exclusions documented.
- [ ] G06 PASS tied to exact hashes.

**Common mistakes:** Declaring QA complete from syntax checks alone; ignoring systematically missed objects.

**Recovery procedure:** Quarantine affected batches, reannotate/adjudicate, issue a new ANN release and reassess G06; preserve failed versions.

**Definition of Done:** G06 PASS for a frozen, auditable annotation release. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-019](#step-019)

---

<a id="step-019"></a>
## STEP-019 — Design preprocessing and coordinate-preserving transforms

**Objective:** Specify the minimal justified preparation and its annotation geometry contract.

**Why this step exists:** Enhancement and resizing can erase visible targets or move boxes if applied without verification.

**Governing section references:** [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-018 complete; G06 PASS; raw/annotation reference-image mapping known.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours.

**Parallelizable:** Independent transform specifications can be drafted together; combined order requires review.

**Inputs:** Quality report, approved labels, report preprocessing proposals and implementation constraints known so far.

**Expected outputs:** PP design, parameter decisions, geometry tests, training-only fit/augmentation rules and baseline transform plan.

**Repository/file changes:** Create `05_Preprocessing/specs/pipeline.md`, proposed `configs/` and PP registry drafts; code specification for `src/opg/`.

**Execution procedure:**

1. Separate fixed pre-annotation/viewing operations from model-input preparation and training-only augmentation.
2. Define resize/padding/channel/normalization behavior and forward/inverse box mapping.
3. Justify any contrast/noise/filtering operation and specify how target visibility will be checked.
4. Specify training-only fit rules and prohibited augmentation effects; leave model-specific values unresolved until candidate selection if necessary.

**Planning/review prompt:**

> Design an OPG preprocessing pipeline grounded in observed quality issues. Explain each operation, geometry mapping and leakage control; do not presume enhancement improves detection.

**Implementation prompt:**

> Implement approved transform and geometry tests using permitted fixtures. Do not fit statistics or materialize split-dependent outputs before STEP-020; unresolved model-specific settings must fail validation.

**Human-only actions and decisions:** Dental reviewer approves visibility-preserving choices; researchers approve UD09 and later model-specific amendments.

**Version-control/artifact expectations:** Commit specs/configuration and safe tests; keep image previews restricted and raw unchanged.

**Documentation updates:** Preprocessing spec, parameter rationale, class/coordinate dependencies and decision register.

**Verification checklist:**

- [ ] Every transform has rationale and effective parameters or explicit blocker.
- [ ] Source-to-output box mapping defined.
- [ ] Training-only fits and augmentation distinguished from deterministic evaluation.
- [ ] No silent crop/drop of target boxes.

**Common mistakes:** Resizing images without boxes; treating all five diagram operations as arbitrary mandatory defaults.

**Recovery procedure:** Disable damaging transforms, correct mappings and recheck approved examples; version changed PP specifications.

**Definition of Done:** A reviewed, testable preprocessing design exists; split-dependent fitting remains blocked until G07. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-020](#step-020)

---

<a id="step-020"></a>
## STEP-020 — Construct and approve the leakage-safe split

**Objective:** Lock partition membership with grouped independence evidence and pass G07.

**Why this step exists:** Image-level random assignment can place repeated patients or derivatives on both sides of evaluation.

**Governing section references:** [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-019 design; G04-G06 PASS; grouping/duplicate findings and class-support data available.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus custodian/supervisor review.

**Parallelizable:** No competing split choices based on performance; metadata audit can be divided before one controlled assignment.

**Inputs:** DS/ANN inventories, patient/study/duplicate relationships, proposed 70/15/15 and UD07/UD08 decisions.

**Expected outputs:** SPLIT manifest, algorithm/config/seed, target versus actual counts, overlap report, test custody rules and G07 assessment.

**Repository/file changes:** Create `03_Datasets/splits/SPLIT####/manifest.csv`, `report.md`, configuration and checksums; update gate/decision records.

**Execution procedure:**

1. Resolve linked patient/study/duplicate components before partition allocation; all derivatives inherit source membership.
2. Generate the approved grouped allocation starting from 70/15/15, preserving groups despite rounding.
3. Audit overlap, class support and metadata limitations; record actual image/object/group counts.
4. Obtain approval of departures or limited-independence claims and seal final-test access; assess G07.

**Planning/review prompt:**

> Design and audit the grouping-based split. Explain any inability to establish patient independence and any departure from proposed proportions; never claim leakage safety from hashes alone.

**Implementation prompt:**

> Implement deterministic assignment and overlap assertions from approved grouping metadata. Save complete manifests and fail on unresolved material cross-partition relations.

**Human-only actions and decisions:** Custodian clarifies identity/grouping; supervisor approves algorithm, proportions, limitations and test custody.

**Version-control/artifact expectations:** Version source/config and permitted split metadata; restrict identifying group maps. Never overwrite an existing SPLIT.

**Documentation updates:** Split report, grouping evidence, UD07/UD08 resolutions, test-access policy and G07 review.

**Verification checklist:**

- [ ] No known linked patient/study/duplicate component crosses partitions.
- [ ] Same inputs/config reproduce membership.
- [ ] Actual proportions and class support reported.
- [ ] G07 approval accurately states residual independence limits.

**Common mistakes:** Breaking patient groups to reach exact ratios; assuming absent patient IDs prove independence.

**Recovery procedure:** Invalidate faulty SPLIT and descendants, repair grouping, create a new SPLIT and reassess; disclose any prior test exposure.

**Definition of Done:** G07 PASS for the exact split and documented independence claim. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-021](#step-021)

---

<a id="step-021"></a>
## STEP-021 — Materialize and verify a versioned prepared dataset

**Objective:** Create a traceable training-ready REL and pass G08.

**Why this step exists:** A valid split is insufficient if exported labels, transforms or class maps drift during preparation.

**Governing section references:** [OS §4](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-020 complete; G07 PASS; approved PP parameters sufficient for a canonical release; G06 current.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus processing duration.

**Parallelizable:** Deterministic processing per partition may run separately; fitted state derives exclusively from training.

**Inputs:** DS/ANN/SPLIT hashes, approved PP configuration, image/label conversion contract.

**Expected outputs:** Prepared image/label manifests, PP/fitted-state record, geometry/visibility audit, REL record and G08 assessment.

**Repository/file changes:** Create restricted `05_Preprocessing/processed/REL####/`, PP reports; populate `preprocessing_registry.csv` and `03_Datasets/releases.csv`.

**Execution procedure:**

1. Fit approved data-dependent parameters on training only and serialize their state.
2. Apply deterministic evaluation transforms and matching label conversion without augmentation of validation/test.
3. Verify round-trip box geometry, bounds, class order, image correspondence, counts and raw hashes.
4. Bind DS/ANN/SPLIT/PP/class map into REL with checksums; assess G08 before baseline use.

**Planning/review prompt:**

> Audit the complete prepared-release lineage and identify any transform fitted outside training. Specify geometry and visibility acceptance evidence before declaring readiness.

**Implementation prompt:**

> Run the approved pipeline into a new immutable release, export labels in the approved schema and generate checksums/count reconciliation. Fail on unresolved settings or mismatched class maps.

**Human-only actions and decisions:** Researchers and dental reviewer approve visibility/geometry findings; any model-driven transform change later requires a new PP/REL and reassessment.

**Version-control/artifact expectations:** Source/config/reports in Git where permitted; image/label bytes and fitted private state in approved storage with verified backup.

**Documentation updates:** PP report, release card/manifest, dataset lineage and G08 review.

**Verification checklist:**

- [ ] No validation/test information used for fitted preprocessing.
- [ ] All boxes/classes align after conversion.
- [ ] Release counts and hashes reconcile.
- [ ] G08 PASS binds exact parent versions.

**Common mistakes:** Augmenting before splitting; regenerating over an existing release; hidden normalization defaults.

**Recovery procedure:** Quarantine derivative, repair pipeline, issue new PP/REL and repeat G08; invalidate affected experiments.

**Definition of Done:** G08 PASS and an immutable prepared release is available for baseline integration. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-022](#step-022)

---

<a id="step-022"></a>
## STEP-022 — Select the YOLO implementation and baseline candidate

**Objective:** Choose a documented, feasible YOLO detector without inventing a mandated version.

**Why this step exists:** The approved title specifies a method family, not a package or model scale.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-021 release/G08 PASS; approved RQs and literature; actual compute/storage constraints.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours plus supervisor choice.

**Parallelizable:** Candidate evidence gathering may run independently; final selection is one documented decision.

**Inputs:** Verified model sources, release schema, licenses, hardware feasibility and UD10.

**Expected outputs:** Model candidate comparison, baseline choice, weight provenance and license/compatibility decision.

**Repository/file changes:** Populate `06_Models/candidates.csv`; create `baseline_plan.md` and a DEC record.

**Execution procedure:**

1. Inspect official candidate documentation/source and record exact implementation/release/commit.
2. Check detection output, class remapping, evaluator, checkpoint/export support, licenses and pretrained-weight origin.
3. Compare resource needs using actual evidence or explicitly provisional estimates.
4. Choose the baseline and record rejected alternatives; return to STEP-019-021 if its required input changes the prepared release.

**Planning/review prompt:**

> Compare feasible YOLO implementations against the project requirements. Recommend a baseline with provenance and limitations, without asserting that a newer version is inherently better.

**Implementation prompt:**

> Documentation only until selection is approved; save candidate records and the actual decision. Do not download or execute unreviewed weights as an implicit choice.

**Human-only actions and decisions:** Researchers/supervisor approve implementation, architecture/scale and weight policy under UD10.

**Version-control/artifact expectations:** Commit comparison/decision; weight binaries remain in approved artifact storage with license and hash.

**Documentation updates:** Baseline plan, Model Candidates, license record and unresolved compatibility issues.

**Verification checklist:**

- [ ] Exact chosen implementation identified.
- [ ] Pretrained source and license verified or pretraining explicitly not used.
- [ ] Compute feasibility and checkpoint/evaluation compatibility addressed.
- [ ] Any data-interface change routes back through G08.

**Common mistakes:** Writing only YOLO with no version; assuming software license covers all pretrained weights.

**Recovery procedure:** Resolve provenance/compatibility gaps or select another candidate; revise the decision and affected data release transparently.

**Definition of Done:** An approved baseline candidate with explicit provenance and integration requirements exists. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-023](#step-023)

---

<a id="step-023"></a>
## STEP-023 — Pin and verify the execution environment

**Objective:** Create a tested runtime for the chosen detector and evaluator.

**Why this step exists:** Unrecorded dependencies and accelerator differences undermine recovery and speed comparisons.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §8](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-022 selection; authorized compute destination and sufficient access/resources.

**Estimated difficulty and time (provisional):** Moderate to hard; 3–6 hours, depending on compatibility.

**Parallelizable:** Documentation and storage checks may proceed during installation; environment verification is sequential.

**Inputs:** Chosen implementation requirements, actual hardware, storage permissions, dependency sources and the preserved `environment/data/` lock used for existing PP/REL artifacts.

**Expected outputs:** Dependency lock, runtime/hardware inventory, installation commands and import/device smoke evidence.

**Repository/file changes:** Populate `environment/model/` with the chosen lock format and `versions.md`; update `12_Documentation/installation.md`. Preserve `environment/data/` and its verification record.

**Execution procedure:**

1. Inspect the actual runtime and existing data-tool lock; choose a compatible model-specific pinned dependency set without silently replacing the earlier environment.
2. Install only approved packages and record sources/versions plus driver/accelerator details.
3. Verify detector/evaluator imports, device behavior and write/access permissions without test-data use.
4. Recreate or validate the environment from recorded commands and retain failures/fixes. If a shared dependency upgrade affects preprocessing, compare outputs and reassess G08/new PP/REL versions as needed before training.

**Planning/review prompt:**

> Define the environment from the actual chosen YOLO implementation and hardware. Identify compatibility and licensing constraints; do not invent installed versions or GPU availability.

**Implementation prompt:**

> Build the approved environment and save exact dependency/runtime inventory. Run minimal import/device/storage checks; report actual output and unresolved limitations.

**Human-only actions and decisions:** Researchers approve platform/cost/resource use and access controls (UD11).

**Version-control/artifact expectations:** Commit lock/instructions; exclude virtual environments, caches and credentials. Record artifact-store connectivity without leaking tokens.

**Documentation updates:** Installation guide, runtime inventory, compatibility notes and recovery instructions.

**Verification checklist:**

- [ ] Versions and hardware are observed, not assumed.
- [ ] Required modules/device operation verified.
- [ ] Environment recreation instructions tested or limitations explicit.
- [ ] No sensitive data sent to unapproved compute.

**Common mistakes:** Depending on a temporary notebook image; recording only framework version and omitting drivers/backend.

**Recovery procedure:** Resolve compatible pins, recreate environment and record changes; do not continue with an unexplained runtime mismatch.

**Definition of Done:** A documented tested runtime exists for pipeline implementation and later reproducibility checks. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-024](#step-024)

---

<a id="step-024"></a>
## STEP-024 — Approve baseline, experiment and evaluation plans

**Objective:** Specify scientific comparisons, model selection and metric/timing conventions before training.

**Why this step exists:** Post-result choices introduce selection bias and ambiguous metrics.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-022/023 complete; G03 and G08 current; dataset support and runtime limits known.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus methodological review.

**Parallelizable:** Timing and detection-metric drafts can be prepared separately; approval reconciles them.

**Inputs:** RQs, baseline choice, REL/SPLIT, observed hardware and UD12-UD16.

**Expected outputs:** Approved experiment matrix, training/stopping/selection policy, evaluator/timing protocol and resolved executable configuration schema.

**Repository/file changes:** Create `07_Experiments/experiment_plan.md`, finalize `06_Models/baseline_plan.md`, `09_Evaluation/protocol.md`, and T14 schema.

**Execution procedure:**

1. Define baseline and feasible controlled factors, budgets, repeats/seeds and stopping rules.
2. Specify class-aware matching, mAP@0.5, P/R operating-point selection, NMS and absent-class rules.
3. Specify timing boundary, warm-up/repetitions, batch/precision/hardware and FPS calculation.
4. Adopt or decline optional analyses with reasons; distinguish validity gates from any approved scientific success target.

**Planning/review prompt:**

> Produce a prospective RQ-to-experiment-to-analysis plan using actual constraints. Preserve required mAP@0.5/FPS and identify every unspecified evaluator setting rather than relying on defaults.

**Implementation prompt:**

> Save approved plans and config schema; build validation rules that reject unresolved required fields. Do not populate result values or select thresholds using test data.

**Human-only actions and decisions:** Supervisor/researchers approve UD12-UD16, budgets, analysis scope and validation selection criterion.

**Version-control/artifact expectations:** Commit timestamped plan before full runs; later amendments are explicit, versioned and classified as prospective or post hoc.

**Documentation updates:** Experiment matrix, metric/timing protocol, configuration contract and decision register.

**Verification checklist:**

- [ ] Every planned comparison answers an approved RQ.
- [ ] Required metrics fully defined, including IoU distinctions.
- [ ] Selection uses validation only.
- [ ] Optional analyses/budgets decided prospectively.

**Common mistakes:** Picking the best seed afterward; conflating NMS IoU with matching IoU; invented speed target.

**Recovery procedure:** Resolve missing choices before G09; document amendments and prohibit retroactive claims of preregistration.

**Definition of Done:** Complete approved baseline/evaluation plans ready for implementation and smoke validation. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-025](#step-025)

---

<a id="step-025"></a>
## STEP-025 — Implement data loading, training and evaluator interfaces

**Objective:** Build a minimal configuration-driven pipeline with meaningful correctness checks.

**Why this step exists:** Reusable interfaces prevent hidden notebook settings and inconsistent metric computation.

**Governing section references:** [OS §2](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-024 approved plans; STEP-023 runtime; G08 release available.

**Estimated difficulty and time (provisional):** Hard; 1–3 provisional focused development days, split by loader/trainer/evaluator.

**Parallelizable:** Loader and evaluator modules can be developed against agreed schemas; integration follows.

**Inputs:** Config/schema, REL/class map, selected YOLO API and evaluation protocol.

**Expected outputs:** Pipeline package, thin entry commands, config/manifest validation and geometry/metric tests.

**Repository/file changes:** Implement `src/opg/` modules, `tests/`, and thin `13_Automation/` entry points; document commands in `12_Documentation/pipeline.md`.

**Execution procedure:**

1. Implement loader/annotation adapter that uses locked membership and rejects class-map/hash mismatch.
2. Wrap training and validation with complete effective-config capture and explicit output locations.
3. Implement prediction coverage and evaluator adapter with protocol-controlled settings.
4. Test known small detection cases: perfect match, miss, duplicate, wrong class, no predictions and absent-class behavior.

**Planning/review prompt:**

> Review interfaces and tests for source-coordinate accuracy, partition isolation and metric semantics. Specify failures that must stop execution rather than be silently skipped.

**Implementation prompt:**

> Implement the approved minimal package and thin callers. Keep scientific parameters in config; add meaningful tests for geometry, matching, coverage and invalid inputs using synthetic/permitted fixtures.

**Human-only actions and decisions:** Method reviewer approves metric interpretation and any implementation-driven protocol clarification.

**Version-control/artifact expectations:** Commit code, safe fixtures and tests; no medical images/checkpoints in source history.

**Documentation updates:** Pipeline commands, schema contracts, effective default capture and test evidence.

**Verification checklist:**

- [ ] Loader uses exact REL/SPLIT/class-map hashes.
- [ ] Effective settings are recorded.
- [ ] Known-case evaluator tests produce expected counts.
- [ ] No final-test access during development.

**Common mistakes:** Assuming a library's default mAP field is the required metric; dropping empty images from coverage.

**Recovery procedure:** Fix failing adapters/tests, verify against manually checked fixtures and rerun integration before readiness.

**Definition of Done:** Approved interfaces implemented and correctness checks pass on non-test development fixtures. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-026](#step-026)

---

<a id="step-026"></a>
## STEP-026 — Verify checkpoint recovery and baseline readiness

**Objective:** Prove a small training-to-recovery-to-inference path and pass G09.

**Why this step exists:** Long runs should not discover missing state, broken labels or unrecoverable artifacts.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-025 package tests pass; G08 current; approved complete config and storage policy.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus short smoke execution.

**Parallelizable:** Logging/storage review may accompany smoke execution; recovery verification waits for a checkpoint.

**Inputs:** Approved training subset and validation sample, environment lock, checkpoint policy and config.

**Expected outputs:** Smoke evidence, reload/resume comparison, backup retrieval proof, effective settings and G09 assessment.

**Repository/file changes:** Create `08_Checkpoints/checkpoint_policy.md`, smoke records under `07_Experiments/` with clearly identified diagnostic purpose, and G09 review.

**Execution procedure:**

1. Define checkpoint roles, immutable naming, state capture, retention and backup behavior.
2. Run a prospectively labeled smoke experiment using training/validation only; inspect label overlays and finite outputs.
3. Interrupt and restore, checking saved epoch/state/config and backup hashes; record exact-resume limitations honestly.
4. Verify config, loader/evaluator/timing instrumentation and all G09 readiness criteria.

**Planning/review prompt:**

> Audit readiness for the first full baseline. Require observed checkpoint recovery and correct data/evaluation behavior; do not infer exact resume from a weights-only file.

**Implementation prompt:**

> Run the diagnostic smoke plan and interruption/restore test, recording all actual state components. Verify logs persist outside transient output and fetch a checkpoint backup to confirm its hash.

**Human-only actions and decisions:** Researchers/method reviewer accepts G09; approve a limited recovery policy if exact resume is unsupported, without mislabeling it.

**Version-control/artifact expectations:** Keep diagnostic EXP/RUN records and checkpoint manifests; binaries in artifact tier, source/tests in Git.

**Documentation updates:** Checkpoint policy, smoke/recovery report, runtime limitations and G09 assessment.

**Verification checklist:**

- [ ] Training/validation load and predictions align.
- [ ] Checkpoint reload and available state restoration demonstrated.
- [ ] Backup retrieval/hash verified.
- [ ] G09 PASS; no test data accessed.

**Common mistakes:** Calling a full failed run a smoke test retrospectively; saving only notebook output.

**Recovery procedure:** Preserve failure evidence, fix loader/checkpoint/logging issues and repeat diagnostic test with appropriate new IDs.

**Definition of Done:** G09 PASS with tested baseline execution and recovery readiness. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-027](#step-027)

---

<a id="step-027"></a>
## STEP-027 — Register and validate a full experiment

**Objective:** Create an immutable, fully specified EXP before spending compute.

**Why this step exists:** A run without a frozen configuration cannot support a reproducible comparison.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-026 complete; G09 PASS; approved experiment plan and current REL; for repeats, STEP-030 authorization.

**Estimated difficulty and time (provisional):** Moderate; 1–2 hours per experiment.

**Parallelizable:** Independent experiment preparation allowed; ID allocation and resource scheduling controlled.

**Inputs:** Approved matrix row, REL/MC IDs, complete settings, source revision and artifact policy.

**Expected outputs:** EXP record, config/hash, run manifest, hypothesis, output locations and launch checklist.

**Repository/file changes:** Create `07_Experiments/EXP####/config.yaml`, `README.md`, `run_manifest.json`; update Experiment Registry.

**Execution procedure:**

1. Assign a new EXP and link its RQ, baseline/comparison and changed factor.
2. Resolve all effective settings, input hashes, seed and stopping/selection rules.
3. Record code revision and configuration hash separately; verify class map, split and storage.
4. Review launch checklist and reserve compute; no training starts until prerequisites are current.

**Planning/review prompt:**

> Review this experiment against the approved matrix and fairness rules. Identify changed versus controlled factors and reject missing settings or stale gates.

**Implementation prompt:**

> Create the immutable experiment bundle, run config/input validation and register its actual ready state. Do not launch until validation and required human decisions are complete.

**Human-only actions and decisions:** Researcher authorizes the approved matrix row and resource use; supervisor reviews departures.

**Version-control/artifact expectations:** Commit launch metadata before execution; record dirty-code state or require clean revision per policy. Never overwrite a launched config.

**Documentation updates:** Experiment README/registry, launch checklist, dashboard and resource estimate.

**Verification checklist:**

- [ ] All references resolve and hashes match.
- [ ] Config has no unresolved required fields.
- [ ] Comparison/stopping/seed policy explicit.
- [ ] Current gates verified and artifact space available.

**Common mistakes:** Hidden command-line overrides; config pointing to a newer data release than the comparison baseline.

**Recovery procedure:** Correct prelaunch bundle and revalidate; if already launched, preserve it and create a new EXP for changed settings.

**Definition of Done:** Experiment ready with validated immutable inputs and documented authorization. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-028](#step-028)

---

<a id="step-028"></a>
## STEP-028 — Train the registered experiment and preserve every attempt

**Objective:** Execute the approved training/validation run with durable logs and checkpoints.

**Why this step exists:** Training results must survive interruptions and remain tied to the actual configuration.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §12](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-12); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-027 launch checklist complete; G09 and data gates current; authorized compute available.

**Estimated difficulty and time (provisional):** Hard; 1–2 hours active setup/monitoring per session plus measured training time, unknown until run.

**Parallelizable:** Independent approved EXPs only if compute permits; never mix outputs or access final test.

**Inputs:** Frozen config, code/runtime, approved training/validation release and checkpoint destinations.

**Expected outputs:** RUN records, complete logs/learning curves, checkpoints, validation outputs and actual stop/failure state.

**Repository/file changes:** Populate `07_Experiments/EXP####/` logs/observations/run manifest and `08_Checkpoints/checkpoint_registry.csv`; store binaries in artifact tier.

**Execution procedure:**

1. Recheck environment/input/config hashes and capture effective settings at runtime.
2. Train using training data, monitor validation under the fixed policy, and persist logs/checkpoints.
3. If interrupted, verify a recovery checkpoint and record whether continuation is exact resume or a new experiment.
4. Save actual termination reason and verify artifacts before ending the compute session.

**Planning/review prompt:**

> Review the launch/recovery runbook for this EXP. Identify monitored anomalies, permitted intervention and evidence that must persist before shutdown.

**Implementation prompt:**

> Execute only the registered configuration. Log warnings, OOM/divergence and interruption honestly; never silently alter batch size, seed, data or stopping budget.

**Human-only actions and decisions:** Researcher decides whether to stop for safety/resource failures; scientific configuration changes require a new approved EXP.

**Version-control/artifact expectations:** Persist artifacts during the run and hash-check transfers. Commit permitted logs/metadata; do not expose sensitive paths or images.

**Documentation updates:** Run manifest, observations, checkpoint ledger and failure report when needed.

**Verification checklist:**

- [ ] Actual settings match registered config or deviations explicitly invalidate/reclassify the run.
- [ ] Training and validation only; test sealed.
- [ ] Logs and checkpoints durable and hash-verified.
- [ ] All attempts and stop reasons recorded.

**Common mistakes:** Leaving sole outputs in an ephemeral session; quietly retrying with changed settings under the same EXP.

**Recovery procedure:** Document interruption/lost work, restore only verified state or start a new EXP; never reconstruct missing metric history.

**Definition of Done:** Run reaches an approved stop or documented failure with preserved evidence; scientific eligibility is assessed next. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-029](#step-029)

---

<a id="step-029"></a>
## STEP-029 — Audit completion and register models/checkpoints

**Objective:** Determine candidate eligibility and pass G10 for each valid completed experiment.

**Why this step exists:** A weight file alone does not establish valid training or recoverable provenance.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-028 stopped with logs/artifacts; original config and input hashes available.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per EXP.

**Parallelizable:** Model-card drafting and hash verification can run independently; final eligibility waits for all evidence.

**Inputs:** Actual RUN logs, stopping reason, validation records, checkpoint manifests and exports.

**Expected outputs:** Completed or failed EXP record, model/card if eligible, checkpoint integrity report and G10 assessment.

**Repository/file changes:** Update Experiment/Checkpoint/Model registries; write `06_Models/cards/MODEL####.md`, EXP conclusions/failure report and G10 review.

**Execution procedure:**

1. Reconcile epochs/steps, logs, stopping criterion, config and all attempts.
2. Verify checkpoint reload, artifact hashes, backup pointers and available training state.
3. Register the selected validation checkpoint as a MODEL with class/preprocessing/license dependencies; validate exports if created.
4. Assess G10; preserve failed runs and keep ineligible models out of final selection.

**Planning/review prompt:**

> Audit whether this EXP met its predeclared completion criteria. Separate poor-but-valid performance from invalid execution and describe any missing evidence.

**Implementation prompt:**

> Validate checkpoint integrity and registry lineage, save actual summaries and model cards. Do not edit historical metrics/configuration or mark an incomplete run complete.

**Human-only actions and decisions:** Experiment reviewer accepts eligibility and G10; researcher approves any declared limitations.

**Version-control/artifact expectations:** Commit safe registry/card/audit records; retain immutable binaries, logs and failed attempts under storage policy.

**Documentation updates:** Model card, EXP conclusion/failure analysis, checkpoint report and G10 record tied to EXP ID.

**Verification checklist:**

- [ ] Stopping and full output history reconcile.
- [ ] Model links to verified CKPT/EXP/REL.
- [ ] Export behavior checked if used.
- [ ] G10 PASS only for valid complete runs; failures retained.

**Common mistakes:** Discarding negative runs; selecting a checkpoint without its validation criterion.

**Recovery procedure:** Retrieve missing evidence from verified backup; otherwise mark ineligible and rerun a new EXP rather than inventing completion.

**Definition of Done:** Every attempted run is accounted for; qualifying candidate has G10 PASS and registered model. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-030](#step-030)

---

<a id="step-030"></a>
## STEP-030 — Execute the approved controlled experiment matrix

**Objective:** Complete justified comparisons and sensitivity runs before final selection.

**Why this step exists:** A contribution claim needs controlled evidence rather than an isolated favorable baseline.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §12](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-12); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** Baseline STEP-029 G10 PASS; approved matrix and remaining budget; G09 current.

**Estimated difficulty and time (provisional):** Hard; 2–4 hours planning/review per experiment plus measured compute; total provisional.

**Parallelizable:** Yes across independent approved comparisons with sufficient resources; serialize shared registry updates.

**Inputs:** Baseline results on validation, approved factors/repeats, RQs and fairness invariants.

**Expected outputs:** All planned EXPs or documented prospective amendments, comparison data, failure records and matrix completion review.

**Repository/file changes:** Repeat STEP-027-029 under new EXP/MODEL IDs; update `experiment_plan.md`, Experiment Registry and validation comparison report.

**Execution procedure:**

1. Check whether each planned comparison is still feasible and record any amendment before execution.
2. Create distinct configs for each factor/seed and hold non-target factors fixed.
3. Run and audit each via STEP-027-029; retain all negative/failed outcomes and G10 statuses.
4. Build the validation-only comparison with budgets, variability and limitations; close or explicitly dispose of every planned row.

**Planning/review prompt:**

> Review the controlled matrix for fairness, resource feasibility and RQ coverage. Propose only justified prospective amendments; do not choose runs based on final-test results.

**Implementation prompt:**

> Execute approved matrix rows using the registered pipeline and new EXP IDs. Aggregate validation results without dropping unfavorable seeds or failed attempts.

**Human-only actions and decisions:** Supervisor/researcher approves matrix amendments and stopping further search; no test access authorized here.

**Version-control/artifact expectations:** Keep immutable per-EXP bundles and complete attempt inventory; version comparison scripts/data and amendment decisions.

**Documentation updates:** Matrix status, comparison report, G10 per qualifying EXP, failed-run lessons and budget actuals.

**Verification checklist:**

- [ ] Every matrix row has an outcome or documented disposition.
- [ ] All comparison factors and budgets explicit.
- [ ] All seeds/attempts retained.
- [ ] No final-test-driven changes or cherry-picking.

**Common mistakes:** Changing resolution and augmentation together while claiming a one-factor effect; reporting only the best seed.

**Recovery procedure:** Label confounded comparisons exploratory, run a properly controlled new EXP if feasible or withdraw the unsupported claim.

**Definition of Done:** Approved experimental program complete enough for validation-only selection, with all candidate G10 evidence available. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-031](#step-031)

---

<a id="step-031"></a>
## STEP-031 — Select on validation and freeze final-test evaluation

**Objective:** Freeze the final model and analysis before opening test data; pass G11.

**Why this step exists:** Model/threshold selection after test inspection biases the final performance estimate.

**Governing section references:** [OS §5](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-030 completed matrix; G10 PASS for every candidate considered; G07-G09 current.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus supervisor/evaluation review.

**Parallelizable:** No for selection and freeze; independent writing background may continue.

**Inputs:** Validation-only comparisons, selection rule, planned evaluator/timing protocol and test-access history.

**Expected outputs:** Selected MODEL/CKPT, fixed P/R operating point and NMS settings, immutable protocol/config hashes, G11 assessment.

**Repository/file changes:** Create `09_Evaluation/freeze.md`; finalize protocol version, decision records, frozen artifact manifest and G11 review.

**Execution procedure:**

1. Apply the predeclared validation criterion and document tradeoffs without peeking at test outcomes.
2. Choose operational thresholds from validation only and distinguish them from AP score collection settings.
3. Freeze model, PP/class map/REL, evaluator, matching/AP settings, timing/optional analyses and failure policy.
4. Audit prior test access and approve test release only if independence claims remain defensible.

**Planning/review prompt:**

> Audit final selection against the prospective rule and test-access history. Identify any contamination or unfrozen setting; no test evaluation may begin with an unresolved item.

**Implementation prompt:**

> Save a hash-addressed freeze bundle and validation selection evidence. Configure final-test execution to reject a different checkpoint, class map or protocol.

**Human-only actions and decisions:** Supervisor and evaluation reviewer approve G11 and test access (UD13-UD15 finalized).

**Version-control/artifact expectations:** Commit freeze before test execution; archive selected model/config/protocol hashes and access record.

**Documentation updates:** Selection decision, threshold rationale, freeze manifest, test custody release and G11 assessment.

**Verification checklist:**

- [ ] Selection and thresholds based only on validation.
- [ ] All evaluation and timing settings frozen.
- [ ] Prior test exposure reviewed and disclosed.
- [ ] G11 PASS precedes test prediction timestamp.

**Common mistakes:** Using test PR curves to pick confidence; assuming a renamed test set is unseen.

**Recovery procedure:** Stop, disclose exposure and redesign with untouched approved data or explicitly exploratory claims; reassess G07/G11 as needed.

**Definition of Done:** G11 PASS and a reproducible frozen final-test specification exists. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-032](#step-032)

---

<a id="step-032"></a>
## STEP-032 — Generate and validate final-test predictions

**Objective:** Produce complete held-out predictions from the frozen inference artifact.

**Why this step exists:** Metrics require aligned ground truth, valid coordinates and explicit zero-detection/failure coverage.

**Governing section references:** [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §8](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-08); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-031 complete; G11 PASS; authorized test access and frozen bundle available.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus inference duration.

**Parallelizable:** Deterministic image batches may run independently under the same frozen configuration; aggregate carefully.

**Inputs:** Frozen MODEL/CKPT/PP/REL, test manifest and approved annotation release.

**Expected outputs:** EVAL record, predictions, evaluated-image coverage ledger, integrity/geometry report and failure counts.

**Repository/file changes:** Create `09_Evaluation/EVAL####/` predictions/coverage/manifests; update Evaluation Registry.

**Execution procedure:**

1. Verify model, data, class-map, code and protocol hashes against freeze.
2. Run inference on every scheduled test image without fitting or threshold tuning.
3. Write one coverage record per image, including no detections and processing errors; store object predictions separately.
4. Check coordinate inversion, labels/scores, duplicates, coverage and ground-truth alignment before metric computation.

**Planning/review prompt:**

> Review final-test inference against freeze and completeness requirements. Specify how zero detections and failed inputs remain visible in reporting.

**Implementation prompt:**

> Run the frozen model and emit predictions plus coverage ledger. Fail on hash mismatch and log all processing failures; do not silently drop images or adjust settings.

**Human-only actions and decisions:** Evaluation lead authorizes execution under G11; reviewer decides handling of unforeseen failures under the preapproved policy.

**Version-control/artifact expectations:** Full predictions/private visualizations in approved artifact storage; hashes and safe aggregate coverage in Git.

**Documentation updates:** Evaluation Registry, prediction-validation report, access log and deviation record.

**Verification checklist:**

- [ ] Freeze hashes match execution.
- [ ] Every intended image accounted for.
- [ ] Reference-coordinate boxes and class IDs valid.
- [ ] No post-test model or threshold change.

**Common mistakes:** Interpreting zero boxes as a failed file; excluding difficult failed images without reporting denominators.

**Recovery procedure:** Mark invalid execution, repair only verified bugs under a new EVAL with disclosure, and preserve original output; model changes trigger test-exposure policy.

**Definition of Done:** Validated frozen-model predictions and complete coverage are ready for metrics. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-033](#step-033)

---

<a id="step-033"></a>
## STEP-033 — Compute Precision, Recall and mAP with explicit IoUs

**Objective:** Calculate required detection metrics and adopted additional analyses reproducibly.

**Why this step exists:** Undefined matching, thresholds or class aggregation make reported mAP uninterpretable.

**Governing section references:** [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-032 prediction validation passed; frozen evaluator/protocol; known-case metric tests passed.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus optional resampling compute.

**Parallelizable:** Yes with STEP-034 after shared freeze; per-class analyses use the same protocol.

**Inputs:** Validated predictions, exact ground truth, coverage ledger, frozen AP/matching settings.

**Expected outputs:** P/R counts and values, per-class AP/mAP@0.5, support counts, optional adopted analyses and metric provenance.

**Repository/file changes:** Write `09_Evaluation/EVAL####/metrics.csv`, per-class/PR data and metric interpretation notes; store sensitive detail appropriately.

**Execution procedure:**

1. Apply the specified class-aware one-to-one matching and record TP/FP/FN at the frozen P/R operating point.
2. Compute AP from confidence-ranked detections and report mAP@0.5 with evaluator/interpolation details.
3. Report class supports, missing-class/zero-denominator behavior and all planned aggregations.
4. Run only adopted uncertainty/repeat/subgroup analyses with stated units and limits; retain raw intermediate evidence.

**Planning/review prompt:**

> Audit metric definitions and denominators. Verify AP IoU 0.50, distinguish NMS IoU, and specify how unsupported classes and undefined Precision/Recall are represented.

**Implementation prompt:**

> Compute metrics with the frozen tested evaluator and save settings, counts, curves and hashes. Do not change a threshold to improve test results or omit weak classes.

**Human-only actions and decisions:** Evaluation reviewer verifies mathematical/implementation interpretation and any disclosed deviation.

**Version-control/artifact expectations:** Version computation code and safe metric outputs; full per-image evidence remains in its approved tier.

**Documentation updates:** Metric dictionary, per-class support, denominator conventions and evaluation report draft.

**Verification checklist:**

- [ ] Required P/R and mAP@0.5 computed under explicit settings.
- [ ] TP/FP/FN and class supports reconcile.
- [ ] AP curve not truncated by a display threshold without disclosure.
- [ ] Optional analyses follow prior adoption; no selective reporting.

**Common mistakes:** Reporting mAP without IoU; averaging undefined classes silently; treating each object as independent for uncertainty.

**Recovery procedure:** Invalidate erroneous metric outputs, correct implementation with new EVAL/correction record and disclose the change; never replace historical files silently.

**Definition of Done:** Reproducible detection metric package complete with honest uncertainty and support. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-034](#step-034)

---

<a id="step-034"></a>
## STEP-034 — Measure inference speed under the frozen timing protocol

**Objective:** Report FPS and latency with reproducible measurement boundaries.

**Why this step exists:** Hardware, batch size and asynchronous execution can dominate apparent speed.

**Governing section references:** [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §8](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-08); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-031 freeze and STEP-032 validated model execution; approved timing workload/hardware available.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus repeated timed runs.

**Parallelizable:** Yes with STEP-033 if workload/resources do not interfere with timing; isolate measurement from competing load.

**Inputs:** Frozen inference artifact, declared workload, timing protocol and actual hardware/runtime.

**Expected outputs:** Raw timing samples, mean/median/tail latency where supported, FPS, failure counts and full runtime context.

**Repository/file changes:** Write `09_Evaluation/EVAL####/timing/` raw samples, hardware record and `timing_report.md`.

**Execution procedure:**

1. Confirm backend/precision/image size/batch/concurrency and mark exact included/excluded processing stages.
2. Perform specified warm-up and timed repetitions, synchronizing accelerator work appropriately.
3. Record successes/failures, image count and duration; separate cold start/model-only/end-to-end boundaries as adopted.
4. Calculate FPS and latency statistics with units; disclose resource variability and avoid clinical efficiency conclusions.

**Planning/review prompt:**

> Review timing for synchronization, workload equivalence and honest boundaries. Explain the relationship between batch throughput and single-image latency without treating them as interchangeable.

**Implementation prompt:**

> Run the frozen benchmark with raw samples and actual device/runtime records. Include the approved processing stages and synchronization; do not report an unmeasured device or hide failed inputs.

**Human-only actions and decisions:** Evaluation lead approves benchmark conditions and any unavoidable hardware deviation; changes require a versioned timing assessment.

**Version-control/artifact expectations:** Retain raw timing evidence and artifact hashes; commit safe summaries and commands.

**Documentation updates:** Timing methodology, runtime details, FPS/latency table and limitations.

**Verification checklist:**

- [ ] Hardware/software and timing boundary complete.
- [ ] Warm-up/repetitions/synchronization recorded.
- [ ] FPS derived from matching counts and duration.
- [ ] All failures and variability disclosed.

**Common mistakes:** Timing only a dispatched GPU call; comparing batch FPS with single-image clinical latency.

**Recovery procedure:** Invalidate faulty benchmark, fix boundaries/instrumentation, rerun under a new documented evaluation/timing record and retain earlier samples.

**Definition of Done:** Required inference-speed evidence produced under a reproducible protocol. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-035](#step-035)

---

<a id="step-035"></a>
## STEP-035 — Consolidate final evaluation and pass G12

**Objective:** Create one traceable final evaluation report with all required metrics.

**Why this step exists:** Scattered favorable numbers are not a complete evaluation record.

**Governing section references:** [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-033/034 complete; frozen model traceability intact; adopted analyses completed or deviations reviewed.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus reviewer sign-off.

**Parallelizable:** Report drafting and evidence cross-check can be divided; final assessment requires all inputs.

**Inputs:** Predictions/coverage, detection metrics, timing, optional analyses and deviation records.

**Expected outputs:** Final evaluation report, complete Evaluation Registry, comparison limitations and G12 assessment.

**Repository/file changes:** Finalize `09_Evaluation/EVAL####/report.md`; update `evaluation_registry.csv`, Claims and G12 review.

**Execution procedure:**

1. Reconcile every reported value to metric/timing evidence and each model/data/protocol version.
2. Include Precision, Recall, mAP@0.5 and FPS plus per-class support and timing conditions.
3. Describe all attempted comparisons, failures and deviations; distinguish validation selection evidence from final-test results.
4. Audit G12 and restrict empirical claims to valid, reproducible evidence.

**Planning/review prompt:**

> Audit the full evaluation package for omitted metrics, ambiguous IoU, selective reporting and mismatched timing conditions. Produce an itemized PASS/FAIL assessment.

**Implementation prompt:**

> Assemble tables/report directly from validated outputs, preserving full precision in source data and documented presentation rounding. Save actual assessment evidence; do not manufacture missing values.

**Human-only actions and decisions:** Evaluation reviewer approves G12 and interpretation limits; supervisor reviews consequential deviations.

**Version-control/artifact expectations:** Commit safe report/registry/aggregate evidence; preserve private predictions and models with stable hashes.

**Documentation updates:** Evaluation report, claim links, comparison caveats, dashboard and G12 assessment.

**Verification checklist:**

- [ ] All four required metrics and settings reported.
- [ ] Counts, versions and timing evidence reconcile.
- [ ] No omitted unfavorable planned result.
- [ ] G12 PASS is based on validity, not a desired performance level.

**Common mistakes:** Mixing best metrics from different checkpoints; presenting incomparable published results as a superiority ranking.

**Recovery procedure:** Correct provenance/comparisons, rerun only justified invalid computations with new records and reassess G12.

**Definition of Done:** G12 PASS and the final quantitative evidence package is complete. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-036](#step-036)

---

<a id="step-036"></a>
## STEP-036 — Review errors, annotation uncertainty and limitations

**Objective:** Produce systematic failure analysis and bounded conclusions; pass G13.

**Why this step exists:** Aggregate scores do not explain where the detector fails or justify clinical claims.

**Governing section references:** [OS §6](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-035 complete; G12 PASS; permitted examples and qualified reviewer available.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per review batch plus dental review.

**Parallelizable:** Case categories may be reviewed in disjoint batches under one sampling protocol.

**Inputs:** Final evaluation, prospective error-sampling rule, reference labels and image-quality metadata.

**Expected outputs:** Error taxonomy/counts, reviewed examples, label-uncertainty notes, limitations and G13 assessment.

**Repository/file changes:** Create `09_Evaluation/EVAL####/error_review.md` and `limitations.md`; update Claims and permitted asset specs.

**Execution procedure:**

1. Select cases systematically, including successes, misses, spurious/duplicate/wrong-class and localization errors.
2. Review actual images/labels with qualified input and distinguish model failure from uncertain reference labels.
3. Describe observable patterns and possible causes without asserting unsupported causality.
4. Bound generalization and clinical interpretation; route any confirmed label correction through versioned correction policy and assess G13.

**Planning/review prompt:**

> Review failure patterns without cherry-picking. State observed evidence separately from causal hypotheses and identify limits due to data, annotation, grouping and hardware.

**Implementation prompt:**

> Generate approved case-selection data and permitted overlays from recorded predictions. Preserve selection logic; do not alter labels or tune the model based on final-test errors.

**Human-only actions and decisions:** Dental reviewer adjudicates interpretation; supervisor approves limitations and clinical wording.

**Version-control/artifact expectations:** Keep sensitive examples restricted; publish only approved de-identified assets. Preserve every correction and original evaluation.

**Documentation updates:** Error report, limitations, claim wording and G13 review.

**Verification checklist:**

- [ ] Sampling method and denominators documented.
- [ ] Errors and label uncertainty distinguished.
- [ ] Possible causes clearly qualified.
- [ ] No validated clinical diagnosis/workload claim inferred; G13 evidenced.

**Common mistakes:** Showing only attractive examples; treating a missed box as proof of disease absence.

**Recovery procedure:** Rebuild representative sample, revise unsupported explanations and re-audit; label changes require ANN/REL/EVAL versioning and disclosure.

**Definition of Done:** G13 PASS with systematic error evidence and appropriately limited conclusions. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-037](#step-037)

---

<a id="step-037"></a>
## STEP-037 — Package the research inference prototype and guide

**Objective:** Make the evaluated image-to-box pipeline usable as a bounded research prototype.

**Why this step exists:** A reproducible demonstration needs a stable entry point and clear limitations, not an unrelated product build.

**Governing section references:** [OS §2](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §8](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-036 complete; G12-G13 PASS; evaluated model/export and UD18 interface decision.

**Estimated difficulty and time (provisional):** Moderate; 4–8 hours, split into packaging and verification sessions.

**Parallelizable:** Guide drafting can accompany packaging; use the same frozen evaluated inference path.

**Inputs:** Registered model, deterministic PP, class map, permitted demonstration inputs and error contract.

**Expected outputs:** Minimal inference entry point, structured results/optional overlays, failure handling and prototype guide.

**Repository/file changes:** Finalize inference entry point in `src/opg/` and thin caller in `13_Automation/`; write `12_Documentation/prototype_guide.md` and permitted demonstration records.

**Execution procedure:**

1. Choose the approved minimal interface and load all model/preprocessing dependencies by versioned configuration.
2. Return class-labeled boxes in original-image coordinates with model/version/status/timing metadata.
3. Test valid, zero-detection, unsupported/corrupt input, missing-model and class-map mismatch cases.
4. Verify export/source output compatibility and label the prototype as research-only supplementary support.

**Planning/review prompt:**

> Review the minimum demonstration needed for the report's final detection output. Keep it consistent with the evaluated artifact and identify any export or interface change requiring re-evaluation.

**Implementation prompt:**

> Package the existing evaluated pipeline and documented entry command. Add clear structured errors and provenance; do not introduce a separate clinical decision or treatment recommendation system.

**Human-only actions and decisions:** Researchers approve UD18 and demonstration material; dental reviewer checks output interpretation.

**Version-control/artifact expectations:** Commit code/guide and safe tests; distribute weights/images only under approved rights. No public hosting requirement is introduced.

**Documentation updates:** Prototype guide, input/output contract, failure cases, version dependencies and limitations.

**Verification checklist:**

- [ ] Boxes map to the reference image correctly.
- [ ] Class labels/model/PP versions displayed or exported.
- [ ] Zero detections distinguished from diagnosis and processing failure.
- [ ] Export behavior matches evaluated model within approved tolerance.

**Common mistakes:** Changing inference preprocessing for a prettier demo; presenting confidence as diagnostic certainty.

**Recovery procedure:** Restore frozen inference behavior or register/evaluate a new artifact; correct guide and rerun functional checks.

**Definition of Done:** A documented, tested research prototype reproduces the evaluated detection behavior. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-038](#step-038)

---

<a id="step-038"></a>
## STEP-038 — Perform a clean-environment reproducibility audit

**Objective:** Verify that recorded artifacts and instructions reproduce the reported results; pass G14.

**Why this step exists:** A working developer session does not prove another researcher can recover the study.

**Governing section references:** [OS §8](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-037 package/guide; G12-G13 current; authorized artifact access and declared reproduction-level plan.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours active audit plus compute/transfer; retraining, if adopted, adds measured run time.

**Parallelizable:** Independent artifact inventory can proceed while environment is recreated; comparisons follow execution.

**Inputs:** Source/config locks, DS/ANN/REL/SPLIT pointers, model/checkpoint, evaluator, raw results and prospective tolerances.

**Expected outputs:** Fresh-environment run evidence, artifact restore proof, metric/figure comparison and G14 assessment.

**Repository/file changes:** Write `12_Documentation/reproduce.md`, `reproducibility_audit.md`; update artifact pointers, gate records and affected evidence if corrected.

**Execution procedure:**

1. Use a fresh authorized environment and only recorded installation/access instructions.
2. Retrieve versioned artifacts, verify hashes and execute inference/evaluation from the documented commands.
3. Compare regenerated predictions/metrics and representative figure data within predeclared tolerances; record hardware context.
4. Assess inference replay and any adopted retraining separately, explain discrepancies and evaluate G14.

**Planning/review prompt:**

> Audit reproducibility without relying on hidden local state. Specify which levels are verified, lawful access limits and expected tolerance before comparing outcomes.

**Implementation prompt:**

> Run the documented clean reproduction, retain actual command outputs and hashes, and report every discrepancy. Do not silently patch archived results to make them match.

**Human-only actions and decisions:** Reproduction reviewer confirms evidence and limitations; researchers/supervisor approve any revised reproducibility claim.

**Version-control/artifact expectations:** Commit safe audit/commands; preserve fresh-run output and restored artifacts in approved tiers. Restricted data stays restricted.

**Documentation updates:** Reproduction guide, access instructions, discrepancy resolution, environment record and G14 review.

**Verification checklist:**

- [ ] Fresh environment and artifact retrieval demonstrated.
- [ ] Hashes match archived parents.
- [ ] Metrics/representative outputs reproduced or discrepancies resolved transparently.
- [ ] G14 states the actual reproduction level, not an untested promise.

**Common mistakes:** Calling metric replay full retraining; relying on an untracked local package or inaccessible private path.

**Recovery procedure:** Identify missing dependency/artifact, repair documentation or implementation with new versions, repeat affected evaluations and reassess G12-G14.

**Definition of Done:** G14 PASS with independently followable reproduction and explicit limits. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-039](#step-039)

---

<a id="step-039"></a>
## STEP-039 — Build the writing evidence map and submission plan

**Objective:** Map thesis/paper sections to verified evidence and actual submission requirements.

**Why this step exists:** Writing from memory creates unsupported claims and late format surprises.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §14](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-14); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-038 complete; G03 and G12-G14 current; verified literature and scientific records.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours plus format/authorship clarification.

**Parallelizable:** Evidence mapping and institutional-format retrieval can proceed separately.

**Inputs:** RQ/objectives, Claims, evaluation/error/reproducibility reports, actual institutional/venue instructions.

**Expected outputs:** Writing Registry, section outline, claim-to-evidence map, submission requirements and UD17 decisions.

**Repository/file changes:** Populate `11_Writing/writing_registry.csv`, `writing_plan.md`, thesis/paper requirement notes and canonical bibliography links.

**Execution procedure:**

1. Collect actual thesis format, deadlines, required declarations, authorship and review expectations.
2. Map each planned section to specific CLAIM/P/EXP/EVAL/FIG/TAB evidence and missing items.
3. Separate thesis depth from concise paper framing while using the same evidence base.
4. Approve the paper obligation/venue/disposition pathway without inventing a required publication acceptance.

**Planning/review prompt:**

> Build an evidence-first writing plan aligned with O1-O3 and actual submission instructions. Mark gaps in evidence and distinguish planned methods from performed methods.

**Implementation prompt:**

> Save the section/evidence map and requirement records. Do not create result prose or citation entries unsupported by the canonical evidence base.

**Human-only actions and decisions:** Supervisor/authors settle UD17, authorship, format, deadlines and paper requirement.

**Version-control/artifact expectations:** Commit writing plan and safe evidence links; keep confidential review correspondence restricted.

**Documentation updates:** Writing Registry, submission schedule with provisional estimates, requirements and decision records.

**Verification checklist:**

- [ ] Every substantive planned claim has evidence or a visible blocker.
- [ ] Actual institutional/venue instructions recorded.
- [ ] Thesis and paper share one evidence source.
- [ ] Authorship and paper disposition responsibilities explicit.

**Common mistakes:** Choosing a journal and declaring submission mandatory without agreement; duplicated conflicting bibliography files.

**Recovery procedure:** Resolve requirements with supervisors, remove unsupported section promises and update the evidence map before drafting.

**Definition of Done:** Approved writing plan and evidence map support complete thesis/paper drafting. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-040](#step-040)

---

<a id="step-040"></a>
## STEP-040 — Draft thesis chapters from realized evidence

**Objective:** Write the complete thesis with traceable methods, results and limitations.

**Why this step exists:** The final document must describe what was actually done rather than what the proposal hoped to achieve.

**Governing section references:** [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-039 approved map; valid results and methods evidence; required chapter structure known.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per chapter/section session, repeated to full draft; total provisional.

**Parallelizable:** Independent sections may be drafted against one glossary/evidence base; integration review follows.

**Inputs:** Writing map, verified literature, actual configs/data counts, evaluations and limitations.

**Expected outputs:** Full chapter drafts, abstract/conclusion grounded in realized findings, references and appendices.

**Repository/file changes:** Create `11_Writing/thesis/` chapter sources and update Writing Registry/review states.

**Execution procedure:**

1. Draft background and literature with verified citations and bounded gap claims.
2. Describe actual data, annotation, splits, YOLO settings and evaluation including deviations.
3. Present all required metrics and relevant negative/failed experiments without selective omission.
4. Write discussion/conclusion and abstract from results, preserving supplementary-prototype and generalization limits.

**Planning/review prompt:**

> Draft the assigned chapter from the linked evidence only. Flag missing information as Evidence pending, distinguish observations from explanations, and avoid claiming validated clinical utility.

**Implementation prompt:**

> Documentation authoring: save source-grounded chapter drafts with internal evidence links and revision history. Never fill a missing metric, count or citation with plausible text.

**Human-only actions and decisions:** Authors own scientific wording; supervisor reviews interpretation and contribution statements.

**Version-control/artifact expectations:** Commit coherent chapter versions; preserve prior drafts and cited artifact versions.

**Documentation updates:** Writing Registry, missing-evidence queue, terminology list and chapter review notes.

**Verification checklist:**

- [ ] All required sections drafted at appropriate depth.
- [ ] Methods match actual configs and counts.
- [ ] Claims/citations traceable and negative outcomes retained.
- [ ] No research result invented; pending evidence clearly visible.

**Common mistakes:** Copying proposal future tense into realized methods; presenting optional unperformed analyses as completed.

**Recovery procedure:** Replace unsupported passages with evidence or remove/restrict claims, correct method descriptions and update affected sections consistently.

**Definition of Done:** A complete evidence-grounded thesis draft exists, ready for asset/citation verification. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-041](#step-041)

---

<a id="step-041"></a>
## STEP-041 — Generate figures/tables and verify every citation and claim

**Objective:** Make the manuscript's visual and textual evidence internally consistent and reproducible.

**Why this step exists:** A correct experiment can still be misrepresented by captions, rounding, references or selected examples.

**Governing section references:** [OS §3](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §14](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-14); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-040 full draft; source data and scripts for planned assets; permissions for illustrative images.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours per verification batch, depending on assets/citations.

**Parallelizable:** Citation verification, asset generation and claim auditing can run separately; reconcile one issue ledger.

**Inputs:** Draft, canonical bibliography, Claims, metrics/timing, asset specifications and image permissions.

**Expected outputs:** Rendered verified figures/tables, captions, verified citations, claim audit and consistency report.

**Repository/file changes:** Populate `10_Figures_Tables/` specs/data/rendered and `assets.csv`; update thesis sources, Claims, Writing Registry and review report.

**Execution procedure:**

1. Generate assets from recorded data with versioned commands and declared units/aggregation.
2. Inspect rendered figures/tables, captions, identifiers, rounding and permitted medical examples.
3. Check every citation against its original source and every empirical statement against artifact evidence.
4. Reconcile titles, class/model/data names, counts, IoU settings, abbreviations, numbering and cross-references.

**Planning/review prompt:**

> Audit the manuscript and assets for unsupported claims, citation errors and inconsistent metric definitions. Explain every issue with its exact source or artifact reference.

**Implementation prompt:**

> Generate figures/tables from real stored values and run citation/link/consistency checks. Do not manually improve plotted results or create a citation merely to fill a gap.

**Human-only actions and decisions:** Authors approve wording/asset choices; dental reviewer checks permitted radiographic examples; supervisor reviews claim boundaries.

**Version-control/artifact expectations:** Version specs, scripts, safe data and reviewed rendered assets; private examples remain restricted.

**Documentation updates:** Asset Registry, captions, claim/citation verification states and issue/resolution report.

**Verification checklist:**

- [ ] Every asset has source/version/command/caption.
- [ ] Every used citation verified and bibliography consistent.
- [ ] Numbers/settings agree across chapters and tables.
- [ ] Identifying imagery and unsupported clinical/novelty claims absent.

**Common mistakes:** Copying bibliographic errors from the report; using different checkpoints' metrics in one unlabeled row.

**Recovery procedure:** Regenerate incorrect assets, correct citations from original evidence and revise every affected claim/location; preserve correction history.

**Definition of Done:** Visuals, citations and claims are verified and consistent with the evidence. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-042](#step-042)

---

<a id="step-042"></a>
## STEP-042 — Complete supervisor review and submission-readiness audit

**Objective:** Resolve substantive reviews, assemble the final draft and pass G15.

**Why this step exists:** Submission readiness requires actual review and format compliance, not merely a complete text file.

**Governing section references:** [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-041 checks complete; G03/G12-G14 current; actual institutional requirements known.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per revision cycle plus supervisor turnaround, unknown.

**Parallelizable:** Independent formatting/reference fixes can proceed; final approval waits for all required review.

**Inputs:** Verified thesis, actual supervisor comments, submission checklist and evidence audits.

**Expected outputs:** Reviewed assembled thesis, responses, final rendering inspection and document-scoped G15 / thesis assessment. Paper drafting/readiness is handled independently in STEP-044 and does not block thesis readiness.

**Repository/file changes:** Update `11_Writing/thesis/`, `reviews/`, readiness/submission checklist and G15 review.

**Execution procedure:**

1. Collect actual supervisor comments and record each with response/action/evidence.
2. Revise scientific content and reopen affected gates if a substantive method/result changes.
3. Assemble and inspect the full document including cover, tables, figures, references and appendices.
4. Verify institutional declarations/permissions/format and obtain final authorization; assess G15.

**Planning/review prompt:**

> Audit submission readiness against actual requirements and supervisor feedback. List unresolved essential items and distinguish editorial fixes from changes needing new scientific evidence.

**Implementation prompt:**

> Apply approved revisions, compile the submission-format document and run consistency checks. Save actual review responses and do not assert approval until it is received.

**Human-only actions and decisions:** Supervisor and authors approve final content/submission; institutional checks completed as required.

**Version-control/artifact expectations:** Version reviewed draft, final compiled-file hash and response records; no overwritten submitted versions.

**Documentation updates:** Review-response ledger, writing completion status, format checklist and G15 assessment.

**Verification checklist:**

- [ ] All substantive comments resolved or explicitly accepted by reviewer.
- [ ] Essential Evidence pending placeholders removed/resolved.
- [ ] Full rendered document inspected.
- [ ] G15 PASS includes actual supervisor authorization.

**Common mistakes:** Inventing feedback because the source form is blank; marking a checklist complete without approval.

**Recovery procedure:** Return failed items to the owning step, revise/reverify and obtain actual sign-off; do not submit while G15 fails.

**Definition of Done:** G15 PASS and authorized thesis submission files are ready. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-043](#step-043)

---

<a id="step-043"></a>
## STEP-043 — Submit the thesis and preserve the exact submission

**Objective:** Complete the actual thesis submission and retain evidence of what was submitted.

**Why this step exists:** Prepared or uploaded drafts do not equal confirmed institutional submission.

**Governing section references:** [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-042 complete; G15 PASS; institution's actual destination/process and authorization known.

**Estimated difficulty and time (provisional):** Moderate; 1–3 hours plus institutional processing.

**Parallelizable:** No for final submission; archive preparation may proceed on the exact approved version.

**Inputs:** Approved final thesis/supplements, submission instructions and required author/supervisor declarations.

**Expected outputs:** Submission receipt/confirmation, submitted file hashes, immutable submission snapshot and status record.

**Repository/file changes:** Create `11_Writing/thesis/submission.md`; preserve submitted files and receipt in approved storage pending STEP-045 archive.

**Execution procedure:**

1. Recheck that final file hashes match the approved version and all required attachments are present.
2. Have the authorized researcher submit through the actual institutional process.
3. Verify receipt/status and record date, destination, files and any pending administrative issue.
4. Keep the submitted version immutable; route later revisions to new versions.

**Planning/review prompt:**

> Prepare a concrete submission checklist from the actual institution's requirements and approved files. Distinguish ready, sent/uploaded and confirmed-submitted states.

**Implementation prompt:**

> Prepare the approved file bundle and checksum list; record actual confirmation supplied by the authorized submitter. Do not fabricate a receipt or perform unrequested external communication.

**Human-only actions and decisions:** Authorized researcher performs submission and any required declarations/signatures.

**Version-control/artifact expectations:** Commit safe submission metadata; retain exact final files/receipts in permitted storage and tag a release only after verified event.

**Documentation updates:** Submission record, dashboard and pending administrative actions.

**Verification checklist:**

- [ ] Submitted files match approved hashes.
- [ ] Actual receipt or institutional confirmation retained.
- [ ] Date/destination/status accurate.
- [ ] Earlier drafts and submitted snapshot preserved.

**Common mistakes:** Calling a locally generated PDF submitted; editing the submitted file without versioning.

**Recovery procedure:** Resolve institution-reported issues, resubmit only as authorized and retain both versions/receipts; correct premature status.

**Definition of Done:** Thesis submission confirmed with exact artifact and receipt evidence. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-044](#step-044)

---

<a id="step-044"></a>
## STEP-044 — Prepare the paper pathway and record submission or disposition

**Objective:** Produce a defensible paper package and carry out the approved publication obligation.

**Why this step exists:** The roadmap must support a paper without inventing a venue, acceptance or mandatory publication outcome.

**Governing section references:** [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-043 thesis record; UD17 publication obligation/venue decision; same valid evidence base and current reviews.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per writing/revision session plus external review time, unknown.

**Parallelizable:** Paper sections/supplements may be prepared independently; final author approval and submission are sequential.

**Inputs:** Thesis evidence, selected venue instructions if adopted, authorship/permission decisions and reviewer comments when received.

**Expected outputs:** Concise paper/supplements and verified submission evidence if required; otherwise explicit approved deferral/not-required disposition with rationale.

**Repository/file changes:** Create `11_Writing/paper/` manuscript, submission/disposition record and `reviews/` response ledger; update Writing Registry.

**Execution procedure:**

1. Adapt the evidence to a concise method/results/limitations narrative without inventing new novelty.
2. Check actual venue scope/format, authorship, declarations, permissions and availability statements.
3. Assess G15 / paper against the actual manuscript/version, citations/claims/figures, supplements, venue requirements and author/supervisor approval. Record a separate AssessmentID in the gate ledger and block paper submission until PASS. Then submit through the authorized researcher if required and preserve the receipt.
4. Track real reviewer comments and versioned responses; new experiments reenter gated workflow. Record an approved deferral if submission is not currently required.

**Planning/review prompt:**

> Prepare the paper from the same verified evidence and actual venue rules. Identify any unsupported claim and specify submission or an explicit approved disposition; never assume acceptance.

**Implementation prompt:**

> Save approved manuscript/supplements, run citation/claim checks and record real submission/reviewer evidence. If publication is deferred, preserve the package and decision rather than claiming completion of a submission.

**Human-only actions and decisions:** Authors/supervisor approve venue, authorship, declarations and submission/disposition; researcher performs external submission.

**Version-control/artifact expectations:** Version all submitted/revised manuscripts and receipts; retain reviews subject to confidentiality.

**Documentation updates:** Paper status, author approvals, review responses, separate G15 / paper assessment in the gate ledger, and submission receipt or approved disposition.

**Verification checklist:**

- [ ] Paper claims match valid evidence.
- [ ] G15 / paper PASS is recorded before any paper submission; an approved deferral/not-required disposition is not labeled PASS.
- [ ] Actual venue/author requirements satisfied when submitting.
- [ ] Submission distinguished from acceptance.
- [ ] Required obligation met or explicit approved disposition recorded.

**Common mistakes:** Making G16 depend on uncertain journal acceptance; asserting a paper was submitted when only drafted.

**Recovery procedure:** Correct status, revise unsupported text and resolve publication obligations with supervisor; preserve review history.

**Definition of Done:** Approved paper obligation fulfilled through G15 / paper PASS followed by verified submission, or through documented accepted deferral/not-required disposition without a fictitious PASS; future reviews remain tracked. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-045](#step-045)

---

<a id="step-045"></a>
## STEP-045 — Create immutable release archives and verify restoration

**Objective:** Preserve the study, submissions and lawful access information beyond active development.

**Why this step exists:** A finished thesis is not enough if models, labels, protocols or source revisions are lost.

**Governing section references:** [OS §8](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-043/044 submission/disposition records; UD20 retention/access decision; scientific gates current.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours plus transfer/restore duration.

**Parallelizable:** Tier-specific inventory can proceed independently; final manifest and restore verification are consolidated.

**Inputs:** All source/config/model/data/evaluation/writing records, permissions, release decisions and receipts.

**Expected outputs:** ARCH release manifest, source snapshot/tag, restricted artifact inventory, final documents, access/retention instructions and restore proof.

**Repository/file changes:** Populate `15_Archive/archive_manifest.csv` and immutable ARCH snapshot/manifest; retain large/private artifacts in approved external tiers.

**Execution procedure:**

1. Inventory every final deliverable and its dependencies, versions/hashes, licenses and sensitivity.
2. Create immutable release snapshots and stable artifact pointers; separate any public subset from restricted data.
3. Verify a restore covering source, a representative data/label manifest, model, predictions/metrics and submission files.
4. Record retention, access owner, backup location and outstanding future publication tasks without altering earlier archives.

**Planning/review prompt:**

> Design a release manifest that can recover the actual study while respecting data and software licenses. Identify missing dependencies and verify retrieval rather than assuming backups exist.

**Implementation prompt:**

> Create the approved immutable snapshot/manifests, calculate hashes and perform restore checks. Never upload restricted data to a public release or overwrite an earlier ARCH object.

**Human-only actions and decisions:** Researchers/custodian approve archival access/retention/public subset under UD20; release owner authorizes snapshot.

**Version-control/artifact expectations:** Tag a verified source revision; archive manifests and permitted records in Git, large/private bytes in approved storage with backup.

**Documentation updates:** Archive index, access/retention guide, restore report and release notes.

**Verification checklist:**

- [ ] All final artifacts/dependencies inventoried and hashed.
- [ ] Permissions and sensitivity control distribution.
- [ ] Restore checks actually performed.
- [ ] Submitted versions/receipts immutable and recoverable.

**Common mistakes:** Archiving only a thesis PDF; using expiring links as sole artifact locators.

**Recovery procedure:** Retrieve missing artifacts, replace unstable pointers with approved versioned storage, repeat restore and preserve archive correction history.

**Definition of Done:** Complete lawful immutable archive and verified recovery evidence exist. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-046](#step-046)

---

<a id="step-046"></a>
## STEP-046 — Perform the final project-completion audit

**Objective:** Declare completion only after every approved obligation is evidenced; pass G16.

**Why this step exists:** Planning completeness, scientific validity, submission and archival are distinct accomplishments.

**Governing section references:** [OS §1](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §9](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./OPG_RESEARCH_OPERATING_SYSTEM.md#os-13); [canonical schemas and DoD](./OPG_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** STEP-045 archive verified; all applicable prior gates current PASS; thesis receipt and paper disposition recorded.

**Estimated difficulty and time (provisional):** Moderate to hard; 3–5 hours plus supervisor sign-off.

**Parallelizable:** Deliverable inventory can be independently checked; final completion decision is serialized.

**Inputs:** Full gate ledger, scientific registries, deliverable inventory, submission records and archive/restore evidence.

**Expected outputs:** Project-completion audit, final dashboard, handover record and G16 assessment.

**Repository/file changes:** Create `01_Project_Management/reviews/project_completion_audit.md`; update `gates.csv`, `dashboard.md` and archive manifest with final audit pointer.

**Execution procedure:**

1. Check every deliverable in OS Section 13.3 against actual artifacts and versions.
2. Confirm each gate is current for the final lineage, including G10 for every qualifying reported experiment.
3. Verify thesis receipt, paper obligation/disposition, limitations, reproducibility and archive restoration.
4. Resolve blocking omissions, record supervisor/researcher decision and hand over remaining nonblocking future work.

**Planning/review prompt:**

> Audit the complete project against the handbook, not against an expectation of positive results. List PASS/FAIL evidence per deliverable and gate; do not mark missing obligations complete.

**Implementation prompt:**

> Generate the final inventory/cross-reference checks and save only evidence-supported audit states. Update the dashboard after actual G16 approval and preserve open future-study tasks separately.

**Human-only actions and decisions:** Researchers and supervisor accept project completion and ownership handover.

**Version-control/artifact expectations:** Commit final safe audit/ledger, bind it to the archived release and preserve backup evidence; no deletion of failed or negative experiments.

**Documentation updates:** Final completion audit, gate ledger, handover/access owner, final dashboard and archive index.

**Verification checklist:**

- [ ] Every approved deliverable exists with recoverable evidence.
- [ ] All applicable prior gates current PASS.
- [ ] Actual submission/disposition and restore evidence present.
- [ ] G16 approval recorded; no clinical validation or publication acceptance invented.

**Common mistakes:** Treating this planning document as proof the study is done; hiding open scientific blockers under future work.

**Recovery procedure:** Keep G16 FAIL, return to the owning step, repair/reassess affected gates and repeat the completion audit.

**Definition of Done:** G16 PASS and all approved research, documentation, submission and archival obligations evidenced. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** None. Close the approved project; later studies require a new approved plan.

---

<a id="roadmap-self-review"></a>
# Final review — roadmap validation record

## Coverage and source fidelity

This roadmap implements the approved title and the report's collection-to-evaluation workflow. It preserves the Figure 1 proposals of 70/15/15 allocation, mAP@0.5 and FPS while requiring implementation details and grouping constraints to be resolved transparently. Candidate dental targets remain examples until clinical/annotation approval. The blank feedback form is recorded as blank; no examiner comments or approvals are inferred.

The report's research-gap argument is tested in STEP-004-009. A narrowed or refuted gap remains in the evidence record. The plan requires honest detection and timing evaluation, not a predetermined favorable result or a clinical validation claim.

## Dependency and recovery review

- Repository and schema bootstrap precede literature/data registration. STEP-001 is explicitly allowed to save initial scope decisions before the complete skeleton, eliminating a bootstrap cycle.
- Data permissions precede acquisition; source quality precedes final class approval; protocol and prospective QA criteria precede pilot and production annotation.
- Patient/study/duplicate grouping precedes partition allocation. All fitted preprocessing and augmentation follow the locked split, while fixed annotation-viewing preparation retains a source-coordinate mapping.
- A canonical prepared release may be established before a YOLO candidate is selected. If that candidate requires different preprocessing, STEP-022 explicitly returns to STEP-019-021 for a new PP/REL and renewed G08. It cannot silently change the dataset used by an experiment.
- Baseline environment, evaluation plan, pipeline checks and checkpoint restore evidence precede full training. G10 applies to each qualifying experiment, including approved repeats.
- Final-test inference starts only after validation-only selection and G11 freeze. Error analysis does not authorize further tuning on the same final test. Exposure and correction procedures preserve the original record.
- Quantitative evaluation, limitations and reproducibility precede submission readiness. Actual thesis submission and paper submission/disposition precede archive and final completion. Journal acceptance is not an invented requirement.

## Canonical cross-reference checklist

| Item | Validation result for the planning documents |
|---|---|
| Exact approved title | Present verbatim in both documents |
| Scope | 2D OPG, YOLO, bounding-box localization, selected approved visible targets, research prototype |
| Stages and steps | S01-S15 aligned to STEP-001-046; contiguous unique step IDs |
| Gates | G01-G16 share names, ownership steps and evidence requirements with OS Section 13 |
| Decisions | UD01-UD20 remain canonical in OS Section 1.6; steps resolve them at their required milestones |
| Registries | OS Appendix B remains the sole schema/path authority; no competing scientific ledger introduced |
| Templates | T01-T28 installed by STEP-003 and instantiated in owning domain folders |
| Per-step completeness | All 46 steps contain all 20 labeled operational fields, including prerequisites, outputs, verification, recovery and DoD; title and ID appear in each heading |
| Links | Relative file links and explicit internal anchors checked across both documents |
| Topic contamination | Search found none of the unrelated reference-project concepts or implementation-stack mandates checked |
| Source history | Original hashes matched at v1.0.0 authoring; later user-directed deletion is recorded in OS Appendix F, with no claim of current source availability |

## Revision v1.1.0 corrections

- Deleted-source links now point to the historical source-status record. No restored source or backup is claimed; source-dependent uncertainties still require original evidence or documented clarification.
- STEP-002 establishes the minimal data-tool runtime and G02 verifies it. STEP-023 separately locks the YOLO runtime and protects earlier preprocessing provenance.
- G15 is assessed per document: thesis at STEP-042, paper at STEP-044 before its submission. A documented paper deferral is not a gate PASS. The 46 steps, 15 stages and 16 gate IDs are retained.

## Verification scope and initial execution state

The authoring review checked both files exist and are non-empty, exact title consistency, all 46 step blocks and required fields, relative-link/anchor targets, absence of unrelated template content, source-file hashes, and editor diagnostics. Manual review checked the stage/gate sequence, unknown scientific decisions, annotation workflow, test-isolation policy, reporting boundaries and source-grounded diagram details. At initial delivery the workspace contained the three sources and two plans. Following the user-directed deletion, it contains only the two planning deliverables; current source links point to the availability record rather than absent files.

These checks establish **planning-document completeness and consistency only**. They do not certify data quality, annotation agreement, a trained model, a passed scientific gate, a submitted thesis or a clinically validated system. All execution steps begin NOT STARTED and all G01-G16 gates remain NOT ASSESSED until their actual evidence is produced. Human adoption of the operating policies and resolution of blocking UD items are still future work.

**Start execution:** [STEP-001](#step-001). **Policy authority:** [OPG Research Operating System](./OPG_RESEARCH_OPERATING_SYSTEM.md).

*End of OPG Project Execution Blueprint — v1.1.0; 46 focused step types across 15 research stages.*
