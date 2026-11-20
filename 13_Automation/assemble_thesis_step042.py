"""STEP-042 Deterministic DIU CSE Thesis Manuscript Assembler (MD + Print-Ready HTML).

Compiles 11_Writing/thesis/00_front_matter_and_abstract.md .. 07_appendices.md,
auto-generates Table of Contents, List of Figures (FIG0001-FIG0006), List of Tables
(TAB0001-TAB0006), embeds all 6 vector SVG figures inline in a self-contained A4
print-to-PDF HTML manuscript, formats all cited BibTeX records from
02_Literature/references.bib in IEEE numeric order, and writes SHA-256 digests to
11_Writing/thesis/assembled_manifest.json.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
THESIS_DIR = ROOT / "11_Writing" / "thesis"
BIB_PATH = ROOT / "02_Literature" / "references.bib"
ASSETS_CSV = ROOT / "10_Figures_Tables" / "assets.csv"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bib(bib_text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    blocks = re.split(r"(?m)^@", bib_text)
    for blk in blocks[1:]:
        m = re.match(r"(\w+)\{([^,]+),(.*)\}\s*$", blk, flags=re.S)
        if not m:
            continue
        etype, key, body = m.group(1), m.group(2).strip(), m.group(3)
        fields: dict[str, str] = {"_type": etype, "_key": key}
        for fm in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body):
            k = fm.group(1).lower().strip()
            v = re.sub(r"\s+", " ", fm.group(2)).strip()
            v = v.replace("\\&amp;", "&").replace("\\&", "&")
            fields[k] = v
        entries[key] = fields
    return entries


def format_ieee_ref(num: int, entry: dict[str, str]) -> str:
    authors_raw = entry.get("author", "Unknown Author")
    authors = [a.strip() for a in authors_raw.split(" and ")]
    if len(authors) > 6:
        auth_str = ", ".join(authors[:6]) + ", et al."
    else:
        auth_str = ", ".join(authors)
    title = entry.get("title", "Untitled")
    venue = entry.get("journal") or entry.get("howpublished") or entry.get("booktitle") or "Preprint"
    year = entry.get("year", "n.d.")
    doi = entry.get("doi", "")
    url = entry.get("url", "")
    key = entry.get("_key", "")
    tail = f" doi: `{doi}`." if doi else (f" {url}." if url else "")
    return f"[{num}] {auth_str}, \"{title},\" *{venue}*, {year}.{tail} *(BibTeX: `{key}`)*"


def load_assets() -> list[dict[str, str]]:
    with ASSETS_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def md_inline_to_html(text: str) -> str:
    s = html.escape(text)
    # Inline code
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    # Bold + italic
    s = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def md_to_html_body(md_text: str, svg_map: dict[str, str]) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped == "---":
            out.append("<hr/>")
            i += 1
            continue

        # Embedded figure marker
        fm = re.match(r"^<!--\s*EMBED_FIG:(FIG\d{4})\|(.*?)\s*-->$", stripped)
        if fm:
            fid, cap = fm.group(1), fm.group(2)
            svg_raw = svg_map.get(fid, "")
            out.append(
                f'<figure class="thesis-fig"><div class="svg-wrap">{svg_raw}</div>'
                f'<figcaption><strong>{fid}:</strong> {html.escape(cap)}</figcaption></figure>'
            )
            i += 1
            continue

        # Headings
        hm = re.match(r"^(#{1,4})\s+(.*)$", line)
        if hm:
            lvl = len(hm.group(1))
            cls = ' class="chapter-break"' if lvl == 1 and ("Chapter " in hm.group(2) or "Appendices" in hm.group(2) or "References" in hm.group(2)) else ""
            out.append(f"<h{lvl}{cls}>{md_inline_to_html(hm.group(2))}</h{lvl}>")
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            q_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + "<br/>".join(md_inline_to_html(q) for q in q_lines) + "</blockquote>")
            continue

        # Markdown Table
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            hdr = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            body_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body_rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thtml = ["<table><thead><tr>"]
            thtml += [f"<th>{md_inline_to_html(c)}</th>" for c in hdr]
            thtml.append("</tr></thead><tbody>")
            for r in body_rows:
                thtml.append("<tr>" + "".join(f"<td>{md_inline_to_html(c)}</td>" for c in r) + "</tr>")
            thtml.append("</tbody></table>")
            out.append("".join(thtml))
            continue

        # Bullet list
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{md_inline_to_html(it)}</li>" for it in items) + "</ul>")
            continue

        # Numbered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip())
                i += 1
            out.append("<ol>" + "".join(f"<li>{md_inline_to_html(it)}</li>" for it in items) + "</ol>")
            continue

        # Paragraph
        p_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt == "---"
                or nxt.startswith("#")
                or nxt.startswith(">")
                or nxt.startswith("|")
                or nxt.startswith("```")
                or nxt.startswith("<!-- EMBED_FIG:")
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
            ):
                break
            p_lines.append(nxt)
            i += 1
        out.append("<p>" + md_inline_to_html(" ".join(p_lines)) + "</p>")

    return "\n".join(out)


def main() -> None:
    chapter_files = [
        "00_front_matter_and_abstract.md",
        "01_chapter1_introduction.md",
        "02_chapter2_literature_review.md",
        "03_chapter3_methodology.md",
        "04_chapter4_results.md",
        "05_chapter5_discussion_and_prototype.md",
        "06_chapter6_conclusion.md",
        "07_appendices.md",
    ]
    chapters = [(fn, (THESIS_DIR / fn).read_text(encoding="utf-8").strip()) for fn in chapter_files]
    assets = load_assets()
    figs = [a for a in assets if a["Kind"] == "Figure"]
    tabs = [a for a in assets if a["Kind"] == "Table"]
    fig_by_id = {a["AssetID"]: a for a in figs}
    svg_map = {a["AssetID"]: (ROOT / a["OutputPath"]).read_text(encoding="utf-8") for a in figs}

    # Build ordered IEEE citation map from first occurrence across chapters 00..07
    bib_entries = parse_bib(BIB_PATH.read_text(encoding="utf-8"))
    cite_order: list[str] = []
    cite_num: dict[str, int] = {}
    for _, body in chapters:
        for k in re.findall(r"[A-Za-z0-9]+_P\d{4}", body):
            if k not in cite_num:
                assert k in bib_entries, f"Missing BibTeX entry: {k}"
                cite_order.append(k)
                cite_num[k] = len(cite_order)

    def replace_cite_group(match: re.Match[str]) -> str:
        inner = match.group(1)
        if not re.search(r"[A-Za-z0-9]+_P\d{4}", inner):
            return match.group(0)
        parts = [p.strip() for p in inner.split(";")]
        nums = []
        others = []
        for p in parts:
            if p in cite_num:
                nums.append(cite_num[p])
            else:
                others.append(p)
        nums = sorted(set(nums))
        formatted = ", ".join(f"[{n}]" for n in nums)
        if others:
            return f"({'; '.join(others)}; {formatted})"
        return formatted

    # Build Table of Contents, List of Figures, List of Tables
    toc_lines = [
        "## Table of Contents",
        "",
        "- Front Matter, Declarations, Abstract & Abbreviations",
        "- Chapter 1: Introduction",
        "- Chapter 2: Literature Review and Methodological Gap Synthesis",
        "- Chapter 3: Methodology and Experimental Design",
        "- Chapter 4: Experimental Results",
        "- Chapter 5: Error Analysis, Discussion, Prototype Packaging & Limitations",
        "- Chapter 6: Conclusion and Future Work",
        f"- References ({len(cite_order)} Verified Primary Sources)",
        "- Appendices A–D (Ontology, SHA-256 Ledger, Per-Class Tables & Gate Audit Trail)",
        "",
        "## List of Figures",
        "",
        "| Figure ID | Caption | Source File |",
        "|---|---|---|",
    ]
    for f in figs:
        toc_lines.append(f"| `{f['AssetID']}` | {f['Caption']} | `{f['OutputPath']}` |")

    toc_lines += [
        "",
        "## List of Tables",
        "",
        "| Table ID | Caption | Source File |",
        "|---|---|---|",
    ]
    for t in tabs:
        toc_lines.append(f"| `{t['AssetID']}` | {t['Caption']} | `{t['OutputPath']}` |")

    # Figure insertion map (chapter filename -> list of FIG IDs to embed at end of relevant chapter)
    chapter_fig_embeds = {
        "03_chapter3_methodology.md": ["FIG0001"],
        "04_chapter4_results.md": ["FIG0002", "FIG0003", "FIG0004", "FIG0005"],
        "05_chapter5_discussion_and_prototype.md": ["FIG0006"],
    }

    assembled_md_parts: list[str] = []
    assembled_html_md_parts: list[str] = []

    for idx, (fn, body) in enumerate(chapters):
        numbered_body = re.sub(r"\[([^\[\]]+)\]", replace_cite_group, body)
        if idx == 0:
            assembled_md_parts.append(numbered_body + "\n\n---\n\n" + "\n".join(toc_lines))
            assembled_html_md_parts.append(numbered_body + "\n\n---\n\n" + "\n".join(toc_lines))
        elif fn == "07_appendices.md":
            # Insert References before Appendices
            ref_lines = [
                "# References",
                "",
                f"> Canonical Bibliography: `02_Literature/references.bib` (`{len(cite_order)}` cited primary peer-reviewed sources verified against Crossref DOI metadata and full-text PDFs; zero unverified seed references).",
                "",
            ]
            for num, k in enumerate(cite_order, 1):
                ref_lines.append(format_ieee_ref(num, bib_entries[k]))
                ref_lines.append("")
            ref_block = "\n".join(ref_lines).strip()
            assembled_md_parts.append(ref_block)
            assembled_html_md_parts.append(ref_block)
            assembled_md_parts.append(numbered_body)
            assembled_html_md_parts.append(numbered_body)
        else:
            md_chunk = numbered_body
            html_chunk = numbered_body
            if fn in chapter_fig_embeds:
                md_figs = ["", "### Chapter Figures (Vector SVG Assets)", ""]
                html_figs = [""]
                for fid in chapter_fig_embeds[fn]:
                    a = fig_by_id[fid]
                    rel_svg = "../../" + a["OutputPath"]
                    md_figs.append(f"![{fid}: {a['Caption']}]({rel_svg})")
                    md_figs.append(f"*{fid}: {a['Caption']}*")
                    md_figs.append("")
                    html_figs.append(f"<!-- EMBED_FIG:{fid}|{a['Caption']} -->")
                md_chunk += "\n" + "\n".join(md_figs)
                html_chunk += "\n" + "\n".join(html_figs)
            assembled_md_parts.append(md_chunk)
            assembled_html_md_parts.append(html_chunk)

    full_md = "\n\n---\n\n".join(assembled_md_parts) + "\n"
    html_src = "\n\n---\n\n".join(assembled_html_md_parts) + "\n"

    md_out = THESIS_DIR / "DIU_CSE_Thesis_Assembled_v1.0.0.md"
    md_out.write_text(full_md, encoding="utf-8", newline="\n")

    html_body = md_to_html_body(html_src, svg_map)
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>DIU CSE B.Sc. Thesis — Automated Object Detection in 2D OPG Images Using YOLO (v1.0.0)</title>
<style>
  @page {{ size: A4; margin: 22mm 20mm 22mm 24mm; }}
  body {{ font-family: Georgia, "Times New Roman", serif; color: #0F172A; line-height: 1.55; max-width: 960px; margin: 0 auto; padding: 24px 32px; background: #FFFFFF; font-size: 11pt; }}
  h1, h2, h3, h4 {{ font-family: "Segoe UI", Helvetica, Arial, sans-serif; color: #1E3A8A; }}
  h1 {{ font-size: 20pt; border-bottom: 2px solid #1E3A8A; padding-bottom: 6px; margin-top: 28px; }}
  h2 {{ font-size: 14pt; margin-top: 22px; color: #0F172A; }}
  h3 {{ font-size: 12pt; margin-top: 16px; color: #334155; }}
  .chapter-break {{ page-break-before: always; }}
  p {{ text-align: justify; margin: 8px 0; }}
  table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-family: "Segoe UI", Arial, sans-serif; font-size: 8.6pt; page-break-inside: auto; }}
  th, td {{ border: 1px solid #CBD5E1; padding: 5px 7px; text-align: left; vertical-align: top; }}
  th {{ background: #F1F5F9; font-weight: 700; color: #0F172A; }}
  tr:nth-child(even) {{ background: #F8FAFC; }}
  code {{ font-family: Consolas, "Courier New", monospace; font-size: 9pt; background: #F1F5F9; padding: 1px 4px; border-radius: 3px; }}
  pre {{ background: #0F172A; color: #F8FAFC; padding: 12px 14px; border-radius: 6px; overflow-x: auto; font-size: 8.8pt; }}
  pre code {{ background: none; color: inherit; padding: 0; }}
  blockquote {{ border-left: 4px solid #2563EB; background: #EFF6FF; padding: 10px 14px; margin: 12px 0; font-family: "Segoe UI", Arial, sans-serif; font-size: 9.8pt; }}
  figure.thesis-fig {{ margin: 18px 0; text-align: center; page-break-inside: avoid; }}
  figure.thesis-fig .svg-wrap svg {{ width: 100%; height: auto; max-width: 100%; }}
  figcaption {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 9.5pt; color: #334155; margin-top: 6px; }}
  hr {{ border: none; border-top: 1px solid #E2E8F0; margin: 18px 0; }}
  @media print {{ body {{ padding: 0; max-width: none; }} }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    html_out = THESIS_DIR / "DIU_CSE_Thesis_Assembled_v1.0.0.html"
    html_out.write_text(html_doc, encoding="utf-8", newline="\n")

    word_count = len(re.findall(r"\b\w+\b", full_md))
    manifest = {
        "schema_version": "1.0.0",
        "step": "STEP-042",
        "version": "v1.0.0",
        "source_chapters": chapter_files,
        "cited_references_formatted": len(cite_order),
        "figures_embedded_inline": len(figs),
        "tables_indexed": len(tabs),
        "assembled_word_count": word_count,
        "outputs": {
            "markdown": {
                "path": "11_Writing/thesis/DIU_CSE_Thesis_Assembled_v1.0.0.md",
                "bytes": md_out.stat().st_size,
                "sha256": sha256_file(md_out),
            },
            "html_print_ready": {
                "path": "11_Writing/thesis/DIU_CSE_Thesis_Assembled_v1.0.0.html",
                "bytes": html_out.stat().st_size,
                "sha256": sha256_file(html_out),
            },
        },
        "submission_gate_status": "HOLD_PENDING_SUPERVISOR_AUTHORIZATION_G15",
    }
    man_out = THESIS_DIR / "assembled_manifest.json"
    man_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print(
        f"STEP-042 THESIS ASSEMBLED: words={word_count:,} | refs={len(cite_order)} | "
        f"inline_svgs={len(figs)} | md_sha256={manifest['outputs']['markdown']['sha256'][:12]} | "
        f"html_sha256={manifest['outputs']['html_print_ready']['sha256'][:12]}"
    )


if __name__ == "__main__":
    main()
