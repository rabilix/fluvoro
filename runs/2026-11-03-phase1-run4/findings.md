# Phase 1, fourth run: findings

Numbering continues after F-043.

## F-044: myBrain sends its workspace folder as the turn's project

- `myBrain/src/renderer/state/chatStore.ts:253` sends `project: config.workspaceRoot`; in the maintainer's myBrain config that is `/Users/rabilix/Documents/GitHub/FlexCortex`, not the project `fluvoro`.
- The facade passes it on unchanged (`scripts/facade_server.py:5662`, relayed at :3684), the core puts it on the turn context (`scripts/routers/chat.py:696/899`), and `flexcore/runtime.py:2617` (`_turn_values`) makes it `project_id`.
- With RE093 the quotpilot tools take their missing `project_id` from the turn, so run 4 would run them against a FlexCortex folder path. The audit log does not record the turn's project, so this is invisible there.
- Found by code reading on 2026-11-03 before run 4; not yet measured live.
- **Tier:** live. **Family:** cluster C (turn context). **Demo-blocker:** yes.
- Fixed core-side in f4bd29d2 (path-shaped project refused, `project_refused` recorded on request.start); the desktop side is I183. Live in run 4 T1: `project: null, project_refused: "path_shaped"`.

## F-045: with the F-044 fix, quotpilot can no longer be selected from myBrain

- T1 (trace 77666c5f…): `skillpack: software_dev`, one retrieval, no quotpilot tool call, no draft, 30 s. The last quotpilot turn in the live audit is run 3 (2026-11-02 22:53Z).
- Cause: the quotpilot pack has `scope: project`; `flexcore/skillpacks/selector.py:360` admits a project-scoped pack only when `project is not None`. In run 3 the workspace path made it eligible by accident; F-044 now empties the project, so the pack is out of scope on every myBrain turn until myBrain sends a project id (I183) or the core supplies one.
- RE093 (tool defaults, carry, collection holdings) was therefore not exercised.
- **Tier:** live. **Family:** cluster C (turn context). **Demo-blocker:** yes.

## F-046: the operator's one project exists only in RBAC, so F-045 fills nothing

- Found while preparing run 5, after "F-045 deployed d9b657c0" (2026-11-03): FlexCortex's own lookup on the deployed code, read-only, for fluvoro-operator: `get_user_projects` → `['fluvoro']`; `get_project("fluvoro")` → no record (records dir `~/.flexcortex/projects` holds only `sdfasfas.yaml`); `membership_project` → `(None, "unrecorded")`.
- `fluvoro` exists in Postgres (the membership row passed its FK in setup) but has no project record; `flexcore/projects.py:283` requires a record, so the turn gets no project and quotpilot stays out of scope (F-045).
- Two project stores that can disagree; a project created the way setup did is invisible to the F-045 fallback.
- **Tier:** live. **Family:** cluster C (turn context) / setup. **Demo-blocker:** yes.

## Turn 1 answer without quotpilot (graded against kit/shown)

- Correct: RFQ §5's three open points are asked; ISO 26262 is read from the RFQ (rfq.md line 27); two variants V1/V2 and the BLE option are named.
- Missing: no CRS requirement ids, no device-level work packages (motor control, BLE, energy management … as RE090 produced in run 3), no effort; seven of ten questions are generic (timeline, acceptance, cost model …). Same quality as cluster B without the skill.
