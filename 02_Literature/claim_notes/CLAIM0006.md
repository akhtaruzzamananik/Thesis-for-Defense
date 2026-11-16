# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0006.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0006 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0002.md`, `P0005.md`, `P0012.md`, `P0013.md`, `P0020.md`–`P0021.md`, `P0026.md`–`P0027.md`, `P0032.md`–`P0034.md`, `P0036.md`, `P0039.md` |
| governing_section | OS §9.1 |

## Exact statement

`2D OPG` has real physical sensitivity boundaries compared to 3D `CBCT` (`P0039` paired `Diagnocat` periapical sensitivity `33.33%` on `OPG` vs `77.78%` on `CBCT`) and intraoral `BW/PA` (`P0032` initial enamel caries excluded on OPG; `P0036` `8` OPG anatomical mimics driving `519` FPs), making cross-modality numerical ranking invalid (`P0002, P0021, P0027`).

## scope

- Governs modality scope boundaries (`scope.md`: 2D OPG only; no CBCT modeling or cross-modality metric ranking) under `GAP0004` / `G4`.

## evidence IDs/locators

- `P0039` (`Kazimierczak 2024`, `49` patients, `1,223` teeth, paired `OPG+CBCT<=30d`): `Diagnocat OPG Sens = 33.33% (F1 = 32.73%)` vs `CBCT 77.78% (F1 = 84.00%)` against CBCT reference (human OPG `Sens = 66.67%, PPV = 31.58%`).
- `P0034` (`Bonfanti-Gris 2025`, `p. 15`): `4/6` impacted-tooth OPG studies needed `CBCT` GT.
- `P0032` (`van Nistelrooij 2026`, `Table 2` & `p. 8`): OPG `FDI Acc = 0.980` beats intraoral (`0.956`), yet `mAP@50-95` trails (`0.779 vs 0.869`; primary `0.625 vs 0.895`) and **initial enamel caries are excluded on OPG**.
- `P0036` (`Pornprasertsuk-Damrongsri 2025`, `Fig. 7`): Required `>=4` same-day bitewings per patient; documents `8` OPG anatomical mimics (`cervical burnout, pulp horns, palatoglossal air space`, etc.) causing `519` (`826` all-teeth) FPs.
- Projection limits acknowledged by `P0005` (`p. 8–9`), `P0012` (`p. 2, 10`: `30–40%` mineral loss threshold; premolar overlap `79.3%`), `P0013` (`p. 13`), `P0020` (`pp. 18–19`), `P0026` (`pp. 11–12`), `P0033` (`p. 11`).
- Invalid cross-modality pooling documented in `P0002` (RGB intraoral labeled OPG), `P0021 Table 4` (vs CT/CBCT/PA), `P0027` (intraoral `0.932` vs OPG `0.760` `mAP50-95`; `P0022` mislabeled intraoral), and `P0032 Tables 3–4` (pooled OPG+BW+PA).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- Paired human+AI OPG performance for gross restorations and permanent tooth numbering (`P0032 FDI Acc = 0.980`) confirms `2D OPG` remains clinically valuable for full-arch triage and gross screening without replacing CBCT/BW.

## uncertainty

`P0039` has a small sample (`49` patients, `26–27` CBCT lesions) and internal `Tables 1–4` GT discrepancies (`26 vs 27`), so exact percentages carry wide uncertainty; the qualitative physical ceiling is independently corroborated by `P0012, P0032, P0034, P0036`.

## permitted wording

*"Per `P0032, P0034, P0036, P0039`, `2D OPG` serves full-arch radiographic triage (`FDI Acc = 0.980`) while facing physical superimposition limits for incipient enamel caries and 3D surgical depth compared to `BW/CBCT`; this thesis operates strictly within `2D OPG` bounds without cross-modality metric ranking."*

## verification

Verified directly across Core `T05` summaries and `GAP0004.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§3.2`, `§5`); `02_Literature/gap_notes/GAP0004.md`.
