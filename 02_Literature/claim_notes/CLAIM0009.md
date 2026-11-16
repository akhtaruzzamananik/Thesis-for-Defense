# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0009.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0009 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0008.md`, `P0009.md`, `P0011.md`, `P0015.md`, `P0017.md`, `P0028.md` |
| governing_section | OS §9.1 |

## Exact statement

Preserving native radiographic spatial detail via **tiling (`P0008 +0.039 to +0.121 mAP@0.50` across 6 YOLO generations; `P0028` citing `Rohrer +294%` RCTs)** or **higher input resolution (`1280–1600 px` in `P0011, P0015, P0017`)** yields more consistent gains for small OPG targets than intensity filtering, whereas naive `75%` central cropping deletes `5.7%` of boxes (`P0015`) and background negative tiles are mandatory (`P0008 Table 8`).

## scope

- Governs resolution, tiling, and cropping strategies for `O2` experiments (`GAP0005` / `G5`).

## evidence IDs/locators

- `P0008` (`Oztekin 2026`, `Tables 4 & 8`, pp. 17, 25): Downsampling full OPGs to `640×640` shrinks `95.7%` of `PAI 3–5` lesions below `32×32 px`; native `640×640` lesion-preserving tiling raised `mAP@0.50` across all `6` YOLO generations (`YOLO12m 0.494 -> 0.615`). However, omitting healthy background tiles collapsed dense sliding-window `mAP` from `0.5125` (`9.6%` FP) to `0.3729` (`37.5%` FP).
- `P0028` (`Lutescu 2026`, p. 5, citing `Rohrer et al. [30]`): `20`-tile partitioning raised `U-Net` restoration `F1` from `0.70 -> 0.95` (`+294%` root-canal fillings).
- `P0011` (`Table 11`, p. 21): Tooth-seg `mAP@50-95` rose monotonically from `0.7151` (`640px`) -> `0.7734` (`1024px`) -> `0.7859` (`1280px`) -> `0.7978` (`1600px`, `+8.27%`).
- `P0015` (`Tables 1–2`, pp. 6–8): Full **`1280×1280`** beat `1024×1024`, while `75%` central margin cropping **deleted `5.7%` of GT boxes and clipped `20.8%`**.
- `P0017` (`p. 11, Table 3`): `Faster R-CNN` at `1024×1024` (`mAP@0.50 = 82.0%, R = 64.2%`) outperformed `YOLOv11` at `640×640` (`70.7%, R = 60.6%`) on small posts/fillings.
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- Dense multi-tile sliding windows sharply reduce throughput (`P0008`: `~26.7` tiles/OPG = `0.42 s/OPG` = `2.38 OPG/s` on RTX 4090), and high `1280–1600 px` inputs increase memory and inference latency (`P0011, P0015`), creating an explicit accuracy–latency trade-off with `O3`.

## uncertainty

Low regarding the mechanism (`<32×32 px` lesion compression at `512–640 px`); optimal resolution/tiling balance depends on target lesion sizes and compute budget.

## permitted wording

*"Literature converges (`P0008, P0011, P0015, P0017, P0028`) that `512–640 px` full-OPG resizing compresses tiny caries and periapical lesions, whereas higher resolution (`1024–1280 px`) or background-aware tiling protects small-lesion recall at a quantifiable latency cost (`O2–O3`)."*

## verification

Verified directly across Core `T05` summaries and `GAP0005.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§4.2`, `§5`); `02_Literature/gap_notes/GAP0005.md`.
