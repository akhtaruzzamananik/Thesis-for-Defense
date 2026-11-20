# Figure Specification — `FIG0002`

| Field | Value |
|---|---|
| AssetID | `FIG0002` |
| OutputPath | `10_Figures_Tables/figures/FIG0002_heldout_scoreboard_ci.svg` |
| GeneratorCommand | `python 13_Automation/generate_step041_assets.py` |
| SourceIDs | `EVAL0001; EVAL0002; EVAL0009; EVAL0010; EVAL0011; EVAL0013; EVAL0014` |
| SafeAggregateData | `10_Figures_Tables/data/FIG0002_scoreboard_data.json` (`sha256: 61686df3fb36871a4a8d95351685ddb98e8f81986bb3f55a6cc99cf3993629da`) |
| Units | `mAP / AP (0-1)` |
| Permission | `Public-Aggregate` (zero identifiable radiographs or private images) |
| Non-Clinical Guardrail | Strictly non-clinical research benchmark visualization; zero clinical diagnostic clearance claimed. |

## Caption
Held-out mAP@0.50 and mAP@0.50:0.95 with 1,000-resample GroupID bootstrap 95% CIs across all 6 independent OPG tracks and per-class radiographic contrast tiers.

## Visual Encoding & Verification Notes
Panel A shows grouped horizontal bars with exact 95% CI whiskers for all 7 primary winner evaluations; Panel B shows 13 representative classes stratified into High-Contrast Metallic/Structural, Moderate, and Subtle Radiolucent/Rare tiers.
