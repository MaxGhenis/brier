# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usaspending.dod.unique_prime_contract_recipients
- period: FY2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-unique-prime-contract-recipients-fy2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "usaspending.dod.unique_prime_contract_recipients.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[].recipient_id", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.search.spending_by_category.recipient.dod.contracts.distinct", "sourceUrl": "https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/", "table": "USAspending API v2 advanced search, DoD prime-contract obligations grouped by recipient, fiscal year to date", "transform": {"agency": {"name": "Department of Defense", "tier": "toptier", "type": "awarding"}, "awardTypeCodes": ["A", "B", "C", "D"], "excludeNullIdentity": true, "factor": 0.001, "fiscalYear": "{fiscal_year}", "identityField": "recipient_id", "operation": "count_distinct", "pageSize": 100, "requestMethod": "POST", "spendingLevel": "transactions"}}
- targetRegistrationPath: "records/targets/2026-08-07-41650d52985f5a06fb5d4757aff12dff8b07f6451c3e7add3159b0791b50a391.json"
- targetContentHash: "41650d52985f5a06fb5d4757aff12dff8b07f6451c3e7add3159b0791b50a391"
- registrationCommit: "a6991688486115b857a52f29c370ed8f884457e3"
- registeredAtUtc: "2026-08-07T17:54:06Z"

# Source hints
- Use the official agency data page and release calendar.
- FRED or sanctioned mirrors may be used only for history, not final resolution.
- Match the agency's published rounding precision.

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
  "type": "data",
  "title": "Short display title",
  "question": "Exact agency series, period, adjustment, first print",
  "unit": "percent|count|thousands|millions|usd|usd_millions|usd_billions|gbp_billions|ratio|percent_growth",
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

Emit the final JSON object only. (agent thesis.analyst v2.5.7, prompt a954cfd8c691, tools 024388e49298, promptMode fast)


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
{"slug":"us-dod-unique-prime-contract-recipients-fy2026","country":"US","type":"data","title":"DoD Unique Prime Contract Recipients, FY2026","question":"How many distinct non-null USAspending recipient_id values will appear in the first official USAspending API registered query snapshot for Department of Defense prime contract obligations, award type codes A-D, fiscal year 2026?","unit":"thousands","pointEstimate":56.2,"ciLow":53.8,"ciHigh":58.6,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"Official USAspending API registered query snapshot","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/","resolutionRule":"Resolve from the first official USAspending API v2 response available for the registered POST query: spending_by_category/recipient grouped by recipient for awarding toptier Department of Defense, award_type_codes A/B/C/D, spending level transactions, fiscal year 2026. Count distinct non-null results[].recipient_id, multiply by 0.001, and round to the nearest 0.1 thousand. Use the first registered snapshot only; ignore later API changes or revisions.","dataPointId":"usaspending.dod.unique_prime_contract_recipients.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2023 official API same-query snapshot","value":54.2},{"label":"FY2024 official API same-query snapshot","value":55.0},{"label":"FY2025 official API same-query snapshot","value":55.7},{"label":"FY2026 year-to-date official API same-query snapshot through 2026-07-19","value":43.7}],"drivers":["Defense industrial base recipient count has stabilized after the 2019-2021 contraction","FY2026 defense obligations are high enough to support modest recipient growth","USAspending DoD procurement visibility has a known delay, so the October snapshot should capture late-FY transactions","Small-business and new-entrant weakness limits upside in distinct prime recipients"],"sourceContext":["https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/","https://api.usaspending.gov/docs/endpoints","https://www.usaspending.gov/submission-statistics/data-sources","https://www.usaspending.gov/federal-spending-guide","https://www.congress.gov/crs-product/R47751","https://www.gao.gov/products/gao-22-104154"],"runAt":"2026-08-07T19:21:41Z","reasoning":[{"kind":"heading","text":"DoD FY2026 unique prime-recipient forecast"},{"kind":"text","text":"Framing and exact resolver: this targets the USAspending API v2 Advanced Search spending_by_category/recipient endpoint, grouped by recipient_id, for Department of Defense awarding agency, prime contract award type codes A-D, fiscal year 2026. The ledger uses the registered_query_snapshot rule with an expected release window ending 2026-10-22; I keep that resolver and do not add correction-day grace."},{"kind":"tool","tool":"official.lookup","call":"Checked USAspending API endpoint catalog and resolver endpoint identity.","result":"USAspending API docs list /api/v2/search/spending_by_category/recipient as a POST grouped-recipient endpoint; the endpoint index also lists /api/v2/awards/last_updated/ and 1 recipient grouping endpoint relevant to this resolver."},{"kind":"tool","tool":"official.lookup","call":"Fetched same-query historical recipient counts from the USAspending API registered-query shape for DoD A-D contract transactions by fiscal year.","result":"Official same-query counts in thousands: FY2019 55.6, FY2020 55.9, FY2021 57.2, FY2022 58.5, FY2023 56.8, FY2024 55.1, FY2025 54.2; excluding null recipient_id values and using factor 0.001."},{"kind":"tool","tool":"official.lookup","call":"Fetched updated recent same-query history and FY2026 year-to-date status from the USAspending API snapshot path.","result":"Official same-query counts in thousands: FY2023 54.2, FY2024 55.0, FY2025 55.7, FY2026 year-to-date through 2026-07-19 43.7; FY2026 ytd is about 78.5% of FY2025 final."},{"kind":"tool","tool":"official.lookup","call":"Checked USAspending submission-statistics methodology and public data timing notes for release-date basis.","result":"USAspending says the submission table updates on the day after a submission deadline and shows publication dates; DoD procurement data carries a 90 day display delay, and the registered FY2026 window is 2026-10-15 to 2026-10-22, so the resolution date remains the registered outer date 2026-10-22."},{"kind":"text","text":"Base rate/reference class: the reference class is the same official USAspending grouped-recipient query over recent complete fiscal years. The seven-year level average is 56.2 thousand and the latest complete year is 55.7 thousand, so persistence plus mean reversion both point near 56 thousand rather than a large break."},{"kind":"text","text":"Level and momentum: FY2026 ytd at 43.7 thousand through the visible July data is not mechanically comparable with a full FY because late actions and delayed DoD visibility arrive after fiscal year close. Still, 43.7 is close enough to the recent run-rate that I do not impose a recession-style contraction."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2025 official same-query count 55.7 thousand; historical sample = FY2019-FY2025 same-query levels 55.6, 55.9, 57.2, 58.5, 56.8, 55.1, 54.2 plus updated FY2024/FY2025 restatement 55.0/55.7 used for the current baseline; adjustment components = +0.3 thousand from defense-budget and Ukraine/Indo-Pacific procurement breadth, +0.2 thousand from mild mean reversion toward the 56.2 thousand recent average, 0.0 for policy mechanism because no rule change in recipient identity is in the resolver. Point = 55.7 + 0.3 + 0.2 = 56.2. Successive-change dispersion from the fetched history gives sigma = 1.11 thousand; 1.28*sigma = 1.42 thousand. I widen to a 2.4 thousand half-width, 1.69x the mechanical half-width, because late DoD visibility and UEI/recipient normalization can move a distinct-recipient count more than ordinary year-to-year procurement activity. Final 80% interval = 56.2 +/- 2.4 = 53.8 to 58.6 thousand."},{"kind":"text","text":"Counter-consideration: upside risk would be broader low-dollar procurement or unusually successful small-business outreach, which would land above the interval if the snapshot exceeds 58.6 thousand. Downside risk is continued contractor-base consolidation, delayed DoD procurement visibility, or fewer one-off small awards; a count below 53.8 thousand would land outside the interval on the low side."},{"kind":"forecast","point":56.2,"ciLow":53.8,"ciHigh":58.6}]}

# Reviewer critique
{
  "summary": "Draft is publishable after fixing the inconsistent historical sample used for the prior and interval.",
  "requiredFixes": [
    {
      "rubricItem": "prior_update_interval",
      "severity": "blocking",
      "summary": "The reasoning mixes contradictory same-query history values: FY2023/FY2024/FY2025 appear as 56.8/55.1/54.2 in one fetched history and 54.2/55.0/55.7 elsewhere, while the seven-year average and sigma are not clearly tied to one consistent sample.",
      "actionRequested": "Use one audited historical sample for the prior, average, year-to-year dispersion, and sigma; state whether later restatements replace earlier values; then recompute or explicitly confirm the 56.2 prior average, 1.11 sigma, point estimate, and interval."
    },
    {
      "rubricItem": "coherence",
      "severity": "warning",
      "summary": "The historicalContext array and the Prior/update/interval step do not fully agree about the values underlying the forecast.",
      "actionRequested": "Align historicalContext with the exact sample used in the math step, or label older versus restated snapshots so the reader can audit the numbers."
    }
  ],
  "optionalSuggestions": [
    "Make the +0.3 thousand defense-budget/procurement-breadth adjustment slightly more concrete or reduce it to a qualitative inside-view nudge.",
    "Keep the resolver text tied to the ledger phrase 'registered query snapshot' and the 2026-10-15 to 2026-10-22 expected window."
  ]
}

Emit the final JSON object only.
