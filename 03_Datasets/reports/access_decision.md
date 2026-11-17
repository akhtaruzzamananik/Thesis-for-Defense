# Dataset Access, Ethics & Custody Decision Memo (`STEP-011`)

| Metadata | Value |
|---|---|
| Step / Gate | **`STEP-011`** (`S05`) / Feeds `G04` (`STEP-013`) & `DEC0003` (`UD03`) |
| Owner (Data Steward) | Akhtaruzzaman Anik (`232-15-252`) |
| Reviewer | Mahajub Al Shabah (`232-15-900`) |
| Date | `2026-11-17` |
| Governing Decisions | `UD03` (`DEC0003.md` `Version 6`), `UD11` (`DEC0011.md`), `UD20`/`UD23` (`S16` web boundaries) |
| Governing Sections | `OS §1.5 #7`, `OS §4.1`, `OS §6.2`, `OS §7.2`, `OS §10.2–10.4`; `Blueprint STEP-011` |

> [!IMPORTANT]
> **6-Dataset Portfolio Cleared (`DEC0003 Version 6`, `2026-11-17`):** Following earlier Option 1 (`CAND0001`+`CAND0003`), team (`Akhtaruzzaman Anik`, `Mahajub Al Shabah`) and Supervisor (`Ms Faiza Feroz`) elected to proceed with the **full `6` valid open-licensed datasets** (`reported 2026-11-17`). Live API verification (`2026-11-17`) confirmed **`CAND0001, CAND0002, CAND0003, CAND0004, CAND0005, CAND0007`** are open-licensed and downloadable now (replacing unpublished **`CAND0006 OPG-233`**, whose Zenodo DOI is still `[ZENODO_DOI_URL] placeholder`). **`CAND0008–CAND0014` remain strictly blocked.** Zero medical image bytes are ever pushed to public GitHub.

---

## 1. Per-Right Matrix Across the `6` Authorized Open `2D OPG` Cohorts

| Candidate & Verified Source | License & Ethics Verified (`2026-11-17`) | Use / Train / Validate | Modify Splits / Dedup / Geom | Weights & Paper Figs | Hosted Defense Demo (`S16`, `UD23`) | Raw Files on GitHub |
|---|---|---|---|---|---|---|
| **`CAND0001` (`UMFIH`)**<br>Zenodo `15487430` (`1.30 GiB` zip) | **`CC BY 4.0`** (`open`, Zenodo API) | **Yes** (Primary multi-class + `180` ext) | **Yes** (`12/13/14`-class audit required) | **Yes** (`CC BY 4.0` attribution) | **Yes** (curated PHI-checked samples + disclaimer) | **FORBIDDEN** (`OS §10.2` & `DEC0011`) |
| **`CAND0002` (`DENTEX`)**<br>Zenodo `7812323` (`10.32 GiB` zips) | **`CC BY 4.0`** (Zenodo) **vs** **`CC-BY-NC-SA-4.0`** (HF) *(inspect in-zip `LICENSE`)* | **Yes** (non-commercial FYDP; `G05/G06` QA required) | **Yes** (apply ShareAlike notice if modified labels shared) | **Conditional** (non-commercial; track `SA` boundary vs pure `CC BY` tracks) | **Conditional** (non-commercial defense demo only) | **FORBIDDEN** (`OS §10.2` & `DEC0011`) |
| **`CAND0003` (`Rahman 2024 Dhaka`)**<br>Mendeley `c4hhrkxytw` V4 (`~197 MB`) | **`CC BY 4.0`** (Mendeley) **vs** **`CC BY-NC 4.0`** (*DiB*, Ethics `MK-198109`) | **Yes** (Bangladesh cross-cohort & `RQ2 CLAHE`) | **Yes** (MUST discard `558` augs, keep `232` origs) | **Yes** (non-commercial attribution) | **Yes** (non-commercial + border-checked OPGs) | **FORBIDDEN** (`OS §10.2` & `DEC0011`) |
| **`CAND0004` (`Do 2024 Hanoi`)**<br>Mendeley `kx52tk2ddj` V3 (`3,924–3,926` origs) | **`CC BY 4.0`** (Mendeley) **vs** **`CC BY-NC 4.0`** (article) | **Yes** (dedicated `PAI 3–5` small-lesion tiling sub-track) | **Yes** (MUST strip pre-aug `Augmentation JPG Images` & run `P0008` dedup) | **Yes** (non-commercial; disclose `0` healthy OPG spectrum bias) | **Yes** (non-commercial research showcase) | **FORBIDDEN** (`OS §10.2` & `DEC0011`) |
| **`CAND0005` (`AU-OPG`)**<br>HF `YSFF/AU-OPG` (`~1.32 GiB`, `901` annotated OPGs) | *IEEE Access* `P0026` **`CC BY 4.0`** (`Ethics D-F-H-6-Mar`; repo omits `LICENSE` tag) | **Yes** (dedicated adult tooth-level `OBB -> AABB` track) | **Yes** (verify `OBB->AABB` + unannotated healthy teeth policy) | **Yes** (`CC BY 4.0` cite `P0026`) | **Yes** (curated samples + disclaimer) | **FORBIDDEN** (`OS §10.2` & `DEC0011`) |
| **`CAND0007` (`MD-OPG`)**<br>Zenodo `17786082` (`241.2 MiB` `.rar`, `170` OPGs) | **`CC BY 4.0`** (Zenodo API) + **`MIT`** (GitHub) + Ethics `IR.ZUMS.REC.1404.242` | **Yes** (distinct pediatric `ages 3–12` caries sub-track) | **Yes** (extract `.rar`, polygon->AABB check, keep separate from adult OPGs) | **Yes** (`CC BY 4.0` + `MIT`) | **Yes** (curated samples + disclaimer) | **FORBIDDEN** (`OS §10.2` & `DEC0011`) |

*(Note: **`CAND0006` (`OPG-233`)** remains **`Blocked-Pending-Author-Release`** because `simzhangbest/opg233-benchmark` still displays `[ZENODO_DOI_URL] placeholder` as of `2026-11-17`; **`CAND0008–CAND0014`** remain **BLOCKED / EXCLUDED** per `03_Datasets/licenses/PENDING_AND_BLOCKED_SOURCES.md`.)*

---

## 2. Institutional Ethics, Privacy & Non-Merge Scientific Rules (`UD03` + `OS §4/§6`)

1. **Source Ethics Coverage Across All 6 Authorized Cohorts:**
   - `CAND0001` (`UMFIH`): De-identified adult clinical OPGs (`2021–2023`, `CC BY 4.0`).
   - `CAND0002` (`DENTEX`): Anonymized Turkish multi-center OPGs (`age >= 12`, institutional approvals in `arXiv:2305.19112`).
   - `CAND0003` (`Rahman 2024 Dhaka`): **Bangladesh Dental College & Hospital (`Protocol No: MK-198109`)**.
   - `CAND0004` (`Do 2024 Hanoi`): Retrospective de-identified Hanoi Medical Univ. OPGs (`CC BY 4.0` public Mendeley V3).
   - `CAND0005` (`AU-OPG`): **Ajman University Dental Clinic Ethics Committee (`Application No. D-F-H-6-Mar`)**.
   - `CAND0007` (`MD-OPG`): **Zanjan University of Medical Sciences (`IR.ZUMS.REC.1404.242`)**.
2. **Non-Merge Ontology Safeguard (`OS §6.2 #4`, `OS §7.2`):**
   - Having `6` cohorts does **not** permit blindly merging incompatible label sets into one training folder (`partial annotation` creates false negatives!). `STEP-013`–`STEP-019` (`UD04–UD08`) will define clean cohort-level / harmonized-subset tracks (Primary `CAND0001`/`CAND0002` + Local `CAND0003` shift + `CAND0004` `PAI` tiling + `CAND0005` OBB/AABB + `CAND0007` pediatric caries).

---

## 3. Binding Custody, Access Control, Compute & Retention Contract (`DEC0011` Alignment)

| Governance Dimension | Approved Rule (`DEC0011` + `OS §10.2`) |
|---|---|
| **Public GitHub (`main`)** | Source code (`src/`, `web/`), docs, configs, safe non-identifying CSVs/manifests ONLY. Strictly excludes `03_Datasets/raw/`, `*.png`, `*.jpg`, `*.dcm`, `*.zip`, `*.rar`, `*.tar*`, `*.7z`, `*.pt`, `*.onnx`, `*_restricted*`, and `linkage*` via `.gitignore`. |
| **Active Local Custody** | `e:\Thesis Phase 1\03_Datasets\raw\` (`118.05 GiB` free verified on `E:\`, gitignored). Immutable read-only copy after checksum verification (`STEP-012`). |
| **Shared Team Backup & Sync** | **Private Google Drive** accessible strictly to `Akhtaruzzaman Anik` & `Mahajub Al Shabah` (invite-only permissions; **"Anyone with the link" strictly disabled**). |
| **Remote GPU Compute (`Colab` / `Kaggle`)** | Permitted ONLY inside private Colab/Drive mounts or private non-public Kaggle datasets derived from authorized `STEP-012` intake; **strictly forbidden** to re-publish raw OPGs publicly (`OS §10.4`). |
| **De-identification & Disclosure (`STEP-013` & `UD23`)** | Strip EXIF metadata (`Samsung Galaxy A52` in `CAND0003`) from derived outputs and visually check borders/headers across all 6 cohorts before choosing any thesis/paper figures or `S16` demo samples. |
| **Retention & Deletion** | Retain immutable SHA-256 verification manifests and `licenses/` copies permanently in Git/archive; raw `CAND####` bytes follow source license & `UD20` post-defense retention closure (`STEP-045`). |

---

## 4. Verification Checklist (`Blueprint STEP-011`)

- [x] Use, annotation, derivative, weight, thesis figure, hosted web-demo, and redistribution rights checked individually across all 6 authorized cohorts (`licenses/CAND0001–CAND0005, CAND0007`).
- [x] Unpublished placeholder (`CAND0006 OPG-233`) and flawed/excluded sources (`CAND0008–CAND0014`) explicitly barred from `STEP-012` acquisition.
- [x] Source IRB/ethics provenance and `DEC0003 Version 6` human/supervisor alignment documented cleanly (`meetings/STEP-011_UD03_6dataset_brief.md`).
- [x] Storage (`118.05 GiB` free on `E:\`), compute destinations, and `.gitignore` protections (incl. `.rar`, `.zip`, `.jpg`, `.png`) verified.
