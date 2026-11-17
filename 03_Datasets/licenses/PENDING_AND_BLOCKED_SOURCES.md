# Blocked, Held & Excluded Candidate License Status (`STEP-011`)

Per **`Blueprint STEP-011` #4** (*"leave denied/pending sources blocked"*) and **`Verification Checklist`** (*"Pending/denied sources cannot proceed"*), the following candidates from `03_Datasets/candidates.csv` remain **BLOCKED from `STEP-012` intake/download** after expanding `DEC0003` to the **6 live open-licensed `2D OPG` datasets (`CAND0001, CAND0002, CAND0003, CAND0004, CAND0005, CAND0007`)**:

| CandidateID | Dataset | Live Status Checked (`2026-11-17`) | Explicit Block Reason (`Why Blocked from STEP-012`) |
|---|---|---|---|
| **`CAND0006`** | `OPG-233` (`simzhangbest/opg233-benchmark`, `P0031`) | Code `MIT` live on GitHub; **Dataset Zenodo deposit NOT PUBLISHED YET** | **Blocked (Unpublished Source Archive):** Live GitHub `README.md` still prints **`> [ZENODO_DOI_URL] (placeholder — replace with the published DOI)`** and `doi = {<ZENODO_DOI>}`, matching `P0031 p. 16` (*Article in Press — "will be released upon acceptance"*). Zenodo search confirms no `OPG-233` record exists yet (`2026-11-17`). Cannot be downloaded until authors publish the live Zenodo DOI. |
| `CAND0008` | `Zhang 2023` (`Figshare 21621705`) | `CC0` verified | **Blocked (Ontology Rejection):** `Dental Caries` class merges active caries with fillings (`P0016 p. 4`) plus bite-block artifacts (`P0030`); prohibited for unedited pathology training (`UD04`, `research_questions.md §1`). |
| `CAND0009` | `Tufts TDD` (`tdd.ece.tufts.edu`) | **Gated institutional agreement** | **Blocked (Unacquired Agreement):** No request form submitted or signed; lacks multi-class pathology labels natively. |
| `CAND0010` | `Khurshid 2026` (`y7dkrpv7g9.2`) | `CC BY 4.0` + inherited `Tufts` | **Blocked (Composite License + Leakage):** Inherits gated `Tufts` images + admitted pre-split augmentation (`P0006 p. 10`) + non-radiographic `RR clinical`. |
| `CAND0011`–`CAND0014` | `ckt876jzr6.1`, `Adnan 2024`, `P0040/PDCNN`, `Roboflow P0009`, `Kaggle P0002` | Broken / Missing / Intraoral mismatch | **Permanently Excluded (`STEP-010`):** Provenance failure, non-OPG modality (`P0002` intraoral RGB), broken link (`P0040`), or narrow scope (`Adnan` teeth-only). |

*(Note: `CAND0007 MD-OPG` moved OUT of this block list into Authorized after live Zenodo REST API `17786082` + GitHub `IASBS-AI-LAB/MD-OPG` verified explicit `CC BY 4.0` + `MIT` licensing and `IR.ZUMS.REC.1404.242` IRB approval on `2026-11-17`.)*
