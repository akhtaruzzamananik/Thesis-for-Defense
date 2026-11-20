# Optional Paper Pathway & Submission Disposition Record (`STEP-044` / `UD17`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-044` (`S14` — Prepare the paper pathway and record submission or disposition) |
| Manuscript Artifact | `11_Writing/paper/manuscript_draft.md` (`WRIT0009–WRIT0013`, `v1.0.0`) & `11_Writing/paper/manuscript_draft_v1.0.0.html` |
| Shared Evidence Base | `02_Literature/references.bib`, `02_Literature/claims.csv` (`CLAIM0001–0017`), `09_Evaluation/final_evaluation_report.md` (`EVAL0001–0014`, `XSHIFT01–06`), `10_Figures_Tables/assets.csv` (`FIG0001–0006`, `TAB0001–0006`) |
| Co-Authors | Akhtaruzzaman Anik (`232-15-252`) & Mahajub Al Shabah (`232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor, CSE, DIU) & Israt Jahan (Co-supervisor, CSE, DIU) |
| **Current Disposition (`UD17` / `DEC0017`)** | **`APPROVED_DEFERRAL_OPTIONAL_PACKAGE_READY` *(Complete verified paper package archived; external journal/conference submission deferred pending post-defense Supervisor venue decision — NOT claimed as submitted or accepted)*** |
| Separate Gate Record | `GA0018` (`G15 / paper` in `01_Project_Management/gates.csv` = **`DEFERRED`**, per Blueprint `STEP-044`: *"an approved deferral/not-required disposition is not labeled PASS"*) |

---

## 1. Purpose & Alignment with `OPG_PROJECT_EXECUTION_BLUEPRINT.md` (`STEP-044`)

Per `OPG_PROJECT_EXECUTION_BLUEPRINT.md` (`STEP-044`, lines 2636–2690):
1. **No Invented Venue or Mandatory Acceptance:** DIU CSE B.Sc. thesis completion (`G16`) does not require external journal acceptance, and an unsubmitted draft must never be misrepresented as submitted.
2. **Complete, Evidence-Verified Paper Package Ready for Future Submission:** We adapted the exact verified evidence base (`G01–G14 PASS`) into a self-contained, `~8–10`-page IMRaD research paper (`11_Writing/paper/manuscript_draft.md` and print-ready `manuscript_draft_v1.0.0.html` with all `6` inline vector SVGs and IEEE references) audited by `13_Automation/compile_and_audit_paper_step044.py` (`11_Writing/reviews/step044_paper_audit.json = PASS`).
3. **Explicit Separate `G15 / paper` Gate Disposition (`GA0018`):** In strict compliance with Blueprint line 2680 (*"G15 / paper PASS is recorded before any paper submission; an approved deferral/not-required disposition is not labeled PASS"*), we record `GA0018` (`G15 / paper`) in `01_Project_Management/gates.csv` with `Outcome = DEFERRED` (`01_Project_Management/reviews/G15_paper_readiness_2026-11-21.md`).

---

## 2. Candidate Target Venues (If Co-Authors & Supervisor Elect Post-Defense Submission)

| Candidate Venue Tier | Example Journals / Conferences | Alignment with Our Evidence | Required Action Before External Submission |
|---|---|---|---|
| Open-Access Medical Imaging / Dental AI Journals | *Diagnostics* (MDPI), *BMC Oral Health*, *Journal of Imaging Informatics in Medicine*, *Dentomaxillofacial Radiology* | Direct fit for 6-cohort leak-free benchmark, `CLAHE` vs `1280px` ablation, `5`-country shift, and `T19` error audit | Confirm OA APC funding/waiver & obtain all 4 authors' signed cover letter + `G15 / paper PASS` |
| IEEE / Springer Computer Vision & Healthcare Conferences | *IEEE Access*, *ICWR / ICCIT / IEEE EMBC / MICCAI Dental Workshops* | Direct fit for `TransformLedger`, `ONNXRuntime` CPU latency Pareto, and `R1–R3` reproducible pipeline | Format `manuscript_draft.md` + `TAB0001–0006.tex` into the chosen venue's official LaTeX class |

---

## 3. Re-Activation Protocol for Future External Submission

If the authors and Supervisor Ms Faiza Feroz decide to submit `manuscript_draft.md` to an external venue after the DIU thesis defense:
1. Select the concrete target venue and record its formatting/word-limit checklist in `11_Writing/reviews/paper_review_ledger.md`.
2. Obtain written sign-off from all authors (`A. Anik`, `M. Al Shabah`, `I. Jahan`, `Ms F. Feroz`) confirming authorship order, conflict-of-interest, data availability (`DS0001–DS0006` public citations, `DS0002 CC-BY-NC-SA` isolation), and non-clinical scope statements.
3. Promote `GA0018` (`G15 / paper`) from `DEFERRED` -> `PASS` **prior** to uploading to the journal/conference portal, and archive the actual portal submission receipt.
