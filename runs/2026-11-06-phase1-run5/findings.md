# Phase 1, fifth run: findings

Numbering continues after F-046.

## What worked for the first time since run 3

- T1 (trace 6ef802a3-f540-4424-a8e6-b4d7c9c467af): `project: fluvoro, project_source: membership, project_refused: path_shaped`, `skillpack: quotpilot`. F-044, F-045 and F-046 are closed on the live path: the workspace path is refused, the membership fallback fills the project, the record exists.
- `quotpilot.analyze` ran against the real inputs: `rfq.md` (17 requirements) and `reqif:fluvoro/fluvoro_crs_v1.reqif` (101 requirements), 118 in total. The ReqIF count after RE034/RE103 is unchanged.
- The deterministic analysis classified the domain as `embedded_device` (High, 67 terms) with `automotive` secondary (ISO 26262/ASIL/HARA), the RFQ type as `engineering_service` (High), and derived 19 packages (LLM-assisted run) / 14 packages (deterministic run) with requirement ids: Motor control (20), Energy management (37), Jam / overload detection (13), BLE connectivity (4), Functional Safety package (6), Service interface (7), … plus 11 timing/resource constraints (start latency 30 s, restore flow 120 s, standby 2 mW, battery 70 % after 5 years, noise 65 dB(A), −20…50 °C) and ASPICE SWE.1/SWE.6.
- No episodic recall, no cache hit (episodic off per D-39; RE100 dropped the old cache rows).

## F-047: the model's first tool round calls all five quotpilot tools without arguments

- At 07:36:53Z, 5 ms after the retrieval, the model issued `quotpilot.fetch_requirements`, `quotpilot.analyze`, `quotpilot.decide`, `quotpilot.analyze_rfq` and `quotpilot.ask` in one round, each with no arguments. All five failed in 0.01 ms: `missing required argument(s): project_id` / `text, files, or requirements is required` / `missing required argument(s): run_id` / `missing required argument(s): text` / `missing required argument(s): run_id, question`.
- RE093 ("tool defaults from the turn") did not fill `project_id` from the turn's project `fluvoro`, although the turn carried it (request.start) and the later `analyze` calls show `project='fluvoro'`.
- Cost: one wasted round; the model recovered on the second round (10 s later) with a correct `analyze(collection='fluvoro', project='fluvoro')`.
- **Tier:** live. **Family:** cluster C (turn context / tool defaults). **Demo-blocker:** no on its own, yes together with F-048.
- Platform audit (2026-11-06, read-only): by the code `_fill_turn_defaults` should have filled `project_id` from `turn_project(ctx.project)`; the refusal means `ctx.project` was not "fluvoro" when the tool round ran, a seam not pinnable from logs (needs a spare-port core; to be reproduced after the lift). Caveats: a working fill would hand Polarion a FlexCortex project id, which is not what `fetch_requirements` means; `analyze`'s missing text is not fillable at all, so four of the five first-round failures are the model's, not the fill's.

## F-048: `analyze` runs twice (LLM-assisted, then deterministic) and the turn is cancelled before the answer

- `quotpilot.analyze` succeeded twice: run 6a135f31… (07:37:04–07:38:03Z, 58 s, `llm_assist: true`, 19 packages, 4 open decisions) and run f20eedc4… (07:38:10–07:39:11Z, 60 s, `llm_assist: false`, 14 packages, 1 open decision). The second run is the same analysis in its fallback mode; nothing in the turn needed it.
- The desktop showed "The FlexCortex agent did not answer in time. Please try again." at 08:38 local; the core logged at 07:40:11Z `[turn_ledger] chat turn 1257fb0f: the interrupted call is still running after cancellation`, then `the interrupted call has returned; row ended`. No `request.complete`, no answer text, no `retrieval` field (RE104) to grade. Turn duration until cancellation: 3 min 18 s.
- The reviews reached the chat only as the raw tool-result JSON, cut after ~150 characters each ("## Executive Summary … Status: DRAFT …"). The person sees two run ids and no analysis.
- Both drafts are in `~/.flexcortex/quotpilot/runs/<run_id>/draft.json` (status DRAFT, owner fluvoro-operator, mock backend); they were not read by the model into an answer.
- **The chat was not saved.** The core's Postgres session `session-vfAG0hEHffqzaPKPfRg8S2HW` exists (created 07:36:53Z, turn_count 1, holdings fluvoro) but holds only the user row (07:36:54Z); the assistant row is written in stage 8 (`flexcore/runtime.py:1482`), which never ran. The facade's own list, `~/.flexcortex/facade/sessions.json` (41 entries, the one myBrain shows), is written by `record_turn` after a completed turn (`scripts/facade/turns.py:1031/1114`); its last write is 2026-11-03 17:34 local (run 4 T1), and the run 5 session is absent. A cancelled turn therefore leaves no conversation in the desktop; two minutes of QuotPilot work and the drafts are orphaned.
- **Tier:** live. **Family:** chat turn budget / tool loop. **Demo-blocker:** yes. Same shape as F-041/F-042 in run 3 (conversation breaks), now one level later: the pack works, the turn does not finish.
- Cause (Platform audit, 2026-11-06, read-only): the cancellation is myBrain's own `CHAT_TIMEOUT_MS = 180_000` (`HttpFlexCortexClient.ts:177`, error text at :327): abort at 07:39:53Z, before the first answer token; the facade's 135 s per-read budget (kept alive by keepalive frames) and the core's 600 s idle abort never fired; the core learned of it only when the facade's write failed, and the model's generation ran until Ollama returned (07:40:11Z). The second `analyze` was the model's third tool round after the first result came back cut at 6 000 chars (`_CHAT_TOOL_RESULT_CHARS`); nothing tells the model a completed analysis is final, and the identical-call guard (B348) only acts on attended surfaces. It came out deterministic because QuotPilot's assist (`_llm_complete_via_server`) has a 60 s budget and the same Ollama daemon was busy with the chat model; the 60.3 s is that budget. Candidate fixes (none applied): pack finality after `analyze`; bound the chat's tool rounds by the client's remaining budget (or a per-chunk desktop budget); the assist skips when the daemon's window is closed and budgets under the round.

## F-049: an orphaned `awaiting_approval` card cannot be removed from the desktop

- myBrain's "My tasks" shows two cards titled "t" under "Awaiting approval" (waiting 3 d / 4 d): `p1/WI-7` (wi_01a19cbd4582464973582b7a48) and `p1/WI-21` (wi_01a19cbd5c4bbf143da34af643), project `p1`, tenant default, profile polarion, created 2026-11-02 14:50Z with 14 other "t" backlog items (probe leftovers, not Fluvoro).
- Both have `pending_action_id` and `pending_session_id` null. Approve/Deny therefore answers 409 "this card is not waiting for an approval" (`scripts/facade_work_items.py:283`); a person's move out of `awaiting_approval` is refused ("Approve or Deny it first", `flexcore/work_items.py` `_transition`), and the profile adds `_refuse_read_only_move`. Only a `system=True` transition or a core sweeper can close them.
- Seen while grading run 5 T1 on 2026-11-06; the maintainer asked for their removal (D-42: Platform audit closes them the supported way and fixes the gap; we do not write to the live store).
- **Tier:** live. **Family:** work items / approvals. **Demo-blocker:** no (cosmetic in the panel), but a person has no way out.

## Noted, not a finding

- 07:35:46Z `facade.handshake_refused` reason `invalid_key` (tenant operator), 29 s before the RBAC handshake of fluvoro-operator succeeded. One refused attempt, probably the desktop's first key before the profile switched; it did not affect T1.
- The myBrain footer showed "backend stale" before T1: the facade (pid 15693, up since 2026-11-05 22:28Z) notes its deploy marker at start; seven core deploys followed without a facade restart. Platform audit states no facade file changed; contract 78 on both sides. Deviation recorded, not a cause.

## T1 grading against kit/shown (from the drafts, since no answer was produced)

- Work packages: device-level and traceable to CRS ids for the first time in this series (motor control, energy management, jam detection, BLE, functional safety, OTA, secure boot, …). This is the content run 4 lacked.
- Questions to the customer: the LLM-assisted draft lists 4 open decisions (target platform, BLE+OTA in the baseline, secure boot, watchdog). Only "BLE in the baseline" matches one of RFQ §5's three open points (volume split, connectivity timing, hardware partner); the other two §5 points are not asked. The deterministic draft has 1 open decision.
- Effort: none in either draft.
- Nothing of this reached the person: grade of the visible answer is "no answer".
