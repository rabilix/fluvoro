# Phase 1, ninth run: findings

Numbering continues after F-062.

## Run 8 fixes, checked on T1 (trace fd629012-5422-4c8d-b4a5-6224b16ee3ed)

- **F-055 closed.** No tool line in the answer; the stored message starts with the answer and carries the call as `toolCalls: [quotpilot.analyze ok]`; the desktop shows only "Did 1 call".
- **RFQ open points asked, for the first time in the series.** The review's next steps ask AP-01 volume split, AP-02 connectivity timing, AP-03 hardware partner, taken by QuotPilot from the RFQ's §5 into the draft (`stated_open_points`). This closes the gap noted since run 6.
- **F-050/F-048 hold:** one analyze, no empty pre-fetch, 1 min 38 s, saved.

## F-060 worse: the model rewrites requirement ids, not only shortens them

- T1's package table (model-written, 10 sections) shortens evidence with "…" AND changes ids: "FLV-041", "FLV-135", "FLV-133", "FLV-073", "FLV-067", "FLV-066", "FLV-065", "FLV-100" (the draft holds FLV-STK-041 etc.). Platform audit confirmed nothing in this build addresses F-060. In run 8 it appeared on follow-up turns only; here on T1 too. Requirement ids that do not exist in the CRS are a traceability error a customer would notice.
- "Analysis mode: Deterministic (no LLM assistance used)" misstates the F-051 outcome (the assist was called and gave no answer within 60 s; the draft says `no_answer`).
- **Tier:** live. **Family:** QuotPilot answer shaping. **Demo-blocker:** yes now (invented ids). Candidate as before: the package table with its ids is passed through unchanged; the model explains around it.

## F-063: the customer's answers to the RFQ's open points reach the chat, not the draft

- T2 (trace 3519e274-89ff-4dbb-a866-c000ecd29439): the customer answered AP-01..AP-03 verbatim. The answer shows them in a table "Customer assumptions that must be included in the quote", but the model's `quotpilot.decide` carried only `{"OC-PLATFORM": "RTOS (FreeRTOS/Zephyr)"}` (plus `overwrite: true`). `decide` accepts AP answers as free-text assumptions (`agent/capabilities.py:846-863`, stored as `assumed` on `stated_open_points`), but none was sent; the draft's AP-01..AP-03 have no `assumed`. Generate builds the Assumptions sheet and both emails from the draft (`outputs/workpackage_writer.py:359`, `supplier_email_en/de.py:151`), so the deliverables will not carry what the customer said, while the chat says they "must be included".
- The model also sent `overwrite: true` on an open decision unasked; harmless here, but it defeats F-061's guard whenever the model chooses to.
- **Tier:** live. **Family:** QuotPilot workflow state (the pack asks, the model records half). **Demo-blocker:** yes for the quote basis. Candidates: the pack prompt names the AP ids as decide answers ("record every customer answer with decide, AP-… included"); after decide, the result lists what is still unassumed so the model sees the gap; `overwrite` only when the person asked to change an answered decision.

## T3: the approve path works end to end

- **F-062 closed.** The held generate carried `run_id = 5654fe3c…` (the T1 run); the card showed it plainly; the maintainer approved; the hold went dispatched → executed; generate ran in 92 ms and wrote `Workpackages.xlsx` and `review.md`. First complete analyse → decide → generate in the series.
- **F-061 holds:** the plan had one step; no decide was repeated; the platform stayed "RTOS (FreeRTOS/Zephyr)".
- Small: no audit row records the approval decision (the denial got one in 9fff709f; the approval did not).

## F-064: the generated work packages are a generic template, not the device

- `Workpackages.xlsx` has 14 work packages: requirement analysis, architecture, integration testing, "Cantata / Unit Tests", "Polyspace / MISRA", OTA, integration support, release/documentation and ASPICE SWE.1–SWE.6. Of the draft's 16 packages only one (OTA / Update Manager) became a work package. Motor control (20 requirements), energy management (37), jam / overload detection (13), BLE, functional safety (6), self-test, fault handling, service interface, event log, time keeping, low-power, sensor acquisition, user indication, RTOS/scheduler and HAL/drivers have none. Thirteen of 14 rows have no related package and no requirement.
- **Effort is empty in every row.** The RFQ asks for effort per work package (§3); the deliverable that should carry it has none.
- The assumptions are automotive ECU defaults (Cantata/VectorCAST and Polyspace licences, "target ECU", HIL) for a consumer garden device on an RTOS, and nothing reflects ISO 26262 / functional safety, which the analysis classified as a mandatory package.
- Overview still says status DRAFT after "GENERATED".
- **Tier:** live. **Family:** QuotPilot generation content. **Demo-blocker:** yes; this is the deliverable the whole conversation leads to. Not a seam: the platform did everything right and handed QuotPilot the right run; the content is QuotPilot's generator. Candidates: one work package per mandatory package carrying its requirement ids; effort per work package (or the explicit statement that effort is the next step and who provides it); assumptions drawn from the detected domain and platform, not the AUTOSAR template; the Overview status follows generation.

## F-065: asked for effort, the model invents a full estimate and cites "our past projects"; the refusal line does not stop it

- T4 (trace f99dd5a3-9a12-4b9d-9227-4396fd172019): "Show me the work packages with the effort per package." The generated workbook has no effort (F-064). The model called a non-existent `quotpilot_generate` twice (refused, "not in the pack's callable set"), read nothing (no `quotpilot.ask`), and then wrote a 14-row effort table, 181 person-days total, a 40 % contingency, roles, confidence levels, and a derivation that cites "similar safety-critical automotive packages in our past projects". It adds content that is in no source: ASIL-B and SOTIF, "CAN-open/SAE J1939" for the service interface, "SUMS" for OTA, and claims the customer's AP answers "were incorporated" (they are not on the draft, F-063).
- RE108 §3 worked mechanically: the runtime appended "[runtime] quotpilot_generate was not run …", but twice, truncated mid-list, and after a confident estimate the reader takes as real. The F-054 rule ("the model is told not to produce the artifact itself") did not hold on the chat path when the tool name was wrong.
- **Tier:** live. **Family:** answer honesty (F-054's class, now with fabricated provenance). **Demo-blocker:** yes, the most serious content defect of the series: an invented quote with an invented basis.
- Candidates: an effort figure may appear in an answer only when a tool result carries it (or is marked "illustrative, not from any source" in the first line, not at the end); a refused call whose name is a near-miss of a real capability is corrected to it or answered "did you mean quotpilot.generate"; the runtime statement goes first, once, untruncated; QuotPilot produces effort (F-064) so the model has a source to read.

## T1 grading against kit/shown

- Work packages: 14 with CRS ids (ids partly corrupted in the visible text, see F-060).
- Questions to the customer: the platform decision plus all three of RFQ §5's open points. First run that asks what the RFQ asks.
- Effort: none yet (by design until generate).
