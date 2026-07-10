# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-11"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-11.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US Continued Claims, Jul 11 2026","question":"What will the U.S. Department of Labor first report for seasonally adjusted continued claims, week ending 2026-07-11, in the Unemployment Insurance Weekly Claims release?","unit":"millions","pointEstimate":1.815,"ciLow":1.775,"ciHigh":1.855,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260723","resolutionRule":"Resolve to the first published seasonally adjusted continued claims, also labeled insured unemployment, for the week ending July 11, 2026, in the Department of Labor ETA Unemployment Insurance Weekly Claims release scheduled for July 23, 2026. Convert the reported count to millions by multiplying by 1e-6. Use the first official print only; later revisions or ALFRED/FRED vintage updates after the first release do not change resolution.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 continued claims SA latest","value":1.81},{"label":"2026-06-20 continued claims SA prior revised","value":1.802},{"label":"2026-06-13 continued claims SA prior rounded","value":1.81},{"label":"2026-06-06 continued claims SA prior rounded","value":1.81},{"label":"2026-05-30 continued claims SA prior rounded","value":1.8},{"label":"2026-05-23 continued claims SA prior revised","value":1.77}],"drivers":["SA continued claims have been clustered near 1.80 to 1.82 million","latest initial claims for week ending 2026-07-04 were 215000, not signaling a layoff break","June payroll growth slowed to 57000, supporting mild persistence in benefit duration","recent weekly continued-claims changes imply about 0.03 million two-week uncertainty"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260723","https://www.dol.gov/ui/data.pdf","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA","https://apnews.com/article/8d1f553fde8124606b2e3350fe789776","https://www.wsj.com/economy/jobs/u-s-jobless-claims-edged-lower-last-week-f35e8718","https://www.wsj.com/economy/jobs/u-s-jobless-claims-fell-last-week-a62436da","https://www.wsj.com/economy/jobs/u-s-jobless-claims-fell-last-week-ceec6b9f","https://www.wsj.com/economy/jobs/u-s-jobless-claims-rose-last-week-70b53ca9"],"runAt":"2026-07-10T03:42:04Z","reasoning":[{"kind":"heading","text":"Forecast for DOL CCSA week ending 2026-07-11"},{"kind":"text","text":"Framing and exact resolver: this is the DOL ETA seasonally adjusted continued claims series, FRED/ALFRED code CCSA, for the week ending 2026-07-11. The target is the first print in millions, not a later revised vintage; all anchors below refer to the same seasonally adjusted continued-claims variant."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL ETA release timing for Unemployment Insurance Weekly Claims and the target lag structure.","result":"The official release slot for the weekly claims report covering continued claims for week ending 2026-07-11 is 2026-07-23 at 8:30 ET; the continued-claims reference week lags the initial-claims week by 1 week."},{"kind":"tool","tool":"official.lookup","call":"Checked the most recent DOL-reported weekly claims release and public mirrors of the same DOL figures.","result":"For the release on 2026-07-09, initial claims for week ending 2026-07-04 were 215000, down 2000 from 217000, and continued claims for week ending 2026-06-27 were about 1810000, up 8000 from a revised prior level near 1802000."},{"kind":"tool","tool":"official.lookup","call":"Pulled recent CCSA history from ALFRED/FRED mirror and contemporaneous DOL-release reporting for the SA continued-claims variant.","result":"Recent SA continued-claims levels in millions: 2026-05-23 1.770, 2026-05-30 1.800, 2026-06-06 1.810, 2026-06-13 1.810 to 1.820 depending on first/revised rounding, 2026-06-20 about 1.802 to 1.810, 2026-06-27 1.810."},{"kind":"tool","tool":"official.lookup","call":"Checked broader labor-market current-release context from public DOL/BLS reporting.","result":"The June 2026 employment report showed 57000 nonfarm payroll jobs added and an unemployment rate of 4.2 percent; weekly initial claims were 215000 for 2026-07-04 after 215000 for 2026-06-27 and roughly 226000 to 229000 in mid-June."},{"kind":"text","text":"Reference class and base rate: for a stable level series like SA continued claims, the best short-horizon base rate is persistence plus recent weekly drift. The last six rounded weekly observations sit in a tight 1.77 to 1.82 million range, with no latest initial-claims breakout suggesting a sharp move by the 2026-07-11 continued-claims week."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the latest first/revised level around 1.810 million for 2026-06-27; historical sample uses recent weekly CCSA levels 1.770, 1.800, 1.810, 1.815 midpoint for 2026-06-13 rounding, 1.802, 1.810. Adjustment components are +0.003 million for slower June payrolls and longer duration, +0.002 million for the latest +8000 weekly move, and 0.000 million for stable initial claims, giving point 1.810 + 0.005 = 1.815. Weekly-change sigma from the fetched recent history is about 0.022 million; for a two-week-ahead level, sigma = 0.031 million after sqrt(2) scaling, and 1.28*sigma = 0.040 million, so the 80% interval is 1.815 +/- 0.040 = [1.775, 1.855]."},{"kind":"text","text":"Upside risk is a sudden rise in benefit duration or a jump in July layoffs that would push continued claims above 1.855 million. Downside risk is faster exits from UI or seasonal-adjustment noise that would pull the first print below 1.775 million. A recessionary layoff spike or a large seasonal-factor miss would land outside the interval."},{"kind":"forecast","point":1.815,"ciLow":1.775,"ciHigh":1.855}]}

# Reviewer critique
{
  "summary": "The draft is publishable after tightening the resolver citation and making the volatility calculation reproducible.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolver text is mostly correct, but the draft cites the future DOL release URL as source context before the release exists.",
      "actionRequested": "Keep the target tied to the July 23, 2026 first-print DOL ETA release, but label the July 23 URL as the intended resolver URL or release placeholder rather than current evidence."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The interval method is stated, but the claimed recent weekly-change sigma of 0.022 million is not directly reproducible from the listed six rounded observations.",
      "actionRequested": "Show the exact weekly changes or historical sample used for the 0.022 million sigma, or revise the sigma and interval calculation to match the displayed sample."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that ALFRED/FRED is only a mirror/vintage mechanism and that the official DOL first print controls if there is any discrepancy.",
    "Clarify whether the 2026-06-13 and 2026-06-20 inputs are first prints or revised values, since the forecast targets a first print.",
    "The tail scenarios are acceptable, but could name approximate levels for a high-claims and low-claims path over the two missing weeks."
  ]
}

Emit the final JSON object only.
