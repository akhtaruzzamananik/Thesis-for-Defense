# T08 — Dataset Card: `DS0004` (`CAND0004` — Hanoi Panoramic Periapical Lesions Cohort — Do 2024)

| Metadata | Value |
|---|---|
| TemplateID | T08 |
| template_version | v1.0.0 |
| entity_id | DS0004 |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-18 |
| status | Technical Quality Audited (`STEP-012/013` Batch 2 complete; `G04` awaiting team/dental suitability sign-off) |
| source_inputs | `https://data.mendeley.com/datasets/kx52tk2ddj/3` (`doi:10.17632/kx52tk2ddj.3`); `03_Datasets/licenses/CAND0004_Do2024_CC-BY-4.0.md`; `03_Datasets/manifests/DS0004_images.csv`; `03_Datasets/reports/DS0004_quality.md` |
| governing_section | OS §4.1–4.2; Blueprint STEP-012–013 |
| sensitivity | Public metadata card (`raw/` & `DS0004_restricted_linkage.csv` strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`) |

## Origin/version

- **Archive:** `kx52tk2ddj-3.zip` (`doi:10.17632/kx52tk2ddj.3`, Mendeley Data V3, `2024-04-10`, Hanoi Medical University `Jan 2016 – Mar 2021`, benchmarked in `P0008` Oztekin et al. 2026 & `P0011`).

## access/license/ethics

- **Permission record:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`, `2026-11-17`).
- **License:** Mendeley public API **`CC BY 4.0`** vs article `CC BY-NC 4.0` (conservatively treated as non-commercial academic `CC BY-NC 4.0` + attribution).
- **Ethics:** Retrospective de-identified Hanoi Medical University collection + DIU secondary track (`DEC0003 v6`).

## modality

- `2D OPG` (panoramic dental radiographs; **visually confirmed two X-ray device formats** inside `Original JPG Images`: `2444 × 1292` `Sirona Orthophos XG` AND `2473 × 1252` / `2624 × 1252` `"R RAYSCAN α"` stamps on `DS0004_qc_sheet.jpg`).

## population known/unknown

- Adult dental patients with `>= 1` consensus periapical lesion (`Hanoi Medical University, Vietnam`); age/sex `not reported`.

## collection

- **Total scanned JPGs (`16,995`, `0` decode errors):**
  - `original_jpg_folder` (`Original JPG Images/`): **`3,924`** active unaugmented OPGs -> **`acquired-uninspected`**
  - `augmentation_jpg_folder` (`Augmentation JPG Images/`): **`13,071`** pre-augmented copies (`0` exact SHA overlap with originals) -> **`quarantined-pre-augmented`**
  - *(Note: archive also bundles 3 redundant compressed `.rar` files under `Compressed file/` and `9` orphan XML files without matching JPGs.)*

## patient/image/object counts

- **Active original images:** **`3,924`** (`3,865` unique SHA-256 hashes — **`59` extra exact duplicate files** found even inside `Original JPG Images`!).
- **Lesion annotations (`3,924 / 3,924` matched Pascal VOC `.xml`s, `6,741` boxes):** **`PAI 3 = 4,277`**, **`PAI 4 = 1,755`**, **`PAI 5 = 709`** (`0` missing XML, `0` empty, `0` malformed, `0` OOB, `0` zero-area). Exact match to `P0008 Table 1`.
- **Patient count:** Unknown (`patient IDs omitted at source`, `P0008 p. 34`).

## quality/exclusions

- Audited in `03_Datasets/reports/DS0004_quality.md`: `2316–2636 × 1252–1292` px (`0 < 800`, `0` aspect outliers), `0` sensitive EXIF tags (`3,054` carry standard `"LEAD Technologies Inc. V1.01"` encoder comment; raw `.xml` `<path>` embeds original Windows path `F:\DuLieuRang\...`, never synced to Git), `1` RGB-mode image (`DS0004_IMG_013187`) which is a `corr = 0.9998` duplicate of `DS0004_IMG_016453`.

## duplicates/grouping

- All `13,071` augmented JPGs quarantined cleanly; inside the `3,924` originals, identified **`61` exact SHA-256 duplicate pairs (`59` extra copies)** PLUS **`2` re-encoded identical pairs (`corr >= 0.99, H=0`)** and `1` `corr = 0.9533` pair (`0` true cross-cohort matches vs other 5 cohorts). **Must deduplicate all `61+` clusters BEFORE splitting (`G07`)!**

## annotations

- Pascal VOC `.xml` with 3 ordinal Periapical Index grades (`3 = PAI 3`, `4 = PAI 4`, `5 = PAI 5`); source consensus `>= 2/3` readers at `IoU > 0.80` (`P0008 pp. 4–5`).

## biases

- **Spectrum bias (`0` lesion-free healthy OPGs):** Every retained radiograph has `>= 1` `PAI 3–5` lesion (`P0008 Table 8` proved `37.5%` false positives on healthy windows unless background negatives are handled); missing patient IDs; single center.

## intended use

- Dedicated **`PAI 3–5` small-lesion & tiling sub-track (`RQ2`)** after stripping all `59+` exact/re-encoded duplicates inside `Original JPG Images` (`UD07`); NOT pooled naively into general multi-class restoration/caries sets (`UD04`).

## access/retention

- **Restricted storage:** `03_Datasets/raw/DS0004/` (`archive/` + `extracted/`, `.gitignore`-excluded) + Private Google Drive (`Anik & Mahajub`).
- **Restricted linkage:** `03_Datasets/manifests/DS0004_restricted_linkage.csv` (`.gitignore`-excluded).

## hashes

- **Archive (`kx52tk2ddj-3.zip`):** `8,922,133,584` B (`8.31 GiB`), `md5:3ce4a0a940f8d66eed92aef0e389addb`, `sha256:5be5d9eb3d46dae3b2e68ef3df6f3e8c8e97a7b5231fa7123876e65548794c53`.
- **Public manifest (`DS0004_images.csv`):** `sha256:b05ad87b806e68e3bcebce5e84b47b6f048068cceb6abfdc4ae5d4d70767345c`.
