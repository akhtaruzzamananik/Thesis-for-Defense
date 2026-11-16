# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0001.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0001 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0001.md`, `P0005.md`, `P0006.md`, `P0009.md`, `P0014.md`–`P0017.md`, `P0021.md`–`P0025.md`, `P0027.md`, `P0042.md` |
| governing_section | OS §9.1 |

## Exact statement

Multi-class (`4` to `13` classes) YOLO and transformer 2D OPG object detectors already exist across multiple independent clinical and public cohorts (`13` of `23` Group A papers in the Core corpus), refuting any broad claim that existing OPG object detection work is exclusively single-class or absent.

## scope

- Valid strictly for the screened `122`-study project corpus (`SEARCH0001` + `SEARCH0002`, `2026-11-16`, `42` Core extracted full-text; `55` Reserve incl. `27` YOLO titles).
- Refutes broad absence/single-task claims (`GAP0001` / `G1`).

## evidence IDs/locators

- `P0023` (`Mureșanu 2024`, `Tables 2–3`, pp. 3–4; `13` pre-RT classes, `UMFIH`) & `P0015` (`Eftimie 2025`, `Tables 1–2`, pp. 7–8; `12` pathology + `32` FDI classes).
- `P0022` (`Bonfanti-Gris 2024`, `Tables 2–3`, pp. 5–6; `12` classes, `YOLOv7m mAP@0.5=0.740`).
- `P0009` (`Peng 2026`, `Tables 4–5`, pp. 14, 18; `11` classes, `8,124` Roboflow OPGs).
- `P0001` (`Baseri Saadi 2026`, `Tables 1 & 3`, pp. 3–4, 8–9; `10` classes via task subsets).
- `P0025` (`Rashidi Ranjbar 2023`, `Table 3–4`, pp. 20, 28; `8`-class `3`-stage treatment planning).
- `P0006` (`Khurshid 2026`, `Table 2`, p. 8; `7` retained-root + periodontal classes).
- `P0005` (`6` third-molar subtypes), `P0017` (`6` restorations), `P0021` (`6` tooth/anomaly classes), `P0024` (`6` clinical classes, Dhaka, `mAP50=93.54%`), `P0014` (`4` `DENTEX` pathologies), `P0016` (`4` pediatric classes), plus Group B (`P0026, P0031, P0032, P0040`) and reviews (`P0027, P0028, P0037`).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- Narrow single-condition detectors also exist in Core (`P0003, P0004, P0008, P0012, P0013, P0018, P0029, P0033, P0035, P0036, P0041`).
- Shared dataset clusters (`UMFIH` in `P0015/P0023`; `Tufts` in `P0006/P0015/P0017/P0042`; `Khurshid` on `P0005/P0006/P0017`) reduce independent dataset counts, yet `>8` disjoint multi-class clinical cohorts remain.

## uncertainty

Low regarding existence of multi-class OPG object detectors; several high headline scores are inflated by pre-split leakage (`P0006, P0021, P0025`) or ontology merging (`P0016`).

## permitted wording

*"Multi-class 2D OPG object detectors (`4–13` classes) exist across multiple cohorts (`P0001, P0005, P0006, P0009, P0014–P0017, P0021–P0025`); therefore, the contribution of this thesis does not rest on claiming multi-class OPG detection is unattempted."*

## verification

Verified directly across `P0001.md`–`P0042.md` and `GAP0001.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§2`, `§5`); `02_Literature/gap_notes/GAP0001.md`.
