# T07 — Claim traceability record (`02_Literature/claim_notes/CLAIM0007.md`)

| Metadata | Value |
|---|---|
| TemplateID | T07 |
| template_version | v1.0.0 |
| entity_id | CLAIM0007 |
| owner | Mahajub Al Shabah |
| reviewer | Akhtaruzzaman Anik |
| date | 2026-11-17 |
| status | Verified-Literature-STEP-008 |
| source_inputs | `02_Literature/summaries/P0015.md`, `P0016.md`, `P0023.md`, `P0024.md`, `P0028.md`–`P0030.md` |
| governing_section | OS §9.1 |

## Exact statement

Within `2D OPG` itself, external cross-scanner, cross-clinic, and acquisition-protocol domain shifts consistently cause large performance drops (`-9.0%` to `-22.2%` `mAP@0.50` in `P0015, P0016, P0023`; `-10.26% IoU` in `P0029`; `-0.048` to `-0.052` `mAP@0.50` + device bite-block hallucinations in `P0030`).

## scope

- Applies to external hold-out 2D OPG validation studies (`GAP0004` / `G4`).

## evidence IDs/locators

- `P0023` (`Mureșanu 2024`, `Tables 2–3`, pp. 3–4, `UMFIH` -> `180` external): `YOLOv8` dropped **`mAP@0.50 = 0.600 -> 0.451` (`-14.9%`)** (`API 0.547->0.315`, `CAR 0.509->0.373`).
- `P0015` (`Eftimie 2025`, `Tables 1–2`, pp. 7–8, same `UMFIH` + `180` external): `RT-DETR-l` dropped **`0.7697 -> 0.5476` (`-22.21%`)** and `YOLO11m` dropped **`0.7416 -> 0.5366` (`-20.50%`)**.
- `P0016` (`Şevik & Mutlu 2025`, `Tables 4–9`, pp. 11–15): `YOLOv11x` dropped from `mAP50 = 0.91 (F1=0.93)` internal (`Zhang 2023`) to **`0.82 (F1=0.81)` (`-9.0%`)** on `150` external Roboflow pediatric OPGs.
- `P0029` (`Nayak 2026`, `Table 19`, p. 28): `ToothLens Mask R-CNN` dropped from `IoU = 79.74% (R=87.00%)` internal to **`69.48% (R=71.90%)` (`-10.26% IoU`)** on `30` external Tufts OPGs.
- `P0030` (`Nishimura 2026`, `Tables 2–4, Fig. 6`, pp. 358–362): Japan<->China bidirectional shift dropped `mAP@0.5` by `-0.048` to `-0.052`, with non-bite-block models hallucinating radiopaque plastic bite blocks as primary tooth `A`.
- Acquisition caveat: `P0024` introduces handheld Samsung A52 X-ray film re-photography (`1176×603` px, Dhaka) vs native DICOM/PNG (`~2500×1500` px) in `P0015/P0032`, highlighting real-world device heterogeneity (`P0028` cites `56%` vs `30.7%` non-diagnostic observer disagreement).
- **Empirical repo verification:** `ExperimentIDs = not-run-yet`; `EvaluationIDs = not-run-yet`.

## contradictions

- `P0021` claimed external validation (`99.05%` Acc) on Mendeley `[38]` (`Brahmi & Jdey 2023`) without domain drop, but `[38]` is a `107`-OPG binary tooth segmentation dataset lacking `P0021`'s 6-class box schema (`P0021.md` §5.2).

## uncertainty

Low: every verified multi-center OPG benchmark (`P0015, P0016, P0023, P0029, P0030`) exhibits substantial external degradation (`P0015` and `P0023` share `UMFIH` cohorts).

## permitted wording

*"Verified external-OPG evaluations (`P0015, P0016, P0023, P0029, P0030`) document `9%` to `22.2%` `mAP@0.50` / `IoU` degradation and bite-block artifacts under cross-center shifts, directly motivating multi-source or cross-cohort external OPG testing (`S04`/`S08`)."*

## verification

Verified directly across Core `T05` summaries and `GAP0004.md` (`STEP-008`).

## writing locations

`02_Literature/synthesis.md` (`§2`, `§3.2`, `§5`); `02_Literature/gap_notes/GAP0004.md`.
