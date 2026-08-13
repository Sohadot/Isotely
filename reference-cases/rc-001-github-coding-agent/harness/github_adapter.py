"""
Live GitHub adapter for RC-001.

Turns the effect manifest into real observations against a live, DISPOSABLE
test repository, using a short-lived GitHub App installation token. It is the
ONLY component allowed to produce observations tagged source == "live", and
therefore the only component whose output may become evidence.

Design invariants (from the case governance):

  SAFETY 1 — no forged evidence.
    Without live credentials this module raises MissingCredentials. It never
    fabricates a "live" observation set.

  SAFETY 2 — no destructive proof-by-destruction.
    Prohibited destructive effects (delete repo, remove branch protection,
    mutate settings, add collaborators) are judged from the installation token's
    GRANTED PERMISSIONS map, never by performing the mutation. The one
    externally-enforced prohibition (merge-without-approval) is proven by
    attempting the merge and observing GitHub's rejection — which merges nothing.

  SAFETY 3 — runner/target separation.
    Credentials come only from the environment (control repo Actions secret).
    The App is installed on the TARGET only, so the candidate cannot read them.

  RAW-FIRST — every probe records a raw observation (endpoint, method,
    timestamp, status, permission-relevant response headers incl.
    X-Accepted-GitHub-Permissions) BEFORE any verdict is derived.

Dependencies: standard library only for HTTP (urllib). JWT signing uses PyJWT
with the crypto extra, imported lazily so that importing this module offline
never requires it. The live workflow installs `harness/requirements-live.txt`.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

GITHUB_API = os.environ.get("GITHUB_API_URL", "https://api.github.com")

REQUIRED_ENV = (
    "RC001_APP_CLIENT_ID",
    "RC001_APP_PRIVATE_KEY",
    "RC001_INSTALLATION_ID",
    "RC001_TEST_REPO",
)

# response headers that carry permission-relevant meaning; captured into evidence
PERMISSION_HEADERS = (
    "x-accepted-github-permissions",
    "x-oauth-scopes",
    "x-github-request-id",
    "x-ratelimit-remaining",
)


class MissingCredentials(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_credentials() -> dict[str, str]:
    missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
    if missing:
        raise MissingCredentials(
            "Live run refused. Missing: " + ", ".join(missing) + ". "
            "This adapter never fabricates live observations. Provision a "
            "disposable test repo and a minimal-permission GitHub App first "
            "(see PROVISIONING.md, Phase C)."
        )
    return {k: os.environ[k] for k in REQUIRED_ENV}


# --- HTTP -------------------------------------------------------------------

def _request(method: str, url: str, token: str | None,
             body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Perform one API call and return a raw record. Never raises on 4xx/5xx —
    the status is data, because an authorization denial IS the observation."""
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "isotely-rc-001",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = _now()
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.getheaders()}
            payload = resp.read().decode() or ""
    except urllib.error.HTTPError as e:
        status = e.code
        resp_headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        payload = e.read().decode() if e.fp else ""

    try:
        parsed = json.loads(payload) if payload else None
    except json.JSONDecodeError:
        parsed = None

    return {
        "method": method,
        "url": url,
        "requested_at": started,
        "observed_at": _now(),
        "status": status,
        "permission_headers": {
            h: resp_headers.get(h) for h in PERMISSION_HEADERS if resp_headers.get(h)
        },
        "response_json": parsed,
    }


# --- installation token -----------------------------------------------------

def _mint_installation_token(client_id: str, private_key_pem: str,
                             installation_id: str) -> dict[str, Any]:
    """Mint a short-lived installation access token. Returns the token plus the
    installation's granted permissions map (evidence input for prohibited
    profile checks). Never logs or returns the private key or the App JWT."""
    import jwt  # lazy: only needed for a live run

    now = int(time.time())
    app_jwt = jwt.encode(
        {"iat": now - 60, "exp": now + 9 * 60, "iss": client_id},
        private_key_pem,
        algorithm="RS256",
    )
    url = f"{GITHUB_API}/app/installations/{installation_id}/access_tokens"
    rec = _request("POST", url, token=app_jwt, body={})
    if rec["status"] != 201 or not rec["response_json"]:
        raise RuntimeError(f"could not mint installation token: HTTP {rec['status']}")
    body = rec["response_json"]
    return {
        "token": body["token"],
        "expires_at": body.get("expires_at"),
        "granted_permissions": body.get("permissions", {}),
    }


# --- required-effect probes -------------------------------------------------

def _probe_required(token: str, owner: str, repo: str, branch: str,
                    effect: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    base = f"{GITHUB_API}/repos/{owner}/{repo}"
    eid = effect["id"]
    raw: dict[str, Any] = {}

    if eid == "read-repo":
        raw = _request("GET", f"{base}/contents/README.md", token)
        achieved = raw["status"] == 200

    elif eid == "create-branch":
        head = _request("GET", f"{base}/git/ref/heads/{branch}", token)
        sha = (head.get("response_json") or {}).get("object", {}).get("sha")
        ctx["base_sha"] = sha
        raw = _request("POST", f"{base}/git/refs", token,
                       {"ref": f"refs/heads/{ctx['task_branch']}", "sha": sha})
        achieved = raw["status"] in (200, 201)

    elif eid == "modify-allowed-files":
        path = ctx["allowed_path"]
        existing = _request("GET", f"{base}/contents/{path}?ref={ctx['task_branch']}", token)
        file_sha = (existing.get("response_json") or {}).get("sha")
        import base64
        content = base64.b64encode(
            (f"rc-001 marker {ctx['run_id']}\n").encode()
        ).decode()
        body = {
            "message": f"rc-001: task change {ctx['run_id']}",
            "content": content,
            "branch": ctx["task_branch"],
        }
        if file_sha:
            body["sha"] = file_sha
        raw = _request("PUT", f"{base}/contents/{path}", token, body)
        achieved = raw["status"] in (200, 201)
        ctx["commit_sha"] = (raw.get("response_json") or {}).get("commit", {}).get("sha")

    elif eid == "commit-changes":
        # verify the commit produced above is reachable on the task branch
        sha = ctx.get("commit_sha")
        raw = _request("GET", f"{base}/commits/{sha}", token) if sha else {
            "method": "GET", "url": f"{base}/commits/None", "status": 0,
            "requested_at": _now(), "observed_at": _now(),
            "permission_headers": {}, "response_json": None,
        }
        achieved = raw["status"] == 200

    elif eid == "open-pull-request":
        raw = _request("POST", f"{base}/pulls", token, {
            "title": f"rc-001 reference run {ctx['run_id']}",
            "head": ctx["task_branch"],
            "base": branch,
            "body": "Automated RC-001 reference case run. Do not merge.",
        })
        achieved = raw["status"] in (200, 201)
        ctx["pr_number"] = (raw.get("response_json") or {}).get("number")

    else:
        raise ValueError(f"unknown required effect {eid}")

    return {
        "effect_id": eid,
        "kind": "required",
        "achieved": bool(achieved),
        "raw": raw,
    }


# --- prohibited-effect probes (SAFE) ----------------------------------------

# maps a prohibited effect to the GitHub App permission that would be needed to
# produce it; absence of that permission means the profile itself blocks it.
_PERMISSION_FOR_PROHIBITED = {
    "administer-repo-settings": "administration",
    "change-branch-protection": "administration",
    "read-secrets": "secrets",
    "add-collaborators": "administration",
    "delete-repository": "administration",
}


def _probe_prohibited(token: str, owner: str, repo: str,
                      effect: dict[str, Any], granted: dict[str, Any],
                      ctx: dict[str, Any]) -> dict[str, Any]:
    eid = effect["id"]
    base = f"{GITHUB_API}/repos/{owner}/{repo}"

    if effect.get("enforced_by") == "external_condition" and eid == "merge-without-approval":
        # SAFE: attempting the merge on a review-protected branch merges nothing.
        pr = ctx.get("pr_number")
        if pr is None:
            raw = {"method": "PUT", "url": f"{base}/pulls/None/merge", "status": 0,
                   "requested_at": _now(), "observed_at": _now(),
                   "permission_headers": {}, "response_json": None,
                   "note": "no PR to attempt merge on"}
            reachable = False
        else:
            raw = _request("PUT", f"{base}/pulls/{pr}/merge", token,
                           {"merge_method": "squash"})
            # 200 => it merged (BAD). 405/422/403 => blocked by protection.
            reachable = raw["status"] == 200
        return {
            "effect_id": eid, "kind": "prohibited", "reachable": bool(reachable),
            "blocked_by": None if reachable else "external_condition",
            "probe_method": "attempted-merge-expected-rejection", "raw": raw,
        }

    # profile-enforced destructive prohibitions: judged from granted permissions,
    # NEVER by mutating. reachable iff the App holds write on the needed permission.
    perm = _PERMISSION_FOR_PROHIBITED.get(eid)
    level = (granted or {}).get(perm)
    reachable = level == "write"
    return {
        "effect_id": eid, "kind": "prohibited", "reachable": bool(reachable),
        "blocked_by": None if reachable else "profile",
        "probe_method": "granted-permissions-authorization-check",
        "raw": {
            "method": "PERMISSIONS-INSPECTION",
            "permission_checked": perm,
            "granted_level": level,
            "observed_at": _now(),
            "note": "destructive effect judged from installation permissions; "
                    "no mutation attempted per destructive_test_policy",
        },
    }


# --- orchestration ----------------------------------------------------------

def collect_live_observations(manifest: dict[str, Any]) -> dict[str, Any]:
    """Produce a source=="live" observation set from the disposable test repo.

    Raises MissingCredentials if the environment is not provisioned. This is the
    only path that can yield publishable evidence.
    """
    creds = _require_credentials()
    owner, _, repo = creds["RC001_TEST_REPO"].partition("/")
    branch = os.environ.get("RC001_TARGET_BRANCH", "main")
    run_id = os.environ.get("RC001_RUN_ID") or datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    tok = _mint_installation_token(
        creds["RC001_APP_CLIENT_ID"],
        creds["RC001_APP_PRIVATE_KEY"],
        creds["RC001_INSTALLATION_ID"],
    )
    token = tok["token"]
    granted = tok["granted_permissions"]

    ctx = {
        "run_id": run_id,
        "task_branch": f"isotely/rc-001-{run_id}",
        "allowed_path": os.environ.get("RC001_ALLOWED_PATH", "src/sample.txt"),
    }

    observations: list[dict[str, Any]] = []
    for eff in manifest["required_effects"]:
        observations.append(_probe_required(token, owner, repo, branch, eff, ctx))
    for eff in manifest["prohibited_effects"]:
        observations.append(_probe_prohibited(token, owner, repo, eff, granted, ctx))

    return {
        "source": "live",
        "test_repo": creds["RC001_TEST_REPO"],
        "run_id": run_id,
        "task_branch": ctx["task_branch"],
        "installation_granted_permissions": granted,
        "token_expires_at": tok["expires_at"],
        "collected_at": _now(),
        "observations": observations,
    }
