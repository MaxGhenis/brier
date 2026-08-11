# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.real_earnings.avg_hourly_mom.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-09-16", "start": "2026-09-08"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-16", "start": "2026-09-08"}, "field": "bls.real_earnings.avg_hourly_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.real_earnings.avg_hourly_mom", "sourceUrl": "https://www.bls.gov/news.release/realer.t01.htm", "table": "U.S. Bureau of Labor Statistics Real Earnings Table A-1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-d131156b732a5d2eeed80a873f599d8c0a54453f2c8eb3c2ce0d53822486ba73.json"
- targetContentHash: "d131156b732a5d2eeed80a873f599d8c0a54453f2c8eb3c2ce0d53822486ba73"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

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
{"slug":"us-real-avg-hourly-earnings-mom-august-2026","country":"US","type":"data","title":"US real average hourly earnings MoM, August 2026","question":"What will the BLS first print for seasonally adjusted real average hourly earnings of all employees on private nonfarm payrolls, over-the-month percent change, be for August 2026?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.6,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-09-11","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 print for August 2026, row 'Real average hourly earnings' under 'OVER-THE-MONTH PERCENT CHANGE' for all employees on private nonfarm payrolls, seasonally adjusted. Use the value as published in percent, normally to one decimal place, on the scheduled September 11, 2026 release; ignore later revisions.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-08.first_print","historicalContext":[{"label":"June 2026 real average hourly earnings MoM, latest BLS Table A-1","value":0.8},{"label":"May 2026 real average hourly earnings MoM, latest BLS Table A-1","value":-0.2},{"label":"April 2026 real average hourly earnings MoM, latest BLS Table A-1","value":-0.5},{"label":"July 2026 nominal average hourly earnings, BLS Employment Situation","value":37.62},{"label":"July 2026 unemployment rate, BLS Employment Situation","value":4.1}],"drivers":["Nominal average hourly earnings growth slowed to near flat in July","August CPI is likely to absorb most nominal wage growth","June real-earnings jump was CPI-deflation driven and unlikely to persist","Recent real hourly earnings changes have high month-to-month CPI noise"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/archives/realer_02132026.htm","https://www.bls.gov/news.release/archives/realer_03112026.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/news.release/archives/realer_06102026.htm","https://www.bls.gov/news.release/archives/realer_09112025.htm","https://www.bls.gov/news.release/archives/realer_12182025.htm","https://www.bls.gov/news.release/empsit.htm"],"runAt":"2026-08-11T13:07:36Z","reasoning":[{"kind":"heading","text":"Forecast for BLS real average hourly earnings MoM, August 2026"},{"kind":"text","text":"Resolver is the all-employees, private nonfarm payrolls, seasonally adjusted variant in BLS Real Earnings Table A-1. The target is the first-print over-the-month percent change for August 2026, not later revised CES or CPI database values."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings release schedule lookup for August 2026 reference month","result":"BLS schedule lists Real Earnings for August 2026 with release date September 11, 2026 and release time 08:30 AM ET; this verifies resolutionDate 2026-09-11."},{"kind":"tool","tool":"official.lookup","call":"BLS current Real Earnings Table A-1 for recent all-employees real hourly earnings and components","result":"Latest Table A-1 shows real average hourly earnings levels of 11.25 in April 2026, 11.23 in May 2026, and 11.32 in June 2026; over-the-month percent changes were -0.5, -0.2, and 0.8; CPI-U changes were 0.6, 0.5, and -0.4; nominal average hourly earnings changes were 0.2, 0.3, and 0.3."},{"kind":"tool","tool":"official.lookup","call":"BLS archived Real Earnings releases for the recent reference class","result":"Archived Table A-1 prints used for the reference class include July 2025 0.2, August 2025 -0.1, September 2025 -0.1, December 2025 -0.3, January 2026 0.3, February 2026 0.2, March 2026 -0.6, April 2026 -0.5, May 2026 -0.2, and June 2026 0.8 percent real average hourly earnings month-over-month."},{"kind":"tool","tool":"official.lookup","call":"BLS July 2026 Employment Situation for nominal wage and labor-market setup before August","result":"The July 2026 Employment Situation reported nonfarm payroll employment -23,000, unemployment rate 4.1 percent, average hourly earnings for all employees on private nonfarm payrolls 37.62 dollars, a +2 cent change, and average weekly hours 34.3."},{"kind":"text","text":"Base rate/reference class: the recent official real-hourly-earnings MoM sample is centered near zero, with a mean around -0.03 percent and median -0.10 percent. Because this is already a change series, the sample values themselves are the realized dispersion input."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the recent BLS Table A-1 monthly real average hourly earnings change sample [0.2, -0.1, -0.1, -0.3, 0.3, 0.2, -0.6, -0.5, -0.2, 0.8], mean = -0.03 and median = -0.10. Update components: July nominal AHE was only +2 cents to 37.62, suggesting softer wage momentum; for August I assume nominal AHE about +0.25 percent and CPI-U about +0.30 percent, so real hourly earnings is approximately 0.25 - 0.30 = -0.05 percent, rounded to -0.1. Sample dispersion gives sigma = 0.42 percentage points, and 1.28*sigma = 0.54 percentage points; applying that to -0.1 gives about -0.64 to 0.44, rounded to an 80 percent interval of -0.6 to 0.4."},{"kind":"text","text":"Upside risk is a soft August CPI print or a rebound in hourly earnings after July's +2 cents, which would land above the interval if real hourly earnings rose more than 0.4 percent. Downside risk is another hot CPI print or weak mix-adjusted wages, which would land below the interval if the published real change is less than -0.6 percent. Outside the interval would most likely require an energy-driven CPI surprise or a large composition shock in payroll earnings."},{"kind":"forecast","point":-0.1,"ciLow":-0.6,"ciHigh":0.4}]}

# Reviewer critique
{"summary":"The draft is publication-ready: resolver, first-print date, prior, update logic, volatility-based interval, tails, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Clarify why the historical reference class uses a non-contiguous 10-month sample rather than all recent first prints, or state that it is a selected recent sample.","Consider noting that the point remains anchored near the prior median, so the inside-view wage/CPI update is directional but not a large move."]}

Emit the final JSON object only.
