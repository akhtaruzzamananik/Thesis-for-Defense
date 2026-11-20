# DIU CSE B.Sc. Thesis Submission Record & Immutable Checksum Ledger (`STEP-043`)

| Field | Value |
|---|---|
| Step / Stage | `STEP-043` (`S14` — Submit the thesis and preserve the exact submission) |
| Bundle ID | `SUBBUNDLE_DIU_CSE_THESIS_v1.0.0` ([submission_bundle_manifest.json](./submission_bundle_manifest.json)) |
| Institution | Department of Computer Science & Engineering (CSE), Daffodil International University (DIU) |
| Thesis Title | *A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO* |
| Authorized Submitters | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor) & Israt Jahan (Co-supervisor) |
| Bundle File Count / Size | `33` verified files (`705,585` bytes) |
| Bundle Merkle `SHA-256` | `91afff083678781b0c925e8f63466f202db8ce40951d53c6168c9ecbbbbfa75b` |
| **Current Submission State** | **`READY_AWAITING_G15_AND_PORTAL_UPLOAD`** *(Pre-submission bundle & checksums locked; actual institutional upload awaits `G15 PASS` supervisor sign-off)* |

> [!IMPORTANT]
> **Strict Non-Fabrication Policy (`STEP-043`):** Per `OPG_PROJECT_EXECUTION_BLUEPRINT.md` (`STEP-043`, lines 2606–2626), preparing or compiling local files must **never** be labeled `CONFIRMED_SUBMITTED`. This ledger explicitly separates **`1. READY_AWAITING_G15_AND_PORTAL_UPLOAD`**, **`2. SENT_OR_UPLOADED`**, and **`3. CONFIRMED_SUBMITTED`**.

---

## 1. Three-Stage Institutional Submission State Tracker

| Stage | State Code | Criteria | Current Status |
|---|---|---|---|
| **Stage 1** | `READY_AWAITING_G15_AND_PORTAL_UPLOAD` | All `33` thesis, slide, figure, table, BibTeX & audit files compiled, verified (`STEP-041/042 PASS`), and SHA-256 hashed (`assembled_manifest.json` match verified). | **ACTIVE (`2026-11-21`)** |
| **Stage 2** | `SENT_OR_UPLOADED` | Supervisor Ms Faiza Feroz approves `G15 -> PASS`, final PDF exported from `DIU_CSE_Thesis_Assembled_v1.0.0.html`, and uploaded/delivered to DIU CSE portal/office. | *Pending human action* |
| **Stage 3** | `CONFIRMED_SUBMITTED` | Actual DIU portal confirmation / signed departmental receipt / supervisor email confirmation received and archived in off-Git restricted storage. | *Pending human action* |

---

## 2. Institutional Receipt & Confirmation Block (Fill Upon Actual DIU Submission)

- **Prerequisite Gate (`GA0015` / `G15`):** Must be promoted from `HOLD` -> `PASS` in `01_Project_Management/gates.csv` after Supervisor Ms Faiza Feroz signs `11_Writing/reviews/supervisor_review_ledger.md`.
- **Actual Submission Date (`YYYY-MM-DD`):** `[Pending actual DIU submission]`
- **Submission Destination (e.g., DIU BLC / CSE Thesis Portal / DSpace / Dept. Office):** `[Pending actual DIU submission]`
- **Submitted By (Authorized Researcher):** `[Akhtaruzzaman Anik (232-15-252) / Mahajub Al Shabah (232-15-900)]`
- **Receipt / Confirmation Reference ID:** `[Pending actual receipt — NEVER fabricate]`
- **Off-Git Receipt File Location (PDF/Screenshot):** `15_Archive/restricted_receipts/[pending_receipt_file]` *(kept off-Git per privacy policy)*
- **Submitted PDF `SHA-256` (Exported from `DIU_CSE_Thesis_Assembled_v1.0.0.html`):** `[Record exact SHA-256 of final exported PDF at upload time]`

---

## 3. Immutable Submission Bundle Checksum Table (`33` Verified Files)

| # | Relative Path | Size (Bytes) | `SHA-256` Digest |
|---:|---|---:|---|
| `1` | `11_Writing/thesis/DIU_CSE_Thesis_Assembled_v1.0.0.md` | `119,276` | `621fd7c2cea07a6258a08e74c512e5938febcc2054310a467ca641ea815988d6` |
| `2` | `11_Writing/thesis/DIU_CSE_Thesis_Assembled_v1.0.0.html` | `264,817` | `4aa968371dd18ecbc35f3e0352fcc4f128693e24533e23749bba3907c6c37d2e` |
| `3` | `11_Writing/slides/defense_slides.md` | `15,149` | `c9b6bae2a3ade4477a0d7c3c9aff236311a2c99f1eaaeacc246b2d2934a28ef0` |
| `4` | `11_Writing/thesis/00_front_matter_and_abstract.md` | `9,535` | `18ebb9c405dba69165406a8b1006ecc2a9adfec498dc69be28c8b294ed139134` |
| `5` | `11_Writing/thesis/01_chapter1_introduction.md` | `9,177` | `6bf532bacf6aa5a14da50e5fa747cd82dce5a28d7d2a338cf5747b444772f358` |
| `6` | `11_Writing/thesis/02_chapter2_literature_review.md` | `10,344` | `9cfde8fa6b5f9bca8c19006c75fc73afc4952bfe9728a01bef978c8bd6e5b1b7` |
| `7` | `11_Writing/thesis/03_chapter3_methodology.md` | `10,173` | `8d8547b8ff3b9a8ed0fae5f87b1461248115a5d6aa1de11aab6970afeca99791` |
| `8` | `11_Writing/thesis/04_chapter4_results.md` | `24,444` | `41810990222b0e12d5d9303ecc951c0c3d88c3c4d88571a64089954e5be5ce15` |
| `9` | `11_Writing/thesis/05_chapter5_discussion_and_prototype.md` | `16,723` | `102e75e185dfc871130544765c75f4fa93ac942a0e3cfae00ab5d16fa1f542f8` |
| `10` | `11_Writing/thesis/06_chapter6_conclusion.md` | `7,953` | `044bc631129962a5d400463f4ced9d233bf4be86384ab22a606f00ee73b84ae9` |
| `11` | `11_Writing/thesis/07_appendices.md` | `14,740` | `9063c57695e52ddfcf558d6a27cff8c16fb12dec537d05bf0f5062bcff1326cd` |
| `12` | `10_Figures_Tables/figures/FIG0001_study_pipeline.svg` | `10,007` | `35a778e6ff8229661f83205b6e109bc27f7c5a3b88a2301dc7dd61a466b42f80` |
| `13` | `10_Figures_Tables/figures/FIG0002_heldout_scoreboard_ci.svg` | `15,248` | `136a922d01ad9a430b6051649415fc3fe0dfbc7da8ca210ef63fc700b20c96d8` |
| `14` | `10_Figures_Tables/figures/FIG0003_rq2_clahe_vs_1280.svg` | `9,432` | `5a53ff18a3284f0331881e56cde43a032eb44a6cc0a0a04871249aae7628ce58` |
| `15` | `10_Figures_Tables/figures/FIG0004_cross_country_shift.svg` | `24,861` | `a9520d88c2e5577b8e8a1763ecbd68fc7e1632f30cdecf2c451797ca9261a396` |
| `16` | `10_Figures_Tables/figures/FIG0005_rq3_latency_pareto.svg` | `12,576` | `e1b9cfd28ef38752c9ec47e91d9be45590ed53c1cce6f6bc5e371a6f68b9b8f4` |
| `17` | `10_Figures_Tables/figures/FIG0006_error_and_size_recall.svg` | `15,326` | `dd10472a935f9fa4821ef5e4f9b309535c5eb8119ff2e3ef05c4441846be072d` |
| `18` | `10_Figures_Tables/tables/TAB0001_literature_audit.md` | `1,505` | `60bac69bfc8f94324d38fb8808744b0a45e7b1aa4ed3e2b282f2a46f21f96100` |
| `19` | `10_Figures_Tables/tables/TAB0001_literature_audit.tex` | `1,615` | `f076519a8a5b4815bc6c6caa398a12c97be0aa0d865c98b951d41747bc3933c1` |
| `20` | `10_Figures_Tables/tables/TAB0002_dataset_splits.md` | `1,342` | `c30071772361a28aa207dc758ee352ae6377084baf33588a0f5f887e950d07e9` |
| `21` | `10_Figures_Tables/tables/TAB0002_dataset_splits.tex` | `1,413` | `356c16bd737a63eeae673ed3f552eb34fc0431118f57f4d322171ad24ed6adf0` |
| `22` | `10_Figures_Tables/tables/TAB0003_experiment_matrix.md` | `2,110` | `3c2191f2e6489bcd6cb1f90519ec1f49e22bd715f5d6bb8a305878db54a26167` |
| `23` | `10_Figures_Tables/tables/TAB0003_experiment_matrix.tex` | `2,200` | `9d16cd82b1170a13541f0e2c4d138b4d67c082ef2229627dbbfdbbc87bdc9a3d` |
| `24` | `10_Figures_Tables/tables/TAB0004_heldout_scoreboard.md` | `2,651` | `5d2dfac086cd64bc6b99dd847749c5a108fb0836f11ad51bca73dd5a76f609e1` |
| `25` | `10_Figures_Tables/tables/TAB0004_heldout_scoreboard.tex` | `2,745` | `2b1d490f6cd454a346d857dc3946add4fd865125de63ff7402c19b3f8268e133` |
| `26` | `10_Figures_Tables/tables/TAB0005_rq2_rq3_pareto.md` | `1,918` | `1e8675b96a378205f558760392ec67aede48c3039cd3a8a9bc7d2a246df29079` |
| `27` | `10_Figures_Tables/tables/TAB0005_rq2_rq3_pareto.tex` | `1,997` | `6bf4c66b37242a81f77a1f3228425ba945baedc609db83a540c7fa82991c1292` |
| `28` | `10_Figures_Tables/tables/TAB0006_cross_country_shift.md` | `3,003` | `faa7b3e5f37d04e0497045cfaaa6cd1cfc899e50233baf77db6ba50ca24863bd` |
| `29` | `10_Figures_Tables/tables/TAB0006_cross_country_shift.tex` | `3,161` | `51654dedcbbe361c9ece661ed145051816025d1628cae352b3d98df788c5b703` |
| `30` | `02_Literature/references.bib` | `62,275` | `514d7082dd8e62c43bb109f7d893c7ffdf8e0282e29f1d3a0a26888657367328` |
| `31` | `09_Evaluation/freeze_manifest.json` | `19,674` | `d6147ffe5a0e6173da4440185c7cddacc2296aaf71908f0388e7aecf9e234ba1` |
| `32` | `09_Evaluation/g12_reconciliation_audit.json` | `4,569` | `bb8f25d0531d3eacebb8e7f72c076e1e3d648cc4da913af5246af3dcac03d469` |
| `33` | `12_Documentation/step038_reproducibility_audit.json` | `3,626` | `a29c94f3c271667ab08f7f09be9c9d0a9f1545e52a35a2edd695a292251f6535` |

---

## 4. Immutability & Post-Submission Revision Rule (`STEP-043` Procedure 4)

Once Stage 3 (`CONFIRMED_SUBMITTED`) is recorded, `DIU_CSE_Thesis_Assembled_v1.0.0.{md,html}` and `submission_bundle_manifest.json` are permanently frozen. Any post-defense committee revision must be emitted as `v1.1.0` with a new bundle manifest and separate receipt record.
