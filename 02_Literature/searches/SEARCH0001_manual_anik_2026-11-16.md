# Search log — SEARCH0001 — Manual Intake Batch (Akhtaruzzaman Anik)

| Metadata | Value |
|---|---|
| TemplateID | T04 |
| template_version | v1.0.0 |
| entity_id | SEARCH0001 |
| owner | Akhtaruzzaman Anik (manual collection batch; reviewed with Mahajub Al Shabah) |
| date | 2026-11-16 |
| status | Historical manual batch registered for STEP-005 traceability |
| source_inputs | `02_Literature/searches/protocol.md` |
| governing_section | OS §3.1 |
| sensitivity | Public metadata |
| reviewer | Mahajub Al Shabah / Akhtaruzzaman Anik |

## Database

Cross-publisher manual PDF collection (Publisher OA, ScienceDirect, IEEE Xplore, MDPI, Springer/BMC, Nature Scientific Reports, Oxford DMFR/EJO, PLOS One, arXiv) organized locally under `Paper(downloaded by Anik)/`.

## Exact query

Manual queries aligned with `protocol.md` themes (`Q1-A` YOLO OPG detection, `Q1-B` other OPG object detectors, `Q2-A` preprocessing/CLAHE, `Q2-B` annotation/ground-truth quality, `Q3` 2D OPG vs CBCT/segmentation/classification).

## Date

Collected on/before 2026-11-16.

## Coverage (years / document types)

Observed publication years 2019–2026; journal articles, conference papers, data articles, reviews, and preprints (`2012.13666v1`, `2511.22911v1`).

## Filters

Manual screening for OPG/dental AI PDF availability; exact per-database filter strings were not exported separately.

## Counts (raw / after dedup / screened)

- Raw files in `Paper(downloaded by Anik)/`: **113 PDFs** (497.9 MB) across 5 subfolders (`42 + 17 + 8 + 28 + 18`).
- Internal duplicates removed (SHA-256 + normalized filename): **14 duplicate copies**.
- Unique studies contributed by `SEARCH0001`: **99 unique papers** (`72` Anik-only + `27` also in `SEARCH0002`).

## Export / pointer

Originally collected under `Paper(downloaded by Anik)/` (removed after deduplication); all 122 unique citations are indexed in `02_Literature/papers.csv` and the 42 Core PDFs (`P0001`–`P0042`) are stored flat in `02_Literature/papers/`.

## Deduplication notes

Exact SHA-256 and normalized-filename deduplication merged 14 redundant copies within `Paper(downloaded by Anik)/` and linked 27 shared studies with `SEARCH0002` (`Paper (downloaded by Shabah)/`).

## Supplementary search (forward/backward snowballing / RF14 check)

`RF14` mapping `[1]–[13]` remains `not-mapped-yet` (`UD19`) pending item-by-item check against the verified bibliography.

## Limitations / access constraints

Because files were collected manually across publisher portals prior to automated API export, raw database hit totals before PDF download are unknown (`not recorded`), and paywalled full texts inaccessible through DIU/OA channels may be absent from this intake batch.
