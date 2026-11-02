# Phase 1 rerun: questions FlexCortex asked the customer

Rules as in Phase 1: answer texts only from `kit/hidden/customer_answer_book.yaml` (exact entry or fallback), only for questions FlexCortex actually asked.

## Turn 1 (trace 6f8f9b40-009f-4a62-817d-8017798b03b9): no customer questions

Four internal decisions for us with invented options and recommended defaults: OC-001 BLE timing (default "From launch"), OC-002 volume split (options "10 % V1 / 90 % V2" or "50/50", default 10/90), OC-003 hardware ("Supplier develops own electronics" recommended), OC-004 OS platform (Classic AUTOSAR recommended).

## Turn 2 (trace c4b738ed-b130-49b0-8018-6fdbef80d5f8): 10 customer questions

| # | Category (verbatim) | Answer-book entry | Note |
|---|---|---|---|
| 1 | Variant mix & volume | CA-01 | RFQ §5.1 |
| 2 | Connectivity timing | CA-02 | RFQ §5.2 |
| 3 | Hardware partner | CA-03 | RFQ §5.3 |
| 4 | OS platform | fallback | an architecture decision of the bidder; framed as "Classic AUTOSAR (our default)" |
| 5 | Optional feature packages | fallback | AUTOSAR modules incl. "UDS extensions" |
| 6 | Compliance & legal | fallback | markets/law given in CRS FLV-STK-090…098; cites EU AI Act, IEC 62351 |
| 7 | Test & validation | fallback | |
| 8 | Documentation | fallback | FLV-STK-142, -146 |
| 9 | Cost & schedule constraints | fallback | dates in RFQ §4; BOM target FLV-STK-144 |
| 10 | Environmental & packaging | fallback | CRS FLV-STK-050…057 |

## Customer reply (turn 3 prompt)

One message, verbatim: 1 → CA-01, 2 → CA-02, 3 → CA-03, 4–10 → fallback.

## Turn 3 (trace 95173335-e7ca-4188-8619-4265af6c9e19)

Nine "pending" items again addressed to the customer (optional features, OS platform, compliance incl. "ASIL D", test benches, documentation, budget/dates, environment, HW-SW interface specs, BLE stub), plus an assumptions table with the CA-01…03 content marked "Confirmed". Not answered (phase closed, D-23).

## Answer-book entries not reached

- CA-04 (reference site and season) and CA-05 (safety assessment) were not asked — same as Phase 1.
