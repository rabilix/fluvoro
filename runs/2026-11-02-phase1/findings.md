# Phase 1 findings (turns 1–3)

Numbering continues the setup findings (F-001…F-018). Grading is against `kit/shown/` (RFQ, CRS); the only comparison with `product/` is the safety-goal ASILs in F-031.

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

- Each quotpilot turn starts with `fetch_requirements`, `analyze`, `decide`, `analyze_rfq`, `ask` called at once (corrected cause, Platform audit: the model's first tool round called them with `{}` because none declared parameters, not the pack prefetch; fixed in RE087) and failing in ~0.01 ms (`tool_failure`, no error text in the audit). Seen in the setup turn f3f52ac5… (QPMT rest) and in turn 1 (QPMT mock), so not backend-related. Continues F-018.
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

## F-027: myBrain presents an invalid key before the profile's key on reload

- After the facade restart, the myBrain reload produced `facade.handshake_refused` (reason `invalid_key`, tenant "operator", no principal) at 16:39:45Z, then a valid `facade.handshake` for fluvoro-operator one second later. Some other stored credential is tried first. Made visible by RE083.
- **Tier:** live (audit). **Demo-blocker:** no.

## F-028: the schedule auto-detect hijacks ordinary text ("concept" contains "once")

- **Seen (17:42 local):** the customer reply was answered "💡 I'll schedule: … When: Once at 2026-11-03 01:00 … Reply /schedule confirm to create it".
- **Cause (source, read-only test, confirmed by Platform audit at parser.py:230):** `flexcore.scheduler.parser` tests `"once" in t` as a substring, so "c-once-pt" ("concept") matches, and any digit in the message becomes the hour: `looks_schedulable("3 concept")` → True ("once" 03:00), "the 3 concepts" → True, "3 accept" → False. The answer-book text CA-03 contains "technical safety concept"; CA-01/CA-02 contain digits.
- **Second defect:** the auto-detect short-circuits in `runtime.py` before `request.start`; the turn leaves no audit row, turn record or outcome.
- **Workaround:** NL_SCHEDULE_AUTODETECT=false for the run (D-17). **Fix:** taken by Platform audit (whole-word matching with a false-positive corpus; audit rows for auto-detected turns).
- **Tier:** live + source. **Family:** F8 (words routed to the wrong path). **Demo-blocker:** yes (no write happens without `/schedule confirm`, but the customer scene breaks).

## F-029: the customer's answers are acknowledged but not used, and the analysis loops

- Turn 3 says "Thanks for the clarification on items 1‑3" but none of the content appears (80/20 split, ~50 000 units/year, connectivity 12 months after SOP with the interface carried from day one, a customer-named hardware partner with HSI spec and hardware safety requirements in our scope).
- The customer said "make an assumption, state it in your quotation"; FlexCortex lists 12 assumptions and asks the customer to confirm every one. No work packages, no quotation after three turns.
- **Tier:** live. **Family:** F1. **Demo-blocker:** yes.

## F-030: the default assumptions contradict the CRS and RFQ and invent context

- Battery "12 V Li‑ion, 500 mAh" vs CRS FLV-STK-038 (LiFePO4-class stability); "0.5 kg, standard DIN‑mounting" vs a gutter-outlet device (FLV-STK-110…124, ≤1.2 kg V1); "0 – 60 °C" vs −20…+50 °C operating (FLV-STK-050); schedule "D‑0…D‑270" vs RFQ §4 (B-sample 10/2027, C-sample 04/2028, SOP 09/2028); REST/MQTT/HTTPS, TPM, Azure IoT Hub and a "GateGuard REST endpoint" outside the RFQ scope (device side of BLE only); "EU‑AI Act"; budget "< €200 k" with no basis.
- **Tier:** live. **Family:** F1 (fabrication), F11. **Demo-blocker:** yes.

## F-031: the ASIL is assumed, not derived

- Turn 3 assumes "ASIL C (or SIL 3 if you prefer a SIL terminology)" without a HARA; the RFQ puts "HARA with ASIL determination" in the bidder's scope and the CRS gives no ASIL. Mixing ASIL (ISO 26262) and SIL (IEC 61508) as interchangeable is wrong.
- Reference (`product/hara.yaml`, reviewed HARA 0.2): SG-01 ASIL A, SG-02 ASIL C, SG-03 ASIL A. The highest value coincides with "C", but nothing in the turn derives it, and the per-goal split (two goals at A) is missing.
- **Tier:** live + reference. **Demo-blocker:** yes for the safety scene.

## F-032: `/schedule cancel` is audited without the person

- The cancel ran as `suggestions.dismiss` (turn record 9f92f949…) with tenant siimplex but no principal on the audit row, while the chat turns around it carry fluvoro-operator.
- **Tier:** live. **Demo-blocker:** no.

## Phase 1 summary

- Asked: what to develop, which work packages, which customer questions. Got: an automotive basic-software package list built from RFQ lines (CRS never read), no work packages in three turns, 15 customer questions of which 3 hit the RFQ's own open points (CA-01…03), none of the two unstated gaps (CA-04 reference site and season, CA-05 safety assessment), and a final loop asking the customer to confirm 12 invented assumptions.
- Infrastructure findings fixed during the phase by Platform audit and passed live: F-008 (RE083), F-009 (RE079), F-010 (RE084, not yet exercised), F-011 (RE080), listing records and outcome attribution (RE081/RE082).
