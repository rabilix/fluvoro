# Concept: code owns the state and the evidence, the model only does the wording

Adopted by the maintainer on 2026-11-10 (D-76). Combined from a read-only Codex architecture review
(Codex session 01a1c488-7c0a-7943-b404-a824909b0b3f) and this session's run evidence (Fluvoro runs 6–9, case 2
runs 1–2). Owners of the implementation: the FlexCortex and Platform audit sessions (plan in FlexForge). This
session supplies fixture raw material and runs the acceptance.

## Why the fix-and-rerun loop did not converge

Each fix closed one symptom. The structural causes (checked on core 9d61105b4, QuotPilot 9f82f6d):

1. **Two routes to one action.** The chat path refuses writes and tells the person to ask again as an action;
   only the planner can hold a card (`flexcore/runtime.py` ~2638). Wording decides the route.
2. **The model authors action arguments.** The executor fills an identifier only when the planner omitted it;
   "a value the planner wrote is never overwritten" (`flexcore/agent.py` ~1542). Hence `{run_id}`, `run-1234`,
   the wrong action (`finalize_quote`), a second analysis.
3. **Customer answers reach the draft only if the model calls `decide`**; assumption and decision share a field
   (QuotPilot `agent/capabilities.py` ~922–944).
4. **The honesty check covers one claim type** (effort, time, cost, share); the action-claim check appends a note
   and is skipped when any tool call succeeded (`flexcore/runtime.py` ~1519, ~2668).
5. **QuotPilot treats partial recognition as knowledge**: a requirement id is attached to a package on a keyword
   hit; an unknown domain exposes every package (`packages/detector.py` ~35).

## The ten parts

| # | Part | Origin |
|---|---|---|
| 1 | Workflow record per chat and project: one active run, draft version, open items, current hold | Codex |
| 2 | One action door: any wording, or a chat tool attempt, becomes the same `request_generate(workflow)`; code binds run id and project; the model cannot choose another action or supply ids; chat returns the real hold instead of a refusal; idempotent; approval stays mandatory | Codex |
| 3 | The system offers the next step from state: when the draft has no open items, the generate card is offered unasked; "go ahead" only approves | this session |
| 4 | Typed answer capture before the model writes: customer_decision, customer_unknown, working_assumption; matched to the draft's open items; applied atomically | Codex |
| 5 | Claim gate, narrow and deterministic first: a cited id exists; a value stated next to an id occurs in that requirement; a standard occurs in some source; "submitted / held / generated" matches the hold store or an execution of this turn; else named or removed. Completeness claims later | both |
| 6 | Packages from the customer's own structure: the specification's chapters and the RFQ's scope section are the package skeleton, the catalogue labels; a domain the catalogue does not cover is an explicit finding, not a generic list; no per-product catalogue | this session |
| 7 | RFQ tables (open points) and a platform named anywhere in the RFQ are read as structured records, with a coverage report | Codex |
| 8 | Bounded model calls: the platform sets the context size per call (16–32k) instead of inheriting the Ollama app's global; the analysis assist works per chapter in small prompts (F-051, the "Lam" corruption) | this session |
| 9 | Fixtures first: every finding of case 2 runs 1 and 2 becomes a replay fixture against a stub model, with wording variants; from then on a live finding becomes a fixture before it is fixed | both |
| 10 | Exit criteria fixed in advance, for both cases: 0 invalid ids, 0 unsourced standards, 0 invented effort, answers recorded 100 %, generate succeeds 5 of 5; packages and questions tracked as content measures with their own target | this session |

Sequence: 9 and 10; then 1–3; then 4; then 5; then 6–8; then one live acceptance run (case 2, then Fluvoro).

## Expected effect (estimate, 2026-11-10)

| Area | Expectation |
|---|---|
| Action path (cards, run ids, claimed actions) | solved; code binds the arguments |
| Honesty for checkable claims | mostly solved; wrong paraphrase and subtle mis-mapping remain |
| Customer answers on the draft | solved only once part 7 makes the open items right |
| Quote content (packages, questions) | improves through parts 6 and 7; unmeasured until the acceptance run |
| Answer quality with gpt-oss:20b | stays limited; the system becomes safe and honest, not clever |

## Left open (maintainer's call)

- Where effort per work package comes from (F-064): a person fills it in, or a rule estimates it.
- One comparison repeat with a stronger model (sends case text to an external service).

## Fixture raw material

`docs/replay_fixture_cases.yaml`: the model outputs and tool-call shapes observed in the runs, without case
content.
