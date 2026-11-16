"""Thin CLI entry point for repository schema and structure checks (STEP-003)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from opg.repo_validator import validate_repository  # noqa: E402


def main() -> int:
    errors = validate_repository(ROOT)
    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1
    print("OK: 21 folder READMEs, 22 Appendix B CSVs, T01-T30 templates, G01-G17 gates, and STEP-002 environment checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
