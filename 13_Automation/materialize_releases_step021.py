"""Execute STEP-021 prepared dataset release materialization, train-only fit, and round-trip geometry audit (REL0001-REL0006 / G08)."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_pilot import DATASET_TRACK_MAP, EXPECTED_CLASSES_CSV_SHA256  # noqa: E402
from opg.annotation_schema import (  # noqa: E402
    compute_class_map_sha256,
    format_yolo_line,
    parse_yolo_line,
    xyxy_to_yolo_norm,
    yolo_norm_to_xyxy,
)
from opg.preprocessing import (  # noqa: E402
    TransformLedger,
    apply_clahe_rgb,
    autocrop_black_border_with_boxes,
    compute_config_sha256,
    fit_training_statistics,
    forward_transform_box,
    inverse_transform_box,
    prepare_image_and_boxes,
)

RAW_ROOT = ROOT / "03_Datasets" / "raw"
DS_MANIFEST_ROOT = ROOT / "03_Datasets" / "manifests"
SPLIT_ROOT = ROOT / "03_Datasets" / "splits"
ANN_ROOT = ROOT / "04_Annotations"
PP_ROOT = ROOT / "05_Preprocessing"
PROCESSED_ROOT = PP_ROOT / "processed"

RELEASE_SPECS: list[dict[str, str]] = [
    {
        "release_id": "REL0001",
        "dataset_id": "DS0001",
        "dataset_version": "v1.1.0",
        "ann_id": "ANN0001",
        "batch_id": "ANNB0001",
        "split_id": "SPLIT0001",
        "track_id": "TrackA",
        "pp_id": "PP0001",
        "desc": "UMFIH Romania 13-class internal (994 train / 214 val / 208 test) + sealed 178 external_test prepared release",
    },
    {
        "release_id": "REL0002",
        "dataset_id": "DS0002",
        "dataset_version": "v1.0.0",
        "ann_id": "ANN0002",
        "batch_id": "ANNB0002",
        "split_id": "SPLIT0002",
        "track_id": "TrackB",
        "pp_id": "PP0001",
        "desc": "DENTEX MICCAI 2023 4-class disease (493 train / 106 val / 106 test) prepared release",
    },
    {
        "release_id": "REL0003",
        "dataset_id": "DS0003",
        "dataset_version": "v1.1.0",
        "ann_id": "ANN0003",
        "batch_id": "ANNB0003",
        "split_id": "SPLIT0003",
        "track_id": "TrackC",
        "pp_id": "PP0001",
        "desc": "Rahman 2024 Dhaka 6-class whole-tooth (163 train / 34 val / 33 test) EXIF-stripped prepared release",
    },
    {
        "release_id": "REL0004",
        "dataset_id": "DS0004",
        "dataset_version": "v1.0.0",
        "ann_id": "ANN0004",
        "batch_id": "ANNB0004",
        "split_id": "SPLIT0004",
        "track_id": "TrackD",
        "pp_id": "PP0001",
        "desc": "Do 2024 Hanoi 3-class PAI 3-5 periapical (2707 train / 578 val / 578 test) deduplicated prepared release",
    },
    {
        "release_id": "REL0005",
        "dataset_id": "DS0005",
        "dataset_version": "v1.1.0",
        "ann_id": "ANN0005",
        "batch_id": "ANNB0005",
        "split_id": "SPLIT0005",
        "track_id": "TrackE",
        "pp_id": "PP0001",
        "desc": "AU-OPG Ajman UAE 6-class OBB->AABB (628 train / 134 val / 133 test) leak-repaired prepared release",
    },
    {
        "release_id": "REL0006",
        "dataset_id": "DS0006",
        "dataset_version": "v1.1.0",
        "ann_id": "ANN0006",
        "batch_id": "ANNB0006",
        "split_id": "SPLIT0006",
        "track_id": "TrackF",
        "pp_id": "PP0001",
        "desc": "MD-OPG Zanjan Iran 2-class pediatric caries (121 train / 25 val / 24 test) black-border autocropped prepared release",
    },
]


def _sha256_file(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def _verify_g07_passed() -> bool:
    gates_csv = ROOT / "01_Project_Management" / "gates.csv"
    with gates_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["GateID"].strip() == "G07":
                return row["Outcome"].strip().upper() == "PASS"
    return False


def _load_linkage(dataset_id: str) -> dict[str, str]:
    path = DS_MANIFEST_ROOT / f"{dataset_id}_restricted_linkage.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["ImageID"]: row["original_relpath"] for row in csv.DictReader(handle)}


def _load_qc_stats_map(dataset_id: str) -> dict[str, dict[str, float]]:
    path = DS_MANIFEST_ROOT / f"{dataset_id}_restricted_qc.csv"
    out: dict[str, dict[str, float]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            out[row["image_id"]] = {
                "mean_luma": float(row.get("mean_luma", 0.0) or 0.0),
                "std_luma": float(row.get("std_luma", 0.0) or 0.0),
                "pct_black_le_3": float(row.get("pct_black_le_3", 0.0) or 0.0),
                "pct_white_ge_252": float(row.get("pct_white_ge_252", 0.0) or 0.0),
                "laplacian_var": float(row.get("laplacian_var", 0.0) or 0.0),
            }
    return out


def _compute_ledger(
    src_w: int,
    src_h: int,
    crop_box: tuple[int, int, int, int],
    target_size: tuple[int, int] = (640, 640),
    pad_value: int = 114,
) -> TransformLedger:
    cx0, cy0, cw, ch = crop_box
    out_w, out_h = target_size
    scale = min(out_w / float(cw), out_h / float(ch))
    new_w = max(1, int(round(cw * scale)))
    new_h = max(1, int(round(ch * scale)))
    scale_x = new_w / float(cw)
    scale_y = new_h / float(ch)
    pad_w = out_w - new_w
    pad_h = out_h - new_h
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left
    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    return TransformLedger(
        src_width=src_w,
        src_height=src_h,
        crop_x0=cx0,
        crop_y0=cy0,
        crop_width=cw,
        crop_height=ch,
        out_width=out_w,
        out_height=out_h,
        scale_x=scale_x,
        scale_y=scale_y,
        pad_left=pad_left,
        pad_top=pad_top,
        pad_right=pad_right,
        pad_bottom=pad_bottom,
        pad_value=pad_value,
    )


def _render_pp_visual_qa_sheet(
    dataset_id: str,
    sample_items: list[tuple[str, str, int, int, list[tuple[int, float, float, float, float]]]],
    linkage: dict[str, str],
    out_jpg_path: Path,
) -> None:
    """Render a 4-row x 3-col visual comparison sheet (PP0001 Raw vs PP0002 CLAHE 2.0 vs PP0003 CLAHE 3.0) on train/val only."""
    extracted = RAW_ROOT / dataset_id / "extracted"
    tile_s = 320
    rows = min(4, len(sample_items))
    cols = 3
    canvas = np.full((rows * tile_s, cols * tile_s, 3), 24, dtype=np.uint8)
    palette = [
        (0, 255, 128),
        (0, 200, 255),
        (255, 180, 0),
        (255, 80, 180),
        (120, 255, 255),
        (80, 160, 255),
    ]
    autocrop = dataset_id == "DS0006"

    for r_idx, (iid, part, _, _, raw_boxes) in enumerate(sample_items[:rows]):
        if part not in ("train", "val"):
            raise RuntimeError(f"LEAKAGE GUARD: Visual QA must never render test images! Got {part}")
        img_p = extracted / linkage[iid]
        raw_bytes = np.fromfile(str(img_p), dtype=np.uint8)
        im_bgr = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
        if im_bgr is None:
            continue
        im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)

        variants = [
            ("PP0001 Raw 640", None),
            ("PP0002 CLAHE 2.0 (8x8)", (2.0, (8, 8))),
            ("PP0003 CLAHE 3.0 (16x16)", (3.0, (16, 16))),
        ]
        for c_idx, (v_title, clahe_cfg) in enumerate(variants):
            out_rgb, out_boxes, _, _ = prepare_image_and_boxes(
                im_rgb,
                raw_boxes,
                target_size=(640, 640),
                preserve_aspect_ratio=True,
                autocrop_black_border=autocrop,
                clahe_params=clahe_cfg,
            )
            out_bgr = cv2.cvtColor(out_rgb, cv2.COLOR_RGB2BGR)
            disp = cv2.resize(out_bgr, (tile_s, tile_s), interpolation=cv2.INTER_AREA)
            scale_disp = tile_s / 640.0
            for cid, x0, y0, x1, y1 in out_boxes:
                color = palette[cid % len(palette)]
                p0 = (int(round(x0 * scale_disp)), int(round(y0 * scale_disp)))
                p1 = (int(round(x1 * scale_disp)), int(round(y1 * scale_disp)))
                cv2.rectangle(disp, p0, p1, color, 1)

            banner = f"{iid} ({part}) | {v_title} | b={len(out_boxes)}"
            cv2.rectangle(disp, (0, 0), (tile_s, 18), (0, 0, 0), -1)
            cv2.putText(disp, banner, (4, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.31, (255, 255, 255), 1, cv2.LINE_AA)
            y_off = r_idx * tile_s
            x_off = c_idx * tile_s
            canvas[y_off : y_off + tile_s, x_off : x_off + tile_s] = disp

    out_jpg_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_jpg_path), canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def main() -> None:
    if not _verify_g07_passed():
        raise RuntimeError("STEP-021 blocked: G07 is not PASS in 01_Project_Management/gates.csv")

    classes_sha = compute_class_map_sha256(ANN_ROOT / "classes.csv")
    if classes_sha != EXPECTED_CLASSES_CSV_SHA256:
        raise RuntimeError(f"ClassMapHash mismatch: {classes_sha}")

    pp_configs = {
        "PP0001": PP_ROOT / "configs" / "PP0001_raw_letterbox_baseline.yaml",
        "PP0002": PP_ROOT / "configs" / "PP0002_clahe_2p0_8x8.yaml",
        "PP0003": PP_ROOT / "configs" / "PP0003_clahe_3p0_16x16.yaml",
        "PP0004": PP_ROOT / "configs" / "PP0004_highres_letterbox_1280.yaml",
    }
    pp_config_shas = {k: compute_config_sha256(v) for k, v in pp_configs.items()}

    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
    (PP_ROOT / "reports").mkdir(parents=True, exist_ok=True)

    all_releases_summary: dict[str, Any] = {}
    grand_canonical_imgs = 0
    grand_train_imgs = 0
    grand_canonical_boxes = 0
    grand_max_rt_err_640 = 0.0
    grand_max_rt_err_1280 = 0.0

    for spec in RELEASE_SPECS:
        rel_id = spec["release_id"]
        ds_id = spec["dataset_id"]
        ann_id = spec["ann_id"]
        batch_id = spec["batch_id"]
        split_id = spec["split_id"]
        track_id = spec["track_id"]

        rel_dir = PROCESSED_ROOT / rel_id
        rel_dir.mkdir(parents=True, exist_ok=True)

        # Load and verify parent manifests
        ds_man_path = DS_MANIFEST_ROOT / f"{ds_id}_images.csv"
        ds_man_sha = _sha256_file(ds_man_path)
        with ds_man_path.open("r", encoding="utf-8", newline="") as handle:
            ds_by_id = {
                r["ImageID"]: r for r in csv.DictReader(handle) if not r["intake_status"].startswith("quarantined")
            }

        exp_dir = ANN_ROOT / "exports" / f"{batch_id}_{track_id}"
        exp_man_path = exp_dir / "export_manifest.csv"
        exp_man_sha = _sha256_file(exp_man_path)
        with exp_man_path.open("r", encoding="utf-8", newline="") as handle:
            exp_by_id = {r["ImageID"]: r for r in csv.DictReader(handle)}

        split_man_path = SPLIT_ROOT / split_id / "manifest.csv"
        split_man_sha = _sha256_file(split_man_path)
        with split_man_path.open("r", encoding="utf-8", newline="") as handle:
            split_rows = list(csv.DictReader(handle))

        linkage = _load_linkage(ds_id)
        qc_map = _load_qc_stats_map(ds_id)
        extracted = RAW_ROOT / ds_id / "extracted"

        # 1. Fit training-only statistics strictly on Partition == 'train' and MemberRole == 'active_canonical'
        train_can_rows = [
            r for r in split_rows if r["Partition"] == "train" and r["MemberRole"] == "active_canonical"
        ]
        # Verify programmatic leakage guard using a 4-image decoded training sample
        sample_train_arrays: list[np.ndarray] = []
        for tr in train_can_rows[:4]:
            raw_b = np.fromfile(str(extracted / linkage[tr["ImageID"]]), dtype=np.uint8)
            im = cv2.imdecode(raw_b, cv2.IMREAD_COLOR)
            if im is not None:
                sample_train_arrays.append(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        guard_stats = fit_training_statistics(
            sample_train_arrays,
            g07_split_passed=True,
            partition_names=["train"] * len(sample_train_arrays),
        )

        train_lumas = [qc_map[r["ImageID"]]["mean_luma"] / 255.0 for r in train_can_rows]
        train_stds = [qc_map[r["ImageID"]]["std_luma"] / 255.0 for r in train_can_rows]
        fit_state_payload = {
            "release_id": rel_id,
            "dataset_id": ds_id,
            "split_id": split_id,
            "fit_partition": "train_only (MemberRole == active_canonical)",
            "val_or_test_accessed_for_fit": False,
            "train_canonical_image_count": len(train_can_rows),
            "train_mean_intensity_0_1": round(float(np.mean(train_lumas)), 6),
            "train_std_intensity_0_1": round(float(np.mean(train_stds)), 6),
            "train_p05_intensity_0_1": round(float(np.percentile(train_lumas, 5)), 6),
            "train_p95_intensity_0_1": round(float(np.percentile(train_lumas, 95)), 6),
            "guard_smoke_verification": guard_stats,
        }
        fit_state_path = rel_dir / "fit_state_train_only.json"
        fit_state_path.write_text(json.dumps(fit_state_payload, indent=2), encoding="utf-8")
        fit_state_sha = _sha256_file(fit_state_path)

        # 2. Process all active_canonical images across train, val, test, external_test
        ledger_rows: list[dict[str, Any]] = []
        part_img_counts: Counter[str] = Counter()
        part_box_counts: Counter[str] = Counter()
        class_box_counts: Counter[int] = Counter()
        ds_max_rt_640 = 0.0
        ds_max_rt_1280 = 0.0
        dropped_boxes = 0
        qa_render_candidates: list[tuple[str, str, int, int, list[tuple[int, float, float, float, float]]]] = []

        for srow in split_rows:
            if srow["MemberRole"] != "active_canonical":
                continue
            iid = srow["ImageID"]
            part = srow["Partition"]
            drow = ds_by_id[iid]
            w = int(drow["width"])
            h = int(drow["height"])
            if srow["SHA256"] != drow["sha256"]:
                raise RuntimeError(f"Raw SHA-256 drift detected for {iid}")

            # Parse frozen STEP-018 canonical boxes in raw pixel space
            txt_in = exp_dir / exp_by_id[iid]["LabelRelPath"]
            in_lines = [ln.strip() for ln in txt_in.read_text(encoding="utf-8").splitlines() if ln.strip()]
            raw_boxes: list[tuple[int, float, float, float, float]] = []
            for ln in in_lines:
                cid, xc, yc, bw, bh = parse_yolo_line(ln)
                x0, y0, x1, y1 = yolo_norm_to_xyxy(xc, yc, bw, bh, w, h)
                raw_boxes.append((cid, x0, y0, x1, y1))

            # For DS0006, compute exact black-border autocrop window from the raw image
            if ds_id == "DS0006":
                raw_b = np.fromfile(str(extracted / linkage[iid]), dtype=np.uint8)
                im_bgr = cv2.imdecode(raw_b, cv2.IMREAD_COLOR)
                assert im_bgr is not None
                im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
                _, _, crop_box = autocrop_black_border_with_boxes(
                    im_rgb, [(b[1], b[2], b[3], b[4]) for b in raw_boxes], black_threshold=8, margin_px=8
                )
            else:
                crop_box = (0, 0, w, h)

            ledger_640 = _compute_ledger(w, h, crop_box, target_size=(640, 640), pad_value=114)
            ledger_1280 = _compute_ledger(w, h, crop_box, target_size=(1280, 1280), pad_value=114)

            out_lines_640: list[str] = []
            img_max_rt_640 = 0.0
            img_max_rt_1280 = 0.0

            for cid, x0, y0, x1, y1 in raw_boxes:
                # 640x640 forward -> YOLO 6-dec -> inverse round-trip check
                ox0, oy0, ox1, oy1 = forward_transform_box((x0, y0, x1, y1), ledger_640)
                if (ox1 - ox0) <= 1e-3 or (oy1 - oy0) <= 1e-3:
                    dropped_boxes += 1
                    continue
                xc6, yc6, wn6, hn6 = xyxy_to_yolo_norm(ox0, oy0, ox1, oy1, 640, 640, clip=False)
                line6 = format_yolo_line(cid, xc6, yc6, wn6, hn6, precision=6)
                out_lines_640.append(line6)

                _, rxc6, ryc6, rwn6, rhn6 = parse_yolo_line(line6)
                px0, py0, px1, py1 = yolo_norm_to_xyxy(rxc6, ryc6, rwn6, rhn6, 640, 640)
                ix0, iy0, ix1, iy1 = inverse_transform_box((px0, py0, px1, py1), ledger_640)
                err6 = max(abs(ix0 - x0), abs(iy0 - y0), abs(ix1 - x1), abs(iy1 - y1))
                img_max_rt_640 = max(img_max_rt_640, err6)

                # 1280x1280 forward -> YOLO 6-dec -> inverse round-trip check (PP0004)
                hx0, hy0, hx1, hy1 = forward_transform_box((x0, y0, x1, y1), ledger_1280)
                xc12, yc12, wn12, hn12 = xyxy_to_yolo_norm(hx0, hy0, hx1, hy1, 1280, 1280, clip=False)
                line12 = format_yolo_line(cid, xc12, yc12, wn12, hn12, precision=6)
                _, rxc12, ryc12, rwn12, rhn12 = parse_yolo_line(line12)
                hpx0, hpy0, hpx1, hpy1 = yolo_norm_to_xyxy(rxc12, ryc12, rwn12, rhn12, 1280, 1280)
                hix0, hiy0, hix1, hiy1 = inverse_transform_box((hpx0, hpy0, hpx1, hpy1), ledger_1280)
                err12 = max(abs(hix0 - x0), abs(hiy0 - y0), abs(hix1 - x1), abs(hiy1 - y1))
                img_max_rt_1280 = max(img_max_rt_1280, err12)

                class_box_counts[cid] += 1

            if len(out_lines_640) != len(raw_boxes):
                raise RuntimeError(f"Box count mismatch on {iid}: {len(out_lines_640)} != {len(raw_boxes)}")

            ds_max_rt_640 = max(ds_max_rt_640, img_max_rt_640)
            ds_max_rt_1280 = max(ds_max_rt_1280, img_max_rt_1280)
            grand_max_rt_err_640 = max(grand_max_rt_err_640, img_max_rt_640)
            grand_max_rt_err_1280 = max(grand_max_rt_err_1280, img_max_rt_1280)

            part_lbl_dir = rel_dir / "labels" / part
            part_lbl_dir.mkdir(parents=True, exist_ok=True)
            out_txt_str = "\n".join(out_lines_640) + ("\n" if out_lines_640 else "")
            out_txt_bytes = out_txt_str.encode("utf-8")
            (part_lbl_dir / f"{iid}.txt").write_bytes(out_txt_bytes)
            lbl_sha = hashlib.sha256(out_txt_bytes).hexdigest()

            part_img_counts[part] += 1
            part_box_counts[part] += len(out_lines_640)

            if part in ("train", "val") and len(qa_render_candidates) < 4 and len(raw_boxes) > 0:
                qa_render_candidates.append((iid, part, w, h, raw_boxes))

            ledger_rows.append(
                {
                    "ImageID": iid,
                    "DatasetID": ds_id,
                    "ReleaseID": rel_id,
                    "Partition": part,
                    "GroupID": srow["GroupID"],
                    "RawSHA256": drow["sha256"],
                    "src_width": w,
                    "src_height": h,
                    "crop_x0": ledger_640.crop_x0,
                    "crop_y0": ledger_640.crop_y0,
                    "crop_width": ledger_640.crop_width,
                    "crop_height": ledger_640.crop_height,
                    "out_width": ledger_640.out_width,
                    "out_height": ledger_640.out_height,
                    "scale_x": round(ledger_640.scale_x, 8),
                    "scale_y": round(ledger_640.scale_y, 8),
                    "pad_left": ledger_640.pad_left,
                    "pad_top": ledger_640.pad_top,
                    "pad_right": ledger_640.pad_right,
                    "pad_bottom": ledger_640.pad_bottom,
                    "ValidBoxCount": len(out_lines_640),
                    "PreparedLabelSHA256": lbl_sha,
                    "MaxRoundTripPxErr640": round(img_max_rt_640, 6),
                    "MaxRoundTripPxErr1280": round(img_max_rt_1280, 6),
                }
            )

        if dropped_boxes > 0:
            raise RuntimeError(f"Dropped boxes detected in {rel_id}: {dropped_boxes}")

        ledger_csv_path = rel_dir / "transform_ledger.csv"
        with ledger_csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(ledger_rows[0].keys()))
            writer.writeheader()
            writer.writerows(ledger_rows)
        ledger_sha = _sha256_file(ledger_csv_path)

        # Render visual QA comparison sheet (PP0001 vs PP0002 vs PP0003 on train/val only)
        qa_sheet_path = rel_dir / "visual_qa" / f"{rel_id}_pp_comparison_sheet.jpg"
        _render_pp_visual_qa_sheet(ds_id, qa_render_candidates, linkage, qa_sheet_path)

        tot_rel_imgs = sum(part_img_counts.values())
        tot_rel_boxes = sum(part_box_counts.values())
        grand_canonical_imgs += tot_rel_imgs
        grand_train_imgs += part_img_counts["train"]
        grand_canonical_boxes += tot_rel_boxes

        rel_manifest_payload = {
            "release_id": rel_id,
            "dataset_id": ds_id,
            "dataset_version": spec["dataset_version"],
            "annotation_id": ann_id,
            "split_id": split_id,
            "track_id": track_id,
            "primary_preprocessing_id": "PP0001",
            "supported_rq2_preprocessing_ids": ["PP0001", "PP0002", "PP0003", "PP0004"],
            "parent_hashes": {
                "dataset_manifest_sha256": ds_man_sha,
                "annotation_export_manifest_sha256": exp_man_sha,
                "class_map_sha256": classes_sha,
                "split_manifest_sha256": split_man_sha,
                "pp_config_sha256": pp_config_shas,
            },
            "fit_state_train_only_sha256": fit_state_sha,
            "transform_ledger_sha256": ledger_sha,
            "val_or_test_used_for_fit": False,
            "dropped_or_collapsed_boxes": dropped_boxes,
            "max_round_trip_px_err_640": round(ds_max_rt_640, 6),
            "max_round_trip_px_err_1280": round(ds_max_rt_1280, 6),
            "total_canonical_images": tot_rel_imgs,
            "total_canonical_boxes": tot_rel_boxes,
            "partition_image_counts": dict(part_img_counts),
            "partition_box_counts": dict(part_box_counts),
            "class_box_counts": {str(k): v for k, v in sorted(class_box_counts.items())},
            "visual_qa_sheet_offgit": f"05_Preprocessing/processed/{rel_id}/visual_qa/{rel_id}_pp_comparison_sheet.jpg",
        }
        rel_man_path = rel_dir / "release_manifest.json"
        rel_man_path.write_text(json.dumps(rel_manifest_payload, indent=2), encoding="utf-8")
        rel_man_sha = _sha256_file(rel_man_path)
        rel_manifest_payload["release_manifest_sha256"] = rel_man_sha
        all_releases_summary[rel_id] = rel_manifest_payload

    summary_out = {
        "step": "STEP-021",
        "gate": "G08",
        "class_map_sha256": classes_sha,
        "pp_config_sha256": pp_config_shas,
        "total_releases": len(all_releases_summary),
        "total_canonical_images": grand_canonical_imgs,
        "total_train_images_used_for_fit": grand_train_imgs,
        "total_canonical_boxes": grand_canonical_boxes,
        "val_or_test_accessed_for_fit": False,
        "total_dropped_boxes": 0,
        "max_round_trip_px_err_640": round(grand_max_rt_err_640, 6),
        "max_round_trip_px_err_1280": round(grand_max_rt_err_1280, 6),
        "releases": all_releases_summary,
    }
    (PP_ROOT / "reports" / "releases_STEP-021_summary.json").write_text(
        json.dumps(summary_out, indent=2), encoding="utf-8"
    )
    print(
        f"RELEASES_DONE: releases={len(all_releases_summary)}, canonical_imgs={grand_canonical_imgs}, "
        f"train_fit_imgs={grand_train_imgs}, boxes={grand_canonical_boxes}, dropped=0, "
        f"max_rt_640={grand_max_rt_err_640:.6f}px, max_rt_1280={grand_max_rt_err_1280:.6f}px"
    )


if __name__ == "__main__":
    main()
