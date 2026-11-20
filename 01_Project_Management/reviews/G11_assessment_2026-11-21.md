# Gate G11 Assessment — Validation Selection & Final-Test Evaluation Freeze (`STEP-031`)

| Field | Value |
|---|---|
| Gate ID | `G11` (`GA0011`) |
| Step / Stage | `STEP-031` (`S12` — Select on validation and freeze final-test evaluation) |
| Entity Versions Assessed | `FREEZE0001 v1.0.0`, `09_Evaluation/freeze.md`, `09_Evaluation/freeze_manifest.json`, `09_Evaluation/protocol.md v1.0.0`, `MODEL0001–MODEL0013`, `CKPT0003–CKPT0028`, `REL0001–REL0006 v1.0.0` |
| Outcome | **`PASS` (`2026-11-21`)** |
| Assessors | Mahajub Al Shabah (`232-15-900`, Evaluation Lead) & Akhtaruzzaman Anik (`232-15-252`, Research Lead) |
| Freeze Record | [freeze.md](../../09_Evaluation/freeze.md) & [freeze_manifest.json](../../09_Evaluation/freeze_manifest.json) |

---

## 1. Mandatory Criteria Audit (`STEP-031` / `OS §5`, `§7`, `§13.2`)

| Criterion | Result | Observed Verification |
|---|---|---|
| **1. Prerequisites current (`G07–G10 PASS`)** | **PASS** | `G07` (`SPLIT0001–0006`), `G08` (`REL0001–0006` + `PP0001–0004`), `G09` (`Tesla T4` smoke/resume), and `G10` (`13/13` `EXP0001–EXP0013` / `MODEL0001–MODEL0013`) all `PASS`. |
| **2. Selection & operating thresholds derived strictly from `validation`** | **PASS** | Predeclared rule (`val mAP@0.50`, tie-breaker `val mAP@0.50:0.95`) selected `6` track winners (`MODEL0005`, `MODEL0004`, `MODEL0006`, `MODEL0013`, `MODEL0008`, `MODEL0007`) + `4` predeclared `RQ1`/`RQ3` comparators (`MODEL0001`, `MODEL0002`, `MODEL0003`, `MODEL0010`) and excluded `3/3` `CLAHE` losers (`MODEL0009`, `MODEL0011`, `MODEL0012`). All `10` `conf_op` thresholds extracted strictly from validation `BoxF1_curve.png`. |
| **3. Immutable hashes locked for all artifacts, code & protocol** | **PASS** | [freeze_manifest.json](../../09_Evaluation/freeze_manifest.json) locks `SHA-256` hashes for all `10` verified local `best.pt` weights (re-checked `10/10` bit-for-bit against `checkpoint_registry.csv`), `classes.csv` (`c3f91dfc...`), `protocol.md` (`26fede09...`), `PP0001`/`PP0004`, `SPLIT0001–0006`, `REL0001–0006` manifests + `TransformLedger`, and `src/opg/{evaluator,preprocessing}.py`. |
| **4. Evaluation, NMS, timing, bootstrap & cross-cohort rules frozen (`UD13–UD15`)** | **PASS** | Frozen: `metric_conf_floor = 0.001`, class-aware `nms_iou = 0.65`, `agnostic_nms = false`, `max_det = 300`, `matching_iou = 0.50` & `[0.50:0.05:0.95]`, `1,000`-resample `GroupID` bootstrap (`seed = 20261131`), serial `BS = 1` GPU/CPU timing (`10` warm-up + `100` timed OPGs), and `12` zero-shot cross-country bridges (`HC01–HC05`). |
| **5. Prior test-access custody audit (`0` contamination)** | **PASS** | `14/14` runs (`EXP0000_SMOKE`, `EXP0001–EXP0013`) enforced `allowed_partitions: ["train", "val"]`, `allow_test_partition = False`, and `val_or_test_used_for_fit = false`; `09_Evaluation/evaluation_registry.csv` has `0` test rows; this freeze commit strictly precedes any `STEP-032` prediction timestamp. |

---

## 2. Decision & Authorization

- **`G11` Outcome:** **`PASS` (`2026-11-21`)**.
- **Test Release Authorization:** Sealed `test` (`1,082` canonical OPGs across `REL0001–REL0006`) and `external_test` (`178` canonical OPGs in `REL0001`) partitions are hereby released **exclusively** for single-pass frozen inference under [freeze_manifest.json](../../09_Evaluation/freeze_manifest.json).
- **Unlocks:** **`STEP-032`** (*Generate and validate final-test predictions*, GPU `batch=1` timing, `ONNX` export, and zero-shot cross-country `HC01–HC05` predictions).
