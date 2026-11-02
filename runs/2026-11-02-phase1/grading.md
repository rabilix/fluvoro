# Phase 1 grading: RFQ analysis

- **Graded by:** cloud "Test Framework" session, 2026-11-02, against `product/`
  (clean reference) and `kit/hidden/customer_answer_book.yaml`
- **Input:** this run directory (commit e5cc8e3); traces 2e5aef9f (turn 1), f7baba90 (turn 2), 7a81cfb4 (turn 3)
- **Model tier:** local_engine, ollama gpt-oss:20b
- **Run validity:** **infra-mixed.** Five deploys or restarts happened during the phase (run.yaml). The chat path diff between turns 1–2 and turn 3 does not touch quotpilot, the prompt composer or the facade, so the grades below hold for both commits. A rerun should be single-commit.

## Verdict: FAIL

The phase produced an analysis that looks complete but is not grounded in the
customer's specification. The run used the clean CRS on purpose, so this failure
comes from the system, not from defects in the input.

| # | Criterion (fixed before the run, concept §6 phase 1) | Reference | Result | Grade |
|---|---|---|---|---|
| 1 | The analysis reads the input: RFQ and all 101 CRS requirements | 101 requirements + RFQ §1–6 | 0 of 101 CRS requirements. Only retrieved RFQ chunks were analysed, as 17 "requirements" QP-001…017 such as the date line and headings. It claims "derived from … the attached CRS" (F-019). | **fail** |
| 2 | What to develop: the item's functions are identified | 7 functions F1–F7 (item definition §2): clog detection, shred cycle and motor control, energy management/BMS/MPPT, access protection, fault handling, signalling and service, BLE option | 0 of 7. A generic automotive ECU basic-software catalogue (OS, BSW, EcuM, DEM, WdgM, Flash Bootloader, UDS, MCAL, NvM, XCP, COM) instead, with "Embedded non-AUTOSAR" detected at the same time (F-020) | **fail** |
| 3 | Safety frame recognised | ISO 26262 tailored to a non-vehicle item. ASILs to be **derived by HARA** (FLV-STK-070) | A "Functional Safety package" is listed (good). Then the ASIL is asked of the customer (turn 2 #4) and **assumed** as "ASIL C (or SIL 3)" in turn 3 (F-031). The reference has C only for SG-02, by HARA; a blanket C is not derived. | **fail** (process) |
| 4 | Work packages proposed | requested in the prompt and in RFQ §3.1 | none in 3 turns (F-024) | **fail** |
| 5 | Questions to the customer: recall | answer book CA-01…CA-05 | **3 of 5** (CA-01–03, which restate RFQ §5). Missed: CA-04 reference site/season, CA-05 safety assessment | partial |
| 6 | Questions to the customer: precision | a question is useful if the RFQ and CRS do not already answer it and it is in scope | **3 of 15** useful. 7 ask for data the CRS or RFQ already gives (#4 in the bidder's scope; #6, #7, #8, #10, #11, #13). 3 assume out-of-scope context (#9 REST/MQTT, #14 PLC/cloud/CI, #15 legacy controls). 2 are vague (#5, #12) (F-025) | **fail** |
| 7 | Factual fidelity: no invented values | every number traceable to the RFQ or CRS | 4 of 4 extracted constraints invented (256 KB, 1 ms, 5 W, 1 Mbps). The turn 2/3 example values and defaults contradict the CRS: Li-ion vs LiFePO4 (FLV-STK-038); 0–60 °C vs −20…+50 °C (FLV-STK-050); 0.5 kg vs ≤ 1.2 kg (FLV-STK-116); DIN mounting; REST/MQTT/Azure; "GateGuard endpoint" (F-020, F-030) | **fail** |
| 8 | The customer's answers are used | the reply said: CA-01–03 answers, then "make an assumption and state it" for 4–15 | Acknowledged, not used. It asked the customer to confirm 12 assumptions, the opposite of the instruction (F-029) | **fail** |
| 9 | Honest statements | ADR-0017: no false completeness, every failure said | Raw tool errors shown truncated (F-022); "Risks & Assumptions: No findings" after 2 of 3 calls failed; "derived from the attached CRS" is false (F-019) | **fail** |

**Positive:** the three RFQ open points were found and given sensible defaults
(turn 1, OC-001–003). The draft is DRAFT-marked and held for "Go", so nothing was
generated without consent. The safety work was recognised as a package.

## Root causes (clustered across F-019…F-031)

| Cluster | Findings | What it means | Fix owner |
|---|---|---|---|
| **A. QuotPilot cannot get the whole input** | F-019, F-021, F-023 | The skill takes text or files. The model can only pass the top-k retrieved chunks; it cannot hand over the collection's files. A 101-requirement CRS never reaches the analyser. | Platform audit / QuotPilot owner |
| **B. Grounding** | F-020, F-025, F-030, F-031 | With about 5 sources the 20B model fills the gaps with plausible automotive defaults, and presents them as findings or assumptions. Partly a consequence of A, and partly the model. | A first; then a model-tier comparison |
| **C. Conversation state** | F-024, F-026, F-029 | It does not move from analysis to work packages. The customer's open points are framed as our decisions, and answers do not change the analysis. | QuotPilot flow |
| **D. Surface, identity, governance** | F-008/9, F-012, F-014–016, F-022, F-027, F-028, F-032 (several already fixed live by Platform audit) | Desktop truth and attribution | Platform audit (in progress) |
| **E. Run hygiene** | F-017, five deploys in phase 1 | Results cannot be pinned to one commit | Agreement: a deploy freeze during a phase |

## Consequences for the next steps

1. **Do not start Phase 2 (quote) on this output.** There are no work packages, and the
   package list does not describe Fluvoro. A quote graded against it would measure
   nothing.
2. **The blind estimate is not blind** (D-16: a worked example by a session that had
   read the answer book; two assumptions match CA-02/CA-03). Phase 2 can only be
   graded without a blind band, unless the maintainer writes a new one from the CRS alone.
3. **Rerun Phase 1 after cluster A is fixed,** single-commit, with the same prompt and the
   same customer rules. Add one comparison run on a stronger model tier (cloud or a
   larger local model) to separate the model's share of cluster B.
4. **Step 6 (team and board)** depends on work packages, so it waits for the rerun. The
   board and crew mechanics could be exercised with hand-made packages, but that
   would no longer test "FlexCortex does the work".

## Demo blockers from Phase 1

F-011 (listing), F-019, F-020, F-024 and F-025 block demo scenes 1–3.
