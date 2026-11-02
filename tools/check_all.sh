#!/bin/sh
# Run every product-spec checker; non-zero if any fails.
set -e
cd "$(dirname "$0")/.."
python3 tools/check_spec.py product/stakeholder_requirements.yaml
python3 tools/check_hara.py product/hara.yaml product/stakeholder_requirements.yaml
python3 tools/check_fsc.py product/functional_safety_concept.yaml product/hara.yaml
python3 tools/check_sys.py product/system_requirements.yaml product/stakeholder_requirements.yaml product/functional_safety_concept.yaml
