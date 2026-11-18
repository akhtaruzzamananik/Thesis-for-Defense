# T09 — Canonical Dental OPG Annotation Protocol, Coordinate Schema & QA Governance (`annotation_protocol_v1.0.0.md`)

| Metadata | Value |
|---|---|
| TemplateID | T09 |
| template_version | v1.0.0 |
| entity_id | `PROTOCOL-v1.0.0` (`04_Annotations/protocols/annotation_protocol_v1.0.0.md`) |
| owner | Mahajub Al Shabah (`232-15-900`, Annotation QA Lead) & Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **Approved & Frozen (`v1.0.0`, `G05 PASS`, `2026-11-19`)** |
| source_inputs | `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`); `04_Annotations/protocols/class_definitions.md`; `src/opg/annotation_schema.py`; `tests/test_annotation_schema.py`; `DEC0004.md`; `DEC0005.md`; `DEC0006.md` |
| governing_section | OS §6.1–6.4, §13.2, §14.2; Blueprint STEP-015 |
| sensitivity | Public methodological protocol (contains zero patient images or PHI) |
| reviewer | Ms Faiza Feroz (Supervisor), Clinical/Dental Review Team, Mahajub Al Shabah & Akhtaruzzaman Anik |

---

## Class table

- **Canonical Registry:** `04_Annotations/classes.csv` (`Version v1.0.0`, normalized `SHA-256: c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`), containing **`41` immutable class records (`CLS0001–CLS0041`)** detailed in `04_Annotations/protocols/class_definitions.md`:
  1. **Track A (`DS0001 UMFIH`, `13` active classes `TrackA:0..12`):** `CLS0001` (`Implant`, `0`), `CLS0002` (`Prosthetic restoration`, `1`), `CLS0003` (`Obturation`, `2`), `CLS0004` (`Endodontic treatment`, `3`), `CLS0005` (`Carious lesion`, `4`), `CLS0006` (`Bone resorption`, `5`), `CLS0007` (`Impacted tooth`, `6`), `CLS0008` (`Apical periodontitis`, `7`), `CLS0009` (`Root fragment`, `8`), `CLS0010` (`Furcation lesion`, `9`), `CLS0011` (`Apical surgery`, `10`), `CLS0013` (`Orthodontic device`, `11`, remapped from source `12`), `CLS0014` (`Surgical device`, `12`, remapped from source `13`). **`CLS0012` (`source 11 Root resorption`, `N = 5` train boxes, `0` val/test/external)** is formally **excluded (`Excluded-Approved-G05`)** under `DEC0004`.
  2. **Track B (`DS0002 DENTEX`, `4` active classes `TrackB:0..3`):** `CLS0015` (`Impacted`, `0`), `CLS0016` (`Caries`, `1`), `CLS0017` (`Periapical Lesion`, `2`), `CLS0018` (`Deep Caries`, `3`), plus auxiliary pooled `Any Caries (1+3)` evaluation.
  3. **Track C (`DS0003 Rahman Dhaka`, `6` whole-tooth classes `TrackC:0..5`):** `CLS0019` (`Caries`, `0`), `CLS0020` (`Infection`, `1`), `CLS0021` (`Impacted Teeth`, `2`), `CLS0022` (`Fractured Teeth`, `3`), `CLS0023` (`BDC/BDR`, `4`), `CLS0024` (`Healthy Teeth`, `5`). Supports both `5-class pathology (0..4)` and `6-class (0..5)` evaluation modes (`DEC0004`).
  4. **Track D (`DS0004 Do 2024 Hanoi`, `3` periapical severity classes `TrackD:0..2`):** `CLS0025` (`PAI 3`, `0`), `CLS0026` (`PAI 4`, `1`), `CLS0027` (`PAI 5`, `2`), plus pooled `1-class Periapical Lesion (PAI 3–5)` evaluation.
  5. **Track E (`DS0005 AU-OPG`, `6` adult tooth classes `TrackE:0..5`):** `CLS0028` (`Filled`, `0`), `CLS0029` (`Crowned`, `1`), `CLS0030` (`Retained Root`, `2`), `CLS0031` (`Cavitated`, `3`), `CLS0032` (`Implant`, `4`), `CLS0033` (`Impacted`, `5`).
  6. **Track F (`DS0006 MD-OPG`, `2` pediatric caries classes `TrackF:0..1`):** `CLS0034` (`Proximal Caries p`, `0`), `CLS0035` (`Occlusal Caries o`, `1`). **`CLS0036` (`Smile Zone z`, `N = 170`)** is excluded from object detection classes (`Excluded-Auxiliary-ROI-G05`) and retained solely as optional ROI crop coordinate metadata (`UD09`).
  7. **Cross-Cohort Evaluation Bridges (`CLS0037–CLS0041` = `HC01–HC05`, `EvalBridge:0..4`):** `HC01` (`Caries`), `HC02` (`Periapical Lesion`), `HC03` (`Impacted Tooth`), `HC04` (`Residual Root / BDC-BDR`), `HC05` (`Dental Implant`).

---

## reference image

1. **Authoritative Coordinate Reference Frame (`OS §6.2 #1`):**
   - For all `6` datasets (`DS0001–DS0006`), the authoritative coordinate system is the **unmodified active raw image** (`width = W`, `height = H` in pixels) registered by `SHA-256` in `03_Datasets/manifests/DS0001_images.csv`–`DS0006_images.csv`, with origin `(0.0, 0.0)` at the **top-left pixel corner**, $x \in [0, W]$ increasing rightwards, and $y \in [0, H]$ increasing downwards.
   - Any fixed viewing enhancement (e.g., contrast windowing during human QA inspection) does not alter image dimensions or pixel coordinates. Any geometric preprocessing transform applied later in `STEP-019`–`021` (such as `DS0006` black-border autocrop or aspect-preserving letterbox resize) must record its exact forward and inverse affine coordinate mapping (`OS §4.3`).

---

## geometry/schema

### 1. Native Source Representations (`Preserved Untouched in 03_Datasets/raw/ & 04_Annotations/native/`)
- **`DS0001` (`UMFIH`) & `DS0003` (`Rahman Dhaka`):** Normalized YOLO `.txt` (`source_class_id xc yc w h` in `[0, 1]`).
- **`DS0002` (`DENTEX`):** Hierarchical COCO JSON (`train_quadrant_enumeration_disease.json`) with pixel `[x_min, y_min, width, height]` and `category_id_3` (`0..3`).
- **`DS0004` (`Do 2024 Hanoi`):** Pascal VOC `.xml` (`<bndbox><xmin>, <ymin>, <xmax>, <ymax></bndbox>`) in pixel coordinates with `<name>` in `{"3", "4", "5", "PAI 3", "PAI 4", "PAI 5"}`.
- **`DS0005` (`AU-OPG`):** Label Studio `.csv` (`train/val/test_annotations.csv`) with percentage coordinates `x, y, width, height` $\in [0, 100]$, clockwise `rotation` (degrees) pivoted at top-left `(px, py)` where $px = \frac{x}{100}W, py = \frac{y}{100}H$, and class column `condition`.
- **`DS0006` (`MD-OPG`):** LabelMe `.json` (`P_###_Ann_.json`) with `shapes[].points = [[x_1, y_1], \dots, [x_k, y_k]]` in pixel coordinates and `label` $\in \{\text{"p"}, \text{"o"}, \text{"z"}\}$.

### 2. Canonical Training & Evaluation Export Format (`UD05` / `DEC0005`)
- Every active image `ImageID` exports to a single canonical axis-aligned bounding-box (`AABB`) text file (`04_Annotations/exports/<TrackID>/<ImageID>.txt`) paired with a structured JSON/CSV manifest row containing:
  $$\texttt{<TrackIndex> <x\_center> <y\_center> <width> <height>}$$
  formatted to **6 decimal places** in normalized `[0.000000, 1.000000]` coordinates:
  $$x_c = \frac{x_{\min} + x_{\max}}{2W}, \quad y_c = \frac{y_{\min} + y_{\max}}{2H}, \quad w = \frac{x_{\max} - x_{\min}}{W}, \quad h = \frac{y_{\max} - y_{\min}}{H}$$
- **Edge & Clipping Rules:**
  - Coordinates exceeding `[0, W] × [0, H]` by minor annotator overhang ($\le 5\text{ px}$ observed in `STEP-013`) are clipped deterministically to `[0.0, W]` and `[0.0, H]` via `clip_xyxy` in `src/opg/annotation_schema.py`.
  - **Degenerate / Zero-Area Filter (`is_degenerate_box`):** Any shape with non-finite coordinates, clipped width $\le 10^{-3}\text{ px}$, clipped height $\le 10^{-3}\text{ px}$, or pixel area $\le 1.0\text{ px}^2$ (`2` `Bone resorbtion` + `1` `Surgical device` boxes in `DS0001`; `1` polygon in `DS0006`) is deterministically dropped and logged in `04_Annotations/annotation_registry.csv`.

### 3. Verified Round-Trip Conversion Evidence (`STEP-015` Procedure #4)
Implemented in `src/opg/annotation_schema.py` and verified via `tests/test_annotation_schema.py` across actual samples from all `6` datasets (`2026-11-19`):
- **`DS0001` (`UMFIH` `2652×1536`):** `verify_yolo_round_trip` max pixel error = **`0.000000 px`**
- **`DS0002` (`DENTEX` `2872×1316`):** `COCO -> xyxy -> YOLO (6-dec) -> xyxy` max pixel error = **`0.001904 px`**
- **`DS0003` (`Rahman Dhaka` `1176×601`):** `verify_yolo_round_trip` max pixel error = **`0.000000 px`**
- **`DS0004` (`Do Hanoi` `2444×1292`):** `VOC XML -> xyxy -> YOLO (6-dec) -> xyxy` max pixel error = **`0.000260 px`**
- **`DS0005` (`AU-OPG` `3292×1500`):** `Label Studio OBB -> tight AABB -> YOLO (6-dec) -> xyxy` max pixel error = **`0.000367 px`**
- **`DS0006` (`MD-OPG` `1920×1535`):** `LabelMe Polygon -> tight AABB -> YOLO (6-dec) -> xyxy` max pixel error = **`0.001030 px`**
- All round-trip errors are **$< 0.002\text{ px}$** (nearly 3 orders of magnitude below 1 pixel).

---

## visibility and negative rules

To satisfy `OS §6.1` and `§6.2 #3–5`, every image and region is assigned an explicit annotation state:

| State Code | Definition | Downstream Pipeline & Evaluator Treatment (`OS §6.2`, `§7.1`) |
|---|---|---|
| **`reviewed_positive`** | Active image reviewed under the track protocol with $\ge 1$ valid in-scope target boxes. | Exported with `.txt` lines; included in training/evaluation denominators. |
| **`reviewed_empty` (True Negative)** | Active image reviewed under the track protocol where `0` objects of an in-scope class (or `0` objects across all in-scope track classes) are present. | Exported as an **empty `.txt` file (`0` bytes)** and explicitly logged in image-level evaluation coverage (`OS §7.1`) so false positives on empty images are counted! |
| **`missing_labels` (Unannotated)** | Image acquired without ground-truth annotations (`DS0002` `50` challenge-val PNGs; `DS0003_IMG_001202`; `DS0005` `134` extra JPGs). | **Quarantined from supervised training and ground-truth metric denominators**; never treated as `reviewed_empty` background! |
| **`unassessed_class_region`** | Anatomical structures outside a dataset's annotation scope (e.g., sound teeth in `DS0001/0002/0004/0005/0006`, non-periapical structures in `DS0004`, or unboxed normal teeth beyond the `~2.8` sample boxes/OPG in `DS0003`). | Governed by track isolation (`Tracks A–F`); in `DS0003` (`Track C`), `5-class pathology (0..4)` evaluation ignores `Class 5 (Healthy Teeth)` so unboxed normal teeth are not penalized. |
| **`uncertain` / `needs_adjudication`** | Borderline radiographic feature flagged during pilot/batch visual QA (`STEP-016`–`018`). | Queued in `04_Annotations/adjudications/` for reviewer resolution; never silently auto-converted into a new trainable class. |
| **`excluded_degenerate`** | Source annotation with zero area (`4` shapes across `DS0001`/`DS0006`), excluded class (`CLS0012 Root resorption N=5`), or auxiliary ROI (`CLS0036 Smile Zone z`). | Filtered deterministically during canonical export with full count reconciliation in `04_Annotations/annotation_registry.csv`. |

---

## overlap

1. **Multi-Class Co-existence on the Same Tooth (`OS §6.2 #2`):**
   - Co-occurring annotations of **different classes** on the same tooth (e.g., `Crown/Obturation` + `Endodontic treatment` + `Apical periodontitis` in `DS0001`, or `Deep Caries` + `Periapical Lesion` in `DS0002`) are retained as distinct valid ground-truth boxes.
   - All model evaluation and inference (`STEP-024`–`035`, `UD13`) **must use class-aware NMS** and **class-aware one-to-one greedy IoU matching** (`match_boxes_greedy(..., class_aware=True)`), ensuring predictions of different classes on the same tooth never suppress or invalidate one another.
2. **Same-Class Duplicate Suppression Audit:**
   - Within the same image and same class, any two source boxes with $\text{IoU} > 0.90$ are flagged as redundant duplicate annotations during `STEP-016`–`018` integrity checks for adjudication/deduplication.

---

## ambiguity

1. **Truncated, Obscured, or Artifact-Overlapped Targets (`OS §6.2 #3`):**
   - Targets partially overlapped by spinal ghost shadows, hyoid superimposition, orthodontic wires, or sensor streaks (`DS0002_IMG_000641`) remain valid if $\ge 50\%$ of the anatomical/lesion contour remains radiographically discernible; completely obscured regions are marked `uncertain` / excluded from modifications.
2. **Moderate vs Deep Caries (`DS0002` `CLS0016` vs `CLS0018`) & `PAI 3–5` (`DS0004` `CLS0025–0027`):**
   - Original specialist consensus labels from `DENTEX` (`P0014`) and Hanoi Medical University endodontists (`P0008`) are preserved without post-hoc relabeling, while also reporting pooled `HC01 (Any Caries)` and `HC02 (Any Periapical PAI 3–5)` metrics to quantify boundary ambiguity cleanly.

---

## examples

- Permitted source locators (all patient pixel data remains strictly off-Git in `03_Datasets/raw/` and `03_Datasets/raw/qc_samples/DS0001–DS0006_qc_sheet.jpg`):
  - **Positive multi-label overlap:** `DS0001` `internal_train` adult OPGs showing co-localized `Prosthetic restoration (1)` + `Endodontic treatment (3)` + `Apical periodontitis (7)`.
  - **Negative / artifacts:** `DS0002_IMG_000641` (sensor streak band on left ramus); `DS0003_IMG_001156` (lightbox moiré + corner clinic stamp); `DS0006` `OPG_Image` (pediatric mixed dentition with unerupted permanent tooth buds below primary molars, which must **not** be misclassified as pathological adult impactions).

---

## tool/export

- **Converter & Validator Package:** `src/opg/annotation_schema.py` (`v1.0.0`, pinned to Python `3.14.6` environment `environment/data/requirements.lock.txt`), tested by `tests/test_annotation_schema.py`.
- **Prohibition on Unapproved External Upload (`OS §6.2 #7`):** Zero radiographic images may be uploaded to public/third-party web annotation platforms (e.g., public Roboflow workspaces). All inspection and overlay rendering runs locally off-Git on `Local PC` + `Private Google Drive` (`DEC0011`).

---

## qualifications

Per `team_roles.md` (`v1.0.0`) and `DEC0006` (`UD06`):
- **Annotation QA Lead (`Primary Auditor`):** **Mahajub Al Shabah** (`232-15-900`) — leads stratified pilot/batch visual overlay inspection and discrepancy logging across the `6` secondary expert-annotated datasets.
- **Data Steward & Co-Auditor (`Independent Second Reviewer`):** **Akhtaruzzaman Anik** (`232-15-252`) — runs independent pilot double-review, schema/geometry verification, and hash custody.
- **Clinical / Methodological Adjudication & Sign-Off (`Adjudicator`):** **Supervisor (`Ms Faiza Feroz`) + Clinical/Dental Review Consultation** — adjudicates clinical labelability/ambiguity items (`UD04–UD06`) and signs off `G05` / `G06`. Because `DS0001–DS0006` are peer-reviewed specialist-annotated datasets (`16–32` yr dentists in `DS0003`, endodontists in `DS0004`, oral radiologists in `DS0001/0002/0005`, pedodontists in `DS0006`), teammates **never overwrite clinical diagnoses**; our QA audits structural fidelity, conversion accuracy, and visual alignment, quarantining defective source items rather than inventing amateur clinical relabels (`OS §6.4`).

---

## pilot/QA sampling and thresholds

Prospective acceptance criteria locked **before** running `STEP-016`–`018` (`UD06` / `DEC0006`):

1. **Pilot QA Sample (`STEP-016`):**
   - **Sample Size & Stratification:** **`60` active OPGs (`10` per dataset across `DS0001–DS0006`)**, selected deterministically (fixed seed `20261119`) stratified across: (a) high-object-count images, (b) minority/rare classes (`Apical surgery`, `Furcation lesion`, `Periapical Lesion`, `Fractured Teeth`, `PAI 5`, `Occlusal Caries`), and (c) low-sharpness / boundary-clipped edge cases.
   - **Independent Double-Audit Procedure:** `Mahajub Al Shabah` (Reviewer 1) and `Akhtaruzzaman Anik` (Reviewer 2) independently audit every box on the `60` pilot overlay sheets for: (i) structural/conversion alignment, (ii) class-map plausibility against `class_definitions.md`, (iii) missed gross targets or spurious background boxes, and (iv) same-class duplicate overlaps ($\text{IoU} > 0.90$).
   - **Prospective Pilot Acceptance Thresholds (`G05` Lock):**
     - **Automated Schema & Round-Trip Integrity:** **`100.0%`** (`0` malformed lines, `0` out-of-bounds boxes $> 1\text{ px}$ after clipping, `0` unremoved zero-area boxes, round-trip error $< 0.01\text{ px}$).
     - **Inter-Reviewer Box/Class Audit Agreement (`F1_agreement` / Cohen's $\kappa$ on audit dispositions):** **$\ge 90.0\%$** agreement ($\kappa \ge 0.80$) between Reviewer 1 and Reviewer 2, and **mean matched box $\text{IoU} \ge 0.85$** (and $\ge 0.99$ for deterministic format conversion).
     - **Gross Source-Label Defect Rate:** **$< 5.0\%$** of audited boxes flagged as grossly misaligned or clinically implausible; any cohort exceeding $5.0\%$ triggers targeted batch quarantine/adjudication.
2. **Production Batch QA & Release Audit (`STEP-017`–`018` / `G06`):**
   - **Batch Structure (`ANNB0001–ANNB0006`):** One controlled production batch per dataset (`7,789` total active OPGs -> `7,738` labeled OPGs + `51` quarantined unannotated files).
   - **100% Automated Structural & Geometry Gate:** Every one of the `44,251` raw annotations across all `6` batches is checked for image-label correspondence, permitted class IDs, finite positive areas, in-bounds `[0, 1]` geometry, same-class duplicate boxes ($\text{IoU} > 0.90$), and exact count reconciliation.
   - **Stratified Visual QA Sample (`240` OPGs total = `40` per dataset, or $\ge 5\%$ of smaller cohorts `DS0003`/`DS0006`):** Audited against the same $\ge 95\%$ conversion/overlay validity and $< 5\%$ unresolved defect threshold before freezing `ANN0001–ANN0006` (`G06 PASS`).

---

## adjudication

1. Disagreements or suspicious source boxes identified during `STEP-016` (pilot) or `STEP-017` (production batches) are logged with `ImageID`, `ClassID`, box coordinates, and issue type (`degenerate_zero_area`, `same_class_duplicate_iou_gt_0.90`, `boundary_overhang`, `unlabeled_file`, or `ambiguous_pathology`) in `04_Annotations/adjudications/`.
2. **Resolution Policy (`OS §6.4`):**
   - Deterministic technical defects (`4` zero-area boxes, `5` excluded `CLS0012` boxes, `170` `CLS0036` ROI frames, minor boundary overhangs $\le 5\text{ px}$, and `51` unlabeled files) are resolved by preapproved rule and logged with full provenance.
   - Any clinically ambiguous box is adjudicated conservatively (flagged in metadata or quarantined if corrupt) — **never silently altered or fabricated**.

---

## version

- **Protocol Version:** `v1.0.0` (`2026-11-19`)
- **Linked Class-Map Version & Hash:** `04_Annotations/classes.csv` `v1.0.0` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`)
- **Change Control:** Any future modification to class definitions, index mappings, coordinate conventions, or QA thresholds requires a new semantic version (`v1.1.0` / `v2.0.0`) and reassessment of `G05` and `G06`.
