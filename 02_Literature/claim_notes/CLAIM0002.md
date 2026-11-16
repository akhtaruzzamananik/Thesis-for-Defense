# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0002.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0002 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0003.md`, `P0006.md`, `P0009.md`, `P0014.md`, `P0016.md`, `P0022.md`–`P0026.md`, `P0030.md`–`P0032.md`, `P0040.md` |
| governing_section | OS §9.1 |

## Exact statement

Inside existing multi-class 2D OPG detectors, high-contrast or large targets (`Impacted teeth`, `Implants`, `Crowns`) routinely reach `mAP@0.50 = 0.83–0.98`, whereas small radiolucent pathologies (`Caries`, `Periapical lesions`), diffuse `Alveolar bone loss`, non-radiographic root exposure, and rare classes (`Supernumerary`) suffer severe per-class AP or recall collapse (`0.000–0.565`).

## scope

- Applies to reported per-class evaluations across multi-class and surface-stratified Core OPG studies (`2023–2026`).
- Governs target-class selection (`UD04`) and mandatory per-class reporting in Phase 2 (`O1–O2`).

## evidence IDs/locators

- `P0009` (`Table 5`, p. 18): `RCTE-Net` `Impacted = 0.9513`, `Implant = 0.9203`, `Crown = 0.7964` vs **`Caries mAP50 = 0.2497 (R=0.1998)`** & **`Periapical lesion mAP50 = 0.0726 (R=0.0685)`**.
- `P0014` (`Table III`, p. 3, `DENTEX`): `Customized YOLOv11` `Impacted AP50 = 0.871` vs `Caries = 0.403`, `Deep Caries = 0.421`, **`Periapical Lesion = 0.322`**.
- `P0023` (`Fig. A2a/b`, pp. 11–12): `IMP 0.957->0.818` vs external **`API = 0.315`**, **`CAR = 0.373`**, **`BON = 0.165->0.154`**, **`FUR = 0.131`**, `APS = 0.000->0.021`.
- `P0003` (`Table 1`, p. 6): Pediatric `Buccal caries TP = 0 (F1=0)`, `Occlusal F1 = 0.240`, `Approximal F1 = 0.576`.
- `P0006` (`Table 4`, p. 8): `PCT mild R = 0.908` vs `RR clinical R = 0.506` (no mucosal contrast).
- `P0022` (`Tables 3, 5`, pp. 5–6): `Tooth 0.996`, `Implant 0.995` vs **`Supernumerary mAP0.5 = 0.000`**.
- `P0025` (`Table 3, Fig. 14`, pp. 20, 26): `Surgical extraction = 0.935` vs empty-gap needed `Implant AP@0.5 = 0.524` (`44% FN`).
- `P0026` (`Table 3`, p. 8): Diagnosis `Implant F1=0.99` vs `Cavitated 0.64`; Treatment **`Filling 0.32, RCT 0.46`**.
- `P0030` (`Supernumerary` `50–74%` missed), `P0031` (MLLM `Caries <= 0.075, PA <= 0.023, Bone loss = 0.000`), `P0032` (`PA Sens = 0.538` vs dentists `0.854`), `P0040` (`Supernumerary 91 R = 0.565`).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- `P0001` (`YOLO26m` subset-only evaluation) reported higher `mAP@0.50` on `Radicular cysts` (`0.91, n=16`) and `Periapical granulomas` (`0.87, n=14`), though trained on small positive-only task subsets rather than unified full-cohort inference.
- `P0016` reported `Dental Caries` recall `0.79–0.89`, but explicitly merged radiolucent caries with radiopaque fillings into the same class (`p. 4`).
- `P0024` reported `93.54% mAP50` without releasing per-class breakdown on minority `Fractured Teeth` (`13` OPGs) or `Infection` (`23` OPGs).

## uncertainty

Moderate due to cross-study variance in annotation schemas, cohort selection, and dataset sizes; qualitative pattern across independent cohorts is strong and consistent.

## permitted wording

*"Across independent multi-class 2D OPG detectors, high aggregate `mAP` frequently masks sharp performance drops on small radiolucent caries, periapical lesions, diffuse bone loss, and rare classes (`P0003, P0006, P0009, P0014, P0022, P0023, P0030, P0032`), motivating class-stratified evaluation and careful radiographic target boundary definition (`UD04`)."*

## verification

Verified directly across Core `T05` summaries and `GAP0001.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§2`, `§5`); `02_Literature/gap_notes/GAP0001.md`.
