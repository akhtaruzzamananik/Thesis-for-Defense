# Final-Test Evaluation Freeze & Validation-Only Model Selection (`STEP-031` / `G11`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-031` (`S12` — Select on validation and freeze final-test evaluation) |
| Gate | **`G11`** (`GA0011` — [G11_assessment_2026-11-21.md](../01_Project_Management/reviews/G11_assessment_2026-11-21.md)) |
| Freeze Version | `v1.0.0` |
| Freeze Date | `2026-11-21` (`+06:00`) |
| Freeze Source Commit | `d47dae64e50b1f77213daf463777e078abbc45af` (`STEP-030` `13/13` `G10 PASS`) |
| Machine-Readable Manifest | [freeze_manifest.json](./freeze_manifest.json) |
| Owners / Reviewers | Mahajub Al Shabah (`232-15-900`, Model & Eval Lead), Akhtaruzzaman Anik (`232-15-252`, Research Lead), Ms Faiza Feroz (`Supervisor`) |
| Governing Sections | `OS §5`, `§7.1–7.4`, `§13.2`; Blueprint `STEP-031`; `DEC0012–DEC0016` |

> [!IMPORTANT]
> **Strict Test-Custody Guarantee:** This freeze record and its companion [freeze_manifest.json](./freeze_manifest.json) are finalized and committed to Git **strictly prior to** any held-out `test` or `external_test` inference (`STEP-032`). Across `EXP0000_SMOKE` and all `13` controlled experiments (`EXP0001–EXP0013`), **zero (`0`) `test` or `external_test` images were exposed** to training, validation, checkpoint selection, or threshold tuning.

---

## 1. Predeclared Validation-Only Selection Rule (`DEC0012` / `experiment_plan.md`)

All `13` controlled experiments (`EXP0001–EXP0013`, yielding `MODEL0001–MODEL0013` and `CKPT0003–CKPT0028`) passed **`G10`** on `2026-11-21` ([STEP030_matrix_tracker.md](../07_Experiments/STEP030_matrix_tracker.md)). Per the predeclared selection rule established before training (`DEC0012`, `07_Experiments/experiment_plan.md`):

1. **Primary Selection Criterion (Validation Only):** Highest **`val mAP@0.50`** on each track's canonical validation partition (`SPLIT0001–SPLIT0006`).
2. **Predeclared Tie-Breaker (Validation Only):** Highest **`val mAP@0.50:0.95`**, followed by lower parameter/artifact footprint for deployment efficiency (`RQ3`).
3. **Held-Out Comparator Retention (Predeclared `RQ1`/`RQ3` Design — NOT Post-Hoc Re-Selection):**
   - Alongside the `6` per-track validation winners (`TrackA–TrackF`), `4` predeclared reference comparators (`MODEL0001` `YOLO11s@640`, `MODEL0002` `YOLOv8s@640`, `MODEL0003` `YOLO11m@640` on `TrackA`, and `MODEL0010` `YOLO11s@640` on `TrackD`) are frozen **exclusively** to answer `RQ1` (cross-generation architecture & model-scale held-out comparison) and `RQ3` (resolution/scale latency-vs-accuracy Pareto frontier).
   - **Primary winner claims are locked to the `6` validation winners below and CANNOT be swapped after `STEP-032` test metrics are observed.**
4. **Excluded Candidates (`RQ2` Negative Evidence):**
   - All `3` `CLAHE` ablations (`EXP0008`/`MODEL0011` `PP0002` `val mAP@0.50 = 0.344`, `EXP0009`/`MODEL0012` `PP0003` `val mAP@0.50 = 0.363`, `EXP0012`/`MODEL0009` `PP0002` `val mAP@0.50 = 0.232`) strictly degraded validation `mAP@0.50` and `mAP@0.50:0.95` relative to matched raw controls (`EXP0001` `0.381`, `EXP0004` `0.259`) across `3/3` tests and are **excluded** from sealed test inference (reported honestly in `RQ2` validation ablation tables).

---

## 2. Complete Validation Comparison & Frozen Model Selection (`13` `G10 PASS` Candidates)

### 2.1 Track-by-Track Selection & Validation-Only Operating Thresholds (`conf_op`)

Every operating confidence threshold `conf_op` below was extracted **strictly from the validation partition's `BoxF1_curve.png`** (macro-averaged `F1` peak across all active classes, per `09_Evaluation/protocol.md §1` & `DEC0013`) before any `test` access:

| Track / Cohort | Role | `EXP ID` | `ModelID` | `CKPT` | Arch / `PP` (`imgsz`) | Best Ep | `val mAP@0.50` | `val mAP@0.50:95` | `val` Peak Macro-`F1` | **Frozen `conf_op`** *(val-only)* | Final-Test Disposition |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| **`TrackA`** (`REL0001`, Romania, `13` cls) | **Primary Winner** | `EXP0010` | **`MODEL0005`** | `CKPT0011` | `YOLO11s` / `PP0004` (`1280`) | `25` | **`0.391`** *(0.3906)* | **`0.1656`** | `0.43` | **`0.227`** | **FROZEN WINNER** (`test` + `external_test` + `HC01–05`) |
| `TrackA` (`REL0001`, Romania, `13` cls) | `RQ1`/`RQ3` Ref (`640`) | `EXP0001` | `MODEL0001` | `CKPT0003` | `YOLO11s` / `PP0001` (`640`) | `65` | `0.381` *(0.3792)* | `0.1570` | `0.44` | **`0.238`** | **FROZEN COMPARATOR** (`test` + `external_test` + timing) |
| `TrackA` (`REL0001`, Romania, `13` cls) | `RQ1`/`RQ3` Ref (`v8s`) | `EXP0002` | `MODEL0002` | `CKPT0005` | `YOLOv8s` / `PP0001` (`640`) | `17` | `0.364` *(0.3637)* | `0.1523` | `0.41` | **`0.197`** | **FROZEN COMPARATOR** (`test` + `external_test` + timing) |
| `TrackA` (`REL0001`, Romania, `13` cls) | `RQ1`/`RQ3` Ref (`11m`) | `EXP0013` | `MODEL0003` | `CKPT0007` | `YOLO11m` / `PP0001` (`640`) | `42` | `0.391` *(0.3906)* | `0.1583` | `0.44` | **`0.253`** | **FROZEN COMPARATOR** (`test` + `external_test` + timing) |
| `TrackA` (`REL0001`, Romania, `13` cls) | `RQ2` CLAHE 2.0 | `EXP0008` | `MODEL0011` | `CKPT0023` | `YOLO11s` / `PP0002` (`640`) | `31` | `0.344` | `0.1479` | — | *N/A* | **EXCLUDED** (`-0.037` vs `EXP0001`) |
| `TrackA` (`REL0001`, Romania, `13` cls) | `RQ2` CLAHE 3.0 | `EXP0009` | `MODEL0012` | `CKPT0025` | `YOLO11s` / `PP0003` (`640`) | `30` | `0.363` | `0.1472` | — | *N/A* | **EXCLUDED** (`-0.018` vs `EXP0001`) |
| **`TrackB`** (`REL0002`, DENTEX, `4` cls, NC-SA) | **Track Winner** | `EXP0003` | **`MODEL0004`** | `CKPT0009` | `YOLO11s` / `PP0001` (`640`) | `32` | **`0.444`** *(peak `0.459`)* | **`0.2913`** | `0.45` | **`0.210`** | **FROZEN WINNER** (`REL0002 test`, license-isolated) |
| **`TrackC`** (`REL0003`, Dhaka, `6` cls) | **Track Winner** | `EXP0004` | **`MODEL0006`** | `CKPT0013` | `YOLO11s` / `PP0001` (`640`) | `34` | **`0.259`** *(0.2588)* | **`0.1506`** | `0.28` | **`0.075`** | **FROZEN WINNER** (`REL0003 test`, dual `5-cls`/`6-cls`) |
| `TrackC` (`REL0003`, Dhaka, `6` cls) | `RQ2` CLAHE 2.0 | `EXP0012` | `MODEL0009` | `CKPT0019` | `YOLO11s` / `PP0002` (`640`) | `6` | `0.232` | `0.1315` | — | *N/A* | **EXCLUDED** (`-0.027` vs `EXP0004`) |
| **`TrackD`** (`REL0004`, Hanoi PAI, `3` cls) | **Track Winner** | `EXP0011` | **`MODEL0013`** | `CKPT0027` | `YOLO11s` / `PP0004` (`1280`) | `24` | **`0.536`** *(peak `0.542`)* | **`0.2514`** | `0.55` | **`0.201`** | **FROZEN WINNER** (`REL0004 test` + `HC02` shift) |
| `TrackD` (`REL0004`, Hanoi PAI, `3` cls) | `RQ2`/`RQ3` Ref (`640`) | `EXP0005` | `MODEL0010` | `CKPT0021` | `YOLO11s` / `PP0001` (`640`) | `25` | `0.488` *(0.4878)* | `0.2117` | `0.51` | **`0.205`** | **FROZEN COMPARATOR** (`REL0004 test` + timing) |
| **`TrackE`** (`REL0005`, UAE, `6` cls) | **Track Winner** | `EXP0006` | **`MODEL0008`** | `CKPT0017` | `YOLO11s` / `PP0001` (`640`) | `88` | **`0.858`** *(peak `0.860`)* | **`0.5705`** | `0.83` | **`0.379`** | **FROZEN WINNER** (`REL0005 test` + `HC03/04/05`) |
| **`TrackF`** (`REL0006`, Pediatric, `2` cls) | **Track Winner** | `EXP0007` | **`MODEL0007`** | `CKPT0015` | `YOLO11s` / `PP0001` (`640`) | `36` | **`0.100`** *(0.0991)* | **`0.0300`** | `0.19` | **`0.091`** | **FROZEN WINNER** (`REL0006 test`, low-N baseline) |

### 2.2 Key Validation Tradeoff & Tie-Break Rationale

1. **`TrackA` Tie-Break (`MODEL0005` `YOLO11s@1280` vs `MODEL0003` `YOLO11m@640`):** Both achieved identical primary `val mAP@0.50 = 0.391` (`0.3906`). Under the predeclared tie-breaker, **`MODEL0005` strictly wins `val mAP@0.50:0.95` (`0.1656` vs `0.1583`, `+4.6%` relative)** while using less than half the weights (`19.34 MB` vs `40.54 MB`) and demonstrating superior localization on fine structures (`Orthodontic_Device +12.4%`, `Furcation_Lesion +3.0%`, `Carious_Lesion +2.5%` vs `EXP0001`).
2. **`TrackD` Decisive High-Resolution Gain (`MODEL0013` `YOLO11s@1280` vs `MODEL0010` `YOLO11s@640`):** `MODEL0013` outperformed `MODEL0010` by **`+0.048` `val mAP@0.50`** (`0.536` vs `0.488`), **`+0.0397` `val mAP@0.50:0.95`** (`+18.8%` relative), and **`+0.081` Recall** (`0.5747` vs `0.4934`), decisively confirming `RQ2` that small apical radiolucencies benefit from input resolution preservation (`1280px`) rather than `CLAHE` histogram warping.
3. **`TrackE` (`MODEL0008`) Showcase Role:** `MODEL0008` (`val mAP@0.50 = 0.858`, `mAP@0.50:0.95 = 0.5705`, `Implant AP = 0.995`, `Crowned = 0.928`, `Filled = 0.881`) is the strongest overall cohort model and is paired with `MODEL0005` (`TrackA` `13`-class) as the primary `ONNX`-exported showcase candidate for `S13`/`S16` (subject to held-out verification in `STEP-032`).
4. **Operating Point vs AP Curve Separation (`OS §7.2` / `DEC0013`):**
   - **AP / mAP & PR Curve Computation:** Uses **`metric_conf_floor = 0.001`** (`nms_iou = 0.65`, `agnostic_nms = false`, `max_det = 300`, `matching_iou = 0.50` & `[0.50:0.05:0.95]`).
   - **Operating-Point `Precision`, `Recall`, `F1`, Confusion & Error Analysis (`T19`):** Uses each model's **frozen validation-only `conf_op`** listed in §2.1 above (never re-tuned on `test`), alongside the protocol fallback reference `conf = 0.25` logged as a secondary fixed comparison column.

---

## 3. Immutable Frozen Artifact & Configuration Hashes

Any `STEP-032` evaluation script MUST verify every hash below before running inference and **abort immediately** on any mismatch:

### 3.1 Core Governance, Ontology & Evaluator Code Hashes

| Artifact | Path | `SHA-256` |
|---|---|---|
| Freeze Source Commit | `git rev-parse HEAD` | `d47dae64e50b1f77213daf463777e078abbc45af` |
| Canonical Class Ontology (`CLS0001–0041`) | `04_Annotations/classes.csv` | `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af` |
| Evaluation & Timing Protocol (`v1.0.0`) | `09_Evaluation/protocol.md` | `26fede09e31475e7e7a5a1cdd3bc2a111815f727d8925300976dc6060a9024c1` |
| Experiment Plan (`v1.0.0`) | `07_Experiments/experiment_plan.md` | `24d26143125afce1fa8bf5c55e8d7cbeb393466d4355bf98933cf7e3e87a086a` |
| Preprocessing `PP0001` (`640×640` Raw) | `05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml` | `04493e1e2bcdfcadbef5b044b392bf7091822439381e158d85c144d420e0b93b` |
| Preprocessing `PP0004` (`1280×1280` Raw) | `05_Preprocessing/configs/PP0004_highres_letterbox_1280.yaml` | `08fd22b42f9fa31465eedc092251d92d7b5338b76de4fc7d321a7c77741dd2de` |
| Deterministic Evaluator Module | `src/opg/evaluator.py` | `8fa2c6d8254f095307d9d081701f7ab5e6494a8a415f7942f7daa9bf0f87a149` |
| Preprocessing / `TransformLedger` Module | `src/opg/preprocessing.py` | `011e67c02c56a1518af45c46627ec6db300330cb5ad233a4a37ca843e8bfac39` |

### 3.2 Frozen Dataset Releases (`REL0001–REL0006`) & Sealed Test Denominators

| Release | Dataset / Track | Canonical `test` OPGs (Boxes) | `external_test` OPGs (Boxes) | `SPLIT` Manifest `SHA-256` (Git) | `release_manifest.json` `SHA-256` | `transform_ledger` `SHA-256` |
|---|---|---:|---:|---|---|---|
| `REL0001` | `DS0001` (`TrackA`, Romania) | **`208`** (`2,888`) | **`178`** (`2,925`) | `b7b40a1af8518644fc14a3a1aa4fa0569cb299f0ed2cc06533f534ff46e1e8ee` | `91c78db160479584070a603256e6607468beb376e5a188e846a98bf0c0414bd3` | `667982c0c0fe72e4cf544769f3703c17ab61b2f13e625aa7291bd9b1ec1a0926` |
| `REL0002` | `DS0002` (`TrackB`, DENTEX) | **`106`** (`530`) | `0` | `f660fa2a09197b3fdf9641e261499ec49effeacc596f6cc633de63997172e092` | `4a268c33bcd7d02ef99d87666337911ec240e210d1fbb80318960fec67f116fd` | `d9cc4678fc41148f13aa4703f8513c60366b0f01865ed340350bfc86e05c05a6` |
| `REL0003` | `DS0003` (`TrackC`, Dhaka) | **`33`** (`182`) | `0` | `7081e461819987c050cb34df5e4534e165dc68499fb7aba6c8dc80fc91fe1151` | `8d749c8ad42aae4288183d888c0d8a2f819d9ed4c9e5d90d99d64b4dcc6b9770` | `ed0a9e4a565204b2897870511eb8f5feb9ec37d4e37bcc0df4774f9c4f569f37` |
| `REL0004` | `DS0004` (`TrackD`, Hanoi PAI) | **`578`** (`999`) | `0` | `74aa4db7b70e72c2655b147b381492a0df5477a4820d4205074bd5cf047f49e0` | `a60e5092ca5bea1730415a25669eeb8e33a7afc25544c129ed20cff3137c6977` | `5384185db0349b3f2cc6e0bc18eb2c160ee8827b21bd5c0b1d5b3ef73fe92edb` |
| `REL0005` | `DS0005` (`TrackE`, UAE) | **`133`** (`1,048`) | `0` | `cb894f5bd138ada998687cfa80a756127db7e70bdc94b4b25335d3ce3dc6d504` | `1b3787527b52012b229168ab73774ef6300e41b9f2205a277e5efc9b3e8e4df5` | `de33c53ac21bec26c5f2ee8b3d1ce8a245a9b3a8ab2f5603b3cceb125681693f` |
| `REL0006` | `DS0006` (`TrackF`, Pediatric) | **`24`** (`137`) | `0` | `04aafcceeeb0215fb4c2d23106c9900bdf8fa892d007ac15cf01e54fdb7f0e5a` | `3f485fbd9425dc6e7d7dc222fbd8f43839527f91aebe7856f6fdd6bbe139fb9f` | `e3ceff8e52faeb2e8cb22839e8f808d14300807c5c73696d7b83d2549ec36ae8` |
| **Total** | **6 Independent Tracks** | **`1,082`** (`5,784`) | **`178`** (`2,925`) | — | — | — |

### 3.3 Frozen Checkpoints (`10` Models: `6` Track Winners + `4` `RQ1`/`RQ3` Comparators)

Every off-Git `best.pt` file below was re-verified on local disk against `08_Checkpoints/checkpoint_registry.csv` on `2026-11-21`:

| `ModelID` | `CKPT` | `EXP` | Role | Size (bytes) | `best.pt` `SHA-256` |
|---|---|---|---|---:|---|
| **`MODEL0005`** | `CKPT0011` | `EXP0010` | **TrackA Winner** | `19,342,746` | `6a845f99bd87b9dcc904386784002864cbdf2031f851902e1678e64c9003612a` |
| `MODEL0001` | `CKPT0003` | `EXP0001` | TrackA Ref (`640`) | `19,191,578` | `ce8e5b44bdce6bee76734dc0241918161874fccd30457c19ab555f5cd798eeef` |
| `MODEL0002` | `CKPT0005` | `EXP0002` | TrackA Ref (`YOLOv8s`) | `22,527,018` | `2f4b5b27f40e0fb8eaa627f910a5ee51c2712dc234828851cf21eb68fc4b82f3` |
| `MODEL0003` | `CKPT0007` | `EXP0013` | TrackA Ref (`YOLO11m`) | `40,535,276` | `a5a89aa41e0559316594d7f306354a5b8ee5d74104e13ea591c89761dccda743` |
| **`MODEL0004`** | `CKPT0009` | `EXP0003` | **TrackB Winner** | `19,180,122` | `33c6453dc59ddbe49ffebe13896a8b6c12ba7906c951655abf4b0768d967827c` |
| **`MODEL0006`** | `CKPT0013` | `EXP0004` | **TrackC Winner** | `19,181,978` | `966d9abcc60a7f27259cedd8882bcbbf5a2378e0847fbf7682115d41bfc4c674` |
| **`MODEL0013`** | `CKPT0027` | `EXP0011` | **TrackD Winner** | `19,334,554` | `ac6dadc9123a58db475ddf0c1d96de5c8f2d9bf2e8a61e98f1b17b478ba9a14e` |
| `MODEL0010` | `CKPT0021` | `EXP0005` | TrackD Ref (`640`) | `19,178,394` | `305d279c747ef016d1225dbe264fef5bdb14e360dbc240cad3ea670b6fa6e272` |
| **`MODEL0008`** | `CKPT0017` | `EXP0006` | **TrackE Winner** | `19,187,866` | `0336a078eb8b0037f2a40ca5a203f444a2e5ead7186ea321997ab3140c5e495b` |
| **`MODEL0007`** | `CKPT0015` | `EXP0007` | **TrackF Winner** | `19,179,034` | `c725343e35bc5af8122461e109ed6d968f62854a227be9b5100fcc9e7599af92` |

---

## 4. Frozen Final-Test, External-Shift & Timing Evaluation Plan (`STEP-032`–`STEP-035`)

### 4.1 In-Domain Held-Out `test` & `external_test` Evaluations (`14` Runs: `EVAL0001–EVAL0014`)

| `EvalID` | Model | Target Release & Partition | `imgsz` / `PP` | Frozen `conf_op` | Purpose |
|---|---|---|---|---:|---|
| `EVAL0001` | **`MODEL0005`** (`TrackA` Winner) | `REL0001` `test` (`208` OPGs) | `1280` / `PP0004` | `0.227` | Primary TrackA held-out test (`RQ0–RQ3`) |
| `EVAL0002` | **`MODEL0005`** (`TrackA` Winner) | `REL0001` `external_test` (`178` OPGs) | `1280` / `PP0004` | `0.227` | Primary TrackA external-hospital test (`RQ1`) |
| `EVAL0003` | `MODEL0001` (`TrackA` `640` Ref) | `REL0001` `test` (`208` OPGs) | `640` / `PP0001` | `0.238` | `RQ1`/`RQ2`/`RQ3` `640px` control |
| `EVAL0004` | `MODEL0001` (`TrackA` `640` Ref) | `REL0001` `external_test` (`178` OPGs) | `640` / `PP0001` | `0.238` | External shift `640px` control |
| `EVAL0005` | `MODEL0002` (`YOLOv8s` Ref) | `REL0001` `test` (`208` OPGs) | `640` / `PP0001` | `0.197` | `RQ1`/`RQ3` cross-gen comparator |
| `EVAL0006` | `MODEL0002` (`YOLOv8s` Ref) | `REL0001` `external_test` (`178` OPGs) | `640` / `PP0001` | `0.197` | External shift `YOLOv8s` comparator |
| `EVAL0007` | `MODEL0003` (`YOLO11m` Ref) | `REL0001` `test` (`208` OPGs) | `640` / `PP0001` | `0.253` | `RQ1`/`RQ3` scale comparator |
| `EVAL0008` | `MODEL0003` (`YOLO11m` Ref) | `REL0001` `external_test` (`178` OPGs) | `640` / `PP0001` | `0.253` | External shift `YOLO11m` comparator |
| `EVAL0009` | **`MODEL0004`** (`TrackB` Winner) | `REL0002` `test` (`106` OPGs) | `640` / `PP0001` | `0.210` | TrackB DENTEX held-out test (CC-BY-NC-SA isolated) |
| `EVAL0010` | **`MODEL0006`** (`TrackC` Winner) | `REL0003` `test` (`33` OPGs) | `640` / `PP0001` | `0.075` | TrackC Dhaka held-out test (`5-cls` + `6-cls` dual) |
| `EVAL0011` | **`MODEL0013`** (`TrackD` Winner) | `REL0004` `test` (`578` OPGs) | `1280` / `PP0004` | `0.201` | TrackD Hanoi PAI `1280px` held-out test (`RQ0–RQ3`) |
| `EVAL0012` | `MODEL0010` (`TrackD` `640` Ref) | `REL0004` `test` (`578` OPGs) | `640` / `PP0001` | `0.205` | TrackD `640px` control for `RQ2`/`RQ3` |
| `EVAL0013` | **`MODEL0008`** (`TrackE` Winner) | `REL0005` `test` (`133` OPGs) | `640` / `PP0001` | `0.379` | TrackE UAE held-out test (`RQ0–RQ3`, showcase candidate) |
| `EVAL0014` | **`MODEL0007`** (`TrackF` Winner) | `REL0006` `test` (`24` OPGs) | `640` / `PP0001` | `0.091` | TrackF Pediatric held-out test (small-N empirical limit) |

### 4.2 Zero-Shot Cross-Country Harmonized Shift Bridges (`HC01–HC05`, `UD15` / `RQ1`)

Strictly honoring box-granularity compatibility (`04_Annotations/classes.csv` rows `CLS0037–CLS0041`):

| Bridge | Clinical Target & Granularity | Source Model -> Target `test` Set | Class Mapping (Source -> Target) |
|---|---|---|---|
| `XSHIFT01` (`HC03/04/05`) | Impacted Tooth (`HC03`), Retained Root (`HC04`), Implant (`HC05`) | `MODEL0005` (`TrackA` Romania) -> `REL0005` `test` (UAE, `133` OPGs) | `TrackA:6->TrackE:5`, `TrackA:8->TrackE:2`, `TrackA:0->TrackE:4` |
| `XSHIFT02` (`HC03/04/05`) | Impacted Tooth (`HC03`), Retained Root (`HC04`), Implant (`HC05`) | `MODEL0008` (`TrackE` UAE) -> `REL0001` `test` (`208`) + `external_test` (`178`) | `TrackE:5->TrackA:6`, `TrackE:2->TrackA:8`, `TrackE:4->TrackA:0` |
| `XSHIFT03` (`HC03/04`) | Impacted Tooth (`HC03`), Retained Root/BDC (`HC04`) | `MODEL0005` (`TrackA` Romania) & `MODEL0008` (UAE) -> `REL0003` `test` (Dhaka, `33` OPGs) | `Impacted->TrackC:2`, `Root->TrackC:4` |
| `XSHIFT04` (`HC03`) | Impacted Tooth (`HC03`, whole-tooth) | `MODEL0005` (`TrackA`) & `MODEL0008` (`TrackE`) -> `REL0002` `test` (DENTEX Türkiye, `106` OPGs) | `Impacted->TrackB:0` |
| `XSHIFT05` (`HC02`) | Focal Periapical Radiolucency (`HC02`, focal apical AABB) | `MODEL0005` (`TrackA:7`) -> `REL0004` `test` (`PAI 3/4/5` pooled); `MODEL0013` (`PAI 3/4/5` pooled) -> `REL0001` `test` + `external_test` (`TrackA:7`) | Bidirectional Romania <-> Vietnam focal periapical shift |
| `XSHIFT06` (`HC01`) | Whole-Tooth Caries (`HC01`, tooth-level) | `MODEL0008` (`TrackE:3` Cavitated) -> `REL0002` `test` (`TrackB:1+3`) & `REL0003` `test` (`TrackC:0`) | Whole-tooth caries shift (never mixed with focal boxes) |

### 4.3 Frozen Statistical Uncertainty, Timing & ONNX Export Policy (`DEC0014–DEC0015`)

- **Uncertainty (`STEP-033`):** `1,000`-resample **GroupID cluster bootstrap** (`seed = 20261131`) yielding `95% CI` for `mAP@0.50`, `mAP@0.50:0.95`, `Precision`, `Recall`, and `F1`, respecting intra-OPG / duplicate-cluster correlation (`P0031`).
- **GPU Timing (`STEP-032` on Kaggle `Tesla T4`):** Serial `batch_size = 1` (`FP32` standard + optional `FP16` separately labeled), `10` warm-up OPGs discarded + `100` consecutive OPGs timed (or full `test` if `< 100`), explicit `torch.cuda.synchronize()`, logging `T_pre`, `T_h2d`, `T_infer`, `T_post`, `T_e2e`, `FPS_infer`, and `FPS_e2e` (`mean ± sd`, `median`, `IQR`, `p95`).
- **ONNX Export & Local CPU Timing (`STEP-032`/`STEP-034`):** Export `MODEL0005`, `MODEL0001`, `MODEL0002`, `MODEL0003`, `MODEL0013`, `MODEL0010`, `MODEL0008` to static `ONNX` (`opset = 17`, `simplify = False/True` recorded) on Kaggle during `STEP-032`, verify `SHA-256` & output parity vs PyTorch (`max_abs_diff` logged), and benchmark local Windows 11 CPU `ONNXRuntime` latency (`batch_size = 1`, `10` warmup + `100` timed OPGs) for `RQ3` & `S16` deployment planning.
- **Failure & Zero-Detection Policy:** Every image in each target partition MUST appear in the coverage ledger (`coverage = 100.0%`). Zero-detection OPGs are recorded explicitly (`n_pred = 0`, never omitted). Any inference exception aborts the run and logs an explicit failure record.

---

## 5. Prior Test-Access Custody Audit (`OS §5` / `STEP-031`)

| Audit Check | Verification Result | Evidence |
|---|---|---|
| `EXP0000_SMOKE` & `EXP0001–EXP0013` `config.yaml` `allowed_partitions` | **PASS (`14/14` `["train", "val"]` only)** | Automated scan of `07_Experiments/EXP*/config.yaml` (`has_test_in_allowed = false` for all `13` experiments) |
| Kaggle training bundle exporter (`export_kaggle_bundle.py`) | **PASS (`allow_test_partition = False`)** | Every training `.zip` bundle omitted `test` and `external_test` completely |
| Kaggle training script (`kaggle_train_exp.py`) | **PASS (`"test" not in raw_data_yaml` assertion)** | Runtime assertion passed on all `13/13` Kaggle runs |
| Preprocessing train-only fit (`REL0001–REL0006`) | **PASS (`val_or_test_used_for_fit = false`)** | `05_Preprocessing/processed/REL0001–0006/release_manifest.json` |
| Prior `09_Evaluation/evaluation_registry.csv` rows | **PASS (`0` prior test rows)** | Header-only at `2026-11-21T01:38+06:00` |
| Freeze commit precedes `STEP-032` prediction timestamp | **PASS (enforced by Git history)** | This commit timestamp strictly precedes any `EVAL0001–EVAL0014` generation |
