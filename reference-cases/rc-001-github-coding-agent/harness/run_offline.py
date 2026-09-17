"""
Offline harness runner for RC-001.

Runs the deterministic evaluator over the fixture observations and prints the
resulting verdict. This validates that the JUDGEMENT MACHINE is correct.

It is NOT a proof of RC-001. It cannot write verdict.json. The output is
labelled 'HARNESS VALIDATION', and is_publishable_evidence() is False for every
fixture result by construction.

    python harness/run_offline.py
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import evaluator  # noqa: E402
import fixture_adapter  # noqa: E402


def main() -> int:
    manifest = evaluator.load_json(os.path.join(CASE, "effect-manifest.json"))
    permissions = evaluator.load_json(os.path.join(CASE, "permissions.json"))
    observations = fixture_adapter.load_observations(
        os.path.join(CASE, "fixtures", "offline-observations.json")
    )

    result = evaluator.evaluate(manifest, permissions, observations)

    print("=" * 68)
    print("RC-001 HARNESS VALIDATION  (offline; fixture observations)")
    print("This is NOT proof of RC-001. No verdict.json is written.")
    print("=" * 68)
    print(json.dumps(result.to_dict(), indent=2))
    print("-" * 68)
    print(f"observation_source     : {result.observation_source}")
    print(f"publishable as evidence: {evaluator.is_publishable_evidence(result)}")
    print(f"verdict (design-only)  : {result.verdict}")

    if evaluator.is_publishable_evidence(result):
        print("ERROR: a fixture run must never be publishable evidence.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
