# License & Permissions Audit — `CAND0002` (`DENTEX Benchmark`)

| Field | Value |
|---|---|
| CandidateID | `CAND0002` |
| Official Zenodo Record | `https://zenodo.org/records/7812323` (`doi:10.5281/zenodo.7812323`, Concept DOI `10.5281/zenodo.7812322`; challenge release `2023-04-09`, `arXiv:2305.19112`) |
| Known Mirror Checked | HuggingFace `ibrahimhamamci/DENTEX` |
| Origin / Custodian | Ibrahim Ethem Hamamci et al. (MICCAI 2023 DENTEX Challenge; Turkish multi-institution retrospective adult/≥12y OPGs) |
| **License Divergence Flagged!** | **Zenodo API `7812323` reports `cc-by-4.0`** (`access_right: open`), **whereas HuggingFace mirror lists `CC-BY-NC-SA-4.0`** (`NonCommercial ShareAlike`) |
| Target Archives Verified (Not Downloaded) | `training_data.zip` (**`10,927,391,529` bytes ≈ `10.18 GiB`**, `md5:eba0c44fa4c6e8ec221db3009eccc1f9`) + `validation_data.zip` (**`149,512,256` bytes ≈ `142.6 MiB`**, `md5:b2a13267740185e42cb59e968bc3ce83`) |
| Custody / Acquisition Status | **Held pending conservative `NC-SA` reconciliation, `10.32 GiB` storage confirmation, and `DEC0003` (`UD03`)** |

## 1. Per-Right Permission Assessment (`Blueprint STEP-011` #1)

Because the HuggingFace release declares `CC-BY-NC-SA-4.0` while official Zenodo `7812323` declares `CC BY 4.0`, **`STEP-011` applies the stricter `CC-BY-NC-SA-4.0` terms conservatively until in-archive `LICENSE/README` text is inspected**:

| Activity | Permitted? | Mandatory Constraints & Conflict Warnings |
|---|---|---|
| **Non-commercial academic research (FYDP)** | **Yes** | Explicitly permitted under both `CC BY 4.0` and `CC-BY-NC-SA-4.0` with citation (`Hamamci et al., 2023`, `arXiv:2305.19112`). |
| **Annotation audit / label cleaning (`UD04/06`)** | **Yes** | Derived annotation splits/corrections must carry attribution and ShareAlike notice if distributed (`SA` constraint if `NC-SA` governs). |
| **Model weights & public demo hosting (`S16`)** | **Conditional (`NC-SA` Caution)** | Allowed for **strictly non-commercial defense demonstration**; **ShareAlike (`SA`)** must be checked before choosing downstream code/weight release license (`UD20`), and commercial hosting tiers avoided. |
| **Publication example figures** | **Yes** | Non-commercial thesis/paper examples permitted after verifying zero residual PHI (`STEP-013`). |
| **Raw archive on GitHub / public cloud** | **PROHIBITED** | Strictly excluded by `OS §10.2`, `DEC0011`, and `.gitignore`; note `10.32 GiB` footprint exceeds lightweight workspace expectations unless Colab/Kaggle direct pull or selective `training_data` check is justified at `UD02/UD03`. |

## 2. Ethics & Provenance Notes

- `arXiv:2305.19112` notes institutional ethics approvals in Türkiye and de-identified selection (`age >= 12`); `P0014` (`p. 3`) warns labeler credentials and `κ` are undisclosed (`G05/G06` dental review mandatory if selected).
