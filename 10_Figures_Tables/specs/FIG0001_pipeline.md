# Figure Specification — `FIG0001`

| Field | Value |
|---|---|
| AssetID | `FIG0001` |
| OutputPath | `10_Figures_Tables/figures/FIG0001_study_pipeline.svg` |
| GeneratorCommand | `python 13_Automation/generate_step041_assets.py` |
| SourceIDs | `DS0001-DS0006; SPLIT0001-0006; PP0001-0004; FREEZE0001` |
| SafeAggregateData | `10_Figures_Tables/data/FIG0001_pipeline_data.json` (`sha256: 8c02666eaa9aa666e1d328dd3ae1318bf2efdd818814a74bb0936a4339fc91c0`) |
| Units | `workflow diagram` |
| Permission | `Public-Aggregate` (zero identifiable radiographs or private images) |
| Non-Clinical Guardrail | Strictly non-clinical research benchmark visualization; zero clinical diagnostic clearance claimed. |

## Caption
End-to-end leak-free 6-cohort 2D OPG detection governance and evaluation architecture (G01–G14).

## Visual Encoding & Verification Notes
Two-row stage-gated architecture highlighting the pre-test FREEZE0001 custody wall separating validation selection (G01–G11) from blind single-pass held-out test evaluation (G12–G14).
