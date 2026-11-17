# License & Permissions Audit — `CAND0005` (`AU-OPG Ajman University OPG Dataset`)

| Field | Value |
|---|---|
| CandidateID | `CAND0005` |
| Official Records | Paper: `https://doi.org/10.1109/ACCESS.2026.3703711` (`P0026`, Alabd-Aljabar et al., *IEEE Access*, 2026, vol. 14, pp. 90109–90121); Code: `https://github.com/akvnn/guiding-neural-nets`; Dataset: `https://huggingface.co/datasets/YSFF/AU-OPG` |
| Origin / Ethics Approval | Dental Clinic, **Ajman University, UAE** (`Cranex` panoramic unit); **Ajman University Dental Clinic Ethics Committee Approval `Application No. D-F-H-6-Mar`** (`P0026 pp. 1, 4`) |
| Declared License Verified (`2026-11-17`) | Governing *IEEE Access* publication (`P0026 p. 1`) explicitly states: **`"© 2026 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License (CC BY 4.0)"`** and releases `"The dataset and source code... at https://github.com/akvnn/guiding-neural-nets"` (linking directly to `YSFF/AU-OPG`). *Gap noted:* GitHub (`akvnn`) and HuggingFace (`YSFF/AU-OPG` `cardData`) omit a standalone `LICENSE` file/tag, so attribution explicitly binds to the governing `CC BY 4.0` IEEE Access release (`Alabd-Aljabar et al., 2026`). |
| Cohort & Size Verified (`2026-11-17`) | HF `train_annotations.csv` (`4,964` rows, `630` imgs) + `val_annotations.csv` (`1,010` rows, `135` imgs) + `test_annotations.csv` (`1,032` rows, `136` imgs) = **`901` annotated adult OPGs (`7,006` tooth-aligned OBBs)**; HF `dataset/` directory lists `1,000` `.jpg`s (`~1.35 GiB` / `1,353.19 MiB`; reconcile extra `99` unannotated `.jpg`s at `STEP-012/013`). |
| Custody / Acquisition Status | **Authorized for off-Git `STEP-012` intake under expanded 6-dataset `DEC0003` (`2026-11-17`; NOT yet downloaded)** |

## 1. Per-Right Permission Assessment (`Blueprint STEP-011` #1)

| Activity | Permitted? | Project Policy & Mandatory Constraints |
|---|---|---|
| **Academic research & training** | **Yes (`CC BY 4.0` paper grant)** | Cite `Alabd-Aljabar et al. (2026)`, *IEEE Access* `10.1109/ACCESS.2026.3703711`, and `YSFF/AU-OPG`. Retain repo-level missing `LICENSE` file disclosure cleanly. |
| **Geometry conversion (`OBB -> AABB`) & split audit (`UD05/07`)** | **Yes** | Labels use percentage-normalized Label Studio rectangles with clockwise `rotation` (`deg`) covering **`6` diagnoses (`Filled, Crowned, Retained Root, Cavitated, Implant, Impacted`)** + **`4` treatments** (`Extraction, Filling, Root Canal, None`). Verify `OBB -> AABB` round-trip geometry & pre-defined splits (`630/135/136`) vs extra `dataset/` files (`STEP-013`). |
| **Isolated evaluation / track boundary (`UD04`)** | **Yes (Dedicated Track)** | **Critical schema rule:** Only diseased/treated teeth are annotated (`sound teeth remain unannotated background`, `P0026 p. 7`). Do **NOT** mix blindly with lesion-tight (`UMFIH/DENTEX`) boxes without an approved ontology reconciliation (`UD04`, `G05`). |
| **Model weights & defense showcase (`S16`)** | **Yes** | Research showcase only (`UD23` disclaimer); never assert clinical treatment recommendation. |
| **Thesis/paper figures** | **Yes** | Check retained distorted clinical films (`P0026 p. 4`) for any residual header/corner identifiers (`STEP-013`). |
| **Raw images on GitHub** | **PROHIBITED BY REPO POLICY** | Off-Git custody only (`DEC0011`: Local PC `03_Datasets/raw/` + Private Google Drive Anik & Mahajub). |
