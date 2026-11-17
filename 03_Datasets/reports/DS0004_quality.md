# STEP-013 Quality, Privacy, Duplicate & Label Forensic Audit — `DS0004` (`CAND0004` Do 2024 Hanoi)

| Field | Value |
|---|---|
| DatasetID / CandidateID | `DS0004` / `CAND0004` (`Hanoi Panoramic Periapical Lesions Dataset` — Do 2024) |
| Audit Scope & Count | **`3,924`** active `Original JPG Images` (`13,071` `Augmentation JPG Images` quarantined out of `16,995` total JPGs); `0` decode errors |
| Owner / Auditor | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| Date | `2026-11-18` |
| Evidence Sources | `03_Datasets/manifests/DS0004_images.csv`, `03_Datasets/manifests/DS0004_qc_summary.json`, off-Git `DS0004_restricted_qc.csv`, `DS0004_restricted_dups.csv`, `qc_samples/DS0004_qc_sheet.jpg` |
| Gate Status | Batch 2 technical audit **complete**; **`G04` review pending human/dental confirmation** |

---

## 1. Decoding, Dimensions, Dual-Machine Provenance & Photometric Quality

| Metric (`N = 3,924` originals) | `min` | `p05` | `median` | `p95` | `max` | Finding |
|---|---|---|---|---|---|---|
| **Width (px)** | `2,316` | `2,444` | `2,444` | `2,624` | `2,636` | High, uniform resolution across all `3,924` scans |
| **Height (px)** | `1,252` | `1,252` | `1,292` | `1,292` | `1,292` | Bimodal resolution (`2444 × 1292` vs `2473–2624 × 1252`) |
| **Aspect Ratio (`W/H`)** | `1.79` | `1.89` | `1.89` | `2.04` | `2.10` | `0` aspect outliers |
| **Mean Luma (`0–255`)** | `109.43` | `113.10` | `116.53` | `131.05` | `140.57` | Very tight photometric consistency |
| **`%` Black (`<= 3`) / White (`>= 252`)** | `0.0 / 3.48` | `0.03 / 4.35` | `0.08 / 6.67` | `0.53 / 7.54` | `3.59 / 9.07` | Thin bright film frame border (`~6.7%` white) |
| **Sharpness (`Laplacian var` @ 800w)** | `88.14` | `108.90` | `145.62` | `353.52` | `490.21` | Consistent diagnostic detail across films |

- **Visual Hardware Discovery (`DS0004_qc_sheet.jpg`):** Bimodal `height = 1292` vs `1252` corresponds to two panoramic machines visible in corner watermarks: **`Sirona Orthophos XG` (`2444×1292`, `[L]` tag)** and **`"R RAYSCAN α"` (`2473×1252`, seen on `DS0004_IMG_013356` & `013628`)**, providing built-in multi-scanner acquisition variation!
- **Channels / Tint:** `3,923` clean grayscale images + **`1` non-identical RGB (`DS0004_IMG_013187`)**, which pixel correlation (`0.9998`) revealed is an RGB-re-encoded duplicate of `DS0004_IMG_016453`!

---

## 2. Privacy & Metadata Inspection

- **EXIF Metadata:** **`0` sensitive EXIF tags** (`0` `DateTime/GPS/Software` EXIF fields). JPEG info chunks include `progressive=3924` and `"LEAD Technologies Inc. V1.01"` `comment` on `3,054` files (encoder library string, `0` PHI).
- **XML Local Path Note:** Upstream `.xml` `<path>` elements contain author Windows directory path `F:\DuLieuRang\UpdateData\...` — kept strictly off-Git inside `raw/` and excluded from derived CSVs (`0` patient IDs observed in visual check).

---

## 3. Critical Duplicate Finding Inside `Original JPG Images` (`Even After Removing All 13,071 Augmentations!`)

Prior work (`P0008`) emphasized stripping the `Augmentation JPG Images` folder to obtain `3,924` originals, yet SHA-256 + pixel-correlation screening on `Original JPG Images` itself (`N = 3,924`) exposed hidden intra-folder duplicates:

1. **Exact byte-for-byte SHA-256 duplicates inside `Original JPG Images`:** **`61` exact SHA-256 pairs (`59` extra duplicate files -> only `3,865` unique SHA-256 hashes!)**.
2. **Additional re-encoded identical pairs (`SHA-256 != SHA-256`, `dHash H=0`, `corr >= 0.99`):**
   - `DS0004_IMG_013187 <-> DS0004_IMG_016453` (`corr = 0.9998`, RGB re-encode of grayscale scan)
   - `DS0004_IMG_014993 <-> DS0004_IMG_016792` (`corr = 0.9971`)
   - Plus `DS0004_IMG_014630 <-> DS0004_IMG_016338` (`corr = 0.9533, H=0` -> inspect/group under `UD07`).
3. *(Note on `47,263` raw `dHash <= 4` count: driven by shared uniform `~6.7%` bright border lines + standardized Sirona jaw silhouette across `3,924` images -> `N(N-1)/2 = 7.7M` pairs; pixel correlation cleanly separates true `corr >= 0.99` duplicates [`2` pairs] from distinct patients.)*

> [!IMPORTANT]
> **Mandatory `UD07 / G07` Action:** Deduplicate all **`59` exact SHA-256 copies + `2` `corr >= 0.99` copies** (`~3,863` unique radiograph clusters) before splitting `DS0004`, exceeding even `P0008`'s un-hashed `3,924` filtering!

---

## 4. XML Label Audit (`Image Annots/`)

- **`3,924 / 3,924` active originals** have paired non-empty Pascal VOC XMLs (`0` missing, `0` empty, `0` malformed, `0` OOB, `0` zero-area).
- **Exact lesion count:** **`6,741` boxes** (`PAI 3 = 4,277` [`63.45%`], `PAI 4 = 1,755` [`26.03%`], `PAI 5 = 709` [`10.52%`]), matching `P0008 Table 1`. (`9` XMLs in `17,004` lack matching JPGs across `3,924 + 13,071 = 16,995` and remain orphaned.)

---

## 5. Prospective Rules (`G04 / UD04 / UD07`)

1. Keep **`13,071` `Augmentation JPG Images` quarantined** and deduplicate **`59` exact SHA + `2` re-encoded duplicate files** inside `Original JPG Images` cleanly (`~3,863` unique OPGs).
2. Analyze **`DS0004` strictly on its dedicated `PAI 3–5` small-lesion / tiling sub-track** (`zero healthy OPGs` spectrum bias prevents blind naive pooling with multi-class restoration datasets).
