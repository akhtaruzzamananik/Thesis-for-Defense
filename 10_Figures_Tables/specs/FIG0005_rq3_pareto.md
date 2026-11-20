# Figure Specification — `FIG0005`

| Field | Value |
|---|---|
| AssetID | `FIG0005` |
| OutputPath | `10_Figures_Tables/figures/FIG0005_rq3_latency_pareto.svg` |
| GeneratorCommand | `python 13_Automation/generate_step041_assets.py` |
| SourceIDs | `EVAL0001; EVAL0003; EVAL0005; EVAL0007; EVAL0011-0013; TIMING` |
| SafeAggregateData | `10_Figures_Tables/data/FIG0005_rq3_pareto_data.json` (`sha256: 7eab8d3840673d98cac8dae55a710759a9774a28c8f0b0ecad530fc0b97727f5`) |
| Units | `ms/OPG, FPS_e2e, and mAP@0.50` |
| Permission | `Public-Aggregate` (zero identifiable radiographs or private images) |
| Non-Clinical Guardrail | Strictly non-clinical research benchmark visualization; zero clinical diagnostic clearance claimed. |

## Caption
RQ3 accuracy versus end-to-end latency Pareto frontier on Kaggle Tesla T4 GPU and local Intel i5-1135G7 CPU ONNXRuntime (serial BS=1 FP32).

## Visual Encoding & Verification Notes
Panel A shows log-scale T_e2e latency vs held-out mAP@0.50 across GPU (circles) and CPU ONNX (squares) with a 1.0 s interactive threshold line; Panel B decomposes CPU latency into T_pre, T_infer, and T_post.
