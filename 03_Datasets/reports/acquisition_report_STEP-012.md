# Unified STEP-012 & Cross-Cohort Acquisition Receipt (`DS0001–DS0006`)

| Metadata | Value |
|---|---|
| Step / Gate | **`STEP-012` Complete** & Technical **`STEP-013` Complete** (`Feeds G04 Assessment`) |
| Owner (Data Steward) | Akhtaruzzaman Anik (`232-15-252`) |
| Reviewer | Mahajub Al Shabah (`232-15-900`) |
| Date Completed | `2026-11-18` |
| Governing Decision | `DEC0003 v6` (`6` Authorized Open `2D OPG` Cohorts; Off-Git Custody `DEC0011`) |
| Cross-Cohort Screening | `03_Datasets/manifests/cross_dataset_dup_summary.json` (`7,789` active OPGs screened across `DS0001–DS0006`: **`0` exact SHA-256 matches, max cross pixel corr = `0.7793`**) |

---

## 1. Master Inventory & Count Reconciliation Across All `6` Cohorts

> [!IMPORTANT]
> **Exact File Conservation Verified (`acquired = active_raw + quarantined + decode_errors`):**
> Across all `6` acquired repositories (**`25,355` scanned image files**, `~21.73 GiB` total raw sources), **`0` decode errors** occurred and **zero medical image bytes or archives exist in Git (`git ls-files = 0`)**.

| DS ID | Cand ID | Upstream Record & Hash Verified | Total Scanned | Active Raw OPGs | Quarantined (`Pre-Aug / Derived / Extra`) | Unique Active `SHA-256` | Manifest `SHA-256` (`DS####_images.csv`) |
|---|---|---|---:|---:|---:|---:|---|
| **`DS0001`** | `CAND0001` (`UMFIH`) | Zenodo `15487430` (`1.30 GiB`, MD5 `18d5ac...`) | `1,808` | **`1,808`** (`1628` int + `180` ext) | `0` | **`1,611`** (`197` exact + `18` re-enc dups!) | `4f75c64e9a295553...` |
| **`DS0002`** | `CAND0002` (`DENTEX`) | Zenodo `7812323` (`10.18 GiB` + `142.6 MiB`, MD5s verified) | `3,654` | **`755`** (`705` labeled train + `50` no-GT val) | `2,899` (`693` quad + `634` enum + `1,571` unlbl + `1` `.ipynb_ckpts`) | **`755`** (`0` dups!) | `fb268930e339b90d...` |
| **`DS0003`** | `CAND0003` (`Dhaka`) | Mendeley `c4hhrkxytw` V4 (`196.67 MiB`, `sha256:f11eaa...`) | `1,352` | **`231`** (`230` `.txt` + `1` unlabeled) | `1,121` (`604` Roboflow aug + `517` cls dup pool) | **`231`** (`1` hand-reshot film pair!) | `abdc75c919884033...` |
| **`DS0004`** | `CAND0004` (`Do 2024`) | Mendeley `kx52tk2ddj` V3 (`8.31 GiB`, `sha256:5be5d9...`) | `16,995` | **`3,924`** (`Original JPG Images`) | `13,071` (`Augmentation JPG Images`) | **`3,865`** (`59` exact + `2` re-enc dups!) | `b05ad87b806e68ec...` |
| **`DS0005`** | `CAND0005` (`AU-OPG`) | HF `YSFF/AU-OPG` (`1.37 GiB`, `1,041` LFS SHA-256 verified) | `1,036` | **`901`** (`630` tr / `135` val / `136` te) | `135` (`134` unannot. extra + `1` figure) | **`901`** (`6` `train-val` re-enc dups!) | `5a23a5cd2c7b7f4b...` |
| **`DS0006`** | `CAND0007` (`MD-OPG`) | Zenodo `17786082` (`241.16 MiB` `.rar`, MD5 `5ea31f...`) | `510` | **`170`** (`OPG_Image/` pediatric PNGs) | `340` (`170` Smile Zone img + `170` mask) | **`170`** (`0` dups; `66%` black margin) | `18678b82101127c7...` |
| **TOTAL** | **`6` Cohorts** | **All archives/snapshots hash-verified** | **`25,355`** | **`7,789`** | **`17,566`** | **`7,533`** exact + clean | `0` decode errors |

---

## 2. Custody, Linkage Isolation & Backup Readiness

- **Public GitHub (`main`):** Only non-identifying manifests (`DS####_images.csv` with pseudonymous `ImageID`s), aggregate JSON QC stats (`DS####_qc_summary.json`), `T08` dataset cards (`DS####_card.md`), and forensic reports (`DS####_quality.md`).
- **Restricted Off-Git Storage (`03_Datasets/raw/` & `03_Datasets/manifests/*_restricted*`):** Holds unmodified archives, extracted images, XML/JSON source annotations (`<path>` / `imageData` kept off-Git), `DS####_restricted_linkage.csv`, `DS####_restricted_qc.csv`, `DS####_restricted_dups.csv`, and QC contact sheets (`raw/qc_samples/`).
- **Backup Action (`DEC0011`):** Sync `03_Datasets/raw/DS0001–DS0006` + `03_Datasets/manifests/*_restricted*` to **Private Google Drive (`Anik & Mahajub` invite-only)** so raw custody is doubly recoverable prior to `G04` lock.
