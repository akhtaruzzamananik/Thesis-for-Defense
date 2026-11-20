# Consolidated Final Evaluation Report (`STEP-035` / `G12 = PASS`, `T18`)

| Metadata | Value |
|---|---|
| Template / Step / Gate | `T18` · `STEP-035` (`S12` — Consolidate final evaluation and pass `G12`) |
| Freeze Record | `FREEZE0001 v1.0.0` ([freeze.md](./freeze.md) & [freeze_manifest.json](./freeze_manifest.json), frozen `2026-11-21T01:40:00+06:00` prior to `STEP-032` start `2026-11-20T20:24:22Z`) |
| Programmatic Audit | [g12_reconciliation_audit.json](./g12_reconciliation_audit.json) (`14/14` EVALs, `128/128` per-class `TP+FN==GT` rows, `12/12` `HC01–HC05` bridges, `10` GPU + `7` CPU timing logs reconciled) |
| Governing Protocol | [protocol.md](./protocol.md) (`v1.0.0`, `sha256: 26fede09e31475e7e7a5a1cdd3bc2a111815f727d8925300976dc6060a9024c1`) |
| Evaluator & Ontology | `src/opg/evaluator.py` (`sha256: 8fa2c6d8...`) · `04_Annotations/classes.csv` (`sha256: c3f91dfc...`) |
| Owners / Reviewers | Mahajub Al Shabah (`232-15-900`, Evaluation Lead) & Akhtaruzzaman Anik (`232-15-252`, Research Lead) |
| Gate Assessment | [G12_assessment_2026-11-21.md](../01_Project_Management/reviews/G12_assessment_2026-11-21.md) (**`G12 = PASS`**) |

> [!NOTE]
> **Validity Basis (`OS §13.2`):** `G12 PASS` certifies methodological validity, traceability, leak-free custody, complete reporting of all four required metrics (`Precision`, `Recall`, `mAP@0.50`, `FPS`) plus adopted `mAP@0.50:0.95` & `GroupID` `95% CI`, and honest disclosure of every unfavorable or negative outcome — **not** an arbitrary target accuracy score (`DEC0016`).

---

## 1. Executive Synthesis of Empirical Answers to `RQ0–RQ3`

| Research Question | Empirical Finding (Strictly Bounded to Leak-Free Held-Out 2D OPG Data) | Traceable Evidence |
|---|---|---|
| **`RQ0`** *(Reproducible Leak-Free Multi-Cohort Benchmark)* | Across `6` independently licensed, connected-component deduplicated 2D OPG cohorts (`7,457` canonical OPGs, `41,103` boxes, `0` cross-partition leaks), single-stage `YOLO11s` achieved **`0.8246` `mAP@0.50`** (`0.5163` `mAP@0.50:0.95`) on `TrackE` (UAE `6`-cls), **`0.4868`** (`0.2207`) on `TrackD` (Hanoi PAI `3`-cls `@1280`), **`0.4397`** (`0.2673`) on `TrackB` (DENTEX `4`-cls), **`0.4165`** (`0.1741`; external hospital **`0.4338`** / **`0.2038`**) on `TrackA` (Romania `13`-cls `@1280`), **`0.2508`** (`5`-cls pathology **`0.2631`**) on `TrackC` (Dhaka handheld `6`-cls), and **`0.0537`** on `TrackF` (pediatric small-N `2`-cls). | `EVAL0001–EVAL0014`, [step033_final_metrics_report.md](./step033_final_metrics_report.md), `CLAIM0013` |
| **`RQ1`** *(Radiographic Contrast Hierarchy, Architecture Scale & Cross-Country Domain Shift)* | High-contrast metallic/structural targets reach **`0.76–0.998` `AP@0.50`** (`TrackE Implant = 0.9980` [`80/80` recall], `Crowned = 0.9203`, `TrackA Ext Implant = 0.9297`, `TrackB Impacted = 0.9012`), whereas subtle radiolucent/diffuse/rare findings remain much harder (`TrackA Bone_Resorption = 0.0906`, `Apical_Periodontitis = 0.3078`, `Apical_Surgery = 0.0428`). On `TrackA` `640px`, `YOLO11s` (`0.3815`) slightly outperformed `YOLOv8s` (`0.3786`) with fewer parameters (`9.4M` vs `11.2M`), while `YOLO11m` (`0.3990` internal / `0.4449` external) traded `2.1×` artifact size for modest `mAP@0.50` gains but trailed `YOLO11s@1280` on both internal `mAP@0.50` (`0.4165`) and external `mAP@0.50:0.95` (`0.2038` vs `0.1940`). Across **`12` zero-shot cross-country bridges (`5` countries)**, high-contrast **`HC03 Impacted Tooth`** generalized strongly (`0.8181` Romania→Türkiye, `0.7109` Romania→Dhaka, `0.6967` UAE→Türkiye), while low-contrast **`HC02 Periapical`** (`0.178–0.236`) and **`HC01 Caries`** (`0.163`) suffered severe domain collapse. | `EVAL0001–EVAL0014`, [xshift_metrics.csv](./xshift_metrics.csv), `CLAIM0014`, `CLAIM0015` |
| **`RQ2`** *(Controlled `PP0001–PP0004` Ablation: `CLAHE` vs `1280px` Resolution)* | **`CLAHE` degraded accuracy in `3/3` controlled validation ablations** (`EXP0008` `PP0002`: `-0.037`, `EXP0009` `PP0003`: `-0.018` on `TrackA`; `EXP0012` `PP0002`: `-0.027` on `TrackC`), refuting blanket `CLAHE` prescriptions. Conversely, **preserving spatial resolution (`PP0004` `1280px` vs `PP0001` `640px`)** delivered consistent held-out `test` gains on BOTH tested tracks: **`+0.0449` `mAP@0.50` & `+20.2%` relative `mAP@0.50:0.95`** on `TrackD` (`0.4868` vs `0.4419`, non-overlapping `mAP50-95` `95% CIs`: `[0.2025, 0.2495]` vs `[0.1659, 0.2085]`) and **`+0.0350` internal / `+0.0622` external `mAP@0.50`** (`+22.5%` relative external `mAP50-95`) on `TrackA`. | `EXP0001`, `EXP0004–0005`, `EXP0008–0012`, `EVAL0001–0004`, `EVAL0011–0012`, `CLAIM0016` |
| **`RQ3`** *(End-to-End GPU vs CPU Latency & Pareto Deployment Tradeoffs)* | Under serial `BS=1` `FP32` `UD14` timing (`0` failures), model-only GPU `FPS_infer` (`20.2–70.4`) exceeds true end-to-end `FPS_e2e` (`6.35–38.20`) by **`1.8×–5.6×`** because full-res decode/letterbox/autocrop overhead is substantial. On a standard laptop CPU (`Intel i5-1135G7`, `ONNXRuntime 1.32.0`, `0.983–0.997` PyTorch box parity IoU), `MODEL0008` (`TrackE@640`) runs in **`201.6 ms` (`4.96 FPS_e2e`)**, `MODEL0001` (`TrackA@640`) in `263.4 ms` (`3.80 FPS_e2e`), `MODEL0003` (`YOLO11m@640`) in `512.4 ms` (`1.95 FPS_e2e`), and `1280px` winners `MODEL0013` / `MODEL0005` in **`847.9–878.1 ms` (`1.14–1.18 FPS_e2e`)** — proving sub-second CPU interactive feasibility for non-clinical `S16` research demos without claiming clinical throughput clearance. | [timing_report.md](./timing_report.md), `09_Evaluation/timing/*.json`, `CLAIM0017` |

---

## 2. Master Consolidated Table (All `14` Held-Out Runs: Accuracy + Uncertainty + GPU/CPU Speed)

All values reconciled directly from `09_Evaluation/EVAL0001..EVAL0014/{metrics.csv, metrics_summary.json, coverage.csv}` and `09_Evaluation/timing/*_{gpu,cpu_onnx}_timing.json`. Fixed evaluation settings: `metric_conf_floor = 0.001`, class-aware `nms_iou = 0.65`, `agnostic_nms = false`, `max_det = 300`, `matching_iou = 0.50` & `[0.50:0.05:0.95]`, `1,000`-resample `GroupID` cluster bootstrap `95% CI` (`seed = 20261131`), validation-only frozen `conf_op`.

| `EvalID` | `ModelID` (`Arch@imgsz`) | `Release:Partition` (`OPGs / Boxes`) | `conf_op` | `val mAP@50` *(sel. only)* | **Test `mAP@0.50` (`95% CI`)** | **Test `mAP@0.50:95` (`95% CI`)** | `Macro-P` | `Macro-R` | `Macro-F1` | **GPU `FPS_e2e`** (`T4`) | **CPU `FPS_e2e`** (`i5 ONNX`) |
|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| **`EVAL0001`** | **`MODEL0005`** (`YOLO11s@1280`, **TrackA Win**) | `REL0001:test` (`208 / 2,888`) | `0.227` | `0.3906` | **`0.4165`** `[0.380, 0.474]` | **`0.1741`** `[0.155, 0.206]` | `0.5336` | `0.4493` | `0.4692` | `9.24` | `1.14` |
| **`EVAL0002`** | **`MODEL0005`** (`YOLO11s@1280`, **TrackA Ext**) | `REL0001:external_test` (`178 / 2,925`) | `0.227` | `0.3906` | **`0.4338`** `[0.390, 0.516]` | **`0.2038`** `[0.181, 0.254]` | `0.4997` | `0.4819` | `0.4631` | `9.24` | `1.14` |
| `EVAL0003` | `MODEL0001` (`YOLO11s@640`, TrackA Ref) | `REL0001:test` (`208 / 2,888`) | `0.238` | `0.3792` | `0.3815` `[0.347, 0.434]` | `0.1577` `[0.141, 0.185]` | `0.5001` | `0.4462` | `0.4652` | `14.00` | `3.80` |
| `EVAL0004` | `MODEL0001` (`YOLO11s@640`, TrackA Ext Ref) | `REL0001:external_test` (`178 / 2,925`) | `0.238` | `0.3792` | `0.3716` `[0.325, 0.458]` | `0.1663` `[0.143, 0.217]` | `0.4971` | `0.4265` | `0.4623` | `14.00` | `3.80` |
| `EVAL0005` | `MODEL0002` (`YOLOv8s@640`, TrackA Ref) | `REL0001:test` (`208 / 2,888`) | `0.197` | `0.3637` | `0.3786` `[0.342, 0.440]` | `0.1578` `[0.142, 0.187]` | `0.5278` | `0.4317` | `0.4798` | `13.42` | `3.76` |
| `EVAL0006` | `MODEL0002` (`YOLOv8s@640`, TrackA Ext Ref) | `REL0001:external_test` (`178 / 2,925`) | `0.197` | `0.3637` | `0.4177` `[0.367, 0.500]` | `0.1848` `[0.162, 0.233]` | `0.5692` | `0.4530` | `0.5324` | `13.42` | `3.76` |
| `EVAL0007` | `MODEL0003` (`YOLO11m@640`, TrackA Ref) | `REL0001:test` (`208 / 2,888`) | `0.253` | `0.3906` | `0.3990` `[0.364, 0.454]` | `0.1682` `[0.153, 0.196]` | `0.5010` | `0.4457` | `0.4612` | `13.14` | `1.95` |
| `EVAL0008` | `MODEL0003` (`YOLO11m@640`, TrackA Ext Ref) | `REL0001:external_test` (`178 / 2,925`) | `0.253` | `0.3906` | `0.4449` `[0.394, 0.521]` | `0.1940` `[0.172, 0.230]` | `0.6108` | `0.4522` | `0.5510` | `13.14` | `1.95` |
| **`EVAL0009`** | **`MODEL0004`** (`YOLO11s@640`, **TrackB Win**) | `REL0002:test` (`106 / 530`) | `0.210` | `0.4438` | **`0.4397`** `[0.399, 0.496]` | **`0.2673`** `[0.242, 0.310]` | `0.4757` | `0.4569` | `0.4466` | `13.78` | *N/A* |
| **`EVAL0010`** | **`MODEL0006`** (`YOLO11s@640`, **TrackC Win**) | `REL0003:test` (`33 / 182`) | `0.075` | `0.2588` | **`0.2508`** *(5-cls `0.2631`)* | **`0.1406`** *(5-cls `0.1465`)* | `0.2545` | `0.2785` | `0.2600` | `38.20` | *N/A* |
| **`EVAL0011`** | **`MODEL0013`** (`YOLO11s@1280`, **TrackD Win**) | `REL0004:test` (`578 / 999`) | `0.201` | `0.5360` | **`0.4868`** `[0.453, 0.531]` | **`0.2207`** `[0.203, 0.250]` | `0.4950` | `0.5242` | `0.5087` | `11.06` | `1.18` |
| `EVAL0012` | `MODEL0010` (`YOLO11s@640`, TrackD Ref) | `REL0004:test` (`578 / 999`) | `0.205` | `0.4878` | `0.4419` `[0.405, 0.486]` | `0.1836` `[0.166, 0.209]` | `0.5024` | `0.4750` | `0.4861` | `17.77` | `5.50` |
| **`EVAL0013`** | **`MODEL0008`** (`YOLO11s@640`, **TrackE Win**) | `REL0005:test` (`133 / 1,048`) | `0.379` | `0.8580` | **`0.8246`** `[0.791, 0.859]` | **`0.5163`** `[0.491, 0.548]` | `0.8483` | `0.8076` | `0.8238` | `12.28` | `4.96` |
| **`EVAL0014`** | **`MODEL0007`** (`YOLO11s@640`, **TrackF Win**) | `REL0006:test` (`24 / 137`) | `0.091` | `0.0991` | **`0.0537`** `[0.026, 0.106]` | **`0.0111`** `[0.005, 0.025]` | `0.1412` | `0.1052` | `0.1197` | `6.35` | *N/A* |

---

## 3. Complete Disclosure of Unfavorable, Excluded & Boundary Results (`OS §7.1` / `§9`)

1. **Excluded `RQ2` `CLAHE` Models (Not Advanced to Sealed Test):** `EXP0008`/`MODEL0011` (`PP0002`, `val mAP@0.50 = 0.344`, `-0.037`), `EXP0009`/`MODEL0012` (`PP0003`, `0.363`, `-0.018`), and `EXP0012`/`MODEL0009` (`PP0002` on Dhaka, `0.232`, `-0.027`) all failed to beat their matched raw controls on validation and were excluded at `G11` prior to test access.
2. **Low-Support & Unfavorable Held-Out Results Retained in Full:**
   - `TrackF` (`EVAL0014`, `MODEL0007`, pediatric mixed dentition, `121` train / `24` test OPGs): `mAP@0.50 = 0.0537` (`Proximal = 0.0823`, `Occlusal = 0.0252`) — honestly establishes the low-sample mixed-dentition physical ceiling at `640px`.
   - `TrackC` (`EVAL0010`, `MODEL0006`, Dhaka handheld-photographed OPGs, `33` test OPGs): `Fractured_Tooth` (`GT = 2`) scored `0.0000` and `Infection_Tooth` (`GT = 6`) scored `0.0016`, whereas `Impacted_Tooth` reached `0.6601` and `BDC_BDR` reached `0.4505`.
   - `TrackA` (`EVAL0001–0002`): Ultra-rare `Apical_Surgery` (`GT = 10` internal / `17` external) scored `0.0428` / `0.0055`, and diffuse `Bone_Resorption` scored `0.0906` / `0.1891`; on `external_test`, `Surgical_Device` had only `GT = 5` boxes (`0.0105`).
   - `HC01`/`HC02` zero-shot cross-country shift: `Periapical` (`0.1779–0.2355`) and `Caries` (`0.1627–0.1635`) collapsed sharply across country/scanner domains, proving that high in-domain metrics cannot be extrapolated to unseen hospitals without external verification.
3. **Deviations & Minor Artifact Notes (`NONE` Material Deviations):**
   - Zero protocol, threshold, split, or checkpoint deviations occurred after `FREEZE0001`.
   - At `metric_conf_floor = 0.001`, `2` zero-area letterbox-padding noise boxes out of `267,561` total score-floor predictions (`1` in `EVAL0001`, `1` in `EVAL0007`) collapsed to zero area upon `inverse_transform_box` clipping and were transparently filtered (`0` invalid boxes persisted).
   - Conditional `3`-seed `TrackA` sensitivity check (`DEC0015`) was not executed to preserve Kaggle GPU quota; uncertainty is rigorously quantified via `1,000`-resample `GroupID` cluster bootstrap `95% CI` across all `14` evaluations (`seed = 20261131`).
4. **Comparison Caveats (`OS §9`):**
   - Do **not** rank `TrackA–TrackF` numerically against each other as if they shared one label taxonomy or box granularity (focal lesion AABBs in `TrackA`/`TrackD`/`TrackF` vs whole-tooth AABBs in `TrackB`/`TrackC`/`TrackE`).
   - Do **not** treat our leak-free deduplicated scores as directly comparable to published studies using pre-split augmentation (`P0011` vs `P0008`), non-deduplicated official splits (`DS0001` `27.5%` official val leak), or 3D CBCT / intraoral bitewing modalities (`CLAIM0006`, `CLAIM0010`).
   - All results are strictly **non-clinical research benchmarks**; no diagnostic sensitivity or clinical decision clearance is claimed.

---

## 4. Complete Artifact & Provenance Index

- **Freeze & Custody:** [freeze.md](./freeze.md) · [freeze_manifest.json](./freeze_manifest.json) · [step032_bundle_manifest.json](./step032_bundle_manifest.json) · [step032_validation_report.md](./step032_validation_report.md)
- **Quantitative Metrics & Uncertainty:** [step033_final_metrics_report.md](./step033_final_metrics_report.md) · `09_Evaluation/EVAL0001..EVAL0014/{metrics.csv, metrics_summary.json, coverage.csv, run_manifest.json}` · [xshift_metrics.csv](./xshift_metrics.csv) · [xshift_metrics_summary.json](./xshift_metrics_summary.json)
- **Speed & Hardware Timing:** [timing_report.md](./timing_report.md) · `09_Evaluation/timing/*_{gpu,cpu_onnx}_timing.json` · `09_Evaluation/timing/*_cpu_raw_samples.csv`
- **Reconciliation & Gate Audit:** [g12_reconciliation_audit.json](./g12_reconciliation_audit.json) · [evaluation_registry.csv](./evaluation_registry.csv) · [G12_assessment_2026-11-21.md](../01_Project_Management/reviews/G12_assessment_2026-11-21.md) · [claims.csv](../02_Literature/claims.csv)
