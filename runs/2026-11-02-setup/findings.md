# Findings: 2026-11-02 setup

Evidence tiers: **live** = observed on the running installation; **source** = read in the deployed source tree (~/Sandbox) only.

## F-001: a help request on `flx department create` writes a department

- **Action:** `flx department create --help` (meant as a help request).
- **What happened:** printed `Created department: {'dept_id': '--help', 'display_name': '--help', 'created_at': '2026-11-02 11:33:19.263436+00:00'}`; a row `--help` was written to `fc.departments` in the real postgres store.
- **Expected:** usage text, nothing written.
- **Contrast:** `flx project create --help` printed usage and wrote nothing, so the two subcommands behave differently.
- **Cause (source):** `department_create` in the flx script only checks for an empty id; any non-empty first argument, including `--help`, goes to `INSERT … ON CONFLICT DO UPDATE` in `flexcore/db/rbac.py:create_department`. No CLI path deletes a department.
- **Cleanup:** the maintainer approved a direct `DELETE FROM fc.departments WHERE dept_id='--help'` (0 references in fc.principals, fc.projects, fc.connector_credentials; exactly 1 row deleted).
- **Tier:** live. **Family:** F8 (words routed to the wrong path). **Demo-blocker:** no.

## F-002: department creation leaves no audit entry

- **Action:** searched `~/Sandbox/logs/flexcortex_audit.log` for `--help` and recent `department` lines right after F-001.
- **What happened:** no entry found. Creating a department (and the direct-SQL cleanup) are invisible in the audit trail.
- **Expected:** an audit record for every write to the RBAC store.
- **Tier:** live (absence observed in the audit log). **Demo-blocker:** no.

## F-003: `IMPROVEMENT_LOOP_DRY_RUN` does not stop proposals in propose mode

- **What happened:** `flexcore/capabilities/improvement_loop.py` (~line 321) gates only `apply` on dry run; by decision I162 D (2026-10-17) propose mode still queues proposals during a dry run. An operator setting `DRY_RUN=true` to keep a run's data out of the suggestion inbox gets no effect.
- **Expected:** the flag name suggests "nothing leaves the loop"; the real lever is `AUTONOMOUS_LOOP_ENABLED`.
- **Tier:** source. **Demo-blocker:** no.

## F-004: `rag ingest <col> --path X` relies on argparse last-value-wins

- **What happened:** `cmd_ingest` in the rag script always passes `--path $KB_DIR/<col>` and then appends the user's flags; a user `--path` only wins because argparse keeps the last value. The watcher only tracks `$KB_DIR/<col>`, so an explicit `--path` collection is silently not kept in sync.
- **Expected:** either reject `--path` with a named collection or document the override.
- **Tier:** source. **Demo-blocker:** no.

## Isolation check (step 3)

The repository is at `~/Documents/GitHub/fluvoro`, outside `FILES_ALLOWED_ROOT=~/Sandbox`; the session workspace grants table is empty. `kit/hidden/` and `product/` are not reachable by file capabilities. The ingest uses a copy of `kit/shown/` only, at `~/Sandbox/knowledge_base/fluvoro`.
