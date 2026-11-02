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

## F-005: retrieval ACL is inactive; the Fluvoro principal can read every collection

- **What happened:** `FLEXRAG_ACL_ENABLED` and `FLEXRAG_TENANT_IN_FILTER` both default to `false` (scripts/conf.py:279, :284) and neither is set in flexcortex.conf or ragstack.conf. The `--dept engineering --project fluvoro` stamps on the 106 fluvoro chunks therefore restrict nothing; `flexrag/db/acl_filter.py` is dormant.
- **Consequence:** nothing in the ACL filter stops the Fluvoro principal from retrieving `oem-*-reqs` and `compliance` (not yet observed live); isolation of `kit/hidden/` and `product/` rests only on them never having been ingested.
- **Expected:** the ingest help text calls the stamps an "ACL scope"; either the scope applies, or ingest/doctor says it is dormant.
- **Tier:** source + config. Confirm live in Phase 1 with one read-only chat question as the Fluvoro profile that names an `oem-1-reqs` requirement id. **Family:** F4. **Demo-blocker:** no.

## F-006: `create_principal` silently overwrites an existing user

- **What happened:** `fc.principals` is keyed by `user_id` across tenants, and `flexcore/db/rbac.py:create_principal` does `INSERT … ON CONFLICT (user_id) DO UPDATE` (tenant_id, dept_id, email, display_name). Re-creating an existing user silently replaces those fields, e.g. `flx principal create rabih siimplex engineering` would change the maintainer's dept from none to `engineering` without a warning.
- **Correction (review):** a cross-tenant move such as `flx principal create rabih fluvoro` is refused before the upsert by the `ADMIN_TENANT_IDS=siimplex` guard in `flx` (ragstack.conf:34). A tenant move is only possible between tenants listed there; today only `siimplex` is, so the live risk is the silent field overwrite within `siimplex`.
- **Expected:** refuse (or ask) when the user already exists.
- **Avoided by:** a new user `fluvoro-operator`. **Tier:** source. **Family:** F4/F1. **Demo-blocker:** no.

## F-007: provider wizard had no API key field ("Add a key below" with nothing below)

- **What the person saw:** myBrain dev → Add Provider Profile → Local FlexCortex → Test Connection: "The FlexCortex backend requires an API key, but this profile doesn't have one. Add a key below to connect." No key field anywhere in the wizard; only Back / Retry; Save only after a passing test.
- **Cause (source, myBrain cb9a818):** message from `src/process/platform/HttpFlexCortexClient.ts:254`; no key input in `ProviderWizard/*.tsx`; the field exists only in the Profiles detail view and BootFailureOverlay (existing profiles only).
- **Status:** fixed by the Platform audit session in myBrain `e070a8b` (develop `4c73cc9`): optional key field in the wizard, stored via the secret store; 401 text changed.
- **Tier:** live (maintainer screenshot) + source. **Demo-blocker:** yes (fixed).

## F-008: nothing records which principal connected to the facade

- **What happened:** after the Fluvoro profile connected, the facade access log (`~/Sandbox/logs/facade.log`) shows only `127.0.0.1 "GET … HTTP/1.1" 200` lines with no principal or key prefix, and the audit log has no entry after 09:00Z (handshakes and polling are not audited). The connecting principal could only be inferred from `fc.api_keys.last_used` (fluvoro-operator 12:56:02Z; a rabih key 12:55:16Z, consistent with the app starting on the everyday profile).
- **Expected:** the handshake (at least) is attributable to a principal in a log or the audit trail.
- **Tier:** live (absence) + store timestamps. **Demo-blocker:** no.

## F-009: the facade drops the caller's identity; every myBrain turn runs as tenant `default`

- **What happened:** the listing turn (trace `d8b23ded-c9db-4fbe-933a-a0a1dafc24d7`) reached the core through the facade, but the core's audit records it as `tenant_id: default` with no principal, and `outcomes.db` has `tenant_id default`, empty `actor_id`.
- **Why the caller was fluvoro-operator:** no static `FACADE_API_KEY` is set in either conf, so the facade accepts only RBAC keys; the only key used after 12:56Z was `fluvoro-operator`'s (`last_used` 13:11:14Z; every `rabih` key last used ≤ 12:55:16Z). `last_used` alone does not pin a single request.
- **Cause (source, confirmed by the Platform audit session):** `scripts/facade_server.py` `_rag_request` calls the core's `/api/v2/chat` with the facade's own server key (`_rag_server_api_key()`) and sends neither user nor tenant; the authenticated principal is used only for facade-side session ownership (`owner=`). Proposed fix (Platform audit): forward the caller's own bearer when the facade resolved it as an RBAC principal, so the core authenticates it and binds tenant/user/dept from the key.
- **Consequence:** per-user/tenant audit, ACL, memory and outcome attribution cannot work for any myBrain turn, not only this run. (F-008, the missing principal in the facade's own access log, is a separate gap.)
- **Tier:** live (audit + outcomes) + source. **Family:** F4. **Demo-blocker:** no (but blocks per-user grading).

## F-010: key authentication hit an exhausted PG connection pool

- **What happened:** `facade.log` at 2026-11-02 14:10:51 local (13:10:51Z), 7 s before the listing turn: `PG authenticate_api_key failed: connection pool exhausted`. Earlier occurrences in the same log (lines ~12894–12934, including "server closed the connection unexpectedly" and "Connection refused").
- **Behaviour:** fail-closed as designed (`auth_unreachable` → 503; the only other accept path, a static `FACADE_API_KEY`, is not configured), and the next request authenticated. The pool exhaustion itself is the defect.
- **Tier:** live (log). **Demo-blocker:** no (intermittent).

## F-011: "list all requirements" returns 3 of 101 and presents it as the full list

- **What the person saw (myBrain, Fluvoro profile, 2:10 PM local):** prompt "List all requirements in the fluvoro collection: every requirement ID with its title, nothing else." Answer: `FLV-STK-135: Identification FLV-STK-095: WEEE FLV-STK-092: Control software safety class`, footer "gpt-oss:20b · 5 sources". Knowledge scope selector: "All knowledge sources".
- **What the records say:** trace `d8b23ded-c9db-4fbe-933a-a0a1dafc24d7`: one `knowledge.retrieve_context` (0.46 s), then `chat_turn` ollama/gpt-oss:20b, 124 tokens, 15.2 s, status success.
- **Check:** the three ids and titles match the CRS exactly (no fabrication); 98 are missing; the answer gives no sign that it is partial. The collection holds all 101 (verified in qdrant).
- **Cause (Platform audit session, source):** the I161 listing path exists only on `/v1/chat/completions` with a `rag-<collection>` model (`scripts/routers/chat.py:276`); myBrain uses `/api/v2/chat` and never reaches it, so "list all" falls through to top-k retrieval. The listing cap `MAX_ROWS=100` is also below the 101 requirements.
- **Expected:** an enumeration request is served by a listing path (all 101), or the answer states that it shows a top-k subset.
- **Tier:** live. **Family:** I161 path (top-k presented as complete). **Demo-blocker:** yes.
- **Correction:** every listing turn records exactly 124 tokens, including control 2 whose answer is a sentence longer, so the token count is not the answer length and is no evidence of truncation; the 3-of-101 count comes from the maintainer's screenshots (see F-016).
- **Turns (all show 3 ids):**

  | Local | Trace | Commit | Chat | Scope | History sent | Caveat |
  |---|---|---|---|---|---|---|
  | 14:10 | `d8b23ded-c9db-4fbe-933a-a0a1dafc24d7` | eefbbeb8 | 1 | All sources | 0 | no |
  | 15:08 | `5280e9a0-9c06-425c-a98f-750280ba7bda` | eefbbeb8 | 1 | All sources | 2 | no |
  | 15:31 control 1 | `edf0db04-b7ea-46ab-8481-2afd315d6342` | b13bbb8e | 1 | fluvoro | 4 | no |
  | 15:36 control 2 | `a587affe-f0a8-4656-9d67-6f2d074df46c` | b13bbb8e | 2 (new) | fluvoro | 0 | yes ("not included in the supplied context") |

  All four are fresh retrieval + generation (own trace, own `knowledge.retrieve_context`), not replays. Control 2 rules out scope and history: the door alone is the cause.
- **Fix:** RE080 (`8644e23b`, deployed in `3d67ba1a` at 14:41:54Z). **Live re-check: PASS** — trace `a2e43c82-0295-49d1-a083-87f54cfd7d71` (16:07 local, new chat, picker fluvoro): audit `chat.listing` rows 101, collection fluvoro, no model; the answer lists the exact 101-id set of the ReqIF. Remaining flaws in F-013.

## F-011a: the partial list was presented as complete while earlier answers sat in the history

- In chat 1 the same 3 ids came three times with no caveat; in a fresh chat (control 2) the model stated that the rest was not in its context. The replayed history (2 and 4 messages, verbatim) likely made the model copy its own uncaveated format. The model knew the total (101) from `rfq.md` lines 16 and 64.
- **Tier:** live. **Family:** F1 (phantom completeness). **Demo-blocker:** fixed with F-011 for this question.

## F-012: holds raised in an RBAC caller's turn do not show on the desktop approval card

- Stated by the Platform audit session as a known gap of RE079: a hold belongs to the caller's tenant, so the myBrain card does not list it; it is decided by a bare yes/no in the chat or with `flx approvals`.
- **Consequence:** a single "yes" in a chat can approve a gated write without the card's context. **Tier:** reported (not yet observed live). **Demo-blocker:** yes for approval scenes.

## F-013: the fixed listing still misstates what it shows

- Trace `a2e43c82…`: (1) header "Requirements all 101 in `fluvoro`, in document order" vs footer "No row carries a recorded order, so this is id order, not document order" (the collection was ingested before order was stored); (2) asked for "ID with its title", it shows the requirement text cut at ~160 characters with no ellipsis; the `#` column is "–" in every row; (3) the sources line says "evidence unavailable".
- **Tier:** live (maintainer's paste). **Demo-blocker:** no (header contradiction is visible in a demo).

## F-014: a listing turn leaves no turn record, trace or outcome

- For trace `a2e43c82…` the only record is the `chat.listing` audit line; `turn_records`, `trace_runs` and `outcomes` have nothing, so `flx audit turn`, the trace view and the outcome spine cannot see the turn. Matches "evidence unavailable" in myBrain.
- **Tier:** live (stores). **Demo-blocker:** no.

## F-015: outcome attribution is still partial after RE079

- Ordinary turn `f3f52ac5-e621-4886-9c5a-92e2aa5fe308`: the audit carries `siimplex` / `fluvoro-operator` on every row (F-009 PASS), but in `outcomes.db` the `chat_turn` row has the tenant and an empty `actor_id`, and the six `capability_call` rows have empty tenant and actor.
- **Tier:** live. **Demo-blocker:** no.

## F-016: the turn token count is constant

- All four listing turns record exactly 124 tokens although the answers differ in length. The `tokens` field in `outcomes.db` does not reflect the answer.
- **Tier:** live (store). **Demo-blocker:** no.

## F-017: an unannounced deploy during the test run

- `b13bbb8e` (work-item merge E1–E5, 30 files) was deployed at 14:19:53Z with a restart at 14:20:03Z, without an announcement to this run; controls 1 and 2 therefore ran on `b13bbb8e`, not `eefbbeb8`. It did not contain either fix, so the results stand. Found only through `~/Sandbox/logs/deploy_receipts.ndjson`.
- **Tier:** live (receipts). **Demo-blocker:** no; mitigated by recording served_commit per phase.

## F-018: QuotPilot was configured against the production QPMT, and its read capabilities fail without an error text

- `~/Sandbox/flexcortex.conf:125` had `QPMT_BACKEND=rest` with `QPMT_URL` set to the production host (code default `mock`), contrary to the run rule "QPMT on the mock backend only".
- Turn `f3f52ac5…` ("What does the RFQ say about the delivery date?") selected the quotpilot skillpack; `quotpilot.fetch_requirements`, `analyze`, `decide`, `analyze_rfq` and `ask` each failed in ~0.01 ms, `cause: tool_failure`, with no error text in the audit row or in outcomes; the turn ended `partial`. No gated write (`generate`, `finalize_quote`) was called.
- **Action:** switched to `mock` for the run (D-13), core restarted 15:15:46Z (announced). The silent failures remain to be checked on mock in Phase 1.
- **Tier:** live (audit, outcomes, config). **Demo-blocker:** yes (the RFQ scene runs through quotpilot).

## Isolation check (step 3)

The repository is at `~/Documents/GitHub/fluvoro`, outside `FILES_ALLOWED_ROOT=~/Sandbox`; the session workspace grants table is empty. `kit/hidden/` and `product/` are not reachable by file capabilities. The ingest uses a copy of `kit/shown/` only, at `~/Sandbox/knowledge_base/fluvoro`.
