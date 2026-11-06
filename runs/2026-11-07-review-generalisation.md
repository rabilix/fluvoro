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

## Open in this review

- The shape of the second test case (domain, format, long requirements per F-066/F-067, open points across a chunk boundary, paraphrased requests, customer answers in prose or another order, repeats per build).
- Whether quote content (F-064, F-065) is this series' to chase or QuotPilot's own roadmap.
- What the handover set out to test beyond Phase 1 (step 6, team and board, never started).
