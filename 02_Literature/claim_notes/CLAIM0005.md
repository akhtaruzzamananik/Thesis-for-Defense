# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0005.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0005 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0006.md`, `P0007.md`, `P0011.md`, `P0013.md`, `P0015.md`, `P0018.md`, `P0022.md`, `P0023.md`, `P0026.md`, `P0029.md`, `P0031.md`, `P0033.md`, `P0035.md` |
| governing_section | OS §9.1 |

## Exact statement

On identical `407` OPGs (`Impacted Tooth`), bounding-box detection (`P0018`: `98.3% mAP@0.5, 96.0% F1`) outperforms binary semantic segmentation (`P0035`: `85.29% IoU, 92.02% F1`) which merges touching instances (`P0007, P0022` confirm detector advantage), whereas axis-aligned bounding boxes (`AABB`) underperform keypoints (`P0013`), oriented boxes (`P0006, P0026`), or diffuse contours (`P0023, P0031`) for morphometric/oblique/diffuse tasks.

## scope

- Compares representation suitability across discrete object detection (`AABB`), oriented detection (`OBB`), keypoint pose (`PE`), instance segmentation, and semantic segmentation (`GAP0003` / `G3`).

## evidence IDs/locators

- **Same-dataset natural experiment (`407` OPGs, `325/21/61`):** `P0018` (`YOLOv8L+RT-DETR+Bayesian WBF`, `Tables 3–4`, pp. 12–13: `mAP@0.5 = 98.3%, F1 = 96.0%`) vs `P0035` (`U-Net+EfficientNetB7`, `Tables 4–9`, pp. 7–11: `IoU = 85.29%, F1 = 92.02%`; adjacent teeth merge in `Fig. 4 Ex. 3`).
- `P0007` (`Table 2`, p. 7, `44` FDI): `YOLOv11` (`mAP50=0.8715, F1=0.8592`) > `Mask R-CNN` (`0.7870`) > semantic `DeepLabV3` (`0.6167`).
- `P0022` (`Tables 2–6`, pp. 5–7, `12` classes): Box `YOLOv7m` (`mAP0.5=0.740, mAP0.5-95=0.481`) > instance-seg `YOLOv8m` (`0.591 / 0.272`; `Maxilla 0.070–0.125`, `Screw 0.011–0.077`).
- **Limits of `AABB`:** `P0013` (`Table 2`, p. 9: `YOLOv12x-OD AABB` `3.13%` length error / `F1=0.60` vs `YOLOv12x-pose` `0.74%` / `F1=0.88` on `OIEARR`); `P0023` (`pp. 8–9`: `AABB` collapses on diffuse `Alveolar Bone Loss AP=0.165/0.154`, mirrored by `P0031` losing `91%` of `Bone loss` polygons); `P0006` (`Table 2`, p. 8: `YOLOv11-OBB-s` `+4.1%` test mAP over `AABB` at `14.2 ms`), echoed by `P0026` (`YOLOv11x-OBB mAP50=0.954`); `P0029` (`BBox-only` ROI masking -> `IoU=0.1489`); `P0033` (`99.08%` background inflates pixel `Acc=0.997`, `AP50:95` vs `Dice` inversion).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- When exact pixel boundaries of teeth are specifically needed (`P0001, P0011, P0015, P0040`), Stage-2 or `YOLO-seg` instance masks reach `0.94–0.98` `mDice/mAP50` and aid tooth-to-lesion association (`P0015 IoU>=0.25 -> F1=0.960`, `P0011 90.32%`), though cascading masks costs latency (`P0011`) or clips `9.7%` of lesions outside ROIs.

## uncertainty

Low for the verified cross-study comparisons; note `P0018` lacks `mAP@0.5:0.95` and used `Bayesian WBF` hyperparameters screened on `>=97%` pairs.

## permitted wording

*"Literature comparison supports `scope.md` bounds: bounding-box detection is well-suited for discrete multi-instance OPG screening (`P0007, P0018 > P0035, P0022`), provided target selection (`UD04`) excludes morphometric linear ratios (`P0013`) and unanchored diffuse bone-loss boxes (`P0023`) that require keypoints or segmentation."*

## verification

Verified directly across Core `T05` summaries and `GAP0003.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§3.4`, `§5`); `02_Literature/gap_notes/GAP0003.md`.
