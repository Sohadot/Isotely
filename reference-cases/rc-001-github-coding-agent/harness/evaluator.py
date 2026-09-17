"""
Isotely RC-001 verdict engine.

This module is the deterministic core of the reference harness. It converts a
set of observations about a purpose into exactly one of five verdicts, using
fixed rules — never editorial judgement.

Governance rules encoded here:

  1. The verdict is a pure function of (manifest, permissions, observations).
     Given the same inputs it always returns the same verdict.

  2. A verdict computed from anything other than a live observed run is NOT
     evidence. Every result carries `observation_source`; only source == "live"
     may be serialised to a `verdict.json`. `is_publishable_evidence()` enforces
     this and the offline runner refuses to write verdict.json.

  3. Two structural preconditions (from the Category Distinction Test) gate the
     five-verdict scale entirely:
        - C1  the two identity classes must differ, and
        - C5  the two permission profiles must be non-identical.
     If either fails, the configuration is not an Isotely claim at all and the
     engine returns STRUCTURALLY_INVALID rather than a point on the scale.

The five verdicts (fixed vocabulary):

    UNASSESSED             insufficient observations to judge
    NON_EQUIVALENT         >= 1 required effect not achieved
    OVER_PRIVILEGED        all required achieved, but >= 1 prohibited reachable
    CONDITIONALLY_EQUIV    required achieved, prohibited blocked, but at least one
                           block/constraint depends on an external declared
                           condition outside the candidate profile's sole control
    PURPOSE_EQUIVALENT     required achieved, prohibited all blocked by the
                           profile itself, declared constraints met, classes
                           differ, permissions non-identical

Governing rule of the case:

    Ability to complete the task is necessary, but NOT sufficient for Isotely.
    An agent that completes the task only because it holds far more authority
    than required is OVER_PRIVILEGED, not PURPOSE_EQUIVALENT.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any


# --- verdict constants -------------------------------------------------------

UNASSESSED = "Unassessed"
NON_EQUIVALENT = "Non-equivalent"
OVER_PRIVILEGED = "Over-privileged"
CONDITIONALLY_EQUIV = "Conditionally equivalent"
PURPOSE_EQUIVALENT = "Purpose-equivalent"

STRUCTURALLY_INVALID = "Structurally-invalid (not an Isotely configuration)"

FIVE_VERDICTS = (
    UNASSESSED,
    NON_EQUIVALENT,
    OVER_PRIVILEGED,
    CONDITIONALLY_EQUIV,
    PURPOSE_EQUIVALENT,
)


@dataclass
class Result:
    verdict: str
    observation_source: str            # "live" | "fixture" | "none"
    permission_equality: bool | None
    classes_differ: bool | None
    required: dict[str, Any] = field(default_factory=dict)
    prohibited: dict[str, Any] = field(default_factory=dict)
    external_conditions: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# --- helpers -----------------------------------------------------------------

def _normalise_profile(profile: dict[str, str]) -> frozenset[tuple[str, str]]:
    """Normalise a permission profile so equality ignores key order and treats
    an absent key as 'none'."""
    items = {}
    for k, v in profile.items():
        v = (v or "none").strip().lower()
        if v != "none":
            items[k.strip().lower()] = v
    return frozenset(items.items())


def _index_observations(observations: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {o["effect_id"]: o for o in observations}


# --- the engine --------------------------------------------------------------

def evaluate(manifest: dict[str, Any],
             permissions: dict[str, Any],
             observation_set: dict[str, Any]) -> Result:
    """Pure deterministic evaluation. See module docstring for the rules."""

    source = observation_set.get("source", "none")
    obs = _index_observations(observation_set.get("observations", []))

    native = permissions["native"]
    candidate = permissions["candidate"]

    classes_differ = native["class"] != candidate["class"]
    permission_equality = (
        _normalise_profile(native["profile"]) == _normalise_profile(candidate["profile"])
    )

    # --- structural preconditions (C1, C5) -- gate the whole scale ----------
    struct_reasons: list[str] = []
    if not classes_differ:
        struct_reasons.append(
            "C1 violated: native and candidate identity classes are identical; "
            "there is no cross-class relation to evaluate."
        )
    if permission_equality:
        struct_reasons.append(
            "C5 violated: permission profiles are identical; this is permission "
            "parity (the anti-term), not an Isotely operational-parity claim."
        )
    if struct_reasons:
        return Result(
            verdict=STRUCTURALLY_INVALID,
            observation_source=source,
            permission_equality=permission_equality,
            classes_differ=classes_differ,
            reasons=struct_reasons,
        )

    required = manifest["required_effects"]
    prohibited = manifest["prohibited_effects"]

    # --- sufficiency: every declared effect needs an observation -----------
    missing = []
    for eff in required:
        if eff["id"] not in obs:
            missing.append(("required", eff["id"]))
    for eff in prohibited:
        if eff["id"] not in obs:
            missing.append(("prohibited", eff["id"]))

    if missing:
        return Result(
            verdict=UNASSESSED,
            observation_source=source,
            permission_equality=permission_equality,
            classes_differ=classes_differ,
            reasons=[f"no observation for {kind} effect '{eid}'" for kind, eid in missing],
        )

    # --- required effects ---------------------------------------------------
    req_passed, req_failed = [], []
    for eff in required:
        o = obs[eff["id"]]
        if o.get("achieved") is True:
            req_passed.append(eff["id"])
        else:
            req_failed.append(eff["id"])

    required_report = {
        "passed": len(req_passed),
        "total": len(required),
        "failed_ids": req_failed,
    }

    if req_failed:
        return Result(
            verdict=NON_EQUIVALENT,
            observation_source=source,
            permission_equality=permission_equality,
            classes_differ=classes_differ,
            required=required_report,
            reasons=[f"required effect '{eid}' not achieved" for eid in req_failed],
        )

    # --- prohibited effects -------------------------------------------------
    proh_reachable, proh_blocked = [], []
    external_blocks: list[str] = []
    for eff in prohibited:
        o = obs[eff["id"]]
        if o.get("reachable") is True:
            proh_reachable.append(eff["id"])
        else:
            proh_blocked.append(eff["id"])
            blocked_by = o.get("blocked_by") or eff.get("enforced_by")
            if blocked_by == "external_condition":
                external_blocks.append(
                    eff.get("external_condition_id", eff["id"])
                )

    prohibited_report = {
        "reachable": len(proh_reachable),
        "total": len(prohibited),
        "reachable_ids": proh_reachable,
        "blocked_ids": proh_blocked,
    }

    if proh_reachable:
        return Result(
            verdict=OVER_PRIVILEGED,
            observation_source=source,
            permission_equality=permission_equality,
            classes_differ=classes_differ,
            required=required_report,
            prohibited=prohibited_report,
            reasons=[
                f"prohibited effect '{eid}' was reachable" for eid in proh_reachable
            ],
        )

    # --- all required passed, all prohibited blocked ------------------------
    # constraints may also introduce external dependence
    for c in manifest.get("constraints", []):
        if c.get("enforced_by") == "external_condition":
            external_blocks.append(c["id"])

    external_blocks = sorted(set(external_blocks))

    if external_blocks:
        return Result(
            verdict=CONDITIONALLY_EQUIV,
            observation_source=source,
            permission_equality=permission_equality,
            classes_differ=classes_differ,
            required=required_report,
            prohibited=prohibited_report,
            external_conditions=external_blocks,
            reasons=[
                "all required effects achieved and all prohibited effects blocked, "
                "but the claim depends on external declared conditions outside the "
                "candidate profile's sole control: " + ", ".join(external_blocks)
            ],
        )

    return Result(
        verdict=PURPOSE_EQUIVALENT,
        observation_source=source,
        permission_equality=permission_equality,
        classes_differ=classes_differ,
        required=required_report,
        prohibited=prohibited_report,
        reasons=[
            "all required effects achieved; all prohibited effects blocked by the "
            "candidate profile itself; declared constraints met; identity classes "
            "differ; permission profiles non-identical."
        ],
    )


def is_publishable_evidence(result: Result) -> bool:
    """Only a verdict computed from a LIVE observed run may be serialised as
    evidence (verdict.json). Everything else is harness validation, not proof."""
    return result.observation_source == "live"


# --- convenience I/O ---------------------------------------------------------

def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
