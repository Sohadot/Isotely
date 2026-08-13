# Category Distinction Test

## Status

- **Type:** existential validation artifact
- **Posture:** adversarial — this document attacks Isotely; it does not defend it
- **Phase gate:** must pass before RC-001 is built as executable proof, and before any `1.0` designation
- **Version:** test-run-001
- **Date:** 2026-08-13
- **Binding:** subordinate to `domain-dossier.md` canonical definition (fixed under `P8`) and `FOUNDATION_DOCTRINE.md`

---

## Why this document exists

Isotely claims to be a distinct conceptual category. That claim is worthless until it survives contact with the vocabulary that already exists. A category that cannot be distinguished from established terms is not a category — it is a synonym with a Greek costume.

This document therefore does the opposite of marketing. It lines up the concepts nearest to Isotely and tries to prove that **one of them already says everything Isotely says**. If any single existing concept passes that test, Isotely is not an independent category and the build stops here.

The test is designed to be **falsifiable**. The falsification condition is stated explicitly in the final section. This is the most important document in the project, because it is the only one that can end the project.

---

## The claim under test (test predicate)

> **Two unlike identity classes can be operationally equivalent for a declared purpose while remaining permission-asymmetric — and this equivalence is bounded, evidence-backed, and defines effects that must remain impossible.**

A concept can only be judged **SAME** as Isotely if it expresses that full predicate *on its own*, without borrowing Isotely's framing. To make the judgment mechanical rather than rhetorical, the predicate is decomposed into six atomic components. A concept "expresses" Isotely only if it carries **all six**.

| # | Component | What it requires |
|---|---|---|
| **C1** | Cross-class | The concept compares **two unlike identity classes** (e.g. human vs. agent), not the footprint of one identity. |
| **C2** | Equivalence relation | It asserts a **binary relation of equivalence/parity** between actors, not a unary grant to a single actor. |
| **C3** | Declared purpose | Equivalence is scoped to a **stated operational purpose**, not evaluated in the abstract. |
| **C4** | Effect, not permission | The unit of evaluation is **operational effect**, not the syntactic permission/entitlement list. |
| **C5** | No permission symmetry | It explicitly permits — even requires — the two actors to hold **different permission sets** (rejects privilege inheritance). |
| **C6** | Prohibited effects first-class | It treats **effects that must remain impossible** as part of the claim, not as an afterthought. |

A concept that carries some components but not all is not a rival category; it is a neighbour that answers a *different* question. The registry records exactly which components each concept carries.

---

## Verdict vocabulary and decision rule

Each concept receives exactly one verdict. The verdicts are ordered by threat to Isotely's independence, most dangerous first.

| Verdict | Meaning | Consequence for Isotely |
|---|---|---|
| **SAME** | The concept alone carries **all of C1–C6**. It already says what Isotely says. | **Fatal.** Isotely is not an independent category. Stop the build. |
| **OVERLAP** | The concept carries **C4 or an adjacent axis strongly** and shares real conceptual ground, but is missing at least one of C1/C2/C5. Isotely and it can be confused. | **Survivable, but a boundary line must be drawn** in writing so the two are never conflated. |
| **ADJACENT** | The concept answers a **neighbouring question** (a different one of the WHO/AUTH/AUTHZ/DELEGATION/EXECUTION layers) and shares vocabulary or lineage, but is not on the same axis. | Safe. Record the relationship; may donate vocabulary. |
| **ORTHOGONAL** | The concept lives on a **different layer entirely** (a mechanism, an enforcement model, or a subject taxonomy). It does not compete with the claim. | Safe. May be an enabling mechanism or an input. |

**Decision rule for the whole test:** Isotely survives if and only if **zero concepts are SAME**. Every OVERLAP additionally obligates a written boundary line before the concept in question may be referenced elsewhere in the asset.

---

## The registry

Each entry uses the eight-field lexicon-governance schema from `domain-dossier.md`, extended with the component checklist and the verdict.

Component checklist legend: `✓` carried, `·` absent, `~` partial/implicit.

---

### 1. Zero Standing Privilege (ZSP)

- **market_term:** Zero Standing Privilege
- **source:** common industry usage; privileged-access-management and cloud-security vendor literature
- **source_type:** industry practice / vendor category
- **observed_definition:** No identity holds persistent (standing) privileges; access is provisioned ephemerally and revoked, so the resting-state privilege footprint approaches zero.
- **overlap_with_isotely:** Both reduce the authority an actor carries beyond what a task needs; ZSP's time dimension can appear inside an Isotely parity boundary (`P6`).
- **conflict_or_gap:** ZSP governs the **temporal persistence of one identity's privilege**. It says nothing about comparing two unlike classes, nothing about a declared purpose as an equivalence scope, and nothing about operational-effect equivalence.
- **components:** C1 `·` · C2 `·` · C3 `·` · C4 `~` · C5 `·` · C6 `·`
- **verdict:** **ADJACENT**
- **rationale:** ZSP answers *"how long should privilege persist?"* Isotely answers *"can an unlike class be operationally equivalent for a purpose without inheriting privilege?"* ZSP can be one constraint (the time axis) inside an Isotely boundary, but it makes no equivalence claim. **Label warning:** the word `standing` is owned by ZSP and Standing Privilege; Isotely must never adopt `standing` as its category label (already flagged as Strategic Risk 2 in the dossier).

---

### 2. Just-in-Time (JIT) access

- **market_term:** Just-in-Time access / JIT provisioning
- **source:** PAM and cloud IAM practice
- **source_type:** industry practice
- **observed_definition:** Access is granted only at the moment of need and expires afterward, minimizing the window of availability.
- **overlap_with_isotely:** Shares the boundary/time constraint idea (`P6`); a JIT grant may implement the time dimension of a parity boundary.
- **conflict_or_gap:** JIT is a **provisioning mechanism about *when* access exists**. No cross-class comparison, no equivalence relation, no purpose-scoped effect evaluation.
- **components:** C1 `·` · C2 `·` · C3 `~` · C4 `·` · C5 `·` · C6 `·`
- **verdict:** **ADJACENT**
- **rationale:** JIT answers *"when is access provisioned?"* It is a delivery mechanism, not a category of equivalence. Same family as ZSP.

---

### 3. Principle of Least Privilege (PoLP)

- **market_term:** Least Privilege / Just Enough Access
- **source:** Saltzer & Schroeder (1975) and universal security doctrine
- **source_type:** foundational security principle
- **observed_definition:** An actor should hold the minimum permissions necessary to perform its function, and no more.
- **overlap_with_isotely:** The **most dangerous overlap.** Isotely's candidate identity is always least-privileged for its purpose; an Isotely `Over-privileged` verdict is precisely a least-privilege failure.
- **conflict_or_gap:** Least privilege is a **unary minimization** — "grant *this* identity as little as possible." It never references a second identity, never asserts equivalence, and never requires a declared purpose as the equivalence scope. You can fully satisfy least privilege without ever making a parity claim.
- **components:** C1 `·` · C2 `·` · C3 `~` · C4 `~` · C5 `~` · C6 `~`
- **verdict:** **OVERLAP**
- **rationale:** Least privilege carries fragments of many components but not the two that define Isotely: **C1 (cross-class) and C2 (equivalence relation)**. It is a minimization principle; Isotely is a comparison verdict.
- **BOUNDARY LINE (required):** *Least privilege answers "how little should this one identity hold?" Isotely answers "are these two unlike classes operationally equivalent for the declared purpose, while permission-asymmetric?" Least privilege is a discipline applied to Isotely's candidate; Isotely is the cross-class judgment that least privilege alone cannot express. Isotely contains least privilege; it is not contained by it.*

---

### 4. Scoped / short-lived credentials (fine-grained tokens)

- **market_term:** scoped tokens / fine-grained permissions / short-lived tokens
- **source:** OAuth scopes, GitHub App fine-grained permissions, cloud STS
- **source_type:** implementation mechanism
- **observed_definition:** Credentials carry a narrow, explicitly enumerated permission scope and a short lifetime.
- **overlap_with_isotely:** This is the exact substrate RC-001 uses to *enforce* a parity boundary.
- **conflict_or_gap:** A pure **mechanism on a different layer**. It can carry an Isotely boundary but makes no conceptual claim about equivalence, purpose, or cross-class comparison.
- **components:** C1 `·` · C2 `·` · C3 `·` · C4 `·` · C5 `~` · C6 `·`
- **verdict:** **ORTHOGONAL**
- **rationale:** Scoped credentials are *how* an Isotely boundary is realized, not *what* Isotely claims. Enabling mechanism, not a competing category.

---

### 5. Purpose-Based Access Control (PBAC)

- **market_term:** Purpose-Based Access Control (also "purpose limitation" in data protection)
- **source:** privacy engineering / GDPR purpose-limitation lineage; some IAM vendor usage
- **source_type:** access-control model / regulatory principle
- **observed_definition:** Access decisions are conditioned on the declared purpose for which data or a resource will be used; the same subject may be permitted or denied depending on stated purpose.
- **overlap_with_isotely:** Strong overlap on the **purpose axis** — this is the established home of Isotely's `P2` (declared purpose is mandatory). Isotely should explicitly acknowledge this lineage.
- **conflict_or_gap:** PBAC binds **one subject's permission** to a purpose. It does not compare two unlike identity classes and does not assert an equivalence relation between them. Purpose is a *gate* in PBAC; in Isotely purpose is the *scope of an equivalence claim*.
- **components:** C1 `·` · C2 `·` · C3 `✓` · C4 `~` · C5 `·` · C6 `~`
- **verdict:** **OVERLAP**
- **rationale:** PBAC owns the purpose primitive but not the cross-class equivalence relation. Isotely adopts PBAC's "purpose" vocabulary and adds C1, C2, C5.
- **BOUNDARY LINE (required):** *PBAC asks "may this subject act, given the declared purpose?" Isotely asks "are these two unlike classes operationally equivalent for the declared purpose, without permission symmetry?" Isotely uses purpose as PBAC does, but as the boundary of a comparison, not as a per-subject gate. Note: some vendors expand "PBAC" to "Policy-Based Access Control"; that reading is an enforcement model and collapses into the ABAC entry below.*

---

### 6. Attribute-Based Access Control (ABAC)

- **market_term:** Attribute-Based Access Control
- **source:** NIST SP 800-162 and policy-engine literature
- **source_type:** enforcement model
- **observed_definition:** Access decisions are computed by policy evaluated over attributes of subject, resource, action, and environment.
- **overlap_with_isotely:** ABAC is expressive enough to *implement* an Isotely boundary as policy.
- **conflict_or_gap:** ABAC is a **general enforcement model on a different layer**. It has no inherent notion of cross-class equivalence, purpose-scoped parity, or first-class prohibited effects; those would be things you *encode in* ABAC policy, not things ABAC *is*.
- **components:** C1 `·` · C2 `·` · C3 `·` · C4 `·` · C5 `·` · C6 `·`
- **verdict:** **ORTHOGONAL**
- **rationale:** ABAC is a mechanism that could enforce Isotely, exactly as arithmetic could compute a tax rate. Different layer; no competition.

---

### 7. Delegation (OAuth delegation, on-behalf-of, constrained delegation)

- **market_term:** delegation / on-behalf-of / Kerberos constrained delegation
- **source:** OAuth, OIDC, Kerberos, enterprise IAM
- **source_type:** authority model
- **observed_definition:** An actor exercises authority **derived from** a principal, acting as or for that principal. Constrained delegation narrows the services/resources for which the derived authority is valid.
- **overlap_with_isotely:** Both frequently involve an agent operating in a human's workflow; the dossier's boundary map places delegation directly adjacent to Isotely ("ON WHOSE BEHALF?").
- **conflict_or_gap:** Delegation is **authority derivation**: the delegate's power *comes from* the principal, and typically trends toward inheriting it — the exact move `P4` rejects. Isotely's claim is equivalence of *effect* achieved with **independently scoped, non-derived** authority. Constrained delegation narrows the derivation but is still derivation, not an equivalence-without-inheritance claim.
- **components:** C1 `~` · C2 `·` · C3 `·` · C4 `~` · C5 `·` (delegation tends to the *opposite* of C5) · C6 `·`
- **verdict:** **ADJACENT** (and the primary contrast class)
- **rationale:** Delegation answers *"whose authority is being exercised?"* Isotely answers *"can the unlike class be equivalent for the purpose without exercising or inheriting the native's authority?"* Delegation is the concept Isotely most sharply defines itself **against**, which strengthens rather than threatens the category.

---

### 8. Effective permissions / effective access

- **market_term:** effective permissions / effective access / net effective access
- **source:** cloud IAM (AWS/Azure/GCP effective-access tooling), CIEM
- **source_type:** analytic / computed view
- **observed_definition:** The computed net set of what an identity can actually do after all grants, denies, inheritance, and policy are resolved.
- **overlap_with_isotely:** Closest concept to Isotely's `P3` "operational effect." Isotely's reachability analysis consumes effective-permission computation as an input.
- **conflict_or_gap:** Effective permissions is a **descriptive, unary enumeration** of one identity's resolved capability. It answers "what can this identity do?" It does not compare two classes, does not scope to a purpose, and renders no verdict; it is a fact, not a judgment.
- **components:** C1 `·` · C2 `·` · C3 `·` · C4 `✓` · C5 `·` · C6 `·`
- **verdict:** **OVERLAP**
- **rationale:** Effective permissions owns the effect axis (C4) but nothing else. It is the *measurement*; Isotely is the *purpose-scoped cross-class judgment built on that measurement*.
- **BOUNDARY LINE (required):** *Effective permissions asks "what can this identity do?" (descriptive, one identity). Isotely asks "for this purpose, are the required effects reachable and the prohibited effects excluded, across two unlike classes?" (evaluative, two classes, purpose-scoped, verdict-bearing). Isotely consumes effective-permission analysis; it is not reducible to it.*

---

### 9. Permission / privilege parity (the anti-term)

- **market_term:** permission parity / privilege parity / "give the agent the same access as the user"
- **source:** informal practitioner shorthand; common misconfiguration pattern
- **source_type:** informal usage / anti-pattern
- **observed_definition:** Making a second identity's permission set equal to a reference identity's so it "can do the same things."
- **overlap_with_isotely:** Shares only the word *parity*.
- **conflict_or_gap:** This is the framing Isotely **negates**. `P3` and `P4` state that permission symmetry is neither necessary nor sufficient for operational parity, and that copying a native identity's privileges is often over-privilege, not parity.
- **components:** C1 `~` · C2 `~` · C3 `·` · C4 `·` (evaluates permissions, not effects) · C5 `✗ inverted` · C6 `·`
- **verdict:** **ADJACENT (inverted / contrast)**
- **rationale:** Permission parity is Isotely's foil, not its rival: Isotely = operational parity **without** permission parity. **Label warning:** because this anti-term owns the bare word `parity`, Isotely must always qualify it as **operational** parity and never let "parity" stand alone as the category label.

---

### 10. Non-Human Identity (NHI) / workload identity / machine identity

- **market_term:** Non-Human Identity, workload identity, machine identity, service identity
- **source:** emerging identity-security category; cloud workload-identity systems
- **source_type:** subject taxonomy
- **observed_definition:** A classification of actors that are not human users — service accounts, workloads, applications, agents — and their lifecycle and governance.
- **overlap_with_isotely:** Supplies the *classes* Isotely compares; "non-native identity" subtypes map onto NHI categories.
- **conflict_or_gap:** NHI is a **noun (a taxonomy of subjects)**; Isotely is a **relation (a verb) between classes**. NHI tells you *what kind of actor* exists; it makes no equivalence claim.
- **components:** C1 `~` (names classes but does not compare them) · C2 `·` · C3 `·` · C4 `·` · C5 `·` · C6 `·`
- **verdict:** **ORTHOGONAL**
- **rationale:** Different layer: subject taxonomy vs. equivalence relation. Isotely adopts NHI vocabulary for its non-native identity classes without competing with it.

---

### 11. Capability-based security

- **market_term:** capability-based security / object capabilities
- **source:** Dennis & Van Horn (1966); ocap literature
- **source_type:** security model
- **observed_definition:** Authority is held as unforgeable capabilities that confer specific rights on specific objects; possession of a capability *is* the authority, independent of identity.
- **overlap_with_isotely:** Shares the stance that authority should attach to specific permitted effects rather than to identity broadly — aligned with `P4`.
- **conflict_or_gap:** A **model on a different layer.** It expresses "authority = specific rights, not identity" but makes no purpose-scoped, cross-class *equivalence* claim and renders no verdict.
- **components:** C1 `·` · C2 `·` · C3 `·` · C4 `~` · C5 `~` · C6 `·`
- **verdict:** **ADJACENT**
- **rationale:** Capability security is a philosophically friendly model that Isotely can build on (authority decoupled from identity), but it answers "how is authority represented?" not "are two classes equivalent for a purpose?"

---

### 12. Segregation / Separation of Duties (SoD)

- **market_term:** Segregation of Duties / Separation of Duties
- **source:** access governance, audit, and fraud-control practice
- **source_type:** governance control
- **observed_definition:** Certain combinations of permissions or duties must never be held by the same actor, to prevent fraud or error.
- **overlap_with_isotely:** Donates the lineage for `P5` — the idea that some effects must remain **impossible** and that prohibiting effects is a first-class control.
- **conflict_or_gap:** SoD constrains **conflicting duties within/among actors** for control purposes. It carries C6-like reasoning but no cross-class equivalence relation and no purpose-scoped parity.
- **components:** C1 `·` · C2 `·` · C3 `·` · C4 `~` · C5 `·` · C6 `~`
- **verdict:** **ADJACENT**
- **rationale:** SoD is the closest lineage for Isotely's prohibited-effects principle, but it is a control pattern, not an equivalence category.

---

## Component coverage matrix

The clearest way to see whether any rival is SAME: no single row carries all six columns.

| Concept | C1 cross-class | C2 equivalence | C3 purpose | C4 effect | C5 no-symmetry | C6 prohibited | Verdict |
|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| Zero Standing Privilege | · | · | · | ~ | · | · | ADJACENT |
| JIT access | · | · | ~ | · | · | · | ADJACENT |
| Least Privilege | · | · | ~ | ~ | ~ | ~ | OVERLAP |
| Scoped/short-lived creds | · | · | · | · | ~ | · | ORTHOGONAL |
| PBAC (purpose-based) | · | · | ✓ | ~ | · | ~ | OVERLAP |
| ABAC | · | · | · | · | · | · | ORTHOGONAL |
| Delegation | ~ | · | · | ~ | · | · | ADJACENT |
| Effective permissions | · | · | · | ✓ | · | · | OVERLAP |
| Permission parity (anti) | ~ | ~ | · | · | inv | · | ADJACENT(inv) |
| NHI / workload identity | ~ | · | · | · | · | · | ORTHOGONAL |
| Capability-based security | · | · | · | ~ | ~ | · | ADJACENT |
| Segregation of Duties | · | · | · | ~ | · | ~ | ADJACENT |
| **Isotely (target)** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | — |

**No row other than Isotely carries C1 + C2 together.** The cross-class equivalence relation is the load-bearing distinction. Every rival that touches effect (effective permissions), purpose (PBAC), or minimization (least privilege) does so as a **unary** statement about one identity. None makes a **binary equivalence judgment across unlike classes**.

---

## Synthesis

1. **Zero concepts are SAME.** Isotely survives the existential test.
2. **The survival is narrow and honest.** Isotely is **not a new primitive.** It is a **named composition** sitting at the intersection of three established axes — *purpose* (from PBAC), *minimization* (from least privilege), and *effect measurement* (from effective permissions) — reassembled as one thing none of them is: a **binary, cross-class, purpose-scoped equivalence verdict with first-class prohibited effects.**
3. **The load-bearing distinction is C1 + C2** (cross-class equivalence relation). If Isotely ever drops the requirement that it compares *two unlike classes* and renders an *equivalence verdict*, it immediately collapses into least privilege or effective permissions and loses its independence.
4. **Three OVERLAP boundary lines are now mandatory** (least privilege, PBAC, effective permissions) and are written above. Any asset surface that mentions these concepts must carry the corresponding line.
5. **Delegation is the productive contrast.** Isotely is sharpest when stated against delegation: *equivalence of effect without derivation or inheritance of authority.*
6. **Two label constraints are confirmed:** never use `standing` (ZSP collision) and never use bare `parity` (permission-parity collision) as the category label. Always `operational parity`.

### The one sentence no rival expresses alone

> **Two unlike identity classes can be operationally equivalent for a declared purpose while remaining permission-asymmetric — and that equivalence is falsifiable.**

This is the sentence Isotely must be able to defend and demonstrate. It is the reason the category is allowed to continue.

---

## Falsification statement

This test is falsifiable. **Isotely fails as an independent category if any of the following is shown:**

1. **A SAME concept exists** — a single established term whose *standard* definition already carries all of C1–C6 and renders a cross-class, purpose-scoped equivalence verdict. *(Result of this run: none found.)*
2. **C1+C2 can be reduced away** — someone demonstrates that "cross-class equivalence" adds nothing that least-privilege-per-identity plus effective-permission analysis does not already give, i.e. the equivalence verdict is never actionably different from independently minimizing each identity. *(Not shown; RC-001 is the intended test of exactly this — see below.)*
3. **No purpose exists where the verdict differs from least privilege** — if every realistic purpose yields the same operational decision whether you reason "Isotely-equivalent" or merely "least-privileged," the extra vocabulary is unjustified.

Falsifiers 2 and 3 **cannot be settled by argument.** They are settled by RC-001 producing a case where `operational parity = satisfied` while `permission equality = false`, and where that distinction changes what an engineer would actually grant. That is why the next step is executable proof, not interface.

---

## Gate result

| Question | Result |
|---|---|
| Any SAME verdict? | **No** |
| Isotely survives as an independent category? | **Yes — provisionally** |
| Mandatory boundary lines written? | Yes — least privilege, PBAC, effective permissions |
| Label constraints confirmed? | Yes — no `standing`, no bare `parity` |
| Remaining existential risk? | Falsifiers 2 and 3 — resolvable only by executable RC-001 |

### Decision

**Proceed to RC-001 as executable proof.** The category has earned the right to be demonstrated, not yet the right to be declared a standard. RC-001 must be built to specifically discharge Falsifiers 2 and 3: it must produce a purpose for which `operational parity = satisfied` and `permission equality = false`, and that distinction must be verifiable, not asserted.

If RC-001 cannot produce that separation on a fully auditable case, this document's verdict is downgraded and the build stops — exactly as `FOUNDATION_DOCTRINE.md` requires: **one failed gate means no publication.**

---

## Consequences to record elsewhere (proposed, not yet canonical)

Per `P8`, the canonical definition is unchanged. The following are *proposed* refinements for the lexicon and positioning, to be logged before adoption:

1. Add to the lexicon that Isotely's independence rests on **C1 (cross-class) + C2 (equivalence relation)**; these two are non-negotiable identity conditions of the category.
2. Record the three boundary lines (least privilege / PBAC / effective permissions) as canonical distinctions once RC-001 confirms them operationally.
3. Record delegation as the canonical **contrast class** in the category boundary section.
4. Confirm the standing/parity label constraints as hard naming rules.

---

## Test log

- **test-run-001 — 2026-08-13:** First adversarial pass against twelve nearest concepts. Zero SAME verdicts. Isotely survives provisionally. Three OVERLAP boundary lines established. Gate decision: proceed to executable RC-001 to discharge Falsifiers 2 and 3.
