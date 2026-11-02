#!/usr/bin/env python3
"""Check product/hara.yaml against ISO 26262-3 Table 4 and against itself.

- every ASIL is recomputed from S/E/C (Table 4) and must equal the stated one;
- S0 / E0 / C0 give no ASIL ("none");
- every hazardous event with ASIL A-D names a safety goal; every QM/none one
  carries a qm_rationale;
- a safety goal's ASIL equals the highest ASIL of its hazardous events, and its
  safe state exists;
- every referenced OS / MF / HE / SG / SS / FLV-STK id exists, and every
  malfunction's leads_to agrees with the hazardous events' malfunction lists.
Exit 1 naming each problem.

    python3 tools/check_hara.py product/hara.yaml product/stakeholder_requirements.yaml
"""
import sys

import yaml

# ISO 26262-3:2018 Table 4 — rows S1..S3 x E1..E4, columns C1..C3
TABLE4 = {
    "S1": {"E1": ["QM", "QM", "QM"], "E2": ["QM", "QM", "QM"], "E3": ["QM", "QM", "A"], "E4": ["QM", "A", "B"]},
    "S2": {"E1": ["QM", "QM", "QM"], "E2": ["QM", "QM", "A"], "E3": ["QM", "A", "B"], "E4": ["A", "B", "C"]},
    "S3": {"E1": ["QM", "QM", "A"], "E2": ["QM", "A", "B"], "E3": ["A", "B", "C"], "E4": ["B", "C", "D"]},
}
RANK = {"none": -1, "QM": 0, "A": 1, "B": 2, "C": 3, "D": 4}


def asil(s, e, c):
    if s == "S0" or e == "E0" or c == "C0":
        return "none"
    return TABLE4[s][e][int(c[1]) - 1]


def main(hara_path, stk_path):
    h = yaml.safe_load(open(hara_path, encoding="utf-8"))
    stk = {r["id"] for r in yaml.safe_load(open(stk_path, encoding="utf-8"))["requirements"]}
    p = []
    os_ids = {o["id"] for o in h.get("operational_situations", [])}
    mf = {m["id"]: m for m in h.get("malfunctions", [])}
    he = {x["id"]: x for x in h.get("hazardous_events", [])}
    sg = {x["id"]: x for x in h.get("safety_goals", [])}
    ss = {x["id"] for x in h.get("safe_states", [])}
    if not he or not sg:
        p.append("no hazardous events or no safety goals (an empty HARA must fail)")
    for e in he.values():
        i = e["id"]
        want = asil(e["severity"], e["exposure"], e["controllability"])
        if str(e.get("asil")) != want:
            p.append(f"{i}: stated ASIL {e.get('asil')} but {e['severity']}/{e['exposure']}/{e['controllability']} gives {want}")
        for o in e.get("situations", []):
            if o not in os_ids:
                p.append(f"{i}: unknown situation {o}")
        for m in e.get("malfunctions", []):
            if m not in mf:
                p.append(f"{i}: unknown malfunction {m}")
            elif i not in mf[m]["leads_to"]:
                p.append(f"{i}: lists {m}, but {m}.leads_to does not list {i}")
        for r in e.get("stakeholder_refs", []):
            if r not in stk:
                p.append(f"{i}: unknown stakeholder requirement {r}")
        if RANK[want] >= 1:
            if e.get("safety_goal") not in sg:
                p.append(f"{i}: ASIL {want} but no valid safety_goal")
        elif not e.get("qm_rationale"):
            p.append(f"{i}: {want} without qm_rationale")
    for m in mf.values():
        for x in m["leads_to"]:
            if x not in he:
                p.append(f"{m['id']}: leads_to unknown {x}")
            elif m["id"] not in he[x].get("malfunctions", []):
                p.append(f"{m['id']}: leads_to {x}, but {x} does not list it")
    for g in sg.values():
        evs = [he[x] for x in g.get("hazardous_events", []) if x in he]
        if not evs:
            p.append(f"{g['id']}: no hazardous events")
            continue
        top = max((asil(x["severity"], x["exposure"], x["controllability"]) for x in evs), key=RANK.get)
        if g.get("asil") != top:
            p.append(f"{g['id']}: ASIL {g.get('asil')} but its highest hazardous event is {top}")
        if g.get("safe_state") not in ss:
            p.append(f"{g['id']}: unknown safe state {g.get('safe_state')}")
        if not g.get("ftti_ms"):
            p.append(f"{g['id']}: no FTTI")
    for x in p:
        print("FAIL", x)
    print(f"{len(he)} hazardous events, {len(sg)} safety goals, {len(mf)} malfunctions; "
          + ", ".join(f"{g['id']}={g['asil']}" for g in sg.values()))
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
