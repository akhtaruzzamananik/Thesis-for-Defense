"""Automated tests for repository structure, registries, templates, and gates."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from opg.repo_validator import validate_repository  # noqa: E402


def test_repository_structure_and_schemas() -> None:
    errors = validate_repository(ROOT)
    assert errors == [], f"Repository validation errors: {errors}"
