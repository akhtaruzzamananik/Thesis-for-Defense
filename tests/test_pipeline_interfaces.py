"""Unit tests for STEP-025 data loading guards, known-case evaluator edge cases, and timing wrapper."""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Sequence

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

import opg.data_loader as data_loader_mod  # noqa: E402
from opg.data_loader import load_locked_partition_items, validate_experiment_config  # noqa: E402
from opg.evaluator import DetectionBox, evaluate_predictions, find_optimal_operating_conf  # noqa: E402
from opg.trainer import benchmark_inference_latency  # noqa: E402


def _make_valid_t14_config() -> dict:
    cfg = yaml.safe_load((ROOT / "07_Experiments" / "experiment_config_schema.yaml").read_text(encoding="utf-8"))
    cfg["identity"]["experiment_id"] = "EXP0001"
    cfg["identity"]["research_question_ids"] = ["RQ0", "RQ1"]
    cfg["identity"]["purpose"] = "primary_baseline"
    cfg["identity"]["approval_record"] = "DEC0012"
    cfg["identity"]["source_commit"] = "0" * 40
    cfg["data"]["release_id"] = "REL0001"
    cfg["data"]["dataset_id"] = "DS0001"
    cfg["data"]["annotation_id"] = "ANN0001"
    cfg["data"]["split_id"] = "SPLIT0001"
    cfg["data"]["preprocessing_id"] = "PP0001"
    cfg["data"]["release_manifest_sha256"] = "a" * 64
    cfg["data"]["split_manifest_sha256"] = "b" * 64
    cfg["data"]["pp_config_sha256"] = "c" * 64
    cfg["model"]["candidate_id"] = "MC0001"
    cfg["model"]["architecture"] = "yolo11s"
    cfg["model"]["initial_weights"] = "yolo11s.pt"
    cfg["model"]["initial_weights_sha256"] = "d" * 64
    cfg["model"]["num_classes"] = 13
    cfg["training"]["image_size"] = 640
    cfg["training"]["batch_size"] = 16
    cfg["runtime"]["platform"] = "kaggle_gpu"
    cfg["runtime"]["hardware_record"] = "T4"
    cfg["evaluation"]["protocol_sha256"] = "e" * 64
    cfg["outputs"]["artifact_destination"] = "offgit/EXP0001"
    return cfg


def test_t14_config_guards_and_locked_loader(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = _make_valid_t14_config()
    validate_experiment_config(cfg, root=ROOT)

    # 1. Null field must fail
    bad_null = copy.deepcopy(cfg)
    bad_null["training"]["image_size"] = None
    with pytest.raises(ValueError, match="Unresolved null"):
        validate_experiment_config(bad_null, root=ROOT)

    # 2. Class-map hash mismatch must fail
    bad_hash = copy.deepcopy(cfg)
    bad_hash["data"]["class_map_sha256"] = "deadbeef"
    with pytest.raises(ValueError, match="Class-map SHA-256 mismatch"):
        validate_experiment_config(bad_hash, root=ROOT)

    # 3. Attempting to include 'test' partition before G11 PASS must fail
    bad_test = copy.deepcopy(cfg)
    bad_test["data"]["allowed_partitions"] = ["train", "val", "test"]
    with monkeypatch.context() as mp:
        mp.setattr(data_loader_mod, "_is_g11_passed", lambda _root: False)
        with pytest.raises(PermissionError, match="SEALED TEST VIOLATION"):
            validate_experiment_config(bad_test, root=ROOT)
        with pytest.raises(PermissionError, match="SEALED TEST VIOLATION"):
            load_locked_partition_items(
                ROOT, dataset_id="DS0003", split_id="SPLIT0003", batch_id="ANNB0003", track_id="TrackC", partition="test"
            )

    # 4. After G11 PASS, locked test loader returns exact canonical test items & still rejects wrong split hash
    if data_loader_mod._is_g11_passed(ROOT):
        ds3_test = load_locked_partition_items(
            ROOT, dataset_id="DS0003", split_id="SPLIT0003", batch_id="ANNB0003", track_id="TrackC", partition="test"
        )
        assert len(ds3_test) == 33
    with pytest.raises(ValueError, match="Split manifest SHA-256 mismatch"):
        load_locked_partition_items(
            ROOT,
            dataset_id="DS0003",
            split_id="SPLIT0003",
            batch_id="ANNB0003",
            track_id="TrackC",
            partition="val",
            expected_split_sha256="wrong_hash",
        )


def test_evaluator_known_detection_cases() -> None:
    classes = ["Caries", "Impacted", "Implant"]  # Class 2 (Implant) will be absent from GT!
    gt: dict[str, Sequence[DetectionBox]] = {
        "img_perfect": [DetectionBox(0, (100, 100, 200, 200))],
        "img_miss": [DetectionBox(0, (100, 100, 200, 200))],
        "img_dup": [DetectionBox(1, (50, 50, 150, 150))],
        "img_wrong_cls": [DetectionBox(1, (300, 300, 400, 400))],
        "img_empty": [],  # reviewed_empty image MUST be counted in coverage!
    }
    preds: dict[str, Sequence[DetectionBox]] = {
        "img_perfect": [DetectionBox(0, (100, 100, 200, 200), score=0.95)],
        "img_miss": [],  # no predictions
        "img_dup": [
            DetectionBox(1, (50, 50, 150, 150), score=0.90),  # TP
            DetectionBox(1, (52, 52, 148, 148), score=0.80),  # Duplicate -> MUST be FP!
        ],
        "img_wrong_cls": [DetectionBox(0, (300, 300, 400, 400), score=0.85)],  # Wrong class -> FP on 0, FN on 1
        "img_empty": [DetectionBox(0, (10, 10, 40, 40), score=0.70)],  # FP on empty image!
    }

    res = evaluate_predictions(gt, preds, classes, matching_ious=(0.50,), operating_conf=0.25)
    assert res["evaluated_images"] == 5
    assert res["reviewed_empty_images"] == 1
    assert res["eligible_class_count"] == 2
    assert res["absent_class_ids"] == [2]

    # Class 0: 2 GTs (perfect + miss), 3 preds (0.95 TP, 0.85 FP wrong_cls, 0.70 FP empty)
    c0 = res["per_class"][0]
    assert (c0["tp_op"], c0["fp_op"], c0["fn_op"]) == (1, 2, 1)
    assert pytest.approx(c0["precision"], abs=1e-5) == 1.0 / 3.0
    assert pytest.approx(c0["recall"], abs=1e-5) == 0.5
    assert pytest.approx(c0["ap"], abs=1e-5) == 0.5

    # Class 1: 2 GTs (dup + wrong_cls), 2 preds (0.90 TP, 0.80 FP dup)
    c1 = res["per_class"][1]
    assert (c1["tp_op"], c1["fp_op"], c1["fn_op"]) == (1, 1, 1)
    assert pytest.approx(c1["precision"], abs=1e-5) == 0.5
    assert pytest.approx(c1["recall"], abs=1e-5) == 0.5
    assert pytest.approx(c1["ap"], abs=1e-5) == 0.5

    # Class 2 (absent from GT): must NOT inflate or deflate mAP!
    c2 = res["per_class"][2]
    assert c2["eligible"] is False
    assert c2["recall"] is None
    assert c2["ap"] is None

    # mAP@0.50 averages ONLY eligible classes (0 and 1): (0.5 + 0.5) / 2 = 0.5
    assert pytest.approx(res["mAP@0.50"], abs=1e-5) == 0.5

    # Test no-prediction edge case -> precision is None (N/A), recall=0.0, AP=0.0
    res_nopred = evaluate_predictions(
        {"im1": [DetectionBox(0, (10, 10, 50, 50))]},
        {"im1": []},
        ["Caries"],
        matching_ious=(0.50,),
    )
    assert res_nopred["per_class"][0]["precision"] is None
    assert res_nopred["per_class"][0]["recall"] == 0.0
    assert res_nopred["mAP@0.50"] == 0.0

    best_c, best_f1 = find_optimal_operating_conf(gt, preds, classes)
    assert 0.05 <= best_c <= 0.70
    assert best_f1 >= 0.0


def test_latency_benchmark_wrapper() -> None:
    items = list(range(15))
    res = benchmark_inference_latency(
        items,
        preprocess_fn=lambda x: x + 1,
        infer_fn=lambda x: x * 2,
        postprocess_fn=lambda x: x,
        warmup_count=5,
    )
    assert res["n_timed_images"] == 15
    assert res["warmup_count"] == 5
    assert res["FPS_e2e"] > 0
