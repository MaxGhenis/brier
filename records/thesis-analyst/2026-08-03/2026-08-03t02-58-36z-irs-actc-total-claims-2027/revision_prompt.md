# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Outbound network access is enabled for this run: you may also run curl -sS against official public data endpoints (agency APIs, data portals, release calendars). Run each fetch so its raw response — or the exact excerpt containing every value you use — is echoed in the command output, and read fetched values only from that echoed content. Never take table values from web-search result summaries or from memory. If a fetch fails or returns an empty body, say so in a text step and stop; a run that cannot fetch its base rate must fail honestly rather than substitute remembered values. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: irs.actc.total_claims
- period: 2027
- conditional_on: Legislation enacted by 2027-12-31 makes the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027.

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "additional-child-tax-credit-total-claims-ty2027-threshold-one-dollar"
- country: "US"
- targetUnit: "millions"
- dataPointId: "irs.actc.total_claims.2027.first_print.threshold_one_dollar"
- resolutionDate: "2029-12-31"
- sourceBinding: {"adapter": "irs-soi-pub1304", "allowedHosts": ["www.irs.gov"], "expectedReleaseWindow": {"end": "2029-12-31", "start": "2029-01-01"}, "field": "refundable_child_tax_credit_returns", "releasePolicy": "first_print", "sourceSeriesId": "irs.actc.total_claims", "sourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304", "table": "IRS SOI Individual Income Tax Returns Complete Report (Publication 1304), Table 3.3, all returns total row, refundable child tax credit or additional child tax credit, number of returns", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-03-e1e24629b485515d803523111d9d5866c88fcbee6e13d0b33a3599e9c15011df.json"
- targetContentHash: "e1e24629b485515d803523111d9d5866c88fcbee6e13d0b33a3599e9c15011df"
- registrationCommit: "966f199f95948a7544dae5ba2f4b7101643a311f"
- registeredAtUtc: "2026-08-03T02:32:28Z"
- conditional: "Legislation enacted by 2027-12-31 makes the IRC \u00a724(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027."

# Source hints
- Use IRS filing-season statistics, annual inflation-adjustment revenue procedures, and official IRS release pages.
- For threshold targets, resolve to the first official IRS value for the named tax year and parameter, not an inferred estimate once the official figure is available.
- Match the catalog unit, usually nominal dollars or billions of nominal dollars.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Include one public reasoning step beginning "Prior/update/interval:" that names the model or persistence prior, historical sample, adjustment components, interval method, and final implied bounds.
- For strict first-print or original-vintage targets, keep the ledger resolver in substance and do not add same-day correction or release-day grace exceptions unless the target rule includes them.
- Size the 80% interval from realized dispersion and SHOW the arithmetic in the Prior/update/interval step: compute sigma from the fetched history (successive changes for level/rate series; the values themselves for change/flow series), state it literally as "sigma = X", and derive the half-width as roughly 1.28*sigma. If you widen or narrow beyond about 0.75x-1.75x of that half-width, state the regime or mechanism reason in the same step. Never default to a round hedged band.
- When a release has variants (gross vs smoothed/synthetic, SA vs NSA, flash vs final), the resolution rule must name the variant and every anchor and historical value must come from that same variant; say so once in a text step.
- resolutionSourceUrl must be the most specific stable page for the exact series (release page, table, or databrowser query with the series code), never a portal or theme landing page; state the series code or table id in a text step when one exists.
- Name concrete upside, downside, and outside-the-interval scenarios, using the literal phrases "upside risk", "downside risk", and "outside the interval" (or "would land above/below the interval") so the falsification step is machine-checkable.

# Required JSON shape
{
  "slug": "kebab-case-unique-vs-catalog",
  "country": "US|UK|CA|AU|EA|JP",
  "type": "conditional",
  "title": "Short display title",
  "question": "Exact agency series, period, adjustment, first print",
  "unit": "percent|count|thousands|millions|usd|usd_billions|gbp_billions|ratio|percent_growth",
  "pointEstimate": 0,
  "ciLow": 0,
  "ciHigh": 0,
  "confidence": 0.8,
  "resolutionDate": "YYYY-MM-DD",
  "resolutionSource": "Official agency release",
  "resolutionSourceUrl": "https://official-source.example",
  "resolutionRule": "First-print rule with rounding and revision policy",
  "dataPointId": "agency.dataset.concept.period.first_print",
  "historicalContext": [
    {
      "label": "latest",
      "value": 0
    }
  ],
  "drivers": [
    "short driver phrases"
  ],
  "sourceContext": [
    "https://urls-actually-used"
  ],
  "runAt": "date -u +%Y-%m-%dT%H:%M:%SZ",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Forecast title"
    },
    {
      "kind": "text",
      "text": "Framing and exact resolver"
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "source lookup description",
      "result": "fetched numbers"
    },
    {
      "kind": "math",
      "text": "point and 80% interval calculation"
    },
    {
      "kind": "forecast",
      "point": 0,
      "ciLow": 0,
      "ciHigh": 0
    }
  ]
}

# Validation rules
- Use confidence 0.8 exactly.
- ciLow < pointEstimate < ciHigh, except discrete policy-rate targets may put the modal point at an interval edge if needed.
- historicalContext must contain at least 3 numeric fetched points.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.4.0, prompt 7ef119647b35, tools 50a06b62f9be, promptMode fast)


# Pre-submit review loop

You already drafted the response below. A reviewer then checked the draft against the Thesis rubric. Produce the final JSON forecast now.

Rules for the final submission:
- Return exactly one JSON object and no Markdown.
- Use only pre-resolution public evidence available to the draft.
- Accept reviewer fixes only when they improve resolver clarity, source grounding, base-rate discipline, uncertainty calibration, or internal coherence.
- Add a public reasoning text step beginning with "Review disposition:" that states which critique items were accepted or rejected. Keep this concise; do not reveal hidden chain-of-thought.
- Put the Review disposition text step before the final forecast step.
- The final reasoning step must be the forecast step, and its numbers must exactly match pointEstimate, ciLow, and ciHigh.

# Draft forecast response
{"slug":"additional-child-tax-credit-total-claims-ty2027-threshold-one-dollar","country":"US","type":"conditional","title":"ACTC claims, TY2027 threshold $1","question":"IRS SOI Publication 1304 Table 3.3, all returns total row, refundable child tax credit or additional child tax credit number of returns for tax year 2027, first print, conditional on legislation enacted by 2027-12-31 making the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027.","unit":"millions","pointEstimate":21.4,"ciLow":18.6,"ciHigh":24.2,"confidence":0.8,"resolutionDate":"2029-12-31","resolutionSource":"IRS SOI Individual Income Tax Returns Complete Report (Publication 1304), Table 3.3","resolutionSourceUrl":"https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304","resolutionRule":"Resolve to the first IRS SOI Publication 1304 Table 3.3 value for tax year 2027, all returns total row, refundable child tax credit or additional child tax credit, number of returns. Convert returns to millions by multiplying by 0.000001. Use the first posted official table only; do not revise for later updates or corrections unless the first post is inaccessible or withdrawn before observation.","dataPointId":"irs.actc.total_claims.2027.first_print.threshold_one_dollar","historicalContext":[{"label":"2016 ACTC claims, Tax Foundation extraction from IRS Table 3.3","value":18.921},{"label":"2018 refundable CTC or ACTC claims, National Academies table citing IRS Table 3.3","value":20.45},{"label":"2021 refundable CTC or ACTC claims, National Academies table citing IRS Table 3.3","value":37.77},{"label":"August 2021 advance CTC payment returns, Treasury and IRS","value":36.049},{"label":"2022 total child credit recipient rate among taxpayers with children, CRS/TPC percent","value":89.6}],"drivers":["Lowering the refundability threshold from $2,500 to $1 adds low-earnings child tax units but does not make zero-earned-income units eligible under the earned-income formula.","Post-TCJA non-ARPA ACTC claims clustered near 19-21 million before full 2021 refundability.","The 2021 fully refundable regime shows a high ceiling near 36-38 million families/returns, but the conditional policy is narrower than full refundability.","SSN, age, residency, phaseout, filing, and take-up frictions still limit claims.","Tax year 2027 demographics and employment among low-income families add moderate drift from the last complete pre-policy base."],"sourceContext":["https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304","https://www.irs.gov/statistics/soi-tax-stats-upcoming-data-releases","https://www.irs.gov/irm/part21/irm_21-008-001r","https://www.irs.gov/irm/part4/irm_04-019-014r","https://home.treasury.gov/news/press-releases/jy0322","https://www.congress.gov/crs-product/R41873","https://www.nationalacademies.org/read/29163/chapter/4"],"runAt":"2026-08-03T02:58:51Z","reasoning":[{"kind":"heading","text":"Forecast ACTC total claims under a $1 earned-income threshold"},{"kind":"text","text":"Framing and exact resolver: the target is not dollars of the credit and not advance-payment counts; it is IRS SOI Publication 1304 Table 3.3, all returns total row, refundable child tax credit or additional child tax credit, number of returns, for tax year 2027, first print. The ledger resolution date is 2029-12-31; this run found the IRS SOI calendar process and a 2026 schedule entry for TY2023 Publication 1304, but not a concrete TY2027 release date yet, so I keep the contract date and treat 2029-12-31 as the target's outside expected-release cutoff rather than a currently announced day."},{"kind":"tool","tool":"official.lookup","call":"Opened IRS SOI Publication 1304 page and Basic Tables Part 3 listing.","result":"Fetched IRS Publication 1304 page states Table 3.3 is 'All Returns: Tax Liability, Tax Credits, and Tax Payments' by size of AGI and lists table years including 2023, 2022, 2021, 2020, 2019, 2018, and older; the page was last reviewed or updated 22-Jul-2026 and the Basic Tables Part 3 page was last reviewed or updated 06-Apr-2026."},{"kind":"tool","tool":"official.lookup","call":"Opened IRS SOI upcoming data releases schedule.","result":"Fetched IRS SOI schedule says Publication 1304 Tables for program year 2023 were scheduled for 3/26/2026; the same schedule states SOI provides quarterly releases, an annual full calendar schedule, and program details, and that dates are tentative and updated as information becomes available."},{"kind":"tool","tool":"official.lookup","call":"Fetched IRS IRM child tax credit and ACTC statutory operating parameters.","result":"Fetched IRS IRM states for tax years 2022-2024 the child tax credit is $2,000 per child, with refundable caps up to $1,500 for 2022, $1,600 for 2023, and $1,700 for 2024; another IRS IRM section states PATH made the reduced ACTC earned-income threshold permanent at $3,000 and that 2021 ARPA made the CTC fully refundable, with $3,000 per child age 6-17 and $3,600 per child age 5 and under."},{"kind":"tool","tool":"official.lookup","call":"Fetched Treasury/IRS advance CTC payment release for the full-refundability reference class.","result":"Fetched Treasury/IRS August 2021 release reports All Returns total of 36,049 thousand payments covering 60,918 thousand qualifying children and $15,429,789 thousand in payments, with an average payment amount of $428; the July 2021 release reported nearly 60 million eligible children and about $15 billion paid."},{"kind":"tool","tool":"official.lookup","call":"Fetched public IRS-derived reference-class summaries from National Academies and CRS.","result":"Fetched National Academies table citing IRS Table 3.3 reports refundable portion of CTC/ACTC number of returns of 20.45 million in 2018 and 37.77 million in 2021, with amounts of $40.72 billion and $115.87 billion in 2021 dollars. Fetched CRS/TPC table reports in 2022 that 89.6% of taxpayers with children received the child credit, including 49.5% under $10,000 income, 63.0% at $10,000-$20,000, and 78.2% at $20,000-$30,000."},{"kind":"text","text":"Base rate/reference class: I anchor on the post-TCJA partial-refundability base around 20.45 million 2018 refundable CTC/ACTC returns, because that is the closest modern non-ARPA regime with a low earnings threshold and similar credit architecture. The 2021 fully refundable 37.77 million return count and 36.049 million advance-payment returns are ceiling references, not the central case, because the conditional threshold change does not remove the earned-income formula or all filing/take-up frictions."},{"kind":"math","text":"Prior/update/interval: persistence prior = 20.45 million claims from 2018 IRS Table 3.3-derived reference, historical sample = 2016 ACTC 18.921, 2018 refundable CTC/ACTC 20.45, 2021 full-refundable 37.77, and 2021 advance-payment 36.049 million. Adjustment components: +0.4 million demographic/filing drift from 2018 to TY2027, +1.1 million for families with earnings from $1 to $2,500 who gain small refundable amounts, -0.6 million because some newly eligible units have too little benefit, missing SSNs, no return filing, or no qualifying child under the 2027 rules. Point = 20.45 + 0.4 + 1.1 - 0.6 = 21.35, rounded to 21.4 million. For interval sizing, use stable-regime changes rather than the one-year ARPA regime jump: 2016 to 2018 change = 20.45 - 18.921 = 1.529 million; assumed post-2027 threshold uptake uncertainty adds another policy-mechanism sigma component of 0.65 million, so sigma = sqrt(1.529^2 + 0.65^2) = 1.66 million. 1.28*sigma = 2.13 million; I widen to 2.8 million because the target is conditional on a new law and IRS first-print take-up can deviate, giving 21.4 +/- 2.8 = 18.6 to 24.2 million."},{"kind":"text","text":"Mechanism check: lowering the threshold from $2,500 to $1 mostly creates small ACTC amounts for workers below the current phase-in threshold; it does not replicate ARPA full refundability for zero-income families. The 2022 low-income recipient rates from CRS/TPC imply substantial remaining headroom among families under $20,000, but only a subset of that headroom is caused by the threshold rather than no filing, no qualifying child, SSN rules, phaseouts, or age limits."},{"kind":"text","text":"Counter-considerations: upside risk is a companion simplification or outreach policy that induces many more low-income families to file, which would land above the interval if claims approach 25 million or more. Downside risk is tight SSN enforcement, weak filing take-up, or a law that technically lowers the threshold but preserves other formula limits, which would land below the interval if claims stay near the 2016-2018 ACTC base under 18.6 million. A full-refundability policy like ARPA would be outside the interval on the upside and should be treated as a different regime."},{"kind":"forecast","point":21.4,"ciLow":18.6,"ciHigh":24.2}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready, with only minor tightening needed around exact resolver wording and support for the interval inputs.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolutionRule adds an exception for later updates or corrections if the first post is inaccessible or withdrawn, which is not in the canonical first-print contract.","actionRequested":"Align the resolver text exactly to the ledger's first-print rule, or explicitly state that any accessibility/withdrawal exception is only explanatory and does not change the registered target contract."},{"rubricItem":"interval","severity":"warning","summary":"The interval relies materially on the 2016 value and a policy-mechanism sigma component, but the 2016 source is not included in sourceContext and the 0.65 million component is judgmental rather than tied to a cited realized series.","actionRequested":"Add the public source for the 2016 18.921 million value and briefly label the 0.65 million policy component as an explicit judgmental uncertainty add-on, or replace it with a cited historical volatility estimate."}],"optionalSuggestions":["Briefly state that a formal time-series model is not used because the usable regime-consistent sample is sparse and structurally broken by ARPA.","Clarify whether the National Academies 2018 and 2021 values are exact Table 3.3 counts or transformed/rounded reproductions from IRS-derived tables."]}

Emit the final JSON object only.
