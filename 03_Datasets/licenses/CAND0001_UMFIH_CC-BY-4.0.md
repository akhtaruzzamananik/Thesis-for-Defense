# License & Permissions Audit — `CAND0001` (`UMFIH Dental Pathology Dataset`)

| Field | Value |
|---|---|
| CandidateID | `CAND0001` |
| Official Record | `https://zenodo.org/records/15487430` (Concept DOI: `https://doi.org/10.5281/zenodo.15487429`) |
| Origin / Custodian | Department of Maxillofacial Surgery and Radiology, Iuliu Hațieganu University of Medicine and Pharmacy (`UMFIH`), Cluj-Napoca, Romania (`P0023` Mureșanu et al., 2024; `P0015` Eftimie et al., 2025) |
| Declared Repository License | **Creative Commons Attribution 4.0 International (`CC BY 4.0`)** — verified via Zenodo REST API (`access_right: open`, `license.id: cc-by-4.0`, `pub_date: 2025-05-22`) |
| Target Archive Verified (Not Downloaded) | `panoramic_radiography_yolo_dataset_14_classes.zip` — **`1,397,393,531` bytes (`~1.30 GiB`)**, **`md5:18d5acaea021f4f3b05b76e9a27fbd42`** |
| Custody / Acquisition Status | **Technical license verified; awaiting `DEC0003` (`UD03`) confirmation prior to `STEP-012` download** |

## 1. Per-Right Permission Assessment (`Blueprint STEP-011` #1)

| Activity | Permitted by `CC BY 4.0`? | Project Policy & Mandatory Constraints |
|---|---|---|
| **Academic research & training** | **Yes** | Cite `Mureșanu et al. (2024)`, `Eftimie et al. (2025)`, and Zenodo DOI `10.5281/zenodo.15487429`; provide link to `CC BY 4.0`. |
| **Class audit & derivative labels/splits** | **Yes** (Adapt/Transform) | Maintain immutable raw SHA-256 copy; version all cleaned/subsetted `ANN`/`SPLIT` manifests (`P0015` uses 12 classes, `P0023` 13, file says `14_classes`). |
| **Model training & weights release** | **Yes** (`CC BY 4.0`) | No ShareAlike restriction; trained YOLO weights may follow project open research license (`UD20`), never suggesting UMFIH endorsement. |
| **Thesis/paper example figures** | **Yes** (`CC BY 4.0`) | Must verify zero burned-in patient identifiers (`STEP-013` inspection) and follow `OS §9.3` privacy checks. |
| **Hosted defense web demo (`S16`, `UD23`)** | **Yes** (inference showcase) | Only curated, disclosure-verified sample OPGs + research disclaimer; zero storage of uploaded patient images. |
| **Raw image redistribution on public GitHub** | **PROHIBITED BY REPO POLICY** | Although `CC BY 4.0` legally permits redistribution, `OS §10.2` and `DEC0011` strictly forbid pushing medical OPG bytes or archives to public GitHub. Cite Zenodo DOI only. |

## 2. Ethics & Provenance Determination Status

- Source papers (`P0023 p. 2, 10`; `P0015`) document retrospective institutional curation of de-identified adult OPGs (`2021–2023`, `Vatech PCH-2500` + `180` external multi-center OPGs).
- Remaining institutional step (`UD03`): confirm whether DIU/Supervisor requires a local secondary-use/exempt waiver record before `STEP-012` intake (`DEC0003`).
