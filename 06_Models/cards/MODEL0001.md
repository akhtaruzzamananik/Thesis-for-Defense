# Model Card — `MODEL0001` (`EXP0001` Primary Baseline `YOLO11s` @ `640×640`)

| Field | Value |
|---|---|
| Model ID | `MODEL0001` |
| Candidate / Architecture | `MC0001` (`ultralytics==8.3.253` `YOLO11s`, COCO-pretrained `yolo11s.pt`, `sha256:85a76fe8...`) |
| Experiment / Run / Checkpoint | `EXP0001` / `RUN0001` / `CKPT0003` (`best.pt`, epoch `65`, `sha256:ce8e5b44...`, `19,191,578` bytes) |
| Data Release & Split | `REL0001` (`DS0001` `UMFIH` `TrackA`, `SPLIT0001`, `994` train / `214` val; **`208` test & `178` external_test SEALED**) |
| Class Map & Preprocessing | `classes.csv` (`sha256:c3f91dfc...`, `13` `TrackA` classes) / `PP0001` (`640×640` raw letterbox, `sha256:04493e1e...`) |
| Training Runtime | Kaggle `Tesla T4` (`torch==2.11.0+cu130`, `ultralytics==8.3.253`, `seed=20261124`, `85` epochs / `1,682.8 s`, `early_stop_patience_20`) |
| License | `AGPL-3.0` (`ultralytics`) + `CC BY 4.0` (`DS0001`) — open-source academic research only |
| Eligibility (`G10`) | **`ELIGIBLE — G10 PASS` (`2026-11-20`)** |

---

## 1. Observed Validation Performance (`REL0001` `val`, `214` OPGs — NO `test` data accessed)

- **Best Epoch (`65` / `85`, `results.csv`):** `Precision = 0.4662`, `Recall = 0.4204`, `F1 = 0.4421`, `mAP@0.50 = 0.3792` (`0.381` final `best.pt` `BoxPR_curve.png`), `mAP@0.50:0.95 = 0.1570`.
- **Per-Class `AP@0.50` (`BoxPR_curve.png`):**
  - High-contrast / structural targets: `Surgical_Device` (`0.904`), `Endodontic_Treatment` (`0.662`), `Impacted_Tooth` (`0.643`), `Prosthetic_Restoration` (`0.544`), `Root_Fragment` (`0.452`), `Obturation` (`0.435`), `Implant` (`0.421`).
  - Low-contrast / tiny focal & ultra-rare targets at `640×640`: `Orthodontic_Device` (`0.265`), `Apical_Periodontitis` (`0.198`), `Carious_Lesion` (`0.173`), `Furcation_Lesion` (`0.150`), `Bone_Resorption` (`0.094`), `Apical_Surgery` (`0.010`).

---

## 2. Intended Use, Limitations & Non-Clinical Disclaimer

- **Intended Use:** Leak-free `640×640` primary baseline anchor for `RQ0`, `RQ1` (`EXP0002 YOLOv8s`, `EXP0013 YOLO11m`), and `RQ2` (`EXP0008–0010` `CLAHE` & `1280×1280`) comparisons.
- **Known Limitations:** `640×640` downscaling degrades tiny radiolucent lesions (`Carious_Lesion`, `Apical_Periodontitis`, `Bone_Resorption`, `Furcation_Lesion`) and ultra-rare `Apical_Surgery` (`N=91` total boxes).
- **Safety Boundary:** Research prototype only; **not** a clinical diagnostic device. Absence of a predicted box does not rule out pathology.
