# Phase 1 rerun findings and comparison

Numbering continues after F-032. Grading against `kit/shown/` (RFQ, CRS); the ASIL comparison uses `product/hara.yaml`.

## Comparison: Phase 1 (3d67ba1a/c63de2a6, infra-mixed) vs rerun (ce3a4d47, one commit)

| Criterion | Phase 1 | Rerun |
|---|---|---|
| Input read | 0 of 101 CRS reqs; RFQ lines as "requirements" | **101 of 101** + RFQ (43 line-split items) |
| Sources stated honestly | no ("RFQ text and the attached CRS") | **yes**, with counts |
| Extracted constraints | 4 of 4 invented | **11 of 12 correct and traceable**; 1 wrong ("asil d", F-034) |
| Platform / packages | automotive BSW list, "Embedded non-AUTOSAR" | **Classic AUTOSAR**, RTE/OS/MCAL/COM… "High · Explicit" (F-033) |
| Work packages | none in 3 turns | 11 in turn 3, AUTOSAR-shaped, no SYS/SWE core, no effort |
| Customer questions (recall of CA-01…05) | 3 of 5 | 3 of 5 (CA-04, CA-05 missed again) |
| Customer questions (precision) | 3 of 15 | 3 of 10; no invented example values, but the AUTOSAR frame reaches the customer |
| Customer answers used | no | **yes** (80/20 → 40 k/10 k, BLE +12 months), but CA-03 read backwards (F-036) |
| ASIL | "ASIL C (or SIL 3)", assumed | "ASIL D", assumed, likely from F-034 |
| Raw tool output on screen | yes, errors, truncated | one raw call line, no errors shown |
| First tool round | 5 empty calls, no reason | 5 empty calls, **with reasons** (F-035) |

Cluster A (RE087) fixed what it targeted: whole input, honest sources, traceable constraints. The remaining failures are cluster B/C plus the tool's domain (F-033).

## F-033: QuotPilot's closed automotive catalogue forces an AUTOSAR frame on a non-automotive item

- **Seen:** "Detected Platform: Classic AUTOSAR (confidence: Medium) · Evidence: FLV-STK-070, FLV-STK-092, FLV-STK-140"; RTE and OS "High · Explicit requirement · FLV-STK-070, FLV-STK-142"; MCAL, COM stack, WdgM "High · Explicit requirement · FLV-STK-015, FLV-STK-016"; baseline BSW, UDS, Watchdog; turn 3 work packages "BSW core: RTE, OS, MCAL, COM, DEM, DCM, NvM, WdgM, BswM, EcuM" and "UDS … Included by default"; a "Supplier Email EN" requesting a quotation for a "Software Integration Package (SIP)".
- **Cause (source, `packages/quotpilot/src/quotpilot/catalog.py`):** closed vocabularies — 7 platforms (Classic/Adaptive AUTOSAR, QNX, POSIX, Embedded non-AUTOSAR, Bootloader-only, unclear) and only AUTOSAR/vehicle packages; `BASELINE` adds UDS and Flash Bootloader to every platform, Classic AUTOSAR adds WdgM, Watchdog, DCM, DEM etc. Nothing can express Fluvoro's content (motor/jam control, clog detection, solar/battery energy management, BLE GATT, service interface, event log).
- **Platform inferred from process standards:** FLV-STK-070 (ISO 26262), -092 (IEC 60730 Class B), -140 (Automotive SPICE) state no architecture; the RFQ/CRS/product contain "AUTOSAR" zero times and no UDS or watchdog.
- **Labels overstate:** items the tool itself marks "(LLM-inferred)" are labelled "Explicit requirement" and "High".
- **Purpose mismatch:** the tool drafts a request to a basic-software supplier; the RFQ asks us to quote system and software development effort.
- **Maintainer's statement:** the first QuotPilot was built to recognise automotive quoting requests and look for AUTOSAR evidence; other domains need more sensitivity to stakeholder requirements; RTE, OS, MCAL at High confidence "cannot be".
- **Status:** fix requested from Platform audit (domain-sensitive identification, extensible catalogue, no forced baselines, honest confidence/source, RFQ-type recognition). **Tier:** live + source. **Family:** F11 (domain mismatch), F1. **Demo-blocker:** yes.

## F-034: the extractor reads "ASIL d" out of "ASIL determination"

- Constraint `{kind: asil, value: "d", requirement_ids: [QP-017]}`; QP-017 is the RFQ scope line "…item definition, HARA with ASIL determination, …".
- Turn 3 then assumes "Safety: ASIL D — Default for high‑consequence automotive system" and plans an "ASIL D safety case". Reference HARA 0.2: SG-01 A, SG-02 C, SG-03 A. A deterministic parsing defect becomes a safety assumption that roughly doubles the safety effort.
- **Tier:** live (draft) + reference. **Demo-blocker:** yes (safety scene).

## F-035: the first tool round still calls every quotpilot tool without arguments

- Despite RE087's declared input schemas, turn 1 again calls fetch_requirements, analyze, decide, analyze_rfq, ask with no arguments; now each fails with a stated reason ("project_id is required", "run_id is required", …). Then `analyze(collection='fluvoro')` succeeds. Corrects the F-023 expectation: the reasons are fixed, the behaviour is not.
- **Tier:** live (audit). **Demo-blocker:** no.

## F-036: the hardware-partner answer is read backwards

- CA-03 (sent verbatim) says our scope includes the hardware-software interface specification and the hardware safety requirements, which the partner designs to. Turn 3 asks Kestrel to "Provide the hardware‑software interface specification and hardware safety requirements from the hardware partner" ("We need those specs") and lists WP8 "Hardware‑software interface — Provided by Kestrel".
- **Tier:** live. **Family:** F1. **Demo-blocker:** yes.

## F-037: the proposed work packages miss the engineering core and carry no effort

- Turn 3's eleven work packages contain no system engineering (SYS.1–5), no software requirements/architecture (SWE.1–2), none of the device's application functions, and no person-days, although RFQ §3.1 asks for effort per work package by role.
- **Tier:** live. **Demo-blocker:** yes for the quote scene.

## F-038: assumptions and references still drift from the CRS/RFQ

- Turn 3: markets "EU, US, China" / "EU (CE), US (FCC)" vs CRS FLV-STK-090…098 (EU regulations only); environmental matrix "beyond what is in FLV‑STK‑063" (063 is the noise limit; environment is 050–057); asks for milestone dates given in RFQ §4; ISO 21434 "CSMS (full) — standard for automotive electronic control units" for a first release without radio; turn 1 volume options "10/90 or 50/50" justified by "V1 is a retrofit niche", which neither RFQ nor CRS says.
- **Tier:** live. **Family:** F1, F11. **Demo-blocker:** no.
