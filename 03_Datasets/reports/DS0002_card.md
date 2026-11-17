# T08 — Dataset Card: `DS0002` (`CAND0002` — DENTEX MICCAI 2023 Benchmark)

| Metadata | Value |
|---|---|
| TemplateID | T08 |
| template_version | v1.0.0 |
| entity_id | DS0002 |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-18 |
| status | Technical Quality Audited (`STEP-012/013` Batch 2 complete; `G04` awaiting team/dental suitability sign-off) |
| source_inputs | `https://zenodo.org/records/7812323` (`doi:10.5281/zenodo.7812323`, `arXiv:2305.19112`); `03_Datasets/licenses/CAND0002_DENTEX_terms.md`; `03_Datasets/manifests/DS0002_images.csv`; `03_Datasets/reports/DS0002_quality.md` |
| governing_section | OS §4.1–4.2; Blueprint STEP-012–013 |
| sensitivity | Public metadata card (`raw/` & `DS0002_restricted_linkage.csv` strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`) |

## Origin/version

- **Archives:** `training_data.zip` + `validation_data.zip` (`Zenodo 7812323`, release `2023-04-09`, `Hamamci et al., 2023`, `arXiv:2305.19112`, used in `P0014` & `P0036`).

## access/license/ethics

- **Permission record:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`, `2026-11-17`).
- **License (`divergence retained`):** Neither `training_data.zip` nor `validation_data.zip` embeds an in-archive `LICENSE` or `README` file. Official Zenodo API declares `CC BY 4.0`, whereas HuggingFace mirror `ibrahimhamamci/DENTEX` declares `CC-BY-NC-SA-4.0`. Conservatively track non-commercial ShareAlike (`NC-SA`) obligations separately from pure `CC BY 4.0` tracks (`UD20`).
- **Ethics:** Multi-institutional retrospective de-identified Turkish OPGs (`age >= 12`, `arXiv:2305.19112`).

## modality

- `2D OPG` (panoramic dental radiographs; `.png` files, `100%` grayscale-identical `RGB`, `0` tinted files).

## population known/unknown

- Turkish clinical patients (`age >= 12` years, `arXiv:2305.19112`); per-image age/sex `not reported`.

## collection

- **Total scanned PNGs across both Zenodo archives (`3,654`, `0` decode errors):**
  - `training_quadrant_enumeration_disease`: **`705`** labeled disease OPGs -> **`acquired-uninspected`**
  - `validation_quadrant_enumeration_disease_no_gt`: **`50`** unlabeled challenge-validation OPGs -> **`acquired-uninspected`**
  - `training_quadrant_only`: `693` PNGs (`277` SHA overlap with `705` active) -> **`quarantined-no-disease-labels`**
  - `training_quadrant_enumeration_only`: `634` PNGs (`278` SHA overlap with `705` active) -> **`quarantined-no-disease-labels`**
  - `training_unlabelled_xrays`: `1,571` unlabeled PNGs -> **`quarantined-unlabeled-pool`**
  - `validation_ipynb_checkpoint` (`.ipynb_checkpoints/` inside `validation_data.zip`): `1` leftover author checkpoint PNG -> **`quarantined-author-checkpoint`**.

## patient/image/object counts

- **Total active (`disease` track):** **`755`** PNGs (`705` JSON-labeled train + `50` unlabeled val; `755` unique SHA-256 hashes).
- **Labeled disease instances (`train_quadrant_enumeration_disease.json`, `3,529` boxes):**
  - **`Caries`: `2,189` (`62.0%`)**
  - **`Impacted`: `604` (`17.1%`)**
  - **`Deep Caries`: `578` (`16.4%`)**
  - **`Periapical Lesion`: `158` (`4.5%`)**
  - *(Critical correction: earlier secondary literature counts `823 / 799 / 965 / 942` were actually `Q1–Q4` tooth-quadrant counts, NOT balanced disease classes!)*
- **Patient count:** Unknown (`patient IDs omitted`).

## quality/exclusions

- Audited in `03_Datasets/reports/DS0002_quality.md`: `1976–3139` px wide (`0 < 800`), `0` aspect outliers (`1.60–2.33`), `0` sensitive EXIF tags, minor `"VistaPano"` / `"R/L"` stamps; **one severe horizontal sensor-streak artifact on `DS0002_IMG_000641` (`DS0002_qc_sheet.jpg`)** flagged for awareness (retain unless explicit clinical exclusion approved before training).

## duplicates/grouping

- **`0` exact SHA-256 duplicates** and **`0` pixel-verified near-duplicates (`corr >= 0.90` across all `25` `dHash <= 4` hits)** inside the `755` active disease OPGs. Check cross-overlap with quarantined `unlabelled`/`quadrant` only if any quarantined unlabeled subset is ever activated later.

## annotations

- COCO JSON (`bbox`, polygon `segmentation`, `category_id_1` quadrant, `category_id_2` FDI tooth, `category_id_3` disease); `0` OOB boxes, `0` zero-area boxes; annotator credentials/`κ` undisclosed (`P0014 p. 3` -> requires dental QA spot-check at `G05/G06`).

## biases

- Heavy class imbalance (`2,189` Caries vs `158` Periapical Lesion); validation `50` OPGs lack public GT JSON (must split labeled `705` via `70/15/15` under `UD08`); `VistaPano` artifact case present; no restoration classes.

## intended use

- `4`-pathology contrast-tier benchmark (`Caries, Deep Caries, Impacted, Periapical Lesion`, `RQ1`) or harmonized pathology sub-track after `G05/G06` dental QA check.

## access/retention

- **Restricted storage:** `03_Datasets/raw/DS0002/` (`archive/` + `extracted/`, `.gitignore`-excluded) + Private Google Drive (`Anik & Mahajub`).
- **Restricted linkage:** `03_Datasets/manifests/DS0002_restricted_linkage.csv` (`.gitignore`-excluded).

## hashes

- `training_data.zip`: `10,927,391,529` B, `md5:eba0c44fa4c6e8ec221db3009eccc1f9`, `sha256:18b2a2dbc5a2b10b0cc6a7677c46a382f4709ab8c9c3bb94f57b74e38e11ffd3`.
- `validation_data.zip`: `149,512,256` B, `md5:b2a13267740185e42cb59e968bc3ce83`, `sha256:6370bb4f1024bd610cde13242a465cb2eff195fc02f56ac22126555e7edc7bc3`.
- `DS0002_images.csv`: `sha256:fb268930e339b90dc70f24a1abaf67c72be4250b1e7fe4f7260c78a4e9a16086`.
