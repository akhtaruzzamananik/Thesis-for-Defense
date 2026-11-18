# G07 assessment — Leakage-safe grouped split and sealed test custody (`STEP-020`)

| Metadata | Value |
|---|---|
| TemplateID | T21 |
| template_version | v1.0.0 |
| entity_id | GA0007 (`G07` in `01_Project_Management/gates.csv`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) & Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) |
| reviewer | Ms Faiza Feroz (Supervisor) & Mahajub Al Shabah |
| date | 2026-11-19 |
| status | **`PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/splits/SPLIT0001–SPLIT0006/manifest.csv`; `03_Datasets/splits/SPLIT0001–SPLIT0006/report.md`; `03_Datasets/splits/SPLIT0001–SPLIT0006/config.json`; `03_Datasets/splits/SPLIT0001–SPLIT0006/checksums.json`; `03_Datasets/splits/splits_STEP-020_summary.json`; `src/opg/dataset_split.py`; `tests/test_dataset_split.py`; `13_Automation/run_splits_step020.py`; `DEC0007.md`; `DEC0008.md` |
| governing_section | OS §4.4, §13.1–13.2; Blueprint STEP-020 |
| sensitivity | Public gate audit record |

---

## Gate/entity versions

- **Gate:** `G07` (`GA0007` — *Leakage-safe split*, `STEP-020`)
- **Entity versions assessed:**
  - `SPLIT0001` (`DS0001`/`ANN0001`, `manifest.csv sha256:8260d222aba799aa7e46720bd604e625ecd43228ad49dc53c8e0ddd6c61c4dc9`)
  - `SPLIT0002` (`DS0002`/`ANN0002`, `manifest.csv sha256:a31c3245ff5eee84135528b4caa477e7886ee959aeaaa49e9a4077db572b2de1`)
  - `SPLIT0003` (`DS0003`/`ANN0003`, `manifest.csv sha256:add134cc9e74b86b1efcae2a8f60c960397251ddb2f8ba5886260a1b85c87952`)
  - `SPLIT0004` (`DS0004`/`ANN0004`, `manifest.csv sha256:3b8a2bf9da87076e0b7dcb81f7b620738415702e33e22d2a690c42834c61af1f`)
  - `SPLIT0005` (`DS0005`/`ANN0005`, `manifest.csv sha256:f81ffcd59eaf8733d3917751ae2c3c242979ab418d352bfdfa1c5eae81ea6c14`)
  - `SPLIT0006` (`DS0006`/`ANN0006`, `manifest.csv sha256:e75744071eeb3a31af233490d01ec9c15d54a65c9353140881573a0031aa9e6f`)
  - `DEC0007.md` (`UD07`) & `DEC0008.md` (`UD08`)

---

## each criterion & evidence/hash

| Mandatory Criterion (`OS §13.2` & `STEP-020` Checklist) | Evidence Path & Verified Hash / Record | PASS/FAIL | Corrective Action / Downstream Rule |
|---|---|---|---|
| **1. Audited grouping & duplicate component resolution (`UD07` / `DEC0007`)** | `01_Project_Management/decision_log/DEC0007.md`; `03_Datasets/splits/SPLIT0001–SPLIT0006/report.md`; `src/opg/dataset_split.py`. Contaminated official splits in `DS0001` (`27.5%` val leak) and `DS0005` (`4.4%` val leak) discarded; `281` redundant byte/re-encoded duplicate copies (`214 DS0001`, `61 DS0004`, `6 DS0005`) deduplicated (`deduplicated_duplicate_copy`); `DS0003` re-shoot pair and `DS0004/0005` near-duplicate pairs locked into connected groups (`7,451` unique groups across `7,457` canonical OPGs); `DS0006` interior pixel correlation verified (`0` pairs $\ge 0.95$, max `0.9149`). | **PASS** | Train and evaluate strictly on `MemberRole == active_canonical` (`7,457` OPGs, `41,103` canonical boxes). |
| **2. Zero cross-partition overlap & deterministic reproducibility (`STEP-020` Checklist #1–2)** | `03_Datasets/splits/splits_STEP-020_summary.json`; `tests/test_dataset_split.py`. `assert_zero_cross_partition_leakage` verified **`0` cross-partition `GroupID`s, `0` cross-partition `SHA-256` hashes, `0` cross-partition exact/re-encoded edges, and `0` cross-partition near-duplicate edges** across all `6` splits (`SPLIT0001–SPLIT0006`). Same inputs and seeds (`20261121–20261126`) deterministically reproduce exact membership. | **PASS** | Enforce `split_manifest_sha256` verification in `STEP-021` release materialization and `STEP-025` loaders. |
| **3. Target (`70/15/15`) vs actual proportions & per-class evaluation support (`UD08` / `DEC0008`)** | `01_Project_Management/decision_log/DEC0008.md`; `03_Datasets/splits/SPLIT0001–SPLIT0006/report.md`. Actual canonical proportions achieve `69.93%–71.18% train`, `14.71%–15.11% val`, `14.12%–15.04% test` (`5,106 train / 1,091 val / 1,082 test` + `178 external_test` in `SPLIT0001`), with **`100%` of active classes represented across `train`, `val`, and `test`**. | **PASS** | Report low-support minority classes (`DS0003 Fractured Teeth` `2 val / 2 test`, `DS0001 Apical surgery` `10 val / 10 test`) with explicit support denominators (`UD13`). |
| **4. Sealed test custody & honest residual independence statement (`OS §4.4`)** | `03_Datasets/splits/SPLIT0001–SPLIT0006/report.md` (`§§ unknown identity limits, custody/access`). Explicitly states residual limitation where upstream repositories (`DS0001–DS0004`) omitted patient IDs, and seals `test` and `external_test` partitions until `G11` freeze (`STEP-031`). | **PASS** | Unlocks **`STEP-021`** (*Materialize and verify versioned prepared dataset* / `G08`). |

---

## PASS/FAIL

**`PASS` (`2026-11-19`)**

## missing items

None. All `OS §13.2` `G07` mandatory criteria and `STEP-020` verification checklist items are complete and verified on disk.

## owner/fix

- **Owners:** Akhtaruzzaman Anik (`Data Steward & Preprocessing Lead`) & Mahajub Al Shabah (`Leakage & Reproducibility Reviewer`).
- **Next Action:** Execute **`STEP-021`** (*Materialize and verify a versioned prepared dataset* `REL0001–REL0006` and pass **`G08`**).

## assessor/date

- **Assessor:** Akhtaruzzaman Anik & Mahajub Al Shabah (verified via `13_Automation/run_splits_step020.py` & `pytest`)
- **Date:** `2026-11-19`

## human approval

- **Approved (`2026-11-19`):** Ms Faiza Feroz (Supervisor) + Akhtaruzzaman Anik + Mahajub Al Shabah (`DEC0007`, `DEC0008`, confirmed `2026-11-19`).

## invalidated descendants

None (`G01–G06` remain `PASS`; `G08–G17` are `NOT ASSESSED`).
