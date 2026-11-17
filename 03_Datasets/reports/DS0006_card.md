# T08 — Dataset Card: `DS0006` (`CAND0007` — MD-OPG Pediatric Mixed Dentition Caries Cohort)

| Metadata | Value |
|---|---|
| TemplateID | T08 |
| template_version | v1.0.0 |
| entity_id | DS0006 |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-17 |
| status | Acquired and Inventoried (`STEP-012` complete; quality/visual audit pending `STEP-013 / G04`) |
| source_inputs | `https://doi.org/10.5281/zenodo.17786082` (Zenodo `17786082`); `doi:10.3390/s26082481` (`P0010`); `03_Datasets/licenses/CAND0007_MD-OPG_CC-BY-4.0.md`; `03_Datasets/manifests/DS0006_images.csv` |
| governing_section | OS §4.1–4.2; Blueprint STEP-012 |
| sensitivity | Public metadata card (`raw/` & `DS0006_restricted_linkage.csv` strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`) |

## Origin/version

- **Archive:** `MD_OPG.rar` (`doi:10.5281/zenodo.17786082`, Zenodo `2025` release accompanying `P0010` Rahimi et al., *Sensors*, 2026, `26(8)`, `2481`, + `github.com/IASBS-AI-LAB/MD-OPG`).

## access/license/ethics

- **Permission record:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`, `2026-11-17`).
- **License:** Zenodo REST API **`CC BY 4.0`** + GitHub repo **`MIT License`** + *Sensors* `CC BY 4.0`.
- **Ethics:** **Research Ethics Committees of Zanjan University of Medical Sciences (`IR.ZUMS.REC.1404.242`)** (`P0010 p. 15`).

## modality

- `2D OPG` (pediatric mixed-dentition panoramic radiographs, `1920 × 1535` px `.png`s; `RGB` full radiographs + `L` binary segmentation masks).

## population known/unknown

- Pediatric patients ages **`3–12` years** (mean `7.2`, `50%` female / `50%` male, Persian/Turkic ethnicity) at a single private clinic in Zanjan, Iran (`2022–2024`, `P0010 pp. 4–5`).

## collection

- **Total scanned image files inside `MD_OPG.rar`:** **`510` `.png`s (`0` decode errors)** + `170` LabelMe-style `.json` annotation files (`OPG_Annotation/P_###_Ann_.json`):
  - `opg_original` (`MD_OPG/OPG_Image/`): **`170`** full `2D OPG` `.png`s -> **`acquired-uninspected`**
  - `smile_zone_crop` (`MD_OPG/Smile_Zone_IMG/`): `170` cropped ROI `.png`s -> **`quarantined-derived-crop`**
  - `smile_zone_mask` (`MD_OPG/Smile_Zone_MSK/`): `170` binary masks -> **`quarantined-derived-mask`**.

## patient/image/object counts

- **Total scanned:** `510` image files (`170` active original full pediatric OPGs + `340` quarantined derived crops/masks + `0` errors).
- **Unique SHA-256 hashes:** `170` across active `opg_original` (`510` total across all files, `0` duplicates).
- **Patient count:** Reported `170` pediatric OPGs at OPG/patient level (`P0010 p. 9`; explicit PatientIDs omitted in public release).

## quality/exclusions

- Pending `STEP-013 / G04` inspection (`0` decode errors; JSON polygon geometry & Smile Zone conversion audit scheduled in `STEP-013`).

## duplicates/grouping

- `0` exact SHA-256 duplicates across active `170` OPGs; derived `Smile_Zone_IMG` and `Smile_Zone_MSK` quarantined cleanly to prevent double-counting.

## annotations

- LabelMe-schema JSON polygons (`shapes` with `label`, `points`, `shape_type`, verified sample `P_001_Ann_.json`: `polygon` `'p'`) covering `716` Proximal caries, `179` Occlusal caries, and `170` Smile Zone `Z` ROIs (`P0010 Table 1`).

## biases

- Single private clinic (`N = 170`), single-pathology focus (`caries` only, `80/20` proximal/occlusal skew), and **mixed dentition (`ages 3–12`)** anatomical difference from adult OPG cohorts (`CAND0001/0002/0005`). Keep as a distinct pediatric caries cohort.

## intended use

- Dedicated **pediatric mixed-dentition caries detection sub-track** (`RQ1/RQ2` conversion of polygons to tight AABBs under `UD04–UD05`), kept separate from adult benchmarks.

## access/retention

- **Restricted storage:** `03_Datasets/raw/DS0006/` (`archive/MD_OPG.rar` + `extracted/`, `.gitignore`-excluded) + Private Google Drive (`Anik & Mahajub`).
- **Restricted linkage:** `03_Datasets/manifests/DS0006_restricted_linkage.csv` (`.gitignore`-excluded).

## hashes

- **Archive (`MD_OPG.rar`):** `252,876,370` bytes (`~241.16 MiB`), `md5:5ea31fe4474307f0bdba9591b39574cf` (matches Zenodo API!), `sha256:e793edead90a62fe2b54d6d01a5612a586d23aef91233ae3de7d7ca7fbe81d07`.
- **Public manifest (`DS0006_images.csv`):** `sha256:18678b82101127c70358b5fba0418b007e4f7ad61113685cd3d6b90a1ee77c00`.
