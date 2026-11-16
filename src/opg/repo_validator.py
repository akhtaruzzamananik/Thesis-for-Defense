"""Repository schema, template, folder, and gate integrity checks (STEP-003)."""

from __future__ import annotations

import csv
from pathlib import Path

COMMON_COLUMNS = ("Owner", "Version", "Status", "Created", "Updated", "EvidencePath")

REQUIRED_FOLDERS = (
    "environment",
    "environment/data",
    "src/opg",
    "tests",
    "01_Project_Management",
    "02_Literature",
    "03_Datasets",
    "04_Annotations",
    "05_Preprocessing",
    "06_Models",
    "07_Experiments",
    "08_Checkpoints",
    "09_Evaluation",
    "10_Figures_Tables",
    "11_Writing",
    "12_Documentation",
    "13_Automation",
    "14_Templates_Prompts",
    "15_Archive",
    "16_Web_Demo",
    "web",
)

APPENDIX_B_REGISTRIES = (
    "01_Project_Management/decisions.csv",
    "01_Project_Management/risk_register.csv",
    "01_Project_Management/gates.csv",
    "02_Literature/papers.csv",
    "02_Literature/screening.csv",
    "02_Literature/gaps.csv",
    "02_Literature/claims.csv",
    "03_Datasets/candidates.csv",
    "03_Datasets/datasets.csv",
    "03_Datasets/releases.csv",
    "04_Annotations/classes.csv",
    "04_Annotations/annotation_registry.csv",
    "05_Preprocessing/preprocessing_registry.csv",
    "06_Models/candidates.csv",
    "06_Models/model_registry.csv",
    "07_Experiments/experiment_registry.csv",
    "08_Checkpoints/checkpoint_registry.csv",
    "09_Evaluation/evaluation_registry.csv",
    "10_Figures_Tables/assets.csv",
    "11_Writing/writing_registry.csv",
    "15_Archive/archive_manifest.csv",
    "16_Web_Demo/deployment_registry.csv",
)


def check_folder_readmes(root: Path) -> list[str]:
    """Return errors for missing OS §2.1 folders or contract READMEs."""
    errors: list[str] = []
    for rel in REQUIRED_FOLDERS:
        readme = root / rel / "README.md"
        if not readme.is_file():
            errors.append(f"Missing folder README: {rel}/README.md")
    return errors


def check_registries(root: Path) -> list[str]:
    """Validate all 22 Appendix B CSV headers, uniqueness, and UTF-8 readability."""
    errors: list[str] = []
    for rel in APPENDIX_B_REGISTRIES:
        path = root / rel
        if not path.is_file():
            errors.append(f"Missing registry: {rel}")
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
        if not header:
            errors.append(f"Empty registry header: {rel}")
            continue
        if len(set(header)) != len(header):
            errors.append(f"Duplicate column names in {rel}: {header}")
        missing_common = [col for col in COMMON_COLUMNS if col not in header]
        if missing_common:
            errors.append(f"Missing common columns {missing_common} in {rel}")
    return errors


def check_templates(root: Path) -> list[str]:
    """Verify all blank operational templates T01-T30 exist."""
    tdir = root / "14_Templates_Prompts" / "templates"
    if not tdir.is_dir():
        return ["Missing templates directory: 14_Templates_Prompts/templates"]
    files = {p.name[:3] for p in tdir.iterdir() if p.is_file()}
    missing = [f"T{i:02d}" for i in range(1, 31) if f"T{i:02d}" not in files]
    return [f"Missing templates: {missing}"] if missing else []


def check_gates(root: Path) -> list[str]:
    """Verify G01-G17 exist in gates.csv and no PASS lacks an evidence file."""
    gates_path = root / "01_Project_Management" / "gates.csv"
    if not gates_path.is_file():
        return ["Missing 01_Project_Management/gates.csv"]
    with gates_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    errors: list[str] = []
    seen_gates = {row.get("GateID", "") for row in rows}
    expected = {f"G{i:02d}" for i in range(1, 18)}
    missing = sorted(expected - seen_gates)
    if missing:
        errors.append(f"Missing GateIDs in gates.csv: {missing}")
    for row in rows:
        if row.get("Outcome", "").strip().upper() == "PASS":
            ev = row.get("EvidencePath", "").strip()
            if not ev or not (root / ev).is_file():
                errors.append(f"Gate {row.get('GateID')} marked PASS without valid EvidencePath: {ev!r}")
    return errors


def check_environment_evidence(root: Path) -> list[str]:
    """Verify STEP-002 data-tool lock and smoke-verification docs exist."""
    required = (
        "environment/data/requirements.lock.txt",
        "environment/data/verification.md",
        ".gitignore",
    )
    return [f"Missing required artifact: {rel}" for rel in required if not (root / rel).is_file()]


def validate_repository(root: Path) -> list[str]:
    """Run all repository structural and schema checks, returning a list of errors."""
    return [
        *check_folder_readmes(root),
        *check_registries(root),
        *check_templates(root),
        *check_gates(root),
        *check_environment_evidence(root),
    ]
