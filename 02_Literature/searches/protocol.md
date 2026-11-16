# Literature search and screening protocol — STEP-004

| Field | Value |
|---|---|
| Record | `02_Literature/searches/protocol.md` |
| Step / gate | STEP-004 / feeds G03 (at STEP-009) |
| Version | v0.1.0 (DRAFT) |
| Status | **DRAFT — awaiting G01/G02 PASS and Research Lead/Supervisor approval. No search executed yet.** |
| Owners | Mahajub Al Shabah (Literature Lead); Akhtaruzzaman Anik (Reviewer); Ms Faiza Feroz (Supervisor) |
| Governing sections | OS §1, §3; Blueprint STEP-004 |

> **Gate notice:** Per OS §13.1 and Blueprint STEP-004, `G01` and `G02` are currently `NOT ASSESSED`. This protocol draft prepares STEP-004 documentation without claiming `G01`/`G02` passed and without executing `STEP-005` searches yet.

## 1. Purpose: testing proposed gaps G1–G6

The title report proposes six gap themes (`G1–G6`, `RF14`) and lists `[1]–[13]` as seed references. Those gaps are **hypotheses to challenge**, not proven facts (`OS §3.3`). This protocol actively searches for **both supporting and contradicting** evidence, especially existing 2D OPG YOLO detectors that already detect dental objects or report FPS.

## 2. Candidate sources and access plan

| Source | Focus | Access status (to confirm before STEP-005) |
|---|---|---|
| **PubMed / PubMed Central** | Dental / clinical radiology OPG detection studies | Open search + open-access PMC full text |
| **IEEE Xplore** | YOLO / computer-vision dental X-ray papers | Index open; full text requires DIU library / subscription |
| **ScienceDirect / Scopus / Web of Science** | Peer-reviewed dental AI & benchmarks | Requires DIU institutional access (log if unavailable) |
| **Google Scholar** | Cross-publisher & recent preprints/conferences | Open search; follow original publisher links |
| **arXiv / OpenAlex / publisher OA** | Open-access YOLO/OPG detection preprints & code | Open access (link preprint to published version; never double-count) |
| **Report references `[1]–[13]` (`RF14`)** | Seed leads from title report | Unverified (`UD19`); verify metadata against original publisher |

Record any inaccessible database or paywalled full text explicitly as a coverage limitation (`OS §3.1`). Never bypass access controls or summarize from abstracts as if full text was read.

## 3. Search queries (exact seeds to adapt per database)

### Query Q1 — Direct 2D OPG object detection and YOLO (primary)

```text
(orthopantomogram OR orthopantomography OR OPG OR "panoramic radiograph" OR "panoramic dental")
AND (dental OR tooth OR teeth OR caries OR lesion OR restoration OR impacted)
AND ("object detection" OR localization OR localisation OR YOLO OR YOLOv5 OR YOLOv7 OR YOLOv8 OR YOLOv9 OR YOLOv10 OR YOLOv11)
```

### Query Q2 — Image quality, preprocessing, and annotation uncertainty in OPG (tests G5)

```text
(orthopantomogram OR OPG OR "panoramic radiograph")
AND (enhancement OR preprocessing OR CLAHE OR denoising OR annotation OR "inter-observer" OR "ground truth")
AND (detection OR YOLO OR bounding)
```

### Query Q3 — Modality & task boundaries: 2D OPG vs CBCT / segmentation / classification (tests G2–G4)

```text
(orthopantomogram OR OPG OR "panoramic radiograph")
AND (CBCT OR "cone beam" OR segmentation OR classification)
AND (detection OR localization OR review OR benchmark)
```

### Search log rules

- Log every search execution in `02_Literature/searches/SEARCH####_<db>_<date>.md` using `search_log_template.md` (`T04`).
- Record exact database syntax, date executed, year/language coverage window, applied filters, raw result count, exported record pointer, deduplication count, and limitations.
- **No arbitrary paper quota** (`STEP-004`).

## 4. Eligibility & classification rules

### Relevance groups

| Group | Criteria | Role in synthesis |
|---|---|---|
| **Group A — Direct evidence** | 2D OPG radiographs + bounding-box object detection (YOLO or comparative box detectors) reporting localization metrics | Primary comparison for `RQ1–RQ3`, `G1–G3`, `G6` |
| **Group B — Contextual / methodological** | 2D OPG classification/segmentation, 3D CBCT comparison, annotation reliability, preprocessing/enhancement, or systematic dental AI reviews | Context for `G2–G5`, methodology & limitations (never ranked directly against 2D box AP) |

### Inclusion criteria

1. Peer-reviewed journal/conference paper, or traceable preprint/benchmark report with clear methodology.
2. Focuses on dental radiographs (primarily 2D OPG; Group B allows CBCT/segmentation only for explicit modality/task comparison) or relevant YOLO OPG methodology.
3. English full text lawfully accessible (or accessible abstract clearly flagged `abstract-only — excluded from numerical extraction`).

### Exclusion criteria (record one code per full-text exclusion in `screening.csv`)

- `EXC-MODALITY`: Non-dental imaging or 3D modality unrelated to OPG comparison.
- `EXC-TASK`: Non-vision or unrelated clinical workflow without detection/localization/OPG methodological value.
- `EXC-NO-FULLTEXT`: Full text legally unavailable (`never summarize unread PDFs`).
- `EXC-DUP`: Exact duplicate, mirror, or preprint superseded by an included journal version (link `DuplicateOf`).
- `EXC-UNVERIFIED`: Broken/unresolvable metadata or retracted source.
- `EXC-NON-ENGLISH`: Full text not in English and no reliable translation available.

## 5. Deduplication & quality appraisal rules

1. **Deduplicate before counting:** Match by DOI first, then normalized title + year + first author. Link preprints and conference-to-journal extensions in `screening.csv` (`DuplicateOf`) so one study is never counted twice.
2. **Verify `RF14` `[1]–[13]` (`UD19`):** Do not copy report reference text blindly (encoding/publisher string anomalies were flagged in `OS §9.3`). Check against publisher DOI pages.
3. **Methodological quality appraisal (not citation count):**
   - Dataset source, public vs private, sample size (`patients` vs `images`).
   - Class ontology clarity and annotator/dental expertise.
   - Partitioning & data-leakage risk (patient-level split vs random image split vs unspecified).
   - Metric precision (IoU threshold, `mAP@0.5` vs `mAP@0.5:0.95`, hardware & timing boundary for `FPS`).
   - Code/dataset availability and stated limitations.

## 6. Screening & extraction workflow (`STEP-005`–`STEP-007`)

1. **STEP-005:** Run approved queries, log exports, deduplicate, assign `P####` in `02_Literature/papers.csv`, update `references.bib`.
2. **STEP-006:** Title/abstract screen, then full-text screen (`Mahajub` primary, `Anik` conflict/spot check) in `screening.csv`.
3. **STEP-007:** Extract full-text papers using `T05` into `02_Literature/summaries/P####.md`, marking unstated items `not reported`.
4. **STEP-008–009:** Test `G1–G6` in `gaps.csv` / `gap_notes/`, map verified claims in `claims.csv`, finalize `research_questions.md`, and assess `G03`.

## 7. Approval block (human sign-off required before STEP-005)

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Literature Lead | Mahajub Al Shabah | | | |
| Research Lead / Reviewer | Akhtaruzzaman Anik | | | |
| Supervisor | Ms Faiza Feroz | | | |
