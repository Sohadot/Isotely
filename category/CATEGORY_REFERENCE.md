# ISOTELY — Category Reference v0.2 (draft)
**Owner:** Sohadot  
**Updated:** 2026-10-25  
**Status:** Proposed strategic pivot; not approved for release, not a legal standard, not trademark clearance.

## Governing proposition
**Equal Treatment. Without Citizenship.**

**Isotely** is an attested English word with a historical lineage in the Greek concept *isoteleia*, associated with privileged fiscal equality for certain noncitizens without necessarily making them citizens. This is the historical root of our modern inquiry, not an assertion that the ancient term already denoted our entire proposed methodology. Academic source: [Lexicon of Citizenship, University of Milan](https://politeia.unimi.it/en/databases/lexicon-of-citizenship/).

**Editorial qualification:** the headline expresses the historically rooted *possibility* of bounded equal treatment without citizenship; it never promises universal equal treatment. The ancient Greek privilege was especially fiscal and did not confer all citizenship rights.

## Modern analytical category (working definition)
**Legal-status treatment parity** is a documented relationship between two expressly defined legal-status profiles with respect to *one specific right, obligation or legal treatment*, in a particular jurisdiction, at a particular effective time, with all relevant conditions and exceptions. It may be equal, conditional, different, inapplicable, disputed or unresolved.

This is **not** a measure of whether an entire country is “equal,” and it is **not** a ranking of human worth, rights in the abstract or quality of governance.

The commercial mark **ISOTELY** identifies the source of a maintained reference framework and potential licensed products. The general analytical expression **legal-status treatment parity** describes the underlying relation. Use of the name as a source identifier should be legally assessed in the actual target markets; a dictionary entry is not a registered trademark.

## Atomic unit / relation key
`jurisdiction | legal_status | comparator_status | specific_right_or_obligation | conditions | legal_source(s) | effective_time | verification_time | confidence_and_review_state`

The same named status may not be equivalent across countries. The same entitlement may have constitutional, statutory or administrative foundations that differ between profiles. Do not infer `no right` from absence of one specific legal foundation.

## Assessment vocabulary (initial, not exhaustive)
- **Equal under specified rule:** identical treatment solely within a narrow and documented legal norm.
- **Equal subject to a condition:** the parity boundary includes conditions or exceptions that change who qualifies.
- **Different legal foundations:** parties may enjoy a related right but under non-equivalent legal sources, durability or limitations.
- **Different entitlement:** one legal profile enjoys the specified right and the other does not under an established source.
- **Excluded / inapplicable:** the relation is outside the scope of an instrument or legally defined entitlement.
- **Unresolved / disputed:** the evidence is insufficient, conflicts, or depends on unresolved interpretation.

**Legal-source uncertainty is not proof of a limitation.** A model implementation must preserve `unresolved` rather than infer `different` or `equal` when legal evidence is insufficient.

## Bounded example (not a change event)
The Canada pilot contains three distinct point-in-time relationships for permanent residents compared with Canadian citizens: mobility/livelihood under Charter section 6(2)(b), different source of the ability to enter/remain (Charter and Immigration and Refugee Protection Act), and federal voting eligibility (Elections Canada guidance). See `evidence/isotely_canada_parity_pilot_v0.1.json` for precise source locations and limitations. The records are research-only, not certified or externally reviewed by qualified counsel.

## Change event — proposal, not demonstrated
A future **Parity Change Record** would tie a new authoritative legal instrument or judgment to a *specific relation key*. A valid event requires confirmed **before** and **after** rules, dates, source text, operative conditions, relevant legal hierarchy, an impact explanation and review sign-off. None of the Canada pilot records has been established as such an event.

## Why a buyer would pay (hypothesis)
A maintained, attributable, machine-readable legal-status comparison might save specialist review time or surface a material operational change. Potential uses: incorporation into LegalTech reference systems, global mobility compliance, or resident-status tools. **The market will not pay merely because the idea is elegant.**

A defensible acquisition asset would require, in addition to the brand and domain, clean transferable rights, updated evidence, documentation of QA, subscriber or license demand, independently tested reliability, manageable cost to refresh records, and repeatable distribution. Neither six- nor seven-figure value is established today.

## Competitive boundary
- **ImmigSR** already operationalizes de jure migrant social rights in 45 countries historically (1980–2021). An Isotely study is not first to encode migrant rights.
- **GLOBALCIT** already maps citizenship law and comparative legal states across many jurisdictions. An Isotely study is not first to compare nationality status internationally.
- **Commercial immigration law firms and platforms** already provide legislative news and some impact alerts. An Isotely study is not first to publish legal-change alerts.

**Hypothesis worth testing:** comparator-specific, right-specific treatment relationship records with version provenance and explicit uncertainty may improve a professional workflow relative to existing tools.

## Publication gate
Nothing in this bundle is approved for direct public release. Before changing the domain or depositing a DOI, complete: rights and trademark review; qualified legal sign-off for any specific legal conclusions; proofreading; provenance checks; removal of any unsupported novelty or market claims; explicit owner approval to shift Isotely's existing AI-identity public positioning. Historical and modern meanings must remain visibly differentiated.

## Sources
1. [University of Milan / Politeia — Isoteles / isoteleia](https://politeia.unimi.it/en/databases/lexicon-of-citizenship/).
2. [USPTO — Strong trademarks](https://www.uspto.gov/trademarks/basics/strong-trademarks).
3. [USPTO — Federal trademark searching](https://www.uspto.gov/trademarks/search/federal-trademark-searching).
4. [DeZIM Institute — ImmigSR technical report](https://www.dezim-institut.de/en/publications/the-immigrant-social-rights-data-set-immigsr/).
5. [European University Institute — GLOBALCIT Citizenship Law Dataset](https://cadmus.eui.eu/handle/1814/73190).
6. Canadian primary sources inside the record JSON.