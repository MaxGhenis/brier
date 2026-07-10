# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.job_openings
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-openings-july-2026"
- targetUnit: "millions"
- dataPointId: "bls.jolts.job_openings.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.job_openings", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.job_openings", "sourceUrl": "https://www.bls.gov/news.release/jolts.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"jolts-openings-july-2026","country":"US","type":"data","title":"July 2026 JOLTS Job Openings","question":"What will the U.S. Bureau of Labor Statistics first report as total nonfarm job openings, seasonally adjusted, for July 2026 in the Job Openings and Labor Turnover Survey?","unit":"millions","pointEstimate":7.45,"ciLow":6.67,"ciHigh":8.23,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t01.htm","resolutionRule":"Resolve to the first BLS-published July 2026 seasonally adjusted Total job openings level in Table 1, Job openings levels and rates by industry and region, seasonally adjusted. The BLS table reports levels in thousands; divide by 1000 and report in millions. Use the first print released on September 1, 2026, and do not use later revisions or annual re-estimates.","dataPointId":"bls.jolts.job_openings.july_2026.first_print","historicalContext":[{"label":"May 2026 total job openings SA first/current table","value":7.594},{"label":"Apr 2026 total job openings SA","value":7.585},{"label":"Mar 2026 total job openings SA","value":6.887},{"label":"Feb 2026 total job openings SA","value":6.922},{"label":"Jan 2026 total job openings SA from FRED mirror","value":7.24}],"drivers":["May openings held near April's elevated level","June payroll growth slowed to 57,000","May hires slipped to 5.170 million","Quits rate remained low at 1.9 percent","Layoffs rose modestly but stayed contained"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.t01.htm","https://www.bls.gov/news.release/jolts.t02.htm","https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/news.release/jolts.t05.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/series/JTSJOL"],"runAt":"2026-07-10T04:25:14Z","reasoning":[{"kind":"heading","text":"Forecast for BLS JOLTS total job openings, July 2026 first print"},{"kind":"text","text":"The target is the seasonally adjusted Total job openings level in BLS JOLTS Table 1 for July 2026, reported in thousands and converted to millions. The BLS JOLTS release schedule verifies the July 2026 reference month is scheduled for Sep. 01, 2026 at 10:00 AM, which I use as the resolutionDate. This is the SA Total variant throughout; the series is mirrored by FRED as JTSJOL, but resolution is to BLS Table 1."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 1 for current job openings levels and rates, seasonally adjusted.","result":"BLS Table 1 Total job openings levels in thousands: May 2025 7,310; Feb 2026 6,922; Mar 2026 6,887; Apr 2026 7,585; May 2026 preliminary 7,594; Apr-to-May change +9; May 2026 openings rate 4.6 percent."},{"kind":"tool","tool":"official.lookup","call":"Read FRED JTSJOL as a BLS-source history mirror for the same seasonally adjusted total nonfarm job openings series.","result":"FRED JTSJOL showed May 2026 7,594 thousand, Apr 2026 7,585 thousand, Mar 2026 6,887 thousand, Feb 2026 6,922 thousand, and Jan 2026 7,240 thousand; units are Level in Thousands, Seasonally Adjusted, updated Jun 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 2 for hires, seasonally adjusted, as a current labor-demand confirmation signal.","result":"BLS Table 2 Total hires levels in thousands: May 2025 5,328; Feb 2026 4,899; Mar 2026 5,535; Apr 2026 5,215; May 2026 preliminary 5,170; Apr-to-May change -45; May 2026 hires rate 3.3 percent."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Tables 4 and 5 for quits and layoffs/discharges, seasonally adjusted.","result":"BLS Table 4 Total quits were 3,065 thousand in May 2026 with a 1.9 percent quits rate, up 22 thousand from Apr 2026; BLS Table 5 layoffs and discharges were 1,708 thousand in May 2026 with a 1.1 percent rate, up 41 thousand from Apr 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Employment Situation for June 2026 as a same-labor-market nowcast signal between the May JOLTS release and July target month.","result":"BLS Employment Situation for June 2026 reported total nonfarm payroll employment +57,000, unemployment rate 4.2 percent, unemployed people 7.1 million, labor force participation 61.5 percent, and prior-12-month average payroll change +36,000."},{"kind":"text","text":"Base rate/reference class: for a two-month-ahead level forecast on JOLTS openings, a persistence/random-walk prior usually beats a strong directional call unless payrolls, hires, or layoffs show a decisive break. The latest level is 7.594 million, but the April-to-May plateau after a large March-to-April jump and softer June payroll signal argue for modest mean reversion rather than extrapolating the April surge."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 openings 7.594 million. Historical sample for volatility = fetched Jan-May 2026 same-series levels 7.240, 6.922, 6.887, 7.585, 7.594 million, giving monthly changes -0.318, -0.035, +0.698, +0.009. Sample sigma = 0.431 million. Adjustment components: -0.06 million for May hires falling to 5.170 million, -0.04 million for quits still low at 1.9 percent and layoffs up to 1.708 million, -0.04 million for June payroll slowing to +57,000, -0.004 rounding/level judgment, so point = 7.594 - 0.144 = 7.45 million. For a two-month horizon, half-width = 1.28 * sqrt(2) * sigma = 1.28 * 1.414 * 0.431 = 0.78 million, so 80 percent interval = 7.45 +/- 0.78 = [6.67, 8.23]."},{"kind":"text","text":"Counter-considerations: upside risk is that April's professional-and-business-services openings rebound persists and July postings remain above 8 million; downside risk is a retrenchment from weak hires and slow payroll growth that pulls openings toward early-2026 levels. A broad white-collar reopening plus low layoffs would land above the interval; a summer demand shock with hires and openings both falling would land below the interval."},{"kind":"forecast","point":7.45,"ciLow":6.67,"ciHigh":8.23}]}

# Reviewer critique
{
  "summary": "The draft is mostly publication-ready, with the main issue being resolver URL/source alignment to the canonical ledger binding.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft resolves to BLS Table 1 and states the first-print rule clearly, but its resolutionSourceUrl is the direct table URL while the ledger sourceBinding sourceUrl is the BLS release URL ending in jolts.nr0.htm.",
      "actionRequested": "Align resolutionSourceUrl with the canonical ledger source URL or explicitly state that the direct Table 1 URL is the table view of the same first-print BLS release."
    }
  ],
  "optionalSuggestions": [
    "Broaden the volatility sample beyond Jan-May 2026 if available, since four monthly changes make the 80% interval mechanically fragile.",
    "Make the upside and downside tails slightly more numeric, for example naming approximate levels above 8.23 million and below 6.67 million."
  ]
}

Emit the final JSON object only.
