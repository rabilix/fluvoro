#!/usr/bin/env python3
"""Render the SHOWN part of the Fluvoro kit from the clean specification.

    python3 tools/build_kit.py          # write kit/shown/fluvoro_crs_v1.reqif
    python3 tools/build_kit.py --check  # exit 1 when the committed file differs

Deterministic (fixed identifiers and timestamp) so a committed .reqif is exactly
what product/stakeholder_requirements.yaml says. Shown attributes: id, name, text,
chapter, variant, verification, rationale. NOT shown: `basis` (which values are
the author's engineering assumptions is internal) and no ASIL (FLV-STK-070: the
supplier determines ASILs by HARA).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "product" / "stakeholder_requirements.yaml"
OUT = ROOT / "kit" / "shown" / "fluvoro_crs_v1.reqif"
TITLE = "Fluvoro - Customer Requirements Specification (CRS) v1"
CHAPTERS = {
    "function": "1 Function", "hydraulic": "2 Hydraulics", "energy": "3 Energy",
    "environment": "4 Environment", "interaction": "5 User interaction", "safety": "6 Safety",
    "compliance": "7 Compliance", "cybersecurity": "8 Cybersecurity (connectivity option)",
    "mechanical": "9 Mechanics", "installation": "10 Installation", "lifecycle": "11 Lifecycle",
    "quality": "12 Quality", "project": "13 Project",
}
VARIANT_TEXT = {"common": "V1 and V2", "V1": "V1 insert", "V2": "V2 replacement outlet",
                "option_ble": "Connectivity option (V1 and V2)"}
#: internal provenance notes in the clean spec never reach the customer document
_INTERNAL = re.compile(r"\s*\(maintainer decision [0-9-]+\)")


def shown(text: str) -> str:
    return _INTERNAL.sub("", text)


ATTRS = [("ad-id", "ReqIF.ForeignID"), ("ad-name", "ReqIF.Name"), ("ad-text", "ReqIF.Text"),
         ("ad-chapter", "ReqIF.ChapterName"), ("ad-variant", "Variant"),
         ("ad-verif", "Verification"), ("ad-rat", "Rationale")]


def render(reqs: list[dict]) -> str:
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         "<!-- Fluvoro customer requirements specification. Synthetic project data. -->",
         '<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd">',
         "  <THE-HEADER>", '    <REQ-IF-HEADER IDENTIFIER="hdr-fluvoro-crs">',
         "      <CREATION-TIME>2026-11-02T00:00:00Z</CREATION-TIME>",
         "      <REQ-IF-TOOL-ID>fluvoro-kit</REQ-IF-TOOL-ID>",
         "      <SOURCE-TOOL-ID>fluvoro-kit</SOURCE-TOOL-ID>",
         f"      <TITLE>{escape(TITLE)}</TITLE>", "    </REQ-IF-HEADER>", "  </THE-HEADER>",
         "  <CORE-CONTENT>", "    <REQ-IF-CONTENT>", "      <DATATYPES>",
         '        <DATATYPE-DEFINITION-STRING IDENTIFIER="dt-str" LONG-NAME="String" MAX-LENGTH="4096"/>',
         "      </DATATYPES>", "      <SPEC-TYPES>",
         '        <SPEC-OBJECT-TYPE IDENTIFIER="sot-req" LONG-NAME="Requirement">', "          <SPEC-ATTRIBUTES>"]
    for ident, name in ATTRS:
        L += [f'            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="{ident}" LONG-NAME="{name}">',
              "              <TYPE><DATATYPE-DEFINITION-STRING-REF>dt-str</DATATYPE-DEFINITION-STRING-REF></TYPE>",
              "            </ATTRIBUTE-DEFINITION-STRING>"]
    L += ["          </SPEC-ATTRIBUTES>", "        </SPEC-OBJECT-TYPE>", "      </SPEC-TYPES>", "      <SPEC-OBJECTS>"]
    for r in reqs:
        vals = [("ad-id", r["id"]), ("ad-name", r["title"]), ("ad-text", shown(r["text"])),
                ("ad-chapter", CHAPTERS[r["category"]]), ("ad-variant", VARIANT_TEXT[r["variant"]]),
                ("ad-verif", r["verification"]), ("ad-rat", shown(r["rationale"]))]
        L += [f'        <SPEC-OBJECT IDENTIFIER="so-{r["id"]}" TYPE-REF="sot-req">', "          <VALUES>"]
        for ident, v in vals:
            L += [f"            <ATTRIBUTE-VALUE-STRING THE-VALUE={quoteattr(str(v))}>",
                  f"              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>{ident}</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>",
                  "            </ATTRIBUTE-VALUE-STRING>"]
        L += ["          </VALUES>", "        </SPEC-OBJECT>"]
    L += ["      </SPEC-OBJECTS>", "    </REQ-IF-CONTENT>", "  </CORE-CONTENT>", "</REQ-IF>", ""]
    return "\n".join(L)


def main(argv: list[str]) -> int:
    reqs = yaml.safe_load(SRC.read_text(encoding="utf-8"))["requirements"]
    text = render(reqs)
    leaks = [w for w in ("maintainer", "basis", "engineering_assumption", "answer key", "seeded") if w in text.lower()]
    if leaks:
        print(f"internal wording would reach the shown file: {leaks}")
        return 1
    if "--check" in argv:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != text:
            print(f"stale: {OUT.relative_to(ROOT)} (run tools/build_kit.py)")
            return 1
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(reqs)} requirements")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
