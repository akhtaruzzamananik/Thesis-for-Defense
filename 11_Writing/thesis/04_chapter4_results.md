# Chapter 4: Experimental Results (`WRIT0005`)

All quantitative results in this chapter are strictly single-pass held-out evaluations executed under `FREEZE0001 v1.0.0` (`G11 PASS`, `0` prior test exposure) over `1,260` canonical held-out 2D OPG radiographs (`1,082` internal `test` + `178` unseen external-hospital `external_test`, `0` cross-partition `GroupID` leaks). Every metric was computed in original source radiograph pixel coordinates (`[W, H]`) using frozen `src/opg/evaluator.py` (`sha256: 8fa2c6d8...`, `metric_conf_floor = 0.001`, class-aware `NMS IoU = 0.65`, `max_det = 300`, continuous all-point AP integration, empty radiographs retained, zero-GT classes excluded from averaging) and programmatically reconciled by `g12_reconciliation_audit.json` (`14/14` evaluations, `128/128` per-class `TP + FN == GT` checks, `12/12` `XSHIFT` bridges, `10` GPU + `7` CPU timing logs; `G12 PASS`). Uncertainty intervals are `1,000`-resample `GroupID` cluster bootstrap `95%` confidence intervals (`seed = 20261131`).

---

## 4.1 Official Held-Out Final-Test Scoreboard (`RQ0`, `CLAIM0013`)

Table `TAB0004` (visualized with bootstrap uncertainty bars in Figure `FIG0002`) presents the complete held-out performance across all `14` frozen evaluations (`EVAL0001–EVAL0014`), comprising the `6` independent track winners (`MODEL0005`, `MODEL0004`, `MODEL0006`, `MODEL0013`, `MODEL0008`, `MODEL0007`) and `4` predeclared `RQ1`/`RQ2`/`RQ3` comparators (`MODEL0001`, `MODEL0002`, `MODEL0003`, `MODEL0010`), evaluated at each model's validation-locked operating confidence threshold `conf_op`.

| `EvalID` | `ModelID` (`Arch@imgsz`) | `Release:Partition` (`OPGs / Boxes`) | `conf_op` | `val mAP@50` *(sel. only)* | **Held-Out `mAP@0.50` (`95% CI`)** | **Held-Out `mAP@0.50:95` (`95% CI`)** | `Macro-P` | `Macro-R` | `Macro-F1` | `Micro-F1` (`@0.25`) |
|---|---|---|---:|---:|---|---|---:|---:|---:|---:|
| **`EVAL0001`** | **`MODEL0005`** (`YOLO11s@1280`, **TrackA Win**) | `REL0001:test` (`208 / 2,888`) | `0.227` | `0.3906` | **`0.4165`** `[0.3797, 0.4744]` | **`0.1741`** `[0.1547, 0.2058]` | `0.5336` | `0.4493` | `0.4692` | `0.5404` (`0.5445`) |
| **`EVAL0002`** | **`MODEL0005`** (`YOLO11s@1280`, **TrackA Ext**) | `REL0001:external_test` (`178 / 2,925`) | `0.227` | `0.3906` | **`0.4338`** `[0.3901, 0.5155]` | **`0.2038`** `[0.1806, 0.2544]` | `0.4997` | `0.4819` | `0.4631` | `0.5616` (`0.5627`) |
| `EVAL0003` | `MODEL0001` (`YOLO11s@640`, TrackA Ref) | `REL0001:test` (`208 / 2,888`) | `0.238` | `0.3792` | `0.3815` `[0.3467, 0.4338]` | `0.1577` `[0.1410, 0.1847]` | `0.5001` | `0.4462` | `0.4652` | `0.5020` (`0.5033`) |
| `EVAL0004` | `MODEL0001` (`YOLO11s@640`, TrackA Ext Ref) | `REL0001:external_test` (`178 / 2,925`) | `0.238` | `0.3792` | `0.3716` `[0.3251, 0.4582]` | `0.1663` `[0.1433, 0.2171]` | `0.4971` | `0.4265` | `0.4623` | `0.5203` (`0.5193`) |
| `EVAL0005` | `MODEL0002` (`YOLOv8s@640`, TrackA Ref) | `REL0001:test` (`208 / 2,888`) | `0.197` | `0.3637` | `0.3786` `[0.3422, 0.4396]` | `0.1578` `[0.1418, 0.1869]` | `0.5278` | `0.4317` | `0.4798` | `0.5029` (`0.5082`) |
| `EVAL0006` | `MODEL0002` (`YOLOv8s@640`, TrackA Ext Ref) | `REL0001:external_test` (`178 / 2,925`) | `0.197` | `0.3637` | `0.4177` `[0.3674, 0.4995]` | `0.1848` `[0.1617, 0.2331]` | `0.5692` | `0.4530` | `0.5324` | `0.5472` (`0.5373`) |
| `EVAL0007` | `MODEL0003` (`YOLO11m@640`, TrackA Ref) | `REL0001:test` (`208 / 2,888`) | `0.253` | `0.3906` | `0.3990` `[0.3642, 0.4540]` | `0.1682` `[0.1525, 0.1955]` | `0.5010` | `0.4457` | `0.4612` | `0.5303` (`0.5289`) |
| `EVAL0008` | `MODEL0003` (`YOLO11m@640`, TrackA Ext Ref) | `REL0001:external_test` (`178 / 2,925`) | `0.253` | `0.3906` | `0.4449` `[0.3942, 0.5210]` | `0.1940` `[0.1721, 0.2302]` | `0.6108` | `0.4522` | `0.5510` | `0.5514` (`0.5516`) |
| **`EVAL0009`** | **`MODEL0004`** (`YOLO11s@640`, **TrackB Win**) | `REL0002:test` (`106 / 530`) | `0.210` | `0.4438` | **`0.4397`** `[0.3985, 0.4958]` | **`0.2673`** `[0.2418, 0.3100]` | `0.4757` | `0.4569` | `0.4466` | `0.4705` (`0.4760`) |
| **`EVAL0010`** | **`MODEL0006`** (`YOLO11s@640`, **TrackC Win**) | `REL0003:test` (`33 / 182`) | `0.075` | `0.2588` | **`0.2508`** `[0.2024, 0.3414]` | **`0.1406`** `[0.1155, 0.1991]` | `0.2545` | `0.2785` | `0.2600` | `0.3333` (`0.3364`) |
| **`EVAL0011`** | **`MODEL0013`** (`YOLO11s@1280`, **TrackD Win**) | `REL0004:test` (`578 / 999`) | `0.201` | `0.5360` | **`0.4868`** `[0.4527, 0.5307]` | **`0.2207`** `[0.2025, 0.2495]` | `0.4950` | `0.5242` | `0.5087` | `0.5560` (`0.5518`) |
| `EVAL0012` | `MODEL0010` (`YOLO11s@640`, TrackD Ref) | `REL0004:test` (`578 / 999`) | `0.205` | `0.4878` | `0.4419` `[0.4050, 0.4859]` | `0.1836` `[0.1659, 0.2085]` | `0.5024` | `0.4750` | `0.4861` | `0.5063` (`0.5025`) |
| **`EVAL0013`** | **`MODEL0008`** (`YOLO11s@640`, **TrackE Win**) | `REL0005:test` (`133 / 1,048`) | `0.379` | `0.8580` | **`0.8246`** `[0.7907, 0.8592]` | **`0.5163`** `[0.4912, 0.5482]` | `0.8483` | `0.8076` | `0.8238` | `0.8395` (`0.8316`) |
| **`EVAL0014`** | **`MODEL0007`** (`YOLO11s@640`, **TrackF Win**) | `REL0006:test` (`24 / 137`) | `0.091` | `0.0991` | **`0.0537`** `[0.0263, 0.1055]` | **`0.0111`** `[0.0049, 0.0249]` | `0.1412` | `0.1052` | `0.1197` | `0.1441` (`0.1222`) |

Four primary observations emerge directly from `EVAL0001–EVAL0014`:

1. **Close Validation-to-Test Calibration (`0` Leakage):** Across all `6` independent tracks, held-out `test` metrics track validation metrics closely without catastrophic overfitting—for example, `TrackB` `0.4397` vs `0.4438 val`, `TrackC` `0.2508` vs `0.2588 val`, `TrackE` `0.8246` vs `0.8580 val`, and `TrackA` `MODEL0005` `0.4165` (`external_test = 0.4338`) vs `0.3906 val`—confirming that connected-component `GroupID` splitting (`SPLIT0001–SPLIT0006`) eliminated the `27.5%` duplicate contamination present in official splits (`CLAIM0010`, `CLAIM0013`). Furthermore, `Micro-F1` at frozen `conf_op` differs from protocol fallback `conf = 0.25` by at most `0.022`, verifying threshold stability.
2. **TrackC Dual Reporting (`DEC0013`):** On the Dhaka handheld-photographed cohort (`REL0003`, `33` test OPGs), reporting strictly the `5` pathology classes (`0..4`, excluding selectively annotated `Healthy_Tooth`) yields **`mAP@0.50 = 0.2631`** (`95% CI [0.2040, 0.3782]`), **`mAP@0.50:0.95 = 0.1465`** (`[0.1173, 0.2158]`), and `Macro-F1 = 0.2510`, versus `6`-class **`0.2508`** / **`0.1406`**.
3. **Honest Disclosure of Small-N Pediatric Ceiling (`TrackF`):** On `REL0006` (MD-OPG pediatric mixed dentition, `121` train / `24` test OPGs, `100%` focal lesions `< 0.2%` image area), `MODEL0007` reached only **`mAP@0.50 = 0.0537`** (`[0.0263, 0.1055]`, `mAP@0.50:0.95 = 0.0111`). This negative boundary result is retained in full (`OS §7.1`) and analyzed mechanistically in Chapter 5.
4. **Non-Comparability Across Granularity Tiers:** `TrackE` (`0.8246`, whole-tooth boxes on a single consistent UAE digital scanner) and `TrackA` (`0.4165`, `13` predominantly focal lesion-level classes across mixed devices) measure fundamentally distinct box-granularity regimes; cross-track numerical ranking is methodologically invalid (`CLAIM0013`).

---

## 4.2 Per-Class Radiographic Contrast Hierarchy & Architecture Comparisons (`RQ1`, `CLAIM0014`)

Inspecting all `34` active classes across the `6` track winners (complete per-class tables in Appendix C) confirms a sharp **radiographic contrast and structural-size hierarchy** (`CLAIM0014`, corroborating literature synthesis `CLAIM0002` [Mureanu2024_P0023; Peng2026_P0009; Dehghani2025_P0014; AlabdAljabar2026_P0026]):

- **Tier 1 — High-Contrast Metallic Hardware & Impacted Structures (`AP@0.50 = 0.73–0.998`):**
  - `TrackE` (`EVAL0013`): `Implant = 0.9980` (`80/80` recall, `F1 = 0.9756`, `AP@0.50:95 = 0.5991`), `Crowned_Tooth = 0.9203` (`F1 = 0.9314`), `Filled_Tooth = 0.8792`, `Impacted_Tooth = 0.8287`, `Retained_Root = 0.7792`.
  - `TrackA`: `Surgical_Device = 0.8567` (internal), `Endodontic_Treatment = 0.6825` internal / `0.7323` external, `Implant = 0.5641` internal / `0.9297` external (`15/16` recall), `Impacted_Tooth = 0.4945` internal / `0.7629` external.
  - `TrackB` (`EVAL0009`): `Impacted = 0.9012` (`F1 = 0.8649`, `AP@0.50:95 = 0.5314`).
  - `TrackC` (`EVAL0010`): Even on handheld-photographed film radiographs, `Impacted_Tooth` reached `0.6601` (`F1 = 0.6000`) and `BDC_BDR` reached `0.4505`.
- **Tier 2 — Moderate-Contrast Focal Restorations & Ordinal Apical Lesions (`AP@0.50 = 0.31–0.62`):**
  - `TrackA`: `Prosthetic_Restoration = 0.5384` / `0.5725`, `Obturation = 0.5315` / `0.6203`, `Root_Fragment = 0.4939` / `0.3486`, `Carious_Lesion = 0.3303` / `0.2779`, `Apical_Periodontitis = 0.3078` / `0.2249`.
  - `TrackD` (`EVAL0011`, `1280px`): Monotonic severity gradient across `PAI` classes—`PAI_3 = 0.5878` (`GT = 633`, `F1 = 0.5939`), `PAI_4 = 0.4976` (`GT = 260`, `F1 = 0.5195`), and `PAI_5 = 0.3751` (`GT = 106`, `F1 = 0.4126`).
  - `TrackB`: `Deep_Caries = 0.3435`, `Caries = 0.3385`, while minority `Periapical_Lesion` (`GT = 24`) dropped to `0.1759`.
  - `TrackE`: `Cavitated_Tooth = 0.5420` (`Recall = 0.4677`), the sole radiolucent pathology class in `TrackE`, lagged metallic/structural classes by `0.24–0.46` AP.
- **Tier 3 — Diffuse Low-Contrast & Ultra-Rare Findings (`AP@0.50 < 0.22`):**
  - Diffuse periodontal defects: `TrackA Bone_Resorption = 0.0906` internal / `0.1891` external (`Recall = 0.0949` / `0.0798`), `Furcation_Lesion = 0.1785` / `0.2153`.
  - Ultra-rare classes: `TrackA Apical_Surgery = 0.0428` (`GT = 10`) / `0.0055` (`GT = 17`), `TrackA External Surgical_Device = 0.0105` (`GT = 5`), `TrackC Infection_Tooth = 0.0016` (`GT = 6`), `TrackC Fractured_Tooth = 0.0000` (`GT = 2`).
  - Mixed-dentition small focal caries: `TrackF Proximal_Caries = 0.0823` (`GT = 110`), `Occlusal_Caries = 0.0252` (`GT = 27`).

**Controlled Architecture & Scale Comparison on `TrackA` (`640px` vs `1280px`, `RQ1`):** Holding `REL0001`, `PP0001` (`640px`), seed, and optimizer constant:
- **`YOLO11s` (`MODEL0001`, `9.4M` params) vs `YOLOv8s` (`MODEL0002`, `11.2M` params):** On internal `test`, `YOLO11s` marginally exceeded `YOLOv8s` in `mAP@0.50` (`0.3815` vs `0.3786`) with virtually identical `mAP@0.50:0.95` (`0.1577` vs `0.1578`) and `16%` fewer parameters; on `external_test`, `YOLOv8s` recorded higher point estimates (`0.4177` vs `0.3716`) with broadly overlapping `95% CIs` (`[0.3674, 0.4995]` vs `[0.3251, 0.4582]`).
- **`YOLO11m` (`MODEL0003`, `20.1M` params, `640px`) vs `YOLO11s@1280` (`MODEL0005`, `9.4M` params, `1280px`):** Doubling parameter count at `640px` raised internal `mAP@0.50` by `+0.0175` (`0.3990` vs `0.3815`) and external `mAP@0.50` to `0.4449`, whereas keeping the compact `9.4M`-parameter `YOLO11s` backbone and doubling input resolution to `1280px` (`MODEL0005`) achieved higher internal `mAP@0.50` (**`0.4165`** vs `0.3990`), higher internal `mAP@0.50:0.95` (**`0.1741`** vs `0.1682`), and higher external strict localization `mAP@0.50:0.95` (**`0.2038`** vs `0.1940`) at **half the checkpoint footprint** (`18.4 MB` vs `38.7 MB` `.pt`).

---

## 4.3 Controlled `RQ2` Preprocessing Ablation: `CLAHE` Failure vs `1280px` Resolution Gain (`CLAIM0016`)

Figure `FIG0003` and Table `TAB0005` synthesize the controlled `RQ2` ablation designed to resolve literature contradiction `CLAIM0008` [CH2026_P0004; Scarano2026_P0011; Nayak2026_P0029; Gwak2024_P0038] versus spatial-resolution hypothesis `CLAIM0009` [Oztekin2026_P0008; Eftimie2025_P0015]:

| Controlled Comparison (`Track`, Fixed `YOLO11s` + Seed `20261124`) | Control (`PP0001` Raw `640px`) | Treatment (`PP0002`/`PP0003`/`PP0004`) | `Δ mAP@0.50` | `Δ mAP@0.50:95` | Partition / Custody |
|---|---|---|---:|---:|---|
| `EXP0008` vs `EXP0001` (`TrackA`, `CLAHE 2.0, 8×8`) | `0.381` (`val`) | `0.344` (`val`) | **`-0.037`** | `-0.015` | Validation (Excluded at `G11`) |
| `EXP0009` vs `EXP0001` (`TrackA`, `CLAHE 3.0, 16×16`) | `0.381` (`val`) | `0.363` (`val`) | **`-0.018`** | `-0.008` | Validation (Excluded at `G11`) |
| `EXP0012` vs `EXP0004` (`TrackC`, `CLAHE 2.0, 8×8`) | `0.259` (`val`) | `0.232` (`val`) | **`-0.027`** | `-0.016` | Validation (Excluded at `G11`) |
| `EVAL0001` vs `EVAL0003` (`TrackA:test`, `PP0004` `1280px`) | `0.3815` `[0.347, 0.434]` | **`0.4165`** `[0.380, 0.474]` | **`+0.0350`** | **`+0.0164`** (`+10.4%` rel.) | Held-out sealed `test` |
| `EVAL0002` vs `EVAL0004` (`TrackA:ext`, `PP0004` `1280px`) | `0.3716` `[0.325, 0.458]` | **`0.4338`** `[0.390, 0.516]` | **`+0.0622`** | **`+0.0375`** (`+22.5%` rel.) | Held-out `external_test` |
| `EVAL0011` vs `EVAL0012` (`TrackD:test`, `PP0004` `1280px`) | `0.4419` `[0.405, 0.486]` | **`0.4868`** `[0.453, 0.531]` | **`+0.0449`** | **`+0.0371`** (`+20.2%` rel.) | Held-out sealed `test` *(non-overlapping `mAP50-95` `95% CI`)* |

- **Empirical Refutation of Blanket `CLAHE` (`3/3` Failures):** Under locked splits and hyperparameters, luminance `CLAHE` degraded validation `mAP@0.50` in **every single trial** (`-0.037` and `-0.018` on digital Romanian OPGs; `-0.027` even on low-contrast handheld-photographed Dhaka OPGs). Qualitatively, local histogram equalization amplifies trabecular bone noise and ghost-shadow borders into false-positive textures while distorting subtle radiodensity gradients between dentin and radiolucent caries. All three `CLAHE` checkpoints (`MODEL0009`, `MODEL0011`, `MODEL0012`) were properly excluded at `G11` without touching sealed test sets.
- **Consistent Held-Out Gain from Spatial Resolution (`1280px`):** Preserving spatial detail via `PP0004` (`1280×1280` raw letterbox) improved held-out accuracy across **every tested cohort and metric**, delivering **`+0.0449` `mAP@0.50`** and **`+20.2%` relative `mAP@0.50:0.95`** on `TrackD` Hanoi (`578` OPGs, with strictly **non-overlapping `95% CIs`** on `mAP@0.50:0.95`: `[0.2025, 0.2495]` vs `[0.1659, 0.2085]`) and **`+0.0350` internal / `+0.0622` external `mAP@0.50`** (`+22.5%` relative external `mAP@0.50:0.95`) on `TrackA`.

---

## 4.4 Zero-Shot Cross-Country Domain-Shift Bridges (`HC01–HC05`, `RQ1`, `CLAIM0015`)

Directly addressing the `87.7%` lack of external validation reported in [Hartman2026_P0027], we executed `12` zero-shot cross-country bridges (`XSHIFT01–XSHIFT06`, Table `TAB0006`, Figure `FIG0004`) across five countries (`Romania`, `Türkiye`, `Bangladesh`, `Vietnam`, `UAE`) using frozen source checkpoints and frozen source `conf_op` with zero target-domain retraining or threshold tuning:

| `BridgeID` | Source -> Target Country (`Model -> Release:Part`) | Concept | `GT` | `Precision` | `Recall` | `F1` | **`AP@0.50`** | `AP@0.50:95` |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `XSHIFT04_A` | Romania -> Türkiye (`MODEL0005 -> REL0002:test`) | `HC03_Impacted_Tooth` | `91` | `0.9155` | `0.7143` | `0.8025` | **`0.8181`** | `0.4083` |
| `XSHIFT03_A` | Romania -> Bangladesh (`MODEL0005 -> REL0003:test`) | `HC03_Impacted_Tooth` | `30` | `0.7727` | `0.5667` | `0.6538` | **`0.7109`** | `0.3752` |
| `XSHIFT04_E` | UAE -> Türkiye (`MODEL0008 -> REL0002:test`) | `HC03_Impacted_Tooth` | `91` | `0.8723` | `0.4505` | `0.5942` | **`0.6967`** | `0.3472` |
| `XSHIFT01` | Romania -> UAE (`MODEL0005 -> REL0005:test`) | `HC03_Impacted_Tooth` | `71` | `0.7442` | `0.4507` | `0.5614` | **`0.6116`** | `0.2513` |
| `XSHIFT02_EXT` | UAE -> Romania Ext (`MODEL0008 -> REL0001:ext`) | `HC03_Impacted_Tooth` | `111` | `0.6180` | `0.4955` | `0.5500` | **`0.4935`** | `0.2242` |
| `XSHIFT03_E` | UAE -> Bangladesh (`MODEL0008 -> REL0003:test`) | `HC03_Impacted_Tooth` | `30` | `0.7333` | `0.3667` | `0.4889` | **`0.4469`** | `0.2418` |
| `XSHIFT02_INT` | UAE -> Romania Int (`MODEL0008 -> REL0001:test`) | `HC03_Impacted_Tooth` | `133` | `0.6489` | `0.4586` | `0.5374` | **`0.3814`** | `0.1684` |
| `XSHIFT03_E` | UAE -> Bangladesh (`MODEL0008 -> REL0003:test`) | `HC04_Residual_Root` | `15` | `0.5385` | `0.4667` | `0.5000` | **`0.5055`** | `0.2245` |
| `XSHIFT01` | Romania -> UAE (`MODEL0005 -> REL0005:test`) | `HC04_Residual_Root` | `140` | `0.6338` | `0.3214` | `0.4265` | **`0.3816`** | `0.1195` |
| `XSHIFT02_EXT` | UAE -> Romania Ext (`MODEL0008 -> REL0001:ext`) | `HC04_Residual_Root` | `93` | `0.4109` | `0.5699` | `0.4775` | **`0.3152`** | `0.1158` |
| `XSHIFT02_INT` | UAE -> Romania Int (`MODEL0008 -> REL0001:test`) | `HC04_Residual_Root` | `178` | `0.3970` | `0.4438` | `0.4191` | **`0.2420`** | `0.0726` |
| `XSHIFT03_A` | Romania -> Bangladesh (`MODEL0005 -> REL0003:test`) | `HC04_Residual_Root` | `15` | `0.2222` | `0.1333` | `0.1667` | **`0.0844`** | `0.0178` |
| `XSHIFT02_EXT` | UAE -> Romania Ext (`MODEL0008 -> REL0001:ext`) | `HC05_Dental_Implant` | `16` | `0.3548` | `0.6875` | `0.4681` | **`0.4626`** | `0.1970` |
| `XSHIFT01` | Romania -> UAE (`MODEL0005 -> REL0005:test`) | `HC05_Dental_Implant` | `80` | `0.4396` | `0.5000` | `0.4678` | **`0.3189`** | `0.1229` |
| `XSHIFT02_INT` | UAE -> Romania Int (`MODEL0008 -> REL0001:test`) | `HC05_Dental_Implant` | `70` | `0.1772` | `0.2000` | `0.1879` | **`0.0723`** | `0.0350` |
| `XSHIFT05_A2D` | Romania -> Vietnam (`MODEL0005 -> REL0004:test`) | `HC02_Periapical_Lesion` | `999` | `0.6471` | `0.0991` | `0.1719` | **`0.2355`** | `0.0573` |
| `XSHIFT05_D2A_EXT` | Vietnam -> Romania Ext (`MODEL0013 -> REL0001:ext`) | `HC02_Periapical_Lesion` | `106` | `0.1873` | `0.4717` | `0.2681` | **`0.2163`** | `0.0602` |
| `XSHIFT05_D2A_INT` | Vietnam -> Romania Int (`MODEL0013 -> REL0001:test`) | `HC02_Periapical_Lesion` | `142` | `0.1781` | `0.3662` | `0.2396` | **`0.1779`** | `0.0517` |
| `XSHIFT06_E2C` | UAE -> Bangladesh (`MODEL0008 -> REL0003:test`) | `HC01_WholeTooth_Caries` | `30` | `0.3636` | `0.2667` | `0.3077` | **`0.1635`** | `0.0909` |
| `XSHIFT06_E2B` | UAE -> Türkiye (`MODEL0008 -> REL0002:test`) | `HC01_WholeTooth_Caries` | `415` | `0.7818` | `0.1036` | `0.1830` | **`0.1627`** | `0.0919` |

The cross-country shift evidence reveals a striking **structural-versus-radiolucent generalization divide** (`CLAIM0015`):
1. **High-Contrast Structural Generalization:** Without seeing a single Turkish or Bangladeshi radiograph during training, Romanian `MODEL0005` achieved **`AP@0.50 = 0.8181`** (`F1 = 0.8025`) on `HC03 Impacted Tooth` in Türkiye (`REL0002`) and **`0.7109`** on handheld-photographed Dhaka films (`REL0003`), actually exceeding `TrackC`'s own small-sample in-domain detector (`0.6601`). Likewise, UAE `MODEL0008` reached `0.6967` on Türkiye `HC03` and `0.5055` on Dhaka `HC04 Residual Root`.
2. **Severe Radiolucency Domain Collapse:** Conversely, low-contrast pathologies collapsed across international scanner and annotation shifts: `HC02 Periapical Lesion` fell to **`0.1779–0.2355`** across Romania <-> Vietnam (vs `0.4868` in-domain `TrackD`), and `HC01 Whole-Tooth Caries` dropped from `0.5420` in-domain UAE to **`0.1627`** in Türkiye and **`0.1635`** in Dhaka (`Recall = 0.1036` on DENTEX due to conservative high `conf_op = 0.379` trained on UAE contrast).
3. **Asymmetric Hardware Box Convention Shift (`HC05`):** Although `MODEL0008` achieved `0.9980` on UAE implants (`whole-tooth/fixture+crown` OBB-derived AABBs), its zero-shot transfer to Romanian internal `DS0001` implants (`tight fixture-only` AABBs, often containing surgical miniplates as distractors) dropped to `0.0723` (`0.4626` on Romanian `external_test`), highlighting how subtle box-extent definitions depress IoU even for high-contrast titanium hardware.
4. **Protocol Consistency Mitigates Same-Country External Shift:** By contrast, when evaluated on an unseen Romanian hospital sharing the UMFIH annotation protocol (`REL0001:external_test`, `EVAL0002`), `MODEL0005` maintained `mAP@0.50 = 0.4338` (`mAP@0.50:0.95 = 0.2038`) versus `0.4165` (`0.1741`) internally, demonstrating that protocol alignment matters as much as raw scanner hardware.

---

## 4.5 Bounded End-to-End GPU vs CPU Latency & `RQ3` Pareto Frontier (`CLAIM0017`)

Table `TAB0005` and Figure `FIG0005` report serial single-image streaming latency (`batch_size = 1`, `FP32`, `10` warm-up OPGs discarded + up to `100` consecutive held-out test OPGs timed, `0` failures) across Kaggle `NVIDIA Tesla T4` GPU (`torch 2.11.0+cu130`, `ultralytics 8.3.253`, explicit `torch.cuda.synchronize()`) and a standard consumer laptop CPU (`11th Gen Intel Core i5-1135G7 @ 2.40 GHz`, `4C/8T`, `7.70 GiB RAM`, `Windows 11`, `onnxruntime 1.32.0` `CPUExecutionProvider`). Timing strictly defines `T_e2e = T_pre (decode + RGB + autocrop + letterbox) + T_infer + T_post (NMS + inverse TransformLedger)`, separating cold session load and disk I/O (`UD14`).

| `ModelID` (`Track`, `Arch@imgsz`) | `.pt` / `.onnx` (MB) | `test mAP@50` (`mAP50-95`) | **GPU `T_e2e` mean / p95 (ms)** | **GPU `FPS_e2e`** (`FPS_inf`) | **CPU `T_e2e` mean / p95 (ms)** | **CPU `FPS_e2e`** (`FPS_inf`) | CPU Cold Load (ms) | ONNX Parity IoU (`|Δs|`) |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| `MODEL0005` (`TrackA`, `YOLO11s@1280`) | `18.4` / `36.6` | `0.4165` (`0.1741`) | `108.2` / `118.7` | **`9.24`** (`20.20`) | `878.1` / `1224.0` | **`1.14`** (`1.24`) | `237.9` | `0.9923` (`0.0021`) |
| `MODEL0001` (`TrackA`, `YOLO11s@640`) | `18.3` / `36.2` | `0.3815` (`0.1577`) | `71.4` / `78.0` | **`14.00`** (`37.63`) | `263.4` / `402.7` | **`3.80`** (`4.92`) | `234.2` | `0.9954` (`0.0028`) |
| `MODEL0002` (`TrackA`, `YOLOv8s@640`) | `21.5` / `42.7` | `0.3786` (`0.1578`) | `74.5` / `81.5` | **`13.42`** (`34.12`) | `266.0` / `330.7` | **`3.76`** (`4.62`) | `213.9` | `0.9842` (`0.0061`) |
| `MODEL0003` (`TrackA`, `YOLO11m@640`) | `38.7` / `76.7` | `0.3990` (`0.1682`) | `76.1` / `82.6` | **`13.14`** (`32.03`) | `512.4` / `706.0` | **`1.95`** (`2.17`) | `460.8` | `0.9965` (`0.0016`) |
| `MODEL0004` (`TrackB`, `YOLO11s@640`) | `18.3` / *iso.* | `0.4397` (`0.2673`) | `72.6` / `77.9` | **`13.78`** (`36.46`) | *(NC-SA isolated)* | — | — | — |
| `MODEL0006` (`TrackC`, `YOLO11s@640`) | `18.3` / — | `0.2508` (`0.1406`) | `26.2` / `38.8` | **`38.20`** (`70.39`) | *(not exported)* | — | — | — |
| `MODEL0013` (`TrackD`, `YOLO11s@1280`) | `18.4` / `36.6` | `0.4868` (`0.2207`) | `90.4` / `93.1` | **`11.06`** (`20.75`) | `847.9` / `1002.0` | **`1.18`** (`1.27`) | `238.4` | `0.9941` (`0.0114`) |
| `MODEL0010` (`TrackD`, `YOLO11s@640`) | `18.3` / `36.1` | `0.4419` (`0.1836`) | `56.3` / `58.1` | **`17.77`** (`42.39`) | `181.9` / `215.4` | **`5.50`** (`7.07`) | `222.0` | `0.9829` (`0.0071`) |
| `MODEL0008` (`TrackE`, `YOLO11s@640`) | `18.3` / `36.1` | `0.8246` (`0.5163`) | `81.4` / `85.6` | **`12.28`** (`35.77`) | `201.6` / `225.5` | **`4.96`** (`7.08`) | `158.8` | `0.9942` (`0.0023`) |
| `MODEL0007` (`TrackF`, `YOLO11s@640`) | `18.3` / — | `0.0537` (`0.0111`) | `157.4` / `172.2` | **`6.35`** (`35.88`) | *(not exported)* | — | — | — |

Three deployment findings answer `RQ3` (`CLAIM0017`):
1. **Model-Only vs End-to-End Speed Discrepancy (`1.8×–5.6×`):** On `Tesla T4`, reporting model+NMS `FPS_infer` (`20.20–70.39 FPS`) exaggerates practical single-OPG throughput by **`1.8×–5.6×`** over true end-to-end `FPS_e2e` (`6.35–38.20 FPS`), because full-resolution panoramic decode (`~2000×1000 px`), letterboxing, and `DS0006` black-border autocrop consume `15–130 ms/OPG` on CPU. This explains the gap between bare GPU claims (`> 30 FPS`) and end-to-end clinical pipelines noted in `CLAIM0011–CLAIM0012` [Peng2026_P0009; Eftimie2025_P0015].
2. **Resolution Dominates Parameter Scaling on the Pareto Frontier:** On `TrackA`, `YOLO11s@1280` (`MODEL0005`, `36.6 MB` ONNX) outperforms `YOLO11m@640` (`MODEL0003`, `76.7 MB` ONNX) on internal `mAP@0.50` (`0.4165` vs `0.3990`) and external `mAP@0.50:0.95` (`0.2038` vs `0.1940`) at half the memory footprint, trading `108.2 ms` vs `76.1 ms` GPU `T_e2e` (`878.1 ms` vs `512.4 ms` CPU `T_e2e`).
3. **Sub-Second CPU Interactive Feasibility:** All `7` exported static `ONNX` (`opset = 17`) models match PyTorch GPU predictions with **`0.9829–0.9965` mean box IoU** and run interactively on a standard laptop CPU (`Intel i5-1135G7`, no GPU): `MODEL0008` (`TrackE@640`, `0.8246 mAP@0.50`) completes in **`201.6 ms` (`4.96 FPS_e2e`)**, `MODEL0010` (`TrackD@640`) in **`181.9 ms` (`5.50 FPS_e2e`)**, and `1280px` winners `MODEL0013` / `MODEL0005` in **`847.9–878.1 ms` (`1.14–1.18 FPS_e2e`)**—confirming non-clinical research web-showcase feasibility on free CPU tiers without claiming real-time video or clinical throughput clearance.
