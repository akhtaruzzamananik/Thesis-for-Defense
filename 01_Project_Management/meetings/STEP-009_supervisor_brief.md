# STEP-009 supervisor brief — literature synthesis, `G1–G6` verdict, `UD19` & `RQ0–RQ3` approval (`G03`)

**To:** Ms Faiza Feroz (Supervisor); cc Israt Jahan (Co-supervisor); Mahajub Al Shabah (Literature Lead)
**From:** Akhtaruzzaman Anik (`232-15-252`), Mahajub Al Shabah (`232-15-900`)
**Project:** A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO.
**Date prepared:** `2026-11-17`
**Literature cutoff date:** `2026-11-16` (`180` files -> `122` unique screened -> `42` Core full-text + `55` Reserve + `25` Excluded)
**Attachments / Evidence Paths:**
- `02_Literature/synthesis.md`
- `02_Literature/research_questions.md` (`v0.9.0`, candidate-final `RQ0–RQ3` map)
- `02_Literature/gaps.csv` & `02_Literature/gap_notes/GAP0001.md`–`GAP0006.md`
- `02_Literature/claims.csv` & `02_Literature/claim_notes/CLAIM0001.md`–`CLAIM0012.md`
- `01_Project_Management/decision_log/DEC0019.md` (`UD19` audit)
- `01_Project_Management/reviews/G03_assessment_2026-11-17.md` (`G03` pre-assessment)

---

## Executive Summary of Literature Audit (`OS §3.3`)

We systematically tested the six provisional report gaps (`G1–G6`) across all `42` full-text Core studies (`23` direct `2D OPG` box detectors + `19` contextual studies) and `55` Reserve papers:
- **Honest refutation of `G1` (`GAP0001 = refuted` as broad novelty claim):** Multi-class `2D OPG` YOLO detectors (`4–13` classes) already exist (`13/23` Group A papers), so we **refute and drop** any claim that multi-class OPG detection does not exist. Instead, we preserve the real surviving gap: severe recall/AP disparity between high-contrast targets (`0.83–0.98`) vs. small radiolucent pathologies (`Caries 0.25–0.40`, `Periapical lesions 0.07–0.32`), plus widespread pre-split augmentation leakage (`+30.4% mAP50` inflation proven in `P0011` vs `P0008`).
- **`G2–G6` narrowed honestly (`GAP0002–0006 = narrowed`):** Bounding boxes outperform semantic segmentation for discrete OPG screening (`P0018 > P0035`), `CLAHE` does not automatically improve OPG detection (`P0004` positive vs `P0011/P0029/P0038/P0041` negative/null -> must be tested empirically), and `73.8%` (`31/42`) of Core papers omit per-image inference latency despite `"real-time"` claims. Cross-modality numeric ranking against `CBCT` / `BW` stays prohibited (`scope.md v1.0.0`).

---

## Decisions Requested for Gate `G03` Sign-Off (`OS §13.2`)

| # | Question / Action Needed | Your Decision |
|---|---|---|
| **1** | **Approve bounded contribution & `RQ0–RQ3` (`research_questions.md` v0.9.0):** Do you approve the four bounded research questions (`RQ0` primary; `RQ1` multi-class & contrast-tier localization under deduplicated splits + external OPG test if permitted; `RQ2` falsifiable `Raw` vs `CLAHE` vs resolution/tiling factor ablation; `RQ3` bounded CPU+GPU `T_pre+T_infer+T_post` timing & error profile) matching `O1–O3` without fabricated targets? | ☐ Yes, approve (`G03 PASS`)<br>☐ With changes: |
| **2** | **Resolve `UD19` (`DEC0019` — deleted report `[1]–[13]` bibliography):** Since `Title Evaluation Report (1).pdf` was deleted prior to `STEP-001` (`OS Appendix F.1`), none of our claims rely on its unverified `[1]–[13]` entries (`100%` of claims cite verified `P0001–P0042` PDFs). Do you confirm **Option 1** (formally exclude unavailable `[1]–[13]` seed entries from evidential support) or wish to supply an external copy of `[1]–[13]`? | ☐ Option 1: Exclude `[1]–[13]` (rely on `P0001–P0042`)<br>☐ Option 2: Will provide `[1]–[13]` text |
| **3** | **Confirm `G03` Gate Verdict (`OS §13.2`):** With items 1–2 confirmed, may we record Gate **`G03 = PASS`** and proceed to `STEP-010` (screening candidate public `2D OPG` datasets such as `DENTEX`, `UMFIH`, `Rahman 2024 Dhaka`, deduplicated `Do 2024`, `MD-OPG`, `AU-OPG`)? | ☐ Authorize `G03 = PASS`<br>☐ Revision needed before `G03` |
| **4** | *(Reminders from `G01` ahead of `STEP-014` & `STEP-047`)* (a) Confirm **`UD21`** whether the hosted defense web demo is Required/Optional & expected defense window; (b) confirm/suggest a **qualified dental reviewer** before `STEP-014` (`G05` class ontology). | (a) Web demo (`UD21`):<br>(b) Dental reviewer: |

---

Supervisor (`Ms Faiza Feroz`) signature / confirmation: __________________   Date: __________

Literature Lead (`Mahajub Al Shabah`) `UD19` confirmation: __________________   Date: __________
