# TAB0006: Zero-shot cross-country domain-shift performance across 12 harmonized HC01–HC05 bridges spanning 5 countries (frozen source checkpoints and conf_op).

> **Provenance:** 09_Evaluation/xshift_metrics.csv (20 concept-bridge evaluations, 100% held-out coverage; CLAIM0015 / UD15).

| BridgeID | Source Model | Target Cohort | Harmonized Concept | GT | P | R | F1 | AP@0.50 | AP@0.50:95 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| XSHIFT01 | MODEL0005 (TrackA) | REL0005:test | HC03_Impacted_Tooth | 71 | 0.7442 | 0.4507 | 0.5614 | 0.6116 | 0.2513 |
| XSHIFT01 | MODEL0005 (TrackA) | REL0005:test | HC04_Residual_Root | 140 | 0.6338 | 0.3214 | 0.4265 | 0.3816 | 0.1195 |
| XSHIFT01 | MODEL0005 (TrackA) | REL0005:test | HC05_Dental_Implant | 80 | 0.4396 | 0.5000 | 0.4678 | 0.3189 | 0.1229 |
| XSHIFT02_INT | MODEL0008 (TrackE) | REL0001:test | HC03_Impacted_Tooth | 133 | 0.6489 | 0.4586 | 0.5374 | 0.3814 | 0.1684 |
| XSHIFT02_INT | MODEL0008 (TrackE) | REL0001:test | HC04_Residual_Root | 178 | 0.3970 | 0.4438 | 0.4191 | 0.2420 | 0.0726 |
| XSHIFT02_INT | MODEL0008 (TrackE) | REL0001:test | HC05_Dental_Implant | 70 | 0.1772 | 0.2000 | 0.1879 | 0.0723 | 0.0350 |
| XSHIFT02_EXT | MODEL0008 (TrackE) | REL0001:external_test | HC03_Impacted_Tooth | 111 | 0.6180 | 0.4955 | 0.5500 | 0.4935 | 0.2242 |
| XSHIFT02_EXT | MODEL0008 (TrackE) | REL0001:external_test | HC04_Residual_Root | 93 | 0.4109 | 0.5699 | 0.4775 | 0.3152 | 0.1158 |
| XSHIFT02_EXT | MODEL0008 (TrackE) | REL0001:external_test | HC05_Dental_Implant | 16 | 0.3548 | 0.6875 | 0.4681 | 0.4626 | 0.1970 |
| XSHIFT03_A | MODEL0005 (TrackA) | REL0003:test | HC03_Impacted_Tooth | 30 | 0.7727 | 0.5667 | 0.6538 | 0.7109 | 0.3752 |
| XSHIFT03_A | MODEL0005 (TrackA) | REL0003:test | HC04_Residual_Root | 15 | 0.2222 | 0.1333 | 0.1667 | 0.0844 | 0.0178 |
| XSHIFT03_E | MODEL0008 (TrackE) | REL0003:test | HC03_Impacted_Tooth | 30 | 0.7333 | 0.3667 | 0.4889 | 0.4469 | 0.2418 |
| XSHIFT03_E | MODEL0008 (TrackE) | REL0003:test | HC04_Residual_Root | 15 | 0.5385 | 0.4667 | 0.5000 | 0.5055 | 0.2245 |
| XSHIFT04_A | MODEL0005 (TrackA) | REL0002:test | HC03_Impacted_Tooth | 91 | 0.9155 | 0.7143 | 0.8025 | 0.8181 | 0.4083 |
| XSHIFT04_E | MODEL0008 (TrackE) | REL0002:test | HC03_Impacted_Tooth | 91 | 0.8723 | 0.4505 | 0.5942 | 0.6967 | 0.3472 |
| XSHIFT05_A2D | MODEL0005 (TrackA) | REL0004:test | HC02_Periapical_Lesion | 999 | 0.6471 | 0.0991 | 0.1719 | 0.2355 | 0.0573 |
| XSHIFT05_D2A_INT | MODEL0013 (TrackD) | REL0001:test | HC02_Periapical_Lesion | 142 | 0.1781 | 0.3662 | 0.2396 | 0.1779 | 0.0517 |
| XSHIFT05_D2A_EXT | MODEL0013 (TrackD) | REL0001:external_test | HC02_Periapical_Lesion | 106 | 0.1873 | 0.4717 | 0.2681 | 0.2163 | 0.0602 |
| XSHIFT06_E2B | MODEL0008 (TrackE) | REL0002:test | HC01_WholeTooth_Caries | 415 | 0.7818 | 0.1036 | 0.1830 | 0.1627 | 0.0919 |
| XSHIFT06_E2C | MODEL0008 (TrackE) | REL0003:test | HC01_WholeTooth_Caries | 30 | 0.3636 | 0.2667 | 0.3077 | 0.1635 | 0.0909 |
