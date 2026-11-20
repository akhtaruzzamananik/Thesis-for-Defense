# Thesis & Optional Paper Submission Requirements (`STEP-039` / `UD17`)

| Field | Value |
|---|---|
| Institution | Department of Computer Science & Engineering (CSE), Daffodil International University (DIU) |
| Degree Program | B.Sc. in Computer Science & Engineering |
| Thesis Title | *A Deep Learning-Based Approach for Automated Object Detection in Orthopantomogram (OPG) Images Using YOLO* |
| Co-Authors | Akhtaruzzaman Anik (`ID: 232-15-252`) & Mahajub Al Shabah (`ID: 232-15-900`) |
| Supervisors | Ms Faiza Feroz (Supervisor, Lecturer, CSE, DIU) & Israt Jahan (Co-supervisor, Senior Lecturer, CSE, DIU) |
| Canonical Bibliography | `02_Literature/references.bib` (single shared BibTeX file; `42` verified Core full-text studies `P0001–P0042` + dataset references; excluded seed list `[1]–[13]` prohibited per `DEC0019`) |

---

## 1. DIU CSE B.Sc. Thesis Structural Checklist

1. **Front Matter:** DIU Cover & Title Page, Declaration of Originality (signed by both co-authors), Supervisor Approval Certificate, Abstract (`<= 300` words grounded strictly in realized `EVAL0001–EVAL0014` metrics), Acknowledgements, Table of Contents, List of Figures (`FIG0001–FIG0006`), List of Tables (`TAB0001–TAB0006`), List of Abbreviations & Symbols.
2. **Core Chapters (`11_Writing/thesis/`):**
   - Chapter 1: Introduction (Background, Motivation, Problem Statement, Objectives `O1–O3`, Research Questions `RQ0–RQ3`, Scope & Thesis Organization)
   - Chapter 2: Literature Review (PRISMA-style Screening of `122` records -> `42` Core Full-Text Studies, Methodological Gaps `GAP0001–GAP0006`, Summary Comparison Table `TAB0001`)
   - Chapter 3: Methodology (6-Cohort Portfolio `DS0001–DS0006`, Ontology `CLS0001–CLS0041`, Connected-Component Deduplication & Group-Stratified `70/15/15` Splits `SPLIT0001–SPLIT0006`, Reversible Preprocessing `PP0001–PP0004`, YOLO Architecture & Controlled `13`-EXP Matrix, Evaluation/Timing/Freeze Protocol `FREEZE0001`)
   - Chapter 4: Experimental Results (`EVAL0001–EVAL0014` Held-Out Scoreboard with `1,000`-Resample `GroupID` `95% CI`, Per-Class Contrast Hierarchy, `RQ2` `CLAHE` vs `1280px` Ablations, `12` Zero-Shot `5`-Country `HC01–HC05` Bridges, `RQ3` Kaggle `Tesla T4` GPU vs Local `Intel i5-1135G7` CPU `ONNXRuntime` Pareto Tradeoffs)
   - Chapter 5: Error Analysis, Limitations & Research Prototype (`T19` TIDE FP/FN & Size-Bucket Recall Analysis, Visual Case Audit Separating Model Error from Source-Label Incompleteness & Ordinal Boundary Ambiguity, Bounded Limitations & Non-Clinical Guardrails, `OPGPrototypeEngine` & `STEP-038` Clean-Run Reproducibility `R1–R3`)
   - Chapter 6: Conclusion & Future Work (Direct Answers to `O1–O3` & `RQ0–RQ3`, Bounded Contributions, Future Directions)
3. **Back Matter:** References (generated solely from `02_Literature/references.bib`), Appendices (Class Ontology Summary, Immutable Freeze & Evaluation Hashes, Reproduction Commands, Gate Audit Trail `G01–G14`).

---

## 2. Mandatory Declarations & Licensing Compliance

- **Non-Clinical Research Scope Statement:** Explicitly states that no model or prototype is clinically validated or regulatory-cleared, and zero detections never rule out pathology.
- **Dataset Provenance & License Attribution:** Cites all `6` public cohorts (`DS0001` UMFIH, `DS0002` DENTEX `CC-BY-NC-SA-4.0`, `DS0003` Rahman Dhaka, `DS0004` Do 2024 Hanoi, `DS0005` AU-OPG Ajman UAE, `DS0006` MD-OPG Pediatric), explicitly confirming `DS0002` non-commercial isolation and `0` private/PII data committed to Git (`tracked_forbidden_count = 0`).
- **Co-Author Contribution Declaration:** Reflects the `50/50` technical and writing ownership recorded in `01_Project_Management/team_roles.md v1.0.0`.

---

## 3. Open Human / Supervisor Confirmations Prior to `G15` (`UD17`)

- [ ] Official DIU CSE final thesis submission & defense date *(pending department calendar confirmation)*.
- [ ] Official DIU LaTeX/Word cover-page margins & citation style confirmation (IEEE numeric vs APA) *(pending Supervisor Ms Faiza Feroz)*.
- [ ] Optional conference/journal paper submission decision & target venue *(strictly optional; no publication acceptance is required or assumed for thesis completion)*.
