"""
Fixture adapter for RC-001.

Loads offline observations from a JSON file and returns them tagged with
source == "fixture". Its only job is to feed the evaluator synthetic
observations so the verdict logic itself can be validated WITHOUT any network
access and WITHOUT any GitHub credentials.

Governance boundary: observations produced by this adapter can never become
evidence. They are always tagged "fixture", and evaluator.is_publishable_evidence()
returns False for them. Running the evaluator over fixtures validates the
harness; it does NOT prove RC-001.
"""

from __future__ import annotations

import json
from typing import Any


def load_observations(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # force the source tag: fixtures are never evidence, whatever the file says
    data["source"] = "fixture"
    return data


def make_observations(observations: list[dict[str, Any]]) -> dict[str, Any]:
    """Build an in-memory fixture observation set (used by tests)."""
    return {"source": "fixture", "observations": observations}
