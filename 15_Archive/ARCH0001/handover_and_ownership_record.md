# Post-Project Ownership, Archival Custodianship & Future-Work Handover Record (`STEP-046`)

| Field | Value |
|---|---|
| Archive / Release | `ARCH0001` (`v1.0.0-arch0001`) |
| Governing Decision | [DEC0020.md](../../01_Project_Management/decision_log/DEC0020.md) (`UD20`) |
| Completion Audit | [project_completion_audit.md](../../01_Project_Management/reviews/project_completion_audit.md) (`STEP-046`) |
| Date | `2026-11-21` |
| Primary Archive & Prototype Custodian | **Akhtaruzzaman Anik** (`Student ID: 232-15-252`, Dept. of CSE, DIU) |
| Co-Custodian (Evaluation & Literature) | **Mahajub Al Shabah** (`Student ID: 232-15-900`, Dept. of CSE, DIU) |
| Institutional Academic Supervisor | **Ms Faiza Feroz** (Lecturer, Dept. of CSE, Daffodil International University) |
| Co-supervisor | **Israt Jahan** (Senior Lecturer, Dept. of CSE, Daffodil International University) |

---

## 1. Custody & Maintenance Responsibilities (`2026–2031`)

1. **Public Git Repository (`Tier 1`, `https://github.com/akhtaruzzamananik/Thesis-for-Defense`):**
   - Maintained publicly by Akhtaruzzaman Anik & Mahajub Al Shabah for `>= 5` years post-defense (`2026–2031`).
   - Tag `v1.0.0-arch0001` and `15_Archive/archive_manifest.csv` remain immutable. Any post-defense updates (e.g., `STEP-047–049` web-demo deployment records or `STEP-043` institutional submission receipt confirmation) are added as `ARCH0002` without overwriting `ARCH0001`.
2. **Restricted Off-Git Storage (`Tier 2` & `Tier 3`):**
   - Dual-copy off-Git backups (`08_Checkpoints/artifacts/` + Private Team Google Drive) storing the `10` frozen `.pt` weights, `7` `.onnx` exports, `14` `predictions.jsonl` logs, and `7` visual error review sheets (`EVAL####_review_sheet.jpg`) are co-maintained by both student authors.
   - `DS0002` (DENTEX) and `MODEL0004` (`Tier 3`) remain strictly isolated under `CC-BY-NC-SA-4.0`.

---

## 2. Non-Blocking Future Study Handover Queue (Separated from Current Thesis Scope)

The following extensions are formally handed over for future post-B.Sc. research and do **not** block current project completion:
1. **Stage `S16` Hosted Web Showcase (`STEP-047–049` -> `G17`):** FastAPI + interactive canvas UI wrapping `OPGPrototypeEngine` (`MODEL0008`/`MODEL0005`/`MODEL0013`) with containerization, parity verification, and defense runbook.
2. **Optional External Paper Submission (`STEP-044` Re-activation):** Formatting `11_Writing/paper/manuscript_draft.md` for a concrete open-access dental imaging or IEEE computer-vision venue once all co-authors and Supervisor Ms Faiza Feroz select a target venue (`GA0018`).
3. **Methodological Extensions (Chapter 6 §6.3):**
   - Native-resolution overlapping tiling with background tiles for `< 0.2%`-area pediatric caries (`TrackF`) and small adult focal caries (`TrackA`).
   - Ordinal-aware focal loss and intra-family class-agnostic NMS for `PAI 3–5` (`TrackD`).
   - Unsupervised domain adaptation / local hospital calibration for cross-country radiolucent pathologies (`HC01–HC02`).
   - Multi-seed (`3–5` seeds) variance benchmarking, rotated `YOLO11-OBB` heads (`DS0005`), and `RT-DETR` comparators.
   - IRB-approved prospective clinical multi-reader validation against paired 3D CBCT / intraoral bitewing gold standards.
