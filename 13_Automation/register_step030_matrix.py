"""Register and validate all STEP-030 controlled experiment matrix rows (EXP0002-EXP0013)."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.data_loader import validate_experiment_config  # noqa: E402

SOURCE_COMMIT = "2f7d41af4a65ccede5d05e602b42eef75e947ab0"
CLASS_MAP_SHA256 = "c3f91dfc8a27e5a0dc4ca6324676dbcb78bb8460112e36f84032b295694640af"
PROTOCOL_SHA256 = "26fede09e31475e7e7a5a1cdd3bc2a111815f727d8925300976dc6060a9024c1"

REL_INFO = {
    "REL0001": ("DS0001", "ANN0001", "ANNB0001", "SPLIT0001", "TrackA", 13, "40d7db1d4a9a2d87d9d689a16dc784a01a79f6a4df6f84b29f66241990d0ef9c", "b7b40a1af8518644fc14a3a1aa4fa0569cb299f0ed2cc06533f534ff46e1e8ee"),
    "REL0002": ("DS0002", "ANN0002", "ANNB0002", "SPLIT0002", "TrackB", 4, "b187d514402a3145ae136127278c125ca563e2d329cdee0bdedd214268ddd8a7", "f660fa2a09197b3fdf9641e261499ec49effeacc596f6cc633de63997172e092"),
    "REL0003": ("DS0003", "ANN0003", "ANNB0003", "SPLIT0003", "TrackC", 6, "5ffe497a21f6ec0a27e04371fa3b8bcb027f5fee224228c64e646c00aee28bb6", "7081e461819987c050cb34df5e4534e165dc68499fb7aba6c8dc80fc91fe1151"),
    "REL0004": ("DS0004", "ANN0004", "ANNB0004", "SPLIT0004", "TrackD", 3, "570f33b421ad415c94055a244ea60b5e9e7afbbe789dec08fc98d1e4e3b08e57", "74aa4db7b70e72c2655b147b381492a0df5477a4820d4205074bd5cf047f49e0"),
    "REL0005": ("DS0005", "ANN0005", "ANNB0005", "SPLIT0005", "TrackE", 6, "1642e409741a5d102a4b0bc8afa45fe2ac6b47ea2ec96794d1b40555a8a35975", "cb894f5bd138ada998687cfa80a756127db7e70bdc94b4b25335d3ce3dc6d504"),
    "REL0006": ("DS0006", "ANN0006", "ANNB0006", "SPLIT0006", "TrackF", 2, "721126e42e302903d5b9970d3a6c1bc14ccbcafba218fff93d29d10d174cce8f", "04aafcceeeb0215fb4c2d23106c9900bdf8fa892d007ac15cf01e54fdb7f0e5a"),
}

PP_INFO = {
    "PP0001": ("04493e1e2bcdfcadbef5b044b392bf7091822439381e158d85c144d420e0b93b", 640, 16),
    "PP0002": ("7482eac3c347664672f287781aba8f5b952bfc219059bc5fdd2570d539eedfbf", 640, 16),
    "PP0003": ("65b7ffd170ce05d5e2ae9f8acbd1f401acaf430e69754ba86caaedc64166c64e", 640, 16),
    "PP0004": ("08fd22b42f9fa31465eedc092251d92d7b5338b76de4fc7d321a7c77741dd2de", 1280, 8),
}

MODEL_INFO = {
    "MC0001": ("yolo11s", "yolo11s.pt"),
    "MC0002": ("yolov8s", "yolov8s.pt"),
    "MC0003": ("yolo11m", "yolo11m.pt"),
}

# (exp_id, rqs, purpose, parent, rel_id, mc_id, pp_id, bundle_zip_name, note)
MATRIX = [
    ("EXP0002", ["RQ1", "RQ3"], "comparator", "EXP0001", "REL0001", "MC0002", "PP0001", "EXP0001_REL0001_PP0001_bundle.zip", "Cross-generation comparator YOLOv8s vs EXP0001 YOLO11s on TrackA (reuses EXP0001 bundle)"),
    ("EXP0003", ["RQ0", "RQ1"], "track_baseline", "NONE", "REL0002", "MC0001", "PP0001", "kaggle_bundles/REL0002_PP0001_bundle.zip", "TrackB DENTEX 4-class baseline YOLO11s @ 640"),
    ("EXP0004", ["RQ0", "RQ1"], "track_baseline", "NONE", "REL0003", "MC0001", "PP0001", "kaggle_bundles/REL0003_PP0001_bundle.zip", "TrackC Rahman 2024 Dhaka handheld OPG 6-class baseline YOLO11s @ 640"),
    ("EXP0005", ["RQ0", "RQ1"], "track_baseline", "NONE", "REL0004", "MC0001", "PP0001", "kaggle_bundles/REL0004_PP0001_bundle.zip", "TrackD Do 2024 Hanoi PAI 3-5 baseline YOLO11s @ 640"),
    ("EXP0006", ["RQ0", "RQ1"], "track_baseline", "NONE", "REL0005", "MC0001", "PP0001", "kaggle_bundles/REL0005_PP0001_bundle.zip", "TrackE AU-OPG Ajman UAE 6-class baseline YOLO11s @ 640"),
    ("EXP0007", ["RQ0", "RQ1"], "track_baseline", "NONE", "REL0006", "MC0001", "PP0001", "kaggle_bundles/REL0006_PP0001_bundle.zip", "TrackF MD-OPG Pediatric 2-class caries baseline YOLO11s @ 640 + autocrop"),
    ("EXP0008", ["RQ2"], "rq2_ablation", "EXP0001", "REL0001", "MC0001", "PP0002", "kaggle_bundles/REL0001_PP0002_bundle.zip", "Single-factor RQ2 ablation: CLAHE 2.0 8x8 vs EXP0001 raw 640 on TrackA"),
    ("EXP0009", ["RQ2"], "rq2_ablation", "EXP0001", "REL0001", "MC0001", "PP0003", "kaggle_bundles/REL0001_PP0003_bundle.zip", "Single-factor RQ2 ablation: CLAHE 3.0 16x16 vs EXP0001 raw 640 on TrackA"),
    ("EXP0010", ["RQ2", "RQ3"], "rq2_ablation", "EXP0001", "REL0001", "MC0001", "PP0004", "kaggle_bundles/REL0001_PP0004_bundle.zip", "Single-factor RQ2 ablation: 1280x1280 raw vs EXP0001 640x640 on TrackA"),
    ("EXP0011", ["RQ2", "RQ3"], "rq2_ablation", "EXP0005", "REL0004", "MC0001", "PP0004", "kaggle_bundles/REL0004_PP0004_bundle.zip", "Single-factor RQ2 ablation: 1280x1280 raw vs EXP0005 640x640 on TrackD PAI 3-5"),
    ("EXP0012", ["RQ2"], "rq2_ablation", "EXP0004", "REL0003", "MC0001", "PP0002", "kaggle_bundles/REL0003_PP0002_bundle.zip", "Single-factor RQ2 ablation: CLAHE 2.0 8x8 vs EXP0004 raw on TrackC Dhaka handheld OPG"),
    ("EXP0013", ["RQ1", "RQ3"], "scale_comparator", "EXP0001", "REL0001", "MC0003", "PP0001", "EXP0001_REL0001_PP0001_bundle.zip", "Conditional scale comparator YOLO11m vs EXP0001 YOLO11s on TrackA (reuses EXP0001 bundle)"),
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    reg_path = ROOT / "07_Experiments" / "experiment_registry.csv"
    with reg_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        existing = {row["ExperimentID"]: row for row in reader}

    for exp_id, rqs, purpose, parent, rel_id, mc_id, pp_id, bundle_zip, note in MATRIX:
        ds_id, ann_id, annb_id, split_id, track_id, nc, rel_sha, split_sha = REL_INFO[rel_id]
        pp_sha, imgsz, bs = PP_INFO[pp_id]
        arch, weights = MODEL_INFO[mc_id]

        cfg = {
            "schema_version": "T14-v1.0.0",
            "identity": {
                "experiment_id": exp_id,
                "research_question_ids": rqs,
                "purpose": purpose,
                "parent_comparison_id": parent,
                "approval_record": "DEC0010 / DEC0012 / STEP-024 / STEP-030",
                "source_commit": SOURCE_COMMIT,
            },
            "data": {
                "release_id": rel_id,
                "dataset_id": ds_id,
                "annotation_id": ann_id,
                "split_id": split_id,
                "preprocessing_id": pp_id,
                "release_manifest_sha256": rel_sha,
                "split_manifest_sha256": split_sha,
                "class_map_sha256": CLASS_MAP_SHA256,
                "pp_config_sha256": pp_sha,
                "allowed_partitions": ["train", "val"],
            },
            "model": {
                "candidate_id": mc_id,
                "implementation": "ultralytics",
                "package_version": "8.3.253",
                "architecture": arch,
                "initial_weights": weights,
                "initial_weights_sha256": "recorded_on_kaggle_download_in_effective_manifest",
                "license_record": "AGPL-3.0",
                "num_classes": nc,
            },
            "training": {
                "seed": 20261124,
                "deterministic": True,
                "image_size": imgsz,
                "batch_size": bs,
                "epochs": 100,
                "patience": 20,
                "optimizer": "AdamW",
                "lr0": 0.001,
                "lrf": 0.01,
                "momentum": 0.937,
                "weight_decay": 0.0005,
                "warmup_epochs": 3.0,
                "amp": True,
                "workers": 4,
                "selection_metric": "mAP@0.50",
                "augmentations": {
                    "degrees": 5.0,
                    "translate": 0.05,
                    "scale": 0.10,
                    "hsv_v": 0.10,
                    "fliplr": 0.0,
                    "flipud": 0.0,
                    "mosaic": 0.5,
                    "close_mosaic": 10,
                },
            },
            "runtime": {
                "platform": "kaggle_gpu",
                "environment_lock": "environment/model/requirements-kaggle.txt",
                "hardware_record": "Kaggle T4/P100 16GB (captured at runtime)",
            },
            "evaluation": {
                "protocol_path": "09_Evaluation/protocol.md",
                "protocol_sha256": PROTOCOL_SHA256,
                "matching_iou": 0.50,
                "nms_iou": 0.65,
                "agnostic_nms": False,
                "max_detections": 300,
                "metric_conf_floor": 0.001,
                "operating_conf_threshold": "val_selected_at_G11",
            },
            "outputs": {
                "checkpoint_policy": "08_Checkpoints/checkpoint_policy.md",
                "artifact_destination": f"08_Checkpoints/artifacts/{exp_id}/",
            },
        }
        validate_experiment_config(cfg, root=ROOT)

        exp_dir = ROOT / "07_Experiments" / exp_id
        exp_dir.mkdir(parents=True, exist_ok=True)
        cfg_path = exp_dir / "config.yaml"
        cfg_text = f"# {exp_id} — {note}\n" + yaml.safe_dump(cfg, sort_keys=False)
        cfg_path.write_text(cfg_text, encoding="utf-8")
        cfg_sha = sha256_bytes(cfg_path.read_bytes())

        manifest = {
            "experiment_id": exp_id,
            "schema_version": "T14-v1.0.0",
            "status": "READY_TO_LAUNCH_STEP030",
            "purpose": purpose,
            "parent_comparison_id": parent,
            "research_questions": rqs,
            "release_id": rel_id,
            "dataset_id": ds_id,
            "split_id": split_id,
            "annotation_batch_id": annb_id,
            "track_id": track_id,
            "preprocessing_id": pp_id,
            "model_candidate": mc_id,
            "architecture": arch,
            "image_size": imgsz,
            "batch_size": bs,
            "source_commit": SOURCE_COMMIT,
            "allowed_partitions": ["train", "val"],
            "forbidden_partitions": ["test", "external_test"],
            "hashes": {
                "config_sha256": cfg_sha,
                "release_manifest_sha256": rel_sha,
                "split_manifest_sha256": split_sha,
                "class_map_sha256": CLASS_MAP_SHA256,
                "pp_config_sha256": pp_sha,
                "protocol_sha256": PROTOCOL_SHA256,
            },
            "off_git_bundle_zip": f"08_Checkpoints/artifacts/{bundle_zip}",
            "artifact_destination": f"08_Checkpoints/artifacts/{exp_id}/",
        }
        (exp_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        if exp_id not in existing:
            existing[exp_id] = {
                "ExperimentID": exp_id,
                "RQ": "; ".join(rqs),
                "Purpose": purpose,
                "ParentComparison": parent,
                "ReleaseID": rel_id,
                "ModelCandidate": mc_id,
                "ConfigPath": f"07_Experiments/{exp_id}/config.yaml",
                "ConfigHash": cfg_sha,
                "SourceCommit": SOURCE_COMMIT,
                "Seed": "20261124",
                "RunIDs": "READY_STEP030",
                "Start": "",
                "End": "",
                "StoppingReason": "",
                "ValidationEvaluationIDs": "PENDING",
                "FailureReport": "NONE",
                "Conclusion": note,
                "Owner": "Mahajub Al Shabah",
                "Version": "v1.0.0",
                "Status": "Ready-To-Launch-STEP030",
                "Created": "2026-11-20",
                "Updated": "2026-11-20",
                "EvidencePath": f"07_Experiments/{exp_id}/run_manifest.json",
            }
        print(f"REGISTERED_VALID: {exp_id} ({arch} @ {imgsz}px, {rel_id}/{pp_id}, cfg_sha={cfg_sha[:8]})")

    ordered_ids = ["EXP0000_SMOKE"] + [f"EXP{i:04d}" for i in range(1, 14)]
    with reg_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for eid in ordered_ids:
            if eid in existing:
                writer.writerow(existing[eid])
    print("UPDATED_REGISTRY:", reg_path)


if __name__ == "__main__":
    main()
