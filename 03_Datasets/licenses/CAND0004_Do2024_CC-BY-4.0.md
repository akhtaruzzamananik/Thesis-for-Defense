# License & Permissions Audit — `CAND0004` (`Hanoi Panoramic Periapical Lesions Dataset — Do 2024`)

| Field | Value |
|---|---|
| CandidateID | `CAND0004` |
| Official Record | `https://data.mendeley.com/datasets/kx52tk2ddj/3` (`doi:10.17632/kx52tk2ddj.3`, Mendeley Data V3, published `2024-04-10`) |
| Origin / Custodian | Hanoi Medical University, Hanoi, Vietnam (`Jan 2016 – Mar 2021`, `Sirona Orthophos XG`, `235 dpi`, `~2444 × 1292` px; externally benchmarked in `P0008` Oztekin et al. 2026 & `P0011`) |
| Declared License | **Mendeley Public API `data_licence`: `CC BY 4.0`** (`Creative Commons Attribution 4.0 International`); accompanying Do et al. release notes cite `CC BY-NC 4.0` -> **conservatively treated as non-commercial academic `CC BY-NC 4.0` + `CC BY 4.0` attribution** |
| Cohort & Layout Verified (`2026-11-17`) | Description reports `3,926` original panoramic radiographs (`3,924` consensus-verified lesion-bearing originals with `6,741` `PAI 3–5` boxes retained in `P0008`) organized into `Original JPG Images`, `Augmentation JPG Images`, and `Image Annotations` (augmented expansion up to `16,519–17,004` files; direct zip pull tested via Mendeley UI/API during `STEP-012`) |
| Custody / Acquisition Status | **Authorized for off-Git `STEP-012` intake under expanded 6-dataset `DEC0003` (`2026-11-17`; NOT yet downloaded)** |

## 1. Per-Right Permission Assessment (`Blueprint STEP-011` #1)

| Activity | Permitted? | Project Policy & Mandatory Constraints |
|---|---|---|
| **Non-commercial academic research (`FYDP` / `RQ2` tiling track)** | **Yes** | Cite Mendeley DOI `10.17632/kx52tk2ddj.3` and original Do et al. release; provide `CC BY 4.0` / `CC BY-NC 4.0` attribution. |
| **Deduplication & isolation of originals (`UD07`)** | **Yes** | **Mandatory intake rule:** Strictly separate `Original JPG Images` (`~3,924`) from `Augmentation JPG Images` (`16,519–17,004`) and run SHA-256 + near-duplicate checks (`P0008` protocol) before any split (`G07`). |
| **Separate single-condition / `PAI 3–5` tiling study (`UD04`)** | **Yes (Dedicated Track)** | Contains **`PAI 3`, `PAI 4`, `PAI 5` periapical lesions only** and **`0` healthy/lesion-free OPGs** (`spectrum bias`). Do **NOT** mix blindly into general multi-class training splits (`CAND0001`/`CAND0002`); analyze as a dedicated small-lesion / ordinal-periapical sub-track or periapical-compatible evaluation with explicit background-tile checks (`P0008 Table 8`). |
| **Model weights & non-commercial defense showcase (`S16`)** | **Yes** | Strictly non-commercial research weights/demo framing (`UD23` disclaimer). |
| **Thesis/paper visual figures** | **Yes** | Visually inspect film edges for clinic/scanner stamps or patient text (`STEP-013`) before selecting figures. |
| **Raw images on GitHub / public links** | **PROHIBITED BY REPO POLICY** | Off-Git custody only (`DEC0011`: Local PC `03_Datasets/raw/` + Private Google Drive Anik & Mahajub). |

## 2. Ethics & Provenance Notes

- Retrospective de-identified clinical collection from Hanoi Medical University (`2016–2021`); Mendeley public repository explicitly marks public `CC BY 4.0` availability.
- Missing patient IDs at source (`P0008 p. 34`) must remain explicitly disclosed in `UD07` / thesis limitations (`radiograph-level independence verified; cross-visit patient overlap unverified`).
