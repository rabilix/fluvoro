# Phase 1, third run: findings

Numbering continues after F-038. Grading against `kit/shown/` (RFQ, CRS).

## RE090 confirmed on the real kit (attempt A1, quotpilot run 2cb1c1ba…)

- Item domain "embedded device (consumer / industrial)", High; RFQ type "engineering service – quote system and software development effort", High.
- Platform "unclear – needs a decision", "none is assumed, and no baseline packages are added"; the platform question offers POSIX / Embedded non-AUTOSAR / Bare-metal MCU / RTOS with the rationale "an architecture must not be assumed from process standards".
- 14 device packages (energy management, BLE connectivity, functional safety, jam/overload detection, motor control, sensor acquisition, self-test, user indication, fault handling, time keeping, low-power management, service interface, event log, OTA), zero AUTOSAR packages, no ASIL "d", no supplier email ("Not applicable: … we are the supplier").
- RFQ parsed by paragraph: 17 items (was 43 line-split); 101 CRS requirements received.
- RFQ §5's three open points listed as clarification questions.

## F-039: the refused empty calls steer the model into asking the user instead of calling the tool

- A3 (trace 9b56c39c…): the first tool round again called all five quotpilot tools without arguments; they were refused with "missing required argument(s): project_id / run_id / text …". The model then did not call `analyze(collection=…)` but asked the person "What would you like the project to be called (e.g., {"name": "Fluvoro"})?", although the turn carried project fluvoro (the project-scoped pack was selected).
- Matches Platform audit's measurement (about 1 in 3 turns answers without the tool); the new error text appears to push the model toward the user.
- **Tier:** live. **Family:** cluster C. **Demo-blocker:** yes.

## F-040: a short follow-up loses the skill and the context, and the answer denies the data exists

- A3b (trace 3c060178…): the reply "Fluvoro" was routed with no skillpack; one retrieval for the bare word, then the model: "I don't have the RFQ (RFQ‑FLV‑2026‑01) or the accompanying customer‑requirements specification in the data you supplied … Please provide the RFQ text or a link to the file". Both are in the fluvoro collection, the first message said so, and 2 history messages were sent.
- Skill selection is per message; a short answer to the model's own question falls out of the pack and out of the task.
- **Tier:** live. **Family:** cluster C, F1 (false statement about available data). **Demo-blocker:** yes.

## F-041: evidence lists are too broad for "Explicit · High"

- A1 review: "Energy management · High · Explicit requirement" cites 37 ids, including FLV-STK-055 (IK08 impact), -077 (V-0 flammability), -094 (battery regulation), -146 (instructions); "Motor control" cites -100/-101 (radio), -093 (EMC). Keyword hits, not the requirement's own statement of the function.
- **Tier:** live. **Demo-blocker:** no (on RE090's follow-up list at Platform audit).

## F-042: extracted constraints regressed from 11 to 4

- A1: only 120 s, 30 s, SWE.1, SWE.6. The ce3a4d47 run extracted 11 correct ones (2 mW, 5 cycles, 65 dB(A), −20/−30 °C, 70 % after 5 years …). Possibly because A1 ran "Deterministic only" (no LLM assist under memory pressure); not re-measured.
- **Tier:** live. **Demo-blocker:** no (on RE090's follow-up list).

## F-043: a test tier loaded a 58 GB model into the live Ollama during the frozen run

- `qwen2.5:72b` (the crew review-judge model, 58 GB) was loaded next to gpt-oss:20b while A1 ran; Platform audit traced it to its own full test tier (`scripts/run_extended_tests.py` on a worktree) reaching the live daemon — a test defect. A1 hit myBrain's 180 s budget (turn record `halted` 22:44:29Z, no request.complete, no chat_turn outcome; server.log "Task was destroyed but it is pending" at routers/chat.py:739). The FlexCortex audit showed no caller — model load outside the core is invisible to it.
- The freeze covered deploys/restarts, not test runs against the live daemon.
- **Tier:** live. **Demo-blocker:** yes when it coincides.

## Summary

The catalogue/domain fix works: for the first time the analysis describes the right product, the right RFQ type and makes no platform assumption. The run still fails as a conversation: in three attempts it timed out (contention), asked for a project name, then denied having the data. The next blocker is cluster C (tool use and context across turns), not the catalogue.
