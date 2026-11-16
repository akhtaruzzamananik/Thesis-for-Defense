# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0010.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0010 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0002.md`, `P0005.md`, `P0006.md`, `P0008.md`, `P0011.md`, `P0014.md`, `P0016.md`, `P0020.md`–`P0022.md`, `P0025.md`, `P0033.md`, `P0036.md`, `P0040.md` |
| governing_section | OS §9.1 |

## Exact statement

Pre-split augmentation leakage, train-in-test contamination, and evaluation-metric errors severely distort published OPG metrics — directly quantified by the **`+30.4% mAP@0.5` (`+50.2% mAP@0.5:0.95`) inflation** between pre-augmented `P0011` (`0.9194 / 0.7794`) and deduplicated `P0008` (`0.494–0.615 / 0.230–0.277`) on the exact same `Do et al. (2024)` cohort and `YOLOv12-m` architecture.

## scope

- Mandatory methodological governance across dataset curation (`S04 / STEP-010`) and deterministic metric evaluation (`O2`).

## evidence IDs/locators

- **Smoking-gun paired leakage proof (`Do et al., 2024` / `YOLOv12-m`):** `P0011` (`Table 1 & 4`, pp. 11, 17) used all `17,004` pre-augmented copies (`mAP@50 = 0.9194, mAP@50-95 = 0.7794`) vs `P0008` (`Tables 4 & 6`, pp. 4, 17, 19) deduplicated to `3,924` originals (`YOLO12m`: `0.494/0.230` full, `0.615/0.277` tiled, `0.664/0.333` final).
- **Additional confirmed pre-split augmentation / split leakage:** `P0006` (`2,405 -> 4,768` before `80/10/10`, confirmed `p. 10`); `P0021` (`15,000 -> 20,000` teeth before `90/10` tooth split -> `F1 = 0.9941`); `P0025` (`687 -> 1,025` before 4-fold CV); `P0002` (Gingivitis/Hypodontia pre-split aug); `P0036` (evaluates `500` OPGs contributing `2,161` training crops vs `clean mIoU = 0.484`); `P0040` (`14,000`-crop random Stage-2 split); `P0005` (`100%` `Inverted` Mendeley scores).
- **Deterministic metric / mathematical contradictions:** `P0014` (`Table II` vs `III` + `P` vs COCO `AP`); `P0020` (`F1 > max(P,R)`: `0.917/0.871 -> F1 0.925`); `P0022` (`P = 1.000` on `R = 0.000`, `Screw` claim; `mAP50-95 > mAP50`); `P0025` (`P=1.00 [conf=0.905], R=0.96 [0.000], F1=0.76 [0.319]`); `P0033` (`Fig. 1` vs `Table 1`); `P0036` (dropping `519` FPs to inflate `Weighted κ = 0.943`).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- Exemplary leak-free protocols DO exist in `P0008` (strict deduplication + OPG-level split), `P0003` (patient-level split), `P0012` (`1` OPG/patient), and `P0032` (`242`-patient test holdout).

## uncertainty

Low: every numerical mismatch and pre-split augmentation sequence is explicitly documented in the source texts and `T05` verification tables.

## permitted wording

*"Forensic extraction demonstrates that pre-split augmentation (`P0002, P0006, P0011, P0021, P0025`), train-in-test leakage (`P0036, P0040`), and inconsistent metric/threshold calculation (`P0014, P0020, P0022, P0025`) substantially inflate literature benchmarks (`+30.4%` in `P0011` vs `P0008`), enforcing strict deduplication and deterministic patient/OPG-level splits in Phase 2."*

## verification

Verified directly across Core `T05` summaries and `GAP0005.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§4.1`, `§5`); `02_Literature/gap_notes/GAP0005.md`.
