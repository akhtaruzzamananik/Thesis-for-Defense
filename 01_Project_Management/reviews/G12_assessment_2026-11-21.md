# Gate G12 Assessment — Evaluation Validity & Results Acceptance (`STEP-035`)

| Field | Value |
|---|---|
| Gate ID | `G12` (`GA0012`) |
| Step / Stage | `STEP-035` (`S12` — Consolidate final evaluation and pass `G12`) |
| Entity Versions Assessed | `FREEZE0001 v1.0.0`, `EVAL0001–EVAL0014 v1.0.0`, `XSHIFT01–XSHIFT06` (`12` bridges), `timing_report.md v1.0.0`, `final_evaluation_report.md v1.0.0`, `CLAIM0013–CLAIM0017` |
| Outcome | **`PASS` (`2026-11-21`)** |
| Assessors | Mahajub Al Shabah (`232-15-900`, Evaluation Lead) & Akhtaruzzaman Anik (`232-15-252`, Research Lead) |
| Reconciliation Evidence | [g12_reconciliation_audit.json](../../09_Evaluation/g12_reconciliation_audit.json) & [final_evaluation_report.md](../../09_Evaluation/final_evaluation_report.md) |

---

## 1. Itemized `G12` Validity Criteria Audit (`STEP-035` / `OS §7`, `§9`, `§13.2`)

| Criterion | Result | Verified Evidence |
|---|---|---|
| **1. Freeze custody & temporal ordering (`G11` strictly precedes `STEP-032`)** | **PASS** | `FREEZE0001` locked at `2026-11-21T01:40:00+06:00` (`2026-11-20T19:40:00Z`, commit `6282385`), strictly preceding `STEP-032` Kaggle start (`2026-11-20T20:24:22Z`). All `4` governance hashes (`classes.csv`, `protocol.md`, `evaluator.py`, `preprocessing.py`), `10/10` `.pt` weights, `14/14` `predictions.jsonl`, and `7/7` `.onnx` exports verified bit-for-bit (`0` post-test model or threshold edits). |
| **2. All 4 required metrics + adopted analyses reported with explicit settings** | **PASS** | Every `EVAL0001–EVAL0014` reports `Precision`, `Recall`, `F1`, `mAP@0.50`, `mAP@0.50:0.95`, per-class `AP` & `GT` support, `1,000`-resample `GroupID` cluster bootstrap `95% CI`, and matched hardware `FPS_e2e`/`FPS_infer` (`Tesla T4` GPU `10/10` + `Intel i5-1135G7` CPU `ONNXRuntime` `7/7`, `0.983–0.997` parity IoU). Explicit `nms_iou=0.65`, `agnostic_nms=false`, `matching_iou=0.50`, `conf_floor=0.001`, and `val`-only `conf_op` documented. |
| **3. Exact arithmetic & coverage reconciliation** | **PASS** | Programmatic audit ([g12_reconciliation_audit.json](../../09_Evaluation/g12_reconciliation_audit.json)) verified `100.0%` coverage (`0` errors) across all `1,082` internal `test` + `178` `external_test` OPGs, `128/128` per-class `TP_op + FN_op == GTCount` identities, exact match to canonical release box sums, and `metrics.csv == metrics_summary.json` reconciliation. |
| **4. Zero selective reporting & honest disclosure of unfavorable results** | **PASS** | All `3/3` `CLAHE` negative `RQ2` runs, low-support `TrackF` (`0.0537`) & `TrackC` (`0.2508`, `Fractured=0.0000`), ultra-rare `TrackA` `Apical_Surgery` (`0.0428`/`0.0055`), and severe `HC01`/`HC02` cross-country radiolucency collapse (`0.163–0.236`) are reported prominently alongside strong findings (`TrackE 0.8246`, `HC03 0.8181`, `1280px` gains). |
| **5. Bounded claims & non-clinical scope compliance** | **PASS** | `CLAIM0013–CLAIM0017` appended to [claims.csv](../../02_Literature/claims.csv) with exact `EXP`/`EVAL` traceability, cross-track/cross-modality non-comparability caveats, and explicit non-clinical research boundary. |

---

## 2. Decision & Next Step

- **`G12` Outcome:** **`PASS` (`2026-11-21`)** — Final quantitative evaluation package is valid, reconciled, and locked for reporting.
- **Unlocks:** **`STEP-036`** (*Review errors, annotation uncertainty and limitations* — `T19` Error Review & **`G13`** Gate Assessment).
