# Front Matter, Institutional Declarations & Abstract (`WRIT0001`)

> **Manuscript Status:** `STEP-040` Complete Evidence-Grounded Draft (`v1.0.0`, `2026-11-21`).  
> **Pending Institutional Confirmations (`DEC0017` / `UD17`):** Exact final defense date and official DIU CSE formatting/cover template confirmation remain pending Supervisor Ms Faiza Feroz sign-off before `G15`.

---

## Title Page

**A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO**

A Thesis Submitted to the Department of Computer Science and Engineering in Partial Fulfillment of the Requirements for the Degree of **Bachelor of Science in Computer Science and Engineering**

**Submitted By:**
- **Akhtaruzzaman Anik** — Student ID: `232-15-252` *(Data Stewardship, Preprocessing, Research Prototype & Reproducibility Lead)*
- **Mahajub Al Shabah** — Student ID: `232-15-900` *(Literature Review, Annotation QA, Modeling & Evaluation Lead)*

**Supervised By:**
- **Ms Faiza Feroz** — Lecturer, Department of Computer Science and Engineering (Supervisor)
- **Israt Jahan** — Senior Lecturer, Department of Computer Science and Engineering (Co-supervisor)

**Department of Computer Science and Engineering**  
**Daffodil International University (DIU)**  
**Dhaka, Bangladesh**  
*[Final Defense Month / Year — Pending Institutional Calendar Confirmation under `UD17`]*

---

## Declaration of Originality

We hereby declare that this thesis, titled *"A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO"*, is our own original work prepared under the supervision of Ms Faiza Feroz and Israt Jahan in the Department of Computer Science and Engineering, Daffodil International University. All primary literature references are drawn exclusively from our verified canonical bibliography (`02_Literature/references.bib`), all six secondary panoramic radiograph datasets are properly attributed under their original source licenses, and every quantitative metric, confidence interval, error count, and timing figure is programmatically reconciled to locked evaluation artifacts (`FREEZE0001`, `G01–G14 PASS`).

- **Akhtaruzzaman Anik (`232-15-252`)** — Signature: `______________________` Date: `____________`
- **Mahajub Al Shabah (`232-15-900`)** — Signature: `______________________` Date: `____________`

---

## Non-Clinical Research Scope Statement

This research evaluates deep-learning object detection strictly on secondary, de-identified 2D orthopantomogram (OPG) radiographs as an **academic research benchmark and supplementary research prototype**. None of the trained models (`MODEL0001–MODEL0013`) or software interfaces (`OPGPrototypeEngine`) constitute a certified medical device or validated clinical diagnostic aid. Predicted confidence scores are not clinical diagnostic probabilities, **zero predicted bounding boxes never exclude dental disease**, and all radiographic interpretation must be performed independently by a qualified dental clinician.

---

## Abstract

Panoramic dental radiography—orthopantomography (OPG)—is among the most widely acquired full-arch screening modalities in dentistry, yet automated multi-object detection on 2D OPGs faces severe methodological pitfalls across the published literature. A systematic audit of `122` screened publications (`42` verified full-text Core studies) reveals that `84.9%` (`62/73`) of prior dental YOLO studies omit strict multi-threshold localization (`mAP@0.50:0.95`), `87.7%` (`64/73`) lack external validation, `73.8%` (`31/42`) omit per-image inference latency, and pre-split augmentation leakage inflates reported benchmarks by up to `+30.4%` `mAP@0.50`.

To address these gaps under strict experimental governance, we construct a leakage-controlled, six-cohort 2D OPG benchmark spanning `7,457` canonical de-duplicated radiographs (`41,103` bounding boxes across Romania, Türkiye, Bangladesh, Vietnam, and the United Arab Emirates) organized into six non-merged, license-isolated tracks (`TrackA–TrackF`, `CLS0001–CLS0041`) with connected-component duplicate-cluster `70/15/15` splits (`0` cross-partition leaks) and invertible coordinate-preserving preprocessing (`max round-trip error <= 0.0041 px`). Across `13` controlled Kaggle `Tesla T4` experiments (`EXP0001–EXP0013`) locked prior to test access (`FREEZE0001`, `0` prior test exposure), held-out evaluation (`1,082` internal `test` + `178` external-hospital OPGs) using a frozen deterministic evaluator with `1,000`-resample `GroupID` cluster bootstrap `95%` confidence intervals yields four core empirical findings:

1. **Multi-Cohort Leak-Free Performance (`RQ0`):** Single-stage `YOLO11s` achieves held-out `test mAP@0.50` of **`0.8246`** (`95% CI [0.7907, 0.8592]`, `mAP@0.50:0.95 = 0.5163`, `Implant AP@0.50 = 0.9980`) on `TrackE` (UAE `6`-class), **`0.4868`** (`0.2207`) on `TrackD` (Hanoi periapical `PAI 3–5` `@1280px`), **`0.4397`** (`0.2673`) on `TrackB` (DENTEX `4`-class), **`0.4165`** (`0.1741`; unseen external hospital **`0.4338`** / **`0.2038`**) on `TrackA` (Romania `13`-class `@1280px`), **`0.2508`** (`5`-class pathology `0.2631`) on `TrackC` (Dhaka handheld `6`-class), and **`0.0537`** on `TrackF` (pediatric small-N mixed dentition), documenting clear small-sample and diffuse-lesion ceilings.
2. **Radiographic Contrast Hierarchy & `5`-Country Domain Shift (`RQ1`):** Across `12` zero-shot cross-country shift bridges spanning five countries (`HC01–HC05`), high-contrast structural targets (`HC03` Impacted Tooth) generalize strongly without target training (`AP@0.50 = 0.8181` Romania→Türkiye, `0.7109` Romania→Bangladesh, `0.6967` UAE→Türkiye), whereas low-contrast radiolucencies collapse sharply (`HC02` Periapical `0.1779–0.2355`; `HC01` Whole-Tooth Caries `0.1627–0.1635`).
3. **Controlled Preprocessing & Resolution Ablation (`RQ2`):** `CLAHE` consistently degraded validation `mAP@0.50` in `3/3` controlled pairs (`-0.018` to `-0.037`), refuting blanket contrast-enhancement claims. Conversely, increasing input scale from `640px` to `1280px` improved held-out detection on both tested cohorts (`+0.0449` `mAP@0.50` and `+20.2%` relative `mAP@0.50:0.95` with non-overlapping `95% CIs` on `TrackD`; `+0.0350` internal and `+0.0622` external `mAP@0.50` on `TrackA`).
4. **Bounded End-to-End Speed, Error Taxonomy & Reproducibility (`RQ3`):** Under serial `batch = 1` `FP32` timing (`0` errors), pure GPU `FPS_infer` (`20.2–70.4`) exceeds true end-to-end `FPS_e2e` (`6.35–38.20`) by `1.8×–5.6×`. Exported static `ONNX` models running on a standard laptop CPU (`Intel Core i5-1135G7`, `ONNXRuntime 1.32.0`) achieve `0.983–0.997` PyTorch box parity IoU at **`201.6 ms/OPG`** (`4.96 FPS_e2e`) for `TrackE@640` and **`847.9–878.1 ms/OPG`** (`1.14–1.18 FPS_e2e`) for `1280px` models. Systematic `T19` error analysis (`6,718` GT boxes) exposes a `2.6×` recall drop from large (`80.3%`) to small `< 0.2%` area targets (`30.9%`), source-label incompleteness (`DS0001_IMG_000722`), and ordinal severity boundary swaps (`86.7%` of `TrackD` class errors). A packaged `OPGPrototypeEngine` and clean-environment audit (`R1–R3 PASS`: `50/50` checksums, `Δ = 0.0` metric replay) ensure end-to-end reproducibility.

**Keywords:** Orthopantomogram (OPG), Panoramic Dental Radiography, YOLO11, Object Detection, Leakage-Controlled Evaluation, Cross-Country Domain Shift, CLAHE Ablation, ONNXRuntime, Error Analysis.

---

## Acknowledgements

We express our deepest gratitude to our supervisor, **Ms Faiza Feroz** (Lecturer, Dept. of CSE, DIU), and co-supervisor, **Israt Jahan** (Senior Lecturer, Dept. of CSE, DIU), for their continuous guidance, methodological feedback, and oversight across every stage of this work. We gratefully acknowledge the research groups who publicly shared de-identified panoramic radiograph datasets under open research licenses: the UMFIH team (`DS0001`, Romania), the DENTEX Challenge organizers (`DS0002`, `CC-BY-NC-SA-4.0`, Türkiye), Rahman et al. (`DS0003`, Bangladesh), Do et al. (`DS0004`, Vietnam), Alabd-Aljabar et al. (`DS0005`, Ajman University, UAE), and Rahimi et al. (`DS0006`, MD-OPG).

---

## List of Abbreviations

| Abbreviation | Full Term |
|---|---|
| `AABB` / `OBB` | Axis-Aligned Bounding Box / Oriented Bounding Box |
| `AP` / `mAP` | Average Precision / Mean Average Precision |
| `BDC / BDR` | Broken-Down Crown / Broken-Down Root |
| `BS` | Batch Size |
| `BW` / `PA` | Intraoral Bitewing / Periapical Radiograph |
| `CBCT` | Cone-Beam Computed Tomography (3D — strictly out of scope for modeling) |
| `CI` | Confidence Interval (`1,000`-resample `GroupID` cluster bootstrap `95% CI`) |
| `CLAHE` | Contrast Limited Adaptive Histogram Equalization |
| `FPS_e2e` / `FPS_infer` | End-to-End Frames Per Second / Model-Only Forward Frames Per Second |
| `GT` | Ground Truth |
| `HC01–HC05` | Harmonized Cross-Cohort Evaluation Concept Bridges `1–5` |
| `IoU` | Intersection over Union |
| `NMS` | Non-Maximum Suppression (`class-aware`, `IoU = 0.65`) |
| `ONNX` | Open Neural Network Exchange |
| `OPG` | Orthopantomogram (2D Panoramic Dental Radiograph) |
| `PAI` | Periapical Index (`PAI 3–5` radiographic severity grades) |
| `TP / FP / FN` | True Positive / False Positive / False Negative |
| `YOLO` | You Only Look Once (single-stage object detector family) |
