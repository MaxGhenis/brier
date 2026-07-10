# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.retail_sales.volume_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-retail-sales-volume-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "ons.retail_sales.volume_mom.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:retail_sales:2026-05:volume_mom", "releasePolicy": "first_print", "sourceSeriesId": "ons.retail_sales.volume_mom", "sourceUrl": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026", "table": "Retail sales, Great Britain: May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-c06ec0e3a9bd14e9983b654f0fce440dc106ef4863d6a5d7624e3ebfa0f49893.json"
- targetContentHash: "c06ec0e3a9bd14e9983b654f0fce440dc106ef4863d6a5d7624e3ebfa0f49893"
- registeredAtUtc: "2026-07-10T05:58:27Z"

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode fast)


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
{"slug":"ons-retail-sales-volume-mom-june-2026","country":"UK","type":"data","title":"ONS retail sales volume m/m, June 2026","question":"ONS Retail Sales Index, Great Britain, all retailing quantity bought volume, seasonally adjusted month-on-month percentage growth for June 2026, first print","unit":"percent_growth","pointEstimate":0.2,"ciLow":-1.2,"ciHigh":1.6,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"Office for National Statistics Retail sales, Great Britain: June 2026","resolutionSourceUrl":"https://www.ons.gov.uk/releases/retailsalesgreatbritainjune2026","resolutionRule":"Resolve to the first ONS-published estimate of seasonally adjusted all-retailing quantity bought retail sales volume month-on-month percentage growth for June 2026 in Retail sales, Great Britain: June 2026 or its linked Retail Sales Index time-series dataset. Use the first official print released on 24 July 2026 at 7:00am UK time; do not use later revisions. Values are percentage growth rates, recorded to the ONS published precision. The registered ledger source URL appears to point to May 2026 and its country field says US; this forecast remains tied to the June 2026 ONS target by slug and dataPointId, but the exact public resolver is the ONS June 2026 release page.","dataPointId":"ons.retail_sales.volume_mom.june_2026.first_print","historicalContext":[{"label":"May 2026 m/m first estimate in latest ONS bulletin","value":1.2},{"label":"April 2026 m/m revised in May bulletin","value":-1.0},{"label":"March 2026 m/m revised in May bulletin","value":0.7},{"label":"February 2026 m/m revised in March bulletin","value":-0.6},{"label":"January 2026 m/m revised in March bulletin","value":1.8},{"label":"December 2025 m/m in December bulletin","value":0.4}],"drivers":["May 2026 strength creates mean-reversion risk for June","Hot weather and promotions supported non-store and department-store volumes in May","Fuel-stockpiling reversal made April unusually weak and May partly rebound-driven","Seasonally adjusted all-retailing volumes are volatile month to month","ONS annual seasonal-adjustment improvements scheduled with the June release add first-print uncertainty"],"sourceContext":["https://www.ons.gov.uk/releases/retailsalesgreatbritainjune2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/april2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/march2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/february2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsales"],"runAt":"2026-07-10T06:06:10Z","reasoning":[{"kind":"heading","text":"June 2026 ONS retail sales volume m/m forecast"},{"kind":"text","text":"Framing and exact resolver: forecast the ONS Retail Sales Index all-retailing quantity bought volume, Great Britain, seasonally adjusted monthly percentage change for June 2026, first print. The public ledger registration appears internally inconsistent because the country is listed as US and the source URL/sourceBinding point to May 2026, while the question, slug, and dataPointId are for the ONS June 2026 Great Britain release."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS upcoming release page for Retail Sales; Great Britain: June 2026.","result":"ONS release page states Retail Sales; Great Britain: June 2026 release date is 24 July 2026 at 7:00am and describes it as a first estimate of retail sales in volume and value terms, seasonally and non-seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS Retail sales, Great Britain: May 2026 bulletin for latest all-retailing volume monthly growth and source variant.","result":"Latest bulletin released 19 June 2026 says retail sales volumes rose 1.2% in May 2026, following a fall of 1.0% in April 2026 and a rise of 0.7% in March 2026; three-month growth to May was 0.4%, year-on-year growth was 3.2%, survey response rate was 57.0%, and turnover coverage was 85.0%."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS March, February, January, and December retail-sales bulletins for recent official monthly reference points.","result":"ONS March 2026 bulletin reported March 2026 up 0.7%, February 2026 down 0.6%, and January 2026 up 1.8%; ONS January 2026 bulletin reported December 2025 up 0.4%; ONS December 2025 bulletin reported November 2025 down 0.1% and October 2025 down 0.8%."},{"kind":"text","text":"Reference class/base rate: the recent official same-variant reference class is the seasonally adjusted all-retailing volume monthly growth rate itself, not value sales, online-only sales, or non-seasonally adjusted volumes. The last six fetched values used for the base rate are 0.4, 1.8, -0.6, 0.7, -1.0, and 1.2, averaging about 0.42 percentage points."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS dataset and quality notes for variant and first-print context.","result":"Retail Sales Index time series dataset ID DRSI was released 19 June 2026 with next release 24 July 2026; the May bulletin says seasonal adjustment uses X-13ARIMA-SEATS, the June release will implement annual seasonal-adjustment improvements on 24 July 2026, and May 2026 response metrics were 57.0% returned forms and 85.0% turnover coverage."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is the six-month official same-variant mean, (0.4 + 1.8 - 0.6 + 0.7 - 1.0 + 1.2) / 6 = 0.42. Adjustment components: -0.30 for payback after May's 1.2% weather/promotion rebound and earlier fuel volatility, +0.10 for continued warm-weather support to summer and non-store demand, yielding 0.22 and rounded to 0.2. Interval method uses realized dispersion of monthly change values themselves for this change/flow target: sample sigma = 1.06 from [0.4, 1.8, -0.6, 0.7, -1.0, 1.2]; 80% half-width is roughly 1.28*sigma = 1.36, rounded to 1.4, so 0.2 +/- 1.4 gives -1.2 to 1.6."},{"kind":"text","text":"Counter-considerations: upside risk is a June heatwave, outdoor-goods demand, or online/non-store strength that keeps momentum near May's pace and would land above the interval if growth exceeds 1.6%. Downside risk is consumer caution, reversal of May promotion pull-forward, or another fuel/non-food setback that would land below the interval if growth is less than -1.2%."},{"kind":"forecast","point":0.2,"ciLow":-1.2,"ciHigh":1.6}]}

# Reviewer critique
{
  "summary": "Draft is publishable in method and coherence terms, with one blocking metadata/source-binding issue caused by the ledger mismatch that must be made explicit in final fields.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft uses the correct ONS June 2026 release page and 24 July 2026 first-print date, but the canonical ledger sourceBinding points to the May 2026 bulletin and field official_release:ons:retail_sales:2026-05:volume_mom.",
      "actionRequested": "Keep slug and dataPointId tied to June 2026, but explicitly flag the ledger resolver/sourceBinding as erroneous and ensure publication metadata does not silently imply that the May 2026 bulletin resolves the June 2026 value."
    },
    {
      "rubricItem": "coherence",
      "severity": "warning",
      "summary": "The draft country field is UK while the canonical ledger country field is US; the reasoning notes this discrepancy, but the JSON field no longer matches the ledger contract.",
      "actionRequested": "Either align the emitted country field with the target contract while noting the ledger country error in reasoning, or document that the catalog metadata should be corrected before publication."
    },
    {
      "rubricItem": "coherence",
      "severity": "warning",
      "summary": "One historicalContext label says 'December 2025 m/m in December bulletin', while the reasoning says December 2025 was reported in the January 2026 bulletin.",
      "actionRequested": "Correct the historicalContext label so the cited month and bulletin timing are consistent."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether the 80% interval is intended as central 80% and say so directly.",
    "The six-month volatility basis is acceptable but thin; add a short note that the narrow sample was chosen for current-regime relevance.",
    "The tail scenarios are concrete enough, but could name which retail components would drive an upside or downside miss."
  ]
}

Emit the final JSON object only.
