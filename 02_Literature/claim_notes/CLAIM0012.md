# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0012.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0012 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Narrowed-Hypothesis |
| source_inputs | `02_Literature/summaries/P0001.md`, `P0006.md`, `P0008.md`, `P0009.md`, `P0011.md`, `P0012.md`, `P0014.md`, `P0015.md`, `P0020.md`, `P0029.md`, `P0041.md` |
| governing_section | OS §9.1 |

## Exact statement

Although single-stage compact YOLO GPU forward passes exceed `30 FPS` (`P0006, P0009, P0012, P0015, P0020`), pipelines designed for higher small-lesion recall or complex preprocessing slow sharply (`P0008` `2.38 OPG/s`, `P0011` `6.29 FPS`, `P0029` `0.30 FPS`, `P0001` `15 s`), leaving reproducible accuracy–efficiency Pareto benchmarking (`mAP@0.50 + mAP@0.50:0.95` vs bounded CPU+GPU `T_pre + T_infer + T_post` E2E timing) as an open Phase 2 contribution (`O3`).

## scope

- Narrowed `G6` contribution hypothesis guiding Phase 2 (`O3`, `S14`, `S16`).

## evidence IDs/locators

- **Fast GPU forward passes (`>30 FPS`, partial accuracy/leakage/boundary caveats):** `P0015` (`RTX 3060 1024px`: `YOLO11m 33.23 ms [30.1 FPS]` GPU / `39.93 ms [25.0 FPS]` CPU vs `RT-DETR-l 67.11 ms [14.9 FPS]`; drops `-20.5%` externally); `P0006` (`P100`: `YOLOv11-OBB-s 14.2 ms [~70.4 FPS]`; pre-split leaked); `P0009` (`RTX 5060`: `202–479 FPS_infer`; omits `FPS_all` & `PA mAP50=0.0726`); `P0012` (`4×V100 512px`: `YOLOv5 45.7 FPS` vs `ViT+FPN 14.2 FPS`); `P0020` (`RTX A5000`: `YOLOv7-M 11.1 ms`; math errors).
- **Accuracy/preprocessing/deployment throughput bottlenecks (`<12 OPG/s`):** `P0041` (`RTX 2080 Ti`: `YOLOv4 90 ms` [`~11.1 FPS`]); `P0011` (`RTX 5000 Ada`: ROI cascade `0.1589 s/OPG [~6.29 FPS]`, full `0.5541 s`); `P0008` (`RTX 4090`: dense 26.7-tile grid `0.42 s/OPG [2.38 OPG/s]`); `P0029` (`Tesla T4`: raw `426.0 ms [2.35 FPS]` -> CPU `CLAHE+FFT+Canny` `3,366.7 ms [0.30 FPS]`, `7.9×` slowdown); `P0001` (`Cloud Run`: `15 ± 1.4 s/OPG`).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet` (Phase 2 benchmarking pending).

## contradictions

- `P0015` (`YOLO11m`: `30.1 FPS` GPU / `25.0 FPS` CPU at `1024px`) comes closest to unified efficiency, but did not report per-class pathology breakdowns across `12` classes, showed a `-20.5%` external `mAP50` drop (`0.742 -> 0.537`), and did not isolate preprocessing/NMS sub-timings.

## uncertainty

Timing comparisons across disparate hardware (`T4, P100, 2080 Ti, 3060, 4090, A5000, 5000 Ada, 5060 Laptop, 4×V100`) and input resolutions (`512–1280 px`) are non-commensurable — making matched-hardware single-rig benchmarking in Phase 2 (`O3`) essential.

## permitted wording

*"Cross-hardware comparisons in existing OPG papers cannot directly establish optimal accuracy–speed trade-offs; a controlled same-hardware benchmark measuring leak-free per-class pathology `mAP@0.50:0.95` alongside single-image (`batch = 1`) CPU and GPU `T_pre + T_infer + T_post` timing (`O3`) remains unaddressed and directly feasible."*

## verification

Verified across Core `T05` summaries and `GAP0006.md` (`STEP-008`); Phase 2 experimental hypothesis approved under `RQ0` & `RQ3` at `G03 PASS` (`2026-11-17`), empirical benchmarking awaiting `S05–S14`.

## writing locations

`02_Literature/synthesis.md` (`§4.3`, `§5`, `§6`); `02_Literature/gap_notes/GAP0006.md`.
