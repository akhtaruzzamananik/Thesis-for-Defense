"""Locked dataset/split loader, T14 experiment config validator, and Kaggle bundle exporter (STEP-025)."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np
import yaml

from opg.annotation_pilot import EXPECTED_CLASSES_CSV_SHA256
from opg.annotation_schema import compute_class_map_sha256, parse_yolo_line, yolo_norm_to_xyxy
from opg.preprocessing import compute_config_sha256, load_and_validate_pp_yaml, prepare_image_and_boxes


@dataclass(frozen=True)
class PartitionItem:
    """Single verified active_canonical image record from a locked SPLIT#### manifest."""

    image_id: str
    dataset_id: str
    split_id: str
    group_id: str
    partition: str
    sha256: str
    width: int
    height: int
    raw_relpath: str
    label_relpath: str


def _sha256_normalized(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def _is_g11_passed(root: Path) -> bool:
    gates_csv = root / "01_Project_Management" / "gates.csv"
    if not gates_csv.is_file():
        return False
    with gates_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("GateID", "").strip() == "G11":
                return row.get("Outcome", "").strip().upper() == "PASS"
    return False


def _assert_no_nulls(obj: Any, prefix: str = "") -> None:
    """Recursively reject None/null values in a resolved executable T14 configuration."""
    if obj is None:
        raise ValueError(f"Unresolved null value in executable T14 config at {prefix!r}")
    if isinstance(obj, dict):
        for k, v in obj.items():
            nxt = f"{prefix}.{k}" if prefix else str(k)
            _assert_no_nulls(v, nxt)
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            _assert_no_nulls(v, f"{prefix}[{idx}]")


def validate_experiment_config(
    config: dict[str, Any],
    *,
    root: Path | None = None,
    allow_null_operating_conf: bool = True,
) -> None:
    """Validate an executable T14 experiment config; raise ValueError/PermissionError on nulls, hash drift, or test leaks."""
    required_sections = ("identity", "data", "model", "training", "runtime", "evaluation", "outputs")
    for sec in required_sections:
        if sec not in config or not isinstance(config[sec], dict):
            raise ValueError(f"Missing required T14 config section: {sec!r}")

    # Allow parent_comparison_id to be None for root baselines, and operating_conf_threshold before G11
    cfg_check = json.loads(json.dumps(config))
    if cfg_check["identity"].get("parent_comparison_id") is None:
        cfg_check["identity"]["parent_comparison_id"] = "NONE"
    if allow_null_operating_conf and cfg_check["evaluation"].get("operating_conf_threshold") is None:
        cfg_check["evaluation"]["operating_conf_threshold"] = "val_selected_pending_G11"
    _assert_no_nulls(cfg_check)

    # Enforce sealed final-test rule until G11 PASS
    allowed_parts = [str(p).strip() for p in config["data"]["allowed_partitions"]]
    if any(p in ("test", "external_test") for p in allowed_parts):
        if root is None or not _is_g11_passed(root):
            raise PermissionError(
                "SEALED TEST VIOLATION (OS §4.4 / §7.1): 'test'/'external_test' cannot be accessed before G11 PASS."
            )

    # Verify class-map SHA-256
    cls_sha = str(config["data"]["class_map_sha256"]).strip()
    if cls_sha != EXPECTED_CLASSES_CSV_SHA256:
        raise ValueError(f"Class-map SHA-256 mismatch: {cls_sha} != {EXPECTED_CLASSES_CSV_SHA256}")

    if root is not None:
        classes_csv = root / "04_Annotations" / "classes.csv"
        if classes_csv.is_file():
            actual_cls_sha = compute_class_map_sha256(classes_csv)
            if actual_cls_sha != cls_sha:
                raise ValueError(f"On-disk classes.csv SHA-256 mismatch: {actual_cls_sha} != {cls_sha}")


def load_locked_partition_items(
    root: Path,
    *,
    dataset_id: str,
    split_id: str,
    batch_id: str,
    track_id: str,
    partition: str,
    expected_class_map_sha256: str = EXPECTED_CLASSES_CSV_SHA256,
    expected_split_sha256: str | None = None,
    allow_test_partition: bool = False,
) -> list[PartitionItem]:
    """Load active_canonical items for one partition from SPLIT####/manifest.csv with hash & leakage checks."""
    if partition in ("test", "external_test") and not allow_test_partition and not _is_g11_passed(root):
        raise PermissionError(
            f"SEALED TEST VIOLATION: Cannot load partition {partition!r} before G11 PASS."
        )

    classes_csv = root / "04_Annotations" / "classes.csv"
    actual_cls_sha = compute_class_map_sha256(classes_csv)
    if actual_cls_sha != expected_class_map_sha256:
        raise ValueError(f"Class-map SHA-256 mismatch: {actual_cls_sha} != {expected_class_map_sha256}")

    split_man_path = root / "03_Datasets" / "splits" / split_id / "manifest.csv"
    if not split_man_path.is_file():
        raise FileNotFoundError(f"Missing split manifest: {split_man_path}")
    actual_split_sha = _sha256_normalized(split_man_path)
    if expected_split_sha256 is not None and actual_split_sha != expected_split_sha256:
        raise ValueError(f"Split manifest SHA-256 mismatch: {actual_split_sha} != {expected_split_sha256}")

    ds_man_path = root / "03_Datasets" / "manifests" / f"{dataset_id}_images.csv"
    linkage_path = root / "03_Datasets" / "manifests" / f"{dataset_id}_restricted_linkage.csv"
    exp_man_path = root / "04_Annotations" / "exports" / f"{batch_id}_{track_id}" / "export_manifest.csv"

    with ds_man_path.open("r", encoding="utf-8", newline="") as handle:
        ds_dims = {
            r["ImageID"]: (int(r["width"]), int(r["height"]), r["sha256"])
            for r in csv.DictReader(handle)
            if not r["intake_status"].startswith("quarantined")
        }

    with linkage_path.open("r", encoding="utf-8", newline="") as handle:
        linkage = {r["ImageID"]: r["original_relpath"] for r in csv.DictReader(handle)}

    with exp_man_path.open("r", encoding="utf-8", newline="") as handle:
        exp_labels = {r["ImageID"]: r["LabelRelPath"] for r in csv.DictReader(handle)}

    items: list[PartitionItem] = []
    with split_man_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["Partition"].strip() != partition:
                continue
            if row["MemberRole"].strip() != "active_canonical":
                continue
            iid = row["ImageID"].strip()
            w, h, ds_sha = ds_dims[iid]
            if row["SHA256"].strip() != ds_sha:
                raise ValueError(f"Image SHA-256 mismatch for {iid}: {row['SHA256']} != {ds_sha}")
            items.append(
                PartitionItem(
                    image_id=iid,
                    dataset_id=dataset_id,
                    split_id=split_id,
                    group_id=row["GroupID"].strip(),
                    partition=partition,
                    sha256=ds_sha,
                    width=w,
                    height=h,
                    raw_relpath=linkage[iid],
                    label_relpath=exp_labels[iid],
                )
            )
    return items


def export_yolo_dataset_bundle(
    root: Path,
    *,
    dataset_id: str,
    split_id: str,
    batch_id: str,
    track_id: str,
    pp_config_path: Path,
    output_dir: Path,
    class_names: Sequence[str],
    partitions: Sequence[str] = ("train", "val"),
    allow_test_partition: bool = False,
) -> dict[str, Any]:
    """Materialize a Kaggle/Ultralytics-ready dataset directory applying exact PP#### transforms."""
    pp_cfg = load_and_validate_pp_yaml(pp_config_path)
    pp_sha = compute_config_sha256(pp_config_path)
    target_w, target_h = int(pp_cfg["target_size"][0]), int(pp_cfg["target_size"][1])
    preserve_ar = bool(pp_cfg["preserve_aspect_ratio"])
    pad_val = int(pp_cfg["pad_value"])
    autocrop_ds = set(pp_cfg["border_autocrop"].get("enabled_for_datasets", []))
    use_autocrop = dataset_id in autocrop_ds
    ce = pp_cfg["contrast_enhancement"]
    clahe_params = (
        (float(ce["clip_limit"]), (int(ce["tile_grid_size"][0]), int(ce["tile_grid_size"][1])))
        if ce["method"] == "clahe"
        else None
    )

    extracted_dir = root / "03_Datasets" / "raw" / dataset_id / "extracted"
    exp_dir = root / "04_Annotations" / "exports" / f"{batch_id}_{track_id}"

    output_dir.mkdir(parents=True, exist_ok=True)
    part_counts: dict[str, int] = {}

    for part in partitions:
        items = load_locked_partition_items(
            root,
            dataset_id=dataset_id,
            split_id=split_id,
            batch_id=batch_id,
            track_id=track_id,
            partition=part,
            allow_test_partition=allow_test_partition,
        )
        img_out_dir = output_dir / "images" / part
        lbl_out_dir = output_dir / "labels" / part
        img_out_dir.mkdir(parents=True, exist_ok=True)
        lbl_out_dir.mkdir(parents=True, exist_ok=True)

        for it in items:
            raw_b = np.fromfile(str(extracted_dir / it.raw_relpath), dtype=np.uint8)
            im_bgr = cv2.imdecode(raw_b, cv2.IMREAD_COLOR)
            if im_bgr is None:
                raise RuntimeError(f"Failed to decode image {it.image_id}")
            im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)

            lbl_lines = [
                ln.strip()
                for ln in (exp_dir / it.label_relpath).read_text(encoding="utf-8").splitlines()
                if ln.strip()
            ]
            boxes: list[tuple[int, float, float, float, float]] = []
            for ln in lbl_lines:
                cid, xc, yc, bw, bh = parse_yolo_line(ln)
                x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, it.width, it.height)
                boxes.append((cid, x0, y0, x1, y1))

            out_rgb, _, out_yolo_lines, _ = prepare_image_and_boxes(
                im_rgb,
                boxes,
                target_size=(target_w, target_h),
                preserve_aspect_ratio=preserve_ar,
                pad_value=pad_val,
                autocrop_black_border=use_autocrop,
                clahe_params=clahe_params,
            )
            out_bgr = cv2.cvtColor(out_rgb, cv2.COLOR_RGB2BGR)
            # Save clean PNG/JPG without EXIF/XMP metadata
            cv2.imwrite(str(img_out_dir / f"{it.image_id}.jpg"), out_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            lbl_str = "\n".join(out_yolo_lines) + ("\n" if out_yolo_lines else "")
            (lbl_out_dir / f"{it.image_id}.txt").write_text(lbl_str, encoding="utf-8")

        part_counts[part] = len(items)

    # Write Ultralytics dataset.yaml (using relative path to output_dir)
    yaml_payload: dict[str, Any] = {
        "path": str(output_dir.resolve()),
        "train": "images/train" if "train" in partitions else None,
        "val": "images/val" if "val" in partitions else None,
        "nc": len(class_names),
        "names": {idx: name for idx, name in enumerate(class_names)},
    }
    if "test" in partitions and allow_test_partition:
        yaml_payload["test"] = "images/test"
    yaml_payload = {k: v for k, v in yaml_payload.items() if v is not None}
    (output_dir / "dataset.yaml").write_text(yaml.safe_dump(yaml_payload, sort_keys=False), encoding="utf-8")

    manifest = {
        "dataset_id": dataset_id,
        "split_id": split_id,
        "track_id": track_id,
        "preprocessing_id": pp_cfg["preprocessing_id"],
        "pp_config_sha256": pp_sha,
        "class_map_sha256": EXPECTED_CLASSES_CSV_SHA256,
        "partitions": part_counts,
    }
    (output_dir / "bundle_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
