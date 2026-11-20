"""STEP-044 Concise Paper Compiler (Print-Ready HTML with Inline SVGs) & Quantitative Auditor.

Verifies 11_Writing/paper/manuscript_draft.md against:
  - 02_Literature/references.bib (100% BibTeX key validity, 0 legacy [1]-[13])
  - 02_Literature/claims.csv (all 17/17 CLAIM0001-CLAIM0017 covered)
  - 10_Figures_Tables/assets.csv (all 12/12 FIG0001-0006 & TAB0001-0006 referenced)
  - 09_Evaluation/EVAL0001..0014/metrics_summary.json, xshift_metrics.csv, timing JSONs
  - Non-clinical & 6-country dataset / 5-country XSHIFT consistency rules
Compiles 11_Writing/paper/manuscript_draft_v1.0.0.html with inline vector SVGs and IEEE refs,
and saves 11_Writing/reviews/step044_paper_audit.json.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "13_Automation"))

from assemble_thesis_step042 import (  # noqa: E402
    format_ieee_ref,
    load_assets,
    md_to_html_body,
    parse_bib,
)

PAPER_MD = ROOT / "11_Writing" / "paper" / "manuscript_draft.md"
PAPER_HTML = ROOT / "11_Writing" / "paper" / "manuscript_draft_v1.0.0.html"
AUDIT_JSON = ROOT / "11_Writing" / "reviews" / "step044_paper_audit.json"
BIB_PATH = ROOT / "02_Literature" / "references.bib"


def load_json(rel: str) -> Any:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    body = PAPER_MD.read_text(encoding="utf-8")
    bib_text = BIB_PATH.read_text(encoding="utf-8")
    bib_entries = parse_bib(bib_text)

    # 1. Citation Audit
    cited_order: list[str] = []
    cite_num: dict[str, int] = {}
    missing_citations: list[str] = []
    for k in re.findall(r"[A-Za-z0-9]+_P\d{4}", body):
        if k not in bib_entries:
            missing_citations.append(k)
        elif k not in cite_num:
            cited_order.append(k)
            cite_num[k] = len(cited_order)

    legacy_hits = [
        m.group(0)
        for m in re.finditer(r"(?<!`)\[([1-9]|1[0-3])\](?!\()", body)
    ]

    # 2. Claims Audit (CLAIM0001..CLAIM0017)
    referenced_claims: set[str] = set()
    for m in re.finditer(r"CLAIM(\d{4})(?:[–-](?:CLAIM)?(\d{4}))?", body):
        s = int(m.group(1))
        e = int(m.group(2)) if m.group(2) else s
        for cid in range(s, e + 1):
            referenced_claims.add(f"CLAIM{cid:04d}")
    expected_claims = {f"CLAIM{i:04d}" for i in range(1, 18)}
    uncited_claims = sorted(expected_claims - referenced_claims)

    # 3. Assets Audit (FIG0001..0006, TAB0001..0006)
    assets = load_assets()
    unreferenced_assets = [a["AssetID"] for a in assets if a["AssetID"] not in body]

    # 4. Quantitative Spot Checks (20 checks)
    metric_checks: list[dict[str, Any]] = []
    for i in range(1, 15):
        eid = f"EVAL{i:04d}"
        ev = load_json(f"09_Evaluation/{eid}/metrics_summary.json")
        m50 = f"{ev['metrics_at_frozen_conf_op']['mAP@0.50']:.4f}"
        m95 = f"{ev['metrics_at_frozen_conf_op']['mAP@0.50:0.95']:.4f}"
        metric_checks.append({"check": f"{eid} mAP50={m50} & mAP50-95={m95}", "pass": (m50 in body and m95 in body)})

    ev10 = load_json("09_Evaluation/EVAL0010/metrics_summary.json")
    tc5 = f"{ev10['trackC_5class_pathology_dual']['metrics']['mAP@0.50']:.4f}"
    metric_checks.append({"check": f"TrackC 5-cls mAP50={tc5}", "pass": tc5 in body})

    for val in ("0.8181", "0.7109", "0.6967", "0.2355", "0.1627", "201.6", "847.9", "878.1", "DS0001_IMG_000722", "6,718"):
        metric_checks.append({"check": f"Key value '{val}' present in paper", "pass": val in body})

    # 5. Anti-Overclaim Wording Audit
    forbidden = [
        r"\bclinically validated\b",
        r"\bapproved medical device\b",
        r"\breplaces (?:the )?(?:dentist|clinician)\b",
        r"\bfirst multi-class OPG (?:object )?detector\b",
    ]
    violations = []
    for pat in forbidden:
        for m in re.finditer(pat, body, flags=re.I):
            ln = body[: m.start()].count("\n") + 1
            ltxt = body.splitlines()[ln - 1]
            if any(neg in ltxt.lower() for neg in ("never ", "not ", "no ", "nor ", "cannot ")):
                continue
            violations.append({"line": ln, "match": m.group(0)})

    # 6. Compile Print-Ready HTML Paper with Inline Vector SVGs + IEEE References
    figs = [a for a in assets if a["Kind"] == "Figure"]
    svg_map = {a["AssetID"]: (ROOT / a["OutputPath"]).read_text(encoding="utf-8") for a in figs}

    def replace_cite_group(match: re.Match[str]) -> str:
        inner = match.group(1)
        if not re.search(r"[A-Za-z0-9]+_P\d{4}", inner):
            return match.group(0)
        parts = [p.strip() for p in inner.split(";")]
        nums = sorted({cite_num[p] for p in parts if p in cite_num})
        others = [p for p in parts if p not in cite_num]
        fmt = ", ".join(f"[{n}]" for n in nums)
        return f"({'; '.join(others)}; {fmt})" if others else fmt

    numbered_md = re.sub(r"\[([^\[\]]+)\]", replace_cite_group, body)
    # Append inline figure markers and IEEE References
    fig_markers = ["", "## Figures", ""]
    for f in figs:
        fig_markers.append(f"<!-- EMBED_FIG:{f['AssetID']}|{f['Caption']} -->")
    ref_lines = ["", "## References", ""]
    for num, k in enumerate(cited_order, 1):
        ref_lines.append(format_ieee_ref(num, bib_entries[k]))
        ref_lines.append("")

    html_body = md_to_html_body(numbered_md + "\n" + "\n".join(fig_markers) + "\n" + "\n".join(ref_lines), svg_map)
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Research Paper Draft v1.0.0 — Leakage-Controlled Multi-Cohort 2D OPG YOLO Detection</title>
<style>
  @page {{ size: A4; margin: 18mm 18mm 18mm 18mm; }}
  body {{ font-family: Georgia, "Times New Roman", serif; color: #0F172A; line-height: 1.5; max-width: 920px; margin: 0 auto; padding: 20px 28px; font-size: 10.5pt; }}
  h1, h2, h3 {{ font-family: "Segoe UI", Helvetica, Arial, sans-serif; color: #1E3A8A; }}
  h1 {{ font-size: 16pt; border-bottom: 2px solid #1E3A8A; padding-bottom: 6px; }}
  h2 {{ font-size: 12.5pt; margin-top: 18px; color: #0F172A; }}
  h3 {{ font-size: 11pt; margin-top: 14px; color: #334155; }}
  p {{ text-align: justify; margin: 7px 0; }}
  code {{ font-family: Consolas, monospace; font-size: 8.8pt; background: #F1F5F9; padding: 1px 4px; border-radius: 3px; }}
  figure.thesis-fig {{ margin: 16px 0; text-align: center; page-break-inside: avoid; }}
  figure.thesis-fig .svg-wrap svg {{ width: 100%; height: auto; }}
  figcaption {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 9pt; color: #334155; margin-top: 5px; }}
  hr {{ border: none; border-top: 1px solid #E2E8F0; margin: 14px 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    PAPER_HTML.write_text(html_doc, encoding="utf-8", newline="\n")

    all_ok = (
        not missing_citations
        and not legacy_hits
        and not uncited_claims
        and not unreferenced_assets
        and all(c["pass"] for c in metric_checks)
        and not violations
    )
    word_count = len(re.findall(r"\b\w+\b", body))
    report = {
        "step": "STEP-044",
        "overall_status": "PASS" if all_ok else "FAIL",
        "disposition": "APPROVED_DEFERRAL_OPTIONAL_PACKAGE_READY (GA0018 = DEFERRED)",
        "word_count": word_count,
        "cited_references": len(cited_order),
        "missing_citations": missing_citations,
        "legacy_bracket_hits": legacy_hits,
        "claims_covered": f"{len(referenced_claims)}/17",
        "uncited_claims": uncited_claims,
        "assets_referenced": f"{len(assets) - len(unreferenced_assets)}/{len(assets)}",
        "unreferenced_assets": unreferenced_assets,
        "metric_checks_passed": f"{sum(1 for c in metric_checks if c['pass'])}/{len(metric_checks)}",
        "failed_metric_checks": [c for c in metric_checks if not c["pass"]],
        "wording_violations": violations,
        "outputs": {
            "markdown_sha256": sha256_file(PAPER_MD),
            "html_sha256": sha256_file(PAPER_HTML),
        },
    }
    AUDIT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(
        f"STEP-044 PAPER AUDIT STATUS={report['overall_status']} | words={word_count:,} | "
        f"refs={len(cited_order)} | claims={report['claims_covered']} | "
        f"assets={report['assets_referenced']} | metrics={report['metric_checks_passed']}"
    )
    assert all_ok, f"STEP-044 paper audit failed: {report}"


if __name__ == "__main__":
    main()
