# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0008.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0008 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0001.md`, `P0002.md`, `P0004.md`, `P0008.md`, `P0011.md`–`P0013.md`, `P0018.md`, `P0024.md`, `P0029.md`, `P0038.md`, `P0041.md`, `P0042.md` |
| governing_section | OS §9.1 |

## Exact statement

`CLAHE` and contrast/super-resolution enhancement do NOT universally improve `2D OPG` detection accuracy: while controlled `CLAHE` + sharpening helped cropped `YOLOv5` on `500` OPGs (`P0004`: `0.701/0.774 -> 0.924/0.948`), controlled negative/null results in `P0011` (`-3.91% mAP50-95`), `P0029` (`0.8173` raw > `0.8104–0.8151`), `P0038` (`95.69% < 97.50%`), `P0018` (`-0.5% to -1.9%`), `P0041`, `P0001`, and `P0008` refute blanket enhancement superiority.

## scope

- Directly informs `O2` experimental design (`GAP0005` / `G5`): treats `Raw` vs `CLAHE` as an empirical ablation factor rather than an assumed prerequisite.

## evidence IDs/locators

- **Positive controlled ablation (`P0004`, `Table 4`, p. 8):** On `500` cropped Indian OPGs (`IMC`), `YOLOv5 mAP@0.5` progressed `Raw 0.701` -> `Cropped 0.774` -> **`CLAHE(clip=2) 0.924`** -> **`CLAHE+Sharp 0.948`**, while `Gaussian` dropped Stage-2 `ResNet50` accuracy (`0.648 -> 0.482`) despite `PSNR = 37.76 dB`.
- **Negative / Null controlled evidence:**
  - `P0011` (`Table 4`, p. 17): `Sharpening + CLAHE + Gaussian` (`Enh.=Yes`) dropped `YOLOv12-m` **`mAP@50 0.9194 -> 0.9023 (-1.71%)`** and **`mAP@50-95 0.7794 -> 0.7403 (-3.91%)`**.
  - `P0029` (`Tables 17, 26, 30`, pp. 27, 36): With `8×` augmentation (`Table 30`), **Raw `Mask R-CNN` (`IoU = 0.8173`) outperformed fixed `CLAHE clip=3.0` (`0.8104`), `Entropy CLAHE` (`0.8134`), `Full CLAHE+FFT+Canny` (`0.8151`, adding `7.9×` latency), and `Global FFT` (`0.8005`, `Bg SSIM=0.522`)**.
  - `P0038` (`716` OPGs): `CLAHE+Intensity+Flip+Rotate = 95.69%` trailed `Intensity+Flip` (`97.50%`) and `+Trapezoid` (`99.17%`).
  - `P0018` (`Table 2`, p. 11): `GFP-GAN` facial-prior SR had `0.0%` effect on `YOLOv8X` and **hurt `RT-DETR-L` (`-0.5%`) & `RT-DETR-X` (`-1.9%`)**.
  - `P0001` (`YOLO26m 0.87–0.98`, p. 4), `P0008` (`YOLO12m`), and `P0041` (`YOLOv4`, citing `Ha 2021 [19]` against `CLAHE`) omitted `CLAHE` cleanly.
  - `P0024` (`YOLOv7`) & `P0013` (`YOLOv12x-pose`) used `CLAHE` without `Raw vs CLAHE` ablations; `P0042` showed visual `AME/LogAME` scores only, warning visual metrics != diagnostic gain.
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- `P0002` (`Table 2`, p. 6) claimed `+1.3%` ViT F1 from `U-Net ROI + CLAHE`, but that comparison bundled ROI cropping + `CLAHE` simultaneously on a pre-split-augmented RGB intraoral dataset; `P0004` vs `P0011/P0029` discrepancy likely depends on scanner exposure distributions, augmentation strength, and whether `Gaussian`/sharpening accompanies `CLAHE`.

## uncertainty

High on predicting a priori whether `CLAHE` helps or hurts a new OPG cohort — which is why **`Raw vs parameterized CLAHE (clipLimit, tileGridSize)`** must be tested empirically in Phase 2 (`S7`).

## permitted wording

*"Evidence on `CLAHE` in `2D OPG` is mixed: `P0004` measured large `YOLOv5` gains (`0.774 -> 0.948`), whereas `P0011`, `P0029`, `P0038`, and `P0041` found contrast filtering neutral or harmful alongside modern augmentation (`P0001, P0008`). Hence our thesis tests `CLAHE` parameters as a falsifiable experimental factor rather than an assumed prerequisite (`O2`)."*

## verification

Verified directly across Core `T05` summaries and `GAP0005.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§4.2`, `§5`); `02_Literature/gap_notes/GAP0005.md`.
