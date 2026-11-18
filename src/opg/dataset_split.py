"""Deterministic connected-component grouping, multi-label stratified 70/15/15 split, and leakage assertions (STEP-020 / G07)."""

from __future__ import annotations

import hashlib
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class SplitMemberRecord:
    """Single row in 03_Datasets/splits/SPLIT####/manifest.csv."""

    image_id: str
    dataset_id: str
    split_id: str
    group_id: str
    partition: str  # train, val, test, external_test, quarantined_missing_labels
    member_role: str  # active_canonical, deduplicated_duplicate_copy, quarantined_missing_labels
    canonical_rep_id: str
    sha256: str
    valid_box_count: int
    class_Vector_str: str


class UnionFind:
    """Deterministic union-find over string ImageIDs keeping lexicographically smallest root."""

    def __init__(self, elements: Iterable[str]) -> None:
        self.parent: dict[str, str] = {e: e for e in sorted(set(elements))}

    def find(self, x: str) -> str:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        curr = x
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt
        return root

    def union(self, a: str, b: str) -> None:
        if a not in self.parent or b not in self.parent:
            return
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if ra < rb:
            self.parent[rb] = ra
        else:
            self.parent[ra] = rb


def build_connected_groups(
    dataset_id: str,
    image_ids: Sequence[str],
    exact_or_reencoded_dup_edges: Iterable[tuple[str, str]],
    near_or_reshoot_group_edges: Iterable[tuple[str, str]],
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Build connected-component GroupIDs and distinguish redundant exact/re-encoded copies from grouped members.

    Returns:
        (group_id_by_image, role_by_image, canonical_rep_by_image)
        - exact_or_reencoded_dup_edges: byte-identical (same SHA-256) or re-encoded identical (corr >= 0.99) pairs.
          Within each exact-duplicate sub-component, only the lexicographically first ImageID is 'active_canonical';
          extra identical copies are 'deduplicated_duplicate_copy'.
        - near_or_reshoot_group_edges: same-film re-shoots or 0.95 <= corr < 0.99 near-matches. They share the same
          outer GroupID (locked into the same train/val/test partition), while remaining 'active_canonical' unless
          also byte/re-encoded identical to another image.
    """
    sorted_ids = sorted(set(image_ids))
    uf_exact = UnionFind(sorted_ids)
    uf_group = UnionFind(sorted_ids)

    for a, b in exact_or_reencoded_dup_edges:
        uf_exact.union(a, b)
        uf_group.union(a, b)

    for a, b in near_or_reshoot_group_edges:
        uf_group.union(a, b)

    # Map outer connected component root -> stable GroupID GRP_DS####_0001..
    roots = sorted({uf_group.find(i) for i in sorted_ids})
    root_to_gid = {r: f"GRP_{dataset_id}_{idx:04d}" for idx, r in enumerate(roots, start=1)}

    group_id_by_image: dict[str, str] = {}
    role_by_image: dict[str, str] = {}
    canonical_rep_by_image: dict[str, str] = {}

    for iid in sorted_ids:
        g_root = uf_group.find(iid)
        e_root = uf_exact.find(iid)
        group_id_by_image[iid] = root_to_gid[g_root]
        canonical_rep_by_image[iid] = e_root
        role_by_image[iid] = "active_canonical" if iid == e_root else "deduplicated_duplicate_copy"

    return group_id_by_image, role_by_image, canonical_rep_by_image


def allocate_grouped_stratified_split(
    group_to_canonical_images: dict[str, list[str]],
    image_to_class_counts: dict[str, dict[int, int]],
    *,
    ratios: tuple[float, float, float] = (0.70, 0.15, 0.15),
    seed: int = 20261120,
) -> dict[str, str]:
    """Deterministically assign each GroupID to ('train', 'val', 'test') preserving group integrity and rare classes.

    Uses iterative multi-label group stratification (Sechidis et al. 2011):
    1. Aggregate object counts per class at the GroupID level over active_canonical images.
    2. Iteratively process the rarest class with unassigned groups, allocating groups to ('train', 'val', 'test')
       to match `ratios` both in class support and total canonical image counts.
    """
    if abs(sum(ratios) - 1.0) > 1e-6:
        raise ValueError(f"Split ratios must sum to 1.0, got {ratios}")

    partitions = ("train", "val", "test")
    ratio_map = dict(zip(partitions, ratios))

    gids = sorted(group_to_canonical_images.keys())
    total_canonical_imgs = sum(len(group_to_canonical_images[g]) for g in gids)
    target_imgs = {p: total_canonical_imgs * ratio_map[p] for p in partitions}

    # Aggregate class box counts per group
    group_class_counts: dict[str, Counter[int]] = {}
    total_class_boxes: Counter[int] = Counter()
    all_classes: set[int] = set()
    for g in gids:
        cnt: Counter[int] = Counter()
        for iid in group_to_canonical_images[g]:
            for cid, cval in image_to_class_counts.get(iid, {}).items():
                if cval > 0:
                    cnt[cid] += cval
                    total_class_boxes[cid] += cval
                    all_classes.add(cid)
        group_class_counts[g] = cnt

    target_class_boxes: dict[int, dict[str, float]] = {
        c: {p: total_class_boxes[c] * ratio_map[p] for p in partitions} for c in all_classes
    }

    rng = random.Random(seed)
    unassigned: set[str] = set(gids)
    assigned_partition: dict[str, str] = {}
    current_imgs: dict[str, int] = {p: 0 for p in partitions}
    current_class_boxes: dict[int, dict[str, int]] = {c: {p: 0 for p in partitions} for c in all_classes}
    current_class_groups: dict[int, dict[str, int]] = {c: {p: 0 for p in partitions} for c in all_classes}

    def _assign(g: str, part: str) -> None:
        assigned_partition[g] = part
        unassigned.remove(g)
        current_imgs[part] += len(group_to_canonical_images[g])
        for cid, cval in group_class_counts[g].items():
            current_class_boxes[cid][part] += cval
            current_class_groups[cid][part] += 1

    # Iterative multi-label allocation ordered from rarest class to most frequent
    while unassigned:
        # Find remaining classes present in unassigned groups
        rem_class_group_counts = {
            c: sum(1 for g in unassigned if group_class_counts[g].get(c, 0) > 0) for c in all_classes
        }
        active_rem_classes = [c for c, cnt in rem_class_group_counts.items() if cnt > 0]

        if not active_rem_classes:
            # Remaining groups have 0 boxes (reviewed_empty true negative groups)
            empty_gids = sorted(unassigned)
            rng.shuffle(empty_gids)
            for g in empty_gids:
                best_p = max(
                    partitions,
                    key=lambda p: (target_imgs[p] - current_imgs[p]) / max(1.0, target_imgs[p]),
                )
                _assign(g, best_p)
            break

        # Pick rarest remaining class (tie-break by total_class_boxes then class_id)
        rarest_c = min(active_rem_classes, key=lambda c: (rem_class_group_counts[c], total_class_boxes[c], c))
        cand_groups = sorted(g for g in unassigned if group_class_counts[g].get(rarest_c, 0) > 0)
        rng.shuffle(cand_groups)
        # Sort by box count of rarest_c descending so larger groups anchor train/val/test first
        cand_groups.sort(key=lambda g: (-group_class_counts[g][rarest_c], -sum(group_class_counts[g].values())))

        for g in cand_groups:
            if g not in unassigned:
                continue
            # Ensure every partition gets at least 1 group of rarest_c if possible (train, then test, then val)
            zero_parts = [p for p in ("train", "test", "val") if current_class_groups[rarest_c][p] == 0]
            if zero_parts:
                chosen_p = zero_parts[0]
            else:
                # Choose partition maximizing weighted relative deficit across class boxes & total images
                def _score(p: str) -> float:
                    cls_def = (
                        target_class_boxes[rarest_c][p] - current_class_boxes[rarest_c][p]
                    ) / max(1.0, target_class_boxes[rarest_c][p])
                    img_def = (target_imgs[p] - current_imgs[p]) / max(1.0, target_imgs[p])
                    return 0.70 * cls_def + 0.30 * img_def

                chosen_p = max(partitions, key=_score)
            _assign(g, chosen_p)

    return assigned_partition


def assert_zero_cross_partition_leakage(
    records: Sequence[SplitMemberRecord],
    exact_or_reencoded_dup_edges: Iterable[tuple[str, str]],
    near_or_reshoot_group_edges: Iterable[tuple[str, str]],
) -> dict[str, int]:
    """Verify zero GroupID, SHA-256, or duplicate/near-duplicate edge crosses train/val/test/external_test."""
    eval_records = [r for r in records if r.partition in {"train", "val", "test", "external_test"}]
    part_by_img = {r.image_id: r.partition for r in eval_records}
    parts_by_group: dict[str, set[str]] = defaultdict(set)
    parts_by_sha: dict[str, set[str]] = defaultdict(set)

    for r in eval_records:
        parts_by_group[r.group_id].add(r.partition)
        parts_by_sha[r.sha256].add(r.partition)

    cross_group = sum(1 for g, ps in parts_by_group.items() if len(ps) > 1)
    cross_sha = sum(1 for s, ps in parts_by_sha.items() if len(ps) > 1)
    cross_exact_edge = 0
    for a, b in exact_or_reencoded_dup_edges:
        if a in part_by_img and b in part_by_img and part_by_img[a] != part_by_img[b]:
            cross_exact_edge += 1
    cross_near_edge = 0
    for a, b in near_or_reshoot_group_edges:
        if a in part_by_img and b in part_by_img and part_by_img[a] != part_by_img[b]:
            cross_near_edge += 1

    if cross_group > 0 or cross_sha > 0 or cross_exact_edge > 0 or cross_near_edge > 0:
        raise RuntimeError(
            f"LEAKAGE DETECTED: cross_group={cross_group}, cross_sha={cross_sha}, "
            f"cross_exact_edge={cross_exact_edge}, cross_near_edge={cross_near_edge}"
        )

    return {
        "evaluated_records": len(eval_records),
        "unique_groups": len(parts_by_group),
        "cross_partition_groups": cross_group,
        "cross_partition_sha256": cross_sha,
        "cross_partition_exact_edges": cross_exact_edge,
        "cross_partition_near_edges": cross_near_edge,
    }
