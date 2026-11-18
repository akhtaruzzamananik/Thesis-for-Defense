"""Execute STEP-016 60-OPG stratified annotation pilot, overlay rendering, and two-pass QA audit."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_pilot import (  # noqa: E402
    DATASET_TRACK_MAP,
    EXPECTED_CLASSES_CSV_SHA256,
    ImageAnnotationRecord,
    audit_box_list,
    compute_cohens_kappa_binary,
    independent_second_pass_verify,
    select_stratified_pilot_sample,
)
from opg.annotation_schema import (  # noqa: E402
    DS0004_NAME_TO_TRACKD,
    DS0005_NAME_TO_TRACKE,
    DS0006_LABEL_TO_TRACKF,
    coco_xywh_to_xyxy,
    compute_class_map_sha256,
    obb_to_aabb_xyxy,
    polygon_to_aabb_xyxy,
    remap_ds0001_class,
    yolo_norm_to_xyxy,
)

RAW_ROOT = ROOT / "03_Datasets" / "raw"
MANIFEST_ROOT = ROOT / "03_Datasets" / "manifests"
ANN_ROOT = ROOT / "04_Annotations"


def _load_linkage(dataset_id: str) -> dict[str, str]:
    path = MANIFEST_ROOT / f"{dataset_id}_restricted_linkage.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["ImageID"]: row["original_relpath"] for row in csv.DictReader(handle)}


def _load_laplacian_map(dataset_id: str) -> dict[str, float]:
    path = MANIFEST_ROOT / f"{dataset_id}_restricted_qc.csv"
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["image_id"]: float(row.get("laplacian_var", 0.0) or 0.0) for row in csv.DictReader(handle)}


def _load_active_manifest(dataset_id: str) -> list[dict[str, str]]:
    path = MANIFEST_ROOT / f"{dataset_id}_images.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [r for r in csv.DictReader(handle) if not r["intake_status"].startswith("quarantined")]


def parse_all_active_records(dataset_id: str) -> list[ImageAnnotationRecord]:
    """Parse all active images in a dataset into ImageAnnotationRecord instances."""
    extracted = RAW_ROOT / dataset_id / "extracted"
    linkage = _load_linkage(dataset_id)
    lap_map = _load_laplacian_map(dataset_id)
    active_rows = _load_active_manifest(dataset_id)
    track_id = DATASET_TRACK_MAP[dataset_id]

    # Pre-index dataset-wide annotation containers for DS0002 (COCO) and DS0005 (CSV)
    coco_by_filename: dict[str, list[dict[str, Any]]] = defaultdict(list)
    coco_cat3_names: dict[int, str] = {}
    if dataset_id == "DS0002":
        jpath = (
            extracted
            / "training_data"
            / "training_data"
            / "quadrant-enumeration-disease"
            / "train_quadrant_enumeration_disease.json"
        )
        data = json.loads(jpath.read_text(encoding="utf-8"))
        coco_cat3_names = {int(c["id"]): str(c["name"]) for c in data.get("categories_3", [])}
        id_to_fname = {int(im["id"]): str(im["file_name"]) for im in data.get("images", [])}
        for ann in data.get("annotations", []):
            fn = id_to_fname.get(int(ann["image_id"]), "")
            if fn:
                coco_by_filename[fn].append(ann)

    au_by_filename: dict[str, list[dict[str, str]]] = defaultdict(list)
    if dataset_id == "DS0005":
        for fn in ("train_annotations.csv", "val_annotations.csv", "test_annotations.csv"):
            with (extracted / fn).open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    au_by_filename[row["image"].strip()].append(row)

    records: list[ImageAnnotationRecord] = []
    for row in active_rows:
        image_id = row["ImageID"]
        rel = linkage[image_id]
        w = int(row["width"])
        h = int(row["height"])
        bucket = row["source_bucket"]
        lap = lap_map.get(image_id, 0.0)

        raw_items: list[tuple[int | None, str, float, float, float, float, str]] = []
        state = "reviewed_positive"

        if dataset_id == "DS0001":
            img_p = extracted / rel
            lbl_p = img_p.parent.parent / "labels" / f"{img_p.stem}.txt"
            if not lbl_p.is_file():
                state = "missing_labels"
            else:
                lines = [ln.strip() for ln in lbl_p.read_text(encoding="utf-8").splitlines() if ln.strip()]
                if not lines:
                    state = "reviewed_empty"
                for ln in lines:
                    parts = ln.split()
                    scid = int(float(parts[0]))
                    xc, yc, bw, bh = (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
                    x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, w, h)
                    mapped = remap_ds0001_class(scid)
                    hint = "excluded_class" if mapped is None else "ok"
                    raw_items.append((mapped, f"DS0001_src_{scid}", x0, y0, x1, y1, hint))

        elif dataset_id == "DS0002":
            if bucket == "validation_quadrant_enumeration_disease_no_gt":
                state = "missing_labels"
            else:
                fname = Path(rel).name
                anns = coco_by_filename.get(fname, [])
                if not anns:
                    state = "reviewed_empty"
                for ann in anns:
                    cid = int(ann["category_id_3"])
                    cname = coco_cat3_names.get(cid, str(cid))
                    x0, y0, x1, y1 = coco_xywh_to_xyxy(*ann["bbox"])
                    raw_items.append((cid, cname, x0, y0, x1, y1, "ok"))

        elif dataset_id == "DS0003":
            img_p = extracted / rel
            lbl_p = img_p.with_suffix(".txt")
            if not lbl_p.is_file():
                state = "missing_labels"
            else:
                lines = [ln.strip() for ln in lbl_p.read_text(encoding="utf-8").splitlines() if ln.strip()]
                if not lines:
                    state = "reviewed_empty"
                for ln in lines:
                    parts = ln.split()
                    cid = int(float(parts[0]))
                    xc, yc, bw, bh = (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
                    x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, w, h)
                    raw_items.append((cid, f"DS0003_cls_{cid}", x0, y0, x1, y1, "ok"))

        elif dataset_id == "DS0004":
            stem = Path(rel).stem
            xml_p = (
                extracted
                / "Panoramic radiographs with periapical lesions Dataset"
                / "Periapical Dataset"
                / "Periapical Lesions"
                / "Image Annots"
                / f"{stem}.xml"
            )
            if not xml_p.is_file():
                state = "missing_labels"
            else:
                rxml = ET.parse(xml_p).getroot()
                objs = rxml.findall("object")
                if not objs:
                    state = "reviewed_empty"
                for obj in objs:
                    name = str(obj.findtext("name", "")).strip()
                    cid = DS0004_NAME_TO_TRACKD[name]
                    bb = obj.find("bndbox")
                    assert bb is not None
                    x0 = float(bb.findtext("xmin", "0"))
                    y0 = float(bb.findtext("ymin", "0"))
                    x1 = float(bb.findtext("xmax", "0"))
                    y1 = float(bb.findtext("ymax", "0"))
                    raw_items.append((cid, f"PAI_{name}", x0, y0, x1, y1, "ok"))

        elif dataset_id == "DS0005":
            fname = Path(rel).name
            rows = au_by_filename.get(fname, [])
            if not rows:
                state = "missing_labels"
            else:
                for r5 in rows:
                    cond = r5["condition"].strip()
                    cid = DS0005_NAME_TO_TRACKE[cond]
                    x0, y0, x1, y1 = obb_to_aabb_xyxy(
                        float(r5["x"]),
                        float(r5["y"]),
                        float(r5["width"]),
                        float(r5["height"]),
                        float(r5["rotation"]),
                        w,
                        h,
                        coords_are_percent=True,
                        pivot="top_left",
                        clip=False,
                    )
                    raw_items.append((cid, cond, x0, y0, x1, y1, "ok"))

        elif dataset_id == "DS0006":
            img_p = extracted / rel
            json_name = img_p.stem.replace("_opg_", "_Ann_") + ".json"
            jp = img_p.parent.parent / "OPG_Annotation" / json_name
            if not jp.is_file():
                state = "missing_labels"
            else:
                jdata = json.loads(jp.read_text(encoding="utf-8"))
                shapes = jdata.get("shapes", [])
                if not shapes:
                    state = "reviewed_empty"
                for sh in shapes:
                    lbl = str(sh.get("label", "")).strip()
                    pts = sh.get("points", [])
                    mapped = DS0006_LABEL_TO_TRACKF.get(lbl)
                    if not pts:
                        raw_items.append((mapped or 0, lbl, 0.0, 0.0, 0.0, 0.0, "ok"))
                        continue
                    x0, y0, x1, y1 = polygon_to_aabb_xyxy(pts, img_w=None, img_h=None)
                    hint = "excluded_roi" if mapped is None else "ok"
                    raw_items.append((mapped, f"MD_OPG_{lbl}", x0, y0, x1, y1, hint))

        valid_boxes, excluded, anomalies = audit_box_list(image_id, dataset_id, w, h, raw_items)
        if state == "reviewed_positive" and len(valid_boxes) == 0:
            state = "reviewed_empty"

        records.append(
            ImageAnnotationRecord(
                image_id=image_id,
                dataset_id=dataset_id,
                track_id=track_id,
                source_bucket=bucket,
                width=w,
                height=h,
                laplacian_var=lap,
                annotation_state=state,
                raw_box_count=len(raw_items),
                valid_boxes=valid_boxes,
                excluded_records=excluded,
                anomalies=anomalies,
            )
        )

    return records


def render_pilot_overlay_sheet(
    dataset_id: str,
    pilot_records: list[ImageAnnotationRecord],
    linkage: dict[str, str],
    out_path: Path,
) -> None:
    """Render a 2x5 visual overlay sheet of the 10 pilot OPGs with canonical bounding boxes."""
    extracted = RAW_ROOT / dataset_id / "extracted"
    tile_w, tile_h = 480, 260
    cols, rows = 2, 5
    canvas = np.full((rows * tile_h, cols * tile_w, 3), 24, dtype=np.uint8)
    palette = [
        (0, 255, 128),
        (0, 200, 255),
        (255, 180, 0),
        (255, 80, 180),
        (120, 255, 255),
        (80, 160, 255),
        (180, 255, 80),
    ]

    for idx, rec in enumerate(pilot_records[:10]):
        r_idx = idx // cols
        c_idx = idx % cols
        img_path = extracted / linkage[rec.image_id]
        raw_bytes = np.fromfile(str(img_path), dtype=np.uint8)
        img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
        if img is None:
            continue
        sx = tile_w / float(rec.width)
        sy = tile_h / float(rec.height)
        resized = cv2.resize(img, (tile_w, tile_h), interpolation=cv2.INTER_AREA)

        for b in rec.valid_boxes:
            color = palette[b.class_id % len(palette)]
            x0 = int(round(b.xmin * sx))
            y0 = int(round(b.ymin * sy))
            x1 = int(round(b.xmax * sx))
            y1 = int(round(b.ymax * sy))
            cv2.rectangle(resized, (x0, y0), (x1, y1), color, 1)
            cv2.putText(
                resized,
                str(b.class_id),
                (x0 + 1, max(10, y0 - 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.33,
                color,
                1,
                cv2.LINE_AA,
            )

        banner = f"{rec.image_id} | {rec.stratum[:12]} | boxes={len(rec.valid_boxes)}"
        cv2.rectangle(resized, (0, 0), (tile_w, 18), (0, 0, 0), -1)
        cv2.putText(
            resized,
            banner,
            (4, 13),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.36,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        y_off = r_idx * tile_h
        x_off = c_idx * tile_w
        canvas[y_off : y_off + tile_h, x_off : x_off + tile_w] = resized

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def main() -> None:
    classes_csv = ANN_ROOT / "classes.csv"
    actual_sha = compute_class_map_sha256(classes_csv)
    if actual_sha != EXPECTED_CLASSES_CSV_SHA256:
        raise RuntimeError(f"classes.csv hash mismatch: {actual_sha} != {EXPECTED_CLASSES_CSV_SHA256}")

    pilot_native_root = ANN_ROOT / "native" / "pilot_STEP-016"
    pilot_export_root = ANN_ROOT / "exports" / "pilot_STEP-016"
    overlay_root = pilot_export_root / "overlays"
    adjudication_dir = ANN_ROOT / "adjudications"
    review_dir = ANN_ROOT / "reviews"
    for d in (pilot_native_root, pilot_export_root, overlay_root, adjudication_dir, review_dir):
        d.mkdir(parents=True, exist_ok=True)

    summary_by_ds: dict[str, Any] = {}
    all_disp_a: list[int] = []
    all_disp_b: list[int] = []
    all_adjudications: list[dict[str, Any]] = []
    total_pilot_images = 0
    total_pilot_valid_boxes = 0
    total_pilot_excluded = 0
    max_pilot_rt_err = 0.0

    for ds_id in ("DS0001", "DS0002", "DS0003", "DS0004", "DS0005", "DS0006"):
        linkage = _load_linkage(ds_id)
        records = parse_all_active_records(ds_id)
        pilot_sample = select_stratified_pilot_sample(records, n_total=10, seed=20261119)

        ds_native_dir = pilot_native_root / ds_id
        ds_export_dir = pilot_export_root / ds_id
        ds_native_dir.mkdir(parents=True, exist_ok=True)
        ds_export_dir.mkdir(parents=True, exist_ok=True)

        ds_disp_a: list[int] = []
        ds_disp_b: list[int] = []
        ds_matched_boxes = 0
        ds_total_boxes = 0
        ds_ious: list[float] = []
        ds_max_rt_err = 0.0
        ds_excluded = 0
        ds_anomalies: list[dict[str, Any]] = []
        stratum_counts: Counter[str] = Counter()
        class_counts: Counter[int] = Counter()

        for rec in pilot_sample:
            total_pilot_images += 1
            stratum_counts[rec.stratum] += 1
            ds_excluded += len(rec.excluded_records)
            total_pilot_excluded += len(rec.excluded_records)

            # Save restricted native audit snapshot
            native_payload = {
                "image_id": rec.image_id,
                "dataset_id": rec.dataset_id,
                "track_id": rec.track_id,
                "stratum": rec.stratum,
                "width": rec.width,
                "height": rec.height,
                "raw_box_count": rec.raw_box_count,
                "valid_box_count": len(rec.valid_boxes),
                "excluded_records": rec.excluded_records,
                "anomalies": rec.anomalies,
            }
            (ds_native_dir / f"{rec.image_id}_native.json").write_text(
                json.dumps(native_payload, indent=2), encoding="utf-8"
            )

            # Save canonical YOLO .txt export
            yolo_txt = "\n".join(b.yolo_line for b in rec.valid_boxes)
            if yolo_txt:
                yolo_txt += "\n"
            (ds_export_dir / f"{rec.image_id}.txt").write_text(yolo_txt, encoding="utf-8")

            for b in rec.valid_boxes:
                class_counts[b.class_id] += 1
                ds_max_rt_err = max(ds_max_rt_err, b.round_trip_px_err)
                max_pilot_rt_err = max(max_pilot_rt_err, b.round_trip_px_err)

            v_res = independent_second_pass_verify(rec)
            m_res = v_res["match_res"]
            ds_matched_boxes += int(m_res["matched"])
            ds_total_boxes += len(rec.valid_boxes)
            total_pilot_valid_boxes += len(rec.valid_boxes)
            if int(m_res["matched"]) > 0:
                ds_ious.append(float(m_res["mean_iou"]))

            ds_disp_a.extend(v_res["dispositions_a"])
            ds_disp_b.extend(v_res["dispositions_b"])
            all_disp_a.extend(v_res["dispositions_a"])
            all_disp_b.extend(v_res["dispositions_b"])

            for anom in rec.anomalies:
                ds_anomalies.append(anom)
                all_adjudications.append(anom)

        overlay_path = overlay_root / f"{ds_id}_pilot_overlay.jpg"
        render_pilot_overlay_sheet(ds_id, pilot_sample, linkage, overlay_path)
        kappa_ds = compute_cohens_kappa_binary(ds_disp_a, ds_disp_b)

        summary_by_ds[ds_id] = {
            "track_id": DATASET_TRACK_MAP[ds_id],
            "pilot_images": len(pilot_sample),
            "pilot_image_ids": [r.image_id for r in pilot_sample],
            "strata": dict(stratum_counts),
            "valid_boxes": ds_total_boxes,
            "excluded_items": ds_excluded,
            "class_distribution": {str(k): v for k, v in sorted(class_counts.items())},
            "matched_boxes_passA_vs_passB": ds_matched_boxes,
            "f1_box_agreement": round(
                (2.0 * ds_matched_boxes / (2 * ds_total_boxes)) if ds_total_boxes > 0 else 1.0, 4
            ),
            "mean_matched_iou": round(float(np.mean(ds_ious)) if ds_ious else 1.0, 6),
            "max_round_trip_px_err": round(ds_max_rt_err, 6),
            "disposition_agreement": kappa_ds,
            "anomalies_flagged_and_adjudicated": len(ds_anomalies),
            "overlay_sheet_offgit": f"04_Annotations/exports/pilot_STEP-016/overlays/{ds_id}_pilot_overlay.jpg",
        }

    overall_kappa = compute_cohens_kappa_binary(all_disp_a, all_disp_b)
    # Write adjudication CSV
    adj_csv_path = adjudication_dir / "pilot_STEP-016_adjudications.csv"
    with adj_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["dataset_id", "image_id", "box_index", "source_label", "issue_type", "detail", "resolution"],
        )
        writer.writeheader()
        for item in all_adjudications:
            writer.writerow(
                {
                    "dataset_id": item.get("dataset_id", ""),
                    "image_id": item.get("image_id", ""),
                    "box_index": item.get("box_index", ""),
                    "source_label": item.get("source_label", ""),
                    "issue_type": item.get("issue_type", ""),
                    "detail": item.get("detail", ""),
                    "resolution": item.get("resolution", ""),
                }
            )

    overall_summary = {
        "step": "STEP-016",
        "protocol_version": "v1.0.0",
        "classes_csv_sha256": actual_sha,
        "seed": 20261119,
        "total_pilot_images": total_pilot_images,
        "total_pilot_valid_boxes": total_pilot_valid_boxes,
        "total_pilot_excluded_items": total_pilot_excluded,
        "max_round_trip_px_err": round(max_pilot_rt_err, 6),
        "overall_disposition_agreement": overall_kappa,
        "total_anomalies_adjudicated": len(all_adjudications),
        "datasets": summary_by_ds,
    }
    out_json = review_dir / "pilot_STEP-016_summary.json"
    out_json.write_text(json.dumps(overall_summary, indent=2), encoding="utf-8")
    print(
        f"PILOT_DONE: images={total_pilot_images}, valid_boxes={total_pilot_valid_boxes}, "
        f"excluded={total_pilot_excluded}, anomalies={len(all_adjudications)}, "
        f"max_rt_err={max_pilot_rt_err:.6f}px, agreement={overall_kappa['agreement_pct']}%, "
        f"kappa={overall_kappa['kappa']}"
    )


if __name__ == "__main__":
    main()
