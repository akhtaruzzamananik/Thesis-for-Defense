# G05 assessment — Classes, annotation protocol, coordinate schema, and QA thresholds (`STEP-014`–`STEP-015`)

| Metadata | Value |
|---|---|
| TemplateID | T21 |
| template_version | v1.0.0 |
| entity_id | GA0005 (`G05` in `01_Project_Management/gates.csv`) |
| owner | Mahajub Al Shabah (`232-15-900`, Annotation QA Lead) & Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| reviewer | Ms Faiza Feroz (Supervisor) & Clinical/Dental Review Team |
| date | 2026-11-19 |
| status | **`PASS` (`2026-11-19`)** |
| source_inputs | `04_Annotations/classes.csv` (`v1.0.0`, `sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`); `04_Annotations/protocols/class_definitions.md`; `04_Annotations/protocols/annotation_protocol_v1.0.0.md`; `src/opg/annotation_schema.py`; `tests/test_annotation_schema.py`; `DEC0004.md`; `DEC0005.md`; `DEC0006.md` |
| governing_section | OS §6.1–6.4, §13.1–13.2; Blueprint STEP-014, STEP-015 |
| sensitivity | Public gate audit record |

---

## Gate/entity versions

- **Gate:** `G05` (`GA0005` — *Classes and protocol*, `STEP-015`)
- **Entity versions assessed:**
  - `04_Annotations/classes.csv` (`v1.0.0`, `41` records `CLS0001–CLS0041`, normalized `SHA-256: c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`)
  - `04_Annotations/protocols/class_definitions.md` (`v1.0.0`)
  - `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`v1.0.0`)
  - `01_Project_Management/decision_log/DEC0004.md` (`UD04`), `DEC0005.md` (`UD05`), `DEC0006.md` (`UD06`)
  - `src/opg/annotation_schema.py` & `tests/test_annotation_schema.py`

---

## each criterion & evidence/hash

| Mandatory Criterion (`OS §13.2` & `STEP-015` Checklist) | Evidence Path & Verified Hash / Record | PASS/FAIL | Corrective Action / Downstream Rule |
|---|---|---|---|
| **1. Approved class ontology & radiographic boundaries (`UD04` / `DEC0004`)** | `04_Annotations/classes.csv` (`v1.0.0`, `sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`); `04_Annotations/protocols/class_definitions.md`; `DEC0004.md`. Track-isolated class maps (`Tracks A–F`) and `5` granularity-matched evaluation bridges (`HC01–HC05`) approved; `CLS0012 Root resorption (N=5)` and `CLS0036 Smile Zone ROI` excluded with full audit trail; radiographic observations separated from clinical diagnoses. | **PASS** | Enforce `classes.csv` SHA-256 check in all downstream export and training scripts. |
| **2. Visibility, overlap, ambiguity & reviewed-negative vs missing-label rules (`OS §6.2`)** | `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`§§ visibility and negative rules, overlap, ambiguity`). Explicitly separates `reviewed_empty` (true negative `0`-byte `.txt`) from `missing_labels` (`51` quarantined unannotated files: `50` in `DS0002`, `1` in `DS0003`, plus `134` in `DS0005`), and mandates class-aware NMS/matching for multi-label tooth overlaps. | **PASS** | Quarantine all `missing_labels` files from training and metric denominators. |
| **3. Exact coordinate & export contract + tested round-trip conversion (`UD05` / `DEC0005`)** | `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`§ geometry/schema`); `src/opg/annotation_schema.py`; `tests/test_annotation_schema.py`; `DEC0005.md`. Tested across real annotations from all `6` datasets (`DS0001: 0.0 px`, `DS0002: 0.001904 px`, `DS0003: 0.0 px`, `DS0004: 0.000260 px`, `DS0005: 0.000367 px`, `DS0006: 0.001030 px` — all `< 0.002 px`). | **PASS** | Drop the `4` degenerate zero-area shapes deterministically and log in `annotation_registry.csv`. |
| **4. Reviewer roles, prospective pilot/QA sampling & acceptance thresholds (`UD06` / `DEC0006`)** | `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`§§ qualifications, pilot/QA sampling and thresholds, adjudication`); `DEC0006.md`. Locks `60`-OPG stratified pilot (`STEP-016`) + `240`-OPG stratified batch visual QA + `100%` automated geometry check (`STEP-017`–`018`) with prospective thresholds (`100%` schema validity, $\ge 90\%$ reviewer agreement, $\text{IoU} \ge 0.85$, $< 5\%$ gross defect rate) before seeing pilot results. | **PASS** | Execute `STEP-016` pilot strictly against these predeclared thresholds without post-hoc lowering. |

---

## PASS/FAIL

**`PASS` (`2026-11-19`)**

## missing items

None. All `STEP-015` verification checklist items and `OS §13.2` `G05` mandatory criteria are complete and evidenced.

## owner/fix

- **Owners:** Mahajub Al Shabah (`Annotation QA Lead`) & Akhtaruzzaman Anik (`Data Steward`).
- **Next Action:** Proceed immediately to **`STEP-016`** (Run and adjudicate the `60`-OPG stratified annotation pilot) and **`STEP-017`–`018`** (Production batch QA `ANNB0001–ANNB0006` and `ANN0001–ANN0006` release freeze for `G06`).

## assessor/date

- **Assessor:** Mahajub Al Shabah & Akhtaruzzaman Anik (verified via `annotation_schema.py` & `pytest`)
- **Date:** `2026-11-19`

## human approval

- **Approved (`2026-11-19`):** Ms Faiza Feroz (Supervisor) + Clinical/Dental Review Team + Mahajub Al Shabah + Akhtaruzzaman Anik (`DEC0004–DEC0006`, confirmed `2026-11-19`).

## invalidated descendants

None (`G01–G04` remain `PASS`; `G06–G17` are `NOT ASSESSED`).
