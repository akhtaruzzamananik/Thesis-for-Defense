# Figure Specification — `FIG0003`

| Field | Value |
|---|---|
| AssetID | `FIG0003` |
| OutputPath | `10_Figures_Tables/figures/FIG0003_rq2_clahe_vs_1280.svg` |
| GeneratorCommand | `python 13_Automation/generate_step041_assets.py` |
| SourceIDs | `EXP0001; EXP0004; EXP0005; EXP0008-0012; EVAL0001-0004; EVAL0011-0012` |
| SafeAggregateData | `10_Figures_Tables/data/FIG0003_rq2_ablation_data.json` (`sha256: 113d4c16cd95f05c202b9bbafc5aa03bc44b057b5930a2ac63a1bff27b1ad2e0`) |
| Units | `mAP delta and mAP@0.50:0.95 (0-1)` |
| Permission | `Public-Aggregate` (zero identifiable radiographs or private images) |
| Non-Clinical Guardrail | Strictly non-clinical research benchmark visualization; zero clinical diagnostic clearance claimed. |

## Caption
Controlled RQ2 ablation: consistent CLAHE degradation (3/3 validation pairs) versus spatial resolution gain from 640px to 1280px on held-out TrackA and TrackD cohorts.

## Visual Encoding & Verification Notes
Panel A plots diverging mAP@0.50 deltas against matched raw 640px controls; Panel B plots paired 640px vs 1280px strict localization mAP@0.50:0.95 with 95% GroupID bootstrap intervals.
