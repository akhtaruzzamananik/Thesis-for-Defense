"""Whole-release annotation integrity, correspondence, and hash audit for STEP-018 (G06)."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_pilot import EXPECTED_CLASSES_CSV_SHA256  # noqa: E402
from opg.annotation_schema import box_iou_xyxy, compute_class_map_sha256, parse_yolo_line, yolo_norm_to_xyxy  # noqa: E402

ALLOWED_TRACK_CLASSES: dict[str, set[int]] = {
    "TrackA": set(range(13)),
    "TrackB": set(range(4)),
    "TrackC": set(range(6)),
    "TrackD": set(range(3)),
    "TrackE": set(range(6)),
    "TrackF": set(range(2)),
}


def _sha256_normalized(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def verify_whole_annotation_release(root: Path = ROOT) -> dict[str, Any]:
    """Audit ANN0001-ANN0006 in annotation_registry.csv against on-disk manifests and exported .txt files."""
    ann_root = root / "04_Annotations"
    ds_manifest_root = root / "03_Datasets" / "manifests"
    classes_sha = compute_class_map_sha256(ann_root / "classes.csv")
    if classes_sha != EXPECTED_CLASSES_CSV_SHA256:
        raise RuntimeError(f"ClassMapHash mismatch: {classes_sha} != {EXPECTED_CLASSES_CSV_SHA256}")

    reg_path = ann_root / "annotation_registry.csv"
    with reg_path.open("r", encoding="utf-8", newline="") as handle:
        reg_rows = list(csv.DictReader(handle))

    if len(reg_rows) != 6:
        raise RuntimeError(f"Expected 6 ANN release rows in annotation_registry.csv, found {len(reg_rows)}")

    release_results: dict[str, Any] = {}
    total_exported_files = 0
    total_verified_boxes = 0
    total_empty_files = 0
    total_orphan_labels = 0
    total_invalid_lines = 0
    total_remaining_dups = 0

    for row in reg_rows:
        ann_id = row["AnnotationID"].strip()
        ds_id = row["DatasetID"].strip()
        batch_id = row["BatchIDs"].strip()
        if row["ClassMapHash"].strip() != classes_sha:
            raise RuntimeError(f"{ann_id} ClassMapHash mismatch in registry")

        # Load active images for ds_id
        with (ds_manifest_root / f"{ds_id}_images.csv").open("r", encoding="utf-8", newline="") as h_img:
            active_dims = {
                r["ImageID"]: (int(r["width"]), int(r["height"]))
                for r in csv.DictReader(h_img)
                if not r["intake_status"].startswith("quarantined")
            }

        native_inv = ann_root / "native" / f"{batch_id}_{ds_id}" / "batch_native_inventory.json"
        actual_native_sha = _sha256_normalized(native_inv)
        if actual_native_sha != row["NativeHash"].strip():
            raise RuntimeError(f"{ann_id} NativeHash mismatch: {actual_native_sha} != {row['NativeHash']}")

        # Find export folder
        export_dirs = list((ann_root / "exports").glob(f"{batch_id}_*"))
        if len(export_dirs) != 1:
            raise RuntimeError(f"Expected 1 export folder for {batch_id}, found {export_dirs}")
        export_dir = export_dirs[0]
        track_id = export_dir.name.split("_", 1)[1]
        allowed_cids = ALLOWED_TRACK_CLASSES[track_id]

        export_man = export_dir / "export_manifest.csv"
        actual_export_sha = _sha256_normalized(export_man)
        if actual_export_sha != row["ExportHash"].strip():
            raise RuntimeError(f"{ann_id} ExportHash mismatch: {actual_export_sha} != {row['ExportHash']}")

        with export_man.open("r", encoding="utf-8", newline="") as h_exp:
            exp_rows = list(csv.DictReader(h_exp))

        ds_boxes = 0
        ds_empty = 0
        ds_orphans = 0
        ds_invalid = 0
        ds_dups = 0

        for erow in exp_rows:
            img_id = erow["ImageID"]
            if img_id not in active_dims:
                ds_orphans += 1
                continue
            w, h = active_dims[img_id]
            txt_p = export_dir / erow["LabelRelPath"]
            if not txt_p.is_file():
                raise RuntimeError(f"Missing exported label file: {txt_p}")
            raw_bytes = txt_p.read_bytes()
            sha = hashlib.sha256(raw_bytes).hexdigest()
            if sha != erow["LabelSHA256"]:
                raise RuntimeError(f"Label file SHA-256 mismatch for {img_id}: {sha} != {erow['LabelSHA256']}")

            lines = [ln.strip() for ln in raw_bytes.decode("utf-8").splitlines() if ln.strip()]
            if not lines:
                ds_empty += 1
            parsed_xyxy: list[tuple[int, list[float]]] = []
            for ln in lines:
                try:
                    cid, xc, yc, bw, bh = parse_yolo_line(ln)
                except ValueError:
                    ds_invalid += 1
                    continue
                if cid not in allowed_cids:
                    ds_invalid += 1
                x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, w, h)
                if (x1 - x0) * (y1 - y0) <= 1.0:
                    ds_invalid += 1
                parsed_xyxy.append((cid, [x0, y0, x1, y1]))
                ds_boxes += 1

            for i in range(len(parsed_xyxy)):
                for j in range(i + 1, len(parsed_xyxy)):
                    if parsed_xyxy[i][0] == parsed_xyxy[j][0]:
                        if box_iou_xyxy(parsed_xyxy[i][1], parsed_xyxy[j][1]) > 0.90:
                            ds_dups += 1

        if ds_orphans > 0 or ds_invalid > 0 or ds_dups > 0:
            raise RuntimeError(
                f"{ann_id} integrity failure: orphans={ds_orphans}, invalid={ds_invalid}, dups={ds_dups}"
            )

        release_results[ann_id] = {
            "dataset_id": ds_id,
            "batch_id": batch_id,
            "track_id": track_id,
            "active_images": len(active_dims),
            "exported_files": len(exp_rows),
            "reviewed_empty_files": ds_empty,
            "quarantined_missing_labels": len(active_dims) - len(exp_rows),
            "verified_boxes": ds_boxes,
            "orphan_labels": ds_orphans,
            "invalid_boxes": ds_invalid,
            "remaining_same_class_dups": ds_dups,
            "native_hash_verified": True,
            "export_hash_verified": True,
        }
        total_exported_files += len(exp_rows)
        total_verified_boxes += ds_boxes
        total_empty_files += ds_empty
        total_orphan_labels += ds_orphans
        total_invalid_lines += ds_invalid
        total_remaining_dups += ds_dups

    out = {
        "step": "STEP-018",
        "gate": "G06",
        "protocol_version": "v1.0.0",
        "class_map_sha256": classes_sha,
        "releases_verified": len(release_results),
        "total_exported_files": total_exported_files,
        "total_reviewed_empty_files": total_empty_files,
        "total_verified_boxes": total_verified_boxes,
        "total_orphan_labels": total_orphan_labels,
        "total_invalid_boxes": total_invalid_lines,
        "total_remaining_same_class_dups": total_remaining_dups,
        "releases": release_results,
    }
    (ann_root / "reviews" / "release_STEP-018_verification.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    return out


if __name__ == "__main__":
    res = verify_whole_annotation_release()
    print(
        f"RELEASE_AUDIT_OK: releases={res['releases_verified']}, files={res['total_exported_files']}, "
        f"empty={res['total_reviewed_empty_files']}, boxes={res['total_verified_boxes']}, "
        f"orphans={res['total_orphan_labels']}, invalid={res['total_invalid_boxes']}, "
        f"remaining_dups={res['total_remaining_same_class_dups']}"
    )
