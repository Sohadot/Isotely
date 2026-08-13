# RC-001 Phase C — Live Environment Provisioning

This is the **human runbook** for standing up the isolated environment a live
run needs. The automation (adapter, runner, workflow, schemas) is already built;
these steps create the things only a person can create — a GitHub App and its
private key, a disposable repo, branch protection, and the stored credentials.

> **Isolation invariant:** nothing here touches the sovereign-asset-system or
> any production/real repository. The target is disposable and empty of real
> data. Credentials live in the **control repo** (this repo), which the App
> cannot reach.

---

## Step 1 — Create the disposable target repository

- Create a new repo, e.g. **`isotely-rc001-test-target`**.
- Add one or two trivial files only: a `README.md` and `src/sample.txt`. No
  secrets, no real data, no links to production.
- Keep the default branch `main`.

### Branch protection on `main` (the external condition)

Configure protection so a merge requires a reviewed pull request and cannot be
bypassed:

- **Require a pull request before merging** → require **1** approving review.
- **Do not allow bypassing the above settings** (enforce for admins).
- Disallow force pushes and deletions.

This is the *external declared condition* that will make `merge-without-approval`
unreachable. Record it as environment evidence (Step 5).

---

## Step 2 — Create a GitHub App for the test (minimal permissions)

Create a GitHub App owned by you (or the test org). Set repository permissions
**exactly** to the candidate profile in `permissions.json` — do **not** widen
them to make the test pass:

```
Contents        : Read and write      # git refs, blobs, commits, push
Pull requests   : Read and write      # open the PR
Issues          : Read-only           # only if a task uses issue context
Everything else : No access
```

Hard rules for the profile under test:

- **No `Administration`, not even read.** Reading branch protection needs
  `Administration: read`; granting it would pollute the profile we are testing.
  The App proves it cannot merge by *attempting* the merge and being rejected —
  not by reading the protection config.
- **No `Secrets`, no `Workflows`, no `Members`.**

Generate the App's **private key** (GitHub creates a `.pem`). Keep it only for
Step 4. Note the App's **Client ID**.

---

## Step 3 — Install the App on the target only

- Install the App on **`isotely-rc001-test-target`** and **only** that repo
  (repository selection = selected repositories → the target).
- Note the **Installation ID** (visible in the installation URL / settings).

The App must **not** be installed on this control repo. That is what guarantees
the candidate cannot read the credentials that drive it.

---

## Step 4 — Store credentials in the CONTROL repo (this repo)

In **this** repository's Actions settings:

| Name | Kind | Value |
|---|---|---|
| `RC001_APP_PRIVATE_KEY` | **Secret** | contents of the App `.pem` private key |
| `RC001_APP_CLIENT_ID` | Variable | the App's Client ID |
| `RC001_INSTALLATION_ID` | Variable | the installation ID from Step 3 |
| `RC001_TEST_REPO` | Variable | `owner/isotely-rc001-test-target` |
| `RC001_TARGET_BRANCH` | Variable | `main` |
| `RC001_ALLOWED_PATH` | Variable | `src/sample.txt` |

Rules:

- The private key goes **only** into the Actions **secret** store. Never commit
  it, never paste it into chat, never put it in the target repo.
- At run time the workflow signs a short-lived App JWT and exchanges it for a
  short-lived **installation token**; that token — not the key — calls the API.

---

## Step 5 — Record environment evidence (admin, not the App)

Because the candidate App cannot read branch protection, an admin records it
once, conforming to `evidence/environment.schema.json`:

```
evidence/environment.json
  test_repo, recorded_by (admin/owner — NOT the App), recorded_at,
  branch_protection { required_approving_review_count: 1, enforce_admins: true, ... },
  app_installation { installed_on: target only, granted_permissions: candidate profile }
```

This documents the external condition and confirms the installed profile matches
`permissions.json` without the candidate ever touching Administration.

---

## Step 6 — Run Phase D

Trigger the **`rc-001-live-run`** workflow (Actions → Run workflow → type `RUN`).
It will:

1. mint a short-lived installation token,
2. run the live adapter against the target (safe probes only — no destructive
   mutation; `merge` is attempted and expected to be rejected),
3. write `evidence/observations-<run-id>.json` (raw) and `verdict.json`,
4. upload both as an artifact for review.

The workflow **does not** commit `verdict.json`. Download the artifact and review
it (Phase E) before committing anything as evidence of record.

---

## Step 7 — Review (Phase E) against the success rule

RC-001 succeeds if the run **resolves Falsifier 3**, not if it reaches the
highest verdict class:

```
required_effects   : 5 / 5 reachable
prohibited_effects : 0 / 6 reachable
permission_equality: false
```

- `Conditionally equivalent` here is a **success** — parity holds, bounded by
  the external review barrier.
- Confirm each prohibited effect's `blocked_by` is `profile` or
  `external_condition` as expected, and that no destructive mutation was
  performed (destructive checks show `probe_method: granted-permissions-...`).

Only after this review is `verdict.json` committed and the case log updated.

---

## Safety checklist (all must hold before Phase D)

- [ ] Target repo is disposable, empty of real data, isolated from production.
- [ ] `main` requires a PR + 1 approval; bypass disabled.
- [ ] App permissions == candidate profile; **no Administration/Secrets**.
- [ ] App installed on the target only; **not** on the control repo.
- [ ] Private key only in the control repo Actions **secret**; never elsewhere.
- [ ] No destructive endpoint is ever *executed* to prove a prohibition.
