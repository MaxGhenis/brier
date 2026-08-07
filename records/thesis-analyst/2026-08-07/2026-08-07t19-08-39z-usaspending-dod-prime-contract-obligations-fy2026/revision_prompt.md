# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usaspending.dod.prime_contract_obligations
- period: FY2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-contract-obligations-fy2026"
- country: "US"
- targetUnit: "billions USD"
- dataPointId: "usaspending.dod.prime_contract_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[category=contracts].aggregated_amount", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.obligations_by_award_category.contracts", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) obligations by award category, contracts row, fiscal year to date", "transform": {"factor": 1e-09, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-8b3a9c297b91e44b81cdda9bca2c64337b021348fba63395c4b5879b6e3e94be.json"
- targetContentHash: "8b3a9c297b91e44b81cdda9bca2c64337b021348fba63395c4b5879b6e3e94be"
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
{"slug":"us-dod-prime-contract-obligations-fy2026","country":"US","type":"data","title":"DoD prime contract obligations FY2026","question":"What will USAspending.gov first print for Department of Defense agency 097 obligations by award category, contracts row, fiscal year 2026, in billions of current U.S. dollars?","unit":"usd_billions","pointEstimate":485,"ciLow":405,"ciHigh":565,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2, agency 097 obligations by award category","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026","resolutionRule":"Resolve to the first registered-query snapshot on 2026-10-22 from api.usaspending.gov API v2 endpoint /api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026, taking results[category=contracts].aggregated_amount and multiplying by 1e-9. Use the first official print only; do not revise for later API restatements or same-day corrections unless the registered snapshot itself is replaced before capture. Round to the agency-published dollar amount converted to billions USD.","dataPointId":"usaspending.dod.prime_contract_obligations.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2024 CRS FPDS DoD contract obligations","value":445.23},{"label":"FY2023 CRS FPDS DoD contract obligations","value":456},{"label":"FY2022 CRS FPDS DoD contract obligations","value":414},{"label":"FY2021 CRS FPDS DoD contract obligations","value":389},{"label":"FY2020 CRS FPDS DoD contract obligations","value":423}],"drivers":["FY2026 total DoD budget request near $961.6B including $113.3B reconciliation funding","acquisition-heavy reconciliation funding should lift contractable dollars but may be multi-year","regular FY2026 procurement and O&M authorizations are not materially above FY2025","DoD contract obligations have recently stayed around the mid-$400B range","USAspending DoD contract data publication lag makes this a strict first-snapshot target"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026","https://api.usaspending.gov/docs/endpoints","https://www.usaspending.gov/agency/department-of-defense","https://www.congress.gov/crs_external_products/R/PDF/R48784/R48784.2.pdf","https://www.cbo.gov/publication/62396","https://www.defense.gov/News/Transcripts/Transcript/Article/4228828/background-briefing-on-fy-2026-defense-budget/","https://www.congress.gov/crs-product/IN12641"],"runAt":"2026-08-07T19:08:54Z","reasoning":[{"kind":"heading","text":"DoD prime contract obligations FY2026 forecast"},{"kind":"text","text":"Framing and exact resolver: the target is the USAspending API v2 agency 097 obligations_by_award_category endpoint, fiscal_year=2026, contracts row only, transformed from dollars to billions USD. I keep the ledger resolver and its 2026-10-22 registered-query snapshot date; the observed value should be the first official API print for that snapshot, not a later revised history."},{"kind":"tool","tool":"official.lookup","call":"USAspending endpoint and publication-variant lookup for agency 097 obligations_by_award_category and DoD award data timing","result":"USAspending documents /api/v2/agency/<TOPTIER_AGENCY_CODE>/obligations_by_award_category/ as the endpoint for a breakdown of obligations by award category within a fiscal year; the target uses agency code 097 and fiscal_year 2026. USAspending pages also state a 90-day delay for displaying Department of Defense contract award data, so the forecast is explicitly for the registered 2026-10-22 API snapshot rather than a later complete-final restatement."},{"kind":"tool","tool":"official.lookup","call":"CRS FPDS history lookup for DOD vs non-DOD contract obligations, FY2015-FY2024","result":"The CRS FPDS figure gives recent DoD contract-obligation history in billions of nominal dollars: FY2020 about 423, FY2021 about 389, FY2022 about 414, FY2023 about 456, and FY2024 about 445.23 from the FY2024 contract-type stack 300.68 fixed-price + 140.46 cost-reimbursement + 4.09 time-and-materials/labor-hours."},{"kind":"tool","tool":"official.lookup","call":"CBO and DoD FY2026 budget request lookup","result":"CBO reports the DoD FY2026 budget request totaled 961 billion dollars including 113 billion dollars from the 2025 reconciliation act; the DoD briefing gives 961.6 billion total for DoD, 848.3 billion discretionary, and 113.3 billion mandatory reconciliation funding."},{"kind":"tool","tool":"official.lookup","call":"CRS FY2026 NDAA funding authorization lookup by appropriation title","result":"CRS reports enacted FY2026 NDAA Division A values of 161.7 billion dollars for Procurement, 145.7 billion for RDT&E, 291.5 billion for O&M, 193.2 billion for MILPERS, and 855.7 billion for total DoD-military subfunction 051; the comparable enacted FY2025 NDAA Procurement and O&M figures were 167.8 billion and 294.5 billion."},{"kind":"text","text":"Base rate/reference class: the best outside-view anchor is recent FPDS/USAspending-style DoD prime contract obligations, not total DoD budget authority. FY2020-FY2024 was roughly 389B to 456B with a recent center near 425B-445B, and FY2024 was 445.23B. That makes a no-shock persistence prior around 450B before considering FY2026 funding changes."},{"kind":"text","text":"Variant consistency: all anchors are for DoD procurement contract obligations or prime contract obligations measured in current-dollar billions, excluding Other Transaction Agreement obligations when the CRS FPDS source says they are excluded. The resolver is narrower in implementation because it reads USAspending's contracts award-category row for agency 097, but it is the closest official public history for the same prime-contract obligation concept."},{"kind":"math","text":"Prior/update/interval: persistence prior model uses FY2023-FY2024 near-last-value history at 450B, with the FY2020-FY2024 reference class 423, 389, 414, 456, 445.23. Adjustment components: +20B for FY2026 acquisition-heavy reconciliation funding that should partly obligate through contracts, +10B for nominal price/wage growth and defense-industrial capacity, +5B for policy emphasis on shipbuilding, munitions, missile defense, and industrial-base buys, offset by -0B to -15B because enacted regular Procurement and O&M are not above FY2025 and some reconciliation budget authority is multi-year. Point = 450 + 35 = 485. Interval method: sample standard deviation of the longer FY2015-FY2024 DoD contract-obligation values, approximately 273, 296, 322, 360, 383, 423, 389, 414, 456, 445, gives sigma = 62.6; 80% half-width = 1.28*sigma = 1.28*62.6 = 80.1, so 485 +/- 80 gives 405 to 565."},{"kind":"text","text":"Upside risk: a fast obligation of the reconciliation-funded acquisition tranche, large munitions and shipbuilding awards, or accelerated year-end contract actions would land above the interval, especially if the USAspending contracts row captures more than 565B by the registered snapshot. Downside risk: continuing resolution effects, slow obligation of multi-year reconciliation funds, award protests, or a stronger DoD publication lag would land below the interval, especially below 405B."},{"kind":"forecast","point":485,"ciLow":405,"ciHigh":565}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready, but it needs to tighten resolver wording and better justify the large FY2026 upward update against the registered USAspending first-snapshot target.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"Resolution rule adds ambiguity by allowing revision if the registered snapshot is replaced before capture, while the target contract is a registered-query snapshot with first-print treatment tied to the 2026-10-22 resolution date.","actionRequested":"Restate the rule as resolving to the captured registered-query snapshot for the exact agency 097 endpoint on 2026-10-22, contracts row aggregated_amount times 1e-9, with no later restatements or same-day corrections unless the registration protocol itself defines recapture."},{"rubricItem":"update","severity":"warning","summary":"The point estimate moves from a 450B persistence prior to 485B, but the draft does not use or explicitly rule out current FY2026 USAspending YTD evidence that is directly relevant to a first-snapshot API target.","actionRequested":"Add the latest pre-forecast USAspending FY2026 agency 097 contracts-row evidence available at run time, or explicitly state why the live partial API value was not used and why budget evidence alone supports the +35B update."},{"rubricItem":"interval","severity":"warning","summary":"The interval is based on final FY2015-FY2024 CRS/FPDS volatility, not volatility of the registered USAspending first-snapshot measurement with DoD reporting lag.","actionRequested":"Either justify final FPDS volatility as a proxy for the first-snapshot USAspending target, or widen/adjust the interval to account for API first-print lag and source-definition mismatch."}],"optionalSuggestions":["Clarify whether CRS history excludes categories that USAspending's contracts row may include or omit, since the draft notes the proxy mismatch but does not quantify it.","Name the exact historical sample source for FY2015-FY2019 values used in sigma, because only FY2020-FY2024 values appear in historicalContext.","Make the downside tail explicitly include an unusually incomplete Oct. 22 DoD reporting snapshot, not only lower underlying obligations."]}

Emit the final JSON object only.
