# T12 — Leakage-Safe Grouped Split Report: `SPLIT0001` (`DS0001` / `TrackA`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `SPLIT0001` (Dataset: `DS0001`, Annotation Release: `ANN0001`, Track: `TrackA`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/DS0001_images.csv` (`sha256:15627853af1a545c86801afb6be5e3a503d3e60921f1da259a65fed21013015f`); `04_Annotations/exports/ANNB0001_TrackA/export_manifest.csv` (`sha256:464057e57980d29f7a97df93fa7a15bd512d22efcd155966426c522c2f6daf64`); `04_Annotations/classes.csv` (`sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/DS0001_images.csv`):** `15627853af1a545c86801afb6be5e3a503d3e60921f1da259a65fed21013015f`
- **Frozen Annotation Release (`ANN0001` / `export_manifest.csv`):** `464057e57980d29f7a97df93fa7a15bd512d22efcd155966426c522c2f6daf64`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`
- **Split Manifest (`03_Datasets/splits/SPLIT0001/manifest.csv`):** `8260d222aba799aa7e46720bd604e625ecd43228ad49dc53c8e0ddd6c61c4dc9`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** Patient IDs omitted at source (Zenodo 15487430); grouped by connected components of exact SHA-256 identity (187 multi-file groups = 197 extra copies) + re-encoded identical pairs (corr >= 0.99: 18 pairs) + high-correlation near-duplicate pairs (0.95 <= corr < 0.99: 2 pairs). Official contaminated train/valid split (42 exact leaks = 27.5% val contamination) discarded; external_validation (180 OPGs -> 178 unique canonical + 2 deduplicated copies; 0 overlap with internal) preserved sealed as external_test.
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`1808`**
  - **Labeled Images Partitioned:** **`1808`** (`1594` unique `active_canonical` radiographs across **`1592`** connected groups + `214` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`0`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{corr} \ge 0.99$):** **`215`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{corr} < 0.99$ or verified re-shoot):** **`2`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`20261121`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
| **`train`** | `992` | **`994`** (`70.20%`) | `145` | **`13253`** (`69.85%`) |
| **`val`** | `214` | **`214`** (`15.11%`) | `35` | **`2833`** (`14.93%`) |
| **`test`** | `208` | **`208`** (`14.69%`) | `32` | **`2888`** (`15.22%`) |
| **`external_test`** | `178` | **`178`** (`100.00%`) | `2` | **`2925`** (`100.00%`) |

---

## class support

Every active class in `TrackA` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`TrackA`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) | `external_test` Boxes (Imgs) |
|---|---:|---:|---:|---:|---|
| `Class 0` | **`478`** (`131`) | `322` (`89`) | `70` (`17`) | `70` (`20`) | `16` (`5`) |
| `Class 1` | **`1747`** (`643`) | `1087` (`389`) | `233` (`86`) | `235` (`88`) | `192` (`80`) |
| `Class 2` | **`4753`** (`922`) | `2738` (`545`) | `568` (`130`) | `573` (`119`) | `874` (`128`) |
| `Class 3` | **`3389`** (`942`) | `2002` (`588`) | `437` (`120`) | `437` (`116`) | `513` (`118`) |
| `Class 4` | **`3037`** (`932`) | `1891` (`585`) | `404` (`120`) | `446` (`126`) | `296` (`101`) |
| `Class 5` | **`3257`** (`519`) | `1804` (`313`) | `386` (`56`) | `390` (`72`) | `677` (`78`) |
| `Class 6` | **`994`** (`400`) | `617` (`247`) | `133` (`49`) | `133` (`53`) | `111` (`51`) |
| `Class 7` | **`1050`** (`567`) | `660` (`369`) | `142` (`76`) | `142` (`74`) | `106` (`48`) |
| `Class 8` | **`1266`** (`436`) | `819` (`277`) | `176` (`64`) | `178` (`62`) | `93` (`33`) |
| `Class 9` | **`277`** (`196`) | `180` (`130`) | `39` (`28`) | `39` (`26`) | `19` (`12`) |
| `Class 10` | **`84`** (`46`) | `47` (`29`) | `10` (`5`) | `10` (`6`) | `17` (`6`) |
| `Class 11` | **`485`** (`202`) | `334` (`142`) | `73` (`28`) | `72` (`29`) | `6` (`3`) |
| `Class 12` | **`1082`** (`213`) | `752` (`147`) | `162` (`32`) | `163` (`33`) | `5` (`1`) |

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
