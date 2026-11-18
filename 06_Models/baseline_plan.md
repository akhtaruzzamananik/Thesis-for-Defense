# YOLO Implementation Selection & Baseline Plan (`STEP-022` / `UD10`)

| Metadata | Value |
|---|---|
| Step / Stage | `STEP-022` (`S10` — Select the YOLO implementation and baseline candidate) |
| Record | `06_Models/baseline_plan.md` (`v1.0.0`) |
| Owner | Mahajub Al Shabah (`232-15-900`, Model & Evaluation Lead) |
| Co-Reviewer & Approver | Akhtaruzzaman Anik (`232-15-252`, Research Lead) & Ms Faiza Feroz (`Supervisor`) |
| Date | `2026-11-19` |
| Linked Decision & Table | `01_Project_Management/decision_log/DEC0010.md` (`UD10`); `06_Models/candidates.csv` (`MC0001–MC0005`) |
| Governing Sections | `OS §3`, `§5.1`, `§10`; Blueprint `STEP-022`; `02_Literature/research_questions.md` (`RQ0–RQ3`) |

---

## 1. Grounded Selection Rationale (`STEP-022` Procedure #1–4)

The approved project title specifies the **YOLO** object-detection family without mandating a specific package, version, or model scale (`OS §5.1`). Evaluating `5` official open-source implementations (`MC0001–MC0005` in `06_Models/candidates.csv`) against our `6` prepared releases (`REL0001–REL0006`, `G08 PASS`), our literature synthesis (`02_Literature/synthesis.md`), and our Kaggle `16 GB` GPU (`T4`/`P100`) compute constraints yields the following selection:

1. **Selected Primary Baseline (`MC0001`): `ultralytics` `YOLO11s` (`yolo11s.pt`, COCO-pretrained)**
   - **Why selected (without assuming newer = better):**
     - **Unified, Maintainable Framework:** Implemented in the official `ultralytics` package (`8.3.x` release branch, explicitly excluding the `8.3.41/42/45/46` PyPI supply-chain incident releases; exact pin verified in `STEP-023`).
     - **Direct Data Compatibility (`Zero G08 Rework`):** Natively consumes normalized YOLO `AABB` `.txt` labels (`REL0001–REL0006`) and `640×640` / `1280×1280` letterboxed `3`-channel RGB inputs (`PP0001–PP0004`) without altering `SPLIT0001–SPLIT0006` or `classes.csv` (`sha256:c3f91dfc...`).
     - **Compute Feasibility (`Kaggle 16 GB VRAM`):** Compact `small` scale (`~9.4M` parameters, `~21.5 GFLOPs` @ `640`, provisional until observed in `STEP-023`/`026`) trains comfortably on Kaggle `T4`/`P100` (`16 GB`) at both `640×640` (`PP0001–0003`) and `1280×1280` (`PP0004`), enabling multi-track training (`Tracks A–F`) and controlled `RQ2` ablations within weekly GPU limits.
     - **Fair Baseline Role:** Serves as the controlled anchor for `RQ0`, `RQ1`, `RQ2` (`PP0001` vs `PP0002/0003/0004`), and `RQ3` (`GPU + CPU` `T_e2e` & `FPS_e2e`).

2. **Selected Cross-Generation Comparator (`MC0002`): `ultralytics` `YOLOv8s` (`yolov8s.pt`, COCO-pretrained)**
   - **Why selected:** Runs inside the **exact same `ultralytics` trainer, augmentation pipeline, and checkpointing stack** as `YOLO11s`, eliminating framework/dataloader confounders during `RQ1`/`RQ3` comparisons while providing direct continuity with `P0008`, `P0014`, `P0023`, `P0025`, and `P0030`.

3. **Selected Conditional Scale Comparator (`MC0003`): `ultralytics` `YOLO11m` (`yolo11m.pt`, COCO-pretrained)**
   - **Why selected:** Enables direct comparison against `P0015` (`Eftimie et al., 2025`, which benchmarked `YOLO11m` on `UMFIH` `DS0001` at `1280px` and `1024px`) on `Track A` (`REL0001`) if Kaggle compute budget allows (`STEP-024` matrix).

4. **Rejected Alternatives (`MC0004 YOLOv9` & `MC0005 YOLOv10`):**
   - `MC0004` (`WongKinYiu/yolov9`, `GPL-3.0`): Requires a separate codebase/trainer interface and auxiliary reversible branch VRAM overhead, introducing codebase confounders.
   - `MC0005` (`THU-MIG/yolov10`, `AGPL-3.0`): NMS-free one-to-one head alters our `UD13` `NMS IoU` operating-point protocol and showed lower OPG recall than `YOLOv8` in `P0030`.

---

## 2. Pretrained Weights, Licensing & `S16` Web-Demo Compliance (`OS §5.1`, `UD10`)

1. **Pretrained Weight Provenance:**
   - Official Ultralytics COCO-80 detection checkpoints (`yolo11s.pt`, `yolov8s.pt`, and optionally `yolo11m.pt`) downloaded directly from official Ultralytics GitHub releases (`https://github.com/ultralytics/ultralytics/releases`).
   - Exact `SHA-256` hashes of downloaded initial weights will be recorded in `06_Models/` and `EXP####/config.yaml` during `STEP-023`/`STEP-026`, stored strictly **off-Git** (`06_Models/weights/`).
   - **Overlap Risk Disclosure:** Natural-image COCO-80 contains zero dental orthopantomograms (`0` OPG overlap risk with `DS0001–DS0006`); fine-tuning on OPG is explicitly reported as transfer learning, **never** claimed as a "novel architecture" (`OS §5.1`).
2. **License & Track Isolation (`AGPL-3.0` + Dataset Licenses):**
   - `ultralytics` is dual-licensed under **`AGPL-3.0`** (free for academic research and open-source network deployments; commercial closed-source deployment requires an Enterprise License).
   - Because our `S16` defense web showcase (`web/` & `16_Web_Demo/`) is an open-source academic research showcase (`UD21–UD24`), `AGPL-3.0` compliance is satisfied by keeping the repository source open under `AGPL-3.0`-compatible terms and never deploying commercially.
   - Weights trained on `REL0002` (`DS0002 DENTEX`, `CC-BY-NC-SA-4.0`) remain strictly non-commercial and isolated from `CC BY 4.0` tracks (`DEC0003 v6`).

---

## 3. Data-Interface & `G08` Impact Check (`STEP-022` Checklist #4)

- **Zero Changes Required to `REL0001–REL0006` (`G08 PASS`):**
  - `ultralytics` consumes our materialized `labels/<partition>/<ImageID>.txt` (`6`-decimal normalized YOLO `AABB`) and `640×640` / `1280×1280` `3`-channel RGB inputs (`PP0001–PP0004`) directly.
  - Because `640` and `1280` are exact multiples of YOLO stride `32`, **no `STEP-019–021` rework or `G08` reassessment is triggered**.
