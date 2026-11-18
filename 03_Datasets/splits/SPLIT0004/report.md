# T12 — Leakage-Safe Grouped Split Report: `SPLIT0004` (`DS0004` / `TrackD`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `SPLIT0004` (Dataset: `DS0004`, Annotation Release: `ANN0004`, Track: `TrackD`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/DS0004_images.csv` (`sha256:0647437ed3778b31c16f2056f0e8f0224dbb2654b2661eef6a71922fc47c29c2`); `04_Annotations/exports/ANNB0004_TrackD/export_manifest.csv` (`sha256:e2ae185dd3f61ffd66bcb901728d30f40ca03876c73ee626ade26c3d392f25c1`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/DS0004_images.csv`):** `0647437ed3778b31c16f2056f0e8f0224dbb2654b2661eef6a71922fc47c29c2`
- **Frozen Annotation Release (`ANN0004` / `export_manifest.csv`):** `e2ae185dd3f61ffd66bcb901728d30f40ca03876c73ee626ade26c3d392f25c1`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`
- **Split Manifest (`03_Datasets/splits/SPLIT0004/manifest.csv`):** `3b8a2bf9da87076e0b7dcb81f7b620738415702e33e22d2a690c42834c61af1f`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** Patient IDs omitted at source (Mendeley kx52tk2ddj V3; P0008 p. 34); all 13,071 Augmentation JPG Images quarantined at STEP-012. Intra-folder forensic audit of the 3,924 Original JPG Images caught 59 extra exact SHA-256 duplicate files + 2 re-encoded identical files (corr >= 0.99: IMG_013187/016453 & IMG_014993/016792) + 1 near-duplicate pair (corr = 0.9533: IMG_014630/016338), yielding 3,863 active_canonical radiographs across 3,862 connected groups.
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`3924`**
  - **Labeled Images Partitioned:** **`3924`** (`3863` unique `active_canonical` radiographs across **`3862`** connected groups + `61` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`0`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{corr} \ge 0.99$):** **`61`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{corr} < 0.99$ or verified re-shoot):** **`1`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`20261124`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
| **`train`** | `2707` | **`2707`** (`70.08%`) | `45` | **`4648`** (`69.95%`) |
| **`val`** | `577` | **`578`** (`14.96%`) | `5` | **`998`** (`15.02%`) |
| **`test`** | `578` | **`578`** (`14.96%`) | `11` | **`999`** (`15.03%`) |

---

## class support

Every active class in `TrackD` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`TrackD`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) |
|---|---:|---:|---:|---:|
| `Class 0` | **`4211`** (`2755`) | `2946` (`1929`) | `632` (`413`) | `633` (`413`) |
| `Class 1` | **`1731`** (`1367`) | `1211` (`957`) | `260` (`206`) | `260` (`204`) |
| `Class 2` | **`703`** (`649`) | `491` (`453`) | `106` (`98`) | `106` (`98`) |

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
