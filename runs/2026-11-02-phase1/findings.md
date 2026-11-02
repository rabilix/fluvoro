# Phase 1 findings (turns 1–2)

Numbering continues the setup findings (F-001…F-018). Grading here is against `kit/shown/` (RFQ, CRS) only; the comparison with `product/` follows at the end of the phase.

## F-019: QuotPilot analysed RFQ lines as requirements and never read the CRS

- **Seen:** "Packages detected: 17", "Project: Unknown", "All figures are derived from the supplied RFQ text and the attached CRS".
- **Record:** the draft holds 17 items QP-001…017, each a line of the RFQ ("**Date:** 2 November 2026", "**From:** …", headings, §5 points), all `Confirmed`, category "Unknown/unclear"; 0 of the 101 CRS requirements; the RFQ scope table (§2), quote items (§3) and schedule (§4) are absent (only the retrieved chunks were passed as `text`).
- **Expected:** the analysis reads the CRS (101 requirements) and the full RFQ; it does not state that the CRS was used when it was not.
- **Tier:** live + run directory. **Family:** F1 (phantom completeness / false provenance). **Demo-blocker:** yes.

## F-020: invented constraints and an automotive package frame

- **Seen:** constraints "Flash memory 256 KB", "Motor control loop 1 ms", "Maximum battery consumption 5 W", "Wireless data rate 1 Mbps"; mandatory packages BSW, EcuM, DEM, WdgM, Flash Bootloader, UDS, optional MCAL, NvM, XCP, COM stack; most cite `QP-006` (the RFQ's introductory paragraph) as "Explicit requirement".
- **Check:** none of the four constraints appears in `rfq.md` or the CRS; the CRS sets average monitoring consumption at 2 mW (FLV-STK-041). The package list is an automotive ECU basic-software catalogue for a solar gutter device; "Embedded non-AUTOSAR" is detected while AUTOSAR module names are listed.
- **Tier:** live. **Family:** F1 (fabrication), F11 (domain mismatch). **Demo-blocker:** yes.

## F-021: the model cannot hand a collection's files to a file-taking capability

- **Seen:** `quotpilot.analyze(files="['rfq.md', 'fluvoro_crs_v1.reqif']")` → "File validation failed".
- **Cause (source):** `flexops/capabilities/quotpilot.py` `_guard_files` resolves names against `FILES_ALLOWED_ROOT` (`~/Sandbox`); the files live at `~/Sandbox/knowledge_base/fluvoro/`. Nothing tells the model where an ingested collection's source files are, and the files argument was passed as a string, not a list.
- **Tier:** live + source. **Demo-blocker:** yes (with F-019).

## F-022: raw tool errors shown to the person, truncated

- The answer opens with two raw error payloads (JSON fragments, `—`, "next_actions", cut at "corre") before the review; footer "3 calls · 2 not ok".
- **Tier:** live. **Demo-blocker:** yes (visible in the first demo scene).

## F-023: QuotPilot's prefetch calls every read capability without arguments

- Each quotpilot turn starts with `fetch_requirements`, `analyze`, `decide`, `analyze_rfq`, `ask` called at once and failing in ~0.01 ms (`tool_failure`, no error text in the audit). Seen in the setup turn f3f52ac5… (QPMT rest) and in turn 1 (QPMT mock), so not backend-related. Continues F-018.
- **Tier:** live. **Demo-blocker:** no (noise, but hides real failures).

## F-024: no work packages, although asked

- Turn 1: "Work packages will be generated … when you say Go"; turn 2: none. The request asked "which work packages do you see"; RFQ §3.1 asks for effort per work package.
- **Tier:** live. **Demo-blocker:** yes for the quote scene.

## F-025: customer questions ignore the CRS and invent out-of-scope context

- Turn 2 asks for data the CRS or RFQ already gives (#6 battery → FLV-STK-030…043, #7 mechanics → 110…124, #8 environment → 050…057, #11 schedule → RFQ §4, #13 deliverables → FLV-STK-142) with example values that contradict the CRS ("12 V Li‑ion, 500 mAh", "0.5 kg" vs ≤1.2 kg and LiFePO4-class stability).
- It assumes a home network, cloud backend, REST/MQTT, existing infrastructure and legacy controls (#9, #14, #15), though RFQ §2 limits scope to the device side of BLE; it cites the EU AI Act.
- #4 asks the customer for the ASIL, which RFQ §2 puts in the bidder's scope (HARA with ASIL determination).
- **Not found:** the unstated reference site/season (CRS FLV-STK-030 uses "reference site" without defining it) and the functional safety assessment / independence.
- **Tier:** live. **Family:** F1, F11. **Demo-blocker:** yes.

## F-026: turn 1 framed the RFQ's open points as our decisions

- OC-001…003 restate RFQ §5.1–5.3 as internal decisions with recommended defaults ("Please reply with your choices … say Go") rather than as assumptions to state or questions to the customer; the RFQ asks the bidder to "state your assumption for each". Turn 2 then turned them into customer questions.
- **Tier:** live. **Demo-blocker:** no.
