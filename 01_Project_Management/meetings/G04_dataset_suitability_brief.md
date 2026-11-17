# `G04` Dataset Access, Relevance & Quality Suitability Brief (`STEP-013`)

**To:** Akhtaruzzaman Anik (Data Steward), Mahajub Al Shabah (Literature / Model Lead), Ms Faiza Feroz (Supervisor), and Dental Reviewer *(needed for `STEP-013`/`STEP-014`)*
**Date prepared:** `2026-11-18`
**Linked Artifacts:** `03_Datasets/datasets.csv`, `03_Datasets/reports/acquisition_report_STEP-012.md`, `03_Datasets/reports/DS0001–DS0006_quality.md`, `DEC0003.md v6`

---

## 1. Ready Evidence Summary Across All `6` Acquired Cohorts (`7,789` Active OPGs)

All `6` authorized cohorts under `DEC0003 v6` have now been downloaded off-Git, MD5/SHA-256 verified, decoded (`0` decode errors across `25,355` scanned image files), deduplicated-screened across cohorts (**`0` cross-cohort overlaps**, max cross pixel correlation `= 0.7793`), and visually sampled:

| Dataset | Country / Track Role | Active Clean Count *(Deduplicated Est.)* | Key `STEP-013` Findings Requiring Approval Before `G04` & `UD04/UD07` |
|---|---|---|---|
| **`DS0001` (`UMFIH`)** | Romania + Ext (`Primary Multi-Class`) | `1,808` -> **`~1,590`** unique (`178` ext) | Official split leaks **`42` (`27.5%`) exact `train<->valid` copies** + `18` re-encoded dups -> discard official split & re-split at `G07`. Verified `external_validation` uses `legend.txt` (`0–13`). Exclude `Class 11 (Root resorption, N=5)` at `UD04`. Footer timestamps visible (`no patient names`). |
| **`DS0002` (`DENTEX`)** | Türkiye (`Balanced-Concept` -> actually Skewed `4`-Class) | **`755`** (`705` labeled + `50` no-GT val; **`0` duplicates**) | **Critical fact correction:** actual disease counts are **`Caries 2,189`, `Impacted 604`, `Deep Caries 578`, `Periapical Lesion 158`** (`4.5%`, `14:1` skew — NOT `800–965/class`!). Validation `50` OPGs have `0` GT labels -> split the `705` labeled OPGs. `1` sensor-streak artifact (`DS0002_IMG_000641`). Conservative `NC-SA` license caution retained. |
| **`DS0003` (`Rahman Dhaka`)** | Bangladesh (`Local Shift + RQ2 CLAHE`) | `231` (`230` `.txt` + `1` unlabeled; `1,189` boxes) | All `604` Roboflow augs & `517` cls copies quarantined. `DS0003_IMG_001202` lacks `.txt`. Two handheld photos of same film (`DS0003_IMG_001153/1321`) grouped. `30` JPGs have Windows Photo Editor EXIF + `"PRESCRIPTION POINT"` corner logo -> **strip EXIF & mask corner logos**. Whole-tooth box schema (`mean_h ~ 0.18–0.25`) vs lesion-tight boxes. |
| **`DS0004` (`Do 2024 Hanoi`)** | Vietnam (`PAI 3–5` Tiling Track) | `3,924` -> **`~3,863`** unique | Quarantined `13,071` augs; caught **`59` extra exact SHA + `2` re-encoded duplicates inside `Original JPG Images`!** Valid `6,741` boxes (`PAI 3=4277, PAI 4=1755, PAI 5=709`), mixes `Sirona` & `RAYSCAN α`. **`0` healthy OPGs** -> dedicated small-lesion/tiling track ONLY (`never blind merge`). |
| **`DS0005` (`AU-OPG`)** | UAE (`Adult OBB->AABB Track`) | `901` (`7,006` OBBs) | Caught **`6` re-encoded identical pairs (`corr >= 0.99`) leaking `train<->val`** despite `"serial excluded"`! Quarantined `134` extra unannotated JPGs (`90/134` overlap annotated splits). Healthy teeth unannotated (`P0026`). |
| **`DS0006` (`MD-OPG`)** | Iran (`Pediatric Caries Ages 3–12`) | `170` (`895` caries polygons) | **`66.17%` median solid-black padding** framing every PNG (`UD09` autocrop needed). Kept strictly as **separate pediatric caries track** (`ages 3–12`). Drop `1` zero-area polygon. |

---

## 2. Decisions Needed for `G04 = PASS` (`Human & Dental Reviewer Sign-Off`)

To mark **`G04 = PASS`** in `01_Project_Management/gates.csv` (`OS §13.2`), please confirm:

1. **Researcher & Custodian Confirmation (`UD02` Selection & Custody):**
   - Confirm keeping all `6` cohorts on their **separate, non-merged track assignments** above (rather than naive pooling across incompatible schemas), using **Private Google Drive** to back up `03_Datasets/raw/DS0001–DS0006/` + `*_restricted*` manifests (`DEC0011`).
2. **Visual & Target-Feasibility Sign-Off (`Dental Reviewer + Researchers`, `STEP-013`):**
   - Review the off-Git stratified contact sheets (`03_Datasets/raw/qc_samples/DS0001–DS0006_qc_sheet.jpg`) with a qualified dental reviewer (or confirm dental reviewer arrangement) verifying:
     - Genuine `2D OPG` clinical target visibility across adult & pediatric cohorts;
     - Proposed exclusions (`17,566` pre-aug/derived/unlabeled/extra images, `~279` exact/re-encoded duplicate files across `DS0001/0003/0004/0005`, `4` zero-area boxes, `DS0001 Class 11` rarity);
     - Mandatory privacy handling (EXIF removal on `DS0003`, corner logo `"PRESCRIPTION POINT"` masking on `DS0003`, and footer/artifact inspection before any `S16` defense web demo).
