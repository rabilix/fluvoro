#!/usr/bin/env python3
"""Check a Fluvoro requirements YAML: schema, unique ids, valid enums, and that
every FLV-* id cited in a text or rationale exists. Exit 1 naming each problem.

    python3 tools/check_spec.py product/stakeholder_requirements.yaml
"""
import re
import sys
from collections import Counter

import yaml

ENUMS = {
    "variant": {"common", "V1", "V2", "option_ble"},
    "category": {"function", "hydraulic", "energy", "environment", "mechanical",
                 "installation", "safety", "compliance", "interaction", "lifecycle",
                 "quality", "project", "cybersecurity"},
    "verification": {"test", "analysis", "inspection", "demonstration"},
    "basis": {"regulation", "standard", "customer_need", "engineering_assumption"},
}
FIELDS = ["id", "title", "text", "variant", "category", "verification", "basis", "rationale"]
REF = re.compile(r"FLV-[A-Z]+-\d{3}")


def main(path: str) -> int:
    doc = yaml.safe_load(open(path, encoding="utf-8"))
    reqs = doc.get("requirements") or []
    problems = []
    if not reqs:
        problems.append("no requirements found (an empty set must fail)")
    ids = [r.get("id") for r in reqs]
    for i, n in Counter(ids).items():
        if n > 1:
            problems.append(f"duplicate id {i}")
    known = set(ids)
    for r in reqs:
        rid = r.get("id", "?")
        for f in FIELDS:
            if not r.get(f):
                problems.append(f"{rid}: missing {f}")
        for f, allowed in ENUMS.items():
            if r.get(f) not in allowed:
                problems.append(f"{rid}: {f}={r.get(f)!r} not in {sorted(allowed)}")
        if "shall" not in (r.get("text") or ""):
            problems.append(f"{rid}: text has no 'shall'")
        for ref in REF.findall((r.get("text") or "") + " " + (r.get("rationale") or "")):
            if ref not in known:
                problems.append(f"{rid}: cites unknown {ref}")
    for p in problems:
        print("FAIL", p)
    c = lambda k: dict(sorted(Counter(r.get(k) for r in reqs).items()))
    print(f"{len(reqs)} requirements; variant {c('variant')}; basis {c('basis')}")
    print(f"category {c('category')}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
