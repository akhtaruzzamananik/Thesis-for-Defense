# Contributing & Collaboration Workflow

This repository follows the governance rules in [OPG_RESEARCH_OPERATING_SYSTEM.md](./OPG_RESEARCH_OPERATING_SYSTEM.md) (`OS §10–§12`) and the team division in [01_Project_Management/team_roles.md](./01_Project_Management/team_roles.md).

## 1. Commit Message Convention

Commit one coherent task unit at a time using clear prefixes:

- `docs:` — Planning documents, README, registries, session notes, reviews
- `research:` — Literature searches, paper summaries, gap/claim records
- `data:` — Dataset manifests, split scripts, preprocessing configs (never raw images)
- `annotation:` — Class ontology, protocols, QA reports (never restricted native labels)
- `experiment:` — Registered experiment configs, run manifests, observations
- `evaluation:` — Evaluation protocols, frozen metric/timing reports, error reviews
- `web:` — Thin defense web demo (`web/`), deployment records, parity/smoke checks
- `writing:` — Thesis/paper drafts, figure/table specs, review responses
- `fix:` — Bug fixes or registry corrections (preserving failed/superseded history)

## 2. Pre-Push Safety Checklist (Mandatory — Public Repo)

Before every `git push`:

1. Run `git status` and `git diff --cached` to inspect staged files.
2. Confirm **zero** OPG images, patient IDs/linkage keys, `.env`/tokens, `.venv/`, or binary model weights (`.pt`, `.onnx`, etc.) are staged.
3. Confirm failed experiments and negative results are preserved rather than deleted.
4. Keep registry CSV schemas aligned with `OS Appendix B` (UTF-8, consistent headers, valid linked IDs).

## 3. Teammate Cross-Review

- Pull `origin/main` before starting work (`git pull --rebase` or merge cleanly).
- Keep primary ownership aligned with `team_roles.md` (Anik: governance/data/preprocessing/web; Mahajub: literature/annotation QA/YOLO modeling/evaluation), and have the other teammate cross-review before closing quality gates (`G01–G17`).
