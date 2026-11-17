# Dataset Access, Ethics & Custody Decision Memo (`STEP-011`)

| Metadata | Value |
|---|---|
| Step / Gate | **`STEP-011`** (`S05`) / Feeds `G04` (`STEP-013`) & `DEC0003` (`UD03`) |
| Owner (Data Steward) | Akhtaruzzaman Anik (`232-15-252`) |
| Reviewer | Mahajub Al Shabah (`232-15-900`) |
| Date | `2026-11-17` |
| Governing Decisions | `UD03` (`DEC0003.md`), `UD11` (`DEC0011.md`), `UD20`/`UD23` (`S16` web boundaries) |
| Governing Sections | `OS §1.5 #7`, `OS §4.1`, `OS §10.2–10.4`; `Blueprint STEP-011` |

> [!IMPORTANT]
> **Option 1 Cleared (`DEC0003` Resolved, `2026-11-17`):** Supervisor `Ms Faiza Feroz`, Co-researcher `Mahajub Al Shabah`, and Data Steward `Akhtaruzzaman Anik` confirmed **Option 1 (`CAND0001 UMFIH 1.30 GiB CC BY 4.0` + `CAND0003 Rahman 2024 Dhaka 197 MB CC BY 4.0 / CC BY-NC 4.0 MK-198109`)** (`reported by A. Anik, 2026-11-17`). **`STEP-012` off-Git intake (`Local PC 03_Datasets/raw/` + `Private Google Drive`) is now authorized ONLY for `CAND0001` & `CAND0003`. `CAND0002 DENTEX` (`10.32 GiB`) and `CAND0004–0014` remain blocked from acquisition.** Zero medical image bytes are ever pushed to public GitHub.

---

## 1. Per-Right Matrix Across Shortlisted Candidates (`CAND0001–CAND0003`)

| Candidate & Official Source | License Verified (API / Primary Record) | Use / Train / Validate | Modify Splits / Clean Labels | Model Weights & Paper Figs | Hosted Defense Demo (`S16`, `UD23`) | Raw Redistribution on GitHub |
|---|---|---|---|---|---|---|
| **`CAND0001` (`UMFIH`)**<br>`doi:10.5281/zenodo.15487429`<br>*(Record `15487430`, `1.30 GiB` zip)* | **`CC BY 4.0`** (`open`, Zenodo API verified `2026-11-17`) | **Yes** | **Yes** (`12/13/14`-class audit required) | **Yes** (attribution required; check figures for burned-in PHI) | **Yes** (frozen model + curated PHI-checked sample OPGs + disclaimer) | **FORBIDDEN** by `OS §10.2` & `DEC0011` |
| **`CAND0002` (`DENTEX`)**<br>`doi:10.5281/zenodo.7812323`<br>*(Record `7812323`, `10.32 GiB` zips)* | **`CC BY 4.0`** on Zenodo API **vs** **`CC-BY-NC-SA-4.0`** on HuggingFace *(conservative `NC-SA` applied)* | **Yes** (non-commercial FYDP) | **Yes** (`SA` notice if modified labels distributed) | **Conditional** (non-commercial attribution; note `SA` on derivatives) | **Conditional** (strictly non-commercial defense demo only) | **FORBIDDEN** by `OS §10.2` & `DEC0011` |
| **`CAND0003` (`Rahman 2024 Dhaka`)**<br>`doi:10.17632/c4hhrkxytw.4`<br>*(Mendeley V4, `197 MB`)* | **`CC BY 4.0`** Mendeley API **vs** **`CC BY-NC 4.0`** article (`MK-198109`) *(treated conservatively as `BY-NC`)* | **Yes** (Bangladesh cross-cohort) | **Yes** (MUST discard `558` pre-split augs, keep `232` originals) | **Yes** (non-commercial attribution; check film borders for clinic text) | **Yes** (strictly non-commercial showcase + curated checked samples) | **FORBIDDEN** by `OS §10.2` & `DEC0011` |

*(All other candidates `CAND0004–CAND0014` remain **BLOCKED** from intake per `03_Datasets/licenses/PENDING_AND_BLOCKED_SOURCES.md`.)*

---

## 2. Institutional Ethics, Privacy & Consent Determination (`UD03`)

1. **Source-side Ethics & De-identification:**
   - `CAND0001` (`UMFIH`): De-identified retrospective adult clinical OPGs curated at UMFIH Cluj-Napoca (`2021–2023`) for open Zenodo scientific release (`CC BY 4.0`).
   - `CAND0002` (`DENTEX`): Anonymized patient scans (`>= 12` yrs) stripped of non-diagnostic identifiers with source institutional approvals (`arXiv:2305.19112`).
   - `CAND0003` (`Rahman 2024`): Ethical approval obtained from **Bangladesh Dental College & Hospital (`Protocol No: MK-198109`)** prior to open release (`P0024 p. 13`).
2. **DIU Institutional / Team Human Determination Required (`DEC0003`):**
   - We make **no self-granted ethics exemption claim**. Because all shortlisted datasets are **already publicly released, de-identified, secondary radiographic collections**, `DEC0003` requests confirmation from Research Lead (`Akhtaruzzaman Anik`), Literature/Model Lead (`Mahajub Al Shabah`), and Supervisor (`Ms Faiza Feroz` / DIU CSE rules) on whether:
     - Secondary computational research on open-licensed (`CC BY 4.0` / `CC-BY-NC-SA-4.0`) anonymized datasets qualifies under DIU's minimal-risk FYDP project track (`no local human-subject recruitment or hospital interaction`), **AND**
     - Which of the three candidates (`CAND0001` `1.30 GiB` + `CAND0003` `197 MB`, and/or `CAND0002` `10.32 GiB` requiring extra disk/Colab bandwidth) are authorized for `STEP-012` download.

---

## 3. Binding Custody, Access Control, Compute & Retention Contract (`DEC0011` Alignment)

| Governance Dimension | Approved Rule (`DEC0011` + `OS §10.2`) |
|---|---|
| **Public GitHub (`main`)** | Source code (`src/`, `web/`), docs, configs, safe non-identifying CSVs/manifests ONLY. Explicitly excludes `03_Datasets/raw/`, `*.png`, `*.jpg`, `*.dcm`, `*.zip`, `*.tar.gz`, `*.pt`, `*.onnx`, `*_restricted*`, and `linkage*` via `.gitignore`. |
| **Active Local Custody** | `e:\Thesis Phase 1\03_Datasets\raw\` (local NTFS, gitignored). Immutable read-only copy after SHA-256 checksum verification (`STEP-012`). |
| **Shared Team Backup & Sync** | **Private Google Drive** accessible strictly to `Akhtaruzzaman Anik` & `Mahajub Al Shabah` (explicit invite-only permissions; **"Anyone with the link" strictly disabled**). |
| **Remote GPU Compute (`Colab` / `Kaggle`)** | Permitted ONLY inside private user Colab/Google Drive mounts or private Kaggle datasets (`non-public visibility`) derived from authorized `STEP-012` intake; **strictly forbidden** to re-publish raw OPGs as public Kaggle datasets or public Roboflow projects (`OS §10.4`). |
| **De-identification & Disclosure (`STEP-013` & `UD23`)** | During `STEP-013`, inspect headers/EXIF (`Samsung Galaxy A52` EXIF metadata in `CAND0003` must be stripped cleanly in derived manifests!) and visually check corners/borders for clinic stamps or burned-in text before selecting any thesis/paper figures or `S16` demo samples. |
| **Retention & Deletion** | Retain immutable SHA-256 verification manifests and `licenses/` copies permanently in Git/archive; raw `CAND####` bytes follow source license & `UD20` post-defense retention closure (`STEP-045`). |

---

## 4. Verification Checklist (`Blueprint STEP-011`)

- [x] Use, annotation, derivative, weight, thesis figure, hosted web-demo, and redistribution rights checked separately across `CAND0001–CAND0003` (`licenses/`).
- [x] Source IRB/ethics provenance documented without inventing DIU institutional waiver approval (`DEC0003` pending human determination).
- [x] Storage, compute destinations, and `.gitignore` protections aligned with `DEC0011` and `OS §10.2`.
- [x] Blocked/pending sources (`CAND0004–CAND0014`) explicitly barred from acquisition.
