"""Read-only STEP-013 quality, privacy/EXIF, perceptual dHash, and label forensic audit CLI."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import math
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.dataset_qc import (  # noqa: E402
    audit_yolo_label_dir,
    find_near_duplicate_pairs,
    inspect_image_qc,
)

RAW_ROOT = ROOT / "03_Datasets" / "raw"
MANIFEST_ROOT = ROOT / "03_Datasets" / "manifests"
QC_SAMPLE_ROOT = RAW_ROOT / "qc_samples"


def _load_linkage(dataset_id: str) -> dict[str, str]:
    """Load restricted ImageID -> original_relpath mapping from off-Git linkage CSV."""
    path = MANIFEST_ROOT / f"{dataset_id}_restricted_linkage.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["ImageID"]: row["original_relpath"] for row in csv.DictReader(handle)}


def _load_manifest(dataset_id: str) -> list[dict[str, str]]:
    """Load public sanitized DS####_images.csv rows."""
    path = MANIFEST_ROOT / f"{dataset_id}_images.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _quantile_summary(values: list[float]) -> dict[str, float]:
    """Compute min, p05, median, p95, max summary dict."""
    if not values:
        return {}
    arr = np.asarray(values, dtype=np.float64)
    return {
        "min": round(float(arr.min()), 2),
        "p05": round(float(np.percentile(arr, 5)), 2),
        "median": round(float(np.median(arr)), 2),
        "p95": round(float(np.percentile(arr, 95)), 2),
        "max": round(float(arr.max()), 2),
    }


def _audit_ds0001_labels(extracted_dir: Path) -> dict[str, object]:
    """Inspect all 4 DS0001 (UMFIH) label splits to verify class-index alignment."""
    split_specs = {
        "internal_train": (extracted_dir / "train" / "images", extracted_dir / "train" / "labels"),
        "internal_valid": (extracted_dir / "valid" / "images", extracted_dir / "valid" / "labels"),
        "internal_test": (extracted_dir / "test" / "images", extracted_dir / "test" / "labels"),
        "external_validation": (
            extracted_dir / "test_alte_cabinete" / "Ext-validation" / "images",
            extracted_dir / "test_alte_cabinete" / "Ext-validation" / "labels",
        ),
    }
    results: dict[str, object] = {}
    for name, (img_dir, lbl_dir) in split_specs.items():
        imgs = sorted(p for p in img_dir.iterdir() if p.is_file())
        results[name] = audit_yolo_label_dir(imgs, lbl_dir)
    return results


def _audit_ds0003_labels_and_branch(extracted_dir: Path, all_qc: list[dict[str, object]]) -> dict[str, object]:
    """Check DS0003 (Dhaka) Original YOLO labels and resolve 231 vs 232 classification mismatch."""
    orig_dir = extracted_dir / "Dental OPG XRAY Dataset" / "Dental OPG (Object Detection)" / "Original Dataset"
    imgs = sorted(p for p in orig_dir.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    yolo_audit = audit_yolo_label_dir(imgs, orig_dir)

    # Check dHash overlap between original (231) and classification unique hashes (232)
    orig_items = [x for x in all_qc if x["source_bucket"] == "object_detection_original"]
    cls_seen_sha: set[str] = set()
    cls_unique: list[dict[str, object]] = []
    for x in all_qc:
        if x["source_bucket"] == "classification_branch" and x["sha256"] not in cls_seen_sha:
            cls_seen_sha.add(str(x["sha256"]))
            cls_unique.append(x)

    orig_sha_set = {str(x["sha256"]) for x in orig_items}
    cls_only = [x for x in cls_unique if x["sha256"] not in orig_sha_set]
    orig_only = [x for x in orig_items if x["sha256"] not in cls_seen_sha]

    unmatched_cls_matches: list[dict[str, object]] = []
    for c in cls_only:
        dists = sorted(
            ((int(str(c["dhash64"]), 16) ^ int(str(o["dhash64"]), 16)).bit_count(), o["image_id"])
            for o in orig_items
        )
        best_dist, best_id = dists[0] if dists else (99, None)
        unmatched_cls_matches.append(
            {
                "cls_image_id": c["image_id"],
                "best_orig_match_id": best_id,
                "min_dhash_hamming_to_orig": best_dist,
            }
        )

    return {
        "original_yolo_audit": yolo_audit,
        "orig_count": len(orig_items),
        "cls_unique_sha_count": len(cls_unique),
        "exact_sha_overlap": len(orig_sha_set & cls_seen_sha),
        "orig_only_count": len(orig_only),
        "cls_only_count": len(cls_only),
        "cls_only_dhash_probe": unmatched_cls_matches,
    }


def _audit_ds0005_csv(extracted_dir: Path, all_qc: list[dict[str, object]]) -> dict[str, object]:
    """Audit DS0005 (AU-OPG) OBB CSV fields, bounds, class counts, and extra image overlap."""
    splits_out: dict[str, object] = {}
    for split, fn in (("train", "train_annotations.csv"), ("val", "val_annotations.csv"), ("test", "test_annotations.csv")):
        cond_cnt: Counter[str] = Counter()
        treat_cnt: Counter[str] = Counter()
        rot_vals: list[float] = []
        oob_unrotated = 0
        oob_rotated_corners = 0
        rows_total = 0
        unique_imgs: set[str] = set()
        with (extracted_dir / fn).open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                rows_total += 1
                unique_imgs.add(row["image"].strip())
                cond_cnt[row["condition"].strip()] += 1
                t_val = row["treatment"].strip() or "None"
                treat_cnt[t_val] += 1
                iw = float(row["image_width"])
                ih = float(row["image_height"])
                px = float(row["x"]) / 100.0 * iw
                py = float(row["y"]) / 100.0 * ih
                pw = float(row["width"]) / 100.0 * iw
                ph = float(row["height"]) / 100.0 * ih
                rot = float(row["rotation"])
                rot_vals.append(rot)
                if px < -1 or py < -1 or px + pw > iw + 1 or py + ph > ih + 1:
                    oob_unrotated += 1
                # Label Studio rotates rectangle clockwise around (px, py)
                rad = math.radians(rot)
                cos_r, sin_r = math.cos(rad), math.sin(rad)
                corners = [(0.0, 0.0), (pw, 0.0), (pw, ph), (0.0, ph)]
                for dx, dy in corners:
                    rx = px + dx * cos_r - dy * sin_r
                    ry = py + dx * sin_r + dy * cos_r
                    if rx < -5 or ry < -5 or rx > iw + 5 or ry > ih + 5:
                        oob_rotated_corners += 1
                        break

        splits_out[split] = {
            "rows": rows_total,
            "unique_images": len(unique_imgs),
            "conditions": dict(cond_cnt),
            "treatments": dict(treat_cnt),
            "rotation_min_max_deg": [round(min(rot_vals), 2), round(max(rot_vals), 2)] if rot_vals else [],
            "oob_unrotated": oob_unrotated,
            "oob_rotated_corners_gt5px": oob_rotated_corners,
        }

    # Check if 134 extra unannotated dataset/ images near-duplicate the 901 annotated images
    active = [x for x in all_qc if x["source_bucket"] in {"train_annotated", "val_annotated", "test_annotated"}]
    extras = [x for x in all_qc if x["source_bucket"] == "unannotated_extra_in_dataset"]
    extra_near_matches = 0
    for ex in extras:
        ex_h = int(str(ex["dhash64"]), 16)
        min_d = min((ex_h ^ int(str(a["dhash64"]), 16)).bit_count() for a in active) if active else 99
        if min_d <= 6:
            extra_near_matches += 1

    return {
        "csv_splits": splits_out,
        "extra_unannotated_count": len(extras),
        "extra_dhash_le6_near_annotated": extra_near_matches,
    }


def _audit_ds0006_json(extracted_dir: Path) -> dict[str, object]:
    """Audit all 170 DS0006 (MD-OPG) LabelMe JSON annotations."""
    ann_dir = extracted_dir / "MD_OPG" / "OPG_Annotation"
    jsons = sorted(ann_dir.glob("*.json"))
    label_cnt: Counter[str] = Counter()
    shape_type_cnt: Counter[str] = Counter()
    oob_points = 0
    zero_area_shapes = 0
    empty_files = 0
    embedded_img_data = 0
    dims: Counter[str] = Counter()

    for jp in jsons:
        data = json.loads(jp.read_text(encoding="utf-8"))
        w = int(data.get("imageWidth", 0))
        h = int(data.get("imageHeight", 0))
        dims[f"{w}x{h}"] += 1
        if data.get("imageData"):
            embedded_img_data += 1
        shapes = data.get("shapes", [])
        if not shapes:
            empty_files += 1
        for sh in shapes:
            label_cnt[str(sh.get("label"))] += 1
            shape_type_cnt[str(sh.get("shape_type"))] += 1
            pts = sh.get("points", [])
            if not pts:
                zero_area_shapes += 1
                continue
            xs = [float(pt[0]) for pt in pts]
            ys = [float(pt[1]) for pt in pts]
            if min(xs) < -1 or min(ys) < -1 or max(xs) > w + 1 or max(ys) > h + 1:
                oob_points += 1
            if max(xs) - min(xs) <= 0 or max(ys) - min(ys) <= 0:
                zero_area_shapes += 1

    return {
        "json_count": len(jsons),
        "empty_annotation_files": empty_files,
        "embedded_imagedata_count": embedded_img_data,
        "reported_dims": dict(dims),
        "shape_labels": dict(label_cnt),
        "shape_types": dict(shape_type_cnt),
        "oob_shapes_gt1px": oob_points,
        "zero_area_shapes": zero_area_shapes,
    }


def _audit_ds0002_coco(extracted_dir: Path, manifest_rows: list[dict[str, str]]) -> dict[str, object]:
    """Audit DS0002 (DENTEX) disease COCO JSON annotations and subfolder SHA-256 overlaps."""
    jpath = (
        extracted_dir
        / "training_data"
        / "training_data"
        / "quadrant-enumeration-disease"
        / "train_quadrant_enumeration_disease.json"
    )
    data = json.loads(jpath.read_text(encoding="utf-8"))
    cat3 = {c["id"]: c["name"] for c in data.get("categories_3", [])}
    cat1 = {c["id"]: c["name"] for c in data.get("categories_1", [])}
    img_map = {im["id"]: im for im in data.get("images", [])}

    dis_cnt: Counter[str] = Counter()
    quad_cnt: Counter[str] = Counter()
    oob_boxes = 0
    zero_area = 0
    for ann in data.get("annotations", []):
        dis_cnt[cat3.get(ann.get("category_id_3"), str(ann.get("category_id_3")))] += 1
        quad_cnt[cat1.get(ann.get("category_id_1"), str(ann.get("category_id_1")))] += 1
        x, y, w, h = (float(v) for v in ann["bbox"])
        im = img_map.get(ann["image_id"], {})
        iw, ih = float(im.get("width", 0)), float(im.get("height", 0))
        if w <= 0 or h <= 0:
            zero_area += 1
        if x < -1 or y < -1 or x + w > iw + 1 or y + h > ih + 1:
            oob_boxes += 1

    # Check exact SHA-256 overlap across active (705 + 50) vs quarantined sub-pools
    active_shas = {r["sha256"] for r in manifest_rows if not r["intake_status"].startswith("quarantined")}
    bucket_overlaps: dict[str, dict[str, int]] = {}
    for bucket in (
        "training_quadrant_enumeration_disease",
        "validation_quadrant_enumeration_disease_no_gt",
        "training_quadrant_only",
        "training_quadrant_enumeration_only",
        "training_unlabelled_xrays",
        "validation_ipynb_checkpoint",
    ):
        sub = [r for r in manifest_rows if r["source_bucket"] == bucket]
        sub_shas = {r["sha256"] for r in sub}
        bucket_overlaps[bucket] = {
            "count": len(sub),
            "unique_sha256": len(sub_shas),
            "overlap_with_active_disease_shas": len(sub_shas & active_shas),
        }

    return {
        "coco_images": len(img_map),
        "coco_annotations": len(data.get("annotations", [])),
        "disease_categories": dict(dis_cnt),
        "quadrant_categories": dict(quad_cnt),
        "oob_boxes_gt1px": oob_boxes,
        "zero_area_boxes": zero_area,
        "validation_public_gt_json_present": False,
        "bucket_sha256_summary": bucket_overlaps,
    }


def _audit_ds0004_xml(extracted_dir: Path, manifest_rows: list[dict[str, str]], linkage: dict[str, str], active_qc: list[dict[str, object]]) -> dict[str, object]:
    """Audit DS0004 (Do 2024 Hanoi) Original JPG XMLs, orphan XMLs, and augmentation SHA overlap."""
    ann_dir = (
        extracted_dir
        / "Panoramic radiographs with periapical lesions Dataset"
        / "Periapical Dataset"
        / "Periapical Lesions"
        / "Image Annots"
    )
    active_dim_by_stem = {
        Path(linkage[str(r["image_id"])]).stem: (int(r["width"]), int(r["height"]))
        for r in active_qc
    }

    missing_xml = 0
    empty_xml = 0
    malformed_xml = 0
    oob_boxes = 0
    zero_area = 0
    pai_counts: Counter[str] = Counter()
    total_boxes = 0
    for stem, (iw, ih) in active_dim_by_stem.items():
        xp = ann_dir / f"{stem}.xml"
        if not xp.is_file():
            missing_xml += 1
            continue
        try:
            root = ET.parse(xp).getroot()
        except ET.ParseError:
            malformed_xml += 1
            continue
        objs = root.findall("object")
        if not objs:
            empty_xml += 1
        for obj in objs:
            total_boxes += 1
            pai_counts[str(obj.findtext("name", "")).strip()] += 1
            box = obj.find("bndbox")
            if box is None:
                malformed_xml += 1
                continue
            xmin = float(box.findtext("xmin", "0"))
            ymin = float(box.findtext("ymin", "0"))
            xmax = float(box.findtext("xmax", "0"))
            ymax = float(box.findtext("ymax", "0"))
            if xmax <= xmin or ymax <= ymin:
                zero_area += 1
            if xmin < -1 or ymin < -1 or xmax > iw + 1 or ymax > ih + 1:
                oob_boxes += 1

    # Count all XML stems vs active original + quarantined aug stems
    all_xml_stems = {p.stem for p in ann_dir.glob("*.xml")}
    all_img_stems = {Path(linkage[r["ImageID"]]).stem for r in manifest_rows}
    orphan_xml_count = len(all_xml_stems - all_img_stems)

    orig_shas = {r["sha256"] for r in manifest_rows if r["source_bucket"] == "original_jpg_folder"}
    aug_shas = {r["sha256"] for r in manifest_rows if r["source_bucket"] == "augmentation_jpg_folder"}

    return {
        "active_originals": len(active_dim_by_stem),
        "missing_xml_for_active": missing_xml,
        "empty_xml_for_active": empty_xml,
        "malformed_xml": malformed_xml,
        "total_lesion_boxes_on_active": total_boxes,
        "pai_grade_counts": dict(sorted(pai_counts.items())),
        "oob_boxes_gt1px": oob_boxes,
        "zero_area_boxes": zero_area,
        "total_xml_files_in_dir": len(all_xml_stems),
        "orphan_xml_without_jpg": orphan_xml_count,
        "aug_quarantined_count": sum(1 for r in manifest_rows if r["source_bucket"] == "augmentation_jpg_folder"),
        "orig_vs_aug_exact_sha_overlap": len(orig_shas & aug_shas),
    }


def _save_qc_contact_sheet(
    dataset_id: str,
    qc_records: list[dict[str, object]],
    extracted_dir: Path,
) -> Path | None:
    """Save an off-Git stratified 2x4 visual QC sheet covering blur, exposure, and aspect outliers."""
    active = [r for r in qc_records if not str(r["intake_status"]).startswith("quarantined")]
    if not active:
        return None

    picks: list[tuple[str, dict[str, object]]] = []
    by_blur = sorted(active, key=lambda r: float(r["laplacian_var"]))
    by_mean = sorted(active, key=lambda r: float(r["mean_luma"]))
    by_ar = sorted(active, key=lambda r: abs(float(r["aspect_ratio"]) - 2.0), reverse=True)
    picks.append(("blurriest_1", by_blur[0]))
    picks.append(("sharpest_1", by_blur[-1]))
    picks.append(("darkest_1", by_mean[0]))
    picks.append(("brightest_1", by_mean[-1]))
    picks.append(("ar_outlier_1", by_ar[0]))
    picks.append(("median_quality_1", by_blur[len(by_blur) // 2]))

    # Include non-grayscale-RGB sample if any exists, else 25th percentile
    tinted = [r for r in active if not bool(r["is_grayscale_identical_rgb"])]
    picks.append(("tinted_rgb_1" if tinted else "p25_blur_1", tinted[0] if tinted else by_blur[len(by_blur) // 4]))
    exif_hit = [r for r in active if list(r["sensitive_exif_keys"])]
    picks.append(("exif_sample_1" if exif_hit else "p75_blur_1", exif_hit[0] if exif_hit else by_blur[(3 * len(by_blur)) // 4]))

    tile_w, tile_h = 480, 260
    cols, rows = 2, 4
    canvas = np.zeros((rows * tile_h, cols * tile_w, 3), dtype=np.uint8)
    for idx, (tag, rec) in enumerate(picks[:8]):
        img_path = extracted_dir / str(rec["relpath"])
        img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
        if img is None:
            continue
        resized = cv2.resize(img, (tile_w, tile_h), interpolation=cv2.INTER_AREA)
        r_idx, c_idx = divmod(idx, cols)
        y0, x0 = r_idx * tile_h, c_idx * tile_w
        canvas[y0 : y0 + tile_h, x0 : x0 + tile_w] = resized
        label = (
            f"{rec['image_id']} [{tag}] {rec['width']}x{rec['height']} "
            f"lap={rec['laplacian_var']} mu={rec['mean_luma']}"
        )
        cv2.rectangle(canvas, (x0, y0), (x0 + tile_w, y0 + 26), (0, 0, 0), -1)
        cv2.putText(canvas, label[:60], (x0 + 6, y0 + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.43, (0, 255, 255), 1, cv2.LINE_AA)

    QC_SAMPLE_ROOT.mkdir(parents=True, exist_ok=True)
    out_path = QC_SAMPLE_ROOT / f"{dataset_id}_qc_sheet.jpg"
    cv2.imwrite(str(out_path), canvas)
    return out_path


def run_dataset_qc(dataset_id: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Execute full read-only STEP-013 QC audit on one dataset and persist JSON/restricted CSVs."""
    manifest_rows = _load_manifest(dataset_id)
    linkage = _load_linkage(dataset_id)
    extracted_dir = RAW_ROOT / dataset_id / "extracted"

    # Decide which rows to inspect: all active rows PLUS classification_branch (DS0003) & unannotated extras (DS0005)
    target_rows = [
        r
        for r in manifest_rows
        if (
            not r["intake_status"].startswith("quarantined")
            or r["source_bucket"] in {"classification_branch", "unannotated_extra_in_dataset"}
        )
    ]

    def _inspect_one(row: dict[str, str]) -> dict[str, object]:
        img_id = row["ImageID"]
        relpath = linkage[img_id]
        rec = inspect_image_qc(img_id, extracted_dir / relpath, relpath, row["source_bucket"], row["sha256"])
        return {
            "image_id": rec.image_id,
            "relpath": rec.relpath,
            "source_bucket": rec.source_bucket,
            "intake_status": row["intake_status"],
            "sha256": rec.sha256,
            "dhash64": rec.dhash64,
            "width": rec.width,
            "height": rec.height,
            "aspect_ratio": rec.aspect_ratio,
            "mode": rec.mode,
            "is_grayscale_identical_rgb": rec.is_grayscale_identical_rgb,
            "mean_luma": rec.mean_luma,
            "std_luma": rec.std_luma,
            "p05_luma": rec.p05_luma,
            "p95_luma": rec.p95_luma,
            "pct_black_le_3": rec.pct_black_le_3,
            "pct_white_ge_252": rec.pct_white_ge_252,
            "laplacian_var": rec.laplacian_var,
            "exif_tag_count": rec.exif_tag_count,
            "sensitive_exif_keys": list(rec.sensitive_exif_keys),
            "png_text_keys": list(rec.png_text_keys),
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        qc_records = list(pool.map(_inspect_one, target_rows))

    # Write restricted QC CSV (ignored by git via *_restricted*)
    restricted_qc_path = MANIFEST_ROOT / f"{dataset_id}_restricted_qc.csv"
    qc_fields = [k for k in qc_records[0].keys()] if qc_records else []
    with restricted_qc_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=qc_fields)
        writer.writeheader()
        for r in qc_records:
            row_copy = dict(r)
            row_copy["sensitive_exif_keys"] = ";".join(r["sensitive_exif_keys"])
            row_copy["png_text_keys"] = ";".join(r["png_text_keys"])
            writer.writerow(row_copy)

    active_qc = [r for r in qc_records if not str(r["intake_status"]).startswith("quarantined")]
    near_dups = find_near_duplicate_pairs(
        [(str(r["image_id"]), str(r["sha256"]), str(r["dhash64"]), str(r["source_bucket"])) for r in active_qc],
        max_hamming=4,
    )
    restricted_dups_path = MANIFEST_ROOT / f"{dataset_id}_restricted_dups.csv"
    with restricted_dups_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id_a", "id_b", "bucket_a", "bucket_b", "same_sha256", "hamming", "dhash_a", "dhash_b"],
        )
        writer.writeheader()
        writer.writerows(near_dups)

    non_exact_near_dups = [p for p in near_dups if not p["same_sha256"]]
    exact_dups = [p for p in near_dups if p["same_sha256"]]
    dup_cross_bucket_near = dict(
        Counter(tuple(sorted((str(p["bucket_a"]), str(p["bucket_b"])))) for p in non_exact_near_dups)
    )

    # Privacy / metadata summary
    exif_key_freq: Counter[str] = Counter()
    png_key_freq: Counter[str] = Counter()
    for r in active_qc:
        for k in r["sensitive_exif_keys"]:
            exif_key_freq[str(k)] += 1
        for k in r["png_text_keys"]:
            png_key_freq[str(k)] += 1

    ar_outliers = sum(1 for r in active_qc if float(r["aspect_ratio"]) < 1.3 or float(r["aspect_ratio"]) > 2.8)
    tinted_count = sum(1 for r in active_qc if not bool(r["is_grayscale_identical_rgb"]))
    low_res_lt800 = sum(1 for r in active_qc if int(r["width"]) < 800)

    sheet_path = _save_qc_contact_sheet(dataset_id, qc_records, extracted_dir)

    extra_audit: dict[str, object] = {}
    if dataset_id == "DS0001":
        extra_audit = _audit_ds0001_labels(extracted_dir)
    elif dataset_id == "DS0002":
        extra_audit = _audit_ds0002_coco(extracted_dir, manifest_rows)
    elif dataset_id == "DS0003":
        extra_audit = _audit_ds0003_labels_and_branch(extracted_dir, qc_records)
    elif dataset_id == "DS0004":
        extra_audit = _audit_ds0004_xml(extracted_dir, manifest_rows, linkage, active_qc)
    elif dataset_id == "DS0005":
        extra_audit = _audit_ds0005_csv(extracted_dir, qc_records)
    elif dataset_id == "DS0006":
        extra_audit = _audit_ds0006_json(extracted_dir)

    summary = {
        "dataset_id": dataset_id,
        "active_inspected_count": len(active_qc),
        "total_qc_scanned_with_branches": len(qc_records),
        "widths": _quantile_summary([float(r["width"]) for r in active_qc]),
        "heights": _quantile_summary([float(r["height"]) for r in active_qc]),
        "aspect_ratios": _quantile_summary([float(r["aspect_ratio"]) for r in active_qc]),
        "aspect_ratio_outliers_lt1.3_or_gt2.8": ar_outliers,
        "low_res_width_lt800": low_res_lt800,
        "non_identical_rgb_tint_count": tinted_count,
        "mean_luma": _quantile_summary([float(r["mean_luma"]) for r in active_qc]),
        "std_luma": _quantile_summary([float(r["std_luma"]) for r in active_qc]),
        "pct_black_le_3": _quantile_summary([float(r["pct_black_le_3"]) for r in active_qc]),
        "pct_white_ge_252": _quantile_summary([float(r["pct_white_ge_252"]) for r in active_qc]),
        "laplacian_var": _quantile_summary([float(r["laplacian_var"]) for r in active_qc]),
        "exif_images_with_sensitive_tags": sum(1 for r in active_qc if r["sensitive_exif_keys"]),
        "sensitive_exif_key_counts": dict(exif_key_freq),
        "png_text_key_counts": dict(png_key_freq),
        "exact_sha256_pairs_in_active": len(exact_dups),
        "near_dup_hamming_le4_non_exact_pairs": len(non_exact_near_dups),
        "near_dup_bucket_pairs": {f"{k[0]}<->{k[1]}": v for k, v in dup_cross_bucket_near.items()},
        "qc_contact_sheet_offgit": sheet_path.relative_to(ROOT).as_posix() if sheet_path else None,
        "label_and_branch_audit": extra_audit,
    }
    summary_path = MANIFEST_ROOT / f"{dataset_id}_qc_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary, active_qc


def main() -> int:
    parser = argparse.ArgumentParser(description="Run STEP-013 read-only QC and cross-cohort duplicate audit.")
    parser.add_argument("--datasets", nargs="+", required=True, help="DatasetIDs to audit.")
    args = parser.parse_args()

    all_active_pool: list[tuple[str, str, str, str]] = []
    for ds_id in args.datasets:
        summary, _ = run_dataset_qc(ds_id)
        print(
            f"[QC {ds_id}] active={summary['active_inspected_count']}, "
            f"exif_sensitive={summary['exif_images_with_sensitive_tags']}, "
            f"exact_dup_pairs={summary['exact_sha256_pairs_in_active']}, "
            f"near_dup_pairs(H<=4)={summary['near_dup_hamming_le4_non_exact_pairs']}, "
            f"tinted_rgb={summary['non_identical_rgb_tint_count']}, "
            f"ar_outliers={summary['aspect_ratio_outliers_lt1.3_or_gt2.8']}",
            flush=True,
        )

    # Load ALL existing DS####_restricted_qc.csv files so cross-cohort check covers all cohorts together
    screened_ds: list[str] = []
    for ds_id in ("DS0001", "DS0002", "DS0003", "DS0004", "DS0005", "DS0006"):
        qc_csv = MANIFEST_ROOT / f"{ds_id}_restricted_qc.csv"
        if qc_csv.is_file():
            screened_ds.append(ds_id)
            with qc_csv.open("r", encoding="utf-8", newline="") as handle:
                for r in csv.DictReader(handle):
                    if not r["intake_status"].startswith("quarantined"):
                        all_active_pool.append((r["image_id"], r["sha256"], r["dhash64"], ds_id))

    # Cross-dataset exact & near-duplicate screen across all inspected cohorts
    cross_pairs = find_near_duplicate_pairs(all_active_pool, max_hamming=4)
    cross_diff_ds = [p for p in cross_pairs if p["bucket_a"] != p["bucket_b"]]
    exact_cross = [p for p in cross_diff_ds if p["same_sha256"]]
    cross_out = MANIFEST_ROOT / "cross_dataset_dup_summary.json"
    cross_out.write_text(
        json.dumps(
            {
                "datasets_screened": screened_ds,
                "total_active_images_screened": len(all_active_pool),
                "cross_dataset_exact_sha256_count": len(exact_cross),
                "cross_dataset_matches_count": len(cross_diff_ds),
                "cross_dataset_matches_preview": cross_diff_ds[:100],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"[CROSS-COHORT DUP CHECK ({','.join(screened_ds)})] "
        f"total={len(all_active_pool)}, exact={len(exact_cross)}, dHash<=4={len(cross_diff_ds)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
