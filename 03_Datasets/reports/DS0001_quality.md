# STEP-013 Quality, Privacy, Duplicate & Label Forensic Audit — `DS0001` (`CAND0001` UMFIH)

| Field | Value |
|---|---|
| DatasetID / CandidateID | `DS0001` / `CAND0001` (`UMFIH` Cluj-Napoca + Multi-Center External) |
| Audit Scope & Count | **`1,808`** active raw images (`1,375` `train`, `153` `valid`, `100` `test`, `180` `external_validation`); `0` quarantined; `0` decode errors |
| Owner / Auditor | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Date | `2026-11-17` |
| Evidence Sources | `03_Datasets/manifests/DS0001_images.csv`, `03_Datasets/manifests/DS0001_qc_summary.json`, off-Git `DS0001_restricted_qc.csv`, `DS0001_restricted_dups.csv`, `qc_samples/DS0001_qc_sheet.jpg`, `dup_pair_verification.jpg` |
| Gate Status | **`G04 PASS` (`2026-11-18`, `G04_assessment_2026-11-18.md`)** |

---

## 1. Decoding, Dimensions, Channels & Photometric Quality

| Metric (`N = 1,808`) | `min` | `p05` | `median` | `p95` | `max` | Finding |
|---|---|---|---|---|---|---|
| **Width (px)** | `804` | `2,386` | `2,652` | `2,868` | `5,538` | `0` images `< 800` px; high diagnostic resolution overall |
| **Height (px)** | `415` | `1,474` | `1,536` | `1,537` | `3,008` | Matches Vatech `PCH-2500` standard + external devices |
| **Aspect Ratio (`W/H`)** | `1.55` | `1.55` | `1.73` | `1.91` | `2.22` | `0` aspect-ratio outliers (`< 1.3` or `> 2.8`) |
| **Mean Luma (`0–255`)** | `61.66` | `92.52` | `122.59` | `147.01` | `180.12` | Natural exposure variation retained (over/under-exposed included) |
| **Std Luma** | `37.33` | `51.97` | `63.44` | `73.71` | `81.76` | Good contrast spread across cohort |
| **`%` Black (`<= 3`)** | `0.0%` | `0.06%` | `3.19%` | `9.45%` | `16.95%` | Normal clinical border framing (no excess letterbox padding) |
| **`%` White (`>= 252`)** | `0.0%` | `0.0%` | `1.59%` | `5.90%` | `12.91%` | Highlighted restorations/screws/plate hardware |
| **Sharpness (`Laplacian var` @ 800w)** | `73.96` | `251.54` | `1,210.25` | `1,750.09` | `1,869.29` | Crisp overall; low-tail (`73.96`) reflects soft external-clinic films |

- **Channels / Tint (`1,807 RGB` + `1 RGBA`):** **`test/images/v60.png`** is `RGBA` (`938 × 491`, visually confirmed as `DS0001_IMG_000339` on `DS0001_qc_sheet.jpg`) with green corner text `"scala 125%"`. Convert `RGBA -> 3-channel RGB` deterministically in loader (`PP`) rather than dropping unless visually unreadable.

---

## 2. Privacy, EXIF & Visual Burned-In Inspection (`DS0001_qc_sheet.jpg`)

- **EXIF & PNG metadata:** **`0` images** carry sensitive EXIF tags (`0` `DateTime/Software/Make/Model/GPS`); `99` images contain `icc_profile`.
- **Visual pixel inspection (`DS0001_qc_sheet.jpg`):**
  - All sampled images are genuine **`2D OPG` clinical adult radiographs** with orthopedic plates/screws, dense crowns, implants, and natural dental pathology.
  - **Bottom exposure footer stamped in pixels:** Many `UMFIH` Vatech scans carry a small burned-in bottom-left white text bar (e.g., `"11/28/2022 8:13 AM - STD PANORAMIC - 68kV 5mA 14.8s - 6.08uGym2"` plus `R`/`L` laterality tags, and `"Pax-i"` / `"R"` side mark on re-encoded external-style films). No patient names or clinic names were visible in sampled frames; **for `S16` web-demo & thesis figures (`UD23`)**, crop/mask or select footer-free samples during disclosure check.

---

## 3. Exact & Perceptual Near-Duplicate Audit (`Critical Leakage Discovery`)

Pre-supplied Zenodo `UMFIH` folders suffer from severe exact and near-duplicate contamination across `internal_train` and `internal_valid`:

1. **Exact byte-for-byte SHA-256 duplicates (`187` multi-file groups = `197` extra copies; `208` pairs):**
   - **`internal_train <-> internal_valid`:** **`42` exact images (`41` pairs + `1` triple) leak directly (`42 / 153 = 27.5%` of official validation set is byte-identical to training!)**.
   - Within splits: `141` groups in `internal_train`, `2` pairs in `internal_test`, `1` pair in `internal_valid`, `1` pair in `external_validation` (`180` external -> `179` unique SHA-256).
2. **Additional re-encoded duplicates (`SHA-256 != SHA-256`, `dHash <= 4` + pixel correlation `>= 0.99`):**
   - **`18` extra exact-visual re-encoded pairs** (`17` inside `internal_train`, `1` inside `external_validation`), visually verified on `dup_pair_verification.jpg` row 4 (`DS0001_IMG_000789` vs `DS0001_IMG_001388`, `corr = 1.0000`, `"Pax-i"` radiograph).
   - Plus `2` pairs at `corr = 0.95–0.99` and `1` pair at `corr = 0.90–0.95` inside `internal_train`.
3. **Cross-cohort overlap (`DS0001` vs `DS0003, DS0005, DS0006`):** `0` true cross-cohort duplicates (`dHash <= 3` pixel correlations against `DS0005 AU-OPG` measured `0.5681–0.7746`, confirming independent populations).

> [!CAUTION]
> **Binding `UD07 / G07` Action:** Pre-supplied `UMFIH` `train/valid/test` splits **MUST NOT** be reused. Before `G07`, collapse all exact SHA-256 + `corr >= 0.95` near-duplicate connected components into single patient/study families (`~1,590` unique clusters), keep `external_validation` (`~178` unique clusters) intact as an external cohort holdout (`0` cross-leakage with internal!), and re-split the deduplicated internal pool (`70/15/15` via `UD08`).

---

## 4. Label-Schema Forensic Audit (`legend.txt` vs `labels (1).txt` Reconciled!)

Extraction revealed a dangerous discrepancy between root `legend.txt` (`14` entries `0–13`) and `test_alte_cabinete/labels (1).txt` (`13` entries with swapped positions for `obturation`/`prosthetic restoration` and `impacted tooth`/`bone resorption`, and shifted `11/12`). Auditing all `24,891` boxes (`18,570` train + `1,972` valid + `1,369` test + `2,980` external; `0` missing `.txt`, `0` empty `.txt`, `0` malformed, `0` OOB) proves empirically which scheme `external_validation` uses:

| Class ID & `legend.txt` Name | `internal_train` Count (`mean_w`) | `internal_valid` Count | `internal_test` Count | `external_validation` Count (`mean_w`) | Alignment Proof |
|---|---|---|---|---|---|
| `0` Implant | `456` (`0.0359`) | `25` | `25` | `16` (`0.0420`) | Consistent |
| `1` Prosthetic restoration | `1,492` (`0.0954` wide) | `103` | `89` | `206` (`0.1002` wide) | **Matches `legend.txt`** (`not swapped` with narrow fillings!) |
| `2` Obturation | `3,615` (`0.0349` narrow) | `359` | `391` | `897` (`0.0344` narrow) | **Matches `legend.txt`** |
| `3` Endodontic treatment | `2,673` | `224` | `267` | `528` | Consistent |
| `4` Carious lesion | `2,745` | `407` | `141` | `296` | Consistent |
| `5` Bone resorbtion | `2,763` (`0.0213`) | `297` | `118` | `680` (`0.0284`) | **Matches `legend.txt`** (not swapped with wide `0.078` impacted!) |
| `6` Impacted tooth | `809` (`0.0608`) | `110` | `58` | `111` (`0.0779`) | **Matches `legend.txt`** |
| `7` Apical periodontitis | `973` | `100` | `80` | `106` | Consistent |
| `8` Root fragment | `1,205` | `171` | `33` | `93` | Consistent |
| `9` Furcation lesion | `268` | `23` | `18` | `19` | Rare (`total = 328`) |
| `10` Apical surgery | `66` | `4` | `4` | `17` | Ultra-rare (`total = 91`) |
| **`11` Root resorption** | **`5`** | **`0`** | **`0`** | **`0`** | **Unsupportable (`5` total boxes -> drop/exclude at `UD04`!)** |
| `12` Orthodontic device | `451` (`0.2768`) | `51` | `25` | `6` (`0.4238`) | **Matches `legend.txt`** (`wide arch`, `id=12`, not `labels (1).txt` line 12!) |
| **`13` Surgical device** | `1,049` (`0.1157`) | `98` | `120` | **`5`** (`0.1178`) | **Proves `0–13` `legend.txt` is used in `external_validation`!** |

- **Geometry anomaly to filter cleanly:** `3` zero-area boxes (`2` in `internal_train`, `1` in `external_validation`) must be dropped cleanly via preapproved rule (`UD05`), and **`Class 11` (`Root resorption`, `N=5`)** must be excluded (`UD04`) alongside handling sparse **`Class 10` (`Apical surgery`) / `Class 9` (`Furcation lesion`) / diffuse `Class 5` (`Bone resorbtion`, `GAP0003`)**.

---

## 5. Prospective Inclusion & Exclusion Rules (`Proposed for G04 / UD04 / UD07`)

1. **Retain all `~1,590` deduplicated unique `2D OPG` image clusters** (after merging exact SHA-256 + `corr >= 0.95` duplicates cleanly — keeping deterministic canonical representatives without post-hoc error filtering!).
2. **Quarantine/drop exact duplicates cleanly (`~197` exact SHA + `18–20` re-encoded copies)** and **`3` zero-area boxes**.
3. **Standardize `RGBA -> RGB`** (`1` PNG `v60.png`) in deterministic preprocessing.
4. **Pending human/dental review (`G04` & `G05`):** Qualified dental reviewer confirms class visibility & exclusion of `Class 11 (Root resorption)` / borderline classes (`UD04`).
