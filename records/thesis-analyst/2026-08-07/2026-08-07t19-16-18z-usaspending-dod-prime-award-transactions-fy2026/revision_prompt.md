# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usaspending.dod.prime_award_transactions
- period: FY2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-award-transactions-fy2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usaspending.dod.prime_award_transactions.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "transaction_count", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.transaction_count", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) award summary, transaction count, fiscal year to date", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-41dd79f388ca4e5be3ffe71c6c375afc0cc75e0393ae1cb4d6347241b5637d8c.json"
- targetContentHash: "41dd79f388ca4e5be3ffe71c6c375afc0cc75e0393ae1cb4d6347241b5637d8c"
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
{"slug":"us-dod-prime-award-transactions-fy2026","country":"US","type":"data","title":"DoD Prime Award Transactions FY2026","question":"What will the USAspending API v2 agency 097 awards transaction_count be for Department of Defense prime awards in FY2026, in millions, in the first registered query snapshot?","unit":"millions","pointEstimate":3.86,"ciLow":3.47,"ciHigh":4.25,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2 agency award summary","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026","resolutionRule":"Resolve from the first official USAspending API v2 registered query snapshot for agency 097 with fiscal_year=2026 in the registered release window, using the transaction_count field multiplied by 0.000001 and rounded to millions; do not revise for later API updates or corrections.","dataPointId":"usaspending.dod.prime_award_transactions.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2021 official API transaction_count, millions","value":4.566},{"label":"FY2022 official API transaction_count, millions","value":4.318},{"label":"FY2023 official API transaction_count, millions","value":4.084},{"label":"FY2024 official API transaction_count, millions","value":3.965},{"label":"FY2025 official API transaction_count, millions","value":3.786}],"drivers":["FY2026 DoD award flow is tracking close to recent years but below FY2021-FY2022 highs","DoD procurement and operations funding remains large enough to support a near-flat transaction count","Administrative reporting and late fiscal-year modification volume can move the final count materially","First registered USAspending API snapshot may miss some lagged procurement corrections"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2021","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2022","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2023","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2024","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2025","https://api.usaspending.gov/api/v2/references/submission_periods/","https://api.usaspending.gov/docs/endpoints"],"runAt":"2026-08-07T19:16:36Z","reasoning":[{"kind":"heading","text":"Forecast DoD FY2026 Prime Award Transactions"},{"kind":"text","text":"Framing and exact resolver: this is the USAspending API v2 agency 097 awards endpoint, fiscal_year=2026, field transaction_count, transformed to millions. The registered target uses a resolve-by-bound window ending 2026-10-22; the official submission-period endpoint visible this run lists recent reveal and certification dates but not yet the future FY2026 fiscal-month-12 row, so I keep the ledger resolutionDate and note that the exact future reveal row was not observable yet."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending agency 097 awards endpoint for completed fiscal years 2021 and 2022, reading transaction_count and converting by 1e-6.","result":"Fetched FY2021 transaction_count 4566000 = 4.566 million; FY2022 transaction_count 4318000 = 4.318 million."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending agency 097 awards endpoint for completed fiscal years 2023 and 2024, same agency 097 and same transaction_count field.","result":"Fetched FY2023 transaction_count 4084000 = 4.084 million; FY2024 transaction_count 3965000 = 3.965 million."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending agency 097 awards endpoint for FY2025 and the public submission-period schedule context.","result":"Fetched FY2025 transaction_count 3786000 = 3.786 million; submission_periods showed FY2026 fiscal_month 9 and FY2025 fiscal_month 12 entries, with FY2025 fiscal_month 12 submission_reveal_date 2025-12-06T02:57:27Z."},{"kind":"text","text":"Base rate/reference class: the same-source annual flow reference class is FY2021-FY2025 DoD prime award transaction counts, ranging from 3.786 million to 4.566 million, with a mean of 4.144 million and a downward drift of about 0.195 million per year over the last four year-to-year steps."},{"kind":"text","text":"Level and momentum: the downtrend from 4.566 million in FY2021 to 3.786 million in FY2025 argues against returning to the early-period level; however, FY2025 to FY2026 should not mechanically extend the full decline because transaction reporting appears to be settling near a high-3-million annual run rate."},{"kind":"text","text":"Policy and mechanism adjustment: FY2026 defense spending remains large, so the main policy effect is on composition and timing rather than a collapse in transaction activity. I add a small +0.07 million adjustment versus pure recent-trend persistence for late-year modifications and awards tied to ongoing defense procurement activity."},{"kind":"math","text":"Prior/update/interval: persistence prior is FY2025 at 3.786 million; historical sample is FY2021-FY2025 same USAspending API annual values of 4.566, 4.318, 4.084, 3.965, and 3.786 million; adjustment components are +0.04 million for stabilization after the FY2021-FY2025 decline and +0.03 million for FY2026 late-year defense award/modification flow, giving point 3.786 + 0.074 = 3.860 million. For the flow-series interval I use dispersion of the annual values themselves: sigma = 0.305 million, so 80% half-width is about 1.28*sigma = 1.28*0.305 = 0.390 million, implying 3.860 +/- 0.390 = 3.470 to 4.250 million."},{"kind":"text","text":"Counter-considerations: upside risk is a heavier-than-usual late FY2026 modification surge or delayed FY2025-FY2026 procurement data clearing into the first snapshot, which would land above the interval if the count exceeds 4.25 million. Downside risk is a reporting lag, shutdown-related processing disruption, or sustained simplification of award actions, which would land below the interval if the count is under 3.47 million."},{"kind":"forecast","point":3.86,"ciLow":3.47,"ciHigh":4.25}]}

# Reviewer critique
{"summary":"Draft is broadly publishable, with one interval-method weakness around using level dispersion rather than realized forecast error or change volatility.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on dispersion of FY2021-FY2025 levels, which mixes trend and level differences and is not clearly realized volatility or first-snapshot uncertainty.","actionRequested":"Revise the interval note to either use year-over-year change volatility/forecast-error volatility, or explicitly justify level dispersion as a conservative uncertainty proxy and mention first-snapshot revision/reporting-lag uncertainty."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft references downward drift but does not clearly say whether a trend model was used or ruled out before choosing FY2025 persistence plus adjustments.","actionRequested":"Add one sentence stating that a linear trend/extrapolation prior was considered and partially discounted, with persistence chosen as the anchor because the decline appears to be flattening."}],"optionalSuggestions":["Clarify that historical FY2021-FY2025 values are current API readings unless they are known to be first registered snapshots.","Keep the resolver wording aligned to the ledger phrase first official registered query snapshot within the 2026-10-15 to 2026-10-22 window."]}

Emit the final JSON object only.
