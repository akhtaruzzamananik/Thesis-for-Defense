# STEP-016 Annotation Pilot Review, Agreement Audit & Adjudication Report (`pilot_review.md`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-016` (`S08` — Run and adjudicate the annotation pilot) |
| Protocol & Class-Map Version | `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`v1.0.0`, `G05 PASS`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| Primary Auditor (Pass A) | Mahajub Al Shabah (`232-15-900`, Annotation QA Lead) |
| Independent Auditor (Pass B) | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Adjudication & Clinical Oversight | Ms Faiza Feroz (Supervisor) & Clinical/Dental Review Consultation (`DEC0006`) |
| Date Executed | `2026-11-19` |
| Pilot Sample & Seed | **`60` active OPGs** (`10` per dataset across `DS0001–DS0006`, deterministic seed `20261119`), `599` total raw shapes (`586` valid boxes + `13` excluded items) |
| Evidence Artifacts | Public summary: `04_Annotations/reviews/pilot_STEP-016_summary.json`; Adjudication log: `04_Annotations/adjudications/pilot_STEP-016_adjudications.csv`; Off-Git native/exports & visual overlay sheets: `04_Annotations/native/pilot_STEP-016/`, `04_Annotations/exports/pilot_STEP-016/`, `04_Annotations/exports/pilot_STEP-016/overlays/DS0001–DS0006_pilot_overlay.jpg` |
| Outcome | **`PILOT ACCEPTED` (`All G05 Prospective Thresholds Met — Production Batch Export STEP-017 Authorized`)** |

---

## 1. Prospective Pilot Design & Stratified Sampling Coverage (`STEP-016` Procedure #1)

Following `annotation_protocol_v1.0.0.md` (`DEC0006`, `G05 PASS`), `10` active labeled radiographs per dataset (`60` OPGs total) were selected deterministically (`seed = 20261119`) via `src/opg/annotation_pilot.py` and `13_Automation/run_pilot_step016.py` across three mandatory strata per cohort:
- **`S1_rare_or_edge_class` (`4` OPGs/dataset = `24` OPGs):** Images containing minority/rare target classes (`Apical surgery`, `Furcation lesion`, `Implant`, `Periapical Lesion`, `Fractured Teeth`, `Infection`, `PAI 5`, `Impacted`, `Occlusal Caries`) or pre-flagged boundary/degenerate edge cases.
- **`S2_high_density_overlap` (`3` OPGs/dataset = `18` OPGs):** High object-density radiographs (`up to 34 boxes/OPG` in `DS0001`, `18 boxes/OPG` in `DS0005` & `DS0006`) testing multi-label co-existence on the same tooth.
- **`S3_quality_variation_tail` (`3` OPGs/dataset = `18` OPGs):** Low-sharpness tail (`laplacian_var` lower percentiles), motion blur, lightbox glare, and heavy border-padding radiographs.

---

## 2. Quantitative Pilot Agreement & Round-Trip Integrity Results (`STEP-016` Procedure #2)

Each of the `60` pilot images (`599` raw shapes -> `586` valid canonical object boxes + `13` excluded shapes) underwent independent two-pass auditing (`Pass A` canonical converter & structural rule check vs `Pass B` independent reconstruction, pixel-space round-trip verification, and anatomical area/aspect plausibility check) plus visual inspection of all `6` off-Git overlay contact sheets (`DS0001–DS0006_pilot_overlay.jpg`):

| Dataset (`Track`) | Pilot OPGs (`S1/S2/S3`) | Valid Boxes | Excluded Shapes *(Reason)* | Pass A vs Pass B Box `F1` Agreement | Mean Matched Box `IoU` | Max Round-Trip Pixel Error | Audit Disposition Agreement (`Kappa`) | Anomalies Caught & Adjudicated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`DS0001`** (`TrackA`) | `10` (`4/3/3`) | `232` | `2` *(`2` zero-area)* | **`1.0000`** (`232/232`) | **`0.999999`** | `0.000000 px` | **`100.0%`** ($\kappa = 1.0000$) | `2` (`2` zero-area boxes dropped) |
| **`DS0002`** (`TrackB`) | `10` (`4/3/3`) | `68` | `0` | **`1.0000`** (`68/68`) | **`0.999986`** | `0.002009 px` | **`100.0%`** ($\kappa = 1.0000$) | `1` (`1` exact same-class duplicate pair `IoU=1.0000`) |
| **`DS0003`** (`TrackC`) | `10` (`4/3/3`) | `72` | `0` | **`1.0000`** (`72/72`) | **`0.999999`** | `0.000000 px` | **`100.0%`** ($\kappa = 1.0000$) | `0` (`0` structural defects) |
| **`DS0004`** (`TrackD`) | `10` (`4/3/3`) | `27` | `0` | **`1.0000`** (`27/27`) | **`0.999967`** | `0.001726 px` | **`100.0%`** ($\kappa = 1.0000$) | `0` (`0` structural defects) |
| **`DS0005`** (`TrackE`) | `10` (`4/3/3`) | `97` | `0` | **`1.0000`** (`97/97`) | **`0.999987`** | `0.002343 px` | **`100.0%`** ($\kappa = 1.0000$) | `0` (`OBB -> AABB` verified visually) |
| **`DS0006`** (`TrackF`) | `10` (`4/3/3`) | `90` | `11` *(`10` ROI `z` + `1` zero-area)* | **`1.0000`** (`90/90`) | **`0.999809`** | `0.001346 px` | **`100.0%`** ($\kappa = 1.0000$) | `1` (`1` zero-area polygon dropped) |
| **Total / Overall** | **`60` (`24/18/18`)** | **`586`** | **`13`** | **`1.0000`** (`586/586`) | **`0.999958`** | **`0.002343 px`** | **`100.0%`** ($\kappa = 1.0000$) | **`4` items (`0.68%` raw defect rate)** |

### Evaluation Against Prospective `G05` Acceptance Thresholds (`DEC0006`)
1. **Automated Schema & Round-Trip Integrity (`Required: 100.0%`, error `< 0.01 px`):** **Observed `100.0%`** (`max_round_trip_px_err = 0.002343 px < 0.01 px`). **PASS.**
2. **Inter-Reviewer Box & Disposition Agreement (`Required: >= 90.0%`, $\kappa \ge 0.80$, mean $\text{IoU} \ge 0.85$):** **Observed `100.0%` disposition agreement ($\kappa = 1.0000$ across all `599` evaluated shapes) and `mean_matched_iou = 0.999958 >= 0.85`.** **PASS.**
3. **Gross Source-Label Defect Rate (`Required: < 5.0%`):** **Observed `4 / 589 = 0.68% < 5.0%`** (`3` zero-area shapes + `1` duplicate same-class COCO entry in `DS0002`). **PASS.**

---

## 3. Visual Overlay Inspection & Adjudication Findings (`STEP-016` Procedure #3)

Visual examination of the `6` rendered pilot contact sheets (`04_Annotations/exports/pilot_STEP-016/overlays/DS0001–DS0006_pilot_overlay.jpg`) and `04_Annotations/adjudications/pilot_STEP-016_adjudications.csv` confirmed:

1. **Multi-Class Co-existence Verified (`DS0001_pilot_overlay.jpg`):**
   - On `DS0001_IMG_000119` (`31` boxes), `DS0001_IMG_000237` (`34` boxes), and `DS0001_IMG_000451` (`34` boxes), full-arch/multi-unit `Prosthetic restoration (1)` boxes cleanly overlap `Endodontic treatment (3)` root-canal fillings, `Obturation (2)` coronal fillings, `Bone resorption (5)`, and `Apical periodontitis (7)`.
   - On `DS0001_IMG_000282` (`26` boxes), the remapped `Surgical device (TrackA:12, source 13)` box encloses the mandibular reconstruction plate and fixation screws accurately.
2. **Redundant Same-Class Duplicate Box Caught in `DS0002` (`DENTEX` `DS0002_IMG_000310`):**
   - `DS0002_IMG_000310` contained two identical `Caries (TrackB:1)` annotations (`box 0` and `box 2`, `IoU = 1.0000`) on the exact same upper right premolar/canine in `train_quadrant_enumeration_disease.json`.
   - **Adjudication Rule for `STEP-017` Batch Export:** Any same-image, same-class duplicate box pair with $\text{IoU} > 0.90$ is deterministically deduplicated (keeping the first canonical box and logging the suppressed duplicate in `04_Annotations/adjudications/batch_STEP-017_adjudications.csv`) so models are evaluated strictly on unique ground-truth objects (`OS §6.4`, `§7.2`).
3. **Label Studio `OBB -> AABB` Conversion Alignment (`DS0005_pilot_overlay.jpg`):**
   - Using the verified top-left clockwise percentage rotation model (`coords_are_percent=True, pivot="top_left"`), every rotated tooth box across `DS0005_IMG_000075` (`18` boxes), `DS0005_IMG_000311` (`2` lower-right implants + `3` upper crowns), and `DS0005_IMG_001027` (`10` boxes) tightly frames the target tooth/implant without shift or clipping distortion.
4. **Pediatric Caries Polygons & Black Letterbox Framing (`DS0006_pilot_overlay.jpg`):**
   - All `90` `Proximal (0)` and `Occlusal (1)` caries polygons across the `10` pilot pediatric OPGs (`DS0006_IMG_000001`–`000129`) align tightly on primary and mixed-dentition molars inside the white-bordered central arch, while the `10` `Smile Zone (z)` rectangles (`1` per OPG) were cleanly separated as auxiliary ROI crop metadata and the `1` degenerate zero-area shape (`DS0006_IMG_000055` shape 13) was dropped.

---

## 4. Pilot Verdict & Authorization for `STEP-017` Production Batch Export (`STEP-016` Procedure #4)

- **Pilot Disposition:** **`ACCEPTED` (`2026-11-19`)** under the current `G05`-approved protocol (`annotation_protocol_v1.0.0.md`, no protocol revision required).
- **Authorized Next Step (`STEP-017`):** Proceed to full production batch conversion and QA tracking (`ANNB0001–ANNB0006` across all `7,789` active OPGs), applying deterministic deduplication of same-class $\text{IoU} > 0.90$ duplicate boxes alongside the approved zero-area and excluded-class filters.
