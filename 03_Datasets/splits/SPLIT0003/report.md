# T12 — Leakage-Safe Grouped Split Report: `SPLIT0003` (`DS0003` / `TrackC`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `SPLIT0003` (Dataset: `DS0003`, Annotation Release: `ANN0003`, Track: `TrackC`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/DS0003_images.csv` (`sha256:da849181d2e7360c6335d6343426c6bc819cc9062a4f1921b4fc903bf2c36cfe`); `04_Annotations/exports/ANNB0003_TrackC/export_manifest.csv` (`sha256:557ec6ccaf110bba13d641ee16dc58a4cb104e93880a04c7c28243a377ee3d24`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/DS0003_images.csv`):** `da849181d2e7360c6335d6343426c6bc819cc9062a4f1921b4fc903bf2c36cfe`
- **Frozen Annotation Release (`ANN0003` / `export_manifest.csv`):** `557ec6ccaf110bba13d641ee16dc58a4cb104e93880a04c7c28243a377ee3d24`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`
- **Split Manifest (`03_Datasets/splits/SPLIT0003/manifest.csv`):** `add134cc9e74b86b1efcae2a8f60c960397251ddb2f8ba5886260a1b85c87952`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** Patient IDs omitted at source (Mendeley c4hhrkxytw V4); all 604 Roboflow pre-split augmented images and 517 classification copies quarantined at STEP-012. Visually verified same-film smartphone re-shoot pair (DS0003_IMG_001153 <-> DS0003_IMG_001321, dHash H=1, corr=0.8625) locked into a single connected group (229 unique groups across 230 labeled OPGs); unlabeled DS0003_IMG_001202 kept quarantined_missing_labels.
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`231`**
  - **Labeled Images Partitioned:** **`230`** (`230` unique `active_canonical` radiographs across **`229`** connected groups + `0` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`1`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{corr} \ge 0.99$):** **`0`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{corr} < 0.99$ or verified re-shoot):** **`2`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`20261123`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
| **`train`** | `162` | **`163`** (`70.87%`) | `0` | **`824`** (`69.30%`) |
| **`val`** | `34` | **`34`** (`14.78%`) | `0` | **`183`** (`15.39%`) |
| **`test`** | `33` | **`33`** (`14.35%`) | `0` | **`182`** (`15.31%`) |
| **`quarantined_missing_labels`** | `1` | **`0`** (`100.00%`) | `0` | **`0`** (`100.00%`) |

---

## class support

Every active class in `TrackC` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`TrackC`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) |
|---|---:|---:|---:|---:|
| `Class 0` | **`194`** (`117`) | `134` (`83`) | `30` (`17`) | `30` (`17`) |
| `Class 1` | **`37`** (`23`) | `25` (`16`) | `6` (`4`) | `6` (`3`) |
| `Class 2` | **`196`** (`86`) | `136` (`61`) | `30` (`12`) | `30` (`13`) |
| `Class 3` | **`14`** (`13`) | `10` (`9`) | `2` (`2`) | `2` (`2`) |
| `Class 4` | **`97`** (`50`) | `67` (`37`) | `15` (`6`) | `15` (`7`) |
| `Class 5` | **`651`** (`221`) | `452` (`156`) | `100` (`32`) | `99` (`33`) |

---

## overlap checks

Verified programmatically by `assert_zero_cross_partition_leakage` (`src/opg/dataset_split.py`):
- **Cross-Partition `GroupID` Count:** **`0`** (Required: `0`)
- **Cross-Partition `SHA-256` Count:** **`0`** (Required: `0`)
- **Cross-Partition Exact/Re-Encoded Duplicate Edges:** **`0`** (Required: `0`)
- **Cross-Partition Near-Duplicate / Re-Shoot Edges:** **`0`** (Required: `0`)

---

## unknown identity limits

- **Explicit Limitation Statement (`OS §4.4`, `DEC0007`):** For `DS0001–DS0004`, upstream public repositories omitted patient-level identifiers at de-identification; for `DS0005`, authors reported excluding serial patient OPGs (`P0026 p. 4`); for `DS0006`, `1` OPG per pediatric patient is reported (`P0010 p. 9`). While connected-component grouping over exact SHA-256, perceptual `dHash`, and pixel correlation ($\ge 0.95$) eliminates all duplicate, re-encoded, and same-film re-shoot leakage, ** longitudinal separate-visit radiographs of the same patient with low global pixel correlation cannot be ruled out where upstream patient IDs were omitted**. Consequently, evaluation claims are bounded as **radiograph/duplicate-cluster-level independence** (and multi-clinic external independence on `DS0001 external_test` and cross-dataset `HC01–HC05` tests).

---

## custody/access

- **Sealed Final Test Rule (`OS §4.4`, `DEC0008`):** The `test` partition (and `DS0001` `external_test`) is **strictly sealed** from all model development, preprocessing statistic fitting (`STEP-021`), baseline smoke tests (`STEP-026`), hyperparameter tuning, and checkpoint/threshold selection (`STEP-028`–`030`). Test predictions may only be generated after the **`G11` Final-Test Release Freeze (`STEP-031`)**.

---

## approval

- **Approved (`2026-11-19`, `G07 PASS`):** Akhtaruzzaman Anik (`Data Steward`), Mahajub Al Shabah (`Leakage & Reproducibility Reviewer`), and Ms Faiza Feroz (`Supervisor`).
