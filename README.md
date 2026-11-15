# AI Digital Forensics Thesis

## Overview

This repository contains the research plan, documentation, experiments, and software artifacts for an OPG thesis on **image-based detection of AI-generated human faces**.

The project investigates how an evidence-driven forensic system can identify synthetic or manipulated face images and communicate its conclusion with calibrated confidence and an explainable forensic report.

## Research Direction

The thesis is designed around an **AI Forensic Analyst** rather than a standalone image classifier. The analyst combines independent evidence sources, validates their quality, fuses the evidence, and produces a reproducible conclusion.

Version 1 focuses on:

- Detecting AI-generated human faces in images
- Building reproducible dataset and preprocessing pipelines
- Training and evaluating FastAI/PyTorch detection models
- Measuring cross-dataset and unseen-generator generalization
- Producing explainable, evidence-backed forensic reports
- Exposing the system through a Django REST API and a React frontend

The architecture is designed to support future audio, video, text, and multimodal forensic specialists without redesigning the core system.

## Primary Contribution

The primary contribution is the **AI Forensic Analyst**: a modular forensic workflow that treats a detector as one replaceable evidence-producing specialist, not as the final decision-maker.

The system is intended to provide:

1. Evidence collection from independent forensic modules
2. Evidence validation and quality checks
3. Evidence fusion and calibrated confidence
4. Human-readable explanations
5. Reproducible forensic case reports

## Technology Stack

| Area | Technology |
|---|---|
| Deep learning | FastAI + PyTorch |
| Backend | Django + Django REST Framework |
| Frontend | React + Vite + Tailwind CSS |
| GPU experimentation | Kaggle |
| Version control | GitHub |

## Planned Repository Structure

```text
01_Project_Management/   # Decisions, milestones, risks, reviews
02_Literature/           # Papers, summaries, claims, and research gaps
03_Datasets/             # Dataset registry, metadata, and validation
04_Preprocessing/        # Reproducible preprocessing pipelines
05_Models/               # Model definitions and training configuration
06_Experiments/          # Experiment specifications and metadata
08_Evaluation/           # Metrics, reports, and comparisons
09_Figures/              # Traceable research figures
10_Tables/               # Thesis and evaluation tables
11_AI_Forensic_System/   # Evidence collectors and analyst modules
12_Web/                  # Frontend application
13_Backend/              # Backend and REST API
15_Writing/              # Thesis and publication drafts
16_Documentation/        # User and developer documentation
20_Archive/              # Immutable project archives
```

Large datasets, trained checkpoints, and other heavy artifacts should be stored in the designated artifact tier rather than committed directly to Git.

## Research Workflow

The project follows a reproducible sequence:

```text
Literature → Research Gap → Dataset → Preprocessing → Baselines
    → Experiments → Evaluation → AI Forensic Analyst
    → API and Web App → Thesis → Publication
```

Every experiment should record its data version, preprocessing version, model configuration, random seed, environment, metrics, and supporting artifacts.

## Research Principles

- Reproducibility comes before convenience.
- Every important decision is documented and version controlled.
- Negative and failed experiments are retained rather than hidden.
- No scientific claim is made without supporting evidence.
- Test data must remain isolated from training and model selection.
- Human approval is required for irreversible scientific decisions.
- The detector provides evidence; the forensic analyst makes the structured assessment.

## Project Status

The repository is at the planning and initialization stage. The research operating system and execution blueprint define the intended workflow from literature review through thesis defense and publication.

## Core Documents

- `MASTER_RESEARCH_OPERATING_SYSTEM.md` — governance, architecture, quality gates, and research policies
- `PROJECT_EXECUTION_BLUEPRINT.md` — sequential execution roadmap from research foundation to archival

## Reproducibility

The final system will document:

- Dataset sources, licenses, versions, and validation results
- Preprocessing and data-split procedures
- Environment and dependency versions
- Experiment configurations and random seeds
- Evaluation protocols and generated reports
- Model checkpoints and artifact locations

## Academic Integrity

This project follows research-integrity requirements: no fabricated results, citations, figures, or claims; no hidden failed experiments; no leakage between training and evaluation data; and no unsupported conclusions.

## License

A project license will be added after the applicable dataset, software, and institutional requirements have been reviewed.
