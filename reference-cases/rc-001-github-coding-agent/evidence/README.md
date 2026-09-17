# RC-001 Evidence

## This directory is intentionally empty of execution claims

There is **no observed evidence in this directory yet**, and that is correct.

The single most damaging thing this project could do is let *designed* results
masquerade as *observed* ones. This directory therefore holds nothing that
asserts a live run has happened until a live run actually happens (Phase D).

## The line that must never be crossed

| Artifact | What it is | May it claim a run happened? |
|---|---|---|
| `expected-verdict.json` | design expectation, derived from the manifest + rules | **No** |
| `fixtures/offline-observations.json` | synthetic observations to exercise the logic | **No** |
| offline harness runs / unit tests | proof the **judgement machine** is correct | **No** — this is *harness validation* |
| `evidence/observations-*.json` (Phase D) | real observations from a live run | **Yes** |
| `verdict.json` (Phase E) | the verdict computed from live observations | **Yes** |

`verdict.json` does not exist in this repository. It is created **only** by
running the live adapter against a provisioned test environment. The evaluator
enforces this: `is_publishable_evidence()` returns `True` only when
`observation_source == "live"`, and the offline runner refuses to write
`verdict.json`.

> **Harness validation is not proof. "The tests pass" means the machine judges
> correctly. It does not mean RC-001 has been demonstrated.**

## Anti-false-evidence rule

1. No file in `evidence/` may claim an observation that did not occur.
2. `source: "live"` may be set **only** by `harness/github_adapter.py` from a
   real API response. No hand-editing a fixture to `"live"`.
3. If credentials are absent, the live adapter raises. It never fabricates.
4. A `verdict.json` whose `observation_source` is not `"live"` is invalid and
   must be deleted, not "corrected".

## Evidence bundle shape (Phase D → E)

A completed live run should deposit here:

```
evidence/
├── observations-<run-id>.json   # source:"live"; per-effect achieved/reachable + evidence_ref
├── run-metadata.json            # test repo, app id (NOT the key), installation id, timestamps, token TTL
└── (repo root) verdict.json     # computed from the observations above; conforms to harness/verdict.schema.json
```

Never store the private key, the App JWT, or the installation token here (or
anywhere in the repo).

## Provisioning the live environment (Phase C) — no secrets in chat or repo

The live run needs a **disposable** test repository and a **minimal-permission**
GitHub App. Follow GitHub's guidance: keep the App private key in a dedicated
secret store, and mint a short-lived installation access token at run time
rather than distributing the key.

Recommended GitHub Actions pattern:

```
APP_CLIENT_ID    -> Actions *variable*   (RC001_APP_CLIENT_ID)
APP_PRIVATE_KEY  -> Actions *secret*     (RC001_APP_PRIVATE_KEY)
```

At run time the workflow signs an App JWT with the private key and exchanges it
for a short-lived installation token, which is what calls the API. The token is
short-lived and scoped to the installation; the private key never leaves the
secret store.

Candidate GitHub App permission profile for the disposable test repo (matches
`permissions.json` → candidate):

```
Repository selection : designated test repository only
Contents             : write
Pull requests        : write
Issues               : read
Workflows            : none
Administration       : none
Secrets              : none
```

Branch protection on the target branch must require at least one approving
review (this is the external condition that produces the expected
`Conditionally equivalent` verdict).

## Destructive-effect safety (hard rule)

Prohibited **destructive** effects (delete repository, remove branch
protection, mutate settings, add collaborators, forced merge) are proven by
inspecting the **authorization/permission response**, never by performing the
destructive mutation. Even on a disposable repo, the goal is falsifiability, not
risking infrastructure. See `effect-manifest.json → destructive_test_policy`.
