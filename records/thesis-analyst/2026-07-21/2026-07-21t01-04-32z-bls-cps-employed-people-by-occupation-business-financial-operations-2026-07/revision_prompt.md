# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.employed_people_by_occupation.business_financial_operations
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-business-financial-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.business_financial_operations.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Business and financial operations occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.business_financial_operations", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-1eb4254c92a69ec666207bbfc46826262f2310402f51a2e107c50cca573945da.json"
- targetContentHash: "1eb4254c92a69ec666207bbfc46826262f2310402f51a2e107c50cca573945da"
- registrationCommit: "36b3b6b19986083e354c0bd56b0090751cfaeba7"
- registeredAtUtc: "2026-07-21T01:00:49Z"

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
{"slug":"cps-business-financial-employment-july-2026","country":"US","type":"data","title":"US business and financial operations employment, July 2026","question":"What will BLS first report for employed people in business and financial operations occupations in July 2026, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":9.69,"ciLow":9.35,"ciHigh":10.03,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published by BLS for July 2026 in CPS Employment Situation Table A-19, row 'Business and financial operations occupations,' Total age 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Use the first official print without later revisions. The official BLS calendar schedules the July release for August 7, 2026; this conflicts with the registered sourceBinding window ending August 6 but does not change the target.","dataPointId":"bls.cps.employed_people_by_occupation.business_financial_operations.july_2026.first_print","historicalContext":[{"label":"June 2025 NSA","value":10.205},{"label":"April 2026 NSA","value":9.857},{"label":"June 2026 NSA","value":9.72},{"label":"2024 annual average","value":9.945}],"drivers":["June 2026 level persistence","recent weakness in financial activities employment","CPS occupational sampling volatility","July seasonal composition"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/2026/home.htm","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/web/empsit/cpseea44.pdf","https://www.bls.gov/opub/reports/womens-databook/"],"runAt":"2026-07-21T01:05:05Z","reasoning":[{"kind":"heading","text":"July 2026 business and financial operations employment forecast"},{"kind":"text","text":"The resolver is the first July 2026 print in BLS CPS Table A-19 for Business and financial operations occupations, total age 16 years and over, not seasonally adjusted. Table values are thousands and are converted to millions by multiplying by 0.001."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest BLS CPS Employment Situation Table A-19 values for the exact NSA occupational row.","result":"BLS Table A-19 reports 9,720 thousand in June 2026 and 10,205 thousand in June 2025, equal to 9.720 million and 10.205 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch an earlier exact-row observation from BLS CPS occupational tables.","result":"BLS Table A-44 reports 9,857 thousand people in Business and financial operations occupations in April 2026, equal to 9.857 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS annual occupation reference value.","result":"The BLS Women in the Labor Force occupation table reports 9,945 thousand employed in Business and financial operations occupations for the 2024 annual average, equal to 9.945 million."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 Employment Situation publication date on official BLS calendars.","result":"The BLS 2026 release schedule and CPS calendar both list the July 2026 Employment Situation for August 7, 2026 at 8:30 a.m. ET; the registered expected window ends August 6, one day too early."},{"kind":"text","text":"The reference class and base rate are persistence around the latest exact-series level, with substantial CPS sampling noise. The official observations show a lower June 2026 level than June 2025, while the 2024 annual average was 9.945 million."},{"kind":"text","text":"Level effect: anchor at June's 9.720 million. Momentum effect: the observed sequence from 10.205 to 9.857 to 9.720 is negative. One-off effect: noisy CPS occupational allocation argues against extrapolating the full decline. Policy mechanism: no discrete policy change identified, while weak financial-activities payroll evidence supports only a small negative adjustment."},{"kind":"math","text":"Prior/update/interval: persistence model prior = 9.720 million; historical sample = 10.205, 9.857, and 9.720 million. Successive observed changes are -0.348 and -0.137 million, giving RMS sigma = sqrt((0.348^2 + 0.137^2)/2) = 0.264 million. Apply a -0.030 million momentum/financial-activities adjustment and no separate one-off or policy adjustment, yielding 9.690 million. The 80% half-width is approximately 1.28*sigma = 1.28*0.264 = 0.338 million, rounded to 0.34, implying 9.35 to 10.03 million."},{"kind":"text","text":"Upside risk is a rebound in sampled professional hiring or July occupational reclassification, which would land above 10.03 million. Downside risk is continued finance-sector weakness combined with adverse CPS sampling, which would land below 9.35 million and outside the interval."},{"kind":"forecast","point":9.69,"ciLow":9.35,"ciHigh":10.03}]}

# Reviewer critique
{"summary":"The draft is broadly publishable, with the main weakness being that the interval is based on only two irregular historical changes rather than a clearer realized-volatility sample.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval uses an RMS sigma from only two non-monthly changes: June 2025 to April 2026 and April 2026 to June 2026, which is a thin and irregular volatility basis for a July CPS occupational target.","actionRequested":"Either compute the interval from a longer realized-volatility sample for the same Table A-19 row, preferably recent monthly or June-to-July changes, or explicitly state that such a sample was unavailable and defend the two-change proxy as a judgmental uncertainty choice."}],"optionalSuggestions":["Quantify the cited financial-activities weakness or soften it to a qualitative minor adjustment.","Keep the explicit note that the official August 7, 2026 BLS release date conflicts with the registered expectedReleaseWindow ending August 6."]}

Emit the final JSON object only.
