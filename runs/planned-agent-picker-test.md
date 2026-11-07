# Planned test: the agent picker (myBrain "Auto" menu)

Asked by the maintainer on 2026-11-07. Not run yet.

## What the picker does (read from the code, 2026-11-07)

The composer's first menu names the agent that answers a turn. "Auto" sends no `agentId`.
myBrain sends `agentId` per turn; the facade passes it to `/api/v2/chat` as `agent`
(`scripts/facade_server.py`, around line 1243); the core (`flexcore/runtime.py`, `_chat_bind_agent`)
replaces the auto-selected pack's persona with the agent's standing identity and uses the agent's
declared model (`default` row) when reachable. The agent is identity only: it does not change the
department, retrieval permissions or project. A session `/model` override beats the agent's model;
a disabled agent is refused. The menu lists the agents in `~/.flexcortex/workers/` (22 on
2026-11-07); an agent whose model is unreachable is greyed out with the reason.

## When and setup

- After case 2 run 1 is graded, under its freeze. About 30 minutes of chats.
- Rabilix profile, project fluvoro (case 2 stays blind), throw-away chats, Decisions default.
- Each check twice (gpt-oss varies).
- Preparation (read-only): read the worker files and pick (a) a plain-role agent without its own
  model, e.g. Requirements Assessor; (b) an agent whose declared model differs from gpt-oss, if any;
  (c) an automotive agent, AUTOSAR Eng.

## Checks

| # | Check | Turn(s) | Pass when (from the trace, not the text alone) |
|---|---|---|---|
| T1 | Identity | "In one short sentence: what is your standing role?" Auto, then (a) | Auto answers generically or as the pack; (a) answers as its role |
| T2 | Model | Same question with (b) | Trace shows (b)'s declared model; if unreachable, (b) is greyed out with a reason |
| T3 | Permissions unchanged | "List the requirement ids of the motor control chapter." Auto vs (a) | Same project, collection and retrieved chunk ids; only the voice differs |
| T4 | Not sticky | Turn 1 with (a), turn 2 back on Auto | Turn 2 has the pack persona and the default model |
| T5 | Pack and agent together | Fluvoro O-1 opening with (a) | QuotPilot still selected and its tools run; persona is (a)'s |
| T6 | Domain leak | T3 question with (c) | Count ECU, ASIL, AUTOSAR and similar terms against Auto; any added term is a finding |
| T7 | Disabled agent (optional) | Needs the maintainer to disable an agent (config change) | Turn refused: "seat … is disabled by the operator" |

## Evidence and outcome

Per turn: trace id; persona source, model, selected pack and retrieved chunk ids from the trace;
the audit row. Findings continue the F-numbering.
Outcomes: works (T1–T5 pass); persona only (T1 passes, T2 fails); unsafe (T3 fails: choosing an
agent changed what the person can see).

## Fixed condition for the case runs

Until this test has run, every case run keeps the picker on Auto (no new variable; several agents
carry automotive roles that would contaminate the forbidden-terms check).
