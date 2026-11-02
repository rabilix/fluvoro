#!/usr/bin/env python3
"""Check product/system_requirements.yaml against the stakeholder spec and the FSC.

- unique ids, required fields, 'shall', valid enums;
- every derived_from id exists (FLV-STK-* or FSR-*);
- ASIL inheritance: a requirement deriving from FSRs carries exactly the ASIL of
  those FSRs (all of them must agree); one deriving from no FSR is QM;
- every FSR is refined by >= 1 system requirement;
- every stakeholder requirement is refined, or listed in not_refined with a
  reason (and not both);
- variant consistency: a requirement derived only from V1 (V2, option_ble)
  stakeholder requirements carries that variant;
- cited FLV-SYS ids in texts exist.
Exit 1 naming each problem.

    python3 tools/check_sys.py product/system_requirements.yaml \
        product/stakeholder_requirements.yaml product/functional_safety_concept.yaml
"""
import re
import sys
from collections import Counter

import yaml

ENUM_VARIANT = {"common", "V1", "V2", "option_ble"}
ENUM_VERIF = {"test", "analysis", "inspection", "demonstration"}
FIELDS = ["id", "title", "text", "variant", "asil", "derived_from", "verification"]
SYSREF = re.compile(r"FLV-SYS-(\d{3})")


def main(sys_path, stk_path, fsc_path):
    s = yaml.safe_load(open(sys_path, encoding="utf-8"))
    stk = {r["id"]: r for r in yaml.safe_load(open(stk_path, encoding="utf-8"))["requirements"]}
    fsr = {r["id"]: r for r in yaml.safe_load(open(fsc_path, encoding="utf-8"))["functional_safety_requirements"]}
    reqs = s.get("requirements") or []
    p = []
    if not reqs:
        p.append("no system requirements (an empty set must fail)")
    ids = [r.get("id") for r in reqs]
    for i, n in Counter(ids).items():
        if n > 1:
            p.append(f"duplicate id {i}")
    known = set(ids)
    used_stk, used_fsr = set(), set()
    for r in reqs:
        i = r.get("id", "?")
        for f in FIELDS:
            if not r.get(f):
                p.append(f"{i}: missing {f}")
        if r.get("variant") not in ENUM_VARIANT:
            p.append(f"{i}: variant {r.get('variant')!r}")
        if r.get("verification") not in ENUM_VERIF:
            p.append(f"{i}: verification {r.get('verification')!r}")
        if "shall" not in (r.get("text") or ""):
            p.append(f"{i}: text has no 'shall'")
        srcs = r.get("derived_from") or []
        fs = [x for x in srcs if x.startswith("FSR-")]
        ss = [x for x in srcs if x.startswith("FLV-STK-")]
        for x in srcs:
            if x not in stk and x not in fsr:
                p.append(f"{i}: derived_from unknown {x}")
        used_stk |= {x for x in ss if x in stk}
        used_fsr |= {x for x in fs if x in fsr}
        want = {str(fsr[x]["asil"]) for x in fs if x in fsr}
        a = str(r.get("asil"))
        if want:
            if len(want) > 1:
                p.append(f"{i}: derives from FSRs with different ASILs {sorted(want)}; split it")
            elif a != next(iter(want)):
                p.append(f"{i}: ASIL {a} but its FSRs are {next(iter(want))}")
        elif a != "QM":
            p.append(f"{i}: ASIL {a} without any FSR source (must be QM)")
        vs = {stk[x]["variant"] for x in ss if x in stk} | {v for x in fs if x in fsr for v in fsr[x].get("variants", [])}
        specific = vs - {"common"}
        if specific and "common" not in vs and len(specific) == 1 and r.get("variant") != next(iter(specific)):
            p.append(f"{i}: sources are only {next(iter(specific))} but variant is {r.get('variant')}")
        for n in SYSREF.findall(r.get("text") or ""):
            if f"FLV-SYS-{n}" not in known:
                p.append(f"{i}: cites unknown FLV-SYS-{n}")
    for x in sorted(set(fsr) - used_fsr):
        p.append(f"{x}: no system requirement refines it")
    nr = {x["id"] for x in s.get("not_refined", [])}
    for x in s.get("not_refined", []):
        if x["id"] not in stk:
            p.append(f"not_refined lists unknown {x['id']}")
        if not x.get("reason"):
            p.append(f"not_refined {x['id']} has no reason")
    for x in sorted(set(stk) - used_stk - nr):
        p.append(f"{x}: not refined by any system requirement and not listed in not_refined")
    for x in sorted(used_stk & nr):
        p.append(f"{x}: listed in not_refined but refined by a system requirement")
    for x in p:
        print("FAIL", x)
    c = Counter(str(r.get("asil")) for r in reqs)
    print(f"{len(reqs)} system requirements; ASIL {dict(sorted(c.items()))}; "
          f"stakeholder covered {len(used_stk)}/{len(stk)} (+{len(nr)} not_refined); FSR covered {len(used_fsr)}/{len(fsr)}")
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
