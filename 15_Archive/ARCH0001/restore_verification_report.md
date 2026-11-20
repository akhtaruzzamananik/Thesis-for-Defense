# `STEP-045` Immutable Release Archive & Restoration Verification Report (`ARCH0001`)

| Metadata | Value |
|---|---|
| ArchiveID / ReleaseTag | `ARCH0001` · `v1.0.0-arch0001` |
| Governing Decision | [DEC0020.md](../../01_Project_Management/decision_log/DEC0020.md) (`UD20` — 3-Tier Lawful Archival Policy) |
| Canonical Registry | [archive_manifest.csv](../archive_manifest.csv) (`35` inventoried items, `100%` SHA-256 verified) |
| Release Owners / Custodians | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |
| Retention Window | `5` years post-defense (`2026–2031`) |
| **Overall Restore Verdict** | **`PASS`** *(completed in `3.94 s` in isolated clean-room temp directory)* |

---

## 1. End-to-End Clean-Room Restoration Verification Summary

| Verification Dimension (`STEP-045` Procedure 3) | Tested Scope | Observed Result | Verdict |
|---|---|---|---|
| **1. Immutable Public Source Snapshot (`git archive`)** | `11,786,240` bytes (`sha256: 3a9d8a1b34ec42ad...`) | Extracted to fresh temp directory (`PYTHONPATH` stripped); `validate_repo.py` exit `0` | **PASS** |
| **2. Public Tier-1 vs Restricted Tier-2/3 Custody** | `42` total items (`25` Tier-1 + `17` Off-Git) | `18/18` Public Tier-1 restored bit-for-bit; `17/17` Restricted `.pt`/`.onnx` verified off-Git & `0` leaked into tar | **PASS** |
| **3. Submission Bundle & Paper Recovery** | `SUBBUNDLE_DIU_CSE_THESIS_v1.0.0` (`33` files) + `manuscript_draft.md` | `33/33` submission files recovered with exact SHA-256 match | **PASS** |
| **4. Deterministic Metric Replay (`restored evaluator.py`)** | `EVAL0001` (`TrackA@1280`), `EVAL0011` (`TrackD@1280`), `EVAL0013` (`TrackE@640`) | `ΔmAP@0.50 = 0.0` across all `3` replayed evaluations (`TP/FP/FN` exact) | **PASS** |
| **5. Live ONNX Model Restore (`restored OPGPrototypeEngine`)** | `MODEL0008.onnx` on raw held-out `DS0005_IMG_000005` | Status `OK`, `12` boxes in `203.48 ms` | **PASS** |

---

## 2. Three-Tier Access, Licensing & Retention Guide (`DEC0020`)

- **Tier 1 (`Public-Tier1`, Git & Tag `v1.0.0-arch0001`):** Code (`MIT`), manifests/protocols/figures/tables/manuscripts (`CC-BY-4.0`). Publicly cloneable without restriction.
- **Tier 2 (`Restricted-Tier2-OffGit`, `08_Checkpoints/artifacts/` + Private Team Drive):** `9` `CC-BY-4.0`-trained `.pt` checkpoints, `7` `.onnx` exports, `STEP-032` `predictions.jsonl`, and visual error sheets. Available for academic verification via SHA-256 pointers in `archive_manifest.csv`.
- **Tier 3 (`Restricted-Tier3-NC-SA-Isolated`):** `DS0002` DENTEX radiographs and `MODEL0004` (`EXP0003/weights/best.pt`) remain strictly isolated under `CC-BY-NC-SA-4.0` (never exported to ONNX or commercial bundles).
- **Additive Future Archive Rule:** When `G15` supervisor sign-off / `STEP-043` institutional receipt or `STEP-047–049` web-demo deployment (`DEPLOY0001`) is finalized, an additive `ARCH0002` entry will be appended without modifying or overwriting `ARCH0001`.
