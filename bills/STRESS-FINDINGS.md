## 119hr1847ih
## stress-119hr1847ih

- **Bill type/size:** H.R. 1847 is a two-page introduced House bill with one section and one operative sentence. The cached raw source is 145 words on one line. It is neither a resolution nor an appropriations measure; its sole operative mechanism is giving Executive Order 14158 force and effect of law by reference.
- **What the contract handled well:** One provision preserves the bill’s actual granularity, and the separate goal and effect fields capture the narrow legal-status change without pretending that the supplied text states DOGE programs or outcomes. Empty `barriers`, `metrics`, and `conditionals` arrays let the extraction record zero forecastable metrics and zero conditional cells instead of manufacturing content or a `series_hint`. The verbatim quote remains traceable to the cached source.
- **Where it strained:** The contract has no typed field for an incorporated instrument, its version, or source completeness, even though virtually all substantive content sits outside this bill. It also has no typed/rendered `sourceLimits` or honesty field, so the source-limit disclosure has to sit in `context`. A legal-status change does not naturally occupy the metric layers (`execution`, `participation`, or `outcome`), and with no metric there is no meaningful stance matrix. The `barriers` shape expects an actor even though the supplied text names no implementing actor and any legal-interpretation barrier would require analysis beyond the source. Likewise, an enactment “conditional” would merely restate the clause rather than define a forecastable official-data outcome. The bill has no short title, forcing `name` to carry its long official title, while `pages: 2` overstates substantive size because the second official page contains only the end of the sentence. Finally, the source specifies no appropriation, effective date, report, or release schedule that could anchor mechanical resolution.

## 119hr1021ih
## stress-119hr1021ih — H.R. 1021

### Bill type and size

H.R. 1021 is a short, ordinary House bill rather than a resolution, naming bill, or appropriations measure. The introduced PDF is four pages and contains four sections: a short title and three substantive provisions. It amends an existing Small Business Act collateral proviso, directs one GAO report, and imposes an ongoing SBA outreach-planning duty. It authorizes no appropriation. The supplied raw artifact is a complete but flattened 2,995-byte, 472-word text stream with no page breaks or metadata sidecar.

The extraction produces three provision records and eight candidate metric records. None of the metrics is presently forecast-ready: the Thesis docket contains no matching SBA or GAO concept, so every `series_hint` is intentionally empty.

### What the contract handled well

- The provision structure cleanly separated a legal rule change (§2), a one-time oversight deliverable (§3), and an administrative/outreach mandate (§4), even in a four-page bill.
- `goals`, `effects`, and `barriers` distinguished what the text commands from plausible participation effects and credit-risk trade-offs. This mattered because the bill does not promise more approvals or lower defaults.
- The `category` and `layer` fields separated execution evidence (a collateral rule, report delivery, or outreach plan), participation proxies (small-loan volume and rural application outcomes), and downstream outcomes (defaults, recoveries, awareness, and access).
- Complete stance matrices made the narrow relationship between each metric and each imputed goal explicit. For example, the outreach-plan metric serves both statutory planning goals while the participation metric separately tests whether rural access outcomes improve.
- Free-text conditionals could preserve enactment dependence and warn that the proposed questions are conceptual rather than resolution-ready.

### WHERE IT STRAINED

- The frozen TypeScript contract and exemplar do not define a `sourceLimits` field, even though this task requires an honesty note. The artifact therefore carries an additive top-level `sourceLimits` string that the current site loader will ignore rather than render.
- `pages` cannot be recovered from the supplied one-line raw text. The four-page value required checking the official Congress.gov PDF; the contract has no field distinguishing source-derived from externally recovered metadata.
- The raw cache flattens headings to forms such as `2. Collateral requirements for disaster loans`; the site's section-text slicer expects line-start `SEC. N.` headings. Quote validation succeeds, but the bill page cannot recover full section disclosures from this otherwise complete source without a normalization rule.
- Sections 2 and 4 are not self-contained: Section 2 supplies amendatory coordinates into 15 U.S.C. §636(d)(6), and Section 4 incorporates GAO-24-106755 recommendations without reproducing them. The one-URL bill block cannot record those distinct interpretive sources or distinguish text-only extraction from source-enriched analysis.
- Section 2 changes two linked dimensions inside one proviso: the mandatory floor rises from $14,000 to $50,000, while the Administrator's power to choose a still-higher floor expands from a “major disaster” to a “disaster.” A provision record can narrate both, but it cannot model them as separable treatments without duplicating the section.
- Current regulation already generally uses a $50,000 threshold for physical loans after presidential major disasters while retaining $14,000 for SBA-declared disasters. The schema has no dedicated baseline-law or baseline-practice field, so that crucial distinction sits in prose.
- `series_hint: ""` conflates several different judgments: no registry match, no public field, a one-time future report, an unstable administrative dataset, and an indirect aggregate proxy. A typed forecastability or registry-status field with reason codes would express these cases better.
- A stance value cannot express direction, lag, uncertainty, or sufficiency. “Serves” can mean that a metric measures a goal, not that a higher value is desirable; “orthogonal” must carry the difference between plan compliance and actual access in prose.
- Section 3's dates are relative to an unknown enactment date: the study window ends two years after enactment and the report is due three years after enactment. The closing phrase “during the period” also does not clearly say whether the window selects originations, observed performance, the amendment's impact, or all three. The bill leaves “default rate,” other performance measures, the comparison design, and public release undefined. Plain conditional strings cannot encode the rolling dates, cohort rule, denominator, maturity rule, public-evidence requirement, or one-sided resolution state.
- Section 4 begins on enactment but defines neither “rural” nor “urban,” mandates no particular actions or spending, sets no quantitative target, and requires no public plan or report. The contract can record these gaps only in prose; it cannot mark a goal as legally definite but empirically underidentified.
- The GAO report provision is both an independent implementation obligation and the evaluation mechanism for Section 2. Splitting it preserves actor and deadline clarity, but the schema has no provision-dependency edge linking §3 back to §2.
- The bill contains no appropriation. The schema has no explicit field for “unfunded mandate/no new budget authority,” so the capacity implication appears only as a barrier.

## 119sjres73is
# Stress-test findings: S.J. Res. 73

## Bill type and size

S.J. Res. 73 is an introduced Senate joint resolution using the congressional-disapproval structure in chapter 8 of title 5. The matching official introduced-version PDF is two pages, while the supplied cache is a 1,233-byte, 190-word, single-line text extraction. The measure has one 41-word operative clause and no numbered sections, findings, appropriations, deadlines, reporting duties, quantitative targets, or replacement policy.

The source records introduction by Mr. Whitehouse on August 1, 2025, two readings, and referral to the Senate Committee on Environment and Public Works. The extraction treats the stated no-force-or-effect consequence as contingent on enactment, not as a result already achieved by the introduced text.

## What the contract handled well

- A one-element `provisions` array represents the entire measure without artificial section splitting.
- `quote` and `context` preserve the exact cited rule, Federal Register reference, procedural posture, and narrow legal mechanism.
- The arrays permit one source-grounded goal and one source-grounded effect while leaving `barriers`, `metrics`, and `conditionals` empty.
- Empty metric and conditional arrays make it possible to record zero forecastable outcomes without inventing an EPA series identifier or a tautological enactment conditional.
- The free-text status and context fields can distinguish introduced text from enacted law.

## Where the contract strained

- The frozen JSON shape has no dedicated `sourceLimits` or honesty field. The note therefore lives in `context`, where the current UI will render it, rather than in an inert extra key.
- `pages` requires a number, but the supplied flattened text has no page boundaries. The value `2` required checking the matching official PDF; it cannot be recovered from the raw text alone.
- The flat extraction omits the standard resolving formula present in the PDF. This does not change the operative clause, but it shows that the cached text is normalized rather than page-verbatim.
- `goals` invites motive imputation, yet this resolution has no findings, purpose section, or short title. The sole goal therefore restates the operative objective and does not infer environmental, health, industry, or sponsor motives.
- `effects` does not distinguish a deterministic legal consequence conditional on enactment from an empirical likely effect. That distinction has to be carried in prose.
- The `barriers.actor` shape assumes an implementation actor. Here the only material contingency is legislative enactment, and the text specifies no post-enactment implementation machinery, so forcing a barrier row would misclassify procedure as implementation.
- The metric taxonomy and stance matrix assume an observable outcome. The binary legal status of the cited rule is observable, but conditional on enactment it follows directly from the clause and is not a useful recurring forecast series. The artifact therefore has no metric rows and, vacuously, no stance matrix.
- A conditional such as `P(rule has no force or effect | resolution enacted)` would be tautological rather than empirical, so `conditionals` is empty.
- The resolution incorporates the EPA rule and chapter 8 of title 5 by reference, but the contract has no dedicated field for an incorporated instrument and its provenance. The supplied bill text cannot support claims about the rule's requirements, regulated entities, emissions, costs, effective dates, enforcement, successor-rule constraints, or replacement baseline.
- The measure has no short title or numbered substantive section, so `name`, `title`, and `heading` necessarily repeat or descriptively compress the official long title. The current full-section UI helper also cannot key this unnumbered clause to a `Section N` or `§N` marker.

The result is intentionally small: one provision, one express goal, one enactment-contingent effect, zero implementation barriers, zero forecastable metrics, zero series hints, and zero conditionals.

## 119hr2449ih
# Stress-test findings: H.R. 2449 IH

## Bill type and size

H.R. 2449 IH is a short administrative-and-reporting House bill, not a joint resolution or appropriations measure. The official introduced-version PDF is five pages. The supplied cache is 4,203 bytes and 680 words on one flattened line. Section 1 is only the short title; Section 2 is the sole substantive provision and contains task-force establishment, membership, draft-and-comment, final-report, and definition subsections.

The extraction therefore uses one provision. Splitting every subsection into a separate provision would obscure that the 180-day draft deadline and one-year final deadline both depend on the actual establishment date created by the same section.

## What the contract handled well

- The bill block can identify the exact introduced version, retain its five-page source size, and distinguish that analyzed text from generic bill naming.
- One provision with context, goals, effects, and barriers preserves the section's integrated administrative sequence without pretending that the bill regulates or deploys 6G.
- The `category` and `layer` fields correctly classify the only candidate metrics as operational execution checks, not participation or downstream outcomes.
- Complete stance matrices make clear that the draft milestone serves the public-comment goal and the final milestone serves the final-report goal; neither is evidence that the Task Force was representatively composed.
- Free-text conditionals can at least sketch the enactment-and-establishment dependencies and state why the checks are not currently registry-ready.

## WHERE IT STRAINED

- The frozen contract has no typed, rendered `sourceLimits` field. The honesty disclosure therefore has to live inside `context`, mixed with substantive analysis.
- `pages` cannot be recovered from the supplied flattened cache. It required the exact-version official PDF, while the contract has no structured source-version or page-count provenance field.
- The bill block has no structured bill-type, text-version, status-as-of, or action-date fields. Those distinctions have to be packed into free-text `status` and `analyzed` strings.
- The one-line normalization removes pagination and the enacting clause, and its headings appear as `1.` and `2.` rather than line-start `SEC.` headings. The current raw-section slicer cannot reliably isolate Section 2 even though the quote-presence gate can still verify normalized fragments.
- Section 2 is one provision with dependent subsections, but the schema has no subsection identifiers or dependency graph. Splitting it would imply false independence; grouping it leaves several distinct duties inside one record.
- The deadlines use two nested clocks: establishment is due within 120 days after enactment, while both reports run from the actual establishment date. `conditionals` can narrate this but cannot encode anchor events, date arithmetic, missing-anchor behavior, or separate resolution sources structurally.
- The membership rule is qualified by “to the extent practicable,” and the trust screen contains discretionary and potentially nonpublic judgments. Goal strings and three-valued metric stances cannot express soft duties, prerequisites, partial compliance, or evidentiary uncertainty.
- The metrics model does not distinguish a one-time binary/date policy-state check from a recurring numeric series. An empty `series_hint` also conflates “observable official event with no registry concept,” “no guaranteed public resolver,” and “no measurable outcome.”
- Draft publication, accepting comments, considering comments, final publication, topic coverage, and committee submission have different evidence properties. A single metric text can explain those differences, but there are no structured fields for multiple venues, qualitative review, or private committee-receipt evidence.
- The report topics are qualitative and partly inherit whatever industry-led standards bodies identify. The bill supplies no quantified target for reliability, standards completion, supply-chain resilience, cybersecurity, siting, deployment, adoption, or intergovernmental coordination, so the contract cannot produce an honest downstream outcome metric here.
- The bill contains no dedicated appropriation, task-force size, quorum, member terms, compensation rule, enforcement mechanism, or required follow-up action. `barriers` can narrate those absences, but the contract has no fields distinguishing an unfunded mandate, use of existing authority, and a genuinely zero-cost duty.
- One `sourceUrl` identifies the introduced bill, but the bill also incorporates criteria from 47 U.S.C. §1601(c). The schema has no source list or citation graph for incorporated law.

## Honest extraction result

The final artifact has one provision, three procedural goals, four effects, three barriers, two one-time execution metrics, two event-conditional sketches, zero nonempty `series_hint` values, and zero recurring series-backed or downstream-outcome metrics. The administrative publication milestones are potentially observable after enactment, but they are not currently registry-ready because the statutory clocks depend on a future, not necessarily public establishment date.

## 119s1188is
# Stress-test findings: S. 1188

## Bill type and size

S. 1188 is a short, ordinary Senate tax bill rather than a resolution, naming measure, or appropriations bill. The official introduced-version PDF is four pages. The supplied raw artifact is a complete but flattened 2,781-byte, 447-word stream with two sections: a short title and one substantive Internal Revenue Code amendment in §2. The provision defines eligible flaring and venting mitigation systems, lists seven gas-disposition pathways, excludes property placed in service by a foreign entity of concern, and sets a post-2025 effective date. It authorizes no appropriation and requires no report.

The extraction produces one provision, three goals, two metric rows, and one conditional. One row is the selected recurring forecastable outcome candidate: EIA's annual U.S. Natural Gas Vented and Flared volume. EPA Greenhouse Gas Reporting Program petroleum-and-natural-gas emissions data were also considered, but their reporting thresholds, facility and source-category boundaries, and emissions units do not isolate bill-defined systems or gas diverted through the listed uses, so they were not inflated into a second metric. The EIA row is not a clean causal measure, and neither it nor the honest-gap row has a matching Thesis docket concept, so both `series_hint` values are intentionally empty.

## What the contract handled well

- A one-element `provisions` array preserves the bill's actual granularity instead of splitting one integrated tax rule into artificial provisions for the percentage, definition, exclusion, conforming amendment, and effective date.
- `goals` can separately expose the tax-treatment objective, the gas-disposition objective implied by the official title and operative definition, and the express foreign-entity exclusion.
- `effects` distinguishes accelerated cost recovery from equipment investment and from downstream gas or emissions outcomes. This avoids treating a first-year deduction as a guaranteed permanent tax saving or a guaranteed methane reduction.
- `barriers` records the post-introduction statutory collision, administrative substantiation, taxpayer documentation, and public measurement gaps without inventing a fiscal score or enforcement program.
- `category` and `layer` keep the recurring EIA outcome separate from the participation-level tax-data gap, while complete stance matrices show that the EIA series bears only on the gas-mitigation goal.
- An empty `series_hint` can honestly preserve a real official series as an unmapped candidate without manufacturing a Thesis registry identifier.
- The free-text conditional can preregister the policy comparison while warning that the aggregate EIA series is not a causal estimator.

## WHERE IT STRAINED

- The frozen site type does not define or render `sourceLimits`, even though the stress contract requires an honesty note. The artifact uses the additive top-level field and repeats the most material current-law limitation in rendered `context` prose.
- `pages` is mandatory but cannot be recovered from the supplied one-line text. The value `4` required checking the matching official Congress.gov PDF; the contract cannot mark that field as externally recovered.
- The flattened cache turns `SEC. 2.` into `2.` and removes page boundaries. Quote validation can normalize it, but the site's section-text helper may not recover the full section using its ordinary heading markers.
- S. 1188 was coherent against the §168(k) structure in existence when introduced, but Public Law 119-21 later struck §168(k)(2)(A)(iii) and paragraphs (6) and (8), all of which the bill still references, while making the general deduction 100 percent and permanent for qualifying post-January 19, 2025 property. The schema has no typed way to say “valid introduced text overtaken by later law,” “requires technical redraft,” or “marginal effect currently unclear.”
- The one-URL bill block cannot separately cite the introduced PDF, current statute, intervening public law, IRS implementation guidance, and EIA outcome series. Those sources and their distinct roles have to sit in prose.
- The official title says the property captures gas that would otherwise be flared or vented, but the operative eligibility definition requires only natural-gas intake plus one listed separation, collection, utilization, or combustion pathway. The contract has no field distinguishing an expressed purpose from an enforceable eligibility condition, so the gap must be narrated in `effects` and `sourceLimits`.
- “Permanent full expensing” combines a legal percentage, accelerated timing, present-value benefit, investment response, and a baseline-dependent fiscal effect. A goal or effect string cannot model those as distinct estimands or record that lifetime depreciation and first-year timing are different concepts.
- The seven eligible pathways include both collection or productive use and combustion, including electricity, computational power, and digital-asset mining. A single aggregate vented-and-flared volume cannot distinguish diversion to those uses, venting-to-combustion substitution, induced production, or net greenhouse-gas effects.
- The foreign-entity-of-concern clause is an eligibility exception rather than a downstream policy outcome. Putting it in `goals` makes the stance matrix possible, but the schema has no dedicated constraints, exceptions, definitions, or cross-reference structure.
- `series_hint: ""` conflates two different cases here: EIA publishes a real recurring official series that is absent from the Thesis registry, while IRS publishes no recurring field that isolates the proposed tax class. A typed forecastability status and reason code would preserve that distinction.
- The conditional is necessarily qualified by technical operability, a future year, a first-print release, and a non-causal interpretation. An unstructured string cannot encode the current-law version, acquisition-versus-placed-in-service treatment, intervention definition, exposure lag, or attribution limits as machine-checkable fields.
- The bill is a tax preference with no appropriation or reporting mandate. The contract has no fiscal-score status or “no dedicated reporting” fields, so the absence of a score and observable tax uptake appears only in prose.

The result is intentionally compact: one substantive provision and one recurring outcome candidate, with no invented series identifier and no claim that the introduced bill still produces a determinate incremental tax change under current law.

## 119hr80ih
## stress-119hr80ih — H.R. 80

- **Bill type / size:** An introduced House bill, not a resolution or appropriation. The supplied flat text is 433 words (2,662 bytes); the official bill is four pages, three of which are largely occupied by a 51-person list. It has two sections, with one substantive section containing a clearance-revocation command, a future-clearance bar, an investigation mandate, and the list that scopes all three.
- **What the contract handled well:** A single provision can preserve the unity of §2 while separating its two express activity goals, three legal/administrative effects, and implementation or verification barriers. Empty `metrics` and `conditionals` arrays make it possible to report no forecastable public series without fabricating a proxy or `series_hint`. The free-text mechanism and context fields can also preserve critical qualifications: the immediate revocation affects only people who actually hold a clearance, the 24-hour deadline does not govern the investigations, and an investigation mandate is not a finding of wrongdoing.
- **Where it strained — express command versus policy objective:** The `goals` array cannot distinguish a directly commanded legal act from an inferred social outcome. This source states only revocation, ineligibility, and investigation duties, so the extraction uses those duties as goals and declines to impute national-security, electoral-integrity, punishment, or deterrence objectives.
- **Where it strained — a fixed named cohort:** The 51-person list consumes most of the bill but the schema has no target-set, named-subject, or cohort field. Reproducing it in prose would bloat the artifact; omitting it entirely would hide the scope. The extraction records the count and location in context, but cannot machine-encode identity matching or the fact that the immediate effect varies with each person’s unreported current clearance status.
- **Where it strained — unlike mechanisms in one provision:** Subsection (a) combines a passively phrased 24-hour legal change with an indefinite eligibility rule, while subsection (b) creates open-ended work for two officials. Splitting them into separate provisions would make observability and timing cleaner but would duplicate the same named cohort and overstate the structure of a bill with one substantive section.
- **Where it strained — observability and stances:** The bill creates no public report, recurring administrative series, or measurable downstream outcome. Clearance status and investigation activity are person-specific and not made public by the text. The honest result is zero metrics, which also means zero stance matrices; the contract therefore has no machine-readable way to say that the goals are proposed legal commands but currently lack a resolvable evidence channel.
- **Where it strained — barriers versus source limits:** Some important constraints are not delivery barriers borne by a named actor. Undefined investigation terms, absent public-evidence rules, and missing baseline facts are partly drafting gaps and partly evaluation limits, but the schema offers only `barriers` plus free-form honesty prose. The additive `sourceLimits` note carries that distinction.
- **Where it strained — pagination and flattened source:** The required numeric `pages` field cannot be recovered from the supplied one-line raw text; it required checking the official PDF. The flat source erases line and page boundaries while retaining textual section and subsection markers, so downstream extraction must reconstruct the hierarchy of the 51-name cohort from markers embedded in one continuous stream.

## 119s1082is
# Stress extraction findings — S. 1082

## Bill type and size

- S. 1082 is an ordinary introduced Senate bill, not a symbolic measure, joint resolution, or appropriations bill. The official introduced version is eight printed pages; the supplied flattened raw text is 7,304 bytes and 1,181 words.
- The bill has four sections: a short title and three substantive provisions. It amends the Social Security Act by reference, expands an administrative verification program, creates a separate resources-eligibility rule, and directs future tracking, reporting, and discretionary enforcement.

## What the frozen contract handled well

- Three provision records preserve the legally important separation between Section 2's asset-verification program, Section 3's resources-eligibility test, and Section 4's measurement and enforcement machinery.
- Indexed goal/stance matrices show which metrics actually bear on which statutory objective. They prevent a broad Medicaid measure from being presented as proof of a narrower asset-verification result.
- The execution, participation, and outcome layers distinguish system adoption, checks or eligibility processing, and claimed federal savings.
- Empty `series_hint` values honestly record that no current registry series directly resolves the bill-created asset-check, resource-denial, attributed-savings, or corrective-action measures. Broad Medicaid enrollment and spending series would be real but too confounded for these fields.
- Free-text conditionals can preserve one-sided enactment-created observations and state that the non-enactment value is missing, not zero.

## Where the contract strained

- The raw source is a single line whose headings are rendered as `2.`, `3.`, and `4.` rather than line-start `SEC.` headings. The site's section slicer is likely to miss them even though the analytical `provisions` split is clear.
- Amendment by reference is not first-class. The raw text does not reproduce Social Security Act §§1940, 1902(e), or 1613, and the schema has no field for the incorporated-law baseline, interpretive confidence, or the exact legal text needed to validate effects.
- Naming invites a substantive mistake: Section 2's heading says “asset test,” but its operative clauses expand asset verification; Section 3 separately creates the resources-eligibility test. A flat provision title cannot encode that legal relationship mechanically.
- Timing is relative and jurisdiction-specific. Section 2 defaults to enactment plus one year, may be delayed up to 365 days for a State, Section 3 starts at enactment plus two years, Section 4 has another two-year deadline, and corrective action uses chained 90-day clocks. String conditionals cannot represent this schedule or the State-specific alignment of Sections 2 and 3.
- The default one-year gap between expanded verification and the resource test is a cross-provision state transition, not a property of either record alone. The schema has no dependency or sequencing edge between provisions.
- “Or such amount as the State shall establish” creates many State policy variants under one enactment condition. The schema cannot express heterogeneous treatment thresholds or compare them without multiplying provisions or conditionals.
- The continuous-eligibility clause is a safeguard on the reach and timing of a rule, not naturally a goal, effect, barrier, or conditional. Treating it as a goal preserves its stance relationships but loses its legal role as a constraint.
- Section 4 creates its own observations. An empty `series_hint` cannot distinguish a temporary “mandated but not yet specified” series from a permanent no-series gap, and the metric shape has no readiness, publication-duty, denominator, cadence, or expected-availability fields.
- Reporting language resists resolution. Reports concern a year, arrive through State-specific triennial PERM reviews, then refer to information during “such month”; paragraph (A)'s punctuation does not cleanly enumerate fields or denominators. The contract has no structured place for textual ambiguity or alternate readings.
- “Savings ... associated with” lacks a defined counterfactual, attribution method, treatment of administrative cost, or publication duty. Category, layer, and stance can classify the intended metric but cannot encode its estimand or causal-identification weakness.
- Stances express direction against goals but not measurement quality, confounding, uncertain direction, or a metric that improves transparency while exposing an adverse access effect.
- The bill contains no express appropriation. That absence can be noted as an implementation barrier, but the contract has no dedicated authorization, appropriation, funding-source, or administrative-cost field.
- The requested top-level `sourceLimits` note carries the extraction's central honesty qualification, but the current site type and bill page do not represent or render that field. Repeating narrower limits in provision context is necessary for visible disclosure.

## 119hr1eh (attempt 1 — DIED MID-DRAFT)
Scale finding: 995k-char mega-bill lane completed structural mapping (planned 13 coarse title-level entries, splitting heterogeneous Titles IV and XI) but the process ended before writing any JSON. Harness lesson: mega-bill lanes must WRITE the coarse artifact first, then enrich — a late death loses everything. Retrying with write-early brief.

## 119hjres42ih
# Stress-test findings: H.J. Res. 42

## Bill type and size

H.J. Res. 42 is a House joint resolution using the congressional-disapproval structure in chapter 8 of title 5. The matching official introduced-version PDF is two pages, while the supplied cache is a 1,463-byte, 210-word, single-line text extraction. The measure has one 49-word operative clause and no numbered sections, findings, appropriations, deadlines, reporting duties, quantitative targets, or replacement policy.

The cached source records submission by Mr. Clyde on February 12, 2025 and referral to the House Committee on Energy and Commerce. Unlike the closest stress-test precedent, this resolution did not remain merely introduced: Congress.gov records that it became Public Law 119-8 on May 9, 2025. The extraction distinguishes the introduced version being analyzed from the measure's later enacted disposition.

## What the contract handled well

- A one-element `provisions` array represents the entire measure without artificial section splitting.
- `quote` and `context` preserve the exact cited rule, Federal Register reference, procedural posture, narrow legal mechanism, and later disposition.
- The arrays permit one source-grounded goal and one source-grounded effect while leaving `barriers`, `metrics`, and `conditionals` empty.
- Empty metric and conditional arrays make it possible to record zero forecastable outcomes without inventing a Department of Energy series identifier or a tautological enactment conditional.
- The free-text status and context fields can at least describe both the analyzed introduced text and the enacted measure.

## Where the contract strained

- The frozen JSON shape has no typed, rendered `sourceLimits` or honesty field. The note therefore lives in `context`, where the current UI can render it, rather than in an inert extra key.
- `pages` requires a number, but the supplied flattened text has no page boundaries. The value `2` required checking the matching official PDF; it cannot be recovered from the raw text alone.
- The flat extraction omits the standard resolving formula present in the PDF. This does not change the sole operative clause, but it shows that the cached text is normalized rather than page-verbatim.
- One free-text `status` field must carry two different facts: the version analyzed is the introduced-in-House text, while the measure later became Public Law 119-8. The contract has no separate source-version and current-disposition fields.
- `goals` invites motive imputation, yet this resolution has no findings, purpose section, or short title. The sole goal therefore restates the operative objective and does not infer energy, consumer, industry, or sponsor motives.
- `effects` does not distinguish a deterministic legal consequence from an empirical likely effect, nor a proposed consequence from one already realized through enactment. Those distinctions have to be carried in prose.
- The `barriers.actor` shape assumes an implementation actor. The introduced text's only material contingency was legislative enactment, which has occurred, and the clause specifies no separate post-enactment implementation machinery, so forcing a barrier row would misclassify procedure as implementation.
- The metric taxonomy and stance matrix assume an observable outcome. The binary legal status of the cited rule is observable and already resolved, but it follows directly from the enacted clause and is not a useful recurring forecast series. The artifact therefore has no metric rows and, vacuously, no stance matrix.
- A conditional such as `P(rule has no force or effect | resolution enacted)` would be tautological rather than empirical, so `conditionals` is empty.
- The resolution incorporates the Department of Energy rule and chapter 8 of title 5 by reference, but the contract has no dedicated field for incorporated instruments and their provenance. The supplied bill text cannot support claims about the rule's requirements, covered products, effective dates, enforcement, energy effects, costs, successor-rule constraints, or replacement baseline.
- The absence of appropriations is part of this measure's minimal structure, not a delivery barrier. The contract offers no dedicated way to distinguish “no appropriation needed for this self-executing legal effect” from “an implementation mandate lacks funding.”
- The measure has no short title or numbered substantive section, so `name`, `title`, and `heading` necessarily repeat or descriptively compress the official long title. A section-based UI helper also cannot key the unnumbered clause to a `Section N` or `§N` marker.

The result is intentionally small: one provision, one express goal, one enacted legal effect, zero implementation barriers, zero forecastable metrics, zero series hints, and zero conditionals.

## 119hr1eh (mega, attempt 2 — write-early brief SUCCEEDED)
# Stress-test findings: `stress-119hr1eh`

## Bill type and size

- The source is H.R. 1 of the 119th Congress, version code `EH`: the House-engrossed reconciliation bill passed on May 22, 2025. It is not the later Senate, enrolled, or Public Law 119-21 text.
- This is a mega-bill rather than an ordinary single-program bill: 995,016 Unicode characters, about 159,308 whitespace-delimited words, 1,116 PDF pages, 331 numbered sections, and 11 top-level committee titles.
- The source has no formal divisions. Its committee-jurisdiction titles vary dramatically in size: Title V has five sections, while Title XI has 114 sections and about 35.6 percent of the cached text. Titles IV and XI together account for about 54 percent of the cached text.
- The cached text is one physical line with no page markers. Section numbers are the only reasonably stable local anchors; line citations are impossible and character offsets are encoding-sensitive.
- The extraction uses 13 coarse provision entries: one for each title, except that heterogeneous Titles IV and XI are each split into two coherent blocks. Five high-impact blocks received close reads, small Titles V, VI, IX, and X were read in full, and Titles II and VIII received selected-section reads. The JSON `sourceLimits` field records the exact coverage and omitted section ranges.

## What the frozen contract handled well

- The `bill` block can identify the exact legislative version and source URL, which is essential here because later versions share the short title but differ materially.
- `provisions[]` can be used at title or coherent-block granularity instead of forcing 331 section objects. Splitting only Titles IV and XI kept the artifact reviewable while preserving the largest policy seams.
- Separate `goals`, `effects`, and `barriers` arrays helped distinguish an appropriation or legal authority from delivery and outcome. That mattered repeatedly: budget authority is not an obligation, an award is not a completed asset, and a lease offering is not production.
- The `category` and `layer` fields allow implementation, participation, intended outcomes, and unintended burdens to coexist without pretending that every observable is an ultimate outcome.
- Empty `series_hint` values made honest sparse registry coverage possible. Only exact concepts verified in the current docket were populated; the artifact did not manufacture dotted identifiers for plausible but unregistered CMS, Education, IRS, DHS, Interior, or Treasury measures.
- Empty `metrics` and `conditionals` arrays worked for the two small titles where the reviewed text did not support a clean, recurring, automatically resolvable series. The contract therefore did not force false precision everywhere.
- A top-level `sourceLimits` note can preserve the coverage map and version warning without inflating every provision's prose.

## Where the contract strained

### Provision granularity explodes or conceals heterogeneity

Section-level extraction would create 331 provision entries and thousands of stance cells. Title-level extraction is manageable, but committee jurisdiction is not policy coherence. Energy appears in Titles I, IV, VIII, and XI; immigration and border policy appear in Titles VI, VII, and XI; health policy appears in Titles IV and XI. Even after splitting Titles IV and XI, several entries still combine mechanisms that do not share a causal chain.

The schema has no structural path such as `title > subtitle > part > section`, no section-range array, and no source-span field. `title`, `heading`, and `context` must carry all three jobs. A single `quote` also cannot fairly anchor a title spanning tens or hundreds of thousands of characters.

### Coverage and confidence are prose-only

`bill.analyzed` is too small to distinguish close read, complete small-title read, selected-section read, heading-only skim, and not reached. The additive `sourceLimits` prose can say this honestly, but it is not typed, validated, or rendered by the current bill UI. There is also no per-claim confidence, evidence anchor, or review status, so the artifact cannot mechanically distinguish a verified statutory effect from an analyst inference.

No top-level title was wholly omitted in this pass, but many sections were not substantively read. The frozen contract has no native way to make that partialness queryable.

### Metrics repeat without a deduplication layer

The same administrative families recur across titles: obligations and outlays for appropriations, enrollment and disenrollment for benefit restrictions, receipts for tax changes, and staffing or throughput for agency expansions. Each provision embeds its own metric text and stance matrix. There is no canonical metric reference, shared definition, vintage policy, or bill-wide deduplication key.

This becomes especially awkward for Titles VI and VII, which both affect border and immigration operations, and for Titles IV and XI, which both affect health eligibility and financing. Repeating a metric risks drift; sharing one is not expressible.

`series_hint: ""` also collapses distinct states: an official series exists but is not registered, no recurring official series exists, a possible source was not checked, or the available aggregate is too confounded to use. Those judgments can only be buried in `kind` or `text`.

### Stance matrices become unwieldy and under-expressive

At title scale, each metric needs a row for every broad goal, producing matrices dominated by `orthogonal`. At section scale, the matrix count would explode. The three stance values cannot express expected direction, causal ambiguity, a ceiling rather than a target, heterogeneous subgroup effects, timing, or a metric that serves one interpretation of a goal while opposing another.

Title III is a concrete failure mode: Pell restrictions and Workforce Pell can move aggregate recipients in opposite directions. Title XI combines tax reductions, offsets, clean-energy credit termination, SALT changes, and a debt-limit increase. A single goal-by-metric stance label cannot encode those offsetting paths.

### Appropriations need a richer delivery chain

The bill repeatedly moves through `budget authority → obligation → outlay → procured input → delivered output → public outcome`. The single `layer` value captures only one point in that chain, and `effects[]` are unstructured prose. The contract cannot record an appropriation account, period of availability, rescission baseline, required quantity, milestone, or the distinction between a grant, loan face value, loan subsidy cost, and purchase commitment.

Rescissions of an “unobligated balance” are especially difficult: the amount depends on a time-specific balance not stated in the bill. Treating the statutory phrase as a fixed dollar outcome would be wrong, but the schema has no baseline-date field.

### Effective dates and conditional forecasts do not compose

This text contains immediate rules, fiscal-year appropriations available through 2029, changes starting in 2026 or 2028, transition cohorts, grandfather periods, temporary deductions, later sunsets, and a 15-year lease-sale schedule. There is no structured effective-date or transition field, so dates live in prose.

A title-level `conditionals[]` string can name an enacted-versus-baseline comparison, but it cannot bind hundreds of mechanisms, dates, cohorts, and resolution sources without becoming ambiguous. Cross-title interactions are also invisible. For example, Medicaid eligibility changes and tax-credit eligibility changes sit in different titles but affect overlapping coverage outcomes.

### Naming and resolution provenance are fragile

The short title survived into later legislation, but this artifact analyzes only `119hr1eh`. A free-text `status` plus URL conveys that to a reader, yet the contract lacks structured Congress, chamber, bill number, version code, passage date, or relationship to later versions. That makes accidental substitution of enacted values a real risk.

The one-line raw cache also exposes a source-resolution problem: quotes can be text-matched, but page and line provenance cannot be reconstructed from the cached artifact. A section-aware source anchor would be more durable than relying on headings and normalized substring matching.

### Stakeholder conflict and causal limits have no native fields

State agencies, beneficiaries, providers, regulated firms, contractors, taxpayers, and Federal administrators often face opposing effects. `barriers[]` captures implementation burden but not support, opposition, incidence, or distribution. Likewise, the contract has no place for the distinction between a forecastable administrative count and a causal policy impact. That limitation is acute in an omnibus reconciliation bill, where almost every aggregate outcome is affected by several simultaneous provisions and external conditions.

## Bottom line

The frozen contract can hold an honest, coarse coverage map of this mega-bill, but only by leaning heavily on prose and leaving most series hints empty. It works best for a coherent section or small title. At H.R. 1 scale, the missing structural hierarchy, coverage status, shared metric registry references, effective dates, appropriation stages, and causal-confidence fields become first-order limitations rather than polish issues.

## Attempt 2 completion note

The scale-first workflow materially improved failure tolerance. A valid 13-provision checkpoint was written from the table of contents before any deepening, with every metric and conditional array present but empty. The interrupted first attempt's richer draft was then recoverable from the local run trace, after which the agriculture, health, immigration, and tax/debt blocks were checked and updated one at a time. At every checkpoint, the on-disk artifact remained parseable JSON.

The finished artifact has 13 provision groups, 37 goals, 37 effects, 34 barriers, 36 conceptual metrics, and 36 conditionals. Only three metrics carry nonempty `series_hint` values, and all three exactly match concepts already present in the local docket. Titles V and IX retain empty metrics and conditionals because the reviewed text did not justify a clean recurring official series; this is an honest absence, not an extraction omission disguised with a proxy.

The contract handled progressive enrichment well. Empty arrays made the coarse checkpoint valid, goal-indexed stance matrices remained mechanically checkable after goals changed, and title splitting kept the largest heterogeneous committee titles within a reviewable 13-entry artifact. The `sourceLimits` note also provided a place to distinguish close reads, selected reads, heading-only coverage, and unresolved metrics.

The second pass confirmed the principal strain: `sourceLimits` is additive prose rather than a typed, validated, or rendered coverage map. A future extractor cannot query which sections were close-read, which claims rest only on headings, or which official products were considered and rejected. Likewise, `series_hint: ""` still conflates “no official series,” “official series not in the docket,” “candidate not verified,” and “aggregate too confounded to use.”

The revised Title XI split exposed another naming problem. Subtitles A–B form a household-and-business tax block, while Subtitles C–D combine clean-energy offsets, immigration-related tax rules, Medicare improper-payment administration, tax filing and enforcement, and the debt limit. Keeping the provision count near 13 requires grouping mechanisms that do not share goals, actors, dates, or resolution sources; splitting them coherently would exceed the requested title-scale granularity.

Finally, exact statutory numbers are often not forecast targets. The 5/15/20/25-percent SNAP State shares are triggered by measured error bands; the 75-percent Exchange verification floor is a minimum; $45 billion for detention is budget authority; 10,000 ICE hires is a statutory minimum over several years; and the $4 trillion debt-limit increase is borrowing headroom rather than spending. The frozen fields can explain these distinctions in prose, but cannot encode ceiling, floor, trigger, appropriation, obligation, output, and outcome as separate machine-readable relationships.

One count from the interrupted mapping needed correction: exact enumeration of distinct table-of-contents `Sec.` entries yields 334, including §§1–2, rather than the earlier 331. Title XI contains 115 listed entries when §110000 is included, rather than 114. This is itself a scale warning: body-text searches overcount because inserted statutes and cross-references also contain section markers, while ad hoc structural parsers can undercount when spacing or Unicode punctuation varies.

## 119hr8058ih
# Stress extraction findings — H.R. 8058 (IH)

## Bill type and size

H.R. 8058 is a short standalone direct-appropriation and contingency-fund bill, not a symbolic measure or resolution. The official introduced-version PDF is four pages. The flattened cache is 515 words and contains two sections: a short title and one substantive provision, §2, divided into seven subsections. I kept §2(a)–(g) together because establishment, permitted use, appropriation, deposit, sweep, reporting, and committee definition form one linked reserve-fund mechanism.

## What the contract handled well

- A single provision can preserve the linked mechanism without manufacturing separate policy programs from ministerial subsections.
- Separate goals, effects, and barriers capture the crucial distinctions between appropriating, depositing, permitting a draw, spending, returning a balance, rescinding it, and reporting afterward.
- Sparse arrays allow an honest result. This bill has zero forecastable metrics, zero empirical conditionals, no stance matrices, and no series hints; the contract does not force fake time series into those fields.
- The free-text context and source-limits note can preserve the operative modal verbs: Treasury **shall** deposit, the Director **may** use, and the Director **shall** transfer and report.
- Effects can state negative scope explicitly: the reserve is limited to specified protective expenses and at most 30 days, and it neither covers all Secret Service operations nor guarantees continuity.

## WHERE IT STRAINED

- `pages` cannot be recovered from the one-line raw cache. Populating the mandatory bill metadata required checking the separate official PDF.
- The bill has no findings or express outcome statement. Its best-supported “goals” are inferred from legal mechanics and guardrails, so the goals field blurs political purpose, permitted use, and compliance design.
- No structured field captures the nested temporal logic: enactment creates the fund; a Secret Service appropriations lapse activates discretionary use; the use window ends at the earlier of lapse end or day 30; a December 31, 2026 balance snapshot feeds a January 31, 2027 transfer and rescission; and the report is due 30 days after actual compliance. Those gates and clocks survive only in prose.
- The schema has no dedicated representation for appropriation stage. A fixed $106 million appropriation is neither an outcome metric nor proof of deposit, obligation, outlay, protective activity, or service continuity.
- The bill rescinds qualifying unused amounts but does not expressly terminate the named fund. The contract cannot cleanly distinguish an existing but empty legal fund from an expired or abolished program.
- The year-end structure is genuinely awkward: the text does not reconcile a lapse/use window spanning December 31 with the balance snapshot and later sweep, and fixed dates can become compressed or stale if enactment occurs late. `barriers` can flag this but cannot encode competing readings.
- The report is a one-off submission to committees, with no public-release command, template, fixed fields, or independent evidence rule. Treating it as a metric would overstate resolvability; omitting it from `metrics` means a legally important but non-public compliance event is represented only as an effect and barrier.
- Stance matrices attach only to metrics. With zero honest metrics, the contract cannot directly relate the nonforecastable appropriation, sweep, and reporting duties to the inferred goals.
- String-only conditionals would either restate tautological legal effects or imply public observability that the bill does not provide. They cannot formally express “missing, not zero” when enactment does not create a published observation.

## Judgment and honesty note

The artifact treats $106 million as a statutory input and maximum potential draw, not as forecast spending. It does not infer a shutdown, its duration, the amount needed or used, the number of protected people or employees, or any protection-performance effect. It also does not invent a Treasury, Secret Service, USAspending, or Thesis registry identifier. Because the only prospective observations are one-time administrative events and the bill names no required public resolution record, `metrics` and `conditionals` are empty.

## 119s3022is
# Stress-test findings: S. 3022 IS

## Bill type and size

S. 3022 IS is a short, ordinary reauthorization bill rather than a symbolic measure or joint resolution. The official introduced-version PDF is two pages. The supplied raw extraction is 1,048 bytes and 176 words including its metadata header, contains two sections, and has one substantive provision: §2 makes the same year substitution and grammatical correction in two cross-referenced authorization paragraphs.

The extraction therefore uses one provision, one narrowly stated legal goal, three effects, one downstream funding/administration barrier, and zero forecastable metrics or conditionals. It does not split the cross-reference into artificial program provisions or treat a new authorization end date as funding or an outcome target.

## What the contract handled well

- A single provision cleanly preserves the scale of the bill. The schema does not force section-count parity or a minimum number of goals, metrics, or conditionals.
- Separate `mechanism` and `text` fields distinguish the substantive date substitution, the technical insertion of “in,” and the authorization-versus-appropriation limit.
- Empty `metrics` and `conditionals` arrays allow an honest zero-forecastability judgment without inventing a recurring series, a resolution rule, or a `series_hint`.
- The free-text `sourceLimits` note can disclose that the supplied text is cross-reference-only and cannot by itself establish program details, appropriations, awards, or environmental results.
- The `barriers` actor/text pair can identify the separate-appropriations and administration gates without misdescribing the authorization as money already provided.

## Where it strained

- Cross-reference drafting does not fit a single-source artifact well. The raw bill does not reproduce §4282(g)(1) and (2), while the schema has no `incorporatedSources` array or claim-level citations. A single `sourceUrl` cannot simultaneously identify the exact analyzed bill version, the incorporated statute, the current bill history, and any budget estimate.
- `status` is one flat string, so it cannot cleanly distinguish the status of the analyzed introduced version from the bill's later, still-unenacted disposition. The artifact has to carry that distinction across `status`, `analyzed`, and prose.
- Authorization, appropriation, obligation, grant award, program output, and environmental outcome are distinct causal gates. Flat `effects` text can explain that chain, but the contract cannot represent it structurally or attach a confidence judgment to each link.
- The same amendatory instruction contains a material date change and a purely grammatical correction. Treating the correction as a policy goal would inflate it, but omitting it from effects would lose a real legal edit; the schema has no technical-amendment field.
- `barriers` is awkward for a direct legal goal. Once enacted, the authorization-date change itself has no implementation barrier; separate appropriations and EPA administration constrain only later program activity. The field cannot mark that causal distance.
- With `metrics: []`, there is correctly no stance matrix, but the schema has no structured `forecastability: none` or `noMetricReason` field. The zero is legible only through prose.
- `conditionals` is an array of strings, with no structured way to distinguish a legislative contingency from an empirical forecast or to record why no mechanically resolvable conditional exists.
- The additive top-level `sourceLimits` field is not declared on the site's current `BillArtifact` interface or rendered on the bill page. The core honesty judgment therefore also has to be summarized in provision context to remain visible to site users.

## 119sjres74is
# Stress-test findings: S.J. Res. 74

## Bill type and size

S.J. Res. 74 is an introduced Senate joint resolution using the congressional-disapproval structure in chapter 8 of title 5. The matching official introduced-version PDF is two pages, while the supplied cache is a 1,344-byte, 220-word, single-line text extraction. The measure has one 51-word operative clause and no numbered sections, findings, appropriations, deadlines, reporting duties, quantitative targets, or replacement policy.

The source records introduction by Mr. Whitehouse on August 1, 2025, two readings, and referral to the Senate Committee on Commerce, Science, and Transportation. The extraction treats the stated no-force-or-effect consequence as contingent on enactment, not as a result already achieved by the introduced text.

## What the contract handled well

- A one-element `provisions` array represents the entire measure without artificial section splitting.
- `quote` and `context` preserve the exact cited rule, Federal Register reference, procedural posture, and narrow legal mechanism.
- The arrays permit one source-grounded goal and one source-grounded effect while leaving `barriers`, `metrics`, and `conditionals` empty.
- Empty metric and conditional arrays make it possible to record zero forecastable outcomes without inventing a PHMSA series identifier or a tautological enactment conditional.
- The free-text status and context fields can distinguish introduced text from enacted law.

## Where the contract strained

- The frozen JSON shape has no dedicated, rendered `sourceLimits` or honesty field. The note therefore lives in `context`, where the current UI can display it, rather than in an inert extra key.
- `pages` requires a number, but the supplied flattened text has no page boundaries. The value `2` depends on the matching official PDF and cannot be recovered from the raw text alone.
- `goals` invites motive imputation, yet this resolution has no findings, purpose section, or short title. The sole goal therefore restates the operative objective and does not infer a sponsor motive or a broader geographic-naming policy.
- `effects` does not distinguish a deterministic legal consequence conditional on enactment from an empirical likely effect. That distinction has to be carried in prose.
- The `barriers.actor` shape assumes an implementation actor. Here the only material contingency is legislative enactment, and the text specifies no post-enactment program or implementation machinery, so forcing a barrier row would misclassify legislative procedure as implementation.
- The metric taxonomy and stance matrix assume an observable outcome. The cited rule’s legal status is observable but categorical; conditional on enactment, it follows directly from the clause and is not a useful recurring forecast series. The artifact therefore has no metric rows and, vacuously, no stance matrix.
- A conditional such as `P(the cited rule has no force or effect | S.J. Res. 74 enacted)` would be tautological rather than empirical, so `conditionals` is empty.
- The resolution incorporates the PHMSA rule and chapter 8 of title 5 by reference, but the contract has no dedicated field for incorporated instruments and their provenance. The supplied bill text cannot support claims about the affected regulatory wording, the terminology that would apply after disapproval, successor-rule constraints, or any government-wide naming effect.
- The rule title calls its change “Editorial,” but the contract has no field that cleanly separates the resolution’s expressive naming stance from its narrow legal effect on one cited rule. Treating pipeline incidents, safety outcomes, compliance costs, agency workload, or counts of name usage as bill metrics would overstate the causal content of the text.
- The absence of an appropriation is part of this measure’s self-contained legal structure, not evidence of an unfunded implementation mandate. The contract has no explicit way to represent that distinction.
- The measure has no short title or numbered substantive section, so `name`, `title`, and `heading` necessarily repeat or descriptively compress the official long title. A section-oriented text viewer also has no `Section N` or `§N` anchor for the operative clause.

The result is intentionally small: one provision, one express legal goal, one enactment-contingent legal effect, zero implementation barriers, zero forecastable metrics, zero series hints, zero stance rows, and zero empirical conditionals.

## 119hjres78ih
## stress-119hjres78ih — H.J. Res. 78

- **Bill type/size:** This is a House joint resolution of congressional disapproval under chapter 8 of title 5, not a ceremonial or symbolic resolution. The official introduced-version PDF is two pages, while the cached flattened extraction is one physical line and 1,524 bytes / 243 words including metadata; it contains one 54-word operative sentence. The measure has no short title, appropriation, program, reporting mandate, quantitative target, or implementation timetable.
- **What the contract handled well:** The one-provision structure preserves the exact agency, rule title, Federal Register citation and date, and binary legal effect without padding the analysis. Separate quote and context fields distinguish the text-grounded result—“no force or effect”—from downstream consequences that the source does not establish. Empty arrays let the extraction remain honest when no barriers, metrics, or empirical conditionals are supported.
- **Where it strained:** `bill.name` assumes a conventional title, but this measure has only a long official purpose clause. `goals` and `effects` nearly collapse into the same operative legal act, and the schema cannot mark a goal as literal rather than analyst-imputed. The program-oriented `barriers`, `metrics`, `conditionals`, and metric `layer` fields invite invented implementation burdens or biological, water-use, agricultural, and economic outcomes. The only direct result is a one-time categorical legal state, not a recurring quantitative series; a conditional on enactment would merely restate the law. The stance matrix has nothing to attach to when `metrics` is correctly empty. The schema also has no structured fields for the resolution type, target agency and rule, Federal Register citation, incorporated external law, or the regulatory baseline that would follow disapproval; only unstructured free-text fields such as `sourceLimits` or provision `context` can carry those absences. No `series_hint` is supplied because neither the raw text nor the registry establishes a defensible series.
- **Ambiguous judgments:** “Express congressional disapproval” and “make the rule have no force or effect” were treated as one goal rather than two redundant goals. Legislative enactment was treated as a precondition, not an implementation barrier. No conditional was added because `P(rule has no force or effect | resolution enacted)` is statutory and tautological rather than an empirical forecast. The raw extraction does not establish pagination or current status, so those metadata values required separate official-source checks; it also incorporates chapter 8 of title 5 and the cited rule without reproducing either, so broader legal consequences and the replacement regulatory regime were not inferred.

## 119hjres122ih
## stress-119hjres122ih — H.J. Res. 122

### Bill type and size

This is an introduced House joint resolution proposing a constitutional amendment, not an ordinary bill that creates a statutory program. The supplied raw extraction is 2,865 bytes and 457 words. Its substantive core is one proposed article with a seven-year ratification condition and four numbered clauses; the separately checked exact-version PDF is three pages, much of which is header and sponsor material. The resolution contains no appropriation, administrator, reporting duty, implementation schedule, or quantitative policy target.

### What the contract handled well

- One `provisions[]` entry can keep the proposed article and its press safeguard together as the single ratification unit instead of inflating four short clauses into four programs.
- `goals`, `effects`, and `barriers` distinguish the text's permissions, their ratification contingency, later implementation needs, and the express press safeguard.
- Empty `metrics` and `conditionals` arrays honestly represent the absence of a forecast-ready outcome series; the contract does not force an invented `series_hint`.
- The free-text `sourceLimits` note can disclose missing source structure and explain why a categorical legal milestone was not promoted into an empirical outcome metric.

### WHERE IT STRAINED

- The constitutional-amendment lifecycle is a chain of legal gates: concurrence by two-thirds of each House and submission, ratification by three-fourths of State legislatures within a clock that starts only on submission, and then optional implementing legislation. A flat `status` string cannot model those phases, and free-text `conditionals` cannot structurally encode or validate nested prerequisites or a contingent resolution date.
- The resolution grants powers; it does not mandate an election-money rule, create public financing, prohibit corporate spending, or fund anything. The schema has no dedicated distinction between constitutional authority, self-executing law, later discretionary legislation, and a later appropriation.
- Clause 4 is a savings clause, not an affirmative program goal. Putting it in `goals` preserves its importance but loses the difference between an objective and a constraint or carveout.
- A one-time ratification state is categorical rather than a recurring outcome series. With `metrics: []`, the nested stance-matrix design has nowhere to express relationships between the four goals and the legal effects.
- The integrated article has four clauses. Splitting them would inflate the provision count, while grouping them makes one `quote` and one heading carry authority grants, an entity distinction, and a press safeguard at once.
- `barriers` conflates a constitutional condition precedent with ordinary implementation friction; ratification is not merely an actor burden.
- The long official title has no short title, so `name`, `title`, and `heading` cannot avoid some awkward repetition.
- The required numeric `pages` value is not present in the raw extraction and had to come from the exact-version PDF. The flattened raw also omits the resolving formula and page/line structure, and its `1.`–`4.` clauses do not match the UI's ordinary `SEC.` section-heading pattern.
- The explicitly requested top-level `sourceLimits` note is absent from the current TypeScript artifact interface and is not rendered or validated, so the most important honesty disclosure can be silently ignored by the site.

## 119hr608ih
# Stress-test findings: H.R. 608 IH

## Bill type and size

H.R. 608 is an ordinary introduced House bill, not a symbolic measure or an appropriation. The authenticated introduced-in-House PDF is 16 pages. The supplied raw extraction is 15,470 bytes and 2,332 whitespace-delimited words flattened onto one line. Section 1 is only the short title; Section 2 is one integrated substantive Medicaid package that adds a local expansion demonstration, State safeguards, Federal administration and reporting rules, and an enrollment-linked State administrative-match provision.

The artifact uses three provision groups to keep the core demonstration, the safeguards/administration block, and the separate §2(b) payment amendment readable. That grouping is analytical rather than a claim that the bill contains three independent programs.

## What the contract handled well

- `goals`, `effects`, and `barriers` separated the bill's literal coverage pathway from implementation mechanisms and actor-specific burdens without requiring a speculative estimate of coverage or cost.
- The `category` and `layer` fields distinguished agency execution, locality or beneficiary participation, and downstream continuity outcomes.
- Complete stance matrices made the analysis say which goal each metric actually bears on. They prevented the required uncompensated-care report item from being mislabeled as evidence that the bill expressly promises to reduce uncompensated care.
- Empty `series_hint` values worked as an honest refusal to mint bill-specific identifiers for new administrative records and a one-time report. The artifact has nine conceptual metrics but zero claimed Thesis mappings or currently registry-ready recurring series.
- `conditionals` could record potentially checkable missed-deadline and transition questions while stating the enactment, application, project-start, or State-expansion trigger still needed to establish a clock.
- `sourceLimits` provided one place to disclose that the raw text is flattened, incorporated statutes are absent, no fiscal or enrollment baseline exists, and apparent drafting defects were preserved rather than repaired.

## Where the contract strained

- The bill is one nested statutory program, but `provisions[]` is flat. Any split either produces an unwieldy single provision or analytically separates clauses whose operation depends on one another. A structured parent/child or cross-reference field would express this better.
- There is no field for legal-text confidence, drafting defects, or competing interpretations. The source says “section subsection,” points paragraph (1) to paragraph (2) even though paragraph (3) defines qualifying subdivisions, points the matching rate to subparagraph (B) although it is in (C), invokes an unclear “clause (ii),” ends the withholding period with “during a calendar,” and uses §1115(g) references for a demonstration created in §1902(uu). Those are not ordinary actor barriers, so placing them under `barriers` requires the artificial actor label “Statutory implementers and reviewers.”
- Numeric schedules have no structured representation. The core Federal match changes by participation year and rural-inclusive status, while §2(b) adds five points “for every 100,000” enrollees without a rounding rule or ceiling. Encoding both only in prose makes later comparison and validation difficult.
- Triggered clocks do not fit fixed-resolution forecasting cleanly. The regulation deadline depends on enactment; application decisions depend on receipt; the report depends on an undefined first demonstration date; automatic enrollment depends on a participating State later expanding. A conditional string can explain this chain but cannot encode its event dependencies or evidence requirements.
- A project can be one locality or a partnership of any number of localities. The 100-project cap therefore does not define a stable locality or population denominator, and the schema has no nested State → project → partnership → locality structure.
- One-time statutory reports sit awkwardly beside recurring series. A blank `series_hint` can mean no series exists, an official product will exist only after enactment, the release is not required to be public, or a plausible broad proxy was rejected. The contract cannot distinguish those reasons mechanically.
- The stance enum cannot express mixed or state-dependent direction. More Federal withholding can mean stronger enforcement and more underlying State interference. State expansion can reduce local-demonstration enrollment because the project ends while simultaneously advancing coverage continuity through automatic State enrollment.
- “The amount of uncompensated care costs for State Medicaid plans” is not a defined estimand. The metric fields cannot record an unknown denominator, counterfactual, attribution method, or observation window except as prose.
- `sourceLimits` is useful in the frozen JSON artifact but is not currently part of the site's typed/rendered bill interface. The most important legal ambiguities therefore also had to be repeated in provision context so they would not disappear from a rendered analysis.

Overall, the contract captured a substantive but compact bill without inventing outcomes or identifiers. Its hardest failure mode here was not small size; it was legal and temporal indeterminacy inside an otherwise highly quantitative program design.

## 119hjres39ih
# Stress extraction findings — H.J. Res. 39

## Bill type / size

This is an introduced Congressional Review Act joint resolution, not a conventional multi-section bill. The supplied cache is a flattened one-line source of 1,168 bytes and 180 words; the matching exact-version official PDF is two pages. The measure has one unnumbered operative clause that disapproves one identified FTC rule and says it shall have no force or effect.

The honest extraction is correspondingly small: one provision, one literal goal, one enactment-contingent legal effect, and no barriers, metrics, conditionals, series hints, or stance matrices.

## What the contract handled well

- The contract permits a single provision and empty arrays, so it did not force a two-page resolution into an artificial multi-provision analysis.
- The quote and context fields cleanly separate the operative language from metadata and the enactment contingency.
- The effects mechanism can label the legal consequence as conditional on enactment rather than imply that introduction already nullified the rule.
- The honesty note can preserve why no downstream FTC, merger, burden, cost, or competition claims were extracted from a source that merely cites the rule.

## WHERE IT STRAINED

- The resolution's goal and effect nearly collapse into the same proposition: Congress's stated goal is to negate the rule, and the only specified effect is that the rule has no force or effect. The schema cannot mark this as an intentionally literal near-duplicate.
- Enactment is a necessary precondition, but it does not fit the actor-and-text `barriers` model, which reads as an implementation-burden field. Recording Congress or the President as a “barrier” would overinterpret ordinary bicameralism and presentment.
- The only resolvable fact created by the clause is a categorical, one-time legal state. The metrics shape is oriented toward empirical series, and a conditional such as `P(rule has no force or effect | resolution enacted)` would be tautological. Empty metrics and conditionals are more honest, but the arrays alone cannot explain that judgment.
- Stances attach only to metrics. With zero defensible metrics, the schema has no place to state that the direct legal effect serves the sole goal; adding a dummy metric solely to carry a stance would inflate the extraction.
- The cited FTC rule is identified only by title and citation and is not reproduced. The contract can record that source gap, but it cannot express the rule's unknown internal mechanisms in structured form without importing another source. Claims about filings, waiting periods, merger behavior, competition, compliance costs, or agency workload would therefore exceed this extraction.
- The raw cache has no page boundaries or metadata sidecar. Page count and current legislative status required separately checked official metadata, but the bill block has no field-level provenance slots to distinguish facts drawn from the supplied text from facts drawn from the matching PDF and actions page.
- The additive top-level `sourceLimits` note carries the central non-inference judgment, but that field is outside the typed bill interface and is not rendered by the current bill page. Repeating a shorter honesty note in `context` preserves it for readers at the cost of duplication.

## 119hr2781ih
# Stress extraction findings: H.R. 2781

## Bill type and size

- H.R. 2781 is an ordinary introduced House bill, not a resolution, naming measure, or appropriation. The official introduced-version PDF is two pages.
- The supplied raw source is a flattened, one-line extraction of 1,195 bytes and 194 words. It contains two sections, but §1 is only a short title; §2 is the sole substantive provision.
- The operative text is a surgical cross-reference amendment. It adds one clause to 10 U.S.C. §503(c)(1)(A), requiring military-recruiting information to be displayed and made accessible to students during school hours.

## What the contract handled well

- A single provision represented the bill without turning the short title or punctuation edit into separate policies.
- The quote, context, goal, effects, and barriers separated the literal legal duty from possible exposure and implementation consequences.
- The contract tolerated empty `metrics` and `conditionals` arrays. That prevented an invented school-compliance series, an unjustified enlistment proxy, and a tautological conditional about whether the legal duty exists after enactment.
- Effects and barriers captured the important distinction between making information available and causing students to view it, contact a recruiter, apply, or enlist.

## Where it strained

- The amendment imports its actual scope from a statutory chapeau, definitions, exemptions, and enforcement sequence that the raw bill does not reproduce. The artifact has no structured field for incorporated law, the applicable base-law version, or uncertainty introduced when the referenced section changes after introduction.
- The legal duty bearer is a covered local educational agency, while the bill title and practical implementation point toward secondary schools. The schema cannot separately encode the statutory actor, physical display site, and covered population.
- For a bill that only creates a duty, the narrowest honest goal and the direct effect are close to duplicates. The schema has no field for whether a goal is express, inferred from the mechanism, or inferred from a title, and no confidence level for that judgment.
- “Display and make accessible” leaves content, medium, placement, duration, updating, accessibility, and minimal compliance undefined. Those interpretive uncertainties fit only indirectly into free-text context, effects, and barriers.
- The new clause is not expressly request-triggered, but the surrounding enforcement sequence is organized around denial of requested recruiting access. The schema has no dedicated field for enforcement-path ambiguity or for the absence of an implementation deadline and funding.
- Compliance is conceptually measurable through a bespoke school audit, but this extraction identified no named recurring official series, denominator, release schedule, or public resolution record. The metrics schema cannot structurally distinguish “auditable in principle” from “mechanically resolvable from an official product”; that judgment lives only in `sourceLimits`.
- With no defensible metric rows, the category, layer, `series_hint`, and stance-matrix fields disappear entirely. This is honest, but the structured contract cannot preserve the reason for their absence except through prose.
- The prompt-required top-level `sourceLimits` note is not declared in the current `BillArtifact` TypeScript interface and is not rendered on the bill page. The honesty disclosure therefore survives in JSON but not in the current user-facing view.
- Because the raw extraction is a single physical line with no page markers, line-based citations are not useful. Page count and page-level location had to come from the exact official PDF.

## 119s767is
# Stress-test findings: S. 767 IS

## Bill type and size

S. 767 is a short, ordinary introduced Senate bill rather than a resolution, symbolic measure, or appropriations act. The official introduced-version PDF is five pages. The supplied raw artifact is a 4,225-byte, 680-word text/XML-derived stream flattened onto one line. It has two sections: §1 supplies the short title, while §2 is the sole substantive section and amends several parts of the existing HIDTA statutes.

The extraction groups §2 into three thematic provisions: reporting and assessments; authorization and supplemental grants; and prosecutorial resources. It contains seven candidate metrics and five conditional sketches. Every series_hint is deliberately empty. ONDCP's annual HIDTA fentanyl-removal output and annual HIDTA appropriations are plausible official quantitative observations, but neither has a verified exact Thesis registry concept, and the other candidates are document, grant-administration, or personnel observations without guaranteed public recurring releases.

## What the frozen contract handled well

- Three provision records separate genuinely different reporting, fiscal, grant, and personnel mechanisms without manufacturing a provision for every amendatory subparagraph.
- Goals, effects, and barriers preserve critical distinctions that the dollar figures and mandatory verbs could otherwise obscure: authorization is not appropriation, a higher ceiling is not an award, a report is not an enforcement outcome, and a required request process does not guarantee a request or reassignment.
- Category and layer distinguish agency execution, participation in grants or temporary assignments, and the seizure output. The schema does not force a downstream harm metric where the bill supplies no attributable outcome measure.
- Complete stance matrices keep each candidate narrow. Reporting-compliance metrics serve the transparency goal, the limitations disclosure serves the diagnostic goal, and fiscal or personnel metrics do not masquerade as evidence for unrelated goals.
- Blank series_hint values let the artifact retain plausible official observations without minting registry identifiers. The free-text conditionals can also record enactment-dependent document and deadline questions while disclosing why they are not mechanically resolution-ready.
- The top-level sourceLimits note provides one place to say that the source omits incorporated law and implementation evidence, and that no direct series measures reduced trafficking, drug availability, attributable prosecutions, or overdose harm.

## WHERE IT STRAINED

- One substantive section changes two different annual assessments, an authorization of appropriations, a ceiling and eligible uses within supplemental grants, and a temporary-personnel process. The flat provisions array has no parent/child or dependency links, so grouping those amendments into three provisions is an editorial judgment rather than a structure encoded by the bill.
- The supplied raw text is one unterminated line with headings rendered as “1.” and “2.” rather than line-start “SEC.” headings. It contains no pagination, and the current site section slicer may not recover §2 even though normalized quote fragments remain verifiable. The mandatory numeric pages field required the matching official PDF.
- Amendment by reference is not first-class. The raw bill does not reproduce 21 U.S.C. §§1705(g) or 1706(b), (l), (p), and (s), so the cadence, recipient, surrounding criteria, and legal meaning of the inserted clauses require external statutory context. One sourceUrl cannot identify the analyzed bill, incorporated statute, annual ONDCP report, appropriations evidence, and any future DOJ process record by role.
- The schema has no machine-readable modality or fiscal-stage fields for authorization of appropriations, not more than, shall as may be practicable, may request, discretionary award selection, and nonbinding recommendations. Those materially different legal forces survive only in prose.
- The reporting amendment combines document compliance, fund-use descriptions, prosecutions, seizure quantities, and qualitative predictive trends. The phrase “in the area” has no clear antecedent or required disaggregation. A single metric model cannot encode that ambiguity, differing units, denominators, geographic aggregation, joint-seizure deduplication, provisional versus final values, revision policy, confidentiality, or the meaning of “resulting prosecution.”
- Existing HIDTA reporting can separate kilograms from pill or dosage-unit counts and can finalize results after the parent assessment deadline. The contract has no structured unit, vintage, first-release, revision, or missingness policy, so a seemingly recurring seizure metric is not yet a safe registry series.
- Stances express relevance but not sign or interpretation. A higher seizure value can serve operational oversight while reflecting more enforcement, more underlying fentanyl supply, broader coverage, or a reporting change; “serves” cannot encode that directional ambiguity.
- The bill mixes prior fiscal years, a prior-calendar-year report, a 180-day enactment clock, fiscal years 2024–2030 for reassignments, and extensions that may outlast that window. String conditionals cannot represent those event dependencies, already elapsed periods, or open-ended extensions mechanically.
- Several observations may exist only inside government. The bill does not require a public standardized assessment, purpose-coded grant table, DOJ request procedure, reassignment log, or case-attribution dataset. An empty series_hint cannot distinguish “official recurring series but no verified registry mapping” from “future administrative observation with no publication duty.”
- The requested additive sourceLimits field is not declared in the site's current BillArtifact interface and is not rendered on the bill page. Material qualifications therefore also have to be repeated inside visible provision context and metric prose.
- The source's descriptive title says “Office of National Drug Control Prevention Act of 1998,” while its operative amendment names the “Office of National Drug Control Policy Reauthorization Act of 1998.” The schema has no field for a source-level naming inconsistency or legal-text confidence judgment.

The result is intentionally conservative: it records recurring and one-time official-data candidates, but claims zero registry mappings, no guaranteed public personnel or grant series, and no direct measure of reduced fentanyl trafficking or harm.

## 119s2075is
# Stress extraction findings — S. 2075

## Bill type and size

S. 2075 is an ordinary introduced Senate authorization bill, not a resolution, naming measure, or appropriation. The official introduced-version PDF is four pages and contains two sections; §1 is only a short title, leaving §2 as the single substantive provision. The supplied raw extraction is 3,304 bytes and 478 words, flattened onto one line without page boundaries or a metadata sidecar.

The substantive section permits the Army to accelerate work on medical-evacuation and special-operations FLRAA variants, makes several objectives conditional on exercising that discretion, authorizes no additional appropriations, and requires one report to congressional defense committees 180 days after enactment.

## What the contract handled well

- A single provision represented this small, tightly coupled bill cleanly. Splitting the two variants, the funding limitation, and the report into separate provisions would have obscured that the objectives and funding constraint govern the same discretionary authority.
- The goals, effects, and barriers separation captured the difference between what the bill seeks, what its language would legally do, and what appropriations and acquisition administration could prevent or delay.
- The free-text effect mechanism made it possible to state the authorization–appropriation boundary and to avoid treating authority as spending, procurement, or fielding.
- The metric rows could distinguish a limited public execution proxy, an observability-limited statutory milestone, and an honest outcome gap. Empty series_hint values avoided inventing a registry mapping.
- Full stance matrices made the asymmetry visible: the public budget proxy covers MEDEVAC activity but not a separately itemized special-operations variant.

## Where it strained

- The schema has no dedicated field for authority strength or activation conditions. Section 2(a) says the Secretary “may accelerate,” while the “shall ensure” duties in §2(b) activate only “in exercising” that discretion. That nested may/shall relationship had to be repeated in context and effects rather than encoded structurally.
- Goals do not distinguish an enforceable duty from a qualitative design aspiration. “Rapid” prototyping, “advanced” systems, increased reach, enhanced survivability, and commonality “to the maximum extent practicable” all fit as prose, but none has a threshold the contract can mark as measurable or nonmeasurable.
- The authorization–appropriation distinction has no first-class representation. “No additional appropriations” and the advance-appropriation condition fit awkwardly as an effect and barrier even though they fundamentally control whether the authorized work can occur.
- The only hard deadline is enactment plus 180 days, so the bill has no fixed report date while it remains unenacted. The conditionals shape can explain that trigger in prose but cannot encode the unresolved start event and derived deadline separately.
- The metrics shape is oriented toward public outcome series. A one-time report to congressional committees is a real statutory deadline, but the bill requires neither publication nor standardized fields or proof of receipt. The contract has no fields for public availability, cadence, resolver, evidence access, or a private administrative milestone.
- The stance vocabulary cannot express partial coverage or nonmonotonicity. The Army budget row covers only the MEDEVAC side of the two-variant acceleration goal, and a larger dollar value can indicate either additional activity or cost growth; serves, opposes, and orthogonal cannot encode those qualifications.
- No quantities, performance thresholds, baselines, or public variant-specific outcome or cost series are supplied. The honest-gap metric records this absence, but the contract cannot attach the gap directly to individual goal fields.
- sourceLimits is useful for the required honesty note but is additive to the currently typed site contract and is not rendered by the bill page. The main bill/provision shape has no visible field for document incompleteness, external metadata checks, or the reason series hints were omitted.
- The required numeric pages field cannot express that the flattened raw source contains no page boundaries. The value had to come from the matching official PDF, while that field carries no field-level provenance.
- The flattened raw text uses 1. and 2. headings rather than line-start SEC. 1. and SEC. 2. headings. The artifact can quote and analyze the provision, but the current full-section text slicer cannot reliably recover it for display from this cache shape.

## 119hjres109ih
# Stress-test findings: H.J. Res. 109

## Bill type and size

H.J. Res. 109 is an introduced House joint resolution disapproving a D.C. Council action under the congressional-review structure cited in section 602(c)(1) of the District of Columbia Home Rule Act. It is not an ordinary program bill, an appropriations measure, or a merely ceremonial resolution. The matching official introduced-version PDF is one page. The supplied cache is a 1,086-byte, 174-word stream flattened onto one unterminated line, with one unnumbered operative clause and no findings, short title, appropriation, implementation directive, reporting duty, quantitative target, or replacement policy.

The honest extraction is correspondingly small: one provision, one literal formal-disapproval goal, one enactment-contingent effect, and zero implementation barriers, forecastable metrics, series hints, stance rows, or empirical conditionals.

## What the contract handled well

- A one-element `provisions` array preserves the whole legal measure without manufacturing sections or treating its metadata as policy content.
- `quote` and `context` separate the exact operative clause from the procedural status, incorporated-law gap, and enactment contingency.
- A single goal and effect capture the resolution's express objective while avoiding unsupported claims about why Congress disapproves or what the underlying open-meetings amendment does.
- Empty `barriers`, `metrics`, and `conditionals` arrays allow the extraction to remain honest. No dummy metric or invented `series_hint` is needed merely to populate a stance matrix.
- The free-text `sourceLimits` note can disclose that the operative content and precise legal effect of the referenced D.C. Act and Home Rule Act provision are outside the supplied source.

## WHERE IT STRAINED

- The resolution is a meta-legislative disapproval by reference. Its real policy content and review mechanics live in D.C. Act 26–86 and section 602(c)(1) of the Home Rule Act, neither of which the source reproduces. The flat contract has no structured slots for an incorporated instrument, review window, transmission event, temporary-law expiration, or field-level provenance.
- Unlike a Congressional Review Act clause that expressly says a rule “shall have no force or effect,” this clause says only that Congress disapproves the D.C. Council action. The schema's generic `effects` field cannot distinguish a textually specified legal consequence from one that depends on external law, so that limit must remain in prose.
- `goals` and `effects` nearly collapse into the same proposition. The contract cannot mark the goal as a literal restatement rather than an analyst-imputed policy purpose, or distinguish a deterministic legal act from an empirical downstream effect.
- The `barriers.actor` shape assumes an implementation burden. Committee referral, bicameral passage, presentment, and any statutory review deadline are legal preconditions, not ordinary implementation barriers; forcing them into `barriers` would blur that distinction.
- The only plausible direct observation is a one-time categorical legal status. It is not a recurring quantitative outcome series, and a conditional such as `P(Congress disapproves | resolution enacted)` would be tautological. With `metrics: []`, the metric-attached stance design has nowhere to express that the direct legal effect serves the sole goal.
- The source offers no basis for metrics about open-meeting access, transparency, meeting closures, attendance, complaints, litigation, compliance cost, or agency workload. The contract can leave metrics empty, but the empty array alone cannot explain why all attractive-sounding downstream measures would be inventions.
- The mandatory numeric `pages` value cannot be recovered from the flattened raw cache and required the matching official PDF. One free-text `status` field likewise mixes source-version identity, sponsor/referral facts, and current disposition.
- The long official title and absence of a short title or numbered substantive section force some repetition across `bill.name`, `title`, and `heading`.
- The requested top-level `sourceLimits` field is not declared in the current TypeScript `BillArtifact` interface and is neither rendered nor validated by the bill page. Repeating the core honesty note in `context` keeps it visible but duplicates material that should be first-class.
- The absence of an appropriation is structural here, not evidence of an unfunded mandate or delivery barrier. The schema has no direct way to say that no post-enactment administrator or funded program is specified because the measure operates, if at all, through an external legal-review framework.

## 119hr978ih
# Stress-test findings: H.R. 978

## Bill type and size

H.R. 978 is a short, ordinary House bill rather than a resolution, naming bill, or appropriations measure. The official introduced-version PDF is five pages. The supplied raw artifact is a 4,354-byte, 721-word text/XML-derived stream flattened to one unterminated line, with two numbered sections: §1 is only the short title, while §2 contains the substantive policy in six subsections. The bill rescinds a public land order, sets Mine Plan review and permit deadlines, restores or grants specified mineral instruments, excludes judicial review of one issuance category, permits related surface use, and defines the responsible Secretary. It authorizes no appropriation and requires no report.

The extraction groups §2 into three coherent provision records and includes seven conceptual metric rows. All are one-time legal states or case-level administrative measures whose recurring public observability has not been established. Every `series_hint` is therefore intentionally empty, and none of the rows is claimed to be a currently forecast-ready Thesis series.

## What the contract handled well

- Three thematic provision records separate withdrawal rescission, review and permitting clocks, and mineral-instrument restoration without manufacturing a provision for every nested paragraph.
- `goals` can preserve the bill's narrow legal operations without inventing claims about mining output, jobs, royalties, domestic mineral supply, forest restoration, or environmental quality.
- `effects` distinguishes self-executing rescission from later agency action, completion of review from approval, mandatory `shall` duties from discretionary `may` authority, lease issuance from mine production, and the narrow §2(c)(1) judicial-review exclusion from later decisions.
- `barriers` identifies who must reconstruct retrospective cohorts, reconcile instrument terms, coordinate across Interior and Agriculture, and operate under very short or undefined deadlines.
- `category` and `layer` correctly classify every candidate as direct legal or agency execution evidence rather than manufacturing a downstream participation or outcome series. Complete stance matrices also make clear that no proposed metric measures the judicial-review goal.
- Free-text conditionals can at least disclose the enactment and case-level triggers and say why unknown cohorts, dates, and public evidence prevent immediate registration.
- The additive `sourceLimits` note provides one place to say that all seven metrics are conceptual, all hints are blank, and the text supports no quantitative downstream target.

## WHERE IT STRAINED

- The frozen TypeScript `BillArtifact` interface and bill page do not define or render `sourceLimits`, even though the stress contract requires the honesty note. The artifact therefore carries an additive top-level string that the current loader silently ignores; narrower qualifications must be repeated in visible provision prose.
- `pages` cannot be recovered from the supplied one-line raw text. The five-page value required the matching official PDF, but the bill block cannot identify which metadata came from the raw cache and which came from a companion source.
- The raw cache flattens headings to `1. Short title` and `2. Superior National Forest System Lands in Minnesota`. The site's raw-section slicer looks for line-start `SEC. N.` headings, so quote validation can succeed while the full-text disclosure cannot recover §2 from this otherwise substantive source.
- The source names but does not reproduce Public Land Order 7917, the governing mineral-leasing and National Forest authorities, or any affected lease, permit, application, or Mine Plan record. A single `sourceUrl` cannot represent the bill, incorporated order, administrative baseline, case records, and any eventual resolution evidence with distinct roles.
- The bill supplies legal operations rather than findings or downstream policy targets. The contract's `goals` field must restate commands such as rescission, deadline compliance, and judicial-review exclusion; it has no typed distinction among stated purposes, inferred aims, legal outputs, and societal outcomes.
- One-time legal-state changes and small retrospective cohorts fit a recurring-series metric model poorly. `series_hint: ""` conflates no exact registry match, no established recurring public product, unknown public availability, and a bespoke cohort that might later be reconstructed from individual official records.
- Section 2(b) creates rolling clocks from submission, supplemental submission, and approval dates over a ten-year intake window. Unstructured metric and conditional strings cannot encode an unknown enactment date, multiple triggers, cohort maturity, right-censoring, completeness, tolling, resubmission, withdrawal, a changing permit set, or multi-agency responsibility.
- The 18-month rule times completion of reviews, not approval or denial. The six-month permit clock starts only after approval, leaving the approval interval untimed. The schema has no workflow or dependency edges to show that end-to-end submission-to-permit time can remain unbounded even when each express deadline is met.
- Section 2(c) mandates reissuance but gives no deadline, while each new 20-year term begins on enactment. The contract cannot represent the possibility that delayed issuance consumes part of the stated term or distinguish instrument eligibility, issuance, legal effect, continued activity, and renewal as separate states without duplicating prose.
- Reissuance on the same terms, except for new duration and renewal provisions, is an instrument-level transformation. There is no structured field for baseline terms, overrides, renewal options, rental or royalty adjustment rights, or the prospecting-permit exception.
- The five-day §2(d) mandate combines a retrospective rejection window, a preliminary-valuable-deposit prerequisite, a `notwithstanding` clause, and cross-referenced §2(c)(1) terms. A free-text goal or metric cannot make that eligibility predicate and deadline machine-checkable.
- Subsection (e)'s discretionary surface-use authority sits beside mandatory lease grants. The schema has no modality field for `shall` versus `may`, no way to encode consultation, and no natural denominator for measuring discretionary exercise.
- Subsection (f) makes Secretary mean Interior generally but Agriculture when used with respect to a National Forest System unit; subsection (e) separately calls for consultation with Agriculture. A single `barriers.actor` string cannot model split or ambiguous authority across actions.
- The §2(c)(2) judicial-review bar is a distinct procedural-rights change, not an implementation barrier or conventional outcome. The three-value stance vocabulary cannot express legal accountability, scope uncertainty, or a tradeoff between issuance finality and review rights, and no honest metric row naturally measures it.
- A single `quote` field strains when one thematic provision depends on several noncontiguous clauses, exceptions, and cross-references. Elision preserves representative text but cannot encode which quote supports which goal, effect, or metric.
- The short title's word “Restoration” can suggest ecological work, but the operative text requires no reforestation, remediation, or environmental outcome. The contract has no field for title framing versus operative legal content, so that distinction must live in context and source limits.
- The bill contains no appropriation, staffing authorization, reporting mandate, public-data requirement, missed-deadline remedy, or deemed approval. The contract has no dedicated fields for these absences, even though they determine whether implementation and resolution evidence will exist.

The result is intentionally limited to legal and administrative implementation: three provisions, seven conceptual metric rows, no non-empty series hint, and no claim that enactment guarantees mining, economic, or environmental outcomes.

## 119sjres56is
# Stress-test findings: S.J. Res. 56

## Bill type and size

S.J. Res. 56 is an introduced Senate joint resolution making ceremonial and expressive congressional statements, not a bill that establishes a program or changes a quantitative policy rule. The matching official introduced-version PDF is three pages. The supplied cache is a flattened, unpaginated, 2,921-byte and 491-word extraction with seven recitals, a short-title section, and one substantive section containing five clauses.

The source contains no appropriation or authorization, statutory amendment, implementing agency, eligibility rule, reporting duty, quantitative target, express or delayed effective date, end date, or recurring public-data product. Congress.gov separately reports the measure as introduced, with its June 3, 2025 referral to the Senate Judiciary Committee as the latest action.

## What the contract handled well

- A one-element `provisions` array keeps §2 together as one symbolic package instead of inflating its five short clauses into five policy programs.
- `goals` can preserve the four distinct functions of the text: annual designation, recognition and reaffirmation, commendation, and exhortation.
- `effects` can distinguish the ceremonial designation, adopted congressional statements, and the nonbinding request for future policy without claiming that §2(5) itself enacts or funds anything.
- Empty `barriers`, `metrics`, and `conditionals` arrays allow an honest extraction with zero forecastable policy outcomes and no invented `series_hint`.
- The additive `sourceLimits` note records why legislative status, abortion or birth statistics, public opinion, pregnancy-resource-center activity, and future legislation were not promoted into causal outcome metrics.

## Where the contract strained

- The current typed bill interface does not declare or render the additive top-level `sourceLimits` field, even though this is the most important disclosure for a symbolic resolution. A consumer can silently ignore it.
- `pages` requires a number, but the flattened raw source has no page boundaries. The three-page value requires the matching official PDF rather than the supplied cache alone. The cache also omits the standard resolving formula visible in the official text.
- The long title says June, while §2(1) designates only “a Life Month” annually. The schema has no structured way to represent a naming detail supplied by a title but omitted from the operative clause.
- `goals` cannot distinguish literal operative functions from analyst-imputed purposes. Here the safest goals closely restate the clauses, and normative terms such as “culture of life,” “sanctity,” “protect the unborn,” and “choose life” remain undefined.
- `effects` does not classify ceremonial designations, expressions of congressional belief, commendations, and nonbinding exhortations separately from empirical or legally operative effects. The goals and effects therefore overlap more than they would for a program bill.
- `barriers` assumes an actor-specific implementation burden. This resolution has no implementation machinery; bicameral passage and presentment are legal prerequisites, not program-delivery barriers, so the honest array is empty.
- Section 2(1) says “annually” but names no responsible actor, first year, recurrence procedure, public record, or resolution rule. The recurrence language sounds metric-like while failing to create an automatically resolvable series.
- The only direct observable milestone is the resolution's one-time legislative status. Treating that as a policy-outcome series would conflate enactment with effect, while `P(the resolution's statements apply | enactment)` would simply restate the instrument. The conditional array is therefore empty.
- Stance matrices attach only to metrics. With zero defensible metrics, the schema cannot express that the direct ceremonial and expressive effects serve the corresponding goals without manufacturing a dummy metric.
- The contract has no structured field for instrument type, bindingness, recital versus operative text, or the difference between urging future appropriations and making an appropriation now. Those distinctions must live in prose.

The result is intentionally small: one substantive provision, four literal or expressive goals, three enactment-contingent expressive effects, zero implementation barriers, zero forecastable metrics, zero stance matrices or series hints, and zero empirical conditionals.

## 119s2718is
## stress-119s2718is — S. 2718 (introduced in Senate)

- **Bill type / size:** A targeted substantive Senate bill, not a resolution, naming measure, or appropriation. The introduced version is six pages and 896 words in the supplied flattened extraction. It has no statutory short title and consists of one numbered section with three linked parts: replacement of Section 113 assistance, eligibility, selection, and cap rules; addition of Section 113 to the uses of Emergency Capital Investment Program receipts; and annual Treasury reporting through 2028 after assistance first begins.
- **What the contract handled well:** One provision preserves the package's dependency chain instead of inflating three subsections into separate policies. Goals, effects, and barriers distinguish the explicit liquidity aim from permissive authority, Fund discretion, transaction administration, funding limits, and reporting. The metric categories and layers separate assistance delivery from claimed downstream outcomes. Full stance matrices show that activity totals bear on liquidity and reporting but do not measure the selection-priority outcomes. An honest-gap metric plus blank `series_hint` values records the missing outcome evidence without inventing a registry concept.
- **Where it strained — future and finite reports:** The bill creates potential official numeric observations, but only after the unknown date of first assistance and only annually through 2028. That is neither a normal pre-existing series nor simply “no series.” The schema has no first-class state for a future, enactment-contingent, short-lived report, so an empty `series_hint` collapses “not yet defined,” “one-off or finite,” “not public,” and “no suitable series.”
- **Where it strained — chained resolution conditions:** A resolvable observation depends on enactment, discretionary assistance actually occurring, an observable first-assistance date, report submission, possible public availability, and stable field definitions. `conditionals` can narrate this chain but cannot encode its gates, missing-versus-zero behavior, or the tension between a first report due one year after assistance and reporting only “through 2028.”
- **Where it strained — metric semantics:** The report's purchase and credit-enhancement totals are operational activity, not evidence that originations, reach, competitiveness, or liquidity improved. Its competitiveness and liquidity items may be entirely narrative. The metric object cannot distinguish a scalar series from a qualitative statutory assessment, and `serves` cannot express “aligned implementation evidence but insufficient proof,” so the stance judgments must be conservative.
- **Where it strained — goal provenance:** Enhancing liquidity is explicit. Increasing originations or expanding services, potentially leveraging the award with private capital, and supporting CDFIs with broad geographic coverage or service to borrowers with unmet needs appear within a conjunctive award-priority test rather than as guaranteed outcomes or findings. The schema has no confidence or provenance field for distinguishing literal goals from restrained intent inferred from selection rules.
- **Where it strained — statutory modality:** One provision mixes permissive assistance and rulemaking authority (`may`) with mandatory prioritization, deposit uses, and reporting duties (`shall`). Goals, effects, metrics, and stances have no structured modality or trigger field, so prose must carry the difference between authority, a duty that applies only if awards are made, and an unconditional mandate.
- **Where it strained — funding and opportunity cost:** This bill does not appropriate a stated sum. It redirects variable receipts and lists both Sections 113 and 108 as uses without an allocation rule or minimum; the $20 million figure is an aggregate cap for an organization and its subsidiaries or affiliates, without the current three-year reset, not total program funding. Effects and barriers can describe that distinction, but the schema has no structured funding-source, appropriation-status, allocation, or crowd-out field.
- **Where it strained — amendment by reference:** The raw bill replaces and cross-references statutory text it does not reproduce. Understanding removal of the existing match and other-assistance limits, displacement of the existing selection cross-references, the complete entity-group cap sentence, and the addition of Section 113 beside an existing Section 108 use required the official current-law baseline. The provision schema has no field separating direct bill text from incorporated-law analysis.
- **Where it strained — naming and pagination:** The bill has no short-title clause, so the artifact must use its official long title rather than an advocacy name. The required numeric `pages` field cannot express that the flattened raw has no pagination; the matching official PDF was needed to establish six pages. The stress-run `sourceLimits` note carries these qualifications even though that field is not declared in the current TypeScript bill interface.
- **Drafting and interpretation pressure:** The text says purchases made “pursuant of this section”; converts the current rolling three-year cap into a $20 million aggregate entity-group cap without a periodic reset or transition instructions; retains a Federal-funds construction after replacing the matching rule that made the classification evidently relevant; does not define “total amount,” “overall competitiveness,” “liquidity,” “broad geographic coverage,” or “significant unmet” needs; and does not reconcile a late first-assistance trigger with the 2028 reporting endpoint. These are material interpretive limits, not values the extraction should silently fill.

## 119hjres79ih
# Stress extraction findings: H.J. Res. 79

## Bill type and size

H.J. Res. 79 is a Congressional Review Act joint resolution of disapproval, not a program bill, authorization, or appropriation. The supplied raw artifact is 1,324 bytes and 217 words including front matter, flattened onto one physical line. The matching introduced-in-House PDF is two pages and contains one operative sentence: Congress disapproves one named EPA final rule and says that the rule shall have no force or effect.

The analyzed House resolution remains at the introduced stage. A related, substantively equivalent Senate resolution, S.J. Res. 31, became Public Law 119-20 on June 20, 2025, so the legal state requested by H.J. Res. 79 has already been produced through a different measure.

## What the contract handled well

- The provision array represented the actual cardinality without padding: one operative clause became one provision.
- Separate `goals` and `effects` fields preserved the distinction between the clause's literal objective and its enactment-contingent legal mechanism.
- Empty `barriers`, `metrics`, and `conditionals` arrays allowed an honest result. No quantitative or recurring empirical outcome appears in the source, so the extraction did not manufacture one.
- The free-text `context` and top-level `sourceLimits` note made it possible to disclose the incorporated rule, missing downstream evidence, flattened-source limitations, and separately enacted companion measure.
- A verbatim `quote` field anchors the extraction to the sole operative sentence.

## Where it strained

- `goals` normally describes intended real-world outcomes, but this resolution states no findings or downstream purpose. The only defensible goal is the operative legal command itself.
- The effect shape cannot cleanly distinguish a bill-text counterfactual from current policy state. H.J. Res. 79 says what would happen if it became law, while the same effect has already occurred through Public Law 119-20. That redundancy fits only as prose; there is no typed related-measure or already-satisfied field.
- The `status` scalar cannot naturally express that H.J. Res. 79 remains introduced while its substantively equivalent companion became law. Putting both facts in that field would risk conflating the two measures, so the related law is explained in `context` and `sourceLimits` instead.
- The metric contract is designed for agency execution, participation, and downstream outcomes. A one-time binary legal state is mechanically checkable but is not a recurring empirical series, and conditioning it on enactment would be tautological. Leaving `metrics` empty also means there is correctly no stance matrix, but the schema has no separate place to say that a legal state is resolvable yet not forecast-worthy.
- The `barriers` actor-and-text shape is oriented toward program implementation. Ordinary passage and presentment are prerequisites to the clause's effect, not implementation barriers stated by the source, so encoding them as a barrier would inflate the analysis.
- The raw artifact has no page boundaries or sidecar. The required numeric `pages` field could only be completed by checking the official PDF, and the contract has no structured provenance slot for that field-level lookup.
- The resolution incorporates an EPA rule by title and Federal Register citation without reproducing it. The contract has no structured way to mark incorporated-but-unreviewed material or to separate source-supported consequences from consequences that would require that external rule.
- The top-level `sourceLimits` note carries essential honesty information but is not currently typed or validated by the site contract, so a consumer could silently discard the most important qualification.

No series hints were added, and no hash or commit claim is made.

## 119hr1811ih
# Stress-test findings: H.R. 1811

## Bill type and size

H.R. 1811 is a standalone introduced House bill that would create a judicial-branch Inspector General; it is not a resolution, naming measure, or appropriations bill. The matching official introduced-version PDF is seven pages. The supplied raw artifact is a complete substantive but flattened 6,804-byte, 1,114-word stream with two top-level sections: a short title and one substantive section that adds six sections to title 28 plus a conforming chapter-table entry. The extraction uses two analytical provisions—one for the integrated Inspector General framework in proposed §§1021–1025 and one for the distinct whistleblower civil action in proposed §1026—and identifies zero currently automatable public-series metrics or conditionals.

## What the contract handled well

- The `provisions` array can preserve the bill's real structure without inflating the short title or conforming table amendment into policy provisions.
- Free-text `effects` distinguish deterministic legal architecture from contingent implementation: establishment is not operation, report transmission is not public disclosure, investigative activity is not proof of less misconduct, and recommendations are not discipline.
- The `barriers` structure surfaces who would bear appointment, startup, resourcing, jurisdictional, subpoena-enforcement, remedial, and disclosure burdens.
- Separating proposed §1026 keeps employee protection and private enforcement from disappearing inside the larger institutional design.
- Empty `metrics` and `conditionals` arrays honestly represent the absence of a guaranteed public, standardized, mechanically resolvable series. They avoid invented identifiers, tautological enactment forecasts, and stance matrices attached to pseudo-metrics.
- The additive `sourceLimits` note records the flattened-source limits, external page/status check, missing incorporated materials, inferred-goal boundary, drafting defect, absent implementation dates and funding, nonpublic-report possibility, and activity-count ambiguity in one place.

## WHERE IT STRAINED

- Six proposed code sections form one interdependent institution. Any analytical grouping is editorial: §1024's powers support both office capacity and investigative work, while §1025 reporting connects investigations to downstream actors. The schema cannot represent cross-provision dependencies without repetition.
- The current TypeScript `BillArtifact` interface does not declare or render the additive top-level `sourceLimits` field. The most complete honesty note can therefore be silently ignored by a site consumer, forcing the most material qualifications to be repeated in visible provision prose.
- `goals` does not distinguish an express statutory duty, an institutional design choice, a safeguard, and an inferred policy objective. This bill has no findings or purpose section, so the extraction must treat duties and limits as restrained goal proxies rather than claim that Congress stated measurable social outcomes.
- The most concrete implementation objects are a one-time appointment, office stand-up, four-year terms, removal notices, and report transmissions. A time-series-oriented `metrics` shape has no event, document, confidentiality, deadline-missing, or verification-status type for them.
- The annual report is policy-created data whose non-enactment path is missing rather than zero, and the bill prescribes neither a first due date nor public release nor standardized fields. The free-text `conditionals` field cannot make that asymmetric, possibly secret observation into an automatically resolvable comparison.
- Investigation, allegation, referral, and civil-action counts have ambiguous signs: higher counts could reflect more underlying misconduct or retaliation, more willingness to report, or more enforcement capacity. A `serves`/`opposes`/`orthogonal` stance cannot encode that directional ambiguity. With no valid metric rows, the artifact also has no machine-readable way to relate these measurement gaps to goals.
- Governance tradeoffs do not fit a stance matrix. Appointment, unlimited reappointment, and removal all sit with the Chief Justice, while consultation and reasons-to-Congress add visibility without confirmation or a cause standard; the schema has no independence, accountability, or tenure-design field.
- The non-Supreme-Court chapter 16 gate does not expressly apply to the separate Supreme Court authority, while the merits/procedural-ruling exclusion applies across the Office. The schema has no typed jurisdiction, prerequisite, exception, or legal-boundary representation, so these distinctions live in prose.
- Proposed §1024(a)(7) literally says “the extent” rather than “to the extent” in its advance-appropriations clause. A grammatical drafting defect is neither an actor barrier nor an outcome, and the contract has no ambiguity or technical-correction field.
- Proposed §1026 lists contractors and subcontractors as potential retaliators but describes the protected person and civil plaintiff as an employee. The schema cannot encode uncertain beneficiary scope, and it has no field for omitted forum, limitations, exhaustion, proof, fees, or remedy rules.
- The required numeric `pages` field is not recoverable from the one-line raw source and required the official PDF. The single `sourceUrl` also cannot separately identify the supplied cache, bill-status page, external cross-referenced law and Code, future reports, and any eventual implementation evidence.
- The bill provides no appropriation or dollar authorization even though contracting is conditioned on amounts provided in advance by appropriations Acts. The schema cannot distinguish legal establishment, hiring authority, conditional contracting authority, appropriations, obligations, and operational capacity except through narrative effects and barriers.

The compact result is deliberate: institutional significance does not itself create a currently automatable public-data series. No `series_hint`, metric, stance matrix, or conditional was added merely to make the seven-page bill resemble the larger exemplars.

## 119sjres48is
# Stress extraction findings — S.J. Res. 48

## Bill type and size

S.J. Res. 48 is an introduced Senate joint resolution proposing a constitutional amendment, not an ordinary statutory bill and not a purely ceremonial sense-of-Congress resolution. The supplied raw extraction is 1,824 bytes and 316 words on one physical line. The separately checked official PDF is two pages. The operative material is one proposed article with three sections: a six-term House cap, a two-term Senate cap, more-than-half partial-term counting rules, and an article-wide exclusion for anyone who served in either chamber during a Congress before the 118th Congress. The extraction therefore uses one provision, three literal legal goals, four legal effects, two adoption or administration barriers, and zero forecastable metrics or empirical conditionals.

## What the contract handled well

- A single provision can preserve the integrated constitutional article without manufacturing separate program components.
- Goals, effects, and barriers distinguish the literal service limits from their ratification gate, partial-term mechanics, scope exclusion, and missing enforcement machinery.
- Empty `metrics` and `conditionals` arrays let the extraction avoid inventing an outcome series, a `series_hint`, a stance matrix, or a tautological conditional on ratification.
- The additive `sourceLimits` honesty note can state that numeric legal thresholds are not automatically forecastable outcomes and can name downstream claims that the source does not support.
- The quote field can retain the three operative clauses verbatim even though the raw source is flattened onto one line.

## Where it strained

- `bill.pages` is mandatory and numeric, but the flattened raw text has no page boundaries. The two-page value required a separate check of the official PDF; the contract has no field distinguishing source-derived metadata from separately verified metadata.
- `status` is a single prose field with no as-of date or source split. The raw supports introduction and referral, while any claim about current status needs a live actions check.
- A constitutional proposal has a submission-and-ratification chain rather than ordinary enactment and implementation. There is no structured field for the two-thirds congressional gate, three-fourths State-legislature gate, seven-year clock, or the fact that the clock has not started, so those rules sit in context, effects, and barriers.
- `barriers[].actor` fits administrative programs better than Article V thresholds. Congress and State legislatures are constitutional decision-makers, not merely actors bearing implementation burdens.
- The goals array cannot distinguish substantive objectives, counting rules, and scope or grandfather clauses. Combining each chamber's partial-term rule with its service-cap goal and treating the pre-118th-Congress exclusion as a literal legal goal preserves the rules, but their type survives only in prose.
- Section 3 says the entire article does not apply to anyone with pre-118th-Congress service, which is facially broader than merely disregarding earlier terms and may operate across chambers. The schema has no field for scope rules, transition rules, interpretive confidence, or unresolved legal ambiguity.
- The text prohibits a person from serving, not expressly from running or being elected, and it supplies no administrator, challenge route, or enforcement procedure. The effects schema can describe that gap but cannot encode the legal mechanism structurally.
- With zero metrics there is nowhere for a stance matrix to live. That is the honest result, but it exposes the contract's metric-centric bias: text-grounded goals and legal effects can exist without a measurable outcome.
- A State-ratification count is objectively checkable, but it is a one-time adoption milestone with no submission date yet, not a recurring downstream outcome series. Free-form conditionals would make it easy to write a tautology such as the term limits applying conditional on ratification, so the extraction leaves them empty.
- Top-level `sourceLimits` is accepted by prior stress artifacts but is not declared or rendered by the current bill UI type. The key honesty disclosure is duplicated in the provision context so it is not silently lost in presentation.
- The current full-section viewer looks for numbered `SEC.` or `SECTION` headings at line starts. This flattened source has the proposed article and its clauses embedded in one line as `1.`, `2.`, and `3.`, so the viewer cannot recover a full-section slice even though the quote verifier can confirm the fragments.

## 119hjres29ih
# Stress extraction findings

## stress-119hjres29ih — H.J. Res. 29

### Bill type and size

H.J. Res. 29 is an introduced House joint resolution proposing a constitutional amendment, not an ordinary statutory bill, authorization, or appropriation. The supplied source is a flattened one-line, 1,452-byte, 252-word record; the operative proposal is about 125 whitespace-delimited words and the proposed article itself about 72. The separately checked matching official introduced-version PDF is two pages. The single proposed article is one natural provision.

### What the contract handled well

The bill block and one-provision structure represented this very short measure without artificial section splitting. `quote` and `context` could preserve both the ratification gate and the article's three election-limit rules. `goals`, `effects`, and `barriers` could distinguish the proposed legal design, its contingent activation, and application questions. Most importantly, the contract permits empty `metrics` and `conditionals`, so the extraction did not need to invent a recurring outcome, stance matrix, or series hint for a one-time constitutional proposal.

### Where the contract strained

The raw text has no page boundaries, while `bill.pages` requires a number; the two-page value depends on separately checking the official PDF. The raw extraction also drops the standard resolving formula, including the two-thirds-of-each-House language, so a material adoption gate comes from that separately checked source rather than the cached text.

`goals` invites an intent claim even though the measure contains no findings or purpose clause. Here the goals had to restate the operative legal design, and the long title describes only the three-election ceiling rather than the article's separate consecutive-term and partial-term rules. `effects` has no dedicated field for legal-construction uncertainty or interaction with existing constitutional text. `barriers.actor` is also a poor fit: congressional submission and three-fourths state-legislature ratification are constitutional adoption prerequisites, not ordinary implementation burdens.

The seven-year clock begins after submission for ratification, not introduction, so the introduced record supplies no fixed deadline. `conditionals` cannot cleanly encode the proposal → submission → ratification path without treating adoption itself as the policy outcome or writing a tautology. Ratification is objectively resolvable as a one-time legal milestone, but it is not a recurring public-data outcome series. The contract has no separate policy-state/event slot for that distinction. With zero metrics, stance matrices are correctly absent, but that also leaves no structured way to express how the three legal-design goals relate to the effects.

Finally, the top-level `sourceLimits` field carries the crucial honesty judgment and is established by the prior stress-artifact convention, but it is not declared or rendered by the current site bill interface. The contract also has only one `sourceUrl`, so it cannot attach separate provenance to the raw extraction, page count, and current legislative status.

### Honest extraction judgment

The extraction uses one provision, three text-grounded legal-design goals, four direct or contingent legal effects, two adoption or interpretation barriers, and zero metrics or empirical conditionals. It does not split the article into artificial provisions; infer sponsor, partisan, or candidate-specific motives; treat introduction as submission; describe the proposal as enacted or signed; invent a ratification, election, tenure, approval, or democracy series; or claim downstream electoral and institutional outcomes the text does not state. No `series_hint` is warranted.

## 119hr5595ih
## stress-119hr5595ih — H.R. 5595 (IH)

### Bill type/size

H.R. 5595 (IH) is a compact nine-page Internal Revenue Code amendment: two numbered sections, one substantive multi-part section, and approximately 1,354 words in the flattened source. It is neither symbolic nor an appropriation, but it is cross-reference-dense enough to warrant one integrated provision rather than four artificial provisions for its linked rate, relief, reporting, and effective-date pieces.

### What the contract handled well

- A single provision keeps the 15 percent rate, two intended relief routes, provider reporting, and effective date together instead of severing mechanisms that depend on one another.
- Separating effects from barriers captures behavioral substitution and tax incidence apart from administrative work and facial drafting defects.
- Complete stance matrices show that gross liability, citizen-and-national relief take-up, provider reporting, and broad remittance flows are not interchangeable observations.
- Empty `series_hint` values prevent confidential tax-return fields or a broad BEA proxy from being mistaken for an exact Thesis registry series.
- The root `sourceLimits` note, used by later stress artifacts and expressly requested for this extraction, can preserve essential honesty about inferred goals, incorporated law, data availability, and defects that should not be silently repaired.

### WHERE IT STRAINED

- The schema has no field for distinguishing stated goals from analyst-inferred goals. This bill has no findings or purpose clause, so even conservative goals based on the rate, headings, and reporting design carry a provenance and confidence judgment that a plain string cannot express.
- A ternary stance cannot express that lower gross collections might reflect successful citizen relief, lawful funding-instrument substitution, reduced transfers, noncompliance, or failed enforcement. Direction and interpretation depend on joint observations that the matrix cannot encode.
- The conditional form assumes a coherent treatment state, but the text inserts a second §4475(c) without renumbering the existing one. It also points §6050BB(a)(2) to information in the wrong paragraph and adds a table entry for existing §6050AA instead of new §6050BB. The extraction can condition on the intended rules becoming legally operative, but it cannot represent competing legal interpretations or a technical-corrections branch.
- The metric shape does not distinguish confidential administrative data from a recurring public release. Form 720, IRS No. 155, is a real quarterly field, while §6050BB would create relevant returns, but neither fact guarantees a public aggregate suitable for mechanical resolution.
- `sourceLimits` is used by later stress artifacts and was requested for this extraction, but it is not typed or rendered by the current `BillArtifact` interface, so the most important honesty disclosure may be preserved in JSON without reaching the bill page.
- The contract has only one `bill.sourceUrl` and no structured supplemental-source or claim-provenance list. This extraction also relies on current §4475, current §6050AA, Form 720 and IRS No. 155, and BEA Table 5.1, forcing material authorities into prose without machine-checkable claim-to-source links.
- The mandatory numeric `pages` field cannot be derived from the flattened raw cache. It required the exact-version official PDF, while the one-line extraction also prevents reliable line, page, or section-span citations within the source artifact.
- The general effective date incorporates amendments into an earlier public law, while the credit has a separate taxable-year rule. A retroactive point-of-transfer tax, provider verification regime, annual refundable credit, and later information return do not fit one simple observation date or outcome direction.
- The malformed short-title quotation, the operative credit's use of “any individual” despite citizen-and-national headings, and the already-occupied §6050AA number all require literal-versus-intended judgments for which the contract has no dedicated field.

