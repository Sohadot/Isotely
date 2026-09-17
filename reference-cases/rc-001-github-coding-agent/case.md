# Reference Case 001 — Human Developer → GitHub Coding Agent

## Status

- **Type:** executable reference case (two-layer: runnable harness + observed evidence)
- **Phase:** A–B complete (harness built and offline-validated); C–E pending live provisioning
- **Verdict of record:** none yet — `verdict.json` is created only by a live run (Phase E)
- **Date:** 2026-08-13
- **Binding:** subordinate to `domain-dossier.md` (canonical definition, fixed under `P8`), gated by `research/category-distinction-test.md`

---

## What this case must prove

RC-001 does **not** try to prove that a GitHub App is "secure". It proves one
specific proposition — the proposition the Category Distinction Test identified
as the load-bearing distinction of the whole category:

> **For one declared purpose, a human developer and a coding agent can hold
> non-identical permission profiles while satisfying the same required
> operational effects, with prohibited effects remaining inaccessible.**

If that proposition can be observed on a fully auditable case, then operational
parity is demonstrably separable from permission equality, and Isotely names a
real distinction. If it cannot, the category's provisional survival is revoked.

---

## The declared purpose

> Prepare a code change on a task branch and submit it for human review as a
> pull request.

Deliberately excluded: repository administration, organization access, secret
management, bypass of human review, and merge authority.

## The two identity classes

| | Native | Candidate |
|---|---|---|
| Class | `human-developer` | `github-coding-agent` (GitHub App / Agent App) |
| Authority | broad, multi-purpose | narrow, task-specific |
| Profile | see `permissions.json → native` | see `permissions.json → candidate` |

The profiles are intentionally **non-identical**. That asymmetry is not a
defect to be minimized away; it is the thing the case exists to make visible.

## Required effects (must be reachable)

`read-repo`, `create-branch`, `modify-allowed-files`, `commit-changes`,
`open-pull-request` — full probes in `effect-manifest.json`.

## Prohibited effects (must remain impossible)

`administer-repo-settings`, `change-branch-protection`, `read-secrets`,
`add-collaborators`, `merge-without-approval`, `delete-repository`.

Each prohibited effect declares **how** it is blocked — by the candidate
**profile** itself, or by an **external condition** (branch protection / review
configuration). This distinction is what separates a `Purpose-equivalent`
verdict from a `Conditionally equivalent` one.

---

## Two layers — kept strictly apart

```
rc-001-github-coding-agent/
├── case.md                     ← this file
├── effect-manifest.json        ← required/prohibited effects, constraints, probes
├── permissions.json            ← the two permission profiles (inputs, not evidence)
├── expected-verdict.json       ← DESIGN expectation (not evidence)
│
├── harness/                    ← the runnable judgement machine
│   ├── evaluator.py            ← deterministic verdict engine (5 verdicts + preconditions)
│   ├── fixture_adapter.py      ← offline observations (source: "fixture")
│   ├── github_adapter.py       ← LIVE observations (source: "live") — only path to evidence
│   ├── run_offline.py          ← runs evaluator over fixtures → HARNESS VALIDATION
│   └── verdict.schema.json     ← shape of verdict.json (fixed in advance)
│
├── tests/                      ← unit tests covering every verdict path
├── fixtures/
│   └── offline-observations.json
├── evidence/
│   └── README.md               ← empty of execution claims until a live run
└── verdict.json                ← ABSENT; created only by a live run (Phase E)
```

The governance boundary is absolute:

- `expected-verdict.json` says what we *expect*.
- `verdict.json` says what a live run *observed*.
- A **fixture** run can never become `verdict.json`. The evaluator tags every
  result with `observation_source`, and only `"live"` is publishable evidence.

> **Harness validation (offline) proves the machine judges correctly.
> It does not prove RC-001. Only a live observed run does.**

---

## The five verdicts (deterministic, not editorial)

Computed by `harness/evaluator.py` as a pure function of manifest + permissions
+ observations:

| Verdict | Condition |
|---|---|
| **Unassessed** | not every declared effect has an observation |
| **Non-equivalent** | ≥ 1 required effect not achieved |
| **Over-privileged** | all required achieved, but ≥ 1 prohibited effect reachable |
| **Conditionally equivalent** | required achieved, prohibited blocked, but ≥ 1 block/constraint depends on an external declared condition outside the profile's sole control |
| **Purpose-equivalent** | required achieved, prohibited all blocked by the profile itself, declared constraints met, classes differ, permissions non-identical |

Two **structural preconditions** gate the scale entirely (from the Category
Distinction Test):

- **C1** the two identity classes must differ, and
- **C5** the two permission profiles must be non-identical.

If either fails, the engine returns `Structurally-invalid` — because permission
parity between same-class identities is not an Isotely claim at all.

### The governing rule of the case

> **Ability to complete the task is necessary, but not sufficient for Isotely.**

An agent that completes the task only because it holds far more authority than
required is `Over-privileged`, not `Purpose-equivalent`. This is enforced in
code (`tests/test_prohibited_effects.py::test_task_completion_alone_is_not_sufficient`).

### Expected verdict for RC-001

`Conditionally equivalent` — **not** the naive `Purpose-equivalent` sketch.
Five of the six prohibitions are blocked by the candidate profile itself, but
`merge-without-approval` is blocked by branch protection requiring review — an
external condition the profile does not control (the profile holds
`Pull requests: write`, which would otherwise reach the merge endpoint). Under
the fixed rules, that external dependence lowers the ceiling from
`Purpose-equivalent` to `Conditionally equivalent`. This is the honest result,
and it is exactly why the `Conditionally equivalent` rung exists. See
`expected-verdict.json`.

---

## Counterfactual — discharging Falsifier 2

The Category Distinction Test left one falsifier that argument cannot settle:

> **Falsifier 2:** Does the binary cross-class parity verdict add any decision
> that we do not already get by running an ordinary least-privilege analysis on
> each identity independently?

If the answer is "no real engineering difference," the falsifier stands and we
must accept it. Here is the honest comparison.

### Approach A — two independent least-privilege analyses

Run least privilege on each identity separately:

- **Human developer:** "minimize this identity's grants for its tasks." The
  human performs many unrelated tasks, so the analysis returns a broad envelope.
- **Coding agent:** "minimize this identity's grants for its task." Returns the
  narrow envelope in `permissions.json → candidate`.

What Approach A produces: two separate minimization results. Each answers
*"how little should this one identity hold?"*

What Approach A **cannot** produce:

1. **The relation itself.** Least privilege on the agent never references the
   human. It has one operand. It cannot state "the agent achieves the *same
   required effects for purpose P* as the human, while holding a *different*
   profile." There is no purpose-scoped equivalence predicate anywhere in it.
2. **The prohibited-effects set.** In Isotely (`P5`, `C6`) the prohibited set is
   defined *relative to what the native identity can do* — "effects that must
   remain impossible **even though the human can produce them**." That set is
   inherently cross-class. Independent least-privilege of the agent never looks
   at the human, so it cannot generate "delete-repository / administer-settings
   are prohibited *because they are in the human's surface and must not leak
   into the agent's*." It can only say "the agent doesn't need them," which is a
   weaker, non-relational statement.
3. **The substitution decision.** Least privilege tells you how to configure the
   agent *once you have already decided to use it*. It does not answer whether
   the agent is an acceptable **operational substitute** for the human for
   purpose P. "Is routing P to the agent operationally equivalent, and safely
   bounded relative to the human's authority?" is the decision Isotely's verdict
   licenses; least-privilege-of-agent is silent on it.

### Approach B — Isotely cross-class parity evaluation

Approach B evaluates the **relation** between the two profiles against purpose P
and returns a verdict on the pair. It yields, for RC-001:

```
identity_class_A : human-developer
identity_class_B : github-coding-agent
permission_equality : false
required_effects  : 5 / 5 reachable
prohibited_effects: 0 / 6 reachable
verdict           : Conditionally equivalent
```

### What B decides that A cannot

- A produces two configurations; **B produces a judgement about their
  relationship for a purpose** — the exact thing (C1 + C2) no rival concept in
  the distinction test carried.
- B's prohibited set is generated from the native's surface (relational); A's is
  not.
- B answers the substitution/authorization question ("can P be routed to the
  candidate, bounded relative to the native?"); A answers only the
  configuration question.

### Honest boundary

If an organization only ever asks *"minimize the agent,"* Isotely adds nothing
over least privilege, and Falsifier 2 would stand for that use. Isotely earns
its keep specifically when the decision is **cross-class and purpose-scoped**:
*can this unlike identity stand in for the native one for this purpose, and what
must remain impossible relative to what the native can do?* RC-001 is
constructed to be exactly that decision, which is why the counterfactual favours
B — but only for that class of decision, and we say so plainly.

**Falsifier 2 is discharged for the cross-class substitution decision, and
explicitly not claimed beyond it.** Falsifier 3 is discharged by the live run
producing `required 5/5`, `prohibited 0/6`, `permission_equality false`
(Phase D).

---

## Live-run success rule (fixed before Phase D)

> **A live run succeeds if it resolves Falsifier 3, not if it produces the
> highest verdict class.**

Success is the observation that **operational parity is satisfied while
permission equality is false** — i.e.

```
required_effects   : 5 / 5 reachable
prohibited_effects : 0 / 6 reachable
permission_equality: false
```

on the fully auditable case. The **verdict class is a description of *how* parity
holds, not a score to be maximised**:

- `Conditionally equivalent` is a **successful** RC-001 result. It says parity
  holds but leans on an external declared barrier (branch protection requiring
  review). This is *more precise*, not weaker, than claiming the profile alone
  suffices.
- `Purpose-equivalent` would also be a successful result, and would say the
  candidate profile enforces every prohibition on its own.

The run report **must state explicitly** why the final verdict is
`Conditionally equivalent` or `Purpose-equivalent` — which prohibitions were
profile-enforced and which relied on an external condition. Chasing a higher
verdict class by widening the candidate profile is forbidden: it would convert a
parity result into privilege inheritance and fail `P4`.

A run that produces `Over-privileged`, `Non-equivalent`, or `Unassessed` has
**not** resolved Falsifier 3, and RC-001 remains undischarged.

---

## Runner / target separation (Phase C safety invariant)

The credential that can act as the candidate must never live where the candidate
can reach it.

```
CONTROL repo (this repo, sohadot/isotely)          TARGET repo (isotely-rc001-test-target)
- holds the live-run workflow                      - disposable; a file or two + protected main
- holds APP_PRIVATE_KEY (Actions secret)           - the GitHub App is installed HERE ONLY
- holds APP_CLIENT_ID   (Actions variable)         - branch protection: PR + 1 approval, no bypass
- the App has NO access to this repo               - the App CANNOT read this repo's secrets
         │  mints short-lived installation token
         └─────────────────────────────►  acts as candidate against TARGET only
```

- The App is installed **only** on the target, so the candidate cannot read the
  private key that drives it. `P9`-style hidden-infrastructure risk is contained.
- The App is **not** granted `Administration` (not even `read`). Reading branch
  protection needs `Administration: read`, which would pollute the very profile
  under test. Branch-protection configuration is therefore recorded separately as
  **environment evidence** by an admin/provisioning step (`evidence/environment.json`),
  never read by the candidate. The candidate proves it cannot merge by *attempting*
  the merge and receiving GitHub's rejection — not by inspecting the protection.

---

## Build phases

| Phase | What | State | Produces evidence? |
|---|---|---|---|
| **A** | Harness construction (manifest, profiles, evaluator, adapters, tests, schema) | **done** | no |
| **B** | Offline harness validation (evaluator + verdict logic proven on fixtures) | **done — 14/14 tests pass; offline verdict = Conditionally equivalent** | no |
| **C** | Live test environment provisioning (disposable repo + minimal GitHub App + branch protection) | **automation + runbook ready** (`PROVISIONING.md`, workflow, live adapter, evidence schemas); human provisioning steps pending | no |
| **D** | Observed run (live adapter → real observations) | pending human provisioning | **yes** |
| **E** | Verdict issuance (`verdict.json` from live observations) | pending Phase D | **yes** |

Phase C splits into what is code (built now) and what only a human can do:

| Phase C step | Who | State |
|---|---|---|
| Live adapter with raw-observation capture + safe destructive probes | this harness | **built** (`harness/github_adapter.py`) |
| Live runner that writes evidence + `verdict.json` (live source only) | this harness | **built** (`harness/run_live.py`) |
| GitHub Actions workflow (control repo mints token, runs against target) | this harness | **built** (`.github/workflows/rc-001-live-run.yml`) |
| Raw-observation + environment evidence schemas | this harness | **built** (`evidence/*.schema.json`) |
| Create disposable target repo + protected `main` | **human** | pending |
| Create GitHub App, generate private key, install on target only | **human** | pending |
| Store `APP_PRIVATE_KEY` secret + `APP_CLIENT_ID` variable in control repo | **human** | pending |

See `PROVISIONING.md` for the exact human steps. The private key is created by
GitHub for the App owner and must never enter this repository, this chat, or the
target repo — only the control repo's Actions secret store.

## How to run the offline validation

```
cd reference-cases/rc-001-github-coding-agent
python3 harness/run_offline.py          # prints HARNESS VALIDATION result
cd tests && python3 -m unittest -v      # 14 tests, every verdict path
```

Neither command produces evidence. Both validate the machine.

---

## What a successful live run establishes — and does not

**Establishes:** on one fully auditable case, operational parity for a declared
purpose exists **without** permission equality, and the distinction changes a
real grant/substitution decision. That is executable, reproducible support for
the Isotely distinction.

**Does not establish:** that "Isotely" is the term practitioners will adopt,
that every coding agent is a GitHub App, or that the category is a standard. One
auditable case earns the right to be demonstrated, not declared.

---

## Case log

- **2026-08-13:** Phases A–B complete. Harness built dependency-free; 14/14
  unit tests pass; offline validation yields `Conditionally equivalent`
  (correctly non-publishable). Counterfactual written; Falsifier 2 discharged
  for the cross-class substitution decision. Awaiting Phase C provisioning for
  live evidence.
