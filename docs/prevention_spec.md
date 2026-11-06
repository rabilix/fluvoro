# Catching the run-series defects before a run: probes and review rules

Written 2026-11-06 after Phase 1 runs 3–7. Nine live defects (F-045, F-047, F-048, F-053, F-054, F-056, F-057, F-058 and the F-049 gap) passed unit tests, the full gate, Codex rounds and CodeRabbit. All of them sat where two components meet, not inside one. This note specifies three things so the next series finds them on the first run: one end-to-end probe (§1), a two-tenant rule for fixtures (§2), and a "say every failure" rule (§3). §4 gives the review rules for Codex and CodeRabbit in the form they read. Platform audit owns the placement in the FlexCortex repo; this document is the hand-off.

Probe style follows the existing live probes (`scripts/probe_*.py`): spare-port core from the deployed tree in scratch, stub Ollama that replays the field model, known answers fixed outside the code under test, exit 0 / 1 (named difference) / 2 (infrastructure), one write outside scratch (the attestation).

## 1. probe_person_path_quotpilot — one person, one conversation, through the desktop route

**Purpose.** Walk the Fluvoro conversation exactly as a person does from myBrain: facade, RBAC caller, chat path, held write, approval card. One probe, one scenario, run on every deploy of the core, the facade or QuotPilot. It replaces nothing; it is the only test that crosses every seam at once.

**Setup.**
- Spare-port core from `$RAG_DIR`, scratch data root, the Fluvoro kit (`kit/shown/` only) as collection `fluvoro`, project `fluvoro` with a record, RBAC membership `fluvoro-operator → fluvoro` in tenant `siimplex`.
- A spare-port facade in front of it with its own service key in tenant `operator` (the production shape: the facade's key is not the caller's key).
- Stub Ollama replaying the field model, scripted per turn: T1 one `analyze(collection, project)` then an answer; T2 one `decide(run_id, answers)`; T3 a plan that calls `decide` with the previous run id and `generate` with the same id.
- QPMT backend mock. Episodic off.

**Turns, sent through the facade as the caller (`fluvoro-operator`), the way myBrain sends them.**
1. T1 = the Phase 1 turn 1 prompt (verbatim, from `runs/2026-11-02-phase1/transcript.md`).
2. T2 = the answer-book fallback sentence ("Customer answer to the platform question: This is not specified by us. …", 27 words).
3. T3 = "Proceed with RTOS and generate the work packages."
4. D = the desktop's Deny on the card T3 raised, via `POST /api/facade/v1/approvals/<id>/deny` with the facade's own key, as myBrain does.

**Known answers (each a named check; the probe fails on the first miss and names it).**
- K1 T1: `request.start` carries project `fluvoro` via membership and skillpack `quotpilot`; no capability ran with empty kwargs before the first model token (F-047/F-050); `quotpilot.analyze` ran exactly once with `collection=fluvoro` and the turn's project (F-048); `request.complete` present; the facade's session list holds the chat with both rows (F-048); the answer text contains neither "say Go" nor a `quotpilot.` call string (F-052).
- K2 T2: `skillpack.carried` with reason "sticky workflow within the carry window" before `request.start` (F-053); `quotpilot.decide` ran with the T1 run id; the draft's OC-PLATFORM is answered and the platform set; no second `analyze` (F-048).
- K3 T3: the turn took the agent path; the pack is the same; the plan's `decide` and `generate` name the T1/T2 run id, not a new one and not a dict (F-056, F-058); `analyze` did not run again; `generate` is held, with `run_id` a 32-char hex string in the recorded kwargs (F-058); no effort number appears in any answer text (F-054).
- K4 D: the deny answers ok; the record's status is `denied`; the facade's approval list for the caller showed the hold before and not after (F-057); a Deny of a hold whose plan was halted is accepted or the hold was already withdrawn with a reason, never "no pending action" (F-058).
- K5 Always: the audit of every tool failure or refusal in the three turns is mirrored by a sentence in the answer the person received (§3).
- K6 The deployed confs are unchanged; one write outside scratch (the attestation).

**Why it would have caught the series.** K1 fails on the trees of runs 4–6, K2 on run 6, K3 and K4 on run 7. None of these needed a real model: the stub replays what gpt-oss did.

**Cost.** Two spare ports, about 90 s. It runs in the full gate and as the post-deploy probe. The scenario file (turns, stub script, known answers) lives next to the probe so a new scenario is a new file, not new code.

## 2. Two tenants, two keys, in every fixture that touches identity

**Rule.** A unit or whole-turn test that creates, lists, decides or carries anything bound to a session (sessions, holds, approval cards, work items, pack carry, memos) runs with two keys: a caller key in tenant A and a service key in tenant B, and asserts the record is visible and decidable to the party the product promises, and invisible to the other.

**Where it applies now.** `flexcore/capabilities/approvals.py` (`_resolve_target`, list, approve, deny), `scripts/facade/turns.py` (`_decide_pending_action`, `_list_pending_actions_via_facade`), the pending-action store, work items, the sticky carry's session metadata.

**Why.** F-057 is a one-line lookup under the wrong tenant. It is invisible in a single-tenant fixture by construction; no amount of review finds it there. RE079 changed the turn's identity after the card code was written, and nothing exercised the pair.

**Fixture shape.** `tenant_pair()` yields `(caller_ctx, service_ctx)` with distinct `tenant_id` and keys; a helper `as_desktop(service_ctx, session_id)` builds the context the card route builds (`decision_door="card"`, caller's session id, service key's tenant). Tests say which of the two must succeed.

## 3. Every failed or refused step is said to the person

**Rule.** Any tool outcome that is not `ok` in a turn (tool_failure, refused, not_run, budget, unknown, assist no_answer, hold withdrawn) produces one plain sentence in the answer the person reads: what was not done and why, in the pack's words, never the raw payload. RE104 does this for retrieval; this extends it to tools, assists and approvals. The model is told the sentence; the runtime appends it if the model drops it.

**Checks.**
- A whole-turn test with one scripted tool failure asserts the sentence in the final answer text.
- `probe_person_path_quotpilot` K5 asserts it live across the three turns.
- The QuotPilot draft file carries `assist` (status and reason); the review's "Analysis mode" line says why when it is deterministic.

**Why.** F-047 (five empty calls shown as the model's), F-051 ("Deterministic only" with no reason), F-054 (a refused write replaced by invented numbers) and the F-057 message ("no pending action") all hid or disguised a failure. Each cost a run to understand.

## 4. Reviewer rules: Codex and CodeRabbit

Both reviewers saw the F-053/F-054 change and passed it, correctly: the diff was right. The rules below make them ask about the seams the diff touches. They go into the repository files the tools read; wording is ready to paste.

### 4.1 Codex — section for `AGENTS.md` (repo root)

```markdown
## Review rules for seams (added 2026-11-06 after Fluvoro runs 3–7)

When a change touches any of: identity (tenant, principal, API key selection),
sessions, holds/approvals/cards, pack selection or carry, the agent path's plan
values, or the facade↔core contract, the review must answer in writing:

1. Which existing code assumed the OLD rule? Name the files. (RE079 made the turn
   run as its caller; the approval card still decided under the facade's key — F-057.)
2. Does a fixture exercise this with two tenants and two keys? If not, say so and
   ask for it (§2 of docs/prevention_spec.md in the fluvoro repo).
3. If a workflow can continue on another path (chat → agent, agent → chat, carry),
   where does that path read the workflow's STATE (run id, open decisions), not
   just its pack? (F-056)
4. If a step value is passed from one tool result to another call, is the field
   named, and is the receiving argument validated against the capability's
   schema before a person is asked to approve it? (F-058)
5. For every non-ok tool outcome this change can produce, which sentence does the
   person read? (§3; F-047, F-051, F-054)
6. Does `scripts/probe_person_path_quotpilot.py` still pass on the changed tree?
   Run it; paste the attestation line.

A review that cannot answer one of these says "not verified" for that item
rather than approving.
```

### 4.2 CodeRabbit — `.coderabbit.yaml` (repo root)

```yaml
reviews:
  path_instructions:
    - path: "flexcore/capabilities/approvals.py"
      instructions: >-
        Any lookup of a pending action, hold or card must be bound to the tenant
        the record was created under (the session's tenant), not to the deciding
        key's tenant. Flag a store.get/list_pending whose tenant_id comes from the
        caller's key when the caller can be a service (facade) key. Ask for a
        two-tenant test (caller key tenant A, service key tenant B).
    - path: "scripts/facade/turns.py"
      instructions: >-
        The facade calls the core with two keys: its own (fs._rag_server_api_key())
        and the caller's (as_caller=True). For any route that lists or decides
        something a turn recorded (approvals, holds, sessions, work items), flag a
        call that uses the facade's key where the record was created by the
        caller's turn, unless the core binds by session tenant. Ask which key the
        chat turn used for the same session.
    - path: "flexcore/runtime.py"
      instructions: >-
        Pack selection and carry: when a pack is carried into another path (agent
        path, plan), flag a hand-off that passes the pack id without the pack's
        workflow state (open run id, open decisions). When a tool result feeds a
        later call, flag passing the whole result object as an argument; the field
        must be named and validated against the capability input_schema before an
        approval card is recorded. Every non-ok tool outcome (tool_failure, refused,
        not_run, budget, unknown) must reach the person's answer as a sentence;
        flag a path that records the outcome only in the audit.
    - path: "flexcore/agent*.py"
      instructions: >-
        A plan that halts (delivery gate) must withdraw its pending holds with a
        reason; flag a halt that leaves a hold in status pending. Corrective rounds
        that retry a failed step with the same malformed argument are a bug, not a
        retry; flag retries that do not change the argument shape.
    - path: "scripts/probe_*.py"
      instructions: >-
        A probe that drives a capability directly is not an end-to-end test. For
        changes under flexcore/runtime.py, scripts/facade/, flexcore/capabilities/
        approvals.py or the QuotPilot pack, ask whether probe_person_path_quotpilot
        was run on the changed tree and request its attestation.
  tools:
    github-checks:
      enabled: true
```

For QuotPilot's own repository, the same two paths apply: `src/quotpilot/agent/capabilities.py` (the assist outcome must be on the draft file and in the result's note; `analyze` must declare its one-of inputs; `generate`/`decide` validate `run_id` as 32-char hex before anything else) and `src/quotpilot/review.py` (the review text is for the person: no operator instructions, no tool syntax; those go into the result's `note`).

## 5. Order of adoption (suggested)

1. §4 files (an hour; no code change; immediately changes what both reviewers ask).
2. §1 probe (a day; Platform audit has the scaffolding from `probe_tool_context_across_turns.py`; the stub script is the field model's calls from runs 6–7's traces).
3. §2 fixture and the retrofits on approvals/facade decisions (half a day; the F-057 fix needs it anyway).
4. §3 as a runtime rule with one whole-turn test (half a day; F-051/F-052/F-054 work needs it anyway).

Then run 8 starts on a tree where the probe already passed.
