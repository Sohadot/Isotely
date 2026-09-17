"""
Live runner for RC-001 (Phase D -> E).

Runs the live adapter against the provisioned disposable target repo, records
raw observations as evidence, evaluates them with the deterministic engine, and
writes verdict.json ONLY if the result is live-sourced.

    python harness/run_live.py

Requires the provisioned environment (see PROVISIONING.md). Without credentials
the live adapter raises and nothing is written — the harness never fabricates
evidence.

Writes:
    evidence/observations-<run-id>.json   (raw, source:"live")
    verdict.json                          (case root; only if publishable)
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import evaluator          # noqa: E402
import github_adapter     # noqa: E402


def main() -> int:
    manifest = evaluator.load_json(os.path.join(CASE, "effect-manifest.json"))
    permissions = evaluator.load_json(os.path.join(CASE, "permissions.json"))

    obs = github_adapter.collect_live_observations(manifest)  # raises if no creds

    run_id = obs.get("run_id", "run")
    ev_dir = os.path.join(CASE, "evidence")
    os.makedirs(ev_dir, exist_ok=True)
    obs_path = os.path.join(ev_dir, f"observations-{run_id}.json")
    with open(obs_path, "w", encoding="utf-8") as fh:
        json.dump(obs, fh, indent=2)
    print(f"raw observations written: {obs_path}")

    result = evaluator.evaluate(manifest, permissions, obs)

    if not evaluator.is_publishable_evidence(result):
        print("REFUSING to write verdict.json: result is not live-sourced "
              f"(observation_source={result.observation_source}).", file=sys.stderr)
        return 3

    verdict_path = os.path.join(CASE, "verdict.json")
    payload = result.to_dict()
    payload["run_id"] = run_id
    payload["test_repo"] = obs.get("test_repo")
    with open(verdict_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"verdict.json written: {verdict_path}")

    # success rule: Falsifier 3 resolved, not "highest verdict class"
    falsifier3_resolved = (
        result.permission_equality is False
        and result.required.get("passed") == result.required.get("total")
        and result.prohibited.get("reachable") == 0
    )
    print("-" * 60)
    print(f"verdict                : {result.verdict}")
    print(f"permission_equality    : {result.permission_equality}")
    print(f"required passed        : {result.required.get('passed')}/{result.required.get('total')}")
    print(f"prohibited reachable   : {result.prohibited.get('reachable')}/{result.prohibited.get('total')}")
    print(f"Falsifier 3 resolved   : {falsifier3_resolved}")
    if not falsifier3_resolved:
        print("NOTE: Falsifier 3 not resolved by this run; RC-001 remains undischarged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
