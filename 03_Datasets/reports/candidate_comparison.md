# Secondary `2D OPG` Dataset Candidate Comparison (`STEP-010`)

| Metadata | Value |
|---|---|
| Step / Stage | **`STEP-010`** (`S05` — Discover and compare OPG dataset candidates) |
| Owner (Data Steward) | Akhtaruzzaman Anik (`232-15-252`) |
| Reviewer (Literature / Model Lead) | Mahajub Al Shabah (`232-15-900`) |
| Date | `2026-11-17` |
| Prerequisite Gate | **`G03 PASS`** (`2026-11-17`, `research_questions.md v1.0.0`, `DEC0019`) |
| Open Governance Decisions | **`UD02`** (dataset selection -> `G04 / STEP-013`), **`UD03`** (licenses/ethics -> **`STEP-011` BEFORE any download**), **`UD07`** (grouping/deduplication -> `STEP-019`) |
| Registry | `03_Datasets/candidates.csv` (`14` evaluated candidates `CAND0001–CAND0014`) |
| Governing Sections | `OS §4.1`; `Blueprint STEP-010`; `research_questions.md` (`RQ0–RQ3`) |

> [!CAUTION]
> **Strict `STEP-010` / `STEP-011` Custody Rule:** Zero medical datasets have been downloaded, acquired, or approved here. Per `Blueprint STEP-010–011`, no raw archives may be fetched until `UD03` licensing, ethics/waiver, and storage compliance are verified in `03_Datasets/licenses/` and `reports/access_decision.md` (`STEP-011`).

---

## 1. Discovery Summary & Modality / Provenance Separation

Screening our **`122`** unique corpus records (`42` Core `P0001–P0042` + `55` Reserve `P0043–P0097` + `25` Excluded) identified **`14` distinct public/secondary dataset sources or clusters (`CAND0001–CAND0014`)** (plus `18+` private institutional clinical cohorts in Core such as `P0001, P0003, P0004, P0007, P0012, P0013, P0019, P0021, P0022, P0025, P0029, P0030, P0032, P0033, P0036, P0038, P0039, P0041` that are not publicly downloadable without bespoke hospital/clinic DUA/IRB agreements).

To prevent common literature pitfalls (`Blueprint STEP-010`), we enforce three strict separation filters:
1. **Strict `2D OPG` Modality Verification:** Rejects `"RGB intraoral"` misattributed mirrors (`P0002 / Kaggle Sajid`, `CAND0014`), CBCT/BW/PA-only cohorts (`P0098–P0106`), and uncurated Roboflow aggregates lacking device/institution provenance (`P0009`, `CAND0014`).
2. **Original Owner vs. Composite / Duplicate Mirrors:** Separates independent collections (`UMFIH`, `DENTEX`, `Rahman Dhaka`, `Do 2024`, `AU-OPG`, `MD-OPG`, `Zhang 2023`, `Tufts`, `Adnan 2024`) from composite/pre-augmented mirrors (`P0006` merging `Tufts` + `4,768` pre-split copies; `P0005` `ckt876jzr6.1`; `P0040` broken link combining `OII-DS + UFBA`; `OPG-233` combining Roboflow `zaks-lab` + China private; `P0018` combining `Imak + Román + Abdi`).
3. **Deduplication & Target-Schema Integrity:** Flags raw repositories polluted by pre-split augmentation (`Do 2024` `16,519/17,004 -> 3,924` originals; `Rahman 2024` `604 -> 232` originals; `Khurshid 2026` `4,768 -> 2,405` originals) and class-definition flaws (`Zhang 2023` merging caries + fillings; `P0023` diffuse `BON`; `P0006` non-radiographic `RR clinical`).

---

## 2. Master Candidate Comparison Table (`CAND0001–CAND0014`)

| CandID | Name & Origin (`PaperID`) | Modality & Count (Raw vs Pre-Aug) | Classes Reported (`RQ1` Fit) | License / Access Terms (`UD03` Check Needed) | Grouping / Leakage Unknowns (`UD07`) | Decision |
|---|---|---|---|---|---|---|
| **`CAND0001`** | **UMFIH + Multi-Center External** (`Zenodo 15487429`, `P0023 / P0015`) | `2D OPG` (`1,628` int + **`180` ext** adult; `804×415`–`2980×1536`) | **`12–13` classes:** Restorations + Implants + Caries + Periapical + Impacted + Roots + Brackets (+ diffuse BON) | Open Zenodo (`CC BY 4.0` reported; inspect archive terms & demo use at `STEP-011`) | Patient IDs unreported (`1`/adult typical); `180` multi-center OPGs give real external holdout; inspect `P0015` vs `P0023` file alignment | **`Shortlist-Primary-1`** |
| **`CAND0002`** | **DENTEX** (`arXiv:2305.19112`, `P0014 / P0036`) | `2D OPG` (`705` train + `50` val PNGs; `3,529` boxes) | **`4` pathology classes:** `Caries (799)`, `Deep Caries (942)`, `Impacted (823)`, `Periapical Lesion (965)` + FDI hierarchy | Open Zenodo/HF (`CC-BY-NC-SA-4.0` reported on HF; verify ShareAlike bounds for weights/demo at `STEP-011`) | Patient IDs unreported; omits labeler credentials/`κ` (`P0014 p.3` -> requires `G05/G06` dental QA check & hash dedup) | **`Shortlist-Primary-2`** |
| **`CAND0003`** | **Dental OPG X-RAY Dhaka** (`Mendeley c4hhrkxytw.4`, `P0024`) | `2D OPG` (**`232` original** JPGs, handheld A52 `~1176×603`; `604` w/ `3×` train aug) | **`6` classes:** `Healthy (223)`, `Caries (119)`, `Impacted (87)`, `BDC/BDR (52)`, `Infection (23)`, `Fractured (13)` | Open Mendeley (`CC BY 4.0` repo / `CC BY-NC 4.0` article; Ethics `MK-198109`; verify `STEP-011`) | Must drop `558` pre-split aug copies & ingest ONLY `232` originals; extreme minority scarcity (`13/23`); smartphone glare/blur -> tests `RQ2 CLAHE` & Bangladesh `RQ1` shift | **`Shortlist-External-3`** |
| `CAND0004` | **Hanoi PAI Lesions (`Do 2024`)** (`Mendeley kx52tk2ddj/3`, `P0008 / P0011`) | `2D OPG` (**`3,924` originals** inside `16,519–17,004` aug archive) | `3` ordinal `PAI 3–5` lesion grades only (`6,741` boxes; 0 healthy OPGs) | Open Mendeley (`CC BY 4.0` repo / `CC BY-NC 4.0` paper; verify `STEP-011`) | No patient IDs (`P0008 p.34`); raw zip has `~4×` pre-aug copies (`P0008`-style dedup mandatory); single pathology + 0 healthy spectrum bias | `Conditional-Reserve` |
| `CAND0005` | **AU-OPG** (`Ajman Univ`, `akvnn/guiding-neural-nets`, `P0026`) | `2D OPG` (`901` adult, `7,006` OBBs) | `6` tooth diagnoses + `4` treatments (tooth-level OBBs; untagged healthy teeth) | Open GitHub/portal (`CC BY-NC-SA 4.0 / CC BY-NC 4.0` cited; check `STEP-011`) | Serial OPGs excluded; single OMFR review (`no κ`); requires OBB->AABB check & background audit (`UD05`) | `Conditional-Reserve` |
| `CAND0006` | **OPG-233** (`simzhangbest/opg233-benchmark`, `P0031`) | `2D OPG` (`233` consensus OPGs; `163` Roboflow + `70` China) | `20` findings mapped to `1,859` tooth–finding polygons | Zenodo `CC BY 4.0` + GitHub `MIT` cited; confirm Zenodo DOI at `STEP-011` | `1` OPG/patient; too small (`233`) for training & composite origin (`87/320` excluded spectrum bias) | `Conditional-Reserve` |
| `CAND0007` | **MD-OPG Pediatric** (`Zenodo 17786082`, `P0010`) | `2D OPG` (`170` pediatric PNGs, `1920×1535`) | `Proximal (716)` + `Occlusal (179)` caries polygons + `Smile Zone Z` | Open Zenodo/GitHub; **explicit license UNDECLARED** (must confirm with authors before `STEP-011`) | `1` OPG/patient stated; single pathology (caries only), small `N=170`, polygon->box conversion needed | `Conditional-Reserve` |
| `CAND0008` | **Children's Pediatric OPG (`Zhang 2023`)** (`Figshare 21621705`, `P0016 / P0030`) | `2D OPG` (`~644` OPGs used in `P0016`, bite blocks) | `Dental Caries` [caries+fillings!], `Deciduous`, `RCT`, `Pulpotomy` (`P0016`) | `CC0 (Public Domain)` verified on Figshare | **Ontology flaw (`P0016 p.4`):** merges radiolucent caries with radiopaque fillings + bite-block artifacts (`P0030`) | `Hold-Ontology-Risk` |
| `CAND0009` | **Tufts Dental Database (`TDD`)** (`tdd.ece.tufts.edu`, `P0042`) | `2D OPG` (`1,000` optimum OPGs, `1615×840`) | Generic abnormality mask + `32`/Univ. teeth masks + gaze/ASR | **Gated request portal** (application/agreement required; non-open) | Optimum-quality bias; lacks specific pathology sub-classes; overlaps `P0006/P0017` | `Hold-Gated-TeethOnly` |
| `CAND0010` | **Khurshid 2026 Roots/PCT** (`Mendeley y7dkrpv7g9.2`, `P0006`) | `2D OPG` (`2,405` base mixed into `4,768` pre-aug) | `4` Retained Roots + `3` `PCT` bone-loss OBBs | `CC BY 4.0` Mendeley + inherits `1,000` Tufts terms | Admitted pre-split aug leakage (`p.10`) + merges Tufts + unlabelable `RR clinical` (`R=0.506`) | `Hold-Leakage-Overlap` |
| `CAND0011` | **Khurshid 2026 3rd Molar Impaction** (`ckt876jzr6.1`, `P0005`) | `2D OPG` (`5,796` OPGs) | `6` third-molar impaction subtypes only | `CC BY 4.0` Mendeley (over `[22,23]`) | Single tooth condition only + suspected source duplicate leakage (`99.6–100%` scores) | **`Exclude-Narrow-DupRisk`** |
| `CAND0012` | **Adnan & Umer 2024** (`Zenodo 10531566`, `P0054`) | `2D OPG` (`250` OPGs) | Teeth segmentation & FDI numbering only | `CC BY-NC 4.0` (*Data in Brief*) | Zero pathology/abnormality labels | **`Exclude-TeethOnly`** |
| `CAND0013` | **DualLabel (`P0040`) / PDCNN (`P0020`)** | `2D OPG` (`2,066–5,000` / `1,747`) | Teeth + exclusive states / `RBL` bone loss | Broken Kaggle placeholder in `P0040`; `PuckBlink/PDCNN` unclear | Unresolvable data link (`OS §4.1`); `P0040` crop leakage & caries loss | **`Exclude-BrokenLink`** |
| `CAND0014` | **Uncurated Roboflow (`P0009`) / Kaggle Oral (`P0002`) Mirrors** | `P0002` = **RGB Intraoral** (`NOT OPG`); `P0009` = unverified Roboflow | `11` (`8,124` imgs) / `4` intraoral (`5,098` imgs) | Unknown provenance, zero ethics/owner metadata | Modality contamination (`P0002`) + missing clinical/annotator traceability (`P0009`) | **`Exclude-Rejected-Provenance`** |

---

## 3. Conditional Shortlist & Architectural Rationale (`RQ0–RQ3`)

Consistent with `research_questions.md` (`v1.0.0`, **`G03 PASS`**) and realistic FYDP Phase 2 capacity, we recommend advancing **only three primary shortlist candidates (`CAND0001`, `CAND0002`, `CAND0003`)** into **`STEP-011` License, Ethics & Custody Clearance** (selecting **1 primary training/validation/test cohort + 1 compatible external/cross-cohort set** at `G04 / STEP-013`, never splitting mirrors as external sets):

1. **`CAND0001` (`UMFIH` Zenodo `15487429` — Primary Candidate #1):**
   - **Why top-ranked:** Directly spans both high-contrast restorations/implants/impacted teeth AND small radiolucent pathologies (`Caries`, `Periapical lesions`, `Root fragments`) on native clinical OPGs, **AND includes an independent `180`-OPG multi-center external set** for `RQ1` generalization testing—all under a clean `CC BY 4.0` repository record (`ICC = 0.91`).
   - **Open checks (`STEP-011–013`):** Verify exact file format/labels (`P0015` 12-class vs `P0023` 13-class), confirm rare-class sample sizes (`FUR, ORD, SRD`), check `CC BY 4.0` compliance for thesis/defense web demo (`UD20/UD23`), and decide under `UD04` how to handle diffuse `Alveolar bone loss` (`GAP0003`).
2. **`CAND0002` (`DENTEX` — Primary Candidate #2 / Alternative or Complementary Cohort):**
   - **Why shortlisted:** Focused `4`-pathology benchmark (`Caries, Deep Caries, Impacted, Periapical Lesion` across `705` OPGs / `3,529` instances) with well-balanced per-class counts (`799–965` instances each) that directly test `Impacted` vs `Caries/Periapical` disparity (`RQ1`).
   - **Open checks (`STEP-011–013`):** Verify **`CC-BY-NC-SA-4.0` ShareAlike** implications on model weights/code/defense demo (`UD03/UD20`), confirm if the `50` validation OPGs include labels, run perceptual/SHA-256 deduplication (`UD07`), and plan mandatory dental reviewer QA (`G05/G06`) because `DENTEX` omits annotator credentials (`P0014 p.3`).
3. **`CAND0003` (`Rahman et al. 2024` Dhaka — Local Bangladeshi Clinical / External Shift Candidate #3):**
   - **Why shortlisted:** Only local Bangladeshi clinical OPG collection (`232` original OPGs from 3 Dhaka centers, 2-tier `16+32`-yr dentist review), uniquely testing `RQ1` cross-population/acquisition shift (handheld camera film re-photography vs native digital OPG) and `RQ2` `CLAHE` impact on variable contrast (`P0024` left `CLAHE` unablated!).
   - **Open checks (`STEP-011–013`):** Verify `CC BY 4.0` (Mendeley) vs `CC BY-NC 4.0` (article), confirm clean extraction of ONLY the **`232` original unaugmented images** (discarding all `558` Roboflow copies), and evaluate class-overlap mapping (`Caries`, `Impacted`, `Infection`~Periapical, `BDC/BDR`~Root fragment) against `CAND0001`/`CAND0002` without merging incompatible definitions (`UD04`).

---

## 4. Verification Checklist (`Blueprint STEP-010`)

- [x] Every candidate (`CAND0001–CAND0014`) has a traceable original source URL/DOI or explicit provenance gap (`CAND0013`, `CAND0014`).
- [x] `2D OPG` relevance cleanly separated from mislabeled intraoral RGB photos (`CAND0014 / P0002`) and non-OPG exclusions (`P0098–P0106`).
- [x] All license/ethics (`UD03`), patient-grouping (`UD07`), pre-augmentation contamination, and ontology ambiguity unknowns (`UD04`) recorded explicitly.
- [x] Zero datasets downloaded, acquired, or prematurely approved (`SelectionDecision` kept conditional pending `STEP-011`–`STEP-013` and `G04`).
