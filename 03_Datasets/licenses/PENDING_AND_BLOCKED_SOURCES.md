# Blocked, Held & Deferred Candidate License Status (`STEP-011`)

Per **`Blueprint STEP-011` #4** (*"leave denied/pending sources blocked"*) and **`Verification Checklist`** (*"Pending/denied sources cannot proceed"*), the following candidates from `03_Datasets/candidates.csv` remain **BLOCKED from intake/download** at this stage:

| CandidateID | Dataset | License Checked (`STEP-010–011`) | Explicit Block Reason (`Why Blocked from STEP-012`) |
|---|---|---|---|
| `CAND0004` | Hanoi `Do 2024` (`kx52tk2ddj/3`) | **`CC BY 4.0`** (verified via Mendeley API, `Hanoi Medical University`, `2024-04-10`) | **Not selected in primary intake batch** (single condition `PAI 3–5`, `0` healthy OPGs, heavy pre-aug contamination). Remains blocked unless primary multi-class shortlist fails and `DEC0003` expands to `CAND0004`. |
| `CAND0005` | `AU-OPG` (`P0026`) | `CC BY-NC-SA 4.0 / CC BY-NC 4.0` cited | **Blocked (Deferred/Secondary):** Tooth-level OBB + attribute format needs separate schema verification (`UD05`) and host license text check before any download. |
| `CAND0006` | `OPG-233` (`P0031`) | `CC BY 4.0` + `MIT` cited in GitHub | **Blocked (Deferred/Secondary):** Composite origin (`Roboflow` + institutional) and tiny sample size (`233`). |
| `CAND0007` | `MD-OPG` (`Zenodo 17786082`, `P0010`) | **UNDECLARED / Unknown** | **Blocked (License Gap):** Explicit data/code license omitted in publication & GitHub metadata; requires written author clarification before use. |
| `CAND0008` | `Zhang 2023` (`Figshare 21621705`) | `CC0` verified | **Blocked (Ontology Rejection):** `Dental Caries` class merges active caries with fillings (`P0016 p. 4`); prohibited for unedited pathology training (`UD04`). |
| `CAND0009` | `Tufts TDD` (`tdd.ece.tufts.edu`) | **Gated institutional agreement** | **Blocked (Unacquired Agreement):** No request form submitted or signed; lacks multi-class pathology labels natively. |
| `CAND0010` | `Khurshid 2026` (`y7dkrpv7g9.2`) | `CC BY 4.0` + inherited `Tufts` | **Blocked (Composite License + Leakage):** Inherits gated `Tufts` images + admitted pre-split augmentation (`P0006 p. 10`). |
| `CAND0011`–`CAND0014` | `ckt876jzr6.1`, `Adnan 2024`, `P0040/PDCNN`, `Roboflow P0009`, `Kaggle P0002` | Broken / Missing / Intraoral mismatch | **Permanently Excluded (`STEP-010`):** Provenance failure, non-OPG modality (`P0002`), broken link (`P0040`), or narrow scope. |
