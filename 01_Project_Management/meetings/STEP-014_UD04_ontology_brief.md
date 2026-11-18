# `STEP-014` Dental Object Ontology & `UD04–UD06` Approval Brief (For `STEP-015 / G05`)

**To:** Mahajub Al Shabah (Annotation Lead), Akhtaruzzaman Anik (Data Steward), Ms Faiza Feroz (Supervisor), and Dental Reviewer  
**Date prepared:** `2026-11-18`  
**Linked Artifacts:** `04_Annotations/classes.csv` (`CLS0001–CLS0041`), `04_Annotations/protocols/class_definitions.md`, `01_Project_Management/decision_log/DEC0004.md`

---

## 1. What Was Completed in `STEP-013` (`G04 PASS`) & `STEP-014`

1. **`G04 = PASS` Recorded (`2026-11-18`):**
   - Closed `DEC0002` (`UD02`) and `G04_assessment_2026-11-18.md` across all `6` open `2D OPG` datasets (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined, `0` cross-cohort overlaps).
   - Mathematically proved the exact `DS0003` (`Rahman 2024 Dhaka`) YOLO class index mapping (`0..5`) via SHA-256 bijection against `Dental OPG (Classification)/`:
     - `0 = Caries (194 boxes)`, `1 = Infection (37 boxes)`, `2 = Impacted Teeth (196 boxes)`, `3 = Fractured Teeth (14 boxes)`, `4 = BDC/BDR (97 boxes)`, `5 = Healthy Teeth (651 boxes)`.
2. **`STEP-014` Ontology Drafted (`04_Annotations/classes.csv` & `protocols/class_definitions.md`):**
   - Registered **`41` canonical class records (`CLS0001–CLS0041`)**:
     - **Track A (`DS0001 UMFIH`):** `13` active classes (`TrackA:0..12`) + **`CLS0012 Root resorption (N=5, 0 eval)` proposed excluded** (`3` zero-area boxes dropped).
     - **Track B (`DS0002 DENTEX`):** `4` active disease classes (`TrackB:0..3`: `Impacted, Caries, Periapical Lesion, Deep Caries`) + pooled `Any Caries` bridge.
     - **Track C (`DS0003 Dhaka`):** `6` whole-tooth classes (`TrackC:0..5`), supporting both **`5-class pathology-only (0..4)`** and **`6-class (0..5)`** modes so selectively boxed `Healthy Teeth` (`~2.8/OPG`) do not distort pathology false-positive rates.
     - **Track D (`DS0004 Hanoi`):** `3` focal apical severity classes (`TrackD:0..2`: `PAI 3, PAI 4, PAI 5`) + pooled `PAI 3–5` view.
     - **Track E (`DS0005 AU-OPG`):** `6` adult tooth classes (`TrackE:0..5`: `Filled, Crowned, Retained Root, Cavitated, Implant, Impacted`) with deterministic `OBB -> AABB` conversion.
     - **Track F (`DS0006 MD-OPG`):** `2` pediatric caries classes (`TrackF:0..1`: `Proximal Caries p, Occlusal Caries o`) converted from polygons to tight `AABB` (`1` zero-area polygon dropped; `CLS0036 Smile Zone z` excluded as auxiliary ROI metadata).
     - **Harmonized Cross-Cohort Bridges (`CLS0037–CLS0041` = `HC01–HC05`):** Granularity-matched bridges for `Caries`, `Periapical Lesion`, `Impacted Tooth`, `Residual Root/BDC`, and `Dental Implant`.

---

## 2. Decisions Needed to Execute `STEP-015` and Pass `G05` (`UD04–UD06`)

To proceed immediately to **`STEP-015`** (*Approve annotation format, protocol and QA thresholds* -> **`G05 PASS`**), please confirm:

1. **`UD04` Ontology Approval (`Q1–Q4` in `class_definitions.md §5`):**
   - Exclude `DS0001 Class 11 (Root resorption, N=5)` and `DS0006 Class z (Smile Zone ROI)` from object classes;
   - Keep `Tracks A–F` separated for training and use `HC01–HC05` bridges for cross-cohort evaluation;
   - Retain rare classes (`DS0001 Apical surgery N=91`, `DS0003 Fractured Teeth N=14`) with explicit low-support reporting caveats (`UD13`).
2. **`UD05` Coordinate & Export Contract (`STEP-015`):**
   - Adopt standard normalized YOLO axis-aligned bounding-box format (`class_id x_center y_center width height` in `[0, 1]`, 6-decimal precision) as the canonical training/evaluation export across `Tracks A–F`, preserving source native formats (`YOLO .txt`, `COCO .json`, `Pascal VOC .xml`, `OBB .csv`, `LabelMe .json`) untouched in restricted storage, and dropping the `4` zero-area annotations cleanly.
3. **`UD06` Secondary-Dataset Label Audit & Pilot/QA Thresholds (`STEP-015`–`STEP-018`):**
   - Because all `6` datasets already supply expert annotations (`UMFIH`, `DENTEX`, `Rahman Dhaka`, `Do Hanoi`, `AU-OPG`, `MD-OPG`), our `STEP-016`–`STEP-018` workflow is a **prospective stratified secondary-label QA & adjudication audit** (rather than drawing 44,251 boxes from scratch):
     - **Pilot QA (`STEP-016`):** Stratified sample of `60` OPGs (`10` per dataset across classes/quality tiers) independently audited by `Mahajub Al Shabah` (Annotation Lead) and cross-checked by `Akhtaruzzaman Anik` + Dental Reviewer/Supervisor (`target schema/conversion integrity = 100%`, `class/box audit agreement >= 90%`, `matched box IoU >= 0.70`).
     - **Production Batch QA & Release Freeze (`STEP-017`–`018` / `G06`):** Automated 100% geometry/correspondence audit across all `7,789` active OPGs (`ANNB0001–ANNB0006`) + stratified visual overlay audit (`240` OPGs = `40` per dataset) before freezing `ANN0001–ANN0006` (`G06 PASS`).
