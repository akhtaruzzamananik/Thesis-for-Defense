# Figure Specification — `FIG0004`

| Field | Value |
|---|---|
| AssetID | `FIG0004` |
| OutputPath | `10_Figures_Tables/figures/FIG0004_cross_country_shift.svg` |
| GeneratorCommand | `python 13_Automation/generate_step041_assets.py` |
| SourceIDs | `XSHIFT01-XSHIFT06` |
| SafeAggregateData | `10_Figures_Tables/data/FIG0004_xshift_data.json` (`sha256: 591fae7a9b3e1ef330474efd03901bbb39b8773fb12d885d431af6fb46853eb3`) |
| Units | `AP@0.50, AP@0.50:95, and F1 (0-1)` |
| Permission | `Public-Aggregate` (zero identifiable radiographs or private images) |
| Non-Clinical Guardrail | Strictly non-clinical research benchmark visualization; zero clinical diagnostic clearance claimed. |

## Caption
Zero-shot 5-country cross-cohort domain-shift AP@0.50 heatmap comparing high-contrast structural findings (HC03–HC05) against low-contrast radiolucencies (HC01–HC02).

## Visual Encoding & Verification Notes
Colorblind-safe heatmap matrix over all 20 zero-shot concept-bridge evaluations grouped into structural (HC03–HC05) and radiolucent (HC01–HC02) concepts.
