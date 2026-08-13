# Foundation Doctrine

## Status

- **Constitutional status:** Active
- **Tracked version:** 1.0
- **Version tracking instituted:** 2026-08-10

This is the constitutional document of the Sovereign Asset System.

It does not describe how assets are built. It defines what may never be violated while building them, who resolves conflicts between documents, and how this system itself is allowed to change.

Every standard, operating rule, template, and asset repository in this portfolio is bound by this doctrine. A rule that is not enforced is a suggestion. This doctrine exists so that governance is enforced, not aspirational.

---

## Purpose

The Sovereign Asset System removes randomness from how digital assets are built, evaluated, and positioned. Randomness re-enters through three doors:

1. **Discretion at publish time** — "this page is good enough for now."
2. **Silent change** — rules, claims, or structures modified without record.
3. **Document conflict** — two governing documents disagree and the weaker one is followed.

This doctrine closes all three doors.

---

## Document Hierarchy

### Methodology level (this repository)

1. `FOUNDATION_DOCTRINE.md` — this document
2. Standards — `CATEGORY_ARTIFACT_STANDARD.md`, `INTELLIGENCE_FACTORY_DOCTRINE.md`, `INTERFACE_GOVERNANCE.md`, `BUYER_LOGIC_AND_VALUE_MAXIMIZATION.md`, `SOVEREIGN_ASSET_EXECUTION_ORDER.md`
3. Operating rules — `operating-rules/`
4. Contexts and templates — `contexts/`, `templates/`

### Asset level (each asset repository)

1. The asset's `ASSET_THESIS.md` — supreme within its repository
2. The asset's plans and policies (`ASSET_INTELLIGENCE_FACTORY_PLAN.md`, content, SEO, security, monetization policies)
3. Data registries (routes, terms, sources, claims)
4. Build and validation tooling

### The binding rule between levels

An asset thesis is supreme **within its repository**, but it may not weaken a portfolio non-negotiable. An asset may always be stricter than the methodology. It may never be looser.

---

## Precedence Rule

When two governing documents conflict:

1. The higher document in the hierarchy governs.
2. At equal rank, **the stricter rule wins**.
3. If strictness is ambiguous, the conflict must be resolved by amendment and recorded in the decision log — not by the judgment of whoever is publishing that day.

No conflict may be resolved silently.

---

## The Non-Negotiables

The following bind every asset in the portfolio, in every language, in every phase. They may not be bypassed for speed, volume, monetization, experimentation, or launch pressure.

1. **No phantom surfaces.** No placeholder pages, thin pages, draft pages in navigation or sitemap, or pages that exist only to increase count.
2. **No broken structure.** No broken internal links, orphaned pages, dead anchors, or missing canonical metadata in production.
3. **No ungoverned claims.** Every scientific, medical, technical, or performance claim is sourced, marked as conceptual interpretation, or excluded.
4. **No random SEO.** No keyword stuffing, auto-generated thin pages, fake comparison surfaces, or sitemap entries for incomplete pages. Search visibility is earned through reference quality.
5. **No trust-lowering revenue.** Revenue that raises trust is permitted. Revenue that lowers trust is forbidden. Monetization is disclosed, reviewed, and policy-bound.
6. **No unregistered surfaces.** No public page exists without a registered route. If a route is not registered, the page does not exist.
7. **No silent change.** Changes to a thesis, ontology, standard, protocol, or policy require a decision log entry and a version reference.
8. **No partial language launches.** A language layer launches complete and governed, or it remains unavailable.
9. **No hidden infrastructure.** No secrets, tokens, undisclosed data collection, or unreviewed third-party scripts in any public build that declares a static-first posture.
10. **No desperation.** No acquisition urgency language, public buyer targeting, or marketplace framing on any asset surface.

---

## Distribution, Authority, Leverage, and Scarcity

Sovereign category assets may intentionally publish doctrine, terminology, evidence, reference cases, and other citable materials when publication strengthens category recognition and long-horizon authority.

Conceptual propagation is not automatically treated as loss of control. For assets whose value depends on category recognition, propagation may be the distribution mechanism through which the category becomes legible.

The system therefore distinguishes four different value mechanisms:

1. **Propagation creates distribution.** Independent discussion, citation, critique, and compatible implementation can widen the conceptual surface of an asset.
2. **Attribution creates authority.** Clear provenance, version history, citable artifacts, and canonical stewardship strengthen the asset's reference position. Timestamped publication establishes provenance; it must not be misrepresented as automatic legal exclusivity or automatic prior-art status in every jurisdiction.
3. **Implementation creates leverage.** Reference implementations, evidence, datasets, tools, operational quality, and accumulated know-how can create practical defensibility beyond the public concept itself.
4. **Scarce identity remains scarce.** Exact domains, established brand identity, and other non-replicable coordination points may concentrate strategic value even when doctrine is public. Domain ownership alone does not establish trademark rights.

### Governing sentence

> **Propagation is distribution. Attribution is authority. Implementation is leverage. The domain is scarcity.**

### Publication restraint

This doctrine does not require indiscriminate disclosure. Public doctrine and reference material should be open enough to earn distribution and authority, while implementation details, security-sensitive material, proprietary datasets, and protectable know-how may remain controlled where disclosure would weaken the asset.

A useful operating formulation is:

> **Open doctrine. Controlled implementation. Owned identity.**

Publication remains subject to the repository's publication, authority, and quality gates.

---

## Enforcement Doctrine

1. Every asset defines a quality gate derived from the Non-Negotiables above and `operating-rules/quality-standard.md`.
2. The gate is **blocking**: one failed criterion means no publication. There is no "publish now, fix later."
3. Gate checks must be automated wherever automation is possible (links, routes, metadata, sitemap, claims coverage). Manual review is reserved for what machines cannot judge: meaning, safety, restraint.
4. A violation discovered after publication freezes further publication on that asset until remediated and logged.
5. Enforcement applies to the system itself: this repository's documents are subject to the same change discipline they impose.

---

## Amendment Procedure

This doctrine and its subordinate standards may change only by deliberate amendment:

1. The proposed change is written, with an explicit statement of whether it **strengthens** or **weakens** governance.
2. Weakening changes require written justification of why the strategic value exceeds the trust cost.
3. The change is recorded in the decision log with date and rationale.
4. The affected document's version reference is updated.
5. Asset repositories inherit the change explicitly, not implicitly — each affected asset records its adoption in its own decision log.

An unrecorded change to a governing document is invalid, regardless of who made it.

---

## Inheritance Requirement

Every Tier 1 and Tier 2 asset repository must:

1. Declare its binding to this doctrine in its thesis or governance documents.
2. Carry an asset-level quality gate document instantiating the Non-Negotiables with concrete, checkable values.
3. Maintain an append-only `DECISION_LOG.md`.
4. Resolve every internal conflict in favor of the stricter rule.

---

## Governing Sentences

> **A rule that is not enforced is a suggestion.**

> **An asset may always be stricter than the methodology. It may never be looser.**

> **No conflict is resolved silently. No change is made without record.**

> **One failed gate means no publication.**

> **Propagation is distribution. Attribution is authority. Implementation is leverage. The domain is scarcity.**
