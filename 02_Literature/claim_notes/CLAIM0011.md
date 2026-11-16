# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0011.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0011 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0001.md`–`P0042.md`; `02_Literature/gap_notes/GAP0006.md` |
| governing_section | OS §9.1 |

## Exact statement

Across all **`42` Core studies**, **`31 / 42` (`73.8%`) omit per-image inference latency (`ms/OPG` or `FPS`)** — comprising **`14 / 23` (`60.9%`) Group A detectors** and **`17 / 19` (`89.5%`) Group B studies** — including `6` studies making unverified `"real-time"` or speed claims (`P0005, P0017, P0018, P0019, P0033, P0035`), while `P0009` omits its own defined `FPS_all` (`T_pre + T_infer + T_post`).

## scope

- Exact accounting across all `42` extracted Core studies (`P0001–P0042`) under `GAP0006` / `G6`.

## evidence IDs/locators

- **Group A omitting per-image `ms/FPS` (`14/23`):** `P0003, P0004, P0005` (`19.7 GFLOPs` only), `P0007, P0014` (Flask web UI, `0` latency), `P0016` (`0.90 s/epoch` only), `P0017` (qualitative `Table 4`), `P0018` (`0` FPS despite `"real-time"` cascade), `P0019` (`0` FPS despite `YOLOv10` latency claims), `P0021, P0022, P0023, P0024, P0025` (plus `P0001` reports only `15 ± 1.4 s` Cloud Run upload-to-Word E2E latency and omits standalone GPU `FPS`).
- **Group B omitting OPG `ms/FPS` (`17/19`):** `P0002` (GPU conflict `A100` vs `T4`, relative only), `P0010, P0026–P0028` (`P0028` cites `<1 s ResNet` & `15 min` manual charting), `P0030–P0040` (incl. `"real-time"` claimants `P0033, P0035`), `P0042`.
- **`P0009` boundary gap (`Eq. 13–14, Table 4`, pp. 13–14):** Defines `FPS_all` (`T_pre + T_infer + T_post`) yet omits `T_pre`, `T_post`, and `FPS_all`, printing only `FPS_infer`.
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- `10` studies report per-OPG GPU/workstation runtime (`P0006, P0008, P0009, P0011, P0012, P0013 [coarse <500 ms], P0015, P0020, P0029, P0041`) plus `P0001` (cloud E2E), confirming that GPU timing is feasible to measure when authors adhere to explicit benchmarking protocols.

## uncertainty

Low: exact audit count directly observed across all `42` verified `T05` summaries.

## permitted wording

*"Within our `42`-paper Core corpus, `73.8%` (`31/42`) report zero per-OPG inference latency — including `6` papers making unverified `'real-time'` claims (`P0005, P0017–P0019, P0033, P0035`) — establishing a concrete reporting and reproducibility gap (`O3`)."*

## verification

Verified directly across all `42` `T05` summaries and `GAP0006.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§4.3`, `§5`); `02_Literature/gap_notes/GAP0006.md`.
