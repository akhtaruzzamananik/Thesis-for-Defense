# License & Permissions Audit — `CAND0003` (`Dental OPG X-RAY Dataset — Dhaka, Bangladesh`)

| Field | Value |
|---|---|
| CandidateID | `CAND0003` |
| Official Record | `https://data.mendeley.com/datasets/c4hhrkxytw/4` (`doi:10.17632/c4hhrkxytw.4`, Mendeley Data V4, published `2024-08-27`) |
| Accompanying Article (`P0024`) | Rahman et al. (2024), *Data in Brief*, 57, 110970 (`doi:10.1016/j.dib.2024.110970`) |
| Origin / Ethics Approval | 3 private clinics in Banani & Dhanmondi, Dhaka (`Prescription Point`, `LabAid`, `Ibn Sina`); Mendeley affiliation: AIUB (`ROR 02j8ga255`); Local Ethics: **Bangladesh Dental College & Hospital (`Protocol No: MK-198109`)** (`P0024 p. 13`) |
| Declared License | **Mendeley API `data_licence`: `CC BY 4.0`** (`Creative Commons Attribution 4.0 International`); *Data in Brief* article text notes **`CC BY-NC 4.0`** (`P0024.md line 87`) |
| Target Archive Size (Not Downloaded) | `~197 MB` `.zip` (`P0024 p. 2`) |
| Custody / Acquisition Status | **Technical license verified (treated conservatively as non-commercial academic `CC BY-NC 4.0` + `CC BY 4.0` attribution); awaiting `DEC0003` (`UD03`)** |

## 1. Per-Right Permission Assessment (`Blueprint STEP-011` #1)

| Activity | Permitted? | Project Policy & Mandatory Constraints |
|---|---|---|
| **Academic research & cross-cohort evaluation (`RQ1/RQ2`)** | **Yes** | Permitted under both `CC BY 4.0` and `CC BY-NC 4.0` with citation (`Rahman et al., 2024`, Mendeley DOI + *Data in Brief*). |
| **Deduplication / discarding pre-split Roboflow copies (`UD07`)** | **Yes** | **Mandatory intake rule:** Discard `558` pre-split augmented training images in archive and retain ONLY **`232` original OPGs** (`1,204` boxes). |
| **Model weights & defense web demo (`S16`)** | **Yes (non-commercial research demo)** | Strictly non-commercial research-showcase framing (`UD23` disclaimer). |
| **Thesis/paper visual examples** | **Yes** | Check smartphone-photographed film edges for any hospital stamp/margin identifiers before rendering (`STEP-013` visual QA). |
| **Raw images on GitHub / public links** | **PROHIBITED BY REPO POLICY** | Off-Git storage only (`DEC0011`: Local PC `03_Datasets/raw/` + Private Google Drive Anik & Mahajub). |
