# Phase 1, fourth run: findings

Numbering continues after F-043.

## F-044: myBrain sends its workspace folder as the turn's project

- `myBrain/src/renderer/state/chatStore.ts:253` sends `project: config.workspaceRoot`; in the maintainer's myBrain config that is `/Users/rabilix/Documents/GitHub/FlexCortex`, not the project `fluvoro`.
- The facade passes it on unchanged (`scripts/facade_server.py:5662`, relayed at :3684), the core puts it on the turn context (`scripts/routers/chat.py:696/899`), and `flexcore/runtime.py:2617` (`_turn_values`) makes it `project_id`.
- With RE093 the quotpilot tools take their missing `project_id` from the turn, so run 4 would run them against a FlexCortex folder path. The audit log does not record the turn's project, so this is invisible there.
- Found by code reading on 2026-11-03 before run 4; not yet measured live.
- **Tier:** live. **Family:** cluster C (turn context). **Demo-blocker:** yes.
