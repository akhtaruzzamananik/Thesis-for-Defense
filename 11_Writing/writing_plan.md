# Evidence-First Writing Plan & Claim-to-Section Map (`STEP-039` / `S14`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-039` (`S14` — Build the writing evidence map and submission plan) |
| Decision Record | [DEC0017.md](../01_Project_Management/decision_log/DEC0017.md) (`UD17`) |
| Canonical Bibliography | [references.bib](../02_Literature/references.bib) *(shared single source for Thesis, Paper & Slides)* |
| Writing Registry | [writing_registry.csv](./writing_registry.csv) (`WRIT0001–WRIT0014`) |
| Planned Assets Ledger | [assets.csv](../10_Figures_Tables/assets.csv) (`FIG0001–FIG0006`, `TAB0001–TAB0006`) |
| Co-Authors | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |

---

## 1. Thesis Chapter-to-Evidence Map (`11_Writing/thesis/`, `WRIT0001–WRIT0008`)

Every substantive scientific statement in `STEP-040` MUST trace directly to the locked evidence IDs below (zero numbers drafted from memory!):

| `WritingID` | Chapter / File | Lead Author | Mapped Claims | Mapped Papers / Evidence | Mapped `EXP` / `EVAL` | Planned Assets | Open Blockers / Dependencies |
|---|---|---|---|---|---|---|---|
| `WRIT0001` | Front Matter, Declarations & Abstract (`00_front_matter_and_abstract.md`) | Joint (Anik & Mahajub) | `CLAIM0013–CLAIM0017` | `scope.md`, `final_evaluation_report.md`, `limitations.md` | `EXP0001–0013`, `EVAL0001–0014`, `XSHIFT01–06` | — | Final defense date confirmation (`UD17`) |
| `WRIT0002` | Ch. 1 Introduction, Problem Statement, `O1–O3` & `RQ0–RQ3` (`01_chapter1_introduction.md`) | Mahajub | `CLAIM0001–CLAIM0006`, `CLAIM0011` | `scope.md`, `research_questions.md`, `P0023`, `P0027`, `P0032`, `P0039` | — | `FIG0001` (Study Pipeline) | `FIG0001` generated in `STEP-041` |
| `WRIT0003` | Ch. 2 Systematic Literature Review & Gap Synthesis (`02_chapter2_literature_review.md`) | Mahajub | `CLAIM0001–CLAIM0012` | `02_Literature/synthesis.md`, `GAP0001–GAP0006`, `P0001–P0042` (`122` screened, `42` Core full-text) | — | `TAB0001` (Lit Gap & Audit Matrix) | `TAB0001` rendered in `STEP-041` |
| `WRIT0004` | Ch. 3 Methodology: 6-Cohort Portfolio, Leak-Free Grouping, Preprocessing & YOLO Architecture (`03_chapter3_methodology.md`) | Anik | `CLAIM0005`, `CLAIM0008–CLAIM0010` | `DS0001–0006`, `ANN0001–0006`, `SPLIT0001–0006`, `REL0001–0006`, `PP0001–0004`, `DEC0002–0016`, `protocol.md`, `freeze.md` | `EXP0000_SMOKE`, `EXP0001–0013` | `FIG0001`, `TAB0002` (Dataset & Split Summary), `TAB0003` (Experiment Matrix & Hyperparams) | `TAB0002–0003` rendered in `STEP-041` |
| `WRIT0005` | Ch. 4 Held-Out Experimental Results, Ablations, Cross-Country Shift & Speed Benchmarks (`04_chapter4_results.md`) | Mahajub | `CLAIM0013–CLAIM0017` | `final_evaluation_report.md`, `step033_final_metrics_report.md`, `timing_report.md`, `xshift_metrics.csv`, `STEP030_matrix_tracker.md` | `EXP0001–0013`, `EVAL0001–0014`, `XSHIFT01–06` | `TAB0004` (Master Scoreboard + `95% CI`), `TAB0005` (`RQ2` CLAHE vs `1280px` + `RQ3` GPU/CPU Pareto), `TAB0006` (`12` `HC01–HC05` Shift Table), `FIG0002` (Track & Per-Class Contrast Chart), `FIG0003` (`RQ2` Ablation Chart), `FIG0004` (`5`-Country Shift Heatmap), `FIG0005` (`RQ3` Accuracy vs GPU/CPU Latency Pareto) | `FIG0002–0005`, `TAB0004–0006` generated in `STEP-041` |
| `WRIT0006` | Ch. 5 Error Analysis, Label Uncertainty, Limitations & Research Prototype (`05_chapter5_discussion_and_prototype.md`) | Joint (Mahajub: Error/Disc; Anik: Prototype/Repro) | `CLAIM0006–CLAIM0007`, `CLAIM0014–CLAIM0017` | `error_review.md`, `limitations.md`, `step036_error_taxonomy.json`, `prototype_guide.md`, `reproducibility_audit.md` | `EVAL0001–0002`, `EVAL0009–0011`, `EVAL0013–0014`, `REPRO0001` | `FIG0006` (TIDE Error Taxonomy & Small/Medium/Large Recall Chart) | `FIG0006` generated in `STEP-041`; optional `S16` web URL added if `STEP-047–049` completed before final bind |
| `WRIT0007` | Ch. 6 Conclusion, Bounded Contributions & Future Work (`06_chapter6_conclusion.md`) | Joint | `CLAIM0013–CLAIM0017` | `final_evaluation_report.md`, `limitations.md`, `reproduce.md` | `EVAL0001–0014`, `XSHIFT01–06` | — | None (all scientific evidence locked at `G12–G14`) |
| `WRIT0008` | Appendices: Ontology `CLS0001–0041`, Freeze Hashes, Per-Class Tables & Reproducibility Ledger (`07_appendices.md`) | Anik | `CLAIM0013–CLAIM0017` | `classes.csv`, `freeze_manifest.json`, `g12_reconciliation_audit.json`, `reproduce.md`, `gates.csv` | `EXP0000_SMOKE`, `EXP0001–0013`, `EVAL0001–0014` | — | None |

---

## 2. Concise Optional Paper Draft Map (`11_Writing/paper/`, `WRIT0009–WRIT0013`)

Shares **one single evidence base** (`CLAIM0001–0017`, `EVAL0001–0014`, `02_Literature/references.bib`, `FIG0002–0006`, `TAB0004–0006`) without duplicating or contradicting thesis numbers:

| `WritingID` | Paper Section | Target Length | Shared Evidence |
|---|---|---|---|
| `WRIT0009` | Title, Abstract & Introduction | `~1.5` pages | `CLAIM0001–0004`, `CLAIM0010–0011`, `RQ0–RQ3` |
| `WRIT0010` | Related Work (Condensed 42-Core Audit) | `~1.5` pages | `CLAIM0001–0012`, `TAB0001` |
| `WRIT0011` | Materials, Leak-Free Splits, Preprocessing & Protocol | `~2.0` pages | `TAB0002`, `TAB0003`, `FIG0001`, `FREEZE0001` |
| `WRIT0012` | Held-Out Results, `RQ2` Ablations, `5`-Country Shift & `RQ3` Latency | `~3.0` pages | `TAB0004–0006`, `FIG0002–0005` |
| `WRIT0013` | Error Analysis, Limitations, Non-Clinical Guardrails & Conclusion | `~1.5` pages | `FIG0006`, `error_review.md`, `limitations.md`, `REPRO0001` |

---

## 3. Defense Slide Deck Plan (`11_Writing/slides/`, `WRIT0014`)

- **`WRIT0014`** (`defense_slides_outline.md` — `15–18` crisp defense slides): Title & O1–O3 -> Lit Gaps (`P0027` `84.9%`/`87.7%`) -> 6-Cohort Leak-Free Pipeline -> `13`-EXP Matrix & `G11` Freeze -> Held-Out Scoreboard + `95% CI` -> `RQ2` (`CLAHE` fails `3/3`, `1280px` wins!) -> `5`-Country Zero-Shot Domain Shift (`HC03 0.82` vs `HC02/01 0.16–0.24`) -> `RQ3` GPU vs CPU `ONNX` Pareto -> `T19` Error & Label Uncertainty Audit -> Bounded Research Prototype / Optional Web Showcase -> Limitations & Conclusion.

---

## 4. Shared Terminology & Non-Clinical Wording Glossary (`OS §9`)

| Preferred Term (Use Consistently) | Prohibited / Imprecise Term (NEVER Use) |
|---|---|
| `2D orthopantomogram (OPG)` / `panoramic dental radiograph` | `dental X-ray` without specifying 2D OPG modality |
| `radiographic finding / candidate bounding box` | `clinical diagnosis` / `confirmed disease` |
| `held-out test / external_test partition` | `unseen clinical trial` |
| `duplicate-cluster group-stratified split (GroupID)` | `strictly verified patient-level split` (where public metadata lacks patient IDs) |
| `zero detections (does not exclude pathology)` | `healthy / disease-free radiograph` |
| `end-to-end latency (T_e2e / FPS_e2e)` vs `model-only (FPS_infer)` | unqualified `real-time` claim |
| `supplementary non-clinical research prototype` | `clinical decision-support / diagnostic tool` |
