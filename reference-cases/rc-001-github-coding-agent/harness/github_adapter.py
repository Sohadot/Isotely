"""
Live GitHub adapter for RC-001.

This adapter turns the effect manifest into real observations against a live,
DISPOSABLE test repository, using a short-lived GitHub App installation token.
It is the ONLY component allowed to produce observations tagged source == "live",
and therefore the only component whose output may become evidence.

It is written to be run, but it is NOT run during harness construction or
offline validation, because it requires credentials that intentionally never
enter this repository or any chat:

    RC001_APP_CLIENT_ID     GitHub App client id           (Actions *variable*)
    RC001_APP_PRIVATE_KEY   GitHub App private key (PEM)    (Actions *secret*)
    RC001_INSTALLATION_ID   installation id on the test repo
    RC001_TEST_REPO         "owner/repo" of the disposable test repository

Credential handling (per GitHub guidance):
  * The private key lives only in a dedicated secret store / Actions secret.
  * At run time the workflow mints a SHORT-LIVED installation access token from
    the App JWT; that token — not the private key — is what talks to the API.
  * Nothing is written back to the repo, logged, or shared.

Two hard safety rules are enforced below:

  SAFETY RULE 1 — no forged evidence.
    Without live credentials this module raises. It will never fabricate a
    "live" observation set. Fabricating observations is the single most
    damaging thing this project could do; the code makes it impossible here.

  SAFETY RULE 2 — no destructive proof-by-destruction.
    Prohibited destructive effects (delete repo, remove branch protection,
    mutate settings, add collaborators, forced merge) are proven by inspecting
    the AUTHORIZATION RESPONSE, never by performing the mutation. The manifest's
    destructive_test_policy is honoured: destructive endpoints are probed with
    authorization/permission checks only.

This file is deliberately dependency-light. The HTTP/JWT calls are sketched with
clear TODO markers where a maintainer wires in `PyJWT` + `requests` (or urllib)
at provisioning time (Phase C). Until then, importing it is safe; calling
`collect_live_observations()` without credentials raises.
"""

from __future__ import annotations

import os
from typing import Any


class MissingCredentials(RuntimeError):
    pass


REQUIRED_ENV = (
    "RC001_APP_CLIENT_ID",
    "RC001_APP_PRIVATE_KEY",
    "RC001_INSTALLATION_ID",
    "RC001_TEST_REPO",
)


def _require_credentials() -> dict[str, str]:
    missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
    if missing:
        raise MissingCredentials(
            "Live run refused. Missing: " + ", ".join(missing) + ". "
            "This adapter never fabricates live observations. Provision a "
            "disposable test repo and a minimal-permission GitHub App first "
            "(see evidence/README.md, Phase C)."
        )
    return {k: os.environ[k] for k in REQUIRED_ENV}


def _mint_installation_token(client_id: str, private_key_pem: str,
                             installation_id: str) -> str:
    """Mint a short-lived installation access token.

    TODO(phase-c): build an App JWT signed with the private key (RS256, ~10 min
    expiry), then POST /app/installations/{installation_id}/access_tokens to
    exchange it for a short-lived installation token. Return the token only;
    never return or log the private key or the JWT.
    """
    raise NotImplementedError(
        "Token minting is wired at provisioning time (Phase C). "
        "Do not stub this to return a fake token."
    )


def _probe_required(token: str, repo: str, effect: dict[str, Any]) -> dict[str, Any]:
    """Attempt a required effect on the disposable repo and observe the result.

    TODO(phase-c): perform the real, NON-destructive API call for this required
    effect (read contents, create task branch, modify allowed file, commit, open
    PR) and set achieved=True/False from the API response. Attach an evidence_ref
    (request id / response digest) for the evidence bundle.
    """
    raise NotImplementedError


def _probe_prohibited(token: str, repo: str, effect: dict[str, Any]) -> dict[str, Any]:
    """Determine whether a prohibited effect is reachable — SAFELY.

    For destructive effects the probe MUST be an authorization check, not a
    mutation:
      * inspect the installation's granted permissions, and/or
      * issue the request in a way that returns the authorization decision
        (e.g. a 403/insufficient-scope or 405 branch-protection rejection)
        WITHOUT completing a destructive change.

    TODO(phase-c): implement per manifest.destructive_test_policy. reachable=True
    only if the effect could actually be produced; reachable=False if the API
    authorization response denies it. Record blocked_by = "profile" or
    "external_condition" from the observed reason.
    """
    raise NotImplementedError


def collect_live_observations(manifest: dict[str, Any]) -> dict[str, Any]:
    """Produce a source=="live" observation set from the disposable test repo.

    Raises MissingCredentials if the environment is not provisioned. This is the
    only path that can yield publishable evidence.
    """
    creds = _require_credentials()
    token = _mint_installation_token(
        creds["RC001_APP_CLIENT_ID"],
        creds["RC001_APP_PRIVATE_KEY"],
        creds["RC001_INSTALLATION_ID"],
    )
    repo = creds["RC001_TEST_REPO"]

    observations: list[dict[str, Any]] = []
    for eff in manifest["required_effects"]:
        observations.append(_probe_required(token, repo, eff))
    for eff in manifest["prohibited_effects"]:
        observations.append(_probe_prohibited(token, repo, eff))

    return {
        "source": "live",
        "test_repo": repo,
        "observations": observations,
    }
