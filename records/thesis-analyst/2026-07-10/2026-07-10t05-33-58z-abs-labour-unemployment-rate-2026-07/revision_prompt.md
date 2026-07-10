# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.labour.unemployment_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-unemployment-rate-july-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.labour.unemployment_rate.australia.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "abs.labour.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "abs.labour.unemployment_rate", "sourceUrl": "https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release", "table": "Australian Bureau of Statistics Labour Force, Australia, June 2026", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-8777624fc229aeba35f9494cd622f11dec8bc5be8f0b7a967d5b1aedcd5e88c3.json"
- targetContentHash: "8777624fc229aeba35f9494cd622f11dec8bc5be8f0b7a967d5b1aedcd5e88c3"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

# Source hints
- Use ABS release calendar and official monthly CPI indicator pages.
- Australia CPI indicator rates print to one decimal.
- Resolution source should be the ABS release page.

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
{"slug":"australia-unemployment-rate-july-2026","country":"AU","type":"data","title":"Australia unemployment rate July 2026","question":"What will the Australian Bureau of Statistics report as Australia's seasonally adjusted unemployment rate for July 2026 in Labour Force, Australia, first print?","unit":"percent","pointEstimate":4.5,"ciLow":4.2,"ciHigh":4.7,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Australian Bureau of Statistics Labour Force, Australia, July 2026","resolutionSourceUrl":"https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/jul-2026","resolutionRule":"Resolve to the national seasonally adjusted unemployment rate (%) for Australia in ABS Labour Force, Australia, July 2026, first published on 20/08/2026 at 11:30am AEST. Use the first-print value as ABS prints it, normally to one decimal percent, and ignore later revisions or later corrected reposts.","dataPointId":"abs.labour.unemployment_rate.australia.july_2026.first_print","historicalContext":[{"label":"May 2026 seasonally adjusted unemployment rate","value":4.355949},{"label":"April 2026 seasonally adjusted unemployment rate","value":4.48134},{"label":"March 2026 seasonally adjusted unemployment rate","value":4.278411},{"label":"February 2026 seasonally adjusted unemployment rate","value":4.30171},{"label":"January 2026 seasonally adjusted unemployment rate","value":4.082555}],"drivers":["Latest ABS first-print anchor is May 2026 seasonally adjusted unemployment rate of 4.4%.","Trend unemployment rate has edged up to 4.4%, keeping the underlying level above early-2026 readings.","May reversed part of April's spike, so persistence should not extrapolate April's 4.5% mechanically.","Two unreleased monthly prints remain before July, so sampling volatility is material."],"sourceContext":["https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release","https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia"],"runAt":"2026-07-10T05:34:16Z","reasoning":[{"kind":"heading","text":"Australia July 2026 unemployment rate forecast"},{"kind":"text","text":"Framing and exact resolver: this is the ABS Labour Force, Australia national seasonally adjusted unemployment rate for July 2026, first print. The ledger table label says June 2026, but the dataPointId and question target July 2026; I keep the target tied to July 2026 and resolve from the July 2026 ABS release."},{"kind":"tool","tool":"official.lookup","call":"ABS Labour Force, Australia release schedule page","result":"Fetched future releases: June 2026 releases 23/07/2026 11:30am AEST; July 2026 releases 20/08/2026 11:30am AEST; August 2026 releases 24/09/2026 11:30am AEST."},{"kind":"tool","tool":"official.lookup","call":"ABS Labour Force, Australia latest release key statistics for May 2026","result":"Fetched May 2026 seasonally adjusted unemployment rate 4.4%, April 2026 4.5%, unemployed people 671,300 in May, employment 14,738,800 in May, participation rate 66.7%."},{"kind":"tool","tool":"official.lookup","call":"ABS latest release unemployment-rate graph table, seasonally adjusted Australia variant","result":"Fetched same-variant unrounded seasonally adjusted unemployment rates: Jan-26 4.082555, Feb-26 4.301710, Mar-26 4.278411, Apr-26 4.481340, May-26 4.355949; trend rates Mar-26 4.327248, Apr-26 4.348103, May-26 4.361273."},{"kind":"tool","tool":"official.lookup","call":"ABS latest release survey-date table","result":"Fetched July 2026 collection timing: Jul-26 reference week starts 28 June 2026 and ends 11 July 2026; enumeration starts 5 July 2026 and ends 25 July 2026."},{"kind":"text","text":"Variant control: all anchors and dispersion inputs are the ABS national seasonally adjusted unemployment rate for Australia, not trend, original, state, or sex-specific rates; trend is used only as a directional current-condition cross-check."},{"kind":"text","text":"The reference class and base rate are recent monthly moves in the same ABS seasonally adjusted unemployment-rate series. From Jul-23 through May-26, the rate rose from 3.697010 to 4.355949, but individual monthly changes were noisy, including Apr-26 up to 4.481340 and May-26 down to 4.355949."},{"kind":"text","text":"Level and momentum: May's 4.355949 is the cleanest public anchor. The trend estimate of 4.361273 and year-on-year unemployment-rate increase of 0.3 percentage points argue for a level around 4.4 rather than a reversion to early-2026 levels near 4.1."},{"kind":"text","text":"Prior/update/interval: persistence prior from May-26 seasonally adjusted 4.355949, historical sample Jul-23 to May-26 same-series monthly changes, adjustment components +0.04 for two months of trend drift and +0.04 for weaker year-on-year labour-market slack, interval method based on monthly successive-change dispersion where sigma = 0.146 percentage points and 1.28*sigma = 0.187; I widen to about 0.25 because the forecast is two monthly prints ahead and July collection is still in progress, giving final implied bounds around 4.2 to 4.7 after first-print rounding."},{"kind":"math","text":"Point calculation: 4.355949 May anchor + 0.04 trend drift + 0.04 slack adjustment = 4.435949, rounded to a one-decimal first-print forecast of 4.5%. Interval calculation: center about 4.45 with half-width about 0.25 gives 4.20 to 4.70, reported as ciLow 4.2 and ciHigh 4.7."},{"kind":"text","text":"Counter-considerations: upside risk is a June or July employment loss with participation holding near 66.7%, which would land above the interval. Downside risk is another May-like fall in unemployed people plus lower participation, which would land below the interval. A one-off rotation-group or survey-modernisation effect outside normal sampling variability could also push the first print outside the interval."},{"kind":"forecast","point":4.5,"ciLow":4.2,"ciHigh":4.7}]}

# Reviewer critique
{"summary":"The draft is mostly publication-ready, but the final point estimate is not coherent with its stated arithmetic and rounding rule.","requiredFixes":[{"rubricItem":"coherence","severity":"blocking","summary":"The stated point calculation is 4.355949 + 0.04 + 0.04 = 4.435949, which rounds to 4.4% to one decimal, not 4.5%.","actionRequested":"Either revise the adjustment arithmetic so the unrounded forecast supports a 4.5% first-print point estimate, or change the point estimate and final forecast fields to match the stated calculation."}],"optionalSuggestions":["Tighten the interval sentence by explicitly saying the two-month sigma is approximately sqrt(2) times the monthly-change sigma, then rounded/widened to the reported 4.2-4.7 bounds.","Keep the ledger table-label discrepancy note; it appropriately preserves the July 2026 target while flagging the apparent June-label error."]}

Emit the final JSON object only.
