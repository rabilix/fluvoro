# Phase 1, sixth run: findings

Numbering continues after F-049.

## Run 5 fixes, checked on T1 (trace b894dca7-3f96-45d3-8c01-9f28dc2184af)

- **F-047 (pre-fetch with empty kwargs): mostly closed.** server.log shows `auto-invoke quotpilot.fetch_requirements/decide/analyze_rfq/ask skipped: it requires […]`. One call still fires empty: see F-050.
- **F-048 (turn budget, analyze finality, chat saved): closed for this turn.** One `analyze` (60.4 s), the model answered from it (`final: true` honoured), request.complete at 1 min 59 s, under myBrain's 180 s; the session is in the facade's sessions.json and in myBrain's list. No "budget" refusal was needed.
- **F-049 (orphaned cards):** not checked in this turn; the maintainer closes the two "t" cards from myBrain once the sweep has moved them to blocked.
- First answer reached the person in this series since run 3, and the first ever with QuotPilot content.

## F-050: the pre-fetch still fires `quotpilot.analyze` with no arguments

- 11:12:43.299Z, 5 ms after the retrieval and before the first model token: `quotpilot.analyze` tool_failure "text, files, or requirements is required". The F-047 filter skips capabilities whose `input_schema.required` is non-empty; `analyze`'s schema (QuotPilot `agent/capabilities.py:1106`) declares no `required` because text | files | requirements are alternatives, so the filter lets it through and the handler refuses it at runtime.
- Cost: one failed audit row per turn, 0.01 ms; myBrain did not show it ("Did 1 call"), so the person is not affected. The audit trail still records a failed analyze on every quotpilot turn.
- **Tier:** live. **Family:** cluster C (chat pre-fetch). **Demo-blocker:** no. Candidate fix (Platform audit's call): the pre-fetch also skips a capability whose schema declares `anyOf`/`oneOf` requirements, or quotpilot declares its alternatives in a way the filter reads; or the pre-fetch fires only capabilities that opt in as argument-less reads.

## F-051: the QuotPilot assist never completes on gpt-oss:20b within its 60 s budget, so the analysis is always "Deterministic only"

- The model's `analyze` call (11:13:02.45 → 11:14:02.80Z) took 60.35 s, almost all of it the LLM assist: `_assist_budget_s` gave min(60, remaining ≈ 160 − reserve) = 60 s (`agent/capabilities.py:267`, ASSIST_BUDGET_S = 60), the completion was cancelled at expiry, and server.log at 11:14:02.791Z says `[ollama] gpt-oss:20b returned reasoning but no content (16696 chars)`. gpt-oss:20b spent the whole budget in its reasoning channel and produced no content, so `analyze_v2` fell back to the deterministic pass: 14 packages, 1 open decision, no interfaces, no findings.
- Run 5 showed the same shape: the second analyze (60.3 s) was deterministic; the first (58.1 s) was LLM-assisted and gave 19 packages, 4 interfaces and 4 open decisions. On this machine and model the assist is marginal at 60 s and loses whenever the daemon is slightly slower (the chat model had just been loaded and had just answered a tool round).
- Consequence for the person: the review says "Deterministic only"; the richer package set (HAL, watchdog, persistent storage, crypto, secure boot), the interfaces and three of the four open decisions of run 5's assisted draft are missing. Nothing in the answer tells the person why the mode is deterministic (the `assist_skipped` note is only set when the budget skips the call, not when the completion times out).
- **Tier:** live. **Family:** QuotPilot assist / model budget. **Demo-blocker:** no (an answer arrives), but the demo shows the weaker analysis. Candidates (Platform audit / QuotPilot): the assist asks for a non-reasoning completion or caps the reasoning (gpt-oss `think` low / `reasoning_effort`); a reasoning-only result counts as a timeout and the review says so; a larger assist budget when the client budget allows it (here 160 s were left; 60 s is a constant cap).

## F-052: the answer relays QuotPilot's operator instructions to the person

- The answer ends with "Waiting for your edits — say Go when ready", the tool syntax `quotpilot.decide({'OC-xxx': 'your choice'})`, `patches=[{'op': 'add_package', ...}]`, `set_platform`, "say Go to trigger quotpilot.generate", and asks for the platform choice as JSON (`{"OC-PLATFORM":"RTOS (FreeRTOS/Zephyr)"}`). Those are instructions for the model (how to continue the QuotPilot workflow), relayed to a person in a desktop chat.
- The model also passed stringified arguments: `files='[]'`, `requirements='[]'`, `project="{'name': 'fluvoro'}"`. The handler coped (collection='fluvoro' did the work), but a project given as a dict string is a model habit to watch (RE093's fill would hand it a plain id).
- **Tier:** live. **Family:** quotpilot skillpack prompt / answer shaping. **Demo-blocker:** no, but the person is asked to type tool calls. Candidate: the review's "waiting for your edits" block is for the model (system side), and the answer to the person states the open decision in plain words and says what the person can say next.

## T1 grading against kit/shown

- What to develop / work packages: 14 device-level packages traceable to CRS ids, consistent with run 5's deterministic draft. No effort, no proposed work packages ("when you say Go"). The 11 timing/resource constraints run 5's assisted draft listed are down to 4.
- Questions to the customer: one, and it is an internal decision (target software platform), not a customer question. None of RFQ §5's three open points (volume split, connectivity timing, hardware partner) was asked, nor the deliverables cross-check against FLV-STK-142 or the schedule. The RFQ's "what we expect" (effort per work package, assumptions and open points) is not addressed.
- Grade of the visible answer: the analysis is usable as a package inventory; as an RFQ analysis it does not reach the quoting questions. Better than every earlier run (an answer, with CRS ids), weaker than run 5's unseen assisted draft.
- Customer answer for T2: the platform question is not in the answer book, so the fallback sentence applies verbatim.
