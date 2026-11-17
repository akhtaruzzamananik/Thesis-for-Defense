# T08 — Dataset Card: `DS0005` (`CAND0005` — AU-OPG Ajman University Adult OPG Cohort)

| Metadata | Value |
|---|---|
| TemplateID | T08 |
| template_version | v1.0.0 |
| entity_id | DS0005 |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-17 |
| status | Acquired and Inventoried (`STEP-012` complete; quality/visual audit pending `STEP-013 / G04`) |
| source_inputs | `https://huggingface.co/datasets/YSFF/AU-OPG`; `doi:10.1109/ACCESS.2026.3703711` (`P0026`); `03_Datasets/licenses/CAND0005_AU-OPG_CC-BY-4.0.md`; `03_Datasets/manifests/DS0005_images.csv` |
| governing_section | OS §4.1–4.2; Blueprint STEP-012 |
| sensitivity | Public metadata card (`raw/` & `DS0005_restricted_linkage.csv` strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`) |

## Origin/version

- **Upstream snapshot:** `huggingface:YSFF/AU-OPG` (`main` branch mirrored `2026-11-17`, accompanied by `github.com/akvnn/guiding-neural-nets` and `P0026` *IEEE Access* 2026, vol. 14, pp. 90109–90121).

## access/license/ethics

- **Permission record:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`, `2026-11-17`).
- **License:** *IEEE Access* paper (`P0026 p. 1`) explicitly grants **`CC BY 4.0`** (`Creative Commons Attribution 4.0 License`); repo metadata lacks a standalone `LICENSE` tag (explicitly disclosed in `CAND0005_AU-OPG_CC-BY-4.0.md`).
- **Ethics:** **Ethics Committee of the Dental Clinic, Ajman University, UAE (`Application No. D-F-H-6-Mar`)** (`P0026 pp. 1, 4`).

## modality

- `2D OPG` (`Cranex` panoramic X-ray unit; `1,035` `.jpg`s in `dataset/` + `1` sample `.png`; mixed `RGB` `1,019` and `RGBA` `17` decoded in inventory).

## population known/unknown

- Adult dental clinic patients (`Ajman University, UAE`); pediatric, edentulous, and serial radiographs excluded at curation; distorted clinical adult OPGs retained (`P0026 pp. 4–5`). Age/sex distributions `not reported`.

## collection

- **Total scanned images (`1,036`, `0` decode errors):**
  - `train_annotated` (`train_annotations.csv`): **`630`** unique OPGs (`4,964` tooth rows) -> `acquired-uninspected`
  - `val_annotated` (`val_annotations.csv`): **`135`** unique OPGs (`1,010` tooth rows) -> `acquired-uninspected`
  - `test_annotated` (`test_annotations.csv`): **`136`** unique OPGs (`1,032` tooth rows) -> `acquired-uninspected`
  - `unannotated_extra_in_dataset`: **`134`** extra `.jpg`s inside HF `dataset/` not referenced in the 3 CSVs -> `quarantined-unannotated-extra` (reconcile in `STEP-013`!)
  - `readme_sample_figure`: `1` root `sample_with_ground_truth.png` -> `quarantined-sample-figure`.

## patient/image/object counts

- **Total scanned:** `1,036` (`901` active annotated OPGs + `135` quarantined unannotated/figure images + `0` errors).
- **Unique SHA-256 hashes:** `1,036` (`901` unique inside active CSV-referenced set; `0` exact duplicates).
- **Patient count:** Unknown (`patient IDs stripped; serial radiographs excluded at curation`, `P0026 p. 4`, so `~1 OPG/patient` intended yet unverified).

## quality/exclusions

- Pending `STEP-013 / G04` inspection (`0` decode errors; all `1,036` LFS files verified byte-for-byte against HuggingFace `lfs.oid` SHA-256).

## duplicates/grouping

- `0` exact SHA-256 duplicates across all `1,036` files; pre-defined `630 / 135 / 136` splits and the `134` extra unannotated `dataset/` images must undergo perceptual near-duplicate screening in `STEP-013 / G07`.

## annotations

- **CSV schema (`7,006` tooth rows across `901` OPGs):** Label Studio percentage-based rectangle (`x, y, width, height`) + clockwise `rotation` (`degrees`), paired with `6` diagnoses (`Filled, Crowned, Retained Root, Cavitated, Implant, Impacted`) and `4` treatments (`None, Extraction, Filling, Root Canal`). Healthy/untargeted teeth are **not annotated** (`P0026 p. 7`).

## biases

- Single OMFR reviewer (`> 20` yrs) corrected graduate labels without `κ`; sound teeth act as detector background (`P0026 pp. 7, 12`); minority treatment classes (`Filling`, `Root Canal`) are sparse (`263`, `326`).

## intended use

- Dedicated adult tooth-level `OBB -> AABB` sub-track & harmonized comparison (kept isolated from lesion-tight exhaustive cohorts unless reconciled under `UD04–UD05`).

## access/retention

- **Restricted storage:** `03_Datasets/raw/DS0005/extracted/` (`.gitignore`-excluded) + Private Google Drive (`Anik & Mahajub`).
- **Restricted linkage:** `03_Datasets/manifests/DS0005_restricted_linkage.csv` (`.gitignore`-excluded).

## hashes

- **Total mirrored bytes (`1,041` verified HF files):** `1,471,815,794` bytes (`~1.37 GiB`; per-file LFS `sha256` verified at fetch).
- **Public manifest (`DS0005_images.csv`):** `sha256:5a23a5cd2c7b7f4b981871447ef3aef657da1d54f94e8b7c9d8c7b0810041478`.
