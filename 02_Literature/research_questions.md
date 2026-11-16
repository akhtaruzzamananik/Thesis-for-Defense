# Provisional Research Questions — bounded by O1–O3

| Field | Value |
|---|---|
| Record | `02_Literature/research_questions.md` |
| Step / gate | Drafted at STEP-004; approved at STEP-009 (`G03`) |
| Status | **PROVISIONAL — awaiting literature synthesis (STEP-008) and G03 approval.** |
| Governing sections | OS §1.4, §3.4 |

## 1. Linkage to approved objectives (`O1–O3`)

Per `scope.md` v0.3.0 (scope & O1–O3 summary confirmed by Ms Faiza Feroz via Telegram, 2026-11-16):

- **O1:** Design/train YOLO detection and localization pipeline for approved visible targets in 2D OPG images.
- **O2:** Evaluate detection on a locked held-out partition using Precision, Recall, and mAP (with `mAP@0.5` required, `RF12`).
- **O3:** Measure inference speed (`FPS` / latency) and computational overhead as a secondary aid.

*(Note: Hosting the validation-selected final best model on a website at the defense is a presentation/deployment deliverable under `S16` / `OS §8.3`, not a separate scientific RQ.)*

## 2. Provisional research questions (from `OS §1.4`)

- **Primary RQ (provisional):** How effectively and efficiently can an approved YOLO detector localize predefined dental objects and selected visible abnormalities in the available secondary 2D OPG dataset under a leakage-controlled evaluation protocol?
- **RQ1 (Detection effectiveness — maps to O1, O2):** What overall and per-class Precision, Recall, and `mAP@0.5` does the selected YOLO model achieve across approved dental target classes on a held-out, leakage-controlled OPG test partition?
- **RQ2 (Controlled factor comparison — maps to O1, O2, G5):** Under identical split and evaluation rules, how does a justified preprocessing or training factor affect validation detection performance compared with the registered baseline?
- **RQ3 (Inference speed & error profile — maps to O3, O2):** What inference latency and `FPS` does the frozen model achieve under documented hardware/timing boundaries, and what systematic error modes or label uncertainties limit performance?

## 3. Revision & approval rule

These RQs are working hypotheses for `STEP-004`. At `STEP-009`, each RQ will be refined against verified `GAP####` evidence, assigned stable approved IDs, linked to dataset/evaluation requirements (`DS`, `ANN`, `EVAL`), and submitted for Supervisor (`G03`) approval.
