# Screening Summary (`STEP-005` / `STEP-006`) — Combined Intake Reconciliation

- **Date:** 2026-11-16
- **Governing protocol:** `02_Literature/searches/protocol.md` (`v1.0.0`)
- **Intake logs:** `SEARCH0001` (Anik: 113 files / 99 unique), `SEARCH0002` (Shabah: 67 files / 50 unique)

## PRISMA-Style Reconciliation Flow

| Stage | Count | Notes |
|---|---:|---|
| Records identified & downloaded (`SEARCH0001` + `SEARCH0002`) | **180 files** | `113` Anik (497.9 MB) + `67` Shabah (254.7 MB) = `752.6 MB` |
| Duplicate file copies removed before screening | **58 copies** | Exact SHA-256 duplicates, publisher/multi-query copies, and cross-named DOI `10.32604/cmc.2025.068797` |
| **Unique studies screened (`papers.csv` / `screening.csv`)** | **122 studies** | `72` Anik-only + `27` Both + `23` Shabah-only (`42` Core PDFs retained locally = `185.0 MB`) |
| Excluded at title/abstract screening (`P0098`–`P0122`, PDFs pruned) | **25 studies** | `EXC-UNVERIFIED`: 1 (`P0122`), `EXC-NO-FULLTEXT`: 1 (`P0107`), `EXC-MODALITY`: 9 (`P0098`–`P0106`), `EXC-TASK`: 14 (`P0108`–`P0121`) |
| Retained in Reserve Pool (`P0043`–`P0097`, metadata-only; PDFs pruned) | **55 studies** | `High_Priority_14` (`P0043`–`P0056`) + `Secondary_41` (`P0057`–`P0097`) |
| **Core Included for `STEP-007` Full-Text Extraction (`02_Literature/papers/`)** | **42 studies** | **`Group A` (25):** `P0001`–`P0025` · **`Group B` (17):** `P0026`–`P0042` · Assigned `21` Anik / `21` Shabah |

## Next Action (`STEP-007`)

1. Both researchers extract their 21 assigned Core papers (`P0001`–`P0042`) into `02_Literature/summaries/P####.md` using `T05`, logging exact dataset counts, class maps, split level, IoU threshold, hardware/FPS boundary, and limitations (explicitly writing `not reported` when absent).
2. Verify `RF14` (`[1]–[13]`) links and metadata (`UD19`) before `G03` (`STEP-009`).
