# Systematic Qualitative & Quantitative Error Review (`STEP-036` / `T19` / `G13`)

| Metadata | Value |
|---|---|
| TemplateID | `T19` (`v1.0.0`) |
| entity_id | `ERRREV0001` (`EVAL0001`, `EVAL0002`, `EVAL0009`, `EVAL0010`, `EVAL0011`, `EVAL0013`, `EVAL0014`) |
| owner | Mahajub Al Shabah (`232-15-900`, Evaluation Lead) & Akhtaruzzaman Anik (`232-15-252`, Research Lead) |
| date | `2026-11-21` |
| status | Complete (`STEP-036` / `G13 PASS`, read-only on frozen `FREEZE0001` outputs) |
| source_inputs | `09_Evaluation/step036_error_taxonomy.json`; `08_Checkpoints/artifacts/STEP032_outputs/evals/EVAL####/predictions.jsonl`; off-Git `error_review_sheets/EVAL####_review_sheet.jpg` |
| governing_section | `OS §6`, `§7.5`, `§9`, `§13.2`; Blueprint `STEP-036` |
| sensitivity | Aggregate taxonomy & ImageIDs public; raw visual radiograph sheets strictly **off-Git** (`08_Checkpoints/artifacts/STEP032_outputs/error_review_sheets/`) |
| reviewer | Akhtaruzzaman Anik & Mahajub Al Shabah (pending supervisor/dental reviewer sign-off for manuscript figure selection in `S14`) |

> [!IMPORTANT]
> **Strict Non-Contamination Policy (`STEP-036`):** Every error count and reviewed example below is strictly **read-only** over frozen `STEP-032` predictions at each model's validation-locked `conf_op`. **Zero ground-truth labels were modified and zero thresholds or weights were re-tuned after observing test errors.**

---

## 1. Selection Method (Deterministic, Non-Cherry-Picked `OS §7.5`)

1. **Exhaustive Quantitative Decomposition:** Every single held-out ground-truth box (`6,718` GT boxes) and every prediction at `conf >= conf_op` across all `7` primary winner evaluations (`1,260` canonical held-out OPGs: `1,082 test` + `178 external_test`) was programmatically decomposed into mutually exclusive FP (`FP_Bkg`, `FP_Loc`, `FP_Cls`, `FP_Dup`) and FN (`FN_Complete_Miss`, `FN_Missed_By_Score`, `FN_Loc_Only`, `FN_Confused_Cls`) error categories plus normalized area size buckets (`Small < 0.2%`, `Medium 0.2–1.0%`, `Large >= 1.0%` of radiograph area) in [analyze_step036_errors.py](../13_Automation/analyze_step036_errors.py).
2. **Prospective 4-Category Visual Sampling (`28` Cases Total — `4` per Primary Eval):** Without manual cherry-picking, `4` disjoint cases per primary winner evaluation were selected deterministically:
   - **`Top_Success`:** Maximum `TP - (FP + FN)`
   - **`Worst_Complete_Miss`:** Maximum `FN_Complete_Miss`
   - **`Worst_Background_Mimic_FP`:** Maximum `FP_Bkg`
   - **`Worst_Class_or_Loc_Error`:** Maximum `FP_Cls + FP_Loc`
3. **Direct Visual Verification:** `2×2` overlay sheets (green = GT, red = prediction at `conf_op`) were generated strictly off-Git (`08_Checkpoints/artifacts/STEP032_outputs/error_review_sheets/EVAL####_review_sheet.jpg`) and directly inspected to separate **genuine detector failures** from **reference-label uncertainty/incompleteness** and **2D OPG radiographic physics artifacts**.

---

## 2. Exhaustive Error Taxonomy & Size-Bucket Recall Across All `7` Primary Winner Evaluations

### 2.1 False Positive (`FP`) & False Negative (`FN`) Decomposition at Frozen `conf_op`

| `EvalID` (`Model`, `Track:Part`) | `conf_op` | `FP` Total | `FP_Bkg` *(Mimic/Unannot.)* | `FP_Loc` *(0.1–0.5 IoU)* | `FP_Cls` *(Wrong Cls)* | `FP_Dup` *(Duplicate)* | `FN` Total | `FN_Miss` *(No Pred)* | `FN_Score` *(< conf_op)* | `FN_Loc` *(Loose Box)* | `FN_Cls` *(Confused)* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `EVAL0001` (`MODEL0005`, `TrackA:test`) | `0.227` | `1,077` | `447` (`41.5%`) | `281` (`26.1%`) | `260` (`24.1%`) | `89` (`8.3%`) | `1,420` | `343` (`24.2%`) | `484` (`34.1%`) | `322` (`22.7%`) | `271` (`19.1%`) |
| `EVAL0002` (`MODEL0005`, `TrackA:ext`) | `0.227` | `832` | `347` (`41.7%`) | `219` (`26.3%`) | `182` (`21.9%`) | `84` (`10.1%`) | `1,458` | `387` (`26.5%`) | `606` (`41.6%`) | `215` (`14.7%`) | `250` (`17.1%`) |
| `EVAL0009` (`MODEL0004`, `TrackB:test`) | `0.210` | `403` | `264` (`65.5%`) | `53` (`13.2%`) | `85` (`21.1%`) | `1` (`0.2%`) | `243` | `38` (`15.6%`) | `87` (`35.8%`) | `50` (`20.6%`) | `68` (`28.0%`) |
| `EVAL0010` (`MODEL0006`, `TrackC:test`) | `0.075` | `183` | `127` (`69.4%`) | `21` (`11.5%`) | `35` (`19.1%`) | `0` (`0.0%`) | `109` | `29` (`26.6%`) | `46` (`42.2%`) | `14` (`12.8%`) | `20` (`18.3%`) |
| `EVAL0011` (`MODEL0013`, `TrackD:test`) | `0.201` | `497` | `247` (`49.7%`) | `22` (`4.4%`) | **`218` (`43.9%`)** | `10` (`2.0%`) | `423` | `68` (`16.1%`) | **`210` (`49.6%`)** | `25` (`5.9%`) | `120` (`28.4%`) |
| `EVAL0013` (`MODEL0008`, `TrackE:test`) | `0.379` | `145` | `44` (`30.3%`) | `14` (`9.7%`) | **`80` (`55.2%`)** | `7` (`4.8%`) | `185` | `34` (`18.4%`) | `43` (`23.2%`) | `34` (`18.4%`) | `74` (`40.0%`) |
| `EVAL0014` (`MODEL0007`, `TrackF:test`) | `0.091` | `82` | `41` (`50.0%`) | `27` (`32.9%`) | `11` (`13.4%`) | `3` (`3.7%`) | `120` | **`69` (`57.5%`)** | `12` (`10.0%`) | `29` (`24.2%`) | `10` (`8.3%`) |

- **Reviewed-Empty Image Audit (`OS §7.2`):** In `EVAL0009` (`TrackB` DENTEX), `4` held-out test OPGs were `reviewed_empty` (`GT = 0`); `3/4` triggered `11` total `FP_Bkg` predictions at `conf_op = 0.210` (all retained in denominators). All other held-out test partitions contained `>= 1` annotated finding per OPG.

### 2.2 Object-Size Bucket Recall (`Small < 0.2%`, `Medium 0.2–1.0%`, `Large >= 1.0%` OPG Area)

| `EvalID` (`Track`) | `Small (< 0.2%)` Recall (`TP / GT`) | `Medium (0.2–1.0%)` Recall (`TP / GT`) | `Large (>= 1.0%)` Recall (`TP / GT`) | Observed Size-Scale Pattern |
|---|---:|---:|---:|---|
| `EVAL0001` (`TrackA:test`, `1280px`) | **`0.3090`** (`428 / 1,385`) | **`0.6636`** (`795 / 1,198`) | **`0.8033`** (`245 / 305`) | Monotonic `2.6×` recall drop from large to small focal targets |
| `EVAL0002` (`TrackA:ext`, `1280px`) | **`0.3087`** (`417 / 1,351`) | **`0.6523`** (`925 / 1,418`) | **`0.8013`** (`125 / 156`) | Identical `Small -> Large` recall profile on unseen external hospital |
| `EVAL0009` (`TrackB:test`, `640px`) | *N/A* (`0`) | `0.4805` (`74 / 154`) | `0.5665` (`213 / 376`) | Whole-tooth boxes eliminate `< 0.2%` small bucket |
| `EVAL0010` (`TrackC:test`, `640px`) | *N/A* (`0`) | `0.3667` (`11 / 30`) | `0.4079` (`62 / 152`) | Low contrast on handheld film limits even large whole-tooth boxes |
| `EVAL0011` (`TrackD:test`, `1280px`) | **`0.6111`** (`462 / 756`) | `0.4726` (`112 / 237`) | `0.3333` (`2 / 6`) | `1280px` preserves small `PAI 3` apices (`61.1%` recall); larger `PAI 4/5` suffer ordinal class swaps |
| `EVAL0013` (`TrackE:test`, `640px`) | `0.0000` (`0 / 1`) | **`0.8482`** (`447 / 527`) | **`0.8000`** (`416 / 520`) | Consistently `>= 80%` recall across whole-tooth targets |
| `EVAL0014` (`TrackF:test`, `640px`) | **`0.1241`** (`17 / 137`) | *N/A* (`0`) | *N/A* (`0`) | **`100%` of pediatric caries boxes are `< 0.2%` area**, exposing the `640px` physical ceiling |

---

## 3. Dominant Cross-Class Confusion Pairs & Visual Case Inspection (`T19` Core Fields)

### 3.1 Top Observed Cross-Class Confusions (Directly from `step036_error_taxonomy.json`)

| Track (`EvalID`) | Top Confusion Pairs (`GT -> Pred`, count) | Observed Quality / Semantic Overlap | Label Issue vs Model Failure |
|---|---|---|---|
| `TrackA` (`EVAL0001`/`0002`) | `Obturation -> Prosthetic` (`48` int / `19` ext), `Prosthetic -> Obturation` (`33` int / `23` ext), `Carious_Lesion -> Obturation` (`18` ext), `Obturation -> Carious_Lesion` (`14` int / `11` ext) | Dense coronal restorations vs crowns overlap visually on 2D OPG; secondary caries abuts fillings directly. | **Mixed:** Both visual similarity (model failure) and coronal restoration extent ambiguity (partial-coverage onlays vs full crowns). |
| `TrackB` (`EVAL0009`) | **`Deep_Caries -> Caries` (`44`)**, `Impacted -> Caries` (`14`), `Caries -> Deep_Caries` (`12`), `Periapical -> Caries` (`7`) | Ordinal pulp-proximity boundary between moderate `Caries` and `Deep_Caries` is continuous on 2D projection. | **High Label Uncertainty:** `Deep_Caries <-> Caries` accounts for **`65.9%` (`56/85`)** of all `FP_Cls` on DENTEX. |
| `TrackC` (`EVAL0010`) | `Caries_Tooth -> Healthy_Tooth` (`10`), `Healthy_Tooth -> Caries_Tooth` (`8`), `BDC_BDR -> Caries` (`3`) | Handheld mobile photographs of film radiographs exhibit glare, moiré, and low contrast; plus selective `~3` healthy teeth annotated per OPG. | **Severe Source-Label Artifact:** `127/183` (`69.4%`) of FPs are `FP_Bkg` because unannotated healthy teeth across the arch are treated as background! |
| `TrackD` (`EVAL0011`) | **`PAI_4 -> PAI_3` (`87`)**, **`PAI_3 -> PAI_4` (`44`)**, **`PAI_5 -> PAI_4` (`33`)**, **`PAI_4 -> PAI_5` (`25`)** | Adjacent ordinal PAI grades (subtle mineral loss vs circumscribed vs exacerbating lesion) share the exact same root apex location. | **Dominant Ordinal Boundary Uncertainty:** Adjacent PAI swaps account for **`86.7%` (`189/218`)** of all `FP_Cls`; only `68/999` (`6.8%`) of lesions are completely missed! |
| `TrackE` (`EVAL0013`) | `Crowned -> Filled` (`19`), `Cavitated -> Filled` (`13`), **`Retained_Root <-> Cavitated` (`12 + 11 = 23`)** | Severely cavitated teeth losing `> 2/3` crown grade continuously into `Retained_Root`; dense crowns resemble large multi-surface fillings. | **Mixed:** Genuine semantic boundary overlap (`Retained_Root <-> Cavitated`) + minor model confusion on radiopaque restorative density. |
| `TrackF` (`EVAL0014`) | `Proximal_Caries <-> Occlusal_Caries` (`6 + 5 = 11`) | In pediatric mixed dentition, large molar caries span both occlusal and proximal surfaces; overlapping erupting tooth buds obscure contacts. | **Model Resolution Limit + Small-N:** `57.5%` (`69/120`) of FNs are complete misses due to `< 0.2%` lesion area + only `121` training OPGs. |

### 3.2 Direct Visual Inspection Findings on Sampled Held-Out Radiograph Sheets (`28` Cases Sampled)

| Sampled Case (`EvalID` / `ImageID`) | Category | Prediction / Reference | Observed Visual Quality & Error Pattern | Label Issue vs Model Cause (Qualified Hypothesis) |
|---|---|---|---|---|
| `EVAL0001` / `DS0001_IMG_000043` | `Top_Success` | `GT=37, TP=32, FP=2, FN=5` | Sharp high-contrast adult OPG; tight boxes across endodontic fills, bridges, obturations, and impacted third molars. | Demonstrates strong multi-object capability on high-contrast structures; `0` background hallucinations. |
| `EVAL0001` / `DS0001_IMG_000722` | `Worst_Background_Mimic_FP` | `GT=6, TP=1, FP_Bkg=27` | Visually crisp `PaX-i` OPG displaying **>15 obvious radiopaque root canal fillings, crowns, and bridges**; source GT only boxed `6` objects! | **Confirmed Source-Label Incompleteness (Not purely model hallucination):** Detector accurately localized visibly present endodontic/prosthetic hardware that was unannotated in UMFIH source ground truth. *(Preserved unaltered per `STEP-036` policy.)* |
| `EVAL0001` / `DS0001_IMG_000509` | `Worst_Complete_Miss` | `GT=27, TP=5, FN_Miss=14` | Lower-contrast OPG with numerous small vertical `Bone_Resorption` strips along mandibular incisors + cervical spine shadow on far-left edge falsely flagged as `Orthodontic: 0.55`. | **Model Failure + Diffuse Boundary Ambiguity:** Small low-contrast crestal bone-loss strips have weak edge gradients (`Small Recall = 30.9%`); vertebral ghost superimposition mimics metallic wire texture. |
| `EVAL0011` / `DS0004_IMG_015728` | `Top_Success` | `GT=4, TP=4, FP=0, FN=0` | Clean panoramic radiograph; all `4` focal `PAI_3` mandibular root-apex radiolucencies localized pixel-tightly (`conf 0.65–0.70`). | Confirms `1280px` high-resolution efficacy on focal small apical radiolucencies. |
| `EVAL0011` / `DS0004_IMG_015992` | `Worst_Background_Mimic_FP` | `GT=1, TP=1, FP_Bkg=4, FP_Dup=1` | Large anterior maxillary `PAI_5` lesion nailed (`0.78`), but class-aware NMS also retained nested `PAI_3: 0.22` inside it + `2` mandibular incisor apex `PAI_3` alerts over chin/mental ridge shadow. | **Anatomical Mimic + Ordinal Co-Firing:** Mental/symphyseal radiolucent overlap mimics periapical rarefaction; class-aware NMS allows adjacent PAI grades to stack at one apex. |
| `EVAL0011` / `DS0004_IMG_014169` | `Worst_Class_or_Loc_Error` | `GT=3, TP=1, FP_Cls=4, FN_Cls=2` | Maxillary left molar apices accurately localized, but detector assigned `PAI_3`/`PAI_4` simultaneously over GT `PAI_4`/`PAI_3`. | **Ordinal Grading Subjectivity:** Detection of lesion *presence* succeeded; error is strictly fine-grained `PAI 3 vs 4` severity grading. |
| `EVAL0013` / `DS0005_IMG_000961` | `Top_Success` | `GT=21, TP=19, FP=1, FN=2` | Clean adult OPG; near-perfect whole-tooth detection across `Filled`, `Crowned`, and `Cavitated` teeth (`conf 0.87–0.93`). | Confirms whole-tooth box granularity + consistent single-center scanner protocol yields `> 0.82` mAP@0.50. |
| `EVAL0013` / `DS0005_IMG_000367` | `Worst_Complete_Miss` | `GT=14, TP=4, FN_Miss=4, FN_Score=3` | Bright central **cervical spine ghost superimposition** washes out contrast across mandibular anterior teeth labeled `Cavitated`. | **2D OPG Physics Limitation:** Spine superimposition degrades anterior interproximal radiolucency visibility on 2D panoramic projection. |
| `EVAL0013` / `DS0005_IMG_000523` | `Worst_Class_or_Loc_Error` | `GT=11, TP=8, FP_Cls=6` | Severely destructed crowns receive overlapping `Retained_Root` and `Cavitated_Tooth` predictions (`0.73–0.90`). | **Semantic Boundary Overlap:** Continuous transition from extensive cavitation to crownless retained root causes dual-class firing. |

---

## 4. Example Permission & Privacy Disposition (`T19` Mandatory Field)

- **Off-Git Diagnostic Sheets:** All `7` `2×2` visual overlay sheets (`08_Checkpoints/artifacts/STEP032_outputs/error_review_sheets/EVAL####_review_sheet.jpg`) remain **strictly off-Git** in local/private artifact storage.
- **Manuscript/Defense Figure Permission:** Only de-identified examples from CC-BY-4.0 cohorts (`DS0001` UMFIH, `DS0003` Dhaka after EXIF/corner-logo sanitization, `DS0004` Do 2024, `DS0005` AU-OPG, `DS0006` MD-OPG) may be used as curated figures in `S14`/`S16` with proper source citation; `DS0002` (DENTEX, `CC-BY-NC-SA-4.0`) examples require explicit non-commercial share-alike attribution and remain isolated from any commercial artifact.
