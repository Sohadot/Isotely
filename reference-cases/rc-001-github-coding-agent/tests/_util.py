"""Shared test helpers: load the real manifest/permissions and build observation
sets programmatically so every verdict path can be exercised."""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
HARNESS = os.path.join(CASE, "harness")
sys.path.insert(0, HARNESS)

import evaluator  # noqa: E402  (re-exported for tests)
import fixture_adapter  # noqa: E402


def manifest():
    return evaluator.load_json(os.path.join(CASE, "effect-manifest.json"))


def permissions():
    return evaluator.load_json(os.path.join(CASE, "permissions.json"))


def all_required_passing(m):
    return [
        {"effect_id": e["id"], "kind": "required", "achieved": True}
        for e in m["required_effects"]
    ]


def all_prohibited_blocked(m):
    out = []
    for e in m["prohibited_effects"]:
        out.append({
            "effect_id": e["id"],
            "kind": "prohibited",
            "reachable": False,
            "blocked_by": e.get("enforced_by"),
        })
    return out


def obs(observations):
    return fixture_adapter.make_observations(observations)
