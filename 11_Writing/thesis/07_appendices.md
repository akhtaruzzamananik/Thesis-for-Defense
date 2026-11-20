# Appendices (`WRIT0008`)

---

## Appendix A: Frozen `41`-Entry Class Ontology Summary (`CLS0001–CLS0041`)

Authoritative machine-readable ledger: `04_Annotations/classes.csv` (`v1.0.0`, `G05 PASS`, `sha256: c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`).

| Track / Role | Active `ClassID` Range | Granularity | Class Index -> Canonical Name (`Excluded Entries Noted`) |
|---|---|---|---|
| `TrackA` (`DS0001` UMFIH) | `CLS0001–CLS0014` (`13` active, `1` excluded) | Focal lesion / hardware AABB | `0`: `Implant`; `1`: `Prosthetic_Restoration`; `2`: `Obturation`; `3`: `Endodontic_Treatment`; `4`: `Carious_Lesion`; `5`: `Bone_Resorption`; `6`: `Impacted_Tooth`; `7`: `Apical_Periodontitis`; `8`: `Root_Fragment`; `9`: `Furcation_Lesion`; `10`: `Apical_Surgery`; `11`: `Orthodontic_Device`; `12`: `Surgical_Device`. *(Excluded: `CLS0012` `Root_Resorption`, `N = 5` train / `0` eval.)* |
| `TrackB` (`DS0002` DENTEX) | `CLS0015–CLS0018` (`4` active; `CC-BY-NC-SA` isolated) | Whole-tooth AABB | `0`: `Impacted`; `1`: `Caries`; `2`: `Periapical_Lesion`; `3`: `Deep_Caries`. |
| `TrackC` (`DS0003` Dhaka) | `CLS0019–CLS0024` (`6` active; dual 5/6-cls eval) | Whole-tooth AABB | `0`: `Caries_Tooth`; `1`: `Infection_Tooth`; `2`: `Impacted_Tooth`; `3`: `Fractured_Tooth`; `4`: `BDC_BDR`; `5`: `Healthy_Tooth` *(selective `~2.8/OPG`)*. |
| `TrackD` (`DS0004` Hanoi) | `CLS0025–CLS0027` (`3` active) | Focal apical AABB | `0`: `PAI_3`; `1`: `PAI_4`; `2`: `PAI_5`. |
| `TrackE` (`DS0005` AU-OPG) | `CLS0028–CLS0033` (`6` active) | Whole-tooth AABB *(from OBB)* | `0`: `Filled_Tooth`; `1`: `Crowned_Tooth`; `2`: `Retained_Root`; `3`: `Cavitated_Tooth`; `4`: `Implant`; `5`: `Impacted_Tooth`. |
| `TrackF` (`DS0006` MD-OPG) | `CLS0034–CLS0036` (`2` active, `1` excluded ROI) | Focal caries AABB *(from polygon)* | `0`: `Proximal_Caries`; `1`: `Occlusal_Caries`. *(Excluded ROI: `CLS0036` `Smile_Zone_ROI`.)* |
| `EvalBridge` (`HC01–HC05`) | `CLS0037–CLS0041` (`5` zero-shot bridges) | Strictly matched granularity tier | `HC01`: Harmonized Caries (`TrackE:3 -> TrackB:{1,3}, TrackC:0`); `HC02`: Harmonized Periapical (`TrackA:7 <-> TrackD:{0,1,2}`); `HC03`: Harmonized Impacted Tooth (`TrackA:6, TrackB:0, TrackC:2, TrackE:5`); `HC04`: Harmonized Residual Root (`TrackA:8, TrackC:4, TrackE:2`); `HC05`: Harmonized Dental Implant (`TrackA:0 <-> TrackE:4`). |

---

## Appendix B: Immutable `FREEZE0001` Cryptographic Hash Ledger (`R1`: `50/50` Verified)

Authoritative freeze manifest: `09_Evaluation/freeze_manifest.json` (frozen `2026-11-21T01:40:00+06:00`, commit `d47dae64e50b1f77213daf463777e078abbc45af`, `0` prior test exposure; independently verified `50/50` in `12_Documentation/step038_reproducibility_audit.json`).

### B.1 Core Governance, Code & Preprocessing Anchors

| Artifact Path | Full `SHA-256` Digest |
|---|---|
| `04_Annotations/classes.csv` | `c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af` |
| `09_Evaluation/protocol.md` | `26fede09e31475e7e7a5a1cdd3bc2a111815f727d8925300976dc6060a9024c1` |
| `07_Experiments/experiment_plan.md` | `24d26143125afce1fa8bf5c55e8d7cbeb393466d4355bf98933cf7e3e87a086a` |
| `src/opg/evaluator.py` | `8fa2c6d8254f095307d9d081701f7ab5e6494a8a415f7942f7daa9bf0f87a149` |
| `src/opg/preprocessing.py` | `011e67c02c56a1518af45c46627ec6db300330cb5ad233a4a37ca843e8bfac39` |
| `05_Preprocessing/configs/PP0001_raw_letterbox_baseline.yaml` | `04493e1e2bcdfcadbef5b044b392bf7091822439381e158d85c144d420e0b93b` |
| `05_Preprocessing/configs/PP0004_highres_letterbox_1280.yaml` | `08fd22b42f9fa31465eedc092251d92d7b5338b76de4fc7d321a7c77741dd2de` |

### B.2 Frozen Model Checkpoints (`10` Evaluated Models; `3` `CLAHE` Models Excluded at `G11`)

| `ModelID` | `Track` / Role | `ExpID` (`Arch@imgsz`) | `conf_op` | Bytes | Checkpoint `best.pt` `SHA-256` Digest |
|---|---|---|---:|---:|---|
| `MODEL0005` | `TrackA` (`track_winner`) | `EXP0010` (`YOLO11s@1280`) | `0.227` | `19,342,746` | `6a845f99bd87b9dcc904386784002864cbdf2031f851902e1678e64c9003612a` |
| `MODEL0001` | `TrackA` (`rq1_rq3_comp`) | `EXP0001` (`YOLO11s@640`) | `0.238` | `19,191,578` | `ce8e5b44bdce6bee76734dc0241918161874fccd30457c19ab555f5cd798eeef` |
| `MODEL0002` | `TrackA` (`rq1_rq3_comp`) | `EXP0002` (`YOLOv8s@640`) | `0.197` | `22,527,018` | `2f4b5b27f40e0fb8eaa627f910a5ee51c2712dc234828851cf21eb68fc4b82f3` |
| `MODEL0003` | `TrackA` (`rq1_rq3_comp`) | `EXP0013` (`YOLO11m@640`) | `0.253` | `40,535,276` | `a5a89aa41e0559316594d7f306354a5b8ee5d74104e13ea591c89761dccda743` |
| `MODEL0004` | `TrackB` (`track_winner`, `NC-SA`) | `EXP0003` (`YOLO11s@640`) | `0.210` | `19,180,122` | `33c6453dc59ddbe49ffebe13896a8b6c12ba7906c951655abf4b0768d967827c` |
| `MODEL0006` | `TrackC` (`track_winner`) | `EXP0004` (`YOLO11s@640`) | `0.075` | `19,181,978` | `966d9abcc60a7f27259cedd8882bcbbf5a2378e0847fbf7682115d41bfc4c674` |
| `MODEL0013` | `TrackD` (`track_winner`) | `EXP0011` (`YOLO11s@1280`) | `0.201` | `19,334,554` | `ac6dadc9123a58db475ddf0c1d96de5c8f2d9bf2e8a61e98f1b17b478ba9a14e` |
| `MODEL0010` | `TrackD` (`rq2_rq3_comp`) | `EXP0005` (`YOLO11s@640`) | `0.205` | `19,178,394` | `305d279c747ef016d1225dbe264fef5bdb14e360dbc240cad3ea670b6fa6e272` |
| `MODEL0008` | `TrackE` (`track_winner`) | `EXP0006` (`YOLO11s@640`) | `0.379` | `19,187,866` | `0336a078eb8b0037f2a40ca5a203f444a2e5ead7186ea321997ab3140c5e495b` |
| `MODEL0007` | `TrackF` (`track_winner`) | `EXP0007` (`YOLO11s@640`) | `0.091` | `19,179,034` | `c725343e35bc5af8122461e109ed6d968f62854a227be9b5100fcc9e7599af92` |

---

## Appendix C: Complete Per-Class Held-Out Tables for All `6` Track Winners

Reconciled directly from `09_Evaluation/EVAL0001..EVAL0014/metrics.csv` (`TP + FN == GT` verified on all `128/128` rows in `g12_reconciliation_audit.json`).

### C.1 `TrackA` Internal (`EVAL0001`, `208` OPGs) & External (`EVAL0002`, `178` OPGs) — `MODEL0005` (`YOLO11s@1280`, `conf_op = 0.227`)

| `ID` | Class Name | `Int GT` | `Int P / R / F1` | **`Int AP@50`** (`AP@50:95`) | `Ext GT` | `Ext P / R / F1` | **`Ext AP@50`** (`AP@50:95`) |
|---:|---|---:|---|---|---:|---|---|
| `0` | `DS0001_Implant` | `70` | `0.783 / 0.671 / 0.723` | **`0.5641`** (`0.3153`) | `16` | `0.833 / 0.938 / 0.882` | **`0.9297`** (`0.4737`) |
| `1` | `DS0001_Prosthetic_Restoration` | `235` | `0.538 / 0.600 / 0.567` | **`0.5384`** (`0.2724`) | `192` | `0.603 / 0.672 / 0.636` | **`0.5725`** (`0.3218`) |
| `2` | `DS0001_Obturation` | `573` | `0.547 / 0.649 / 0.594` | **`0.5315`** (`0.2027`) | `874` | `0.648 / 0.673 / 0.660` | **`0.6203`** (`0.2449`) |
| `3` | `DS0001_Endodontic_Treatment` | `437` | `0.638 / 0.785 / 0.704` | **`0.6825`** (`0.2695`) | `513` | `0.741 / 0.809 / 0.774` | **`0.7323`** (`0.3117`) |
| `4` | `DS0001_Carious_Lesion` | `446` | `0.539 / 0.341 / 0.418` | **`0.3303`** (`0.1058`) | `296` | `0.460 / 0.307 / 0.368` | **`0.2779`** (`0.0987`) |
| `5` | `DS0001_Bone_Resorption` | `390` | `0.270 / 0.095 / 0.140` | **`0.0906`** (`0.0265`) | `677` | `0.593 / 0.080 / 0.141` | **`0.1891`** (`0.0540`) |
| `6` | `DS0001_Impacted_Tooth` | `133` | `0.647 / 0.564 / 0.602` | **`0.4945`** (`0.2237`) | `111` | `0.816 / 0.838 / 0.827` | **`0.7629`** (`0.4108`) |
| `7` | `DS0001_Apical_Periodontitis` | `142` | `0.607 / 0.239 / 0.343` | **`0.3078`** (`0.0805`) | `106` | `0.403 / 0.255 / 0.312` | **`0.2249`** (`0.0867`) |
| `8` | `DS0001_Root_Fragment` | `178` | `0.562 / 0.534 / 0.548` | **`0.4939`** (`0.1763`) | `93` | `0.455 / 0.484 / 0.469` | **`0.3486`** (`0.1417`) |
| `9` | `DS0001_Furcation_Lesion` | `39` | `0.500 / 0.128 / 0.204` | **`0.1785`** (`0.0589`) | `19` | `0.444 / 0.211 / 0.286` | **`0.2153`** (`0.0460`) |
| `10` | `DS0001_Apical_Surgery` | `10` | `0.000 / 0.000 / 0.000` | **`0.0428`** (`0.0119`) | `17` | `0.000 / 0.000 / 0.000` | **`0.0055`** (`0.0023`) |
| `11` | `DS0001_Orthodontic_Device` | `72` | `0.519 / 0.375 / 0.436` | **`0.3033`** (`0.1198`) | `6` | `0.500 / 1.000 / 0.667` | **`0.7500`** (`0.4552`) |
| `12` | `DS0001_Surgical_Device` | `163` | `0.787 / 0.859 / 0.821` | **`0.8567`** (`0.3995`) | `5` | `0.000 / 0.000 / 0.000` | **`0.0105`** (`0.0021`) |

### C.2 `TrackB–TrackF` Frozen Track Winners (`EVAL0009`, `EVAL0010`, `EVAL0011`, `EVAL0013`, `EVAL0014`)

| Track (`EvalID`, `Model`, `conf_op`) | `ID` | Class Name | `GT` | `TP` | `FP` | `FN` | `P` | `R` | `F1` | **`AP@0.50`** | `AP@0.50:95` |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `TrackB` (`EVAL0009`, `MODEL0004`, `0.210`) | `0` | `DS0002_Impacted` | `91` | `80` | `14` | `11` | `0.8511` | `0.8791` | `0.8649` | **`0.9012`** | `0.5314` |
| `TrackB` (`EVAL0009`, `MODEL0004`, `0.210`) | `1` | `DS0002_Caries` | `328` | `173` | `358` | `155` | `0.3258` | `0.5274` | `0.4028` | **`0.3385`** | `0.2336` |
| `TrackB` (`EVAL0009`, `MODEL0004`, `0.210`) | `2` | `DS0002_Periapical_Lesion` | `24` | `1` | `5` | `23` | `0.1667` | `0.0417` | `0.0667` | **`0.1759`** | `0.0942` |
| `TrackB` (`EVAL0009`, `MODEL0004`, `0.210`) | `3` | `DS0002_Deep_Caries` | `87` | `33` | `26` | `54` | `0.5593` | `0.3793` | `0.4521` | **`0.3435`** | `0.2102` |
| `TrackC` (`EVAL0010`, `MODEL0006`, `0.075`) | `0` | `DS0003_Caries_Tooth` | `30` | `10` | `34` | `20` | `0.2273` | `0.3333` | `0.2703` | **`0.2031`** | `0.1199` |
| `TrackC` (`EVAL0010`, `MODEL0006`, `0.075`) | `1` | `DS0003_Infection_Tooth` | `6` | `0` | `7` | `6` | `0.0000` | `0.0000` | `0.0000` | **`0.0016`** | `0.0006` |
| `TrackC` (`EVAL0010`, `MODEL0006`, `0.075`) | `2` | `DS0003_Impacted_Tooth` | `30` | `18` | `12` | `12` | `0.6000` | `0.6000` | `0.6000` | **`0.6601`** | `0.4230` |
| `TrackC` (`EVAL0010`, `MODEL0006`, `0.075`) | `3` | `DS0003_Fractured_Tooth` | `2` | `0` | `1` | `2` | `0.0000` | `0.0000` | `0.0000` | **`0.0000`** | `0.0000` |
| `TrackC` (`EVAL0010`, `MODEL0006`, `0.075`) | `4` | `DS0003_BDC_BDR` | `15` | `5` | `6` | `10` | `0.4545` | `0.3333` | `0.3846` | **`0.4505`** | `0.1892` |
| `TrackC` (`EVAL0010`, `MODEL0006`, `0.075`) | `5` | `DS0003_Healthy_Tooth` | `99` | `40` | `123` | `59` | `0.2454` | `0.4040` | `0.3053` | **`0.1898`** | `0.1109` |
| `TrackD` (`EVAL0011`, `MODEL0013`, `0.201`) | `0` | `DS0004_PAI_3` | `633` | `397` | `307` | `236` | `0.5639` | `0.6272` | `0.5939` | **`0.5878`** | `0.2483` |
| `TrackD` (`EVAL0011`, `MODEL0013`, `0.201`) | `1` | `DS0004_PAI_4` | `260` | `133` | `119` | `127` | `0.5278` | `0.5115` | `0.5195` | **`0.4976`** | `0.2289` |
| `TrackD` (`EVAL0011`, `MODEL0013`, `0.201`) | `2` | `DS0004_PAI_5` | `106` | `46` | `71` | `60` | `0.3932` | `0.4340` | `0.4126` | **`0.3751`** | `0.1850` |
| `TrackE` (`EVAL0013`, `MODEL0008`, `0.379`) | `0` | `DS0005_Filled_Tooth` | `428` | `366` | `64` | `62` | `0.8512` | `0.8551` | `0.8531` | **`0.8792`** | `0.6065` |
| `TrackE` (`EVAL0013`, `MODEL0008`, `0.379`) | `1` | `DS0005_Crowned_Tooth` | `205` | `190` | `13` | `15` | `0.9360` | `0.9268` | `0.9314` | **`0.9203`** | `0.5749` |
| `TrackE` (`EVAL0013`, `MODEL0008`, `0.379`) | `2` | `DS0005_Retained_Root` | `140` | `113` | `30` | `27` | `0.7902` | `0.8071` | `0.7986` | **`0.7792`** | `0.3913` |
| `TrackE` (`EVAL0013`, `MODEL0008`, `0.379`) | `3` | `DS0005_Cavitated_Tooth` | `124` | `58` | `25` | `66` | `0.6988` | `0.4677` | `0.5604` | **`0.5420`** | `0.3953` |
| `TrackE` (`EVAL0013`, `MODEL0008`, `0.379`) | `4` | `DS0005_Implant` | `80` | `80` | `4` | `0` | `0.9524` | `1.0000` | `0.9756` | **`0.9980`** | `0.5991` |
| `TrackE` (`EVAL0013`, `MODEL0008`, `0.379`) | `5` | `DS0005_Impacted_Tooth` | `71` | `56` | `9` | `15` | `0.8615` | `0.7887` | `0.8235` | **`0.8287`** | `0.5304` |
| `TrackF` (`EVAL0014`, `MODEL0007`, `0.091`) | `0` | `DS0006_Proximal_Caries` | `110` | `15` | `58` | `95` | `0.2055` | `0.1364` | `0.1639` | **`0.0823`** | `0.0172` |
| `TrackF` (`EVAL0014`, `MODEL0007`, `0.091`) | `1` | `DS0006_Occlusal_Caries` | `27` | `2` | `24` | `25` | `0.0769` | `0.0741` | `0.0755` | **`0.0252`** | `0.0049` |

---

## Appendix D: Independent Reproduction Commands (`R1–R4`) & Stage-Gate Audit Trail (`G01–G14`)

### D.1 One-Command Verification Suite (`12_Documentation/reproduce.md`)

```bash
# 1. Repository schema, registry, and custody verification (0 forbidden binaries tracked)
python 13_Automation/validate_repo.py

# 2. Automated unit, preprocessing, locked-loader, and prototype contract test suite (26 tests)
python -m pytest -q

# 3. Full R1 (50/50 SHA-256) + R2 (exact 0.0 metric replay) + R3A (ONNX CPU parity) + R3B (clean git archive) audit
python 13_Automation/audit_step038_reproducibility.py

# 4. Single-OPG research prototype inference (CPU ONNXRuntime, non-clinical)
python 13_Automation/run_opg_inference.py --model MODEL0008 --image <path_to_opg.jpg> --out-json out.json
```

### D.2 Stage-Gate Verification Ledger (`01_Project_Management/gates.csv`, `G01–G14 PASS`)

| Gate | Date | Status | Verified Artifact Milestone |
|---|---|---|---|
| `G01` | `2026-11-16` | **PASS** | Scope `v1.0.0`, `O1–O3`, and Research/Evaluation role split confirmed |
| `G02` | `2026-11-16` | **PASS** | Repository architecture, registries, `validate_repo.py`, and initial `pytest` suite |
| `G03` | `2026-11-17` | **PASS** | Systematic review (`122` screened / `42` Core full-text), `GAP0001–0006`, `RQ0–RQ3`, `DEC0019` |
| `G04` | `2026-11-18` | **PASS** | Six-cohort portfolio (`DS0001–DS0006`, `7,789` active OPGs, `17,566` quarantined) & non-merge rule |
| `G05` | `2026-11-19` | **PASS** | Frozen `41`-entry ontology (`classes.csv`, `sha256: c3f91dfc...`) & `< 0.002 px` converter contract |
| `G06` | `2026-11-19` | **PASS** | `ANN0001–ANN0006` frozen (`7,738` `.txt` files, `44,241` valid boxes, `300` visual QA OPGs, `0` errors) |
| `G07` | `2026-11-19` | **PASS** | Connected-component grouped `70/15/15` splits `SPLIT0001–0006` (`7,457` OPGs, `0` leaks) |
| `G08` | `2026-11-19` | **PASS** | Prepared releases `REL0001–0006` & invertible `PP0001–0004` (`max_rt_err = 0.004 px`, train-only fit) |
| `G09` | `2026-11-19` | **PASS** | Kaggle `Tesla T4` interrupt/checksum/`resume=True` smoke test (`EXP0000_SMOKE`) |
| `G10` | `2026-11-21` | **PASS** | All `13/13` controlled experiments (`EXP0001–EXP0013`) verified bit-for-bit (`0` sealed test access) |
| `G11` | `2026-11-21` | **PASS** | `FREEZE0001` locked (`6` track winners + `4` comparators, `3/3` `CLAHE` excluded, `val`-only `conf_op`) |
| `G12` | `2026-11-21` | **PASS** | `EVAL0001–0014`, `12/12` `XSHIFT` bridges, `10` GPU + `7` CPU timing logs & `CLAIM0013–0017` reconciled |
| `G13` | `2026-11-21` | **PASS** | `ERRREV0001` (`6,718`-box FP/FN taxonomy, size recall, `28` visual cases) & bounded `limitations.md` |
| `G14` | `2026-11-21` | **PASS** | `OPGPrototypeEngine` + `REPRO0001` (`R1` `50/50`, `R2` `0.0`, `R3A` `0.994` IoU, `R3B` clean checkout) |
