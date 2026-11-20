# TAB0003: Controlled 13-experiment training matrix (EXP0001–EXP0013, seed=20261124), validation selection metrics, and pre-test FREEZE0001 disposition.

> **Provenance:** 07_Experiments/experiment_registry.csv & 09_Evaluation/freeze_manifest.json (G10–G11 PASS; 0 sealed test access during selection).

| ExpID | RQs | Release | Architecture | Preprocessing | val mAP@50 | val mAP50-95 | conf_op | G11 Disposition |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| EXP0001 | RQ0; RQ1 | REL0001 | YOLO11s | PP0001 (Raw 640) | 0.3792 | 0.1570 | 0.238 | Frozen (MODEL0001, rq1_rq3_comparator) |
| EXP0002 | RQ1; RQ3 | REL0001 | YOLOv8s | PP0001 (Raw 640) | 0.3637 | 0.1523 | 0.197 | Frozen (MODEL0002, rq1_rq3_comparator) |
| EXP0003 | RQ0; RQ1 | REL0002 | YOLO11s | PP0001 (Raw 640) | 0.4438 | 0.2913 | 0.210 | Frozen (MODEL0004, track_winner) |
| EXP0004 | RQ0; RQ1 | REL0003 | YOLO11s | PP0001 (Raw 640) | 0.2588 | 0.1506 | 0.075 | Frozen (MODEL0006, track_winner) |
| EXP0005 | RQ0; RQ1 | REL0004 | YOLO11s | PP0001 (Raw 640) | 0.4878 | 0.2117 | 0.205 | Frozen (MODEL0010, rq2_rq3_comparator) |
| EXP0006 | RQ0; RQ1 | REL0005 | YOLO11s | PP0001 (Raw 640) | 0.8580 | 0.5705 | 0.379 | Frozen (MODEL0008, track_winner) |
| EXP0007 | RQ0; RQ1 | REL0006 | YOLO11s | PP0001 (Raw 640) | 0.0991 | 0.0300 | 0.091 | Frozen (MODEL0007, track_winner) |
| EXP0008 | RQ2 | REL0001 | YOLO11s | PP0002 (CLAHE 2.0) | 0.344 | — | Excluded | Excluded at G11 (MODEL0011, CLAHE hurt) |
| EXP0009 | RQ2 | REL0001 | YOLO11s | PP0003 (CLAHE 3.0) | 0.363 | — | Excluded | Excluded at G11 (MODEL0012, CLAHE hurt) |
| EXP0010 | RQ2; RQ3 | REL0001 | YOLO11s | PP0004 (1280px) | 0.3906 | 0.1656 | 0.227 | Frozen (MODEL0005, track_winner) |
| EXP0011 | RQ2; RQ3 | REL0004 | YOLO11s | PP0004 (1280px) | 0.5360 | 0.2514 | 0.201 | Frozen (MODEL0013, track_winner) |
| EXP0012 | RQ2 | REL0003 | YOLO11s | PP0002 (CLAHE 2.0) | 0.232 | — | Excluded | Excluded at G11 (MODEL0009, CLAHE hurt) |
| EXP0013 | RQ1; RQ3 | REL0001 | YOLO11m | PP0001 (Raw 640) | 0.3906 | 0.1583 | 0.253 | Frozen (MODEL0003, rq1_rq3_comparator) |
