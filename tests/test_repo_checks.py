"""Automated tests for repository structure, registries, templates, and gates."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from opg.repo_validator import check_registries, validate_repository  # noqa: E402


def test_repository_structure_and_schemas() -> None:
    errors = validate_repository(ROOT)
    assert errors == [], f"Repository validation errors: {errors}"


def test_registry_row_width_catches_unquoted_commas(tmp_path: Path) -> None:
    """Verify check_registries flags rows whose column count drifts from the header."""
    for rel in ("01_Project_Management/decisions.csv",):
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "DecisionID,Owner,Version,Status,Created,Updated,EvidencePath\n"
            "DEC1,Owner,1,OK,unquoted,comma,2026-11-17,2026-11-17,path\n",
            encoding="utf-8",
        )
    errors = [e for e in check_registries(tmp_path) if "decisions.csv" in e]
    assert len(errors) == 1
    assert "expected 7, found 9" in errors[0]
