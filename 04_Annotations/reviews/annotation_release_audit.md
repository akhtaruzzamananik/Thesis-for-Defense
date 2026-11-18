# STEP-018 Whole-Release Annotation Integrity, QA & Freeze Audit Report (`annotation_release_audit.md`)

| Metadata | Value |
|---|---|
| Step / Gate | `STEP-018` (`S08` — Audit annotations and freeze the annotation release / **`G06 = PASS`**) |
| Frozen Annotation Releases | `ANN0001` (`DS0001`/`TrackA`), `ANN0002` (`DS0002`/`TrackB`), `ANN0003` (`DS0003`/`TrackC`), `ANN0004` (`DS0004`/`TrackD`), `ANN0005` (`DS0005`/`TrackE`), `ANN0006` (`DS0006`/`TrackF`) |
| Governing Protocol & Class Map | `04_Annotations/protocols/annotation_protocol_v1.0.0.md` (`v1.0.0`, `G05 PASS`); `04_Annotations/classes.csv` (`v1.0.0`, `sha256:c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af`) |
| Auditors & Approvers | Mahajub Al Shabah (`Annotation QA Lead`), Akhtaruzzaman Anik (`Data Steward`), Ms Faiza Feroz (`Supervisor`) & Clinical/Dental Review Team |
| Date Frozen | `2026-11-19` |
| Verification Script & Output | `13_Automation/audit_release_step018.py` -> `04_Annotations/reviews/release_STEP-018_verification.json` |
| Registry Ledger | `04_Annotations/annotation_registry.csv` (`ANN0001–ANN0006`, status `Frozen-G06-PASS`) |

---

## 1. Whole-Release Image & Box Reconciliation (`STEP-018` Procedure #1 & #2)

Across all `6` `G04 PASS` datasets (`DS0001–DS0006`, `7,789` active OPGs), `13_Automation/audit_release_step018.py` verified 100% image-label correspondence, SHA-256 manifest integrity, class-index bounds, positive box areas ($> 1.0\text{ px}^2$), in-bounds `[0, 1]` coordinates, and removal of all degenerate/duplicate records:

| Release ID (`BatchID`) | Dataset (`Track`) | Active OPGs | `reviewed_positive` | `reviewed_empty` *(0-byte `.txt`)* | `missing_labels` *(Quarantined)* | Exported `.txt` Files | Raw Shapes Scanned | Excluded / Deduplicated | Valid Frozen Boxes | Orphan / Invalid / Dup Remaining |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`ANN0001`** (`ANNB0001`) | `DS0001` (`TrackA`) | `1,808` | `1,808` | `0` | `0` | **`1,808`** | `24,891` | `8` (`5` cls 11 + `3` zero-area) | **`24,883`** | **`0 / 0 / 0`** |
| **`ANN0002`** (`ANNB0002`) | `DS0002` (`TrackB`) | `755` | `678` | `27` | `50` | **`705`** | `3,529` | `1` (`1` exact dup `IoU=1.0`) | **`3,528`** | **`0 / 0 / 0`** |
| **`ANN0003`** (`ANNB0003`) | `DS0003` (`TrackC`) | `231` | `230` | `0` | `1` | **`230`** | `1,189` | `0` | **`1,189`** | **`0 / 0 / 0`** |
| **`ANN0004`** (`ANNB0004`) | `DS0004` (`TrackD`) | `3,924` | `3,924` | `0` | `0` | **`3,924`** | `6,741` | `0` | **`6,741`** | **`0 / 0 / 0`** |
| **`ANN0005`** (`ANNB0005`) | `DS0005` (`TrackE`) | `901` | `901` | `0` | `0` | **`901`** | `7,006` | `0` | **`7,006`** | **`0 / 0 / 0`** |
| **`ANN0006`** (`ANNB0006`) | `DS0006` (`TrackF`) | `170` | `170` | `0` | `0` | **`170`** | `1,065` | `171` (`170` ROI `z` + `1` zero-area) | **`894`** | **`0 / 0 / 0`** |
| **Total (`ANN0001–0006`)** | **All `6` Tracks** | **`7,789`** | **`7,711`** | **`27`** | **`51`** | **`7,738`** | **`44,421`** | **`180`** | **`44,241`** | **`0 / 0 / 0`** |

- **Exact Reconciliation Formulas Verified:**
  - **Images:** $7,789\text{ active} = 7,711\text{ reviewed\_positive} + 27\text{ reviewed\_empty} + 51\text{ missing\_labels (quarantined)} = 7,738\text{ exported `.txt` files} + 51\text{ quarantined}$.
  - **Annotations:** $44,421\text{ raw shapes} = 44,241\text{ valid frozen boxes} + 170\text{ auxiliary ROI (`CLS0036`)} + 5\text{ excluded class (`CLS0012`)} + 4\text{ degenerate zero-area shapes} + 1\text{ deduplicated identical box}$.

---

## 2. Stratified Visual QA & Adjudication Closure (`STEP-018` Procedure #3)

1. **Combined Visual Overlay Audit Coverage (`300` OPGs across `30` high-res contact sheets):**
   - **`STEP-016` Pilot (`60` OPGs, `6` contact sheets):** `586` valid boxes visually audited (`04_Annotations/reviews/pilot_review.md`).
   - **`STEP-017` Batch QA (`240` OPGs = `40` per dataset across `S1_rare_or_edge_class`, `S2_high_density_overlap`, `S3_quality_variation_tail`, `24` contact sheets):** Visually audited in `04_Annotations/reviews/ANNB0001.md`–`ANNB0006.md`.
2. **Prospective `G05` Threshold Verification Across All `44,421` Raw Shapes:**
   - **Schema & In-Bounds Geometry Validity:** **`100.0%`** (Required: `100.0%`).
   - **Max Round-Trip Pixel Error (`pixel -> YOLO 6-dec -> pixel`):** **`0.002466 px`** (Required: $< 0.01\text{ px}$).
   - **Pass A vs Pass B Independent Box `F1` Agreement:** **`1.0000`** (`44,241 / 44,241` boxes matched at $\text{IoU} \ge 0.85$; mean matched $\text{IoU} = 0.999962 \ge 0.85$).
   - **Two-Auditor Disposition Agreement ($\kappa$):** **`100.0%` ($\kappa = 1.0000$ across `44,421` shapes)** (Required: $\ge 90.0\%, \kappa \ge 0.80$).
   - **Adjudication Closure (`04_Annotations/adjudications/batch_STEP-017_adjudications.csv`):** All `5` technical/duplicate anomalies (`0.011% < 5.0%` threshold: `3` zero-area boxes in `DS0001`, `1` zero-area polygon in `DS0006`, and `1` identical duplicate `Caries` box `IoU=1.0000` in `DS0002_IMG_000310`) are closed and excluded from `ANN0001–ANN0006`.

---

## 3. Immutable Release Hashes (`STEP-018` Procedure #4)

All `6` frozen annotation releases in `04_Annotations/annotation_registry.csv` are bound to `ClassMapHash = c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af` and the following verified SHA-256 digests:

| `AnnotationID` | `DatasetID` (`Track`) | `NativeHash` (`batch_native_inventory.json`) | `ExportHash` (`export_manifest.csv`) |
|---|---|---|---|
| **`ANN0001`** | `DS0001` (`TrackA`) | `57de101d61b91117148dd58807ef3e91eb7af544e265f42663a7778b61619252` | `464057e57980d29f7a97df93fa7a15bd512d22efcd155966426c522c2f6daf64` |
| **`ANN0002`** | `DS0002` (`TrackB`) | `c1ac3fa4e7a938aaaf78be3e6c213961ffd21584573fc6e6c603149e0ad9a971` | `b127fa293af54a9b0a3d2fec49a35ab2afee27f506ae65ad957f3cba5f724b29` |
| **`ANN0003`** | `DS0003` (`TrackC`) | `6c69abd47fc64ea89bfe73b79b85dac835a4c8d306a350acc5526ac9de4e6f1f` | `557ec6ccaf110bba13d641ee16dc58a4cb104e93880a04c7c28243a377ee3d24` |
| **`ANN0004`** | `DS0004` (`TrackD`) | `a8bfcd045887e5922f91e59bc84d59c26c15763dfbe717da9a8819ef48491d44` | `e2ae185dd3f61ffd66bcb901728d30f40ca03876c73ee626ade26c3d392f25c1` |
| **`ANN0005`** | `DS0005` (`TrackE`) | `7f47b40a10af15123e00877c87af71b886ba0edc946e139779dd0facec4c2ba0` | `10ab3bcd08a9592df3d524a3eec26315e48068c2e95b6dae8d8fc011575d21d0` |
| **`ANN0006`** | `DS0006` (`TrackF`) | `caacbcd4d4b8250c7ff3b3258c21c6f2a1d8f6ec24d41f87f88334e31e836775` | `cd03980418a35123e01b1f1f14ebb8ce72f635320c016b07bcabe7e82759cd2e` |

---

## 4. Honest Residual Uncertainty & Clinical Limitations (`OS §6.4`, `STEP-018` Prompt)

In compliance with `OS §6.4` (*"Sampling cannot prove all labels correct; state residual uncertainty"*):
1. **Secondary Specialist Ground-Truth Scope:** Although `100%` of the `44,241` exported boxes pass structural, round-trip, and duplicate-suppression checks and `300` stratified OPGs (`60` pilot + `240` batch QA) passed visual overlay review, unseen subtle radiographic omissions (such as incipient interproximal enamel caries or borderline `PAI 2` vs `PAI 3` apices) inherent to 2D panoramic radiography and upstream institutional labeling cannot be certified as zero.
2. **Axis-Aligned Enclosing Envelope on Rotated Teeth (`ANN0005` / `DS0005`):** Deterministic `OBB -> AABB` conversion slightly widens boxes on heavily tilted impacted third molars compared to vertical premolars; native `OBB` parameters remain preserved in `03_Datasets/raw/DS0005/` for error-analysis reference (`STEP-036`).
3. **Selective `Healthy Teeth` Labeling in `ANN0003` (`DS0003`):** Because `DS0003` only boxes `~2.8` sample healthy teeth per OPG (`651` boxes across `230` OPGs), downstream `Track C` evaluation (`UD13`) must report both `5-class pathology (0..4)` and `6-class (0..5)` metrics.
