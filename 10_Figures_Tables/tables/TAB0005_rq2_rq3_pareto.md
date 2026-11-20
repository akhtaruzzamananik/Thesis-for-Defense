# TAB0005: RQ3 serial BS=1 FP32 end-to-end latency, throughput (FPS_e2e vs FPS_infer), artifact footprint, and ONNX parity across Kaggle Tesla T4 GPU and Intel i5-1135G7 CPU.

> **Provenance:** 09_Evaluation/timing/*_{gpu,cpu_onnx}_timing.json & 09_Evaluation/freeze_manifest.json (10 warm-up + 100 timed OPGs, 0 errors; UD14).

| ModelID | Track (Arch@imgsz) | .pt / .onnx (MB) | Test mAP50 (mAP50-95) | GPU T_e2e mean/p95 (ms) | GPU FPS_e2e (inf) | CPU T_e2e mean/p95 (ms) | CPU FPS_e2e (inf) | ONNX IoU |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MODEL0005 | TrackA (YOLO11s@1280) | 18.4 / 36.6 | 0.4165 (0.1741) | 108.2 / 118.7 | 9.24 (20.20) | 878.1 / 1224.0 | 1.14 (1.24) | 0.9923 |
| MODEL0001 | TrackA (YOLO11s@640) | 18.3 / 36.2 | 0.3815 (0.1577) | 71.4 / 78.0 | 14.00 (37.63) | 263.4 / 402.7 | 3.80 (4.92) | 0.9954 |
| MODEL0002 | TrackA (YOLOv8s@640) | 21.5 / 42.7 | 0.3786 (0.1578) | 74.5 / 81.5 | 13.42 (34.12) | 266.0 / 330.7 | 3.76 (4.62) | 0.9842 |
| MODEL0003 | TrackA (YOLO11m@640) | 38.7 / 76.7 | 0.3990 (0.1682) | 76.1 / 82.6 | 13.14 (32.03) | 512.4 / 706.0 | 1.95 (2.17) | 0.9965 |
| MODEL0004 | TrackB (YOLO11s@640) | 18.3 / — | 0.4397 (0.2673) | 72.6 / 77.9 | 13.78 (36.46) | Not exported | — | — |
| MODEL0006 | TrackC (YOLO11s@640) | 18.3 / — | 0.2508 (0.1406) | 26.2 / 38.8 | 38.20 (70.39) | Not exported | — | — |
| MODEL0013 | TrackD (YOLO11s@1280) | 18.4 / 36.6 | 0.4868 (0.2207) | 90.4 / 93.1 | 11.06 (20.75) | 847.9 / 1002.0 | 1.18 (1.27) | 0.9941 |
| MODEL0010 | TrackD (YOLO11s@640) | 18.3 / 36.1 | 0.4419 (0.1836) | 56.3 / 58.1 | 17.77 (42.39) | 181.9 / 215.4 | 5.50 (7.07) | 0.9829 |
| MODEL0008 | TrackE (YOLO11s@640) | 18.3 / 36.1 | 0.8246 (0.5163) | 81.4 / 85.6 | 12.28 (35.77) | 201.6 / 225.5 | 4.96 (7.08) | 0.9942 |
| MODEL0007 | TrackF (YOLO11s@640) | 18.3 / — | 0.0537 (0.0111) | 157.4 / 172.2 | 6.35 (35.88) | Not exported | — | — |
