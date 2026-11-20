# Study Limitations, Modality Boundaries & Non-Clinical Interpretation Guardrails (`STEP-036` / `G13`)

| Metadata | Value |
|---|---|
| Step / Gate | `STEP-036` (`S12` — Review errors, annotation uncertainty and limitations; `G13 = PASS`) |
| Owners | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |
| Date | `2026-11-21` |
| Companion Evidence | [final_evaluation_report.md](./final_evaluation_report.md), [error_review.md](./error_review.md), [timing_report.md](./timing_report.md) |
| Governing Sections | `OS §1.3`, `§4.4`, `§6`, `§7.5`, `§9` |

---

## 1. Modality & Radiographic Physics Limitations (2D OPG vs 3D CBCT / Intraoral)

1. **2D Projective Superimposition:** Orthopantomograms compress 3D maxillofacial anatomy onto a single curved focal trough. As visually confirmed in `STEP-036` (`DS0005_IMG_000367`, `DS0001_IMG_000509`, `DS0004_IMG_015992`), cervical spine ghost shadows obscure anterior caries/apices, vertebral edges mimic metallic hardware, and anatomical radiolucencies (mental foramen, incisive canal, maxillary sinus recess) mimic periapical lesions.
2. **No Equivalence to 3D CBCT or Intraoral Bitewing/Periapical Radiographs:** Per `scope.md v1.0.0` and literature evidence (`CLAIM0006`, `P0039`, `P0032`), 2D OPG has lower intrinsic physical sensitivity for incipient enamel caries and buccal/palatal apical bone defects than bitewings or 3D CBCT. All detections in this study are strictly **radiographic box observations on 2D OPG**, never definitive histological or chairside diagnoses.

## 2. Dataset, Grouping & Annotation Limitations

3. **Bounded Patient-Independence Claim (`DEC0007`):** Public secondary datasets (`DS0001–DS0006`) omit cryptographic patient IDs. Although connected-component `SHA-256` + perceptual-hash + intensity-correlation grouping eliminated `281` redundant copies and guaranteed `0` cross-partition exact/near-duplicate leaks (`SPLIT0001–SPLIT0006`), two distinct non-duplicate longitudinal OPGs of the same patient taken years apart could theoretically exist across partitions if unlinked in the public metadata.
4. **Source Reference-Label Incompleteness & Subjectivity:** Direct `T19` visual review of `EVAL0001` (`DS0001_IMG_000722`) exposed sparsely annotated source radiographs where visibly radiopaque endodontic treatments and prosthetic bridges lacked ground-truth boxes, inflating apparent `FP_Bkg`. Similarly, `DS0003` selectively annotates only `~2.8` healthy teeth per OPG (causing `69.4%` `FP_Bkg` when the detector boxes other healthy teeth), and ordinal boundaries (`PAI 3 ↔ 4 ↔ 5` in `TrackD`, `Caries ↔ Deep_Caries` in `TrackB`, `Retained_Root ↔ Cavitated` in `TrackE`) carry inherent inter-observer subjectivity.
5. **Non-Comparable Track Granularities:** `TrackA`/`TrackD`/`TrackF` use tight focal lesion-level AABBs (`Small < 0.2%` area), whereas `TrackB`/`TrackC`/`TrackE` use whole-tooth AABBs (`Medium/Large`). Higher `mAP@0.50` on `TrackE` (`0.8246`) vs `TrackA` (`0.4165`) reflects both taxonomy/granularity and single-scanner consistency — tracks must **never** be ranked directly against one another.
6. **Small-Sample & Ultra-Rare Class Ceilings:** `TrackF` pediatric mixed dentition (`121` train / `24` test OPGs, `100%` `< 0.2%` small boxes) yielded `test mAP@0.50 = 0.0537`, and ultra-rare classes (`TrackA Apical_Surgery` `GT=10`, `TrackC Fractured_Tooth` `GT=2`) had near-zero test AP (`0.0000–0.0428`), establishing clear data-support minimums before automated detection is reliable.

## 3. Generalization, Training & Compute Limitations

7. **Cross-Country Radiolucency Domain Collapse (`HC01`/`HC02`):** While high-contrast structural findings (`HC03 Impacted Tooth`) generalized zero-shot across 4 countries (`AP@0.50 = 0.697–0.818`), subtle radiolucent pathologies (`HC02 Periapical`: `0.178–0.236`; `HC01 Caries`: `0.163`) degraded sharply under unseen country/scanner/protocol shifts. Any deployment at a new clinic requires local external validation and/or target-domain fine-tuning.
8. **Single-Seed Training Matrix & Model Scope:** Under free Kaggle GPU quotas (`30 h/week`), each of the `13` experiments was trained with one locked seed (`20261124`) rather than `3–5` repeated seeds; statistical uncertainty is therefore quantified via `1,000`-resample `GroupID` cluster bootstrap `95% CI` over held-out test cohorts rather than training-seed variance. Model scope was intentionally fixed to the approved single-stage YOLO family (`YOLO11s`, `YOLOv8s`, `YOLO11m`); two-stage or transformer baselines (e.g., Faster R-CNN, RT-DETR) remain outside this study's scope.
9. **Timing & Hardware Variability:** Local CPU latencies (`201.6–878.1 ms/OPG` on `Intel i5-1135G7`) depend on single-machine OS scheduling and thermal state (`IQR` and `p95` reported in `timing_report.md`). Serial `BS=1` latency must not be conflated with batched throughput or real-time clinical workflow efficiency.

## 4. Strict Non-Clinical Research Boundary (`OS §1.3` / `G13`)

10. **No Clinical Diagnostic or Screening Clearance:** None of the models (`MODEL0001–MODEL0013`), prototypes, or web demonstrations in this thesis constitute a certified medical device or validated clinical diagnostic aid. **A missed detection (zero predicted boxes) MUST NEVER be interpreted as proof of disease absence**, and all outputs require independent interpretation by a qualified dental clinician.
