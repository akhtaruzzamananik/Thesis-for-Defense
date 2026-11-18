# Dental Object Ontology, Granularity Rules & Cross-Cohort Harmonization Specification (`STEP-014`)

| Metadata | Value |
|---|---|
| TemplateID | T09 (`STEP-014` Ontology Specification; full QA/export protocol freezes at `STEP-015 / G05`) |
| template_version | v1.0.0 |
| entity_id | `ONTOLOGY-v0.1.0` (`04_Annotations/classes.csv` `CLS0001–CLS0041`) |
| owner | Mahajub Al Shabah (`232-15-900`, Annotation QA Lead) & Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-18 |
| status | **Draft Proposal Complete (`STEP-014` DoD met)** — Ready for Dental Reviewer & Supervisor `UD04–UD06` approval at `STEP-015` (`G05`) |
| source_inputs | `01_Project_Management/scope.md` (`v1.0.0`); `02_Literature/research_questions.md` (`v1.0.0`); `01_Project_Management/decision_log/DEC0002.md`; `DEC0003.md v6`; `03_Datasets/reports/DS0001_quality.md`–`DS0006_quality.md`; `04_Annotations/classes.csv` |
| governing_section | OS §1.3, §6.1–6.2, §7.2, §13.2; Blueprint STEP-014 |
| sensitivity | Public methodological specification (contains zero patient images or PHI) |
| reviewer | Qualified Dental Reviewer & Ms Faiza Feroz (Supervisor) — *`Unresolved / Human Decision Required` until `STEP-015 / G05`* |

---

## 1. Purpose & Clinical-to-Radiographic Boundary (`STEP-014` Procedure #1 & #3)

The deleted report's Figure 1 listed high-level candidate examples (*teeth, impacted tooth, cavities, lesions, restorations*) without specifying class counts, box granularity, overlap rules, or radiographic visibility limits (`OS §6.1`). Following `G04 PASS` (`2026-11-18`) across our **6 approved secondary `2D OPG` cohorts (`DS0001–DS0006`, `7,789` active OPGs, `44,251` total raw annotations)**, this specification converts those examples into an explicit, auditable ontology (`CLS0001–CLS0041` in `04_Annotations/classes.csv`).

### 1.1 Mandatory Separation of Radiographic Observations from Clinical Diagnoses (`OS §6.1`)
1. **Radiographic Appearance Only:** Every object class in `04_Annotations/classes.csv` denotes a **2D panoramic radiographic feature** (localized radiopacity, radiolucency, structural contour, or tooth position visible on a single 2D projection), **never** a definitive histological or chairside clinical diagnosis.
   - *Example 1 (`CLS0008 / CLS0017 / CLS0020 / CLS0025–0027` — Periapical Radiolucencies):* Labeled as *Apical Periodontitis / Periapical Lesion / PAI 3–5* based strictly on periapical bone rarefaction on OPG. Differentiating a radicular cyst from a periapical granuloma requires histopathology (`P0008`, `P0023`), and acute apical abscess vs chronic asymptomatic apical periodontitis requires clinical percussion/vitality testing.
   - *Example 2 (`CLS0005 / CLS0016 / CLS0018 / CLS0019 / CLS0031 / CLS0034–0035` — Caries):* Labeled as *Radiographic Carious Lesion / Cavitation*. Initial non-cavitated enamel white-spot lesions (`ICDAS 1–2`), buccal/lingual pit lesions masked by enamel superimposition (`P0003 TP=0`), and chairside tactile softness cannot be diagnosed from `2D OPG` (`P0032`).
   - *Example 3 (`CLS0006` — Bone Resorption):* Represents visible radiographic alveolar crest lowering relative to the cementoenamel junction (`CEJ`), not clinical periodontal pocket probing depth or active attachment loss (`GAP0003`).
2. **Prohibited / Out-of-Scope Concepts (`scope.md v1.0.0` & `research_questions.md §1`):**
   - Soft-tissue mucosal pathology (`P0006`);
   - Continuous millimeter root-length morphometry (`P0013`);
   - Merged `Caries + Restoration` labels (`P0016` `CAND0008` defect — strictly avoided here).

---

## 2. Track-Isolated Native Ontologies (`Tracks A–F`, `CLS0001–CLS0036`)

Per `DEC0002` and `DEC0003 v6` (`OS §6.2 #4`, `§7.2`), our `6` datasets use fundamentally different background and bounding-box conventions and **must never be blindly pooled into a single multi-class training matrix**. Each track has its own deterministic `TrainingIndex` map:

### 2.1 Track A — `DS0001` (`UMFIH` Romania + External Multi-Center, `13` Active Classes `TrackA:0..12`)
- **Source inventory (`24,891` raw boxes across `1,808` OPGs; `3` zero-area boxes dropped -> `24,888` valid boxes):**
  - Reconciled in `STEP-013` (`DS0001_quality.md §4`): both internal (`train/valid/test`) and `external_validation` (`180` OPGs) follow root `legend.txt` (`0–13`), **not** the corrupted `test_alte_cabinete/labels (1).txt`.
- **Proposed Exclusion of `Source Class 11` (`CLS0012 Root resorption`, `N = 5` boxes):**
  - `Root resorption` (`source id=11`) has **only `5` boxes in `internal_train` and `0` boxes in `internal_valid`, `internal_test`, and `external_validation`**.
  - Under `OS §4.4`, `§6.1`, and `§7.2`, a class with `5` total instances cannot support a leakage-safe `70/15/15` split (`< 1` expected validation/test instance) and causes undefined `AP` denominators on held-out and external sets.
  - **Rule (`UD04`):** Exclude `CLS0012` (`source id=11`) during canonical `STEP-015/018` export (logging all `5` source instances in `annotation_registry.csv`), and shift `Orthodontic device` (`source 12 -> TrackA:11`) and `Surgical device` (`source 13 -> TrackA:12`).

| `ClassID` | `TrackA` Index | Source ID & Name (`legend.txt`) | Total Boxes (`Int + Ext`) | Contrast Tier (`RQ1`) | Box Granularity | Status Proposal (`UD04`) |
|---|---:|---|---:|---|---|---|
| `CLS0001` | `0` | `0` Implant | `522` (`506 + 16`) | **Tier 1 (High-Contrast Radiopaque)** | Focal fixture `AABB` | **Retain (`Active`)** |
| `CLS0002` | `1` | `1` Prosthetic restoration | `1,890` (`1,684 + 206`) | **Tier 1 (High-Contrast Radiopaque)** | Crown / bridge span `AABB` | **Retain (`Active`)** |
| `CLS0003` | `2` | `2` Obturation | `5,262` (`4,365 + 897`) | **Tier 1 (High-Contrast Radiopaque)** | Focal intracoronal filling `AABB` | **Retain (`Active`)** |
| `CLS0004` | `3` | `3` Endodontic treatment | `3,692` (`3,164 + 528`) | **Tier 1 (High-Contrast Radiopaque)** | Root canal fill `AABB` | **Retain (`Active`)** |
| `CLS0005` | `4` | `4` Carious lesion | `3,589` (`3,293 + 296`) | **Tier 2 (Radiolucent Pathology)** | Focal carious defect `AABB` | **Retain (`Active`)** |
| `CLS0006` | `5` | `5` Bone resorbtion | `3,856` valid (`+2` zero-area dropped) | **Tier 2 (Periodontal / Diffuse)** | Alveolar crest defect `AABB` | **Retain (`Active`, diffuse boundary noted)** |
| `CLS0007` | `6` | `6` Impacted tooth | `1,088` (`977 + 111`) | **Tier 1 (Structural Tooth)** | Whole impacted tooth `AABB` | **Retain (`Active`)** |
| `CLS0008` | `7` | `7` Apical periodontitis | `1,259` (`1,153 + 106`) | **Tier 2 (Radiolucent Pathology)** | Focal periapical `AABB` | **Retain (`Active`)** |
| `CLS0009` | `8` | `8` Root fragment | `1,502` (`1,409 + 93`) | **Tier 1/2 (Structural Remnant)** | Whole root remnant `AABB` | **Retain (`Active`)** |
| `CLS0010` | `9` | `9` Furcation lesion | `328` (`309 + 19`) | **Tier 2 (Radiolucent Minority)** | Interradicular furcation `AABB` | **Retain (`Active`, minority support)** |
| `CLS0011` | `10` | `10` Apical surgery | `91` (`74 + 17`) | **Tier 2 (Ultra-Rare Procedure)** | Resected apex / retro-fill `AABB` | **Retain with Rare-Class Flag (`UD04/UD13`)** |
| `CLS0012` | `EXCLUDED` | `11` Root resorption | `5` (`5 + 0`) | Unsupportable (`N=5`) | N/A | **Exclude (`UD04` Proposal)** |
| `CLS0013` | `11` | `12` Orthodontic device | `533` (`527 + 6`) | **Tier 1 (High-Contrast Hardware)** | Appliance / archwire `AABB` | **Retain (`Active`)** |
| `CLS0014` | `12` | `13` Surgical device | `1,271` valid (`+1` zero-area dropped) | **Tier 1 (High-Contrast Hardware)** | Plate / screw assembly `AABB` | **Retain (`Active`)** |

---

### 2.2 Track B — `DS0002` (`DENTEX` MICCAI 2023 Türkiye, `4` Active Classes `TrackB:0..3`)
- **Source inventory (`3,529` disease boxes across `705` labeled training PNGs; `50` validation PNGs have `0` GT labels):**
  - Forensic JSON audit (`DS0002_quality.md §3`) proved a **`14:1` class imbalance** across `categories_3` (`Caries = 2,189`, `Impacted = 604`, `Deep Caries = 578`, `Periapical Lesion = 158`).
  - **Box convention:** Whole-tooth `AABB` (`[x, y, w, h]` in pixels) enclosing the affected tooth (with `quadrant` `categories_1` and `FDI tooth number` `categories_2` preserved in auxiliary metadata).
  - **Granularity & Ambiguity Note (`CLS0016 Caries` vs `CLS0018 Deep Caries`):** Both are retained as native classes (`TrackB:0..3`) for direct `DENTEX` benchmark comparability (`P0014`, `P0036`), while also supporting an auxiliary pooled `Any Caries (CLS0016 + CLS0018)` evaluation under `HC01` to diagnose inter-grade confusion between moderate and deep dentin caries.

---

### 2.3 Track C — `DS0003` (`Rahman 2024` Dhaka, Bangladesh, `6` Classes `TrackC:0..5`)
- **Source inventory (`1,189` boxes across `230` labeled original OPGs; `1` unlabeled original `DS0003_IMG_001202` quarantined):**
  - Exact class-ID mapping proven via `STEP-013` SHA-256 bijection against `Dental OPG (Classification)/`:
    - `CLS0019` (`TrackC:0` = `Caries`, `194` boxes in `117` OPGs)
    - `CLS0020` (`TrackC:1` = `Infection` / periapical abscess, `37` boxes in `23` OPGs)
    - `CLS0021` (`TrackC:2` = `Impacted Teeth`, `196` boxes in `86` OPGs)
    - `CLS0022` (`TrackC:3` = `Fractured Teeth`, `14` boxes in `13` OPGs — **ultra-rare minority flag**)
    - `CLS0023` (`TrackC:4` = `BDC/BDR` Broken-Down Crown/Root, `97` boxes in `50` OPGs)
    - `CLS0024` (`TrackC:5` = `Healthy Teeth`, `651` boxes in `221` OPGs)
- **Critical Partial-Label Warning (`CLS0024 Healthy Teeth`):**
  - An adult OPG typically contains `24–32` teeth, yet `DS0003` annotates an average of only **`2.83` `Healthy Teeth` boxes per OPG** (`651 / 230`) as selected reference examples (`P0024`).
  - Therefore, on Track C: (a) we evaluate both **all `6` native classes (`0..5`)** for comparability with `P0024`, and (b) **the `5` pathology-only classes (`0..4`, ignoring `Class 5 Healthy Teeth`)** so unboxed normal teeth do not penalize pathology precision as false positives (`UD04/UD13`).

---

### 2.4 Track D — `DS0004` (`Do 2024` Hanoi, Vietnam, `3` Periapical Severity Classes `TrackD:0..2`)
- **Source inventory (`6,741` Pascal VOC XML boxes across `3,924` active originals -> `~3,863` deduplicated unique OPGs):**
  - `CLS0025` (`TrackD:0` = `PAI 3`, `4,277` boxes [`63.45%`])
  - `CLS0026` (`TrackD:1` = `PAI 4`, `1,755` boxes [`26.03%`])
  - `CLS0027` (`TrackD:2` = `PAI 5`, `709` boxes [`10.52%`])
- **Granularity & Spectrum Rule:** Tight focal apical radiolucency `AABB`s (`mean_w = 0.025, mean_h = 0.038`). Because `DS0004` contains **`0` healthy OPGs** and leaves `PAI 1–2` unannotated, it is evaluated strictly on Track D (`3-class PAI 3/4/5` ordinal detection + pooled `1-class Periapical Lesion PAI 3–5` under `HC02` for `RQ2` tiling/resolution ablations).

---

### 2.5 Track E — `DS0005` (`AU-OPG` Ajman, UAE, `6` Adult Tooth Classes `TrackE:0..5`)
- **Source inventory (`7,006` oriented bounding boxes `OBB` across `901` annotated OPGs -> `~893` deduplicated unique OPGs):**
  - `CLS0028` (`TrackE:0` = `Filled`, `2,857` boxes)
  - `CLS0029` (`TrackE:1` = `Crowned`, `1,377` boxes)
  - `CLS0030` (`TrackE:2` = `Retained Root`, `941` boxes)
  - `CLS0031` (`TrackE:3` = `Cavitated`, `815` boxes)
  - `CLS0032` (`TrackE:4` = `Implant`, `544` boxes)
  - `CLS0033` (`TrackE:5` = `Impacted`, `472` boxes)
- **Coordinate Conversion Rule (`OBB -> AABB` for `scope.md v1.0.0` Compliance):**
  - Because our approved project scope (`scope.md v1.0.0`, `G01 PASS`) is standard axis-aligned `2D OPG` bounding-box detection (`AABB`), each rotated `OBB (xc, yc, w, h, θ)` is deterministically converted at `STEP-015/021` to its tight enclosing axis-aligned bounding box:
    $$\text{xmin} = \min_k x_k, \quad \text{ymin} = \min_k y_k, \quad \text{xmax} = \max_k x_k, \quad \text{ymax} = \max_k y_k$$
    over the `4` rotated corners $k \in \{1,2,3,4\}$, clipped to `[0, W] × [0, H]`, while retaining native `OBB` parameters in restricted manifests for reference.

---

### 2.6 Track F — `DS0006` (`MD-OPG` Zanjan, Iran, `2` Pediatric Caries Classes `TrackF:0..1` + Excluded ROI `z`)
- **Source inventory (`170` pediatric mixed-dentition OPGs, ages `3–12`; `895` caries polygons + `170` `Smile Zone` rectangles; `1` zero-area polygon dropped):**
  - `CLS0034` (`TrackF:0` = `Proximal Caries` [`p`], `716` polygons -> tight lesion `AABB`)
  - `CLS0035` (`TrackF:1` = `Occlusal Caries` [`o`], `179` polygons -> tight lesion `AABB`)
  - `CLS0036` (`EXCLUDED-ROI` = `Smile Zone` [`z`], `170` arch-framing rectangles — **excluded from object detection classes**; retained solely as optional ROI crop coordinate metadata for `STEP-019` preprocessing to strip the `66.17%` black letterbox border).

---

## 3. Overlap, Nesting, Negative & Ambiguity Governance (`OS §6.1–6.2`)

1. **Co-existing & Nested Boxes (`Multi-Label Spatial Overlap`):**
   - On dental OPGs, multiple true clinical entities frequently occupy overlapping spatial regions of the same tooth (e.g., `DS0001`: a tooth with `CLS0002 Prosthetic restoration` on the crown, `CLS0004 Endodontic treatment` in the root canal, and `CLS0008 Apical periodontitis` at the root apex; or `CLS0003 Obturation` adjacent to `CLS0005 Carious lesion`).
   - **Rule:** Overlapping boxes of **different classes** are valid co-existing ground-truth objects. Therefore, post-processing (`UD13`) **must use class-aware NMS** (never class-agnostic NMS that suppresses an apical lesion or crown overlapping a root canal filling!).
2. **Reviewed Negatives vs Unassessed Regions (`OS §6.1`, `§6.2 #4–5`):**
   - An image with `0` ground-truth boxes for a given class is a **valid negative** for that class *only* within the dataset's declared annotation scope (e.g., `DS0001` OPGs with zero `Implant` boxes are true negatives for `Implant`, whereas `DS0004` OPGs without `Implant` labels are **unassessed** for implants because `DS0004` only annotated `PAI 3–5`).
   - Unannotated files (`DS0002` `50` challenge-val PNGs, `DS0003_IMG_001202`, `DS0005` `134` extra JPGs) are **quarantined as unassessed (`missing_labels`)**, never treated as reviewed negative background images!
3. **Zero-Area & Degenerate Box Rule (`STEP-013` Defects):**
   - The `4` degenerate zero-area annotations found across all `25,355` files (`2` `Bone resorbtion` + `1` `Surgical device` in `DS0001`, and `1` polygon in `DS0006`) are deterministically dropped during canonical export (`area <= 1.0 px²` or `w <= 0` or `h <= 0`) and logged in `04_Annotations/annotation_registry.csv`.

---

## 4. Cross-Cohort Harmonized Evaluation Bridges (`HC01–HC05`, `CLS0037–CLS0041`)

To support `RQ1` and `RQ2` external domain-shift experiments (`UD15`) **without violating box-granularity or partial-annotation rules**, we define `5` explicit evaluation bridges (`CLS0037–CLS0041`):

| Bridge ID (`ClassID`) | Concept Name | Directly Compatible Granularity Pairings (`IoU @ 0.50` Valid) | Cross-Granularity Pairings *(Require Center-Inside-Tooth or Tooth-Level Mapping Caveat)* |
|---|---|---|---|
| **`HC01`** (`CLS0037`) | **Dental Caries** | **Focal Lesion Tier:** `DS0001 (CLS0005)` $\leftrightarrow$ `DS0006 (CLS0034+0035)` *(adult vs pediatric shift)*<br>**Whole-Tooth Tier:** `DS0002 (CLS0016+0018)` $\leftrightarrow$ `DS0003 (CLS0019)` $\leftrightarrow$ `DS0005 (CLS0031)` | Focal box (`DS0001`) vs Whole-tooth box (`DS0002/0003/0005`) differs in box height (`0.04` vs `0.22`) — never evaluate standard `IoU>=0.50` across focal vs whole-tooth without explicit granularity note! |
| **`HC02`** (`CLS0038`) | **Periapical Lesion** | **Focal Apical Tier:** `DS0001 (CLS0008 Apical periodontitis)` $\leftrightarrow$ `DS0004 (CLS0025+0026+0027 PAI 3–5)` *(Romania $\leftrightarrow$ Vietnam direct focal apical test!)* | `DS0002 (CLS0017)` and `DS0003 (CLS0020)` use tooth-plus-apex boxes (`mean_h ~ 0.22–0.24`). |
| **`HC03`** (`CLS0039`) | **Impacted Tooth** | **Whole-Tooth Tier (`4` Countries Directly Compatible!):** `DS0001 (CLS0007)` $\leftrightarrow$ `DS0002 (CLS0015)` $\leftrightarrow$ `DS0003 (CLS0021)` $\leftrightarrow$ `DS0005 (CLS0033)` (`2,360` total boxes across Romania, Türkiye, Bangladesh, UAE) | None — all `4` cohorts box the entire impacted tooth (`mean_w ~ 0.06–0.08, mean_h ~ 0.15–0.20`). |
| **`HC04`** (`CLS0040`) | **Residual Root / BDC-BDR** | **Whole-Remnant Tier (`3` Countries Directly Compatible!):** `DS0001 (CLS0009 Root fragment)` $\leftrightarrow$ `DS0003 (CLS0023 BDC/BDR)` $\leftrightarrow$ `DS0005 (CLS0030 Retained Root)` (`2,540` total boxes) | None — all `3` cohorts box the residual root/broken-down remnant. |
| **`HC05`** (`CLS0041`) | **Dental Implant** | **Fixture Tier (`2` Countries Directly Compatible!):** `DS0001 (CLS0001 Implant)` $\leftrightarrow$ `DS0005 (CLS0032 Implant)` (`1,066` total boxes across Romania & UAE) | None — both box the endosseous implant fixture. |

---

## 5. Required Human & Dental Reviewer Approval Questions (`UD04` -> `STEP-015 / G05`)

Before freezing `04_Annotations/protocols/annotation_protocol_v1.0.0.md` and assessing **`G05`** (`STEP-015`), the **Dental Reviewer** and **Supervisor (`Ms Faiza Feroz`)** + **Team (`Anik & Mahajub`)** must confirm the following `4` decisions (`recorded in DEC0004.md`):

1. **`Q1 — Track A (`DS0001`) Exclusion of `Class 11 (Root resorption, N=5)` & Handling of Rare Classes:**
   - Approve excluding `CLS0012 Root resorption` (`5` train boxes, `0` valid/test/external boxes) from trainable classes (`13` active classes `TrackA:0..12`), and keeping `CLS0011 Apical surgery` (`91` boxes) + `CLS0010 Furcation lesion` (`328` boxes) active with explicit support-weighted + per-class reporting (`UD13`)?
2. **`Q2 — Track B (`DS0002 DENTEX`) & Track C (`DS0003 Dhaka`) Dual Evaluation Modes:**
   - For `DS0002`: Approve training on all `4` native classes (`Impacted, Caries, Periapical Lesion, Deep Caries`) while also reporting pooled `Any Caries (Caries + Deep Caries)`?
   - For `DS0003`: Because `Class 5 (Healthy Teeth)` is only selectively boxed (`~2.8` teeth/OPG), approve evaluating **both** the `5` pathology classes (`0..4`: `Caries, Infection, Impacted, Fractured, BDC/BDR`) and the full `6`-class setup (`0..5`), flagging `Fractured Teeth` (`N=14`) as low-support descriptive?
3. **`Q3 — Track D (`DS0004 PAI 3–5`), Track E (`DS0005 OBB->AABB`) & Track F (`DS0006 Pediatric`) Conversions:**
   - Approve deterministic conversion of `DS0005` rotated `OBB`s and `DS0006` caries polygons (`p, o`) to tight axis-aligned bounding boxes (`AABB`), excluding `DS0006` `z` (`Smile Zone` ROI rectangle) from object classes, and dropping the `4` zero-area shapes (`3` in `DS0001`, `1` in `DS0006`)?
4. **`Q4 — Cross-Cohort Harmonization Bridges (`HC01–HC05`):**
   - Approve restricting cross-cohort generalization tests (`RQ1/UD15`) to granularity-matched bridges (`HC02` `DS0001 <-> DS0004` focal apical; `HC03` `DS0001/0002/0003/0005` impacted; `HC04` `DS0001/0003/0005` root fragment/BDC; `HC05` `DS0001/0005` implant; `HC01` focal vs whole-tooth caries separated)?
