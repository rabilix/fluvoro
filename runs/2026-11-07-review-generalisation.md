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
