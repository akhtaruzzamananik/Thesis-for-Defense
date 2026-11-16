# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0004.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0004 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0019.md`, `P0027.md`, `P0003.md`–`P0004.md`, `P0012.md`, `P0014.md`–`P0016.md`, `P0018.md`, `P0020.md`–`P0025.md` |
| governing_section | OS §9.1 |

## Exact statement

In the `73`-study dental YOLO systematic review (`P0027`), **`84.9%` (`62/73`) omit strict `mAP@0.50:0.95`**, **`38.4%` (`28/73`) omit `mAP@0.50`**, and **`87.7%` (`64/73`) omit external validation**; omitting `mAP@0.50:0.95` conceals severe box-alignment errors such as `P0019 Tooth 71` (`mAP@0.50 = 0.995` vs `mAP@0.50:0.95 = 0.0995`).

## scope

- Quantitative meta-audit findings from `P0027` (`Jan 2020–Aug 2025`, `73` studies across dental imaging incl. `~31` OPG) paired with direct Core OPG extraction (`P0001–P0025`).

## evidence IDs/locators

- `P0027` (`Hartman et al., 2026`, `Tables 2–3`, pp. 9–23): Only `11/73` (`15.1%`, `5` OPG) report `mAP@0.50:0.95`; `45/73` (`61.6%`) report `mAP@0.50`; `44/73` (`60.3%`) report `F1`; `64/73` (`87.7%`) mark `"No"` for external validation (`3/73` `"Yes"` + `[74]` in `Table 2`).
- `P0019` (`Peker & Kurtoglu, 2025`, `Table 1`, p. 9): Primary incisor `Tooth 71` yields `mAP@0.50 = 0.995` yet collapses to **`mAP@0.50:0.95 = 0.0995`**.
- Among Core Group A detectors (`23` papers), `mAP@0.5:0.95` is also omitted (`not reported`) by `P0003, P0004, P0012, P0013, P0017 [YOLOv11], P0018, P0020, P0021, P0023, P0024, P0025` (curve only in `P0025`).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- Notable recent OPG benchmarks (`P0001, P0005, P0006, P0007, P0008, P0009, P0011, P0014, P0015, P0016, P0019, P0022`) DO report `mAP@0.5:0.95`, and `P0015, P0016, P0023, P0029, P0030` conduct multi-center external validation (`P0027`'s Scopus `"DENT"` filter & Aug 2025 cutoff undercounted CS venues & late-2025/2026 external tests, plus mis-marked `P0016` external val as `"No"`).

## uncertainty

Low for the verified `P0027` corpus percentages and `P0019` per-class gap; note that `P0027` reflects pre-Aug-2025 indexed dental-journal literature and `2025–2026` Group A papers are already improving `mAP@0.5:0.95` adoption (`12/23` Group A report it numerically).

## permitted wording

*"Systematic review evidence (`P0027`: `84.9%` omitting `mAP@0.50:0.95`, `87.7%` lacking external validation among `73` YOLO studies through Aug 2025) and concrete box-loosening failures (`P0019 Tooth 71`: `0.995` vs `0.0995`) establish why both `mAP@0.50` and `mAP@0.50:0.95` plus external OPG testing are mandatory in Phase 2."*

## verification

Verified directly from `P0027`, `P0019`, and Group A `T05` summaries (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§3.1`, `§4.1`); `02_Literature/gap_notes/GAP0002.md`.
