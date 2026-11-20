# Figure Specification — `FIG0006`

| Field | Value |
|---|---|
| AssetID | `FIG0006` |
| OutputPath | `10_Figures_Tables/figures/FIG0006_error_and_size_recall.svg` |
| GeneratorCommand | `python 13_Automation/generate_step041_assets.py` |
| SourceIDs | `ERRREV0001; EVAL0001-0002; EVAL0009-0011; EVAL0013-0014` |
| SafeAggregateData | `10_Figures_Tables/data/FIG0006_error_taxonomy_data.json` (`sha256: 045999bf311c6dc0b14f5be2a873ccb7a72343b043bffaa9feb36f239715ccec`) |
| Units | `proportion (%) and recall (0-1)` |
| Permission | `Public-Aggregate` (zero identifiable radiographs or private images) |
| Non-Clinical Guardrail | Strictly non-clinical research benchmark visualization; zero clinical diagnostic clearance claimed. |

## Caption
TIDE-style FP/FN error decomposition and normalized box-area size-bucket recall (Small <0.2% vs Medium vs Large) across all 7 primary held-out evaluations.

## Visual Encoding & Verification Notes
Panel A shows 100% stacked FP breakdown highlighting TrackC selective-annotation FP_Bkg (69.4%) and TrackD ordinal FP_Cls (43.9%, 86.7% adjacent PAI swaps); Panel B contrasts Small/Medium/Large recall.
