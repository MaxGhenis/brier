# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usaspending.dod.small_business_contract_obligation_share
- period: FY2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-small-business-contract-obligation-share-fy2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "usaspending.dod.small_business_contract_obligation_share.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[time_period.fiscal_year={fiscal_year}].aggregated_amount", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.search.spending_over_time.dod.contracts.small_business_obligation_share", "sourceUrl": "https://api.usaspending.gov/api/v2/search/spending_over_time/", "table": "USAspending API v2 advanced search, small-business share of DoD prime-contract obligations, fiscal year to date", "transform": {"agency": {"name": "Department of Defense", "tier": "toptier", "type": "awarding"}, "awardTypeCodes": ["A", "B", "C", "D"], "denominatorRecipientTypeNames": [], "factor": 1, "fiscalYear": "{fiscal_year}", "group": "fiscal_year", "numeratorRecipientTypeNames": ["small_business"], "operation": "ratio_percent", "requestMethod": "POST", "spendingLevel": "transactions"}}
- targetRegistrationPath: "records/targets/2026-08-07-b7ebec1228518b70de1c1c2f93d0b0084f260ea989d72d0b12968b776082e8cf.json"
- targetContentHash: "b7ebec1228518b70de1c1c2f93d0b0084f260ea989d72d0b12968b776082e8cf"
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
{"slug":"us-dod-small-business-contract-obligation-share-fy2026","country":"US","type":"data","title":"DoD Small-Business Contract Obligation Share FY2026","question":"What will USAspending API v2 first-print registered-query snapshot show for the Department of Defense FY2026 small-business share of prime-contract obligations, using award type codes A/B/C/D, awarding toptier agency Department of Defense, grouped by fiscal year, with numerator recipient_type_names=[small_business] and denominator without recipient type restriction?","unit":"percent","pointEstimate":20.2,"ciLow":18.6,"ciHigh":21.8,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2 advanced search spending_over_time registered query snapshot","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/search/spending_over_time/","resolutionRule":"Resolve to the first registered-query snapshot value for FY2026 from USAspending API v2 /api/v2/search/spending_over_time/ using the registered transform: percent = 100 * aggregated_amount for DoD prime-contract transactions with recipient_type_names=[small_business] divided by aggregated_amount for the same DoD prime-contract transactions without a recipient type filter. Use award_type_codes A, B, C, and D; awarding toptier agency Department of Defense; group=fiscal_year; spending_level=transactions; fiscalYear=2026. Round to the agency/API displayed precision available in the resolver artifact. Do not revise after the first registered snapshot.","dataPointId":"usaspending.dod.small_business_contract_obligation_share.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2025 GSA all-prime DoD small-business share, computed from fetched dollars","value":19.79},{"label":"FY2024 GSA all-prime DoD small-business share, computed from fetched dollars","value":20.81},{"label":"FY2020 DoD historical prime-contract small-business share","value":33.4},{"label":"FY2019 DoD historical prime-contract small-business share","value":38.6},{"label":"FY2018 DoD historical prime-contract small-business share","value":33.5}],"drivers":["Recent all-prime DoD small-business share near 20 percent","FY2025 small-business dollars rose but total non-small DoD obligations also rose","DoD/SBA small-business policy goals support persistence rather than collapse","Defense procurement mix can swing with large weapons and services obligations","USAspending registered query differs from SBA eligible-dollar scorecard denominator"],"sourceContext":["https://api.usaspending.gov/api/v2/search/spending_over_time/","https://api.usaspending.gov/api/v2/references/submission_periods/","https://www.gsa.gov/system/files/FPDS%20Report.pdf","https://www.gsa.gov/system/files/Final%20Data%20Report_%20%20FY%202024%20FPDS%20GSA%20Report.pdf","https://business.defense.gov/About/Goals-and-Performance/","https://api.usaspending.gov/docs/endpoints"],"runAt":"2026-08-07T18:00:00Z","reasoning":[{"kind":"heading","text":"DoD FY2026 small-business prime-contract obligation share"},{"kind":"text","text":"Framing and exact resolver: the target is the USAspending API v2 registered-query snapshot for Department of Defense FY2026 prime-contract obligations, not the SBA eligible-dollar scorecard. The numerator is recipient_type_names=[small_business]; the denominator is the same A/B/C/D DoD prime-contract query without recipient type restriction. The registered target sets the bounded snapshot resolutionDate to 2026-10-22; the official USAspending submission-period endpoint currently shows published periods only through FY2026 fiscal month 9, so the exact FY2026 year-end period was not yet visible there during this run."},{"kind":"tool","tool":"official.lookup","call":"Opened USAspending API endpoint index and endpoint documentation for /api/v2/search/spending_over_time/ and /api/v2/references/submission_periods/.","result":"Fetched endpoint facts: /api/v2/search/spending_over_time/ is listed as POST and returns transaction aggregated amounts for Spending Over Time; /api/v2/references/submission_periods/ returned FY2026 fiscal month 9 with period_start_date 2026-06-01, period_end_date 2026-06-30, submission_due_date 2026-07-31, certification_due_date 2026-08-15, and submission_reveal_date 2026-07-31T01:20:01.167456Z."},{"kind":"tool","tool":"official.lookup","call":"Opened GSA FY2025 FPDS report required by Section 15(h)(3)(A)(ii) of the Small Business Act and extracted the Department of Defense rows.","result":"Fetched FY2025 DoD all-prime dollars: Small Business Concerns in aggregate = $103,824,203,209.59 from 2,365,483 contracts; Other Than Small Business Concerns in aggregate without exclusions = $420,887,508,061.02 from 57,454,020 contracts; computed small-business share = 103.82420320959 / (103.82420320959 + 420.88750806102) * 100 = 19.79 percent."},{"kind":"tool","tool":"official.lookup","call":"Opened GSA FY2024 FPDS report required by Section 15(h)(3)(A)(ii) of the Small Business Act and extracted the Department of Defense rows.","result":"Fetched FY2024 DoD all-prime dollars: Small Business Concerns in aggregate = $99,891,645,499.74 from 2,233,536 contracts; Other Than Small Business Concerns in aggregate without exclusions = $380,230,594,309.65 from 87,148,396 contracts; computed small-business share = 99.89164549974 / (99.89164549974 + 380.23059430965) * 100 = 20.81 percent."},{"kind":"tool","tool":"official.lookup","call":"Opened the DoD Office of Industrial Base Growth goals and performance page for small-business prime-contract history and current goals context.","result":"Fetched DoD historical prime-contract small-business performance points: FY2020 Total Awards $165.2B, SB Awards $55.1B, share 33.4 percent; FY2019 Total Awards $161.5B, SB Awards $62.3B, share 38.6 percent; FY2018 Total Awards $124.5B, SB Awards $41.7B, share 33.5 percent. Fetched DoD prime-contracting goal row: FY2023 goal 22.43 percent, FY2024 goal 22.43 percent, FY2025 goal 23.17 percent."},{"kind":"text","text":"Base rate/reference class: the best exact-variant recent base rate is the GSA all-prime FPDS Department of Defense ratio, because it uses all prime procurements without the SBA goaling exclusions and is closer to the USAspending denominator than the SBA eligible-dollar scorecard. The two fetched exact-variant observations average 20.30 percent, with FY2025 at 19.79 percent and FY2024 at 20.81 percent."},{"kind":"math","text":"Prior/update/interval: persistence prior = average of fetched exact-variant all-prime FY2024 and FY2025 shares = (20.81 + 19.79) / 2 = 20.30 percent; historical sample = GSA FPDS all-prime FY2024-FY2025 plus DoD published older prime-contract reference points for regime checks; adjustment components = -0.3 percentage point for FY2025 downward momentum and large non-small defense obligation growth, +0.2 percentage point for DoD small-business goal pressure and program continuity, net -0.1; point = 20.30 - 0.10 = 20.20 percent. For the exact-variant fetched successive change, sigma = 1.02 percentage points from |19.79 - 20.81|; 1.28*sigma = 1.31 percentage points. I widen to a 1.60 percentage point half-width because the USAspending registered-query recipient-type filter may not exactly match the GSA FPDS report classification, giving 20.2 - 1.6 = 18.6 and 20.2 + 1.6 = 21.8."},{"kind":"text","text":"Level and momentum: the FY2025 all-prime DoD share fell about 1.02 percentage points from FY2024 even though small-business dollars increased by about $3.93B, because the other-than-small denominator increased by about $40.66B. That argues for a point below the two-year average but not a break far below 20 percent."},{"kind":"text","text":"Policy and mechanism: upside risk is a stronger FY2026 small-business set-aside mix or slower growth in major-prime obligations, which could move the registered USAspending share toward or above 21.8 percent. Downside risk is a surge in large weapons, IT, construction, or services obligations to non-small primes, which would land below the interval. Outside the interval would require either a larger denominator-mix shock than FY2025 or a material query-classification mismatch between USAspending recipient_type_names and FPDS small-business status."},{"kind":"forecast","point":20.2,"ciLow":18.6,"ciHigh":21.8}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the interval/sample language and denominator comparability caveat.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The interval labels a single FY2024-to-FY2025 change as sigma, which overstates the statistical basis for an 80% interval.","actionRequested":"Rephrase the interval method as a one-change persistence error proxy plus explicit query-classification uncertainty, or add more realized comparable changes if available."},{"rubricItem":"model_prior","severity":"warning","summary":"The historical sample mixes recent GSA all-prime ratios with older DoD performance points that may use a different denominator/regime.","actionRequested":"State clearly that the older DoD points are non-comparable regime checks and are not used quantitatively in the prior or volatility estimate."}],"optionalSuggestions":["Mention that resolution uses the registered FY2026 snapshot as of the bounded window ending 2026-10-22, not later USAspending revisions.","Keep the final math step's implied 80% bounds exactly aligned with the JSON fields."]}

Emit the final JSON object only.
