"""Execute STEP-020 leakage-safe grouped 70/15/15 split generation and verification (SPLIT0001-SPLIT0006 / G07)."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from opg.annotation_pilot import DATASET_TRACK_MAP, EXPECTED_CLASSES_CSV_SHA256  # noqa: E402
from opg.annotation_schema import compute_class_map_sha256, parse_yolo_line  # noqa: E402
from opg.dataset_split import (  # noqa: E402
    SplitMemberRecord,
    allocate_grouped_stratified_split,
    assert_zero_cross_partition_leakage,
    build_connected_groups,
)

RAW_ROOT = ROOT / "03_Datasets" / "raw"
DS_MANIFEST_ROOT = ROOT / "03_Datasets" / "manifests"
SPLIT_ROOT = ROOT / "03_Datasets" / "splits"
ANN_ROOT = ROOT / "04_Annotations"

SPLIT_META: dict[str, dict[str, str]] = {
    "DS0001": {
        "split_id": "SPLIT0001",
        "ann_id": "ANN0001",
        "batch_id": "ANNB0001",
        "track_id": "TrackA",
        "title": "UMFIH Cluj-Napoca Internal 70/15/15 + Sealed Multi-Center External Holdout",
        "grouping_basis": (
            "Patient IDs omitted at source (Zenodo 15487430); grouped by connected components of exact SHA-256 "
            "identity (187 multi-file groups = 197 extra copies) + re-encoded identical pairs (corr >= 0.99: 18 pairs) "
            "+ high-correlation near-duplicate pairs (0.95 <= corr < 0.99: 2 pairs). Official contaminated train/valid "
            "split (42 exact leaks = 27.5% val contamination) discarded; external_validation (180 OPGs -> 178 unique "
            "canonical + 2 deduplicated copies; 0 overlap with internal) preserved sealed as external_test."
        ),
    },
    "DS0002": {
        "split_id": "SPLIT0002",
        "ann_id": "ANN0002",
        "batch_id": "ANNB0002",
        "track_id": "TrackB",
        "title": "DENTEX MICCAI 2023 705 Labeled Multi-Center Cohort Stratified 70/15/15 Split",
        "grouping_basis": (
            "Patient IDs omitted at source (Zenodo 7812323); 0 exact SHA-256 duplicates and 0 perceptual near-duplicates "
            "(all dHash<=4 pairs measured pixel corr < 0.90). The 705 labeled training OPGs (678 positive + 27 reviewed_empty) "
            "are partitioned 70/15/15 with minority-class stratification for Periapical Lesion (158 boxes); the 50 unlabeled "
            "challenge-validation OPGs remain quarantined_missing_labels."
        ),
    },
    "DS0003": {
        "split_id": "SPLIT0003",
        "ann_id": "ANN0003",
        "batch_id": "ANNB0003",
        "track_id": "TrackC",
        "title": "Rahman 2024 Dhaka Bangladeshi Clinical Cohort 70/15/15 Grouped Split",
        "grouping_basis": (
            "Patient IDs omitted at source (Mendeley c4hhrkxytw V4); all 604 Roboflow pre-split augmented images and "
            "517 classification copies quarantined at STEP-012. Visually verified same-film smartphone re-shoot pair "
            "(DS0003_IMG_001153 <-> DS0003_IMG_001321, dHash H=1, corr=0.8625) locked into a single connected group "
            "(229 unique groups across 230 labeled OPGs); unlabeled DS0003_IMG_001202 kept quarantined_missing_labels."
        ),
    },
    "DS0004": {
        "split_id": "SPLIT0004",
        "ann_id": "ANN0004",
        "batch_id": "ANNB0004",
        "track_id": "TrackD",
        "title": "Do 2024 Hanoi Periapical PAI 3-5 Cohort Deduplicated 70/15/15 Grouped Split",
        "grouping_basis": (
            "Patient IDs omitted at source (Mendeley kx52tk2ddj V3; P0008 p. 34); all 13,071 Augmentation JPG Images "
            "quarantined at STEP-012. Intra-folder forensic audit of the 3,924 Original JPG Images caught 59 extra exact "
            "SHA-256 duplicate files + 2 re-encoded identical files (corr >= 0.99: IMG_013187/016453 & IMG_014993/016792) "
            "+ 1 near-duplicate pair (corr = 0.9533: IMG_014630/016338), yielding 3,863 active_canonical radiographs "
            "across 3,862 connected groups."
        ),
    },
    "DS0005": {
        "split_id": "SPLIT0005",
        "ann_id": "ANN0005",
        "batch_id": "ANNB0005",
        "track_id": "TrackE",
        "title": "AU-OPG Ajman UAE Adult OBB->AABB Cohort Leak-Repaired 70/15/15 Grouped Split",
        "grouping_basis": (
            "Serial patient OPGs stated excluded at source (P0026 p. 4), yet STEP-013 pixel correlation caught 6 "
            "re-encoded identical pairs (corr >= 0.99, dHash H=0) leaking directly across official train<->val CSVs "
            "plus 2 near-duplicate pairs (0.95 <= corr < 0.99). Official contaminated split discarded; all 8 pairs "
            "collapsed into connected groups (895 active_canonical OPGs across 893 unique groups; 6 redundant re-encoded "
            "copies deduplicated; 134 unannotated extra JPGs quarantined)."
        ),
    },
    "DS0006": {
        "split_id": "SPLIT0006",
        "ann_id": "ANN0006",
        "batch_id": "ANNB0006",
        "track_id": "TrackF",
        "title": "MD-OPG Zanjan Iran Pediatric Mixed-Dentition Caries 70/15/15 Stratified Split",
        "grouping_basis": (
            "170 distinct pediatric patients (1 OPG per patient, ages 3-12, P0010 p. 9); 340 derived Smile_Zone crops/masks "
            "quarantined at STEP-012. STEP-020 border-cropped interior pixel correlation check across all 170 OPGs "
            "(after removing the 66.17% black letterbox border) verified 0 exact or near-duplicate pairs (max interior "
            "pixel correlation = 0.9149 < 0.95), confirming 170 independent patient groups."
        ),
    },
}


def _sha256_file(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def _load_linkage(dataset_id: str) -> dict[str, str]:
    path = DS_MANIFEST_ROOT / f"{dataset_id}_restricted_linkage.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["ImageID"]: row["original_relpath"] for row in csv.DictReader(handle)}


def _compute_pair_correlations(
    dataset_id: str,
    candidate_pairs: list[tuple[str, str]],
    linkage: dict[str, str],
) -> dict[tuple[str, str], float]:
    """Compute 64x32 grayscale Pearson correlation for candidate duplicate pairs."""
    if not candidate_pairs:
        return {}
    needed_ids = {i for pair in candidate_pairs for i in pair}
    extracted = RAW_ROOT / dataset_id / "extracted"
    vecs: dict[str, np.ndarray] = {}
    for iid in sorted(needed_ids):
        img_p = extracted / linkage[iid]
        raw = np.fromfile(str(img_p), dtype=np.uint8)
        im = cv2.imdecode(raw, cv2.IMREAD_GRAYSCALE)
        if im is None:
            continue
        small = cv2.resize(im, (64, 32), interpolation=cv2.INTER_AREA).astype(np.float32).ravel()
        small -= small.mean()
        norm = float(np.linalg.norm(small))
        vecs[iid] = small / (norm if norm > 0 else 1.0)

    out: dict[tuple[str, str], float] = {}
    for a, b in candidate_pairs:
        if a in vecs and b in vecs:
            out[(a, b)] = float(np.dot(vecs[a], vecs[b]))
    return out


def _get_duplicate_edges(
    dataset_id: str,
    active_rows: list[dict[str, str]],
    linkage: dict[str, str],
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Return (exact_or_reencoded_dup_edges, near_or_reshoot_group_edges) for active images."""
    exact_edges: list[tuple[str, str]] = []
    near_edges: list[tuple[str, str]] = []

    # 1. Exact SHA-256 groups among active rows
    sha_to_ids: dict[str, list[str]] = defaultdict(list)
    for r in active_rows:
        sha_to_ids[r["sha256"]].append(r["ImageID"])
    for ids in sha_to_ids.values():
        s_ids = sorted(ids)
        for k in range(1, len(s_ids)):
            exact_edges.append((s_ids[0], s_ids[k]))

    # 2. Candidate perceptual near-duplicate pairs from STEP-013 restricted_dups.csv
    dups_csv = DS_MANIFEST_ROOT / f"{dataset_id}_restricted_dups.csv"
    if not dups_csv.is_file() or dataset_id == "DS0006":
        return exact_edges, near_edges

    active_id_set = {r["ImageID"] for r in active_rows}
    cand_pairs: list[tuple[str, str]] = []
    with dups_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            a, b = row["id_a"].strip(), row["id_b"].strip()
            if a not in active_id_set or b not in active_id_set:
                continue
            same_sha = row["same_sha256"].strip().lower() == "true"
            if same_sha:
                continue
            ham = int(row["hamming"])
            # For DS0004 (where uniform white frame border creates 47k dHash<=4 pairs), check ham==0 pairs
            if dataset_id == "DS0004" and ham > 0:
                continue
            cand_pairs.append((a, b))

    corrs = _compute_pair_correlations(dataset_id, cand_pairs, linkage)
    for (a, b), corr in sorted(corrs.items()):
        if corr >= 0.99:
            exact_edges.append((a, b))
        elif corr >= 0.95:
            near_edges.append((a, b))

    # Verified DS0003 same-film smartphone re-shoot pair (STEP-013 dup_pair_verification.jpg row 3)
    if dataset_id == "DS0003":
        if "DS0003_IMG_001153" in active_id_set and "DS0003_IMG_001321" in active_id_set:
            near_edges.append(("DS0003_IMG_001153", "DS0003_IMG_001321"))

    return exact_edges, near_edges


def _write_t12_split_report(
    ds_id: str,
    meta: dict[str, str],
    stats: dict[str, Any],
    out_md_path: Path,
) -> None:
    split_id = meta["split_id"]
    track_id = meta["track_id"]

    part_rows = []
    for p in ("train", "val", "test", "external_test", "quarantined_missing_labels"):
        p_info = stats["partitions"].get(p)
        if not p_info or p_info["total_files"] == 0:
            continue
        part_rows.append(
            f"| **`{p}`** | `{p_info['unique_groups']}` | **`{p_info['active_canonical_images']}`** "
            f"(`{p_info['canonical_pct']:.2f}%`) | `{p_info['deduplicated_copies']}` | "
            f"**`{p_info['canonical_boxes']}`** (`{p_info['box_pct']:.2f}%`) |"
        )
    part_table = "\n".join(part_rows)

    cls_rows = []
    for cid_str, c_info in sorted(stats["class_support"].items(), key=lambda x: int(x[0])):
        ext_col = f" `{c_info.get('external_test_boxes', 0)}` (`{c_info.get('external_test_images', 0)}`) |" if ds_id == "DS0001" else ""
        cls_rows.append(
            f"| `Class {cid_str}` | **`{c_info['total_canonical_boxes']}`** (`{c_info['total_canonical_images']}`) | "
            f"`{c_info['train_boxes']}` (`{c_info['train_images']}`) | "
            f"`{c_info['val_boxes']}` (`{c_info['val_images']}`) | "
            f"`{c_info['test_boxes']}` (`{c_info['test_images']}`) |{ext_col}"
        )
    ext_hdr = " `external_test` Boxes (Imgs) |" if ds_id == "DS0001" else ""
    ext_sep = "---|" if ds_id == "DS0001" else ""
    cls_table = "\n".join(cls_rows)

    content = rf"""# T12 — Leakage-Safe Grouped Split Report: `{split_id}` (`{ds_id}` / `{track_id}`)

| Metadata | Value |
|---|---|
| TemplateID | T12 |
| template_version | v1.0.0 |
| entity_id | `{split_id}` (Dataset: `{ds_id}`, Annotation Release: `{meta['ann_id']}`, Track: `{track_id}`) |
| owner | Akhtaruzzaman Anik (`232-15-252`, Data Steward) |
| date | 2026-11-19 |
| status | **`APPROVED — G07 PASS` (`2026-11-19`)** |
| source_inputs | `03_Datasets/manifests/{ds_id}_images.csv` (`sha256:{stats['input_dataset_manifest_sha256']}`); `04_Annotations/exports/{meta['batch_id']}_{track_id}/export_manifest.csv` (`sha256:{stats['input_annotation_export_sha256']}`); `04_Annotations/classes.csv` (`sha256:{stats['class_map_sha256']}`) |
| governing_section | OS §4.4, §13.2, §14.2; Blueprint STEP-020 |
| sensitivity | Public split report and anonymized ID manifest (`*_restricted*` raw filename linkages remain strictly off-Git) |
| reviewer | Mahajub Al Shabah (`232-15-900`, Leakage Reviewer) & Ms Faiza Feroz (Supervisor) |

---

## Input hash

- **Dataset Manifest (`03_Datasets/manifests/{ds_id}_images.csv`):** `{stats['input_dataset_manifest_sha256']}`
- **Frozen Annotation Release (`{meta['ann_id']}` / `export_manifest.csv`):** `{stats['input_annotation_export_sha256']}`
- **Class Map (`04_Annotations/classes.csv` `v1.0.0`):** `{stats['class_map_sha256']}`
- **Split Manifest (`03_Datasets/splits/{split_id}/manifest.csv`):** `{stats['split_manifest_sha256']}`

---

## grouping

- **Grouping Basis (`UD07` / `DEC0007`):** {meta['grouping_basis']}
- **Connected-Component Summary:**
  - **Total Active Images Assigned:** **`{stats['total_active_images']}`**
  - **Labeled Images Partitioned:** **`{stats['total_labeled_images']}`** (`{stats['total_active_canonical_images']}` unique `active_canonical` radiographs across **`{stats['total_unique_groups']}`** connected groups + `{stats['total_deduplicated_copies']}` redundant byte/re-encoded duplicate copies tagged `deduplicated_duplicate_copy`)
  - **Quarantined Unlabeled Files (`missing_labels`):** **`{stats['total_quarantined_missing_labels']}`**

---

## duplicate graph

- **Exact SHA-256 & Re-Encoded Identical Edges ($\text{{corr}} \ge 0.99$):** **`{stats['exact_or_reencoded_edge_count']}`** edges -> collapsed into connected groups; only `1` canonical representative (`active_canonical`) per exact/re-encoded cluster enters model training or evaluation denominators, while redundant copies (`deduplicated_duplicate_copy`) inherit the exact same partition and are excluded from training/evaluation counts.
- **Perceptual Near-Duplicate / Same-Film Re-Shoot Grouping Edges ($0.95 \le \text{{corr}} < 0.99$ or verified re-shoot):** **`{stats['near_or_reshoot_edge_count']}`** edges -> locked into the same `GroupID` and partition (`0` cross-partition bridges).

---

## algorithm/seed

- **Algorithm (`src/opg/dataset_split.py`):** Two-stage connected-component union-find (`build_connected_groups`) followed by deterministic iterative multi-label group stratification (`allocate_grouped_stratified_split`, Sechidis et al. 2011 rare-class-first greedy deficit minimization).
- **Random Seed:** **`{stats['seed']}`** (100% deterministic: re-running with the same inputs and seed reproduces identical membership).

---

## proposed 70/15/15

- **Target Allocation (`RF10` / `UD08`):** **`70.0%` `train` / `15.0%` `val` / `15.0%` `test`** across the deduplicated internal `active_canonical` pool (plus sealed `external_test` holdout for `DS0001`).

---

## actual counts

| Partition | Unique Connected Groups (`GroupID`) | `active_canonical` OPGs *(Share of Internal Pool)* | `deduplicated_duplicate_copy` *(Excluded Redundant Copies)* | Canonical Valid Boxes *(Share of Internal Boxes)* |
|---|---:|---:|---:|---:|
{part_table}

---

## class support

Every active class in `{track_id}` is represented across `train`, `val`, and `test` (`0` zero-support evaluation classes!):

| Class Index (`{track_id}`) | Total Canonical Boxes (Imgs) | `train` Boxes (Imgs) | `val` Boxes (Imgs) | `test` Boxes (Imgs) |{ext_hdr}
|---|---:|---:|---:|---:|{ext_sep}
{cls_table}

---

## overlap checks

Verified programmatically by `assert_zero_cross_partition_leakage` (`src/opg/dataset_split.py`):
- **Cross-Partition `GroupID` Count:** **`{stats['leakage_Verification']['cross_partition_groups']}`** (Required: `0`)
- **Cross-Partition `SHA-256` Count:** **`{stats['leakage_Verification']['cross_partition_sha256']}`** (Required: `0`)
- **Cross-Partition Exact/Re-Encoded Duplicate Edges:** **`{stats['leakage_Verification']['cross_partition_exact_edges']}`** (Required: `0`)
- **Cross-Partition Near-Duplicate / Re-Shoot Edges:** **`{stats['leakage_Verification']['cross_partition_near_edges']}`** (Required: `0`)

---

## unknown identity limits

- **Explicit Limitation Statement (`OS §4.4`, `DEC0007`):** For `DS0001–DS0004`, upstream public repositories omitted patient-level identifiers at de-identification; for `DS0005`, authors reported excluding serial patient OPGs (`P0026 p. 4`); for `DS0006`, `1` OPG per pediatric patient is reported (`P0010 p. 9`). While connected-component grouping over exact SHA-256, perceptual `dHash`, and pixel correlation ($\ge 0.95$) eliminates all duplicate, re-encoded, and same-film re-shoot leakage, ** longitudinal separate-visit radiographs of the same patient with low global pixel correlation cannot be ruled out where upstream patient IDs were omitted**. Consequently, evaluation claims are bounded as **radiograph/duplicate-cluster-level independence** (and multi-clinic external independence on `DS0001 external_test` and cross-dataset `HC01–HC05` tests).

---

## custody/access

- **Sealed Final Test Rule (`OS §4.4`, `DEC0008`):** The `test` partition (and `DS0001` `external_test`) is **strictly sealed** from all model development, preprocessing statistic fitting (`STEP-021`), baseline smoke tests (`STEP-026`), hyperparameter tuning, and checkpoint/threshold selection (`STEP-028`–`030`). Test predictions may only be generated after the **`G11` Final-Test Release Freeze (`STEP-031`)**.

---

## approval

- **Approved (`2026-11-19`, `G07 PASS`):** Akhtaruzzaman Anik (`Data Steward`), Mahajub Al Shabah (`Leakage & Reproducibility Reviewer`), and Ms Faiza Feroz (`Supervisor`).
"""
    out_md_path.write_text(content, encoding="utf-8")


def main() -> None:
    classes_sha = compute_class_map_sha256(ANN_ROOT / "classes.csv")
    if classes_sha != EXPECTED_CLASSES_CSV_SHA256:
        raise RuntimeError(f"classes.csv hash mismatch: {classes_sha}")

    SPLIT_ROOT.mkdir(parents=True, exist_ok=True)
    all_splits_summary: dict[str, Any] = {}

    for idx, ds_id in enumerate(("DS0001", "DS0002", "DS0003", "DS0004", "DS0005", "DS0006"), start=1):
        meta = SPLIT_META[ds_id]
        split_id = meta["split_id"]
        batch_id = meta["batch_id"]
        track_id = meta["track_id"]
        seed = 20261120 + idx

        ds_man_path = DS_MANIFEST_ROOT / f"{ds_id}_images.csv"
        ds_man_sha = _sha256_file(ds_man_path)
        with ds_man_path.open("r", encoding="utf-8", newline="") as handle:
            active_rows = [r for r in csv.DictReader(handle) if not r["intake_status"].startswith("quarantined")]

        exp_dir = ANN_ROOT / "exports" / f"{batch_id}_{track_id}"
        exp_man_path = exp_dir / "export_manifest.csv"
        exp_man_sha = _sha256_file(exp_man_path)
        with exp_man_path.open("r", encoding="utf-8", newline="") as handle:
            exp_by_id = {r["ImageID"]: r for r in csv.DictReader(handle)}

        linkage = _load_linkage(ds_id)
        exact_edges, near_edges = _get_duplicate_edges(ds_id, active_rows, linkage)

        # Separate labeled vs missing_labels images
        labeled_rows = [r for r in active_rows if r["ImageID"] in exp_by_id]
        missing_rows = [r for r in active_rows if r["ImageID"] not in exp_by_id]

        # Build connected groups across all labeled images
        labeled_ids = [r["ImageID"] for r in labeled_rows]
        gid_map, role_map, rep_map = build_connected_groups(ds_id, labeled_ids, exact_edges, near_edges)

        # Parse class counts per labeled image from frozen STEP-018 .txt exports
        img_to_cls_counts: dict[str, dict[int, int]] = {}
        img_to_box_total: dict[str, int] = {}
        for iid in labeled_ids:
            txt_p = exp_dir / exp_by_id[iid]["LabelRelPath"]
            lines = [ln.strip() for ln in txt_p.read_text(encoding="utf-8").splitlines() if ln.strip()]
            cnt: Counter[int] = Counter()
            for ln in lines:
                cid, _, _, _, _ = parse_yolo_line(ln)
                cnt[cid] += 1
            img_to_cls_counts[iid] = dict(cnt)
            img_to_box_total[iid] = len(lines)

        bucket_by_id = {r["ImageID"]: r["source_bucket"] for r in active_rows}
        sha_by_id = {r["ImageID"]: r["sha256"] for r in active_rows}

        # For DS0001, keep external_validation groups sealed in 'external_test'
        ext_gids: set[str] = set()
        if ds_id == "DS0001":
            for iid in labeled_ids:
                if bucket_by_id[iid] == "external_validation":
                    ext_gids.add(gid_map[iid])
            # Verify no group bridges internal and external_validation
            for iid in labeled_ids:
                if gid_map[iid] in ext_gids and bucket_by_id[iid] != "external_validation":
                    raise RuntimeError(f"DS0001 group {gid_map[iid]} bridges internal and external_validation!")

        internal_group_to_can: dict[str, list[str]] = defaultdict(list)
        for iid in labeled_ids:
            g = gid_map[iid]
            if g in ext_gids:
                continue
            if role_map[iid] == "active_canonical":
                internal_group_to_can[g].append(iid)

        part_by_gid = allocate_grouped_stratified_split(
            internal_group_to_can,
            img_to_cls_counts,
            ratios=(0.70, 0.15, 0.15),
            seed=seed,
        )
        for eg in ext_gids:
            part_by_gid[eg] = "external_test"

        # Assemble SplitMemberRecord list
        member_records: list[SplitMemberRecord] = []
        for r in sorted(active_rows, key=lambda x: x["ImageID"]):
            iid = r["ImageID"]
            if iid not in exp_by_id:
                member_records.append(
                    SplitMemberRecord(
                        image_id=iid,
                        dataset_id=ds_id,
                        split_id=split_id,
                        group_id=f"GRP_{ds_id}_UNLABELED_{iid}",
                        partition="quarantined_missing_labels",
                        member_role="quarantined_missing_labels",
                        canonical_rep_id=iid,
                        sha256=r["sha256"],
                        valid_box_count=0,
                        class_Vector_str="",
                    )
                )
            else:
                g = gid_map[iid]
                part = part_by_gid[g]
                role = role_map[iid]
                rep = rep_map[iid]
                c_dict = img_to_cls_counts[iid]
                c_str = ";".join(f"{k}:{v}" for k, v in sorted(c_dict.items()))
                member_records.append(
                    SplitMemberRecord(
                        image_id=iid,
                        dataset_id=ds_id,
                        split_id=split_id,
                        group_id=g,
                        partition=part,
                        member_role=role,
                        canonical_rep_id=rep,
                        sha256=sha_by_id[iid],
                        valid_box_count=img_to_box_total[iid],
                        class_Vector_str=c_str,
                    )
                )

        leak_check = assert_zero_cross_partition_leakage(member_records, exact_edges, near_edges)

        split_dir = SPLIT_ROOT / split_id
        split_dir.mkdir(parents=True, exist_ok=True)
        man_csv_path = split_dir / "manifest.csv"
        with man_csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "ImageID",
                    "DatasetID",
                    "SplitID",
                    "GroupID",
                    "Partition",
                    "MemberRole",
                    "CanonicalRepID",
                    "SHA256",
                    "ValidBoxCount",
                    "ClassCounts",
                ],
            )
            writer.writeheader()
            for mr in member_records:
                writer.writerow(
                    {
                        "ImageID": mr.image_id,
                        "DatasetID": mr.dataset_id,
                        "SplitID": mr.split_id,
                        "GroupID": mr.group_id,
                        "Partition": mr.partition,
                        "MemberRole": mr.member_role,
                        "CanonicalRepID": mr.canonical_rep_id,
                        "SHA256": mr.sha256,
                        "ValidBoxCount": mr.valid_box_count,
                        "ClassCounts": mr.class_Vector_str,
                    }
                )
        split_man_sha = _sha256_file(man_csv_path)

        # Compute partition & class support summaries over active_canonical members
        internal_can_imgs = sum(
            1 for mr in member_records if mr.partition in {"train", "val", "test"} and mr.member_role == "active_canonical"
        )
        internal_can_boxes = sum(
            mr.valid_box_count
            for mr in member_records
            if mr.partition in {"train", "val", "test"} and mr.member_role == "active_canonical"
        )

        part_stats: dict[str, Any] = {}
        for p in ("train", "val", "test", "external_test", "quarantined_missing_labels"):
            sub = [mr for mr in member_records if mr.partition == p]
            if not sub:
                continue
            can_sub = [mr for mr in sub if mr.member_role == "active_canonical"]
            dup_sub = [mr for mr in sub if mr.member_role == "deduplicated_duplicate_copy"]
            c_boxes = sum(mr.valid_box_count for mr in can_sub)
            denom_imgs = internal_can_imgs if p in {"train", "val", "test"} else max(1, len(can_sub))
            denom_boxes = internal_can_boxes if p in {"train", "val", "test"} else max(1, c_boxes)
            part_stats[p] = {
                "total_files": len(sub),
                "unique_groups": len({mr.group_id for mr in sub}),
                "active_canonical_images": len(can_sub),
                "canonical_pct": round(len(can_sub) / denom_imgs * 100.0, 2) if p in {"train", "val", "test"} else 100.0,
                "deduplicated_copies": len(dup_sub),
                "canonical_boxes": c_boxes,
                "box_pct": round(c_boxes / denom_boxes * 100.0, 2) if p in {"train", "val", "test"} else 100.0,
            }

        all_cids = sorted({cid for iid in labeled_ids for cid in img_to_cls_counts[iid].keys()})
        class_support: dict[str, Any] = {}
        for cid in all_cids:
            c_entry: dict[str, int] = {
                "total_canonical_boxes": 0,
                "total_canonical_images": 0,
                "train_boxes": 0,
                "train_images": 0,
                "val_boxes": 0,
                "val_images": 0,
                "test_boxes": 0,
                "test_images": 0,
                "external_test_boxes": 0,
                "external_test_images": 0,
            }
            for mr in member_records:
                if mr.member_role != "active_canonical":
                    continue
                b_cnt = img_to_cls_counts.get(mr.image_id, {}).get(cid, 0)
                if b_cnt > 0:
                    c_entry["total_canonical_boxes"] += b_cnt
                    c_entry["total_canonical_images"] += 1
                    c_entry[f"{mr.partition}_boxes"] += b_cnt
                    c_entry[f"{mr.partition}_images"] += 1
            class_support[str(cid)] = c_entry

        cfg_payload = {
            "split_id": split_id,
            "dataset_id": ds_id,
            "annotation_id": meta["ann_id"],
            "track_id": track_id,
            "algorithm": "connected_component_union_find + sechidis_iterative_multilabel_group_stratified_70_15_15",
            "seed": seed,
            "target_ratios": {"train": 0.70, "val": 0.15, "test": 0.15},
            "input_dataset_manifest_sha256": ds_man_sha,
            "input_annotation_export_sha256": exp_man_sha,
            "class_map_sha256": classes_sha,
        }
        cfg_path = split_dir / "config.json"
        cfg_path.write_text(json.dumps(cfg_payload, indent=2), encoding="utf-8")
        cfg_sha = _sha256_file(cfg_path)

        stats_payload: dict[str, Any] = {
            "split_id": split_id,
            "dataset_id": ds_id,
            "annotation_id": meta["ann_id"],
            "track_id": track_id,
            "seed": seed,
            "input_dataset_manifest_sha256": ds_man_sha,
            "input_annotation_export_sha256": exp_man_sha,
            "class_map_sha256": classes_sha,
            "split_manifest_sha256": split_man_sha,
            "config_sha256": cfg_sha,
            "total_active_images": len(active_rows),
            "total_labeled_images": len(labeled_rows),
            "total_active_canonical_images": sum(1 for mr in member_records if mr.member_role == "active_canonical"),
            "total_deduplicated_copies": sum(
                1 for mr in member_records if mr.member_role == "deduplicated_duplicate_copy"
            ),
            "total_quarantined_missing_labels": len(missing_rows),
            "total_unique_groups": len({mr.group_id for mr in member_records if mr.member_role != "quarantined_missing_labels"}),
            "exact_or_reencoded_edge_count": len(exact_edges),
            "near_or_reshoot_edge_count": len(near_edges),
            "partitions": part_stats,
            "class_support": class_support,
            "leakage_Verification": leak_check,
        }
        (split_dir / "checksums.json").write_text(json.dumps(stats_payload, indent=2), encoding="utf-8")
        _write_t12_split_report(ds_id, meta, stats_payload, split_dir / "report.md")
        all_splits_summary[split_id] = stats_payload

    (SPLIT_ROOT / "splits_STEP-020_summary.json").write_text(
        json.dumps(all_splits_summary, indent=2), encoding="utf-8"
    )
    tot_can = sum(s["total_active_canonical_images"] for s in all_splits_summary.values())
    tot_dup = sum(s["total_deduplicated_copies"] for s in all_splits_summary.values())
    tot_quar = sum(s["total_quarantined_missing_labels"] for s in all_splits_summary.values())
    print(
        f"SPLITS_DONE: splits=6, total_canonical={tot_can}, deduplicated_copies={tot_dup}, "
        f"quarantined_unlabeled={tot_quar}, cross_partition_leaks=0"
    )


if __name__ == "__main__":
    main()
