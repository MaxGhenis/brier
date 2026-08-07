# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usaspending.dod.prime_award_obligations
- period: FY2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-award-obligations-fy2026"
- country: "US"
- targetUnit: "billions USD"
- dataPointId: "usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "obligations", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) award summary, prime award obligations, fiscal year to date", "transform": {"factor": 1e-09, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907.json"
- targetContentHash: "59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907"
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
{"slug":"us-dod-prime-award-obligations-fy2026","country":"US","type":"data","title":"US DoD prime award obligations FY2026","question":"What will USAspending API v2 report as Department of Defense agency 097 prime award obligations for fiscal year 2026 in the first registered query snapshot?","unit":"usd_billions","pointEstimate":532,"ciLow":493,"ciHigh":571,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2 agency 097 awards endpoint","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026","resolutionRule":"Resolve to the first official USAspending API v2 response for /api/v2/agency/097/awards/?fiscal_year=2026 after the FY2026 period-12 Data Broker publication window, using the obligations field for agency 097 prime award obligations, multiplied by 1e-09 and rounded to the nearest 0.1 billion USD. Do not revise for later USAspending updates or corrections.","dataPointId":"usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2023 first-print comparable USAspending agency 097 awards obligations","value":463.8},{"label":"FY2024 first-print comparable USAspending agency 097 awards obligations","value":454.6},{"label":"FY2025 first-print comparable USAspending agency 097 awards obligations","value":505.2},{"label":"FY2026 current fiscal-year-to-date check as of run date","value":500.6}],"drivers":["FY2025 DoD prime award obligations were near $505B on the same USAspending agency-awards basis","FY2026 defense budget authority and procurement/RDT&E support a moderate nominal increase","DoD procurement reporting lag makes late-year catch-up important for the first post-period snapshot","The range is sized from realized annual flow dispersion rather than a hand-rounded band"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2023","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2024","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2025","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026","https://tfx.treasury.gov/data-transparency/resources","https://files.gao.gov/multimedia/Federal_Government_Contracting-FY2025/index.html"],"runAt":"2026-08-07T18:20:00Z","reasoning":[{"kind":"heading","text":"US DoD prime award obligations FY2026"},{"kind":"text","text":"Framing and exact resolver: this is the USAspending API v2 agency 097 awards endpoint, fiscal_year=2026, obligations field, transformed from USD to billions USD. I keep the ledger target's 2026-10-22 resolution date and first-print snapshot rule."},{"kind":"tool","tool":"official.lookup","call":"Checked Treasury TFX resources page for Data Broker Reporting Submission Dates FY26 and the USAspending publication timing note.","result":"TFX listed Data Broker Reporting Submission Dates FY26 as a 37.42 KB official document; for FY2026 period 12 the target period ends 2026-09-30, the registered public window is 2026-10-15 to 2026-10-22, and the resolver uses 2026-10-22."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending API v2 agency 097 awards endpoint for recent full fiscal years on the same obligations field and 1e-09 transform.","result":"Fetched comparable obligations: FY2021 421.5 billion USD, FY2022 447.2 billion USD, FY2023 463.8 billion USD, FY2024 454.6 billion USD, FY2025 505.2 billion USD."},{"kind":"tool","tool":"official.lookup","call":"Checked USAspending/official procurement context for the current FY2026 and reporting lag context.","result":"The current FY2026 public context showed about 500.6 billion USD in DoD award/contract spending already visible before final period-12 publication, while USAspending notes DoD contract data can have a 90-day publication lag."},{"kind":"tool","tool":"official.lookup","call":"Checked GAO FY2025 governmentwide contracting snapshot for an official outside benchmark on defense-agency contract obligations.","result":"GAO reported FY2025 governmentwide contract obligations of 793 billion USD and defense-agency products plus services of 253 + 238 = 491 billion USD, excluding small missing/other categories and excluding other transaction agreements of 18.2 billion USD."},{"kind":"text","text":"Base rate / reference class: the same-variant USAspending agency 097 prime-award obligations history is a steadily rising but noisy annual flow. The base rate from FY2021-FY2025 is centered in the high-$450B range, with FY2025 stepping up to just above $500B."},{"kind":"text","text":"Variant control: anchors are DoD agency 097 prime award obligations or the nearest official defense-agency contract-obligation cross-check; the resolution itself remains the USAspending agency-awards obligations field, not budgetary resources, outlays, FRED, or news."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2025 same-endpoint value 505.2; historical sample = FY2021-FY2025 values 421.5, 447.2, 463.8, 454.6, 505.2; adjustment components = +14.0 for nominal defense topline/inflation, +8.0 for procurement and RDT&E mix, +4.8 for late DoD reporting catch-up and FY2026 current run-rate, giving point 532.0. For the flow-series interval I used the values themselves: sample sigma = 30.5, so 80% half-width = 1.28*sigma = 1.28*30.5 = 39.0; point 532.0 +/- 39.0 gives 493.0 to 571.0."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger late-September procurement closeout, supplemental defense funds, or faster DoD reporting that would land above the interval; downside risk is continuing-resolution friction, delayed award reporting, or deobligation cleanup that would land below the interval. A material accounting or API classification change would be outside the interval risk in either direction."},{"kind":"forecast","point":532,"ciLow":493,"ciHigh":571}]}

# Reviewer critique
{"summary":"Draft is publishable with one nonblocking interval-method issue: the resolver and prior/update structure are clear, but the uncertainty band should better justify using level dispersion as forecast volatility.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on the sample sigma of FY2021-FY2025 obligation levels, which mixes trend/level dispersion with actual forecast uncertainty and annual volatility.","actionRequested":"Either recompute the interval from annual changes, persistence residuals, or another realized-volatility/error proxy, or explicitly state why level dispersion is the chosen uncertainty proxy for this target."}],"optionalSuggestions":["Clarify whether the first-print snapshot is taken on 2026-10-22 or the first successful API fetch after that date, matching the registered query snapshot wording.","Briefly state why the FY2026 year-to-date value is not being treated as near-final despite DoD reporting lag."]}

Emit the final JSON object only.
