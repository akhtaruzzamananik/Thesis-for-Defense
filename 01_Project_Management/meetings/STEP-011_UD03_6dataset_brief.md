# STEP-011 `UD03` Update Brief — Expanded `6`-Dataset Public `2D OPG` Clearance

**To:** Ms Faiza Feroz (Supervisor) & Mahajub Al Shabah (Co-researcher)
**From:** Akhtaruzzaman Anik (`232-15-252`, Data Steward)
**Date prepared:** `2026-11-17`
**Linked Decision:** `01_Project_Management/decision_log/DEC0003.md` (`Version 6`) & `03_Datasets/reports/access_decision.md`

---

## Live Verification Summary & 6-Dataset Slate

Per team & Supervisor preference (`2026-11-17`) to proceed with the full `6`-dataset valid maximum (off-Git storage ONLY on local `03_Datasets/raw/` [`118.05 GiB` free on `E:\`] + Private Google Drive; **zero datasets on GitHub**), live API inspection completed on `2026-11-17` verified the exact **`6` live, open-licensed, downloadable `2D OPG` datasets**:

| # | CandID & Name | Live Host & Size | License & Ethics Verified (`2026-11-17`) | Intended Scientific Role (`Non-Merged Tracks`) |
|---|---|---|---|---|
| **1** | **`CAND0001` (`UMFIH`, Romania)** | Zenodo `15487430` (`1.30 GiB`) | **`CC BY 4.0`** (`1,628` int + `180` ext adult OPGs) | Primary multi-class track (`12–13` classes + `180` ext holdout) |
| **2** | **`CAND0002` (`DENTEX`, Türkiye)** | Zenodo `7812323` (`10.32 GiB`) | **`CC BY 4.0`** (Zenodo) / **`CC-BY-NC-SA-4.0`** (HF) (`arXiv:2305.19112`) | Balanced `4`-pathology benchmark (`705` train + `50` val PNGs) |
| **3** | **`CAND0003` (`Rahman 2024 Dhaka`)** | Mendeley `c4hhrkxytw.4` (`~197 MB`) | **`CC BY 4.0` / `CC BY-NC 4.0`**, Ethics `MK-198109` | Bangladeshi shift (`232` orig OPGs; strip `558` augs) + `RQ2 CLAHE` |
| **4** | **`CAND0004` (`Do 2024 Hanoi`)** | Mendeley `kx52tk2ddj.3` | **`CC BY 4.0` / `CC BY-NC 4.0`** | Dedicated `PAI 3–5` small-lesion tiling track (`3,924–3,926` origs; strip augs) |
| **5** | **`CAND0005` (`AU-OPG`, Ajman UAE)** | HF `YSFF/AU-OPG` (`~1.32 GiB`) | *IEEE Access* `P0026` **`CC BY 4.0`**, Ethics `D-F-H-6-Mar` | Dedicated adult tooth `OBB -> AABB` diagnosis track (`901` annotated OPGs) |
| **6** | **`CAND0007` (`MD-OPG`, Zanjan Iran)** | Zenodo `17786082` (`241.2 MiB` `.rar`) | **`CC BY 4.0`** (Zenodo) + **`MIT`** (GitHub), Ethics `IR.ZUMS.REC.1404.242` | Distinct pediatric (`ages 3–12`) mixed-dentition caries track (`170` OPGs) |

> [!NOTE]
> **Why `CAND0007` (`MD-OPG`) replaces `CAND0006` (`OPG-233`) in the active `6`:**
> Live inspection of `github.com/simzhangbest/opg233-benchmark` (`2026-11-17`) showed `OPG-233` (`P0031`, *Article in Press*) still has **`[ZENODO_DOI_URL] (placeholder)`** with no dataset uploaded to Zenodo yet (`Blocked-Pending-Author-Release`). Meanwhile, live Zenodo API `17786082` + GitHub `IASBS-AI-LAB/MD-OPG` verified that **`CAND0007 MD-OPG` DOES have explicit `CC BY 4.0` + `MIT` licensing and IRB approval (`IR.ZUMS.REC.1404.242`)**, cleanly taking the 6th active slot!

---

## Binding Safeguards (No Naive Blind Pooling)
1. **No raw image files on GitHub:** All 6 cohorts stay strictly in `.gitignore`-excluded `03_Datasets/raw/` + Private Google Drive (`DEC0011`).
2. **No invalid ontology merging (`OS §6.2 #4`, `§7.2`):** Because each cohort differs in label exhaustiveness (`AU-OPG` omits healthy teeth; `Do 2024` has `0` healthy OPGs & `PAI 3–5` only; `MD-OPG` is pediatric `ages 3–12`; `DENTEX` has `4` classes; `UMFIH` has `12–13`), incompatible cohorts will be benchmarked on clean cohort-aligned tracks/sub-studies rather than blindly pooled (`UD04–UD08`).
3. **Audit-trail note:** Retain Supervisor/co-researcher Telegram confirmation screenshot for this 6-dataset (`CAND0007` swap) update in `01_Project_Management/meetings/`.
