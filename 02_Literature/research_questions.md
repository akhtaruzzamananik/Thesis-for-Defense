# Research Questions, Contribution Limits & Evaluation Map (`STEP-009`)

| Metadata | Value |
|---|---|
| Record | `02_Literature/research_questions.md` |
| Version | `v0.9.0` (**Candidate-Final — STEP-009 technical mapping complete; awaiting Supervisor `G03` sign-off**) |
| Step / Gate | `STEP-009` / `G03` (**`NOT ASSESSED`**, Supervisor reviewer: Ms Faiza Feroz) |
| Authors / Owners | Mahajub Al Shabah (Literature Lead, `232-15-900`); Akhtaruzzaman Anik (Research Lead, `232-15-252`) |
| Literature Cutoff Date | **`2026-11-16`** (`SEARCH0001` + `SEARCH0002`: `180` files -> `122` unique screened -> `42` Core extracted `P0001–P0042`, `55` Reserve `P0043–P0097`, `25` Excluded `P0098–P0122`) |
| Date Updated | `2026-11-17` |
| Governing Sections | `OS §1.3–1.4`, `§3.3–3.4`, `§13.2`; `01_Project_Management/scope.md` (`v1.0.0`, `G01 PASS`); `02_Literature/synthesis.md` |

---

## 1. Bounded Scientific Contribution Statement (`STEP-009` Procedure #3)

Testing the six report hypotheses (`G1–G6`) against `42` full-text Core studies (`23` Group A + `19` Group B) plus `55` Reserve records **refuted** the broad novelty claim (`GAP0001` / `G1`) that YOLO/deep-learning `2D OPG` studies are limited to narrow single-class tasks (`13/23` Group A papers already cover `4–13` classes). Retaining the approved topic (`scope.md v1.0.0`, `O1–O3`), our contribution is honestly bounded to **three verified, feasible gaps (`GAP0002`–`GAP0006` plus the narrowed radiolucent-tier sub-problem of `GAP0001`)**:

1. **Leakage-controlled multi-class `2D OPG` benchmarking (`O1–O2`):** Address the stark performance disparity between high-contrast targets (`Impacted teeth, Implants, Crowns`: `0.83–0.98 mAP@0.50`) and small radiolucent/rare targets (`Caries 0.25–0.40`, `Periapical lesions 0.07–0.32`, `Supernumerary 0.00–0.58`) under deduplicated, patient/OPG-level splits, strict localization metrics (`mAP@0.50` + `mAP@0.50:0.95`, background `FP/FN`, fixed `conf/NMS` operating thresholds), and external `2D OPG` domain-shift checks where permitted.
2. **Falsifiable preprocessing and scale/tiling comparison (`O2`):** Empirically resolve whether raw unenhanced `OPG`, parameterized `CLAHE`, or resolution/background-aware tiling helps or harms multi-class pathology detection (`P0004` positive vs `P0011, P0029, P0038, P0041` negative/null evidence) under identical leak-free splits and deterministic metrics.
3. **Hardware-bounded accuracy–efficiency protocol (`O3`):** Eliminate unverified `"real-time"` claims (`73.8%` [`31/42`] of Core papers omit latency) by reporting single-image (`batch = 1`, post-warmup) GPU and CPU end-to-end timing decomposition (`T_preprocess + T_infer + T_postprocess = T_e2e`, `FPS_e2e`), parameter count, `GFLOPs`, VRAM, and systematic error profiling.

### Binding Scope Exclusions (`scope.md v1.0.0`, `G01 PASS` + `GAP0003`/`GAP0004`)
- Strictly **`2D OPG` bounding-box object detection** only: **no `3D CBCT` modeling**, **no segmentation replacement** (`GAP0003` confirms boxes outperform semantic seg for discrete multi-instance screening), **no whole-image/patch classifier substitution** (`GAP0002`), and **no cross-modality numeric ranking** against `CBCT`, bitewings (`BW`), periapical radiographs (`PA`), or intraoral clinical photos (`GAP0004`).
- Target classes (`UD04`) must exclude non-radiographic mucosal findings (`P0006 RR clinical R=0.506`), buccal surface labels (`P0003 TP=0`), initial non-cavitated enamel caries (`P0032`), or morphometric continuous root-length grading (`P0013`), and must not merge radiopaque fillings into caries labels (`P0016` flaw).
- **No fabricated target numbers or model locks here:** Dataset selection (`UD02–UD03`), final class table (`UD04`), split rules (`UD07–UD08`), preprocessing specs (`UD09`), YOLO model variants (`UD10`), thresholds (`UD13`), and timing protocol (`UD14`) remain **`Unresolved / Human Decision Required`** until their owning Phase 2 gates (`G04–G11`).

---

## 2. Candidate-Approved Research Questions (`O1–O3` <-> `GAP` <-> `CLAIM` <-> `EVAL`)

| RQ ID | Final Proposed Wording (awaiting `G03` sign-off) | Objectives (`O1–O3`) | Linked Gaps & Verified Claims | Data & Annotation Reqs (`S04–S08`) | Experimental Factor & Baseline (`S09–S11`) | Required Evaluation Metrics & Protocol (`S12–S14`) | Permitted Intended Claim Bounds (No Invention!) |
|---|---|---|---|---|---|---|---|
| **`RQ0`** *(Primary)* | How effectively and efficiently can an approved YOLO bounding-box detector localize predefined dental objects and radiographically visible abnormalities across available public `2D OPG` datasets under a deduplicated, patient/OPG-level leakage-controlled evaluation protocol? | `O1`, `O2`, `O3` | `GAP0001` (`refuted` broad / narrowed tier), `GAP0002`–`GAP0006`; `CLAIM0001`–`0012` | Verified `2D OPG` public dataset(s) (`UD02–UD03`), deduplicated (`UD07`), visible box ontology (`UD04–UD06`), immutable raw manifests (`G04–G08`) | Frozen baseline + compared modern single-stage YOLO detectors (`UD10, UD12`) selected strictly on `val` (`RF11`) | Held-out test evaluation once after `G11` freeze (`UD13, UD14`): `P, R, F1, mAP@0.50, mAP@0.50:0.95`, E2E `ms/FPS` | Bounded to tested cohorts, frozen operating threshold, and research screening scope (`scope.md`; **no autonomous diagnosis or clinical utility claim**). |
| **`RQ1`** *(Localization & Contrast Tiers)* | Under a deduplicated, patient/OPG-level grouped split (`UD07–UD08`), what overall, visibility-tier (high-contrast restorations/impactions vs. small radiolucent pathologies), and per-class bounding-box localization performance (`P`, `R`, `F1`, `mAP@0.50`, `mAP@0.50:0.95`) does the frozen YOLO detector achieve on held-out and (if available) external `2D OPG` test sets? | `O1`, `O2` | `GAP0001` *(narrowed radiolucent tier)*, `GAP0002`, `GAP0003`, `GAP0004`; `CLAIM0001`–`0007` | Public `2D OPG` source(s) checked for pre-augmented duplicates (`P0008`-style audit); unambiguous visible box schema (`UD04–UD05`); QA-verified boxes (`UD06`); multi-center/external `2D OPG` cohort if permitted (`UD02, UD15`) | Baseline YOLO architecture vs. modern scale/family comparators (`UD10`); unified multi-class detection (no Oracle-ROI `P0029` / tight tooth-crop truncation `P0032`) | Overall + per-class `P, R, F1, AP@0.50, AP@0.50:0.95` at stated single `conf/NMS` operating threshold (`UD13`); explicit background `FP/FN` counts; optional cross-dataset OPG shift check (`UD15`) | Distinguishes true spatial box detection from classifiers; honestly reports low-contrast/minority class drops; never ranks `2D OPG` numerically vs `CBCT`/`BW`. |
| **`RQ2`** *(Controlled Factor / Image Quality)* | Under identical grouped splits, class schemas, training budgets, and deterministic evaluation rules, how do candidate preprocessing and spatial-scale configurations (unenhanced raw `OPG` vs. parameterized `CLAHE` vs. resolution/tiling strategy under `UD09`) affect validation localization (`mAP@0.50`, `mAP@0.50:0.95`), small radiolucent pathology recall, and preprocessing time? | `O1`, `O2` | `GAP0005` (`CLAHE` clash `P0004` vs `P0011, P0029, P0038, P0041` + `P0008, P0015` tiling/res); `CLAIM0008`–`0010` | Same frozen dataset release & pre-aug split (`G07`); coordinate round-trip geometry checks (`OS §4.3`); training-only stochastic aug isolation (`UD09`) | Registered raw-input baseline vs. controlled single-factor variations: explicit `CLAHE (clipLimit, tileGridSize)` and/or resolution/background-aware tiling (`UD09, UD12`) | **Validation-set** head-to-head comparison (`RF11`) across seeds/runs (`UD12, UD15`) on `mAP@0.50`, `mAP@0.50:0.95`, per-class radiolucent `R/AP`, plus `T_preprocess` latency; winner frozen before held-out test | Resolves `CLAHE`/tiling impact strictly empirically for tested `2D OPG` distribution (**never assumes enhancement helps**; preserves negative/null findings). |
| **`RQ3`** *(Bounded Speed & Error Modes)* | Under an explicit single-image (`batch = 1`, post-warmup) GPU and CPU measurement boundary (`T_preprocess + T_infer + T_postprocess = T_e2e`), what end-to-end inference speed (`ms/OPG`, `FPS_e2e`) and computational footprint (`Params`, `GFLOPs`, peak VRAM) do compared detectors achieve, and what systematic radiographic failure modes and label uncertainties account for errors? | `O3`, `O2` | `GAP0006` (`73.8%` Core omit runtime; `P0009` omits `FPS_all`), `GAP0002`, `GAP0004`; `CLAIM0011`–`0012` | Representative held-out test set + permitted sample error-review gallery (`T19`, `S14`) | Lightweight/medium single-stage YOLO baselines (`UD10`) benchmarked on matched fixed hardware (`UD14`) | GPU + CPU `T_pre`, `T_infer`, `T_post`, `T_e2e`, `FPS_e2e` (`mean ± sd / median / IQR` over `N` OPGs after warmup, `UD14`); systematic categorized qualitative FP/FN audit (`T19` mimics/artifacts/label ambiguity) | No unmeasured `"real-time"` claims; clearly separates pure GPU pass from `T_e2e`; reports failure modes honestly without claiming clinical time savings (`O3`). |

*(**`S16` Defense Web Showcase Boundary:** Hosting the frozen validation-selected `G11`/`G12` model via `web/` and `16_Web_Demo/` at defense [`STEP-047–049`, `G17`, `UD21–UD24`] is an engineering demonstration deliverable displaying a research-only disclaimer and parity-checked inference outputs—not clinical deployment and not an additional scientific RQ.)*

---

## 3. Source-Verification Audit (`UD19` / `RF14` Disposition)

- **Deleted seed source status (`DEC0019`):** Per `OS Appendix F.1` and `01_Project_Management/reviews/source_inventory_2026-11-16.md`, the historical `Title Evaluation Report (1).pdf` (`SHA-256: 300EA7...`) was deleted prior to `STEP-001` at user request; its `References [1]–[13]` text is unavailable in the repository (`ReportRef = not-mapped-yet` across `papers.csv`).
- **Blueprint `STEP-009` Rule 2 Compliance (`line 594`):** All **`12`** trace claims (`CLAIM0001–0012`), all **`6`** tested gaps (`GAP0001–0006`), and every numerical statement in `02_Literature/synthesis.md` are verified **exclusively** from the **`42`** full-text Core papers extracted in `02_Literature/summaries/P0001.md`–`P0042.md` (cross-checked against legal PDFs and Publisher/Crossref DOIs in `papers.csv`: `111 verified-crossref` + `11 verified-pdf-page1`). **Zero** unverified `[1]–[13]` report strings are cited as supporting evidence.
- Formal human closure of `DEC0019` (`Option 1: Exclude deleted `[1]–[13]` from evidential support` vs. `Option 2: Supply external copy to verify`) is requested alongside `G03` in `01_Project_Management/meetings/STEP-009_supervisor_brief.md`.

---

## 4. Downstream Dependency Hand-Off (`G04–G17`)

| Downstream Gate / Step | Blocking UDs Governed by `RQ0–RQ3` | Immediate Readiness Action After `G03 PASS` |
|---|---|---|
| `G04` (`STEP-010–013`) | `UD02` (dataset(s)), `UD03` (licenses/ethics) | Screen candidate public `2D OPG` datasets flagged in `synthesis.md §6` (`DENTEX`, `UMFIH`, `Rahman 2024 Dhaka`, deduplicated `Do 2024`, `MD-OPG`, `AU-OPG`, `Tufts`) inside `03_Datasets/candidates.csv`. |
| `G05–G06` (`STEP-014–018`) | `UD04` (visible classes), `UD05` (box schema), `UD06` (QA/`κ`) | Lock radiographically visible class list excluding impossible `2D OPG` targets (`GAP0001, GAP0003, GAP0004`); appoint dental reviewer. |
| `G07–G08` (`STEP-019–021`) | `UD07` (dedup/grouping), `UD08` (`70/15/15`), `UD09` (`PP` factors) | Enforce pre-augmentation deduplication & patient/OPG grouping before splitting (`CLAIM0010`); register `Raw` vs parameterized `CLAHE` / tiling specs (`RQ2`). |
| `G09–G14` (`STEP-022–038`) | `UD10–UD18` (models, hardware, training, thresholds, timing) | Benchmark unified YOLO variants on fixed GPU+CPU rig (`RQ1–RQ3`) with `mAP@0.50`, `mAP@0.50:0.95`, `T_pre+T_infer+T_post`, and error review (`T19`). |

---

## 5. Supervisor Approval Block (`G03` Sign-Off — Required at `STEP-009`)

| Role | Name | Decision | Date | Evidence |
|---|---|---|---|---|
| Literature Lead (`STEP-004–009` owner) | Mahajub Al Shabah | Prepared / Endorsed (`v0.9.0`) | `2026-11-17` | `synthesis.md`, `GAP0001–0006`, `CLAIM0001–0012` |
| Research Lead / Reviewer | Akhtaruzzaman Anik | Technical Audit Endorsed (`v0.9.0`) | `2026-11-17` | `G03_assessment_2026-11-17.md`, `DEC0019.md` |
| **Supervisor (`G03` Mandatory Approver, `OS §13.2`)** | **Ms Faiza Feroz** | **Pending Supervisor Sign-Off** | | Brief sent: `01_Project_Management/meetings/STEP-009_supervisor_brief.md` |
| Co-supervisor *(if required)* | Israt Jahan | _(optional)_ | | |
