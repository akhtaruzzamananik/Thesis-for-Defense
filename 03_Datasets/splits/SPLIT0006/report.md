# T12 — Leakage-Safe Grouped Split Report: `SPLIT0006` (`DS0006` / `TrackF`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `SPLIT0006` (Dataset: `DS0006`, Annotation Release: `ANN0006`, Track: `TrackF`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/DS0006_images.csv` (`sha256:e4fe6f06dc45a38ff01ab721eb1759c5237ce13d1b5402fc66183f3aefea8f2d`); `04_Annotations/exports/ANNB0006_TrackF/export_manifest.csv` (`sha256:cd03980418a35123e01b1f1f14ebb8ce72f635320c016b07bcabe7e82759cd2e`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/DS0006_images.csv`):** `e4fe6f06dc45a38ff01ab721eb1759c5237ce13d1b5402fc66183f3aefea8f2d`
- **Frozen Annotation Release (`ANN0006` / `export_manifest.csv`):** `cd03980418a35123e01b1f1f14ebb8ce72f635320c016b07bcabe7e82759cd2e`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`
- **Split Manifest (`03_Datasets/splits/SPLIT0006/manifest.csv`):** `e75744071eeb3a31af233490d01ec9c15d54a65c9353140881573a0031aa9e6f`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** 170 distinct pediatric patients (1 OPG per patient, ages 3-12, P0010 p. 9); 340 derived Smile_Zone crops/masks quarantined at STEP-012. STEP-020 border-cropped interior pixel correlation check across all 170 OPGs (after removing the 66.17% black letterbox border) verified 0 exact or near-duplicate pairs (max interior pixel correlation = 0.9149 < 0.95), confirming 170 independent patient groups.
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`170`**
  - **Labeled Images Partitioned:** **`170`** (`170` unique `active_canonical` radiographs across **`170`** connected groups + `0` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`0`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{corr} \ge 0.99$):** **`0`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{corr} < 0.99$ or verified re-shoot):** **`0`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`20261126`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
| **`train`** | `121` | **`121`** (`71.18%`) | `0` | **`622`** (`69.57%`) |
| **`val`** | `25` | **`25`** (`14.71%`) | `0` | **`135`** (`15.10%`) |
| **`test`** | `24` | **`24`** (`14.12%`) | `0` | **`137`** (`15.32%`) |

---

## class support

Every active class in `TrackF` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`TrackF`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) |
|---|---:|---:|---:|---:|
| `Class 0` | **`716`** (`166`) | `498` (`119`) | `108` (`24`) | `110` (`23`) |
| `Class 1` | **`178`** (`84`) | `124` (`60`) | `27` (`12`) | `27` (`12`) |

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
