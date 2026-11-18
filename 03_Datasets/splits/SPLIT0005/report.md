# T12 — Leakage-Safe Grouped Split Report: `SPLIT0005` (`DS0005` / `TrackE`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `SPLIT0005` (Dataset: `DS0005`, Annotation Release: `ANN0005`, Track: `TrackE`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/DS0005_images.csv` (`sha256:002e869126a19806d9f6aa1827893ed0c390f8154e8fdce6075df309681450ac`); `04_Annotations/exports/ANNB0005_TrackE/export_manifest.csv` (`sha256:10ab3bcd08a9592df3d524a3eec26315e48068c2e95b6dae8d8fc011575d21d0`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/DS0005_images.csv`):** `002e869126a19806d9f6aa1827893ed0c390f8154e8fdce6075df309681450ac`
- **Frozen Annotation Release (`ANN0005` / `export_manifest.csv`):** `10ab3bcd08a9592df3d524a3eec26315e48068c2e95b6dae8d8fc011575d21d0`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`
- **Split Manifest (`03_Datasets/splits/SPLIT0005/manifest.csv`):** `f81ffcd59eaf8733d3917751ae2c3c242979ab418d352bfdfa1c5eae81ea6c14`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** Serial patient OPGs stated excluded at source (P0026 p. 4), yet STEP-013 pixel correlation caught 6 re-encoded identical pairs (corr >= 0.99, dHash H=0) leaking directly across official train<->val CSVs plus 2 near-duplicate pairs (0.95 <= corr < 0.99). Official contaminated split discarded; all 8 pairs collapsed into connected groups (895 active_canonical OPGs across 893 unique groups; 6 redundant re-encoded copies deduplicated; 134 unannotated extra JPGs quarantined).
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`901`**
  - **Labeled Images Partitioned:** **`901`** (`895` unique `active_canonical` radiographs across **`893`** connected groups + `6` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`0`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{corr} \ge 0.99$):** **`6`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{corr} < 0.99$ or verified re-shoot):** **`2`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`20261125`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
| **`train`** | `626` | **`628`** (`70.17%`) | `4` | **`4857`** (`69.91%`) |
| **`val`** | `134` | **`134`** (`14.97%`) | `1` | **`1043`** (`15.01%`) |
| **`test`** | `133` | **`133`** (`14.86%`) | `1` | **`1048`** (`15.08%`) |

---

## class support

Every active class in `TrackE` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`TrackE`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) |
|---|---:|---:|---:|---:|
| `Class 0` | **`2831`** (`658`) | `1978` (`457`) | `425` (`104`) | `428` (`97`) |
| `Class 1` | **`1366`** (`359`) | `957` (`257`) | `204` (`49`) | `205` (`53`) |
| `Class 2` | **`939`** (`385`) | `659` (`271`) | `140` (`57`) | `140` (`57`) |
| `Class 3` | **`812`** (`431`) | `566` (`305`) | `122` (`63`) | `124` (`63`) |
| `Class 4` | **`528`** (`180`) | `368` (`127`) | `80` (`26`) | `80` (`27`) |
| `Class 5` | **`472`** (`262`) | `329` (`186`) | `72` (`38`) | `71` (`38`) |

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
