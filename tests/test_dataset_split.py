"""Unit tests for STEP-020 connected-component grouping, 70/15/15 stratified splitting, and leakage assertions."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.dataset_split import (  # noqa: E402
    SplitMemberRecord,
    allocate_grouped_stratified_split,
    assert_zero_cross_partition_leakage,
    build_connected_groups,
)


def test_connected_groups_and_stratified_split_zero_leakage() -> None:
    img_ids = [f"DS0001_IMG_{i:06d}" for i in range(1, 45)]
    # Exact duplicate pair (1, 2) and re-encoded identical pair (3, 4)
    exact_edges = [("DS0001_IMG_000001", "DS0001_IMG_000002"), ("DS0001_IMG_000003", "DS0001_IMG_000004")]
    # Re-shoot pair (5, 6)
    near_edges = [("DS0001_IMG_000005", "DS0001_IMG_000006")]

    gid_map, role_map, rep_map = build_connected_groups("DS0001", img_ids, exact_edges, near_edges)
    assert gid_map["DS0001_IMG_000001"] == gid_map["DS0001_IMG_000002"]
    assert role_map["DS0001_IMG_000001"] == "active_canonical"
    assert role_map["DS0001_IMG_000002"] == "deduplicated_duplicate_copy"
    # Re-shoot pair shares GroupID but both have distinct exact roots
    assert gid_map["DS0001_IMG_000005"] == gid_map["DS0001_IMG_000006"]
    assert role_map["DS0001_IMG_000005"] == "active_canonical"
    assert role_map["DS0001_IMG_000006"] == "active_canonical"

    group_to_can: dict[str, list[str]] = {}
    for iid in img_ids:
        if role_map[iid] == "active_canonical":
            group_to_can.setdefault(gid_map[iid], []).append(iid)

    img_cls: dict[str, dict[int, int]] = {}
    for idx, iid in enumerate(img_ids):
        # Include rare class 10 on 6 images and common class 0 on all
        img_cls[iid] = {0: 2, 10: 1 if idx < 8 else 0}

    part_by_gid = allocate_grouped_stratified_split(group_to_can, img_cls, ratios=(0.70, 0.15, 0.15), seed=20261120)
    assert set(part_by_gid.values()) == {"train", "val", "test"}

    # Re-running with same seed must reproduce identical partition membership
    part_by_gid_2 = allocate_grouped_stratified_split(group_to_can, img_cls, ratios=(0.70, 0.15, 0.15), seed=20261120)
    assert part_by_gid == part_by_gid_2

    records = [
        SplitMemberRecord(
            image_id=iid,
            dataset_id="DS0001",
            split_id="SPLIT0001",
            group_id=gid_map[iid],
            partition=part_by_gid[gid_map[iid]],
            member_role=role_map[iid],
            canonical_rep_id=rep_map[iid],
            sha256="sha_12" if iid in ("DS0001_IMG_000001", "DS0001_IMG_000002") else f"sha_{iid}",
            valid_box_count=3,
            class_Vector_str="0:2",
        )
        for iid in img_ids
    ]
    res = assert_zero_cross_partition_leakage(records, exact_edges, near_edges)
    assert res["cross_partition_groups"] == 0
    assert res["cross_partition_sha256"] == 0

    # Inject a deliberate cross-partition leak and verify assertion fails
    bad_records = list(records)
    bad_records[1] = SplitMemberRecord(
        image_id="DS0001_IMG_000002",
        dataset_id="DS0001",
        split_id="SPLIT0001",
        group_id=gid_map["DS0001_IMG_000002"],
        partition="val" if records[0].partition != "val" else "test",
        member_role="deduplicated_duplicate_copy",
        canonical_rep_id="DS0001_IMG_000001",
        sha256="sha_12",
        valid_box_count=3,
        class_Vector_str="0:2",
    )
    with pytest.raises(RuntimeError, match="LEAKAGE DETECTED"):
        assert_zero_cross_partition_leakage(bad_records, exact_edges, near_edges)
