"""Unit tests for STEP-016 annotation pilot selection, box auditing, and agreement metrics."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_pilot import (  # noqa: E402
    ImageAnnotationRecord,
    audit_box_list,
    compute_cohens_kappa_binary,
    independent_second_pass_verify,
    select_stratified_pilot_sample,
)


def test_audit_box_list_filters_degenerate_and_excluded() -> None:
    raw = [
        (0, "Implant", 100.0, 200.0, 180.0, 420.0, "ok"),
        (0, "Implant", 100.0, 200.0, 180.0, 420.0, "ok"),  # exact same-class duplicate IoU=1.0
        (None, "Root resorption", 300.0, 400.0, 350.0, 480.0, "excluded_class"),
        (5, "Bone resorbtion", 500.0, 600.0, 500.0, 600.0, "ok"),  # degenerate zero-area
        (2, "Obturation", -3.5, 100.0, 80.0, 190.0, "ok"),          # boundary overhang > 1px
    ]
    valid, excluded, anomalies = audit_box_list("DS0001_IMG_000001", "DS0001", 2652, 1536, raw)
    assert len(valid) == 2
    assert len(excluded) == 3
    assert any(a["issue_type"] == "degenerate_zero_area" for a in anomalies)
    assert any(a["issue_type"] == "same_class_duplicate_iou_gt_0.90" for a in anomalies)
    assert any(a["issue_type"] == "boundary_overhang_gt1px" for a in anomalies)
    assert valid[1].xmin == 0.0
    assert valid[0].round_trip_px_err < 0.01


def test_pilot_selection_and_kappa_agreement() -> None:
    recs: list[ImageAnnotationRecord] = []
    for i in range(1, 25):
        valid, excluded, anomalies = audit_box_list(
            f"DS0001_IMG_{i:06d}",
            "DS0001",
            2000,
            1000,
            [(10 if i <= 4 else 2, "test", 10.0 * i, 20.0, 10.0 * i + 60.0, 140.0, "ok")],
        )
        recs.append(
            ImageAnnotationRecord(
                image_id=f"DS0001_IMG_{i:06d}",
                dataset_id="DS0001",
                track_id="TrackA",
                source_bucket="internal_train",
                width=2000,
                height=1000,
                laplacian_var=float(100 + i * 10),
                annotation_state="reviewed_positive",
                raw_box_count=1,
                valid_boxes=valid,
                excluded_records=excluded,
                anomalies=anomalies,
            )
        )
    sample = select_stratified_pilot_sample(recs, n_total=10, seed=20261119)
    assert len(sample) == 10
    strata = {r.stratum for r in sample}
    assert "S1_rare_or_edge_class" in strata
    assert "S2_high_density_overlap" in strata
    assert "S3_quality_variation_tail" in strata

    all_a: list[int] = []
    all_b: list[int] = []
    for r in sample:
        v = independent_second_pass_verify(r)
        assert v["match_res"]["f1_agreement"] == 1.0
        all_a.extend(v["dispositions_a"])
        all_b.extend(v["dispositions_b"])
    k = compute_cohens_kappa_binary(all_a, all_b)
    assert k["agreement_pct"] == 100.0
    assert k["kappa"] == 1.0
