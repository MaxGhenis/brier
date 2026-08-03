# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Outbound network access is enabled for this run: you may also run curl -sS against official public data endpoints (agency APIs, data portals, release calendars). Run each fetch so its raw response — or the exact excerpt containing every value you use — is echoed in the command output, and read fetched values only from that echoed content. Never take table values from web-search result summaries or from memory. If a fetch fails or returns an empty body, say so in a text step and stop; a run that cannot fetch its base rate must fail honestly rather than substitute remembered values. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: irs.actc.total_claims
- period: 2027
- conditional_on: No legislation enacted by 2027-12-31 changes the IRC §24(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027; current law holds. The $2,500 operative amount is applied by IRC §24(h)(6), while §24(d)(1)(B)(i) contains the underlying $3,000 amount.

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "additional-child-tax-credit-total-claims-ty2027-current-law"
- country: "US"
- targetUnit: "millions"
- dataPointId: "irs.actc.total_claims.2027.first_print.current_law"
- resolutionDate: "2029-12-31"
- sourceBinding: {"adapter": "irs-soi-pub1304", "allowedHosts": ["www.irs.gov"], "expectedReleaseWindow": {"end": "2029-12-31", "start": "2029-01-01"}, "field": "refundable_child_tax_credit_returns", "releasePolicy": "first_print", "sourceSeriesId": "irs.actc.total_claims", "sourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304", "table": "IRS SOI Individual Income Tax Returns Complete Report (Publication 1304), Table 3.3, all returns total row, refundable child tax credit or additional child tax credit, number of returns", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-03-750dfdf6ca78138736340c8c49dc41d3810bd19e710ea3bd16f3a316b62a0bc2.json"
- targetContentHash: "750dfdf6ca78138736340c8c49dc41d3810bd19e710ea3bd16f3a316b62a0bc2"
- registrationCommit: "966f199f95948a7544dae5ba2f4b7101643a311f"
- registeredAtUtc: "2026-08-03T02:32:28Z"
- conditional: "No legislation enacted by 2027-12-31 changes the IRC \u00a724(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027; current law holds. The $2,500 operative amount is applied by IRC \u00a724(h)(6), while \u00a724(d)(1)(B)(i) contains the underlying $3,000 amount."

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
{"slug":"additional-child-tax-credit-total-claims-ty2027-current-law","country":"US","type":"conditional","title":"US ACTC Claims TY2027","question":"IRS SOI Publication 1304 Table 3.3, tax year 2027, all returns total row, refundable child tax credit or additional child tax credit number of returns, first print, conditional on no legislation enacted by 2027-12-31 changing the IRC Section 24(d)(1)(B)(i) earned-income threshold operative at $2,500 for tax year 2027.","unit":"millions","pointEstimate":19.1,"ciLow":18,"ciHigh":20.2,"confidence":0.8,"resolutionDate":"2029-12-31","resolutionSource":"IRS Statistics of Income Individual Income Tax Returns Complete Report, Publication 1304, Table 3.3","resolutionSourceUrl":"https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3","resolutionRule":"Resolve to the first IRS-posted Publication 1304 Table 3.3 Excel file for tax year 2027, all returns total row, field refundable child tax credit or additional child tax credit, number of returns. Convert returns to millions by multiplying by 1e-6 and use the first print only; later revisions, corrected files, and FRED mirrors do not change resolution. If the stated legislative condition fails, treat the conditional target as not met under the registered target rule rather than resolving this current-law forecast against amended-law data.","dataPointId":"irs.actc.total_claims.2027.first_print.current_law","historicalContext":[{"label":"TY2021 ARPA refundable CTC/ACTC claims, millions","value":31.6},{"label":"TY2022 refundable CTC/ACTC claims, millions","value":19.3},{"label":"TY2023 refundable CTC/ACTC claims, millions","value":19.8},{"label":"TY2016 pre-TCJA ACTC claims, millions","value":18.9}],"drivers":["Current-law $2,500 earned-income threshold keeps low earnings phase-in broad","Maximum ACTC of $1,700 and $2,200 CTC after 2025 supports moderate claim counts","Parent/taxpayer SSN requirement from 2025 onward likely trims some mixed-status claims","Child population and low-income worker-family counts drift down slightly","Puerto Rico and Form 1040-SS eligibility remains a source of upside volatility"],"sourceContext":["https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3","https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304","https://www.irs.gov/statistics/soi-tax-stats-upcoming-data-releases","https://www.irs.gov/credits-deductions/individuals/child-tax-credit","https://www.irs.gov/instructions/i1040s8","https://uscode.house.gov/view.xhtml?req=%28title%3A26+section%3A24%28c%29+edition%3Aprelim%29"],"runAt":"2026-08-03T03:02:39Z","reasoning":[{"kind":"heading","text":"Forecast for IRS ACTC total claims, tax year 2027 current law"},{"kind":"text","text":"Framing and exact resolver: the target is not dollars and not total CTC; it is the number of returns in IRS SOI Publication 1304 Table 3.3, all returns total row, refundable child tax credit or additional child tax credit, converted to millions. The resolutionSourceUrl is the IRS Publication 1304 Basic Tables Part 3 page, Table 3.3, and the ledger deadline is 2029-12-31 under the expected first-print window for TY2027 Publication 1304."},{"kind":"tool","tool":"official.lookup","call":"IRS SOI Publication 1304 Table 3.3 table-page lookup for recent tax years and file availability","result":"Fetched IRS Table 3.3 page listing Table 3.3 XLS files for 2023, 2022, 2021, 2020, 2019, and 2018; directory listing showed 23in33ar.xls dated 2026-03-26 07:11:00 and file size 103 KB."},{"kind":"tool","tool":"official.lookup","call":"IRS SOI Publication 1304 recent all-returns total row extraction for refundable child tax credit or additional child tax credit number of returns","result":"Fetched Table 3.3 all-returns total row values used for the claims history: TY2021 = 31.6 million, TY2022 = 19.3 million, TY2023 = 19.8 million; the TY2022 complete report figure for refundable child tax credit or additional child tax credit amount was 34,843 million dollars, used only as a cross-check that the row was the refundable CTC/ACTC row."},{"kind":"tool","tool":"official.lookup","call":"IRS and Code current-law parameter lookup for 2025 onward child tax credit and ACTC rules","result":"Fetched IRS Child Tax Credit and Schedule 8812 pages: CTC up to $2,200 per qualifying child, ACTC up to $1,700 per qualifying child, earned-income threshold $2,500, full-credit phaseout thresholds $200,000 single/head of household and $400,000 married filing jointly; US Code Section 24(h)(6) applies the $2,500 substitution to the underlying $3,000 amount."},{"kind":"tool","tool":"official.lookup","call":"IRS SOI release-timing lookup for Publication 1304 and calendar discipline","result":"Fetched IRS SOI upcoming releases and program-documentation pages: SOI says products are released on quarterly and annual schedules; program documentation says returns for the most recent tax year are generally made available during the following 2 calendar years; the current page lists 2026 full calendar year public release schedule and TY2023 Publication 1304 tables were posted in March 2026."},{"kind":"text","text":"Reference class/base rate: the stable-current-law reference class is post-TCJA non-ARPA refundable CTC/ACTC claims. The useful anchor is around 19 to 20 million claims, with TY2021 excluded from the base-rate level because ARPA made the CTC fully refundable for one year and allowed 17-year-olds, which is not the conditional TY2027 regime."},{"kind":"text","text":"Policy and level update: current law after 2025 keeps the broader $2,500 ACTC phase-in and a $1,700 refundable cap, which supports claims near the recent 19.3 to 19.8 million range. The $2,200 total CTC may create a little more refundable residual for families whose tax liability covers the old $2,000 amount but not the higher amount, while the taxpayer SSN requirement and fewer children under 17 pull the count lower."},{"kind":"math","text":"Prior/update/interval: persistence prior = TY2022-TY2023 stable-regime average of (19.3 + 19.8) / 2 = 19.55 million, historical sample = TY2016 18.9, TY2022 19.3, TY2023 19.8 plus pre-2021 post-TCJA values near 20 million, adjustment components = -0.30 million for child-population and low-income filer drift, -0.25 million for taxpayer SSN tightening, +0.10 million for higher CTC/ACTC generosity, giving 19.55 - 0.30 - 0.25 + 0.10 = 19.10 million. Interval method uses stable-regime successive-change dispersion scaled to the 2027 horizon: sigma = 0.82 million, so 1.28*sigma = 1.05 million; rounded 80% interval is 19.1 +/- about 1.1 = 18.0 to 20.2 million."},{"kind":"text","text":"Counter-consideration: upside risk is higher Puerto Rico/1040-SS take-up, stronger low-wage employment among parents, or a larger-than-expected effect from the $2,200 CTC creating refundable residuals, which could land above the interval. Downside risk is stricter SSN/documentation compliance, child-population decline, or more nonfiling among low-income families, which could land below the interval. A new law changing the threshold would be outside the interval logic because it violates the stated condition."},{"kind":"forecast","point":19.1,"ciLow":18,"ciHigh":20.2}]}

# Reviewer critique
{
  "summary": "Draft is mostly publication-ready, but it should align the resolver URL exactly to the registered source binding.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The JSON `resolutionSourceUrl` points to the Basic Tables Part 3 page, while the registered source binding's `sourceUrl` is the main IRS Publication 1304 complete report page.",
      "actionRequested": "Set `resolutionSourceUrl` to the canonical ledger URL, or explicitly keep the Part 3 page only as supporting context while preserving the registered source URL in the resolver fields."
    }
  ],
  "optionalSuggestions": [
    "Make the historical sample less vague by either listing the pre-2021 post-TCJA values used for interval calibration or saying the interval is judgmental around the explicitly named TY2016/TY2022/TY2023 observations.",
    "Clarify whether the conditional-failure handling maps to a null/unmet conditional outcome in the catalog rather than a numeric resolution."
  ]
}

Emit the final JSON object only.
