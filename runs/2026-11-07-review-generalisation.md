# Review after run 9: are the fixes general or fitted to Fluvoro?

Held 2026-11-07 with the maintainer after Phase 1 run 9. Trigger, in the maintainer's words: "I am afraid you are overfitting over this one task."

## Why the concern holds

- Nine runs used one RFQ, one prompt, one set of customer answers and the same three or four turns. Each fix moved the failure one step further along that one path.
- The end-to-end probe (RE108 `probe_person_path_quotpilot`) replays that conversation with a stub that plays back gpt-oss's calls.
- Several fixes are phrase- or format-shaped (routing on "Proceed … and generate", the RFQ open-points reader, pack keywords), and two prompt patches overshot (F-052 → F-060).
- Grading used one sample per build, although the same prompt on the same build gave visibly different answers (fenced or rendered review; RFQ open points asked or not).
- Fluvoro's specification is short (longest requirement 285 characters), so ingestion splitting never happened; reading the code found two latent gaps (F-066, F-067).

## Fix list

| Fix | What it does | Read |
|---|---|---|
| F-044/45/46 | workspace path refused; project from the RBAC membership | mixed: the fallback needs exactly one membership |
| F-049 | orphaned approval cards moved to blocked | general |
| F-057 | approvals listed and decided as the caller | general |
| F-058 | step values name the field; a halted plan withdraws its holds | general |
| F-062 | declared run_id filled only from a single conversation value; validated before the card | general |
| denial audit row | a denial is in the audit trail | general |
| F-055 | tool calls kept out of the answer text | general |
| F-047/F-050 | pre-fetch never fires a capability that needs arguments | general |
| F-048 | tool rounds bounded by the client budget; analyze final | general (finality QuotPilot-specific) |
| F-051 | assist outcome stated | general |
| F-054 part 1 | a refused write is said; the model is told not to produce the artifact | general, not effective (F-065) |
| in progress | figures only from a tool result; near-miss tool names; runtime statement first | general |
| RE093 carry | previous pack kept for a reply ≤ 6 words answering a "?" | fitted (run 3's one-word reply) |
| F-053 | sticky pack; switch needs 3 own hits and 3 more | mixed: thresholds set on our turns; a genuine task switch untested |
| F-054 part 2 | a go-ahead plus an action verb routes to the agent path | fitted (our T3 sentence) |
| F-056 | the open run handed to the agent path | mixed: knows only calls that declare a run id |
| F-052 | operator block out of the review; "verbatim" out of the prompt | fitted, overshot (F-060) |
| F-061 | decide refuses values outside the options; keeps answered decisions | general |
| AP open points | reads "Points still open on our side" and "whether A or B" | fitted (this RFQ's heading and wording) |
| pending | F-060 ids, F-063 answers into the draft, F-064 generator | F-063 at risk of fitting our T2 message |
| RE108 probe | replays our conversation | fitted by design; regression value only |
| grading | one sample per build | fitted |

## Decisions

- **D-53** (2026-11-07). Question: the review found several fitted or mixed fixes (RE093 carry, F-053 thresholds, F-054 routing phrase, F-056, F-052 prompt wording, the RFQ open-points reader, the probe) — how to handle them? Chosen: keep them all; test them first on a second synthetic case with paraphrased prompts and repeated runs; Platform audit reworks only those that break, as general rules. Rules out: reworking the fitted ones before a second case exists; reverting them.
- Earlier in the same review (recorded in the cross-session hand-off, 2026-11-07): Platform audit continues the general fixes and holds the fitted ones; no run-10 deploy until the review is done.

- **D-54** (2026-11-07). Question: what is the second test case? Chosen: a new fictional customer and product in another domain, with its own RFQ, specification and answer book. Rules out: a Fluvoro variant only; both with the variant first.
- **D-55** (2026-11-07). Question: input formats? Chosen: requirements in Excel, RFQ in Word (intake paths Fluvoro never used). Rules out: ReqIF + markdown again; ReqIF + PDF.
- **D-56** (2026-11-07). Question: may Platform audit and the FlexCortex session see the case? Chosen: blind until graded; they receive only findings after a run. Rules out: sharing the shape; sharing the content.
- **D-57** (2026-11-07). Question: repeats per build? Chosen: 5 per build (key turns), known answers written before the first run. Rules out: 1 (single samples misled us), 3.

- **D-58** (2026-11-07). Question: where is the blind case built? Chosen: a new local git repository without a remote, outside this repository, until the case is graded; its domain and content are recorded there only. Rules out: a private GitHub repo now; building it under this repo's kit/ (readable on the shared branch). Note: the shape table below was pushed before this decision and is readable by the platform sessions; the content is not.

- **D-59** (2026-11-07). Question (Platform audit's design for F-065): when is an answer held until complete so that a note on unsourced figures can open it? Chosen: hold every answer; any unsourced effort, cost or percentage figure is named in the first line. Rules out: holding only turns where a call did not run (Platform audit's recommendation, keeps streaming); keeping the note at the end. Accepted cost: no live streaming on any turn. Also agreed: figures are never deleted from the model's text; refused or unknown tools tell the model not to supply what the tool would produce.

- **D-60** (2026-11-07). Question: deploy Platform audit's general fix list (near-miss names, runtime statement first, refusal wording, approval audit row, F-066, F-067, F-063 open-items list, D-59 held answers) and what runs first? Chosen: deploy, then the first run of the second case; the maintainer updates myBrain for the held-answer status. Rules out: a Fluvoro check run first; holding the deploy until the case files are reviewed. F-064 and F-060 stay held.

- **D-61** (2026-11-07). Question: the second case needs a project; F-045 fills a turn's project only from a person's ONE membership, so adding it to fluvoro-operator gives `ambiguous:2` and no project-scoped pack. How? Chosen: a separate operator `case2-operator` with only the `case2` membership and its own myBrain profile and key (issued by the maintainer). Rules out: moving fluvoro-operator's membership and restoring it; keeping two memberships (known failure).
- **D-62** (2026-11-07). Question: authorise the live writes for the case? Chosen: project `case2` (department engineering), principal and membership now; knowledge_base folder and ingestion only at run start under a freeze, after the maintainer's review of the files. Rules out: ingesting before the review; holding all writes.
- **Generalisation note (from D-61):** F-045's one-membership fallback fails for any person in two projects, the normal real-world case; the desktop does not name a project, so project-scoped packs drop out. Mixed fix per D-53; handed to Platform audit to rework as a general rule.

- **D-63** (2026-11-07). Question (maintainer: "In the future, i will have a dozen of projects running under my profile"): a separate operator per project only works around F-045. How to go on? Chosen: Platform audit first makes one profile work with many projects (the turn's project from the chat or the named collection, retrieval kept inside that project's collections); the second case then runs on the existing operator with both memberships, testing the real setup including cross-project leakage. Supersedes D-61 (no case2-operator; the setup commands given to the maintainer are not needed). Rules out: running the case now on a separate profile; running it on two memberships unfixed. Consequence: the second case starts after this fix.

- **D-64** (2026-11-07). Question: Platform audit's design for one operator with many projects (projects own collections; turn project from desktop, session, named collection, single membership, else asked once; retrieval narrowed to the project's collections on every door; desktop project chip) and its open points. Chosen: accepted; unassigned collections fail closed in project turns; the ask-once lists every membership; in addition memory (episodic recall, answer cache, facts store) and QuotPilot runs are project-bound, and a turn naming another project's collection is told to switch. Rules out: memory and runs per person only; unassigned collections readable everywhere.

- **Finding from D-64 (Platform audit, read in code 2026-11-07):** the answer cache and episodic replay are keyed by `principal_scope_key(user, dept, all of the person's projects)` (`scripts/routers/_deps.py`), not by the turn's project; the facts store by tenant only; and the replay lookup runs before project resolution. So one operator in two projects shares one cache and one episodic memory across both today: a latent cross-project leak that a single-project test like Fluvoro cannot show. The D-64 build keys cache, episodic and facts by the turn's resolved project (existing rows become the no-project bucket) and resolves the project before the first memory read.

- **D-65** (2026-11-07). Question: Open WebUI (`/v1/chat/completions`, all FlexRag: `rag-<collection>`, `rag-tag-<tag>`, `rag-cortex` = CortexRAG domain/topic search over every permitted collection) and the MCP server have no chat project — how do they respect projects? (The maintainer needs MCP client and server; Open WebUI for FlexRag.) Chosen: pick a project explicitly — one Open WebUI model per project (`rag-project-<id>`), MCP tools take a project argument; a named collection is checked against its owning project; `rag-cortex` and tags without a project read only unassigned or shared collections. Rules out: named collection only (no whole-project search from Open WebUI); searching across all the person's projects. Note: an earlier explanation in this session wrongly called `rag-cortex` the FlexCortex agent mode; it is FlexRag.
- **D-66** (2026-11-07). Question: projects start with no assigned collections and would read nothing. Chosen: until a project has any assignment, it reads the collection with its own id, and says so; fluvoro and case2 are still assigned at deploy. Rules out: failing closed until assigned (Platform audit's recommendation). The test leftover `sdfasfas` is left untouched.

- **D-67** (2026-11-07). Question: Platform audit's two security calls in the multi-project build. Chosen: (a) with RBAC off, the single operator sees every project; (b) with membership on, a key naming no person picks no project and reads only unassigned collections through Open WebUI and MCP. Consequence: Open WebUI and MCP clients need a key tied to the person to reach project data. Rules out: a person-less key reading every collection.
- **D-68** (2026-11-07). Question: when do the multi-project build (D-64/65/66) and held answers (D-59) deploy? Chosen: after the Codex review round passes, with probes and before/after messages; at deploy the collections are assigned (fluvoro, case2), project case2 is created and the maintainer's operator added; no ingestion until run start. Rules out: deploying the multi-project part alone first; waiting longer.
- Incident note (2026-11-07): Docker Desktop's backend crashed at 08:54Z (Qdrant, Postgres, Neo4j down); the maintainer restarted Docker and the whole stack (`rag restart`, 10:20Z); the new core (pid 74293) logged a clean start and vanished at about 10:21Z without a log line or crash report — either the launching terminal closed or a native crash of the Homebrew Python 3.11.16 (seen segfaulting under load, no faulthandler). The FlexCortex session's deploy 211fc8a6 started the core detached at 10:23Z. Open: whether the live core needs crash tracing and the standalone interpreter.

- Incident note (2026-11-07, later): the maintainer's PC crashed; it was up again at 12:28 local. Docker, core, facade and manager were down afterwards (only Ollama restarted); last deploy 211fc8a6, nothing of the series lost (no run, no freeze). Two Platform audit sessions started after the crash; this session works with the one that wrote first (socket 3567).
- **D-69** (2026-11-07). Question: after the crash, bring the old 211fc8a6 stack up first, or wait for the approved deploy? Chosen: wait; FlexCortex comes back with the D-59 + D-64/65/66 deploy once Platform audit's gate and reviews pass; the maintainer starts Docker Desktop. Rules out: an extra restart on 211fc8a6; the maintainer starting the stack by hand. Consequence: myBrain is unavailable until the deploy.

- **D-70** (2026-11-07). Question (maintainer: "I would like to use my profile … All tests should run under it so we can find bugs and interference early"): which identity do the tests run as? Chosen: a personal principal `rabilix` (tenant siimplex, department engineering, role member), member of fluvoro and case2, created by the maintainer in their own terminal, with its own myBrain profile "Rabilix"; every run from now on runs as it. Rules out: fluvoro-operator with an added case2 membership; a separate operator per case. Changed variable for every later run: two memberships, fresh per-person memory, no access to fluvoro-operator's QuotPilot drafts.
- Incident note (2026-11-07): the Mac kernel-panicked twice (11:53:52 and 14:30:13 local), same signature `pmap_recycle_page: page … is referenced` (macOS 27.0.1, 26A434), under load 20–35. Not caused by a user program; the morning's Homebrew Python GC crashes may share the cause. A memtester pass over 16 of 128 GB found no fault (not conclusive; Apple Diagnostics outstanding).
- **D-71** (2026-11-07). Question: after the memory test, how to go on? Chosen: bring the stack back up under light-load rules (one gate at a time, unneeded sessions closed), Apple Diagnostics when convenient. Rules out: Apple Diagnostics first; staying down.

- **D-72** (2026-11-07). Question: the first case 2 ingest showed that a spreadsheet requirement longer than one chunk loses its id and column names, the graph loads the automotive ontology for every collection, the graph extractor sees only the first 1,500 characters of a chunk, and Word sections and tables are split by size. Run 1 on these chunks, or fix first? Chosen (maintainer): fix first. Platform audit makes each spreadsheet row one requirement chunk carrying its column names, a long row split into "(part k of n)" pieces naming the row's id and joined again when read, and the graph seeing the whole chunk. The ontology and Word points were sent to Platform audit as general defects without naming the domain; the maintainer then put both into the same fix, before the re-ingest (FlexForge RE108). The fix has six parts: spreadsheet rows as requirements; the graph extractor's window sized in tokens (twice the chunk size; the 1,500-character window was a unit mismatch); retrieval pulls a long requirement's sibling parts by id; QuotPilot's intake reads requirement spreadsheets as joined requirements; every Word chunk carries its heading path and a table stays with its heading; the ontology profile follows the collection or its project, neutral when none is set. Tests use synthetic rows only. Sequence: build, review, the maintainer's go, deploy, re-ingest case2 with `--reset`, freeze, run 1. The before-picture is kept in the case 2 repo (runs/run1). Blindness (D-56): Platform audit knows the case is one Word and one Excel file; the grading and the hidden kit stay unshared, and the known answers stay as fixed. Rules out: running run 1 on the current chunks as a baseline; fixing the ontology and Word path after run 1 (a second re-ingest, and a graph that blurs the forbidden-terms score). Run condition added: the myBrain agent picker stays on Auto in every case run until the planned picker test has run (runs/planned-agent-picker-test.md).
- **D-73** (2026-11-09). Question: after the RE108 deploy (2834187ee) the case 2 re-ingest is mostly right (ids on every row, parts with id and title, values in their own row, the RFQ open-points table whole), but F-068 remains: a table inside a requirement cell produces extra points with no id heading that reuse the part number, so the retrieval join refuses that requirement (2 of 7 long ones). Also, myBrain had started its own facade from the working repo on Homebrew Python with open auth. Run now, or fix first? Chosen (maintainer: "fix and do all what needed"): fix first. Platform audit fixes F-068 (general: tables in requirement cells), starts the deployed facade on ~/flexEnv with auth, and finds why myBrain started its own; then a `--reset` re-ingest, the chunk check, the freeze, run 1. Rules out: running run 1 with F-068 as a known defect. Record: case 2 repo runs/run1/ingest_after_re108.md.
- **D-74** (2026-11-09). Question: case 2 run 1 is done (five repeats on 97f5883b5; summary in the case 2 repo, runs/run1/summary.md); lift the freeze and what next? Chosen (maintainer: "lift, and start fix"): freeze lifted; the six general findings F-069..F-074 go to the FlexCortex session as single owner, in the order F-073 (approved generate fails the project check, blocker), F-071 (unsourced-figure check misses table cells and U+2011 hyphens), F-072 (`{run_id}` placeholder held), F-074 (analyze_rfq writes deliverables without approval), F-070 (spreadsheet ids replaced by QP ids), F-069 (`--path` ingest not analysable). Case 2 run 2 runs only after all are live, with the same script. Not requested: a medical package catalogue or reading this RFQ's open-points table specifically (that would fit the platform to case 2; to be decided separately). Rules out: further runs before the fixes; fixing case-specific content.
- **D-75** (2026-11-09). Question: case 2 run 2 (core 6c9d6410c, QuotPilot 696937e) showed in turn 1 that F-070 is not effective (the draft still holds 124 QP ids from "pasted") and that the model's text was corrupted ("Lam" inserted 32 times, F-075; not in tool results). Continue run 2 for the other fixes, or stop? Chosen (maintainer: "re-fix all"): stop run 2, lift the freeze; the FlexCortex session re-fixes F-070 in the intake `analyze` actually uses, investigates F-075, and re-verifies F-069, F-071..F-074 end to end through the real chat and approval path; run 2 restarts from repeat 1 after its notice. Rules out: continuing run 2 on the current build; restarting only Ollama. Record: case 2 repo runs/run2/aborted.md.

### Second test case: required shape

| Dimension | Required |
|---|---|
| Domain | not consumer garden / motor-solar; own product, customer, packages |
| Requirements | Excel; several requirements well above 400 tokens (one with a table, one with its acceptance value in the last paragraph); ids in another scheme than FLV-STK |
| RFQ | Word; open points under another heading and phrasing, not "whether A or B"; one section across a chunk boundary |
| Requests | three paraphrases of the opening request, including a short one and a German one |
| Customer answers | in prose, out of the asked order, one partial; answer book written before any run |
| Follow-ups | "go ahead", "make the quote", and one genuine task switch mid-conversation |
| Grading | known answers (expected packages, expected questions, expected ids) fixed before the first run; 5 repeats per build |
| Isolation | same rule as Fluvoro: only the shown part is ingested; plus D-56 blindness toward the platform sessions |

## Open in this review
- Whether quote content (F-064, F-065) is this series' to chase or QuotPilot's own roadmap.
- What the handover set out to test beyond Phase 1 (step 6, team and board, never started).
