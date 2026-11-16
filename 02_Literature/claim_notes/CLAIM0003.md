# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0003.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0003 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0002.md`, `P0010.md`, `P0017.md`, `P0021.md`, `P0026.md`, `P0029.md`, `P0031.md`, `P0032.md`, `P0034.md`, `P0036.md`, `P0038.md` |
| governing_section | OS §9.1 |

## Exact statement

Although explicit 2D OPG box detection exists (`23` Group A + `5` Group B detectors), multiple published studies mislabel whole-image, patch, Grad-CAM, or tooth-crop classification pipelines as "detection" without standard IoU-matched `mAP` or background `FP/FN` metrics, while decoupled tight-crop classification truncates apical lesions.

## scope

- Covers task framing and evaluation comparability across `P0002, P0010, P0017, P0021, P0026, P0029, P0031, P0032, P0034, P0036, P0038` (`GAP0002` / `G2`).

## evidence IDs/locators

- `P0002` (pp. 1, 4–12): Title claims *"OPG dental disease detection"* yet trains whole-image `ViT/Swin` classification (`96.0% F1`) on Kaggle *"RGB intraoral images"* (`0` boxes/`mAP`).
- `P0010` (pp. 1, 9–12): Title claims *"Detection"* yet trains `64×64` `ResNet-18` patch classifier (`Precision = 0.318, F1 = 0.464`, >2 FP/TP) and oracle `Smile Zone` U-Net segmentation.
- `P0038` (pp. 1–7): Claims `Grad-CAM Soft-IoU` weakly-supervised lesion localization on `ResNet50` classification with **zero** test localization metrics (`IoU/Dice/mAP` omitted).
- `P0017` (`Table 3`, p. 14): Ranks box-less `ViT` classifier (`94.15%`) directly against `Faster R-CNN` (`82.0% mAP50`) and `YOLOv11` (`70.7% mAP50`).
- `P0021` (`Tables 2–3`, p. 10): Reports closed-set `6×6` matrix (`F1=0.9941`) with `0` background `FP/FN` and omits `mAP` and `IoU` matching threshold.
- `P0031` (`Tables 4–5`, pp. 9–10): MLLMs fail at whole-OPG tooth–finding localization (`Pair F1 = 0.340–0.485`), and geometric FDI recommender fails on `85.2%` of lesion boxes.
- `P0034` & `P0036`: `P0034` pools classifier `Aljabri [32]` into detection meta-analysis; `P0036` substitutes tooth-level binary classification `IoU/DSC` (`0.75/0.85`) for pixel localization (`Table 6` vs `Table 7`).
- `P0032` (`p. 8`): Tight tooth BBox crops truncate apical lesions (`Sens = 0.538` vs dentists `0.854`), while `P0026` omits Stage-1 `9.4%` misses from Stage-2 eval and `P0029` (`0.9507 -> 0.7974`) proves Oracle GT-ROI overstates deployable localization.
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- `23` Group A papers plus `P0026, P0030, P0032, P0036, P0041` DO evaluate genuine spatial bounding-box localization; therefore blanket claims that OPG literature lacks box detectors are false.

## uncertainty

Low: every task-type discrepancy is directly verified in the primary methods and tables of the cited `T05` files.

## permitted wording

*"While true 2D OPG box detection is established across Group A studies, literature comparisons must guard against studies that equate non-locating whole-image/patch/CAM classifiers or closed-set confusion matrices with IoU-thresholded object detection (`P0002, P0010, P0017, P0021, P0031, P0034, P0036, P0038`), as well as Oracle/tight-crop pipelines that hide misses or truncate apical anatomy (`P0026, P0029, P0032`)."*

## verification

Verified directly across Core `T05` summaries and `GAP0002.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§1`, `§3.3`, `§5`); `02_Literature/gap_notes/GAP0002.md`.
