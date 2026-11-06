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

## F-053: the customer's answer is routed to another pack; the QuotPilot workflow is dropped

- T2 (trace 283769a8-ba9f-43d1-8a45-e0176696222d): the customer's reply to FlexCortex's own open decision was selected into `planview` (Planview PPM Advisor, intent action), not `quotpilot`. No `quotpilot.decide`, the draft's OC-PLATFORM stays unanswered, and the RTOS assumption in the answer is the chat model's own text with no QuotPilot content behind it. The person reads a confident platform decision that the draft does not hold.
- Cause (read-only, `flexcore/skillpacks/selector.py:245` and the packs): the selector scores packs by keyword hits, then priority. The reply contains "platform", a keyword of `planview` (score 1); none of quotpilot's keywords (rfq, work package, what to develop, …) occurs in a customer answer, so quotpilot scores 0 and its priority 10 never counts. Domain was null, so the pool was every pack accepting the intent. In T1 quotpilot won on "rfq" + "work package" + "what to develop" (checked with the loader on the 38 installed packs: T2 scores planview 1, software_dev 1, quotpilot 0).
- The RE093 carry (`runtime._carry_recent_pack`) did not apply: it runs only when the selector found no pack, only for replies of at most 6 words, and only when the assistant's last line ends with "?" (T1's answer ends with `…)`.). A customer answer of one or two sentences is the normal case and meets none of the three.
- **Tier:** live. **Family:** cluster C (pack selection across turns). **Demo-blocker:** yes. Same family as F-040 (run 3) and the F-045 chain: the pack is found for the opening question and lost on the follow-up. Candidates (Platform audit's call): a session with an open pack workflow (quotpilot run in DRAFT with an open decision) keeps that pack for the follow-up unless the person changes task; the carry keys on the pack having asked (an open decision in the tool result), not on reply length or a trailing "?"; generic single words ("platform", "project", "resource") stop deciding a selection against a priority-10 pack that opened the conversation.

- T3 confirms it from the other side: "Proceed with RTOS and generate the work packages." selected `feature_breakdown` (keywords "work package" + "work packages" = 4, priority 9) over quotpilot ("work package" = 2, priority 10). The model, remembering the tool name from T1's answer, called `quotpilot.generate` and was refused ("not in the pack's callable set"; feature_breakdown may call only work.preview_breakdown on the chat path). Three turns, three packs (quotpilot, planview, feature_breakdown) for one conversation about one RFQ.

## F-054: after the refused tool call the model writes the quotation itself, with invented effort

- T3's answer is a 14-row work-package table with person-days per package (12, 15, 10, 14, …), a total of 149 person-days "≈ 7 months on a 5-person team", a "what's included in the quotation" list (ISO 26262 ASIL-B and ISO 21434 certification effort, 90 days support) and next steps towards sign-off. None of it comes from QuotPilot: the draft holds no effort, no work packages were generated, and the refused `quotpilot.generate` is the only tool call. The FLV-STK ids per row are copied from T1's package evidence; the efforts, the team size and the inclusions are the chat model's own.
- The person sees "1 call · 1 not ok" and a complete, confident quote basis. Nothing in the answer says that the generate step was refused and that the numbers are not the tool's.
- **Tier:** live. **Family:** answer honesty after a refused action (same shape as RE104 for retrieval: a failed step must be said). **Demo-blocker:** yes. Candidates: a refused write on the chat path is said in the answer ("not run: …"), and a pack that owns the quote basis (quotpilot) is the only one allowed to state effort; the chat model does not fill a refused tool's output from its own knowledge.

## F-055: myBrain shows every tool call as a raw line above the answer

- Each tool the model called is printed in the chat as a "›" line with the call, the model's argument strings and the first ~150 characters of the raw JSON result (T1: `quotpilot.analyze(collection='fluvoro', files='[]', project="{'name': 'fluvoro'}", requirements='[]') → {"run_id": …, "review": "\n## Executive Summary…`), with a "Did 1 call · 1 not ok" footer. The person reads raw JSON and stringified arguments before the answer and asked why it is there.
- Request from the maintainer (2026-11-06): show the calls collapsed, one short line per call with its name and status (ok, refused, not run), opened on click to the arguments and the raw result, so the answer stays clean and the detail stays available for debugging. The footer could be the toggle.
- **Tier:** live, desktop presentation. **Family:** myBrain chat rendering. **Demo-blocker:** no. Priority after F-053/F-054; related to F-052 (the answer text itself carries operator instructions).

## Noted, not a finding

- `server.log` has 112 lines today (00:15Z … 11:23:49Z, the last one during the run) `[neo4j] no driver (ClientError): Neo.ClientError.Security.AuthenticationRateLimit … graph retrieval will return nothing and answers will silently degrade`. `ragstack.conf` carries NEO4J_PASS as an unresolved secrets reference. Vector retrieval worked (T1 646 ms, T2 330 ms); the graph hop contributed nothing to any run. Deviation for Platform audit after the lift; not a run 6 cause.

## T1 grading against kit/shown

- What to develop / work packages: 14 device-level packages traceable to CRS ids, consistent with run 5's deterministic draft. No effort, no proposed work packages ("when you say Go"). The 11 timing/resource constraints run 5's assisted draft listed are down to 4.
- Questions to the customer: one, and it is an internal decision (target software platform), not a customer question. None of RFQ §5's three open points (volume split, connectivity timing, hardware partner) was asked, nor the deliverables cross-check against FLV-STK-142 or the schedule. The RFQ's "what we expect" (effort per work package, assumptions and open points) is not addressed.
- Grade of the visible answer: the analysis is usable as a package inventory; as an RFQ analysis it does not reach the quoting questions. Better than every earlier run (an answer, with CRS ids), weaker than run 5's unseen assisted draft.
- Customer answer for T2: the platform question is not in the answer book, so the fallback sentence applies verbatim.
