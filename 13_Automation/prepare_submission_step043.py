"""STEP-043 DIU CSE Thesis Submission Bundle & Checksum Ledger Generator.

Verifies that all assembled thesis files match 11_Writing/thesis/assembled_manifest.json
bit-for-bit, computes exact SHA-256 checksums across all 33 submission deliverables
(8 modular chapters, assembled MD + print-ready HTML, 17-slide defense deck, 6 vector
SVGs, 12 MD/LaTeX tables, canonical BibTeX bibliography, and 3 cryptographic freeze/audit
manifests), and generates:
  - 11_Writing/thesis/submission_bundle_manifest.json
  - 11_Writing/thesis/submission.md
Strictly obeys Blueprint STEP-043: distinguishes READY_AWAITING_G15_AND_PORTAL_UPLOAD
from SENT_OR_UPLOADED and CONFIRMED_SUBMITTED without fabricating a submission receipt.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS_DIR = ROOT / "11_Writing" / "thesis"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assembled_man = json.loads((THESIS_DIR / "assembled_manifest.json").read_text(encoding="utf-8"))
    md_path = ROOT / assembled_man["outputs"]["markdown"]["path"]
    html_path = ROOT / assembled_man["outputs"]["html_print_ready"]["path"]

    assert sha256_file(md_path) == assembled_man["outputs"]["markdown"]["sha256"], "Assembled MD hash mismatch!"
    assert sha256_file(html_path) == assembled_man["outputs"]["html_print_ready"]["sha256"], "Assembled HTML hash mismatch!"

    bundle_relpaths = [
        # Primary Assembled Deliverables
        "11_Writing/thesis/DIU_CSE_Thesis_Assembled_v1.0.0.md",
        "11_Writing/thesis/DIU_CSE_Thesis_Assembled_v1.0.0.html",
        "11_Writing/slides/defense_slides.md",
        # Modular Chapter Sources (WRIT0001-WRIT0008)
        "11_Writing/thesis/00_front_matter_and_abstract.md",
        "11_Writing/thesis/01_chapter1_introduction.md",
        "11_Writing/thesis/02_chapter2_literature_review.md",
        "11_Writing/thesis/03_chapter3_methodology.md",
        "11_Writing/thesis/04_chapter4_results.md",
        "11_Writing/thesis/05_chapter5_discussion_and_prototype.md",
        "11_Writing/thesis/06_chapter6_conclusion.md",
        "11_Writing/thesis/07_appendices.md",
        # Vector SVG Figures (FIG0001-FIG0006)
        "10_Figures_Tables/figures/FIG0001_study_pipeline.svg",
        "10_Figures_Tables/figures/FIG0002_heldout_scoreboard_ci.svg",
        "10_Figures_Tables/figures/FIG0003_rq2_clahe_vs_1280.svg",
        "10_Figures_Tables/figures/FIG0004_cross_country_shift.svg",
        "10_Figures_Tables/figures/FIG0005_rq3_latency_pareto.svg",
        "10_Figures_Tables/figures/FIG0006_error_and_size_recall.svg",
        # Markdown + LaTeX Tables (TAB0001-TAB0006)
        "10_Figures_Tables/tables/TAB0001_literature_audit.md",
        "10_Figures_Tables/tables/TAB0001_literature_audit.tex",
        "10_Figures_Tables/tables/TAB0002_dataset_splits.md",
        "10_Figures_Tables/tables/TAB0002_dataset_splits.tex",
        "10_Figures_Tables/tables/TAB0003_experiment_matrix.md",
        "10_Figures_Tables/tables/TAB0003_experiment_matrix.tex",
        "10_Figures_Tables/tables/TAB0004_heldout_scoreboard.md",
        "10_Figures_Tables/tables/TAB0004_heldout_scoreboard.tex",
        "10_Figures_Tables/tables/TAB0005_rq2_rq3_pareto.md",
        "10_Figures_Tables/tables/TAB0005_rq2_rq3_pareto.tex",
        "10_Figures_Tables/tables/TAB0006_cross_country_shift.md",
        "10_Figures_Tables/tables/TAB0006_cross_country_shift.tex",
        # Canonical Bibliography & Audit Proofs
        "02_Literature/references.bib",
        "09_Evaluation/freeze_manifest.json",
        "09_Evaluation/g12_reconciliation_audit.json",
        "12_Documentation/step038_reproducibility_audit.json",
    ]

    files_inventory = []
    total_bytes = 0
    concat_hashes = []
    for rel in bundle_relpaths:
        p = ROOT / rel
        assert p.is_file(), f"Missing submission bundle file: {rel}"
        h = sha256_file(p)
        sz = p.stat().st_size
        total_bytes += sz
        concat_hashes.append(f"{rel}:{h}")
        files_inventory.append({"path": rel, "bytes": sz, "sha256": h})

    bundle_root_sha256 = hashlib.sha256("\n".join(concat_hashes).encode("utf-8")).hexdigest()

    bundle_manifest = {
        "schema_version": "1.0.0",
        "step": "STEP-043",
        "bundle_id": "SUBBUNDLE_DIU_CSE_THESIS_v1.0.0",
        "submission_state": "READY_AWAITING_G15_AND_PORTAL_UPLOAD",
        "allowed_states": [
            "READY_AWAITING_G15_AND_PORTAL_UPLOAD",
            "SENT_OR_UPLOADED",
            "CONFIRMED_SUBMITTED",
        ],
        "g15_thesis_gate_state": "HOLD (Technical Readiness 100% PASS; awaiting Ms Faiza Feroz authorization & UD17 defense date)",
        "institution": "Department of Computer Science and Engineering (CSE), Daffodil International University (DIU)",
        "authorized_submitters": [
            "Akhtaruzzaman Anik (ID: 232-15-252)",
            "Mahajub Al Shabah (ID: 232-15-900)",
        ],
        "supervisors": [
            "Ms Faiza Feroz (Supervisor, Lecturer, CSE, DIU)",
            "Israt Jahan (Co-supervisor, Senior Lecturer, CSE, DIU)",
        ],
        "file_count": len(files_inventory),
        "total_bytes": total_bytes,
        "bundle_merkle_sha256": bundle_root_sha256,
        "institutional_receipt": {
            "submitted_date": None,
            "destination_portal_or_office": None,
            "receipt_or_confirmation_id": None,
            "restricted_receipt_artifact_path": None,
            "note": "Populate ONLY after actual institutional submission by authorized researcher following G15 PASS.",
        },
        "files": files_inventory,
    }
    man_out = THESIS_DIR / "submission_bundle_manifest.json"
    man_out.write_text(json.dumps(bundle_manifest, indent=2), encoding="utf-8", newline="\n")

    md_lines = [
        "# DIU CSE B.Sc. Thesis Submission Record & Immutable Checksum Ledger (`STEP-043`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Step / Stage | `STEP-043` (`S14` — Submit the thesis and preserve the exact submission) |",
        "| Bundle ID | `SUBBUNDLE_DIU_CSE_THESIS_v1.0.0` ([submission_bundle_manifest.json](./submission_bundle_manifest.json)) |",
        "| Institution | Department of Computer Science & Engineering (CSE), Daffodil International University (DIU) |",
        "| Thesis Title | *A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO* |",
        "| Authorized Submitters | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |",
        "| Supervisors | Ms Faiza Feroz (Supervisor) & Israt Jahan (Co-supervisor) |",
        f"| Bundle File Count / Size | `{len(files_inventory)}` verified files (`{total_bytes:,}` bytes) |",
        f"| Bundle Merkle `SHA-256` | `{bundle_root_sha256}` |",
        "| **Current Submission State** | **`READY_AWAITING_G15_AND_PORTAL_UPLOAD`** *(Pre-submission bundle & checksums locked; actual institutional upload awaits `G15 PASS` supervisor sign-off)* |",
        "",
        "> [!IMPORTANT]",
        "> **Strict Non-Fabrication Policy (`STEP-043`):** Per `OPG_PROJECT_EXECUTION_BLUEPRINT.md` (`STEP-043`, lines 2606–2626), preparing or compiling local files must **never** be labeled `CONFIRMED_SUBMITTED`. This ledger explicitly separates **`1. READY_AWAITING_G15_AND_PORTAL_UPLOAD`**, **`2. SENT_OR_UPLOADED`**, and **`3. CONFIRMED_SUBMITTED`**.",
        "",
        "---",
        "",
        "## 1. Three-Stage Institutional Submission State Tracker",
        "",
        "| Stage | State Code | Criteria | Current Status |",
        "|---|---|---|---|",
        "| **Stage 1** | `READY_AWAITING_G15_AND_PORTAL_UPLOAD` | All `33` thesis, slide, figure, table, BibTeX & audit files compiled, verified (`STEP-041/042 PASS`), and SHA-256 hashed (`assembled_manifest.json` match verified). | **ACTIVE (`2026-11-21`)** |",
        "| **Stage 2** | `SENT_OR_UPLOADED` | Supervisor Ms Faiza Feroz approves `G15 -> PASS`, final PDF exported from `DIU_CSE_Thesis_Assembled_v1.0.0.html`, and uploaded/delivered to DIU CSE portal/office. | *Pending human action* |",
        "| **Stage 3** | `CONFIRMED_SUBMITTED` | Actual DIU portal confirmation / signed departmental receipt / supervisor email confirmation received and archived in off-Git restricted storage. | *Pending human action* |",
        "",
        "---",
        "",
        "## 2. Institutional Receipt & Confirmation Block (Fill Upon Actual DIU Submission)",
        "",
        "- **Prerequisite Gate (`GA0015` / `G15`):** Must be promoted from `HOLD` -> `PASS` in `01_Project_Management/gates.csv` after Supervisor Ms Faiza Feroz signs `11_Writing/reviews/supervisor_review_ledger.md`.",
        "- **Actual Submission Date (`YYYY-MM-DD`):** `[Pending actual DIU submission]`",
        "- **Submission Destination (e.g., DIU BLC / CSE Thesis Portal / DSpace / Dept. Office):** `[Pending actual DIU submission]`",
        "- **Submitted By (Authorized Researcher):** `[Akhtaruzzaman Anik (232-15-252) / Mahajub Al Shabah (232-15-900)]`",
        "- **Receipt / Confirmation Reference ID:** `[Pending actual receipt — NEVER fabricate]`",
        "- **Off-Git Receipt File Location (PDF/Screenshot):** `15_Archive/restricted_receipts/[pending_receipt_file]` *(kept off-Git per privacy policy)*",
        "- **Submitted PDF `SHA-256` (Exported from `DIU_CSE_Thesis_Assembled_v1.0.0.html`):** `[Record exact SHA-256 of final exported PDF at upload time]`",
        "",
        "---",
        "",
        "## 3. Immutable Submission Bundle Checksum Table (`33` Verified Files)",
        "",
        "| # | Relative Path | Size (Bytes) | `SHA-256` Digest |",
        "|---:|---|---:|---|",
    ]
    for idx, item in enumerate(files_inventory, 1):
        md_lines.append(f"| `{idx}` | `{item['path']}` | `{item['bytes']:,}` | `{item['sha256']}` |")

    md_lines += [
        "",
        "---",
        "",
        "## 4. Immutability & Post-Submission Revision Rule (`STEP-043` Procedure 4)",
        "",
        "Once Stage 3 (`CONFIRMED_SUBMITTED`) is recorded, `DIU_CSE_Thesis_Assembled_v1.0.0.{md,html}` and `submission_bundle_manifest.json` are permanently frozen. Any post-defense committee revision must be emitted as `v1.1.0` with a new bundle manifest and separate receipt record.",
    ]

    sub_out = THESIS_DIR / "submission.md"
    sub_out.write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")
    print(
        f"STEP-043 SUBMISSION BUNDLE PREPARED: files={len(files_inventory)} | "
        f"bytes={total_bytes:,} | merkle_sha256={bundle_root_sha256[:16]} | "
        f"state=READY_AWAITING_G15_AND_PORTAL_UPLOAD"
    )


if __name__ == "__main__":
    main()
