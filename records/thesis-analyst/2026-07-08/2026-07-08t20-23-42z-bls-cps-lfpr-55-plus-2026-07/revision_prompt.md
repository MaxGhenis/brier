# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.lfpr_55_plus
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-lfpr-55-plus-july-2026"
- targetUnit: "percent"

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"us-lfpr-55-plus-july-2026","country":"US","type":"data","title":"US 55+ LFPR, July 2026","question":"BLS Current Population Survey labor force participation rate for people age 55 years and over, seasonally adjusted, July 2026 first print","unit":"percent","pointEstimate":37.1,"ciLow":37.0,"ciHigh":37.2,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS series LNS11324230","resolutionSourceUrl":"https://data.bls.gov/timeseries/LNS11324230","resolutionRule":"Resolve to the first BLS-published July 2026 value for CPS series LNS11324230, Labor Force Participation Rate - 55 Yrs. & over, seasonally adjusted, in percent, as released in the Employment Situation at 8:30 a.m. ET on August 7, 2026. Use the initially published value rounded to the BLS displayed 0.1 percentage point; ignore later revisions.","dataPointId":"bls.cps.lfpr_55_plus.2026-07.first_print","historicalContext":[{"label":"2026-06 latest","value":37.1},{"label":"2026-05","value":37.1},{"label":"2026-04","value":37.1},{"label":"2026-03","value":37.2},{"label":"2026-02","value":37.3}],"drivers":["55+ participation has flattened at 37.1 for three months","recent older-worker participation is near a 21-year low","aggregate June LFPR fell to 61.5","monthly rounded changes are usually 0.0 or 0.1 percentage point"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/series/LNS11324230"],"runAt":"2026-07-08T20:24:14Z","reasoning":[{"kind":"heading","text":"Forecast for BLS CPS 55+ labor force participation, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the seasonally adjusted CPS household-survey series LNS11324230, Labor Force Participation Rate - 55 Yrs. & over, in percent. Resolution is the first BLS July 2026 Employment Situation print, not a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Schedule of Releases for the Employment Situation.","result":"BLS calendar lists July 2026 reference month release on 2026-08-07 at 08:30 AM; June 2026 was released 2026-07-02 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS June 2026 Employment Situation Summary for current labor-market context.","result":"BLS reported June 2026 total nonfarm payroll employment +57,000, unemployment rate 4.2 percent, aggregate labor force participation rate 61.5 percent, and aggregate participation down 0.3 percentage point in June."},{"kind":"tool","tool":"public.history_mirror","call":"Opened FRED mirror page for BLS CPS series LNS11324230 to read recent same-variant values.","result":"FRED/BLS series LNS11324230 shows Jun 2026 37.1, May 2026 37.1, Apr 2026 37.1, Mar 2026 37.2, Feb 2026 37.3, percent, seasonally adjusted; updated 2026-07-02 8:33 AM CDT; next release date 2026-08-07."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Employment Situation Table A-1 for aggregate household-survey participation context.","result":"BLS Table A-1 shows seasonally adjusted total participation rates of Feb 2026 62.0, Mar 2026 61.9, Apr 2026 61.8, May 2026 61.8, Jun 2026 61.5."},{"kind":"text","text":"Reference class and base rate: for a monthly rounded participation-rate series, the best short-horizon reference class is recent same-series one-month changes in the same seasonally adjusted variant. The fetched 55+ path fell 0.2 percentage point from Feb to Jun but was unchanged at 37.1 in Apr, May, and Jun, so persistence at 37.1 is the base rate anchor."},{"kind":"math","text":"Prior/update/interval: persistence prior using recent BLS/FRED same-series history Feb-Jun 2026 = 37.3, 37.2, 37.1, 37.1, 37.1. Successive changes are -0.1, -0.1, 0.0, 0.0, so sample sigma = 0.058 percentage point. Level component = 37.1; momentum component = -0.05 from the Feb-Jun drift but muted because the last three readings were flat; one-off June aggregate LFPR weakness adds small downside risk of -0.02; policy-mechanism effect = 0.00. Final point rounds to 37.1. 80% half-width is roughly 1.28*sigma = 1.28*0.058 = 0.074, widened to 0.10 after rounding outward to BLS 0.1-point display precision, giving 37.0 to 37.2."},{"kind":"text","text":"Upside risk: a rebound in older workers re-entering after the June labor-force drop, or sampling reversal after three flat 37.1 readings, would land above 37.2. Downside risk: another retirement-heavy labor-force exit like June's aggregate participation decline would land below 37.0; outside the interval would require a rounded monthly move of at least 0.2 percentage point from June."},{"kind":"forecast","point":37.1,"ciLow":37.0,"ciHigh":37.2}]}

# Reviewer critique
{
  "summary": "The draft is publication-ready with no blocking issues; it states the official first-print resolver, uses a persistence prior, and keeps the point/interval coherent with the target contract.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Clarify whether the 0.058 percentage-point volatility estimate is based only on the four Feb-Jun 2026 changes or whether a longer historical sample was considered and intentionally rejected.",
    "The interval rationale would be stronger if it named realized volatility from a longer recent window, since four monthly changes is a very small sample."
  ]
}

Emit the final JSON object only.
