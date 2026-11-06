# Phase 1, eighth run: findings

Numbering continues after F-059.

## Run 7 fixes, checked on T1 (trace 0fc9d29b-2e09-4d2e-8919-0a888a942c90)

- **F-052 closed.** The review reached the person rendered (tables as tables, no code fence, no "Review (verbatim)" heading), with no "say Go", no `quotpilot.decide`/`patches` syntax; the closing is plain words ("reply with your choice, or ask for a package to be added, removed or changed"). The model also passed plain arguments this time (`collection='fluvoro', project='fluvoro'`).
- **F-051 closed as stated, cause still open.** The answer now says why the analysis is deterministic ("the LLM assist did not return usable content within its budget (timeout or reasoning without content)") and the draft file carries `assist: {status: no_answer, budget_s: 60, took_s: 60}`. The assist itself still fails on gpt-oss:20b at 60 s, now with load 4.6; the richer assisted analysis (interfaces, more decisions) remains out of reach on this machine and model. Kept open as an F-051 tail: budget or model choice for the assist, not honesty.
- **F-050, F-048 hold:** no empty pre-fetch, one analyze, answer in 1 min 41 s, chat saved.
- **F-055 open, owner corrected.** The tool line above the answer is still raw (T1, T2; screenshot of T2 at 20:49 local). It is not a desktop rendering: the facade writes it into the answer TEXT (`scripts/facade/turns.py:538`, `_agent_event_text` for `type == "tool"`: `` `› name(args)` → `` plus the first 160 characters of the raw result), and the line is stored in `sessions.json` as part of the assistant message. myBrain therefore receives markdown and cannot fold it. The summary has no line break after its cut, so the raw JSON runs into the answer's first heading ("…the LLM assi **Review of the Fluvoro RFQ**"). The earlier hand-off ("desktop-only change, the facade already sends typed tool frames") does not match the code. Fix lives in the facade first: send the call as a typed frame only (name, status, args, result) and keep it out of the stored text, then myBrain renders it collapsed; at minimum end the line with a newline and never put raw result JSON in the text.

## T2 (trace 57a9bdb2-90ec-45de-9e36-1cfbffe2e9a2)

- **F-053 holds:** carried sticky, `quotpilot.decide` on the T1 run, draft platform RTOS, 16 packages, 0 open decisions; one send, one decide.
- **The answer now speaks for the person and states the assumption as the customer asked** ("the customer asked us to state a reasonable baseline").

## F-060: with "verbatim" removed, the model paraphrases the review and drops the traceability

- T2's answer rewrote the review in the model's words. The package table's evidence column became "Multiple FLV-STK identifiers" (Energy management, 37 ids in the draft) or two ids and "…" for every other package. T1, from the same pack prompt, still rendered the full id lists. The requirement-to-package trace is the one thing in this answer a quoting engineer checks first, and it is now lost on the follow-up turn.
- The model also stringified its arguments again (`answers="{'OC-PLATFORM': …}"`, `patches='[]'`); the handler copes.
- **Tier:** live. **Family:** QuotPilot answer shaping (the F-052 fix overshot). **Demo-blocker:** no, but a credibility hit. Candidate: the pack prompt keeps "explain, don't paste" for the operator parts and says the package table and its requirement ids are shown in full; or the review hands the table as a block the answer must include unchanged.

## T3 (agent path, 19:51:42Z)

- **F-057 closed live.** The maintainer's Deny on the card resolved the hold: `2c79ce2fbf28` reads `denied`, resolved 19:53:03Z; the maintainer: "Deny worked now". Small gap: no audit row records the denial (the store has it, the audit log does not), so a denied write is not visible in the trail.
- **F-056 closed in substance.** `agent.workflow_state` handed the session's open run to the plan; no new analyze, no "Project: Unknown", no invented decision id; the plan had 2 steps instead of 3.
- **F-054 holds.** No effort numbers; generate held, then denied.
- **F-058 partly.** The card no longer shows a JSON blob, but see F-062.

## F-061: the plan re-applies the decision with a different value and narrows the person's assumption

- Step 1 ("Record the assumed RTOS platform") called `quotpilot.decide` again on the run whose OC-PLATFORM was already answered in T2 as "RTOS (FreeRTOS/Zephyr)". It succeeded and the draft's platform is now "FreeRTOS", a value that is not one of the decision's four options. The answer says "the device will target FreeRTOS as the RTOS". Nobody chose FreeRTOS over Zephyr; the planner did, from its own reading of "Proceed with RTOS".
- `decide` accepts an answer outside the decision's options and overwrites an answered decision without saying so.
- **Tier:** live. **Family:** agent path / workflow state (F-056 tail) and QuotPilot decide validation. **Demo-blocker:** no, but the customer's confirmed assumption changes silently. Candidates: the plan does not repeat a step the workflow state shows as done (decide answered); `decide` refuses a value outside the options and states when it overwrites an answered decision.

## F-062: the held generate carries no run_id; approving it would have failed

- Pending action 2c79ce2fbf28 was recorded with kwargs `{}`; the card said "No arguments". `quotpilot.generate` needs the run (`_owned_draft(ctx, run_id, …)`, `agent/capabilities.py:864`), so an approval would have run a call certain to fail. `agent.workflow_state` lists run ids for `analyze` and `decide` only, not for `generate`, so the plan's last step got nothing.
- F-058's other half (validate the call against the capability's schema before asking a person) is not in place either: a card was raised for a call missing its key argument.
- **Tier:** live. **Family:** agent path / plan values (F-058 tail). **Demo-blocker:** yes, for the next step of the demo (approving generate). Candidates: workflow state covers every pack capability that takes the run id (generate, ask, finalize_quote, close); the hold is validated against `input_schema` before the card is shown, and an invalid one is refused to the planner, not shown to the person.

## T1 grading against kit/shown

- Work packages: the same 14 packages with CRS ids; no effort (by design until the person asks for work packages).
- Questions to the customer: only the platform decision. RFQ §5's three open points are still not asked; the pack does not ask for them and the model did not add them this time. Unchanged since run 6; a pack-content gap, not a seam (to raise after the run).
- Presentation: the best of the series. The review reads as a document, the decision as a question.
