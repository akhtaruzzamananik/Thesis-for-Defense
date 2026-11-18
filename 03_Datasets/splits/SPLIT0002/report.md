# T12 — Leakage-Safe Grouped Split Report: `SPLIT0002` (`DS0002` / `TrackB`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `SPLIT0002` (Dataset: `DS0002`, Annotation Release: `ANN0002`, Track: `TrackB`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/DS0002_images.csv` (`sha256:f8a6218fc1e3700b1508fa100f114976f42507cf1dc3f91b256a861be8f1815d`); `04_Annotations/exports/ANNB0002_TrackB/export_manifest.csv` (`sha256:b127fa293af54a9b0a3d2fec49a35ab2afee27f506ae65ad957f3cba5f724b29`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/DS0002_images.csv`):** `f8a6218fc1e3700b1508fa100f114976f42507cf1dc3f91b256a861be8f1815d`
- **Frozen Annotation Release (`ANN0002` / `export_manifest.csv`):** `b127fa293af54a9b0a3d2fec49a35ab2afee27f506ae65ad957f3cba5f724b29`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`
- **Split Manifest (`03_Datasets/splits/SPLIT0002/manifest.csv`):** `a31c3245ff5eee84135528b4caa477e7886ee959aeaaa49e9a4077db572b2de1`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** Patient IDs omitted at source (Zenodo 7812323); 0 exact SHA-256 duplicates and 0 perceptual near-duplicates (all dHash<=4 pairs measured pixel corr < 0.90). The 705 labeled training OPGs (678 positive + 27 reviewed_empty) are partitioned 70/15/15 with minority-class stratification for Periapical Lesion (158 boxes); the 50 unlabeled challenge-validation OPGs remain quarantined_missing_labels.
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`755`**
  - **Labeled Images Partitioned:** **`705`** (`705` unique `active_canonical` radiographs across **`705`** connected groups + `0` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`50`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{corr} \ge 0.99$):** **`0`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{corr} < 0.99$ or verified re-shoot):** **`0`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`20261122`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
| **`train`** | `493` | **`493`** (`69.93%`) | `0` | **`2468`** (`69.95%`) |
| **`val`** | `106` | **`106`** (`15.04%`) | `0` | **`530`** (`15.02%`) |
| **`test`** | `106` | **`106`** (`15.04%`) | `0` | **`530`** (`15.02%`) |
| **`quarantined_missing_labels`** | `50` | **`0`** (`100.00%`) | `0` | **`0`** (`100.00%`) |

---

## class support

Every active class in `TrackB` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`TrackB`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) |
|---|---:|---:|---:|---:|
| `Class 0` | **`604`** (`254`) | `422` (`176`) | `91` (`38`) | `91` (`40`) |
| `Class 1` | **`2188`** (`623`) | `1532` (`438`) | `328` (`94`) | `328` (`91`) |
| `Class 2` | **`158`** (`116`) | `110` (`82`) | `24` (`17`) | `24` (`17`) |
| `Class 3` | **`578`** (`321`) | `404` (`223`) | `87` (`51`) | `87` (`47`) |

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
