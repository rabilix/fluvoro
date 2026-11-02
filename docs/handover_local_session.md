# Handover: run Fluvoro through FlexCortex from a local session

- From: cloud session https://claude.ai/code/session_017J6AA7HMip1BMg6rQNNXoc (2026-11-02)
- To: a Claude Code session running **on the maintainer's Mac**, opened in this repository
- Why: the cloud session cannot reach the Mac. Remote Control showed no shared folder.

## 1. What this is

Fluvoro is a synthetic customer project: a solar-powered gutter-outlet leaf
shredder, with variant V1 insert, variant V2 replacement outlet, and a BLE option.
It is run through FlexCortex by a team of agents to find weak points in FlexCortex,
FlexRag and myBrain. The same run is also the basis for a myBrain demo.

- **Concept:** FlexForge, branch `claude/sleepy-meitner-rm81pw`,
  `docs/superpowers/specs/2026-11-01-user-simulation-gutter-shredder-concept.md`.
  Read sections 3–11a.
- **Ownership:** the Platform audit session owns the release-gate and disruption
  test items (RE060/RE061 and others; FlexForge develop `902445b`). This project is
  the later user-simulation and demo layer and reuses their runner and approver.

## 2. Repository layout and the isolation rule

| Path | Content | FlexCortex may see it? |
|---|---|---|
| `kit/shown/rfq.md` | RFQ-FLV-2026-01 from the fictional customer Kestrel Home Systems | **yes**: the input |
| `kit/shown/fluvoro_crs_v1.reqif` | CRS v1: 101 clean stakeholder requirements (no ASILs, no internal notes) | **yes**: the input |
| `kit/hidden/customer_answer_book.yaml` | the customer's answers, given only when asked | **no** |
| `product/` | clean reference: stakeholder requirements, item definition, HARA 0.2 (reviewed), FSC, 140 system requirements | **no**: grading reference and real product spec |

**Before FlexCortex runs anything:** check whether its file capabilities
(`FILES_ALLOWED_ROOT`, any session workspace grant) can reach this repository. If
they can, copy `kit/shown/` to a separate folder (for example
`~/fluvoro-input/`) and ingest from there, so `kit/hidden/` and `product/` stay out
of reach. Only `kit/shown/` may ever go into a collection the team can query.

## 3. Decisions already taken (do not re-ask)

- Everything is in English. V1 is primary, at NW 333 / DN 87–100 first.
- ISO 26262 is the customer's contractual frame. The team must **derive** the ASILs itself (the CRS gives none).
- The maintainer accepted all five HARA review recommendations (SG-01 A, SG-02 C, SG-03 A).
- The first run uses the **clean** CRS. The version with seeded defects comes later.
- The maintainer writes the blind quote estimate from the CRS alone, before the quote phase is graded.
- QPMT runs on the **mock backend** only. The only live write target ever allowed is scratch quote M10534, and only if the maintainer says so.

## 4. Steps (ask the maintainer before each write)

1. **Read-only state:** `flx doctor`, `rag status`, `curl -s localhost:8001/health`
   (note `served_commit`, `code_current`, the provider and the model), and the facade
   handshake on :8788. Report it; change nothing.
2. **Ask:** use the real installation (a new project, its own collection and board),
   or a separate core on a spare port with its own data root?
3. **Isolation check** (section 2).
4. **Project:** create the project. `flx project create fluvoro <dept>`, and
   `flx department create` first if no department fits. Check `flx project --help`
   for the real arguments.
5. **Ingest** `kit/shown/` into a new collection, for example `fluvoro`:
   `rag ingest fluvoro --path <folder holding only kit/shown>` (check
   `rag ingest --help`). Verify that all 101 requirement ids can be listed ("list all
   requirements in fluvoro").
6. **Team and board:** create the work packages on the board and assign the crew
   seats (requirements_assessor, systems_modeller, architect, sw_dev, tester,
   review_judge, traceability_analyst). Crew runs are born paused at GATE 1; the
   maintainer approves in myBrain.
7. **Phase 1:** the RFQ analysis through myBrain chat (`quotpilot`). Answer the
   customer's open questions only from `kit/hidden/customer_answer_book.yaml`, and
   only for questions FlexCortex actually asked. Record which ones it asked.
8. **Log every finding** as you go: what the person saw, what the audit or turn
   records say, the trace id, and the evidence tier.

## 5. Rules from FlexCortex's CLAUDE.md that apply here

- Verify the **running** process (`/health.served_commit`, the audit log), not the source.
- Never write under the deployed roots from a test. A run on the real installation is real use, so say clearly which root it writes to.
- No commits to `main` or `develop`. In this repository, work on `claude/sleepy-meitner-rm81pw`.
