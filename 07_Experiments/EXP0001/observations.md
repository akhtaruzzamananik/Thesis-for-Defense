# `EXP0001` Run Observations & Attempt Log (`STEP-028`)

| Attempt | RunID | Status | Hardware | Start (UTC) | End (UTC) | Epochs Completed | Stopping Reason | Best Epoch (`val mAP@0.50`) | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `1` | `RUN0001` | **`COMPLETED`** | Kaggle `Tesla T4` (`torch 2.11.0+cu130`, `ultralytics 8.3.253`) | `2026-11-19T17:52:40Z` | `2026-11-19T18:22:22Z` | `85 / 100` (`1,682.8 s` / ~`28 min`) | `early_stop_patience_20` (no `val` improvement after epoch `65`) | **`65`** (`P=0.4662`, `R=0.4204`, `F1=0.4421`, `mAP@0.50=0.3792` [`0.381` final val], `mAP@0.50:0.95=0.1570`) | Zero NaN/Inf, `config_sha256` & `best.pt`/`last.pt` SHA-256 verified on local retrieval (`ce8e5b44...` / `14701b6e...`). |

## Observed Per-Class `val` `AP@0.50` (`BoxPR_curve.png`, `214` `REL0001` `val` OPGs)

- **High-contrast / large structural targets:** `Surgical_Device` (`0.904`), `Endodontic_Treatment` (`0.662`), `Impacted_Tooth` (`0.643`), `Prosthetic_Restoration` (`0.544`), `Root_Fragment` (`0.452`), `Obturation` (`0.435`), `Implant` (`0.421`).
- **Low-contrast / tiny focal lesions & ultra-rare targets at `640×640` (`PP0001`):** `Orthodontic_Device` (`0.265`), `Apical_Periodontitis` (`0.198`), `Carious_Lesion` (`0.173`), `Furcation_Lesion` (`0.150`), `Bone_Resorption` (`0.094`), `Apical_Surgery` (`0.010`, ultra-rare `N=91` dataset-wide).
- **Scientific Implication (`RQ1` / `RQ2`):** Confirms strong radiopaque/structural detection at `640×640` while directly motivating controlled `RQ2` tests (`EXP0010` `1280×1280` `PP0004` & `EXP0008–0009` `CLAHE`) for small/low-contrast radiolucent lesions.
