# DIU CSE B.Sc. Final Thesis Defense Slide Deck (`WRIT0014`)

> **Presentation Metadata:** `17` Slides · Target Duration: `15–18` minutes + Q&A  
> **Presenters:** Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`)  
> **Supervisors:** Ms Faiza Feroz (Supervisor) & Israt Jahan (Co-supervisor) — Dept. of CSE, Daffodil International University  
> **Evidence Lock:** Every metric strictly matches `FREEZE0001`, `EVAL0001–EVAL0014`, `XSHIFT01–06`, `ERRREV0001`, and `REPRO0001` (`G01–G14 PASS`).

---

## Slide 1 — Title & Research Identity
- **Title:** *A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO*
- **Team:** Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`), Dept. of CSE, DIU
- **Supervisors:** Ms Faiza Feroz (Supervisor) & Israt Jahan (Co-supervisor)
- **Scope Guardrail:** Non-clinical 2D OPG bounding-box detection research benchmark & parity-verified CPU prototype (**not** a clinical diagnostic device)
- *Speaker Cue (Anik, 45 s): Introduce title, team split, and strict non-clinical academic scope upfront.*

---

## Slide 2 — Clinical-Technical Motivation: Why 2D OPG Object Detection?
- Panoramic radiography (2D OPG) captures full upper/lower dentition, alveolar bone, and restorations in one low-dose exposure.
- Unlike whole-image classifiers (`P0002`, `P0038`), **spatial bounding-box detectors (YOLO)** localize *what* and *where* across up to 32 teeth.
- **Core Challenge:** High-contrast titanium implants coexist alongside tiny `< 0.2%`-area radiolucent caries & periapical lesions under 2D superimposition.
- *Speaker Cue (Mahajub, 60 s): Contrast bounding-box localization with image-level classification and highlight why 2D OPG is physically challenging.*

---

## Slide 3 — Systematic Literature Audit (`122` Screened -> `42` Core Full-Text)
- **Visual:** `TAB0001` (`10_Figures_Tables/tables/TAB0001_literature_audit.md`)
- `180` harvested -> `122` unique screened -> **`42` full-text Core studies** (`23` Group A direct OPG detectors + `19` Group B context/reviews).
- **Five Quantified Methodological Gaps (`GAP0001–GAP0006`):**
  1. **`84.9%` (`62/73`)** omit `mAP@0.50:0.95` (`Hartman et al., 2026` `P0027`).
  2. **`87.7%` (`64/73`)** perform zero external validation (`P0027`).
  3. **`73.8%` (`31/42`)** omit per-image inference latency (`ms/FPS`) (`CLAIM0011`).
  4. **Pre-split augmentation leakage** inflates identical data by **`+30.4%` `mAP@0.50`** (`0.9194` `P0011` vs `0.494–0.615` `P0008`).
  5. **Unresolved `CLAHE` contradiction:** `P0004` gain vs `P0011`, `P0029`, `P0038` drops (`CLAIM0008`).
- *Speaker Cue (Mahajub, 75 s): Emphasize we refute naive novelty ("first detector") and instead solve verifiable methodological rigor gaps.*

---

## Slide 4 — Objectives (`O1–O3`) & Research Questions (`RQ0–RQ3`)
- **`O1` / `RQ0`:** Leak-free, connected-component deduplicated multi-cohort 2D OPG benchmark across `6` public cohorts.
- **`O2` / `RQ1`:** Per-class contrast hierarchy, architecture scale (`YOLO11s/v8s/11m`), unseen external-hospital & **5-country zero-shot domain shift (`HC01–HC05`)**.
- **`O2` / `RQ2`:** Controlled preprocessing ablation (`Raw 640px` vs `CLAHE 2.0/3.0` vs `High-Res 1280px`) under locked splits & seed.
- **`O3` / `RQ3`:** Bounded single-image (`BS = 1`, `FP32`) **GPU (`Tesla T4`) vs CPU (`i5-1135G7 ONNXRuntime`)** end-to-end latency, `T19` error audit & `R1–R3` reproducible prototype.
- *Speaker Cue (Anik, 50 s): Map each RQ directly to the results slides ahead.*

---

## Slide 5 — Leak-Free Stage-Gated Governance Architecture (`G01–G14`)
- **Visual:** **`FIG0001`** (`10_Figures_Tables/figures/FIG0001_study_pipeline.svg`)
- **Zero Contamination Custody:**
  - `17,566` pre-augmented/unlabeled files quarantined (`G04`).
  - `281` duplicate/re-shoot copies removed via `SHA-256 + pHash + correlation` (`0` cross-partition `GroupID` leaks, `G07`).
  - Programmatic `_is_g11_passed()` lock sealed `test`/`external_test` until `FREEZE0001` (`G11`).
  - Raw OPGs & `.pt`/`.onnx` binaries strictly off-Git (`tracked_forbidden_count = 0`).
- *Speaker Cue (Anik, 60 s): Highlight the red custody wall between G01–G11 and blind single-pass test evaluation G12.*

---

## Slide 6 — Six-Cohort Portfolio (`6` Countries, `7,457` OPGs, `41,103` Boxes)
- **Visual:** `TAB0002` (`10_Figures_Tables/tables/TAB0002_dataset_splits.md`)
- **Never Blindly Merged:** Six independent tracks respecting granularity & licenses (`CLS0001–CLS0041`):
  - `TrackA` (`DS0001` Romania, `13` focal cls, `+178` external hospital)
  - `TrackB` (`DS0002` Türkiye DENTEX, `4` whole-tooth cls, `CC-BY-NC-SA` isolated)
  - `TrackC` (`DS0003` Bangladesh Dhaka handheld film, `6` cls, dual 5/6-cls eval)
  - `TrackD` (`DS0004` Vietnam Hanoi `PAI 3–5`, `3` focal apical cls, `3,863` OPGs)
  - `TrackE` (`DS0005` UAE Ajman AU-OPG, `6` whole-tooth cls)
  - `TrackF` (`DS0006` Iran Zanjan MD-OPG pediatric ages `3–12`, `2` focal caries cls)
- *Speaker Cue (Anik, 60 s): Mention why we discarded official DS0001 (27.5% leak) and DS0005 (4.4% leak) splits.*

---

## Slide 7 — Invertible Preprocessing (`PP0001–0004`) & `13`-EXP Matrix
- **Visual:** `TAB0003` (`10_Figures_Tables/tables/TAB0003_experiment_matrix.md`)
- **`TransformLedger` (`src/opg/preprocessing.py`):** Exact round-trip coordinate mapping (`max error = 0.0036 px @ 640`, `0.0041 px @ 1280`), ensuring every evaluation box is scored in original `[W, H]` pixels.
- **`13` Controlled Kaggle `Tesla T4` Runs (`EXP0001–EXP0013`):** Locked `AdamW`, `seed = 20261124`, `fliplr = 0.0` (preserves quadrant laterality).
- **`FREEZE0001` (`G11`):** `6` winners + `4` comparators frozen with `val`-only `conf_op`; **`3/3` degrading `CLAHE` models excluded before test access**.
- *Speaker Cue (Mahajub, 55 s): Explain why disabling horizontal flip matters anatomically and why val-only conf_op prevents test overfitting.*

---

## Slide 8 — `RQ0` Official Held-Out Scoreboard & `95%` Bootstrap CIs
- **Visual:** **`FIG0002` Panel A** + `TAB0004` (`10_Figures_Tables/figures/FIG0002_heldout_scoreboard_ci.svg`)
- Single-pass evaluation (`1,260` OPGs, `1,000`-resample `GroupID` `95% CI`):
  - **`TrackE` UAE (`MODEL0008`):** **`0.8246`** `[0.791, 0.859]` · `mAP50:95 = 0.5163`
  - **`TrackD` Hanoi `@1280` (`MODEL0013`):** **`0.4868`** `[0.453, 0.531]` · `mAP50:95 = 0.2207`
  - **`TrackB` DENTEX (`MODEL0004`):** **`0.4397`** `[0.399, 0.496]` · `mAP50:95 = 0.2673`
  - **`TrackA` Romania `@1280` (`MODEL0005`):** **`0.4165`** internal / **`0.4338`** external hospital
  - **`TrackC` Dhaka (`MODEL0006`):** **`0.2508`** (`5`-cls pathology **`0.2631`**)
  - **`TrackF` Pediatric (`MODEL0007`):** **`0.0537`** *(honest small-N `<0.2%`-area ceiling)*
- *Speaker Cue (Mahajub, 70 s): Emphasize close val-to-test calibration (0 leakage) and remind judges not to rank focal vs whole-tooth tracks numerically.*

---

## Slide 9 — `RQ1` Radiographic Contrast Hierarchy (`34` Active Classes)
- **Visual:** **`FIG0002` Panel B**
- **Tier 1 — High-Contrast Metallic & Structural (`0.73–0.998 AP@0.50`):**
  - `TrackE Implant = 0.9980 (80/80 recall)`, `Crowned = 0.9203`, `TrackA Ext Implant = 0.9297`, `TrackB Impacted = 0.9012`, `TrackA Surgical_Device = 0.8567`.
- **Tier 2 — Moderate Restorations & Ordinal Apices (`0.31–0.68`):**
  - `TrackA Endodontic = 0.6825`, `TrackD PAI_3 = 0.5878 / PAI_4 = 0.4976 / PAI_5 = 0.3751`, `TrackE Cavitated = 0.5420`.
- **Tier 3 — Diffuse & Ultra-Rare (`< 0.22`):**
  - `Bone_Resorption = 0.0906`, `Apical_Surgery = 0.0428 (GT=10)`, `Fractured_Tooth = 0.0000 (GT=2)`.
- *Speaker Cue (Mahajub, 55 s): Connect empirical contrast tiers directly back to CLAIM0002 & CLAIM0014.*

---

## Slide 10 — `RQ2` Controlled Ablation: `CLAHE` Fails (`3/3`) vs `1280px` Wins
- **Visual:** **`FIG0003`** (`10_Figures_Tables/figures/FIG0003_rq2_clahe_vs_1280.svg`)
- **Blanket `CLAHE` Refuted (`3/3` Validation Degradations):**
  - `TrackA CLAHE 2.0`: **`-0.037`** · `TrackA CLAHE 3.0`: **`-0.018`** · `TrackC Dhaka CLAHE 2.0`: **`-0.027`**
- **Spatial Resolution (`1280px` vs `640px`) Wins Across Both Tested Tracks:**
  - `TrackD Hanoi`: **`+0.0449` `mAP@0.50`** & **`+20.2%` rel. `mAP@0.50:0.95`** *(strictly non-overlapping `95% CIs`: `[0.203, 0.250]` vs `[0.166, 0.209]`!)*
  - `TrackA Romania`: **`+0.0350` internal / `+0.0622` external `mAP@0.50`** (`+22.5%` rel. external `mAP@0.50:0.95`).
- *Speaker Cue (Mahajub, 65 s): Highlight this as a centerpiece scientific finding—preserving pixels beats contrast filtering AND beats doubling parameters (`YOLO11m@640`).*

---

## Slide 11 — `RQ1` Five-Country Zero-Shot Cross-Cohort Shift (`12` Bridges)
- **Visual:** **`FIG0004`** + `TAB0006` (`10_Figures_Tables/figures/FIG0004_cross_country_shift.svg`)
- Frozen source checkpoints evaluated on unseen countries with **zero fine-tuning**:
  - **Strong Structural Transfer (`HC03 Impacted Tooth`):** Romania -> Türkiye **`0.8181`**, Romania -> Bangladesh **`0.7109`** *(beats Dhaka's own `0.6601`!)*, UAE -> Türkiye **`0.6967`**.
  - **Severe Radiolucent Collapse (`HC01–HC02`):** `HC02 Periapical` **`0.1779–0.2355`** (Romania <-> Vietnam); `HC01 Caries` **`0.1627–0.1635`** (UAE -> Türkiye/Dhaka).
  - **Box-Convention Sensitivity (`HC05`):** UAE whole-fixture+crown boxes drop on Romanian tight-fixture boxes (`0.0723` internal vs `0.4626` external).
- *Speaker Cue (Mahajub, 65 s): Explain why single-center accuracy cannot be assumed portable across countries for subtle pathologies.*

---

## Slide 12 — `RQ3` Bounded GPU vs CPU Latency & Pareto Frontier
- **Visual:** **`FIG0005`** + `TAB0005` (`10_Figures_Tables/figures/FIG0005_rq3_latency_pareto.svg`)
- Serial `BS = 1`, `FP32`, `10` warm-up + `100` timed OPGs (`0` failures):
  - **`1.8×–5.6×` Reporting Gap:** Pure `Tesla T4` `FPS_infer` (`20.2–70.4`) dramatically overstates true `FPS_e2e` (`6.35–38.20`) because full-res decode/letterbox is non-trivial.
  - **Pareto Winner:** `YOLO11s@1280` (`36.6 MB` ONNX) outperforms `YOLO11m@640` (`76.7 MB` ONNX) on `TrackA` at half the memory footprint.
  - **Sub-Second Consumer Laptop CPU (`Intel i5-1135G7`, `ONNXRuntime 1.32.0`, `0.983–0.997` parity IoU):**
    - `TrackE@640`: **`201.6 ms/OPG` (`4.96 FPS_e2e`)** · `TrackD@1280` / `TrackA@1280`: **`847.9–878.1 ms/OPG` (`1.14–1.18 FPS_e2e`)**.
- *Speaker Cue (Anik, 65 s): Emphasize sub-second CPU interactive feasibility for academic web demos without claiming clinical throughput.*

---

## Slide 13 — `T19` Systematic Error Taxonomy & Size-Bucket Recall (`G13`)
- **Visual:** **`FIG0006`** (`10_Figures_Tables/figures/FIG0006_error_and_size_recall.svg`)
- Exhaustive audit of **`6,718` GT boxes** (`0` post-hoc label/threshold edits):
  - **Monotonic `2.6×` Small-Target Bottleneck (`TrackA`):** `Large (>=1%) = 80.3%` -> `Medium = 66.4%` -> `Small (<0.2%) = 30.9%` *(identical on external hospital: `80.1% -> 65.2% -> 30.9%`!)*.
  - **Pediatric Ceiling (`TrackF`):** `100%` (`137/137`) of caries boxes are `< 0.2%` area (`12.4%` recall at `640px`).
  - **Ordinal Confusion Dominates `FP_Cls`:** **`86.7%` (`189/218`)** of `TrackD` class errors are adjacent `PAI 3 ↔ 4 ↔ 5` swaps (only `6.8%` completely missed!); **`65.9%`** of `TrackB` class errors are `Deep_Caries ↔ Caries`.
- *Speaker Cue (Mahajub, 65 s): Show how TIDE decomposition explains WHY metrics look the way they do.*

---

## Slide 14 — Visual Case Audit: Detector Failure vs Label & Physics Limits
- `28` deterministically sampled non-cherry-picked cases (`4` per primary winner eval) inspected visually off-Git:
  - **Source-Label Incompleteness (`DS0001_IMG_000722`):** Sharp OPG with `>15` visible radiopaque RCTs/bridges, but source GT boxed only `6` -> `27` apparent `FP_Bkg` are actually unannotated real restorations.
  - **2D OPG Physics Superimposition (`DS0005_IMG_000367`, `DS0001_IMG_000509`):** Cervical spine ghost washes out anterior mandibular caries and mimics metallic wire texture.
  - **Anatomical Mimics & Co-Firing (`DS0004_IMG_015992`):** Mental ridge shadow mimics `PAI_3`; class-aware NMS allows nested `PAI_3` inside `PAI_5`.
- *Speaker Cue (Mahajub, 60 s): This slide shows examiner-level critical maturity—distinguishing model error from dataset/physics limits.*

---

## Slide 15 — Packaged Research Prototype (`OPGPrototypeEngine`) & Reproducibility (`G14`)
- **Zero Train/Serve Skew:** Reuses frozen `src/opg/preprocessing.py` verbatim (`sha256: 011e67c0...`), enforces startup `SHA-256` hash verification, isolates `CC-BY-NC-SA` `MODEL0004`, and returns structured `OK / ZERO_DETECTIONS / ERROR` JSON with mandatory non-clinical disclaimer (`26/26` `pytest` passing).
- **Clean-Run Audit (`REPRO0001`, `32.23 s` on local CPU):**
  - **`R1` PASS:** `50/50` SHA-256 checksums exact (`0` mismatches).
  - **`R2` PASS:** Exact `Δ = 0.0` metric replay (`EVAL0001/0011/0013`).
  - **`R3A` PASS:** `0.0` ONNX CPU self-diff & `0.9938–0.9946` IoU parity vs `Tesla T4` PyTorch on `40` raw OPGs.
  - **`R3B` PASS:** Fresh `git archive` checkout (stripped `PYTHONPATH`, `0` off-Git files) passes `validate_repo.py` & tests.
  - **`R4` Transparently Archived:** Full `13`-EXP GPU training recipes (`seed = 20261124`) archived, honestly marked not re-executed.
- *Speaker Cue (Anik, 65 s): Highlight how any reviewer can clone and verify R1–R3 cleanly.*

---

## Slide 16 — Limitations & Strict Non-Clinical Guardrails
1. **2D OPG Physics Ceiling:** Not equivalent to 3D CBCT or intraoral bitewings (`P0039`, `P0032`).
2. **Bounded Patient Independence:** Public cohorts omit patient IDs; connected-component dedup removes exact/near duplicates (`0` leaks) but cannot link unlinked longitudinal visits.
3. **Single-Seed Matrix & YOLO Scope:** Uncertainty captured via `1,000`-resample `GroupID` `95% CI`; two-stage/transformer/OBB baselines deferred to future work.
4. **Non-Clinical Boundary:** Not a certified medical device; **zero predicted boxes NEVER exclude dental pathology**; independent clinician review is mandatory.
- *Speaker Cue (Anik, 50 s): State limitations proactively before the committee asks.*

---

## Slide 17 — Conclusions, Contributions & Future Work (Q&A Ready)
- **Four Bounded Contributions:**
  1. Leak-free `6`-cohort, `6`-country (`7,457` OPG / `41,103` box) benchmark with `G01–G14` cryptographic audit trail.
  2. Controlled proof that **`1280px` resolution (`+20.2%` rel. `mAP50:95`)** beats both **`CLAHE` (`3/3` failures)** and parameter doubling (`YOLO11m@640`).
  3. First `5`-country zero-shot granularity-aware shift matrix (`HC03` generalizes `0.70–0.82` vs `HC01–02` collapse `0.16–0.24`).
  4. `T19` error disentanglement + `R1–R3` verified sub-second CPU `ONNXRuntime` research prototype (`OPGPrototypeEngine`).
- **Next Research Steps:** Overlapping high-res tiling for `< 0.2%` pediatric caries, ordinal focal losses + inter-grade NMS for `PAI 3–5`, domain adaptation for radiolucencies, and prospective CBCT-verified clinical adjudication.
- **Thank You — Questions & Live Prototype Inspection Welcome!**
