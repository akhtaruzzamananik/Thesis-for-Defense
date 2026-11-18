# G06 assessment — Annotation quality and release integrity (`STEP-016`–`STEP-018`)

| Metadata | Value |
|---|---|
| TemplateID | T21 |
| template_version | v1.0.0 |
| entity_id | GA0006 (`G06` in `01_Project_Management/gates.csv`) |
| owner | Mahajub Al Shabah (`232-15-900`, Annotation QA Lead) & Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| reviewer | Ms Faiza Feroz (Supervisor) & Clinical/Dental Review Team |
| date | 2026-11-19 |
| status | **`PASS` (`2026-11-19`)** |
| source_inputs | `04_Annotations/annotation_registry.csv` (`ANN0001–ANN0006`); `04_Annotations/reviews/pilot_review.md`; `04_Annotations/reviews/ANNB0001.md`–`ANNB0006.md`; `04_Annotations/reviews/annotation_release_audit.md`; `04_Annotations/reviews/release_STEP-018_verification.json`; `04_Annotations/adjudications/batch_STEP-017_adjudications.csv`; `13_Automation/audit_release_step018.py` |
| governing_section | OS §6.3–6.4, §13.1–13.2; Blueprint STEP-016, STEP-017, STEP-018 |
| sensitivity | Public gate audit record |

---

## Gate/entity versions

- **Gate:** `G06` (`GA0006` — *Annotation quality/integrity*, `STEP-018`)
- **Entity versions assessed:**
  - `04_Annotations/annotation_registry.csv` (`ANN0001 v1.0.0` through `ANN0006 v1.0.0`, status `Frozen-G06-PASS`)
  - `04_Annotations/classes.csv` (`v1.0.0`, `sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`)
  - `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`v1.0.0`)
  - `04_Annotations/reviews/pilot_review.md` (`STEP-016`), `ANNB0001.md`–`ANNB0006.md` (`STEP-017`), `annotation_release_audit.md` (`STEP-018`)

---

## each criterion & evidence/hash

| Mandatory Criterion (`OS §13.2` & `STEP-018` Checklist) | Evidence Path & Verified Hash / Record | PASS/FAIL | Corrective Action / Downstream Rule |
|---|---|---|---|
| **1. Accepted annotation pilot (`STEP-016`)** | `04_Annotations/reviews/pilot_review.md`; `04_Annotations/reviews/pilot_STEP-016_summary.json`; `04_Annotations/adjudications/pilot_STEP-016_adjudications.csv`. `60` stratified OPGs (`586` valid boxes) passed all prospective `G05` thresholds (`100.0%` schema validity, `100.0%` disposition agreement, $\kappa = 1.0000$, mean $\text{IoU} = 0.999958 \ge 0.85$, max round-trip error `0.002343 px < 0.01 px`, defect rate `0.68% < 5.0%`). | **PASS** | Same-class duplicate deduplication ($\text{IoU} > 0.90$) applied across all production batches. |
| **2. Reviewed production batches (`STEP-017`, `ANNB0001–ANNB0006`)** | `04_Annotations/reviews/ANNB0001.md`–`ANNB0006.md`; `04_Annotations/reviews/batch_STEP-017_summary.json`. All `7,789` active OPGs processed (`7,738` canonical `.txt` files exported = `7,711` `reviewed_positive` + `27` `reviewed_empty`; `51` `missing_labels` quarantined). `44,421` raw shapes reconciled to **`44,241` valid boxes** + `180` excluded/deduplicated shapes. | **PASS** | Retain `51` `missing_labels` files quarantined from supervised training/eval denominators. |
| **3. 100% structural integrity & stratified visual QA (`STEP-018`)** | `04_Annotations/reviews/annotation_release_audit.md`; `04_Annotations/reviews/release_STEP-018_verification.json`; `13_Automation/audit_release_step018.py`. Verified `0` orphan labels, `0` invalid/out-of-bounds boxes, `0` zero-area boxes, `0` remaining same-class duplicates across all `7,738` exported `.txt` files, plus `240`-OPG batch visual overlay QA (`300` OPGs total with pilot). Residual uncertainty honestly documented. | **PASS** | Enforce `ExportHash` and `ClassMapHash` verification in `STEP-019`–`021` preprocessing and `STEP-025` loaders. |
| **4. Adjudication closure & frozen `ANN` / `class-map` hashes** | `04_Annotations/annotation_registry.csv` (`ANN0001–ANN0006`); `04_Annotations/adjudications/batch_STEP-017_adjudications.csv`. Every `NativeHash` and `ExportHash` verified on disk against `ClassMapHash = c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`. | **PASS** | Proceed to **`S09` (`STEP-019`–`STEP-021`: Preprocessing, Leakage-Safe Split & Prepared Release `REL`)**. |

---

## PASS/FAIL

**`PASS` (`2026-11-19`)**

## missing items

None. All `OS §13.2` `G06` mandatory criteria and `STEP-018` verification checklist items are complete and verified on disk.

## owner/fix

- **Owners:** Mahajub Al Shabah (`Annotation QA Lead`) & Akhtaruzzaman Anik (`Data Steward & Preprocessing Lead`).
- **Next Action:** Proceed to **`STEP-019`** (*Design preprocessing and coordinate-preserving transforms*).

## assessor/date

- **Assessor:** Mahajub Al Shabah & Akhtaruzzaman Anik (verified via `13_Automation/audit_release_step018.py` & `pytest`)
- **Date:** `2026-11-19`

## human approval

- **Approved (`2026-11-19`):** Ms Faiza Feroz (Supervisor) + Clinical/Dental Review Team + Mahajub Al Shabah + Akhtaruzzaman Anik (`2026-11-19`).

## invalidated descendants

None (`G01–G05` remain `PASS`; `G07–G17` are `NOT ASSESSED`).
