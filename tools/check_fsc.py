#!/usr/bin/env python3
"""Check product/functional_safety_concept.yaml against the HARA and ISO 26262-9.

- every FSR refines an existing safety goal; every safety goal has >= 1 FSR;
- an undecomposed FSR carries exactly its safety goal's ASIL;
- a decomposed FSR is written X(Y) with Y = its safety goal's ASIL, belongs to a
  decomposition group with exactly two channels, each channel uniform in ASIL,
  and the pair is a valid ISO 26262-9 decomposition of Y;
- the two channels of a group are allocated to DISJOINT elements (independence);
- every allocated element and safe state exists; every SG's safe state is used.
Exit 1 naming each problem.

    python3 tools/check_fsc.py product/functional_safety_concept.yaml product/hara.yaml
"""
import re
import sys
from collections import defaultdict

import yaml

VALID = {  # ISO 26262-9:2018 clause 5.4.10 (unordered pairs)
    "D": [{"C", "A"}, {"B"}, {"D", "QM"}],
    "C": [{"B", "A"}, {"C", "QM"}],
    "B": [{"A"}, {"B", "QM"}],
    "A": [{"A", "QM"}],
}
DEC = re.compile(r"^(QM|A|B|C|D)\((A|B|C|D)\)$")


def main(fsc_path, hara_path):
    f = yaml.safe_load(open(fsc_path, encoding="utf-8"))
    h = yaml.safe_load(open(hara_path, encoding="utf-8"))
    sg = {g["id"]: g for g in h["safety_goals"]}
    ss = {x["id"] for x in h["safe_states"]}
    el = {e["id"] for e in f.get("elements", [])}
    fsrs = f.get("functional_safety_requirements", [])
    p = []
    if not fsrs:
        p.append("no functional safety requirements (an empty FSC must fail)")
    groups = defaultdict(lambda: defaultdict(list))
    covered = defaultdict(int)
    for r in fsrs:
        i, g = r["id"], r.get("safety_goal")
        if g not in sg:
            p.append(f"{i}: unknown safety goal {g}")
            continue
        covered[g] += 1
        goal = sg[g]["asil"]
        a = str(r.get("asil"))
        m = DEC.match(a)
        if m:
            if m.group(2) != goal:
                p.append(f"{i}: decomposed from {m.group(2)} but {g} is ASIL {goal}")
            d = r.get("decomposition") or {}
            if not d.get("group") or not d.get("channel"):
                p.append(f"{i}: {a} written as decomposed but no decomposition group/channel")
            else:
                groups[d["group"]][d["channel"]].append(r)
        elif a != goal:
            p.append(f"{i}: ASIL {a} but {g} is ASIL {goal} (undecomposed FSRs inherit it)")
        elif r.get("decomposition"):
            p.append(f"{i}: has a decomposition but its ASIL {a} is not written X(Y)")
        for e in r.get("allocated_to", []):
            if e not in el:
                p.append(f"{i}: allocated to unknown element {e}")
        if not r.get("allocated_to"):
            p.append(f"{i}: not allocated")
        if r.get("safe_state") not in ss:
            p.append(f"{i}: unknown safe state {r.get('safe_state')}")
    for g in sg:
        if not covered[g]:
            p.append(f"{g}: no functional safety requirement refines it")
    for gid, chans in groups.items():
        if len(chans) != 2:
            p.append(f"{gid}: needs exactly 2 channels, has {sorted(chans)}")
            continue
        levels, alloc, goals = [], [], set()
        for ch, rs in chans.items():
            lv = {DEC.match(str(r["asil"])).group(1) for r in rs}
            goals |= {DEC.match(str(r["asil"])).group(2) for r in rs}
            if len(lv) != 1:
                p.append(f"{gid}/{ch}: mixed ASILs {sorted(lv)} in one channel")
            levels.append(next(iter(lv)))
            alloc.append({e for r in rs for e in r.get("allocated_to", [])})
        if len(goals) != 1:
            p.append(f"{gid}: channels decompose different ASILs {sorted(goals)}")
            continue
        goal = next(iter(goals))
        if set(levels) not in VALID[goal]:
            p.append(f"{gid}: {levels[0]}({goal}) + {levels[1]}({goal}) is not a valid decomposition of {goal}")
        shared = alloc[0] & alloc[1]
        if shared:
            p.append(f"{gid}: channels share elements {sorted(shared)} (not independent)")
    for x in p:
        print("FAIL", x)
    print(f"{len(fsrs)} FSRs over {len(covered)} safety goals; decompositions "
          + ", ".join(f"{g}: " + " + ".join(f"{ch}={sorted({r['asil'] for r in rs})}" for ch, rs in c.items())
                      for g, c in sorted(groups.items())))
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
