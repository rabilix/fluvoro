# Phase 1: questions FlexCortex asked the customer

Answer texts are given only from `kit/hidden/customer_answer_book.yaml` (exact entry text, or its fallback) and only for questions FlexCortex actually asked. This file lists the CA ids only; the reply has **not been sent yet** (D-14: blind estimate first).

## Turn 1 (trace 2e5aef9f-c488-46df-b5bb-b18550c8a8f4): no customer questions

QuotPilot presented three **internal decisions** for us (OC-001 volume split, OC-002 connectivity timing, OC-003 hardware partner) with recommended defaults, and asked us to choose and say "Go". These restate RFQ §5 points 1–3. Nothing was addressed to the customer.

## Turn 2 (trace f7baba90-6e91-4dce-9481-e98b93daec47): 15 customer questions, verbatim titles

| # | Question (verbatim) | Answer-book entry | Note |
|---|---|---|---|
| 1 | Total production volume and mix of V1 vs. V2 for the first 2 years | CA-01 | RFQ §5.1 |
| 2 | When connectivity (Wi‑Fi/BT) must be available | CA-02 | RFQ §5.2; the RFQ specifies BLE, not Wi‑Fi |
| 3 | Hardware partner decision | CA-03 | RFQ §5.3 |
| 4 | Safety integrity level (SIL) / ASIL | fallback | ASIL determination is in the bidder's scope (RFQ §2 "HARA with ASIL determination") |
| 5 | Safety‑case and test‑environment requirements | fallback | not the CA-05 topic (assessment / independence) |
| 6 | Battery/charging specs | fallback | specified in CRS FLV-STK-030…043 |
| 7 | Mechanical constraints (size, weight, mounting method) | fallback | specified in CRS FLV-STK-110…124 |
| 8 | Environmental test conditions | fallback | specified in CRS FLV-STK-050…057 |
| 9 | Interface specifications | fallback | home network / cloud not in scope (RFQ §2: device side of BLE only) |
| 10 | Data‑privacy & security | fallback | CRS FLV-STK-100…103 |
| 11 | Release schedule & milestones | fallback | given in RFQ §4 |
| 12 | Cost constraints & budget envelope | fallback | |
| 13 | Documentation & certification deliverables | fallback | CRS FLV-STK-142 |
| 14 | Existing infrastructure (e.g., PLC, cloud platform, CI/CD pipeline) | fallback | |
| 15 | Any legacy or integration requirements (e.g., existing gutter‑system controls) | fallback | |

## Answer-book entries not reached

- **CA-04** (unstated in the RFQ: reference site and season) and **CA-05** (unstated: safety assessment) were not asked in turns 1–2.
