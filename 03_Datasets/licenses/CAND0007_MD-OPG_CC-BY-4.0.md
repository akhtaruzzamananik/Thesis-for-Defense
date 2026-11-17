# License & Permissions Audit — `CAND0007` (`MD-OPG Pediatric Mixed Dentition Caries Dataset`)

| Field | Value |
|---|---|
| CandidateID | `CAND0007` |
| Official Records | Dataset: `https://doi.org/10.5281/zenodo.17786082` (Zenodo `17786082`); Code: `https://github.com/IASBS-AI-LAB/MD-OPG`; Paper: `https://doi.org/10.3390/s26082481` (`P0010`, Rahimi et al., *Sensors*, 2026, `26(8)`, `2481`) |
| Origin / IRB Approval | Private dental clinic, **Zanjan, Iran** (`2022–2024`), pediatric mixed dentition (`ages 3–12`, mean `7.2` yrs); **Research Ethics Committees of Zanjan University of Medical Sciences (`IR.ZUMS.REC.1404.242`)** (`P0010 p. 15`) |
| Declared License Verified (`2026-11-17`) | **Zenodo REST API `17786082` explicitly declares `CC BY 4.0`** (`access_right: open`, `pub_date: 2025`); **GitHub repo (`IASBS-AI-LAB/MD-OPG`) declares `MIT License`**; accompanying *Sensors* paper (`P0010`) is MDPI `CC BY 4.0`. *(Earlier `STEP-010` flag of undeclared PDF metadata is resolved cleanly via live Zenodo + GitHub API verification.)* |
| Target Archive Verified (Not Downloaded) | **`MD_OPG.rar`** — **`252,876,370` bytes (`~241.2 MiB`), `md5:5ea31fe4474307f0bdba9591b39574cf`** (`170` PNGs `1920 × 1535` px, `716` Proximal + `179` Occlusal caries polygons + `170` Smile Zone `Z` ROIs) |
| Custody / Acquisition Status | **Authorized for off-Git `STEP-012` intake under expanded 6-dataset `DEC0003` (`2026-11-17`; NOT yet downloaded)** |

## 1. Per-Right Permission Assessment (`Blueprint STEP-011` #1)

| Activity | Permitted? | Project Policy & Mandatory Constraints |
|---|---|---|
| **Academic research & training (`RQ1/RQ2`)** | **Yes (`CC BY 4.0` + `MIT`)** | Cite `Rahimi et al. (2026)`, *Sensors* `26(8)`, `2481`, and Zenodo DOI `10.5281/zenodo.17786082`. |
| **Archive extraction & polygon-to-AABB audit (`UD05`)** | **Yes** | Extract `.rar` using `bsdtar` (`3.8.9` verified locally) cleanly to off-Git `raw/`, preserve original JSON polygons, and verify deterministic tight AABB export (`STEP-013` / `UD05`). |
| **Population boundary (`Pediatric ages 3–12`, `UD04`)** | **Yes (Separate Pediatric Caries Cohort)** | Primary + permanent teeth coexist (`mixed dentition`). Must remain a **distinct pediatric caries evaluation / sub-study cohort** (never silently merged into adult OPG training sets `CAND0001/0002/0005` without explicit age-domain stratification). |
| **Model weights & defense showcase (`S16`)** | **Yes (`CC BY 4.0`)** | Research showcase framing (`UD23` disclaimer). |
| **Thesis/paper visual figures** | **Yes (`CC BY 4.0`)** | Check OPG corners/margins for identifiers at `STEP-013`. |
| **Raw images on GitHub** | **PROHIBITED BY REPO POLICY** | Off-Git custody only (`DEC0011`: Local PC `03_Datasets/raw/` + Private Google Drive Anik & Mahajub). |
