# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.employed_people_by_occupation.transportation_material_moving
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-transport-material-moving-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.transportation_material_moving.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Transportation and material moving occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.transportation_material_moving", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-c022dea86383a42504a748b91016eb3303bf77dbb7184ffbce6566046bcacbbe.json"
- targetContentHash: "c022dea86383a42504a748b91016eb3303bf77dbb7184ffbce6566046bcacbbe"
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
{"slug":"cps-transport-material-moving-employment-july-2026","country":"US","type":"data","title":"US transportation and material-moving employment, July 2026","question":"What will BLS first report for July 2026 employment in transportation and material moving occupations, total age 16+, not seasonally adjusted, in CPS Table A-19?","unit":"millions","pointEstimate":12.01,"ciLow":11.83,"ciHigh":12.19,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published for July 2026 in BLS CPS Employment Situation Table A-19, row 'Transportation and material moving occupations,' Total, 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Retain that first print despite later revisions. The registered resolutionDate is 2026-08-06, but the official BLS calendar now schedules the July release for 2026-08-07; this ledger discrepancy should be corrected without changing the target identity.","dataPointId":"bls.cps.employed_people_by_occupation.transportation_material_moving.july_2026.first_print","historicalContext":[{"label":"March 2026 first print","value":12.214},{"label":"April 2026 first print","value":12.127},{"label":"May 2026 first print","value":12.12},{"label":"June 2026 first print","value":12.01},{"label":"June 2025","value":11.619}],"drivers":["June-level persistence","recent NSA monthly declines","positive year-over-year level","CPS sampling volatility","weak transportation payroll momentum"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/news.release/archives/empsit_04032026.pdf","https://www.bls.gov/news.release/archives/empsit_05082026.pdf","https://www.bls.gov/news.release/archives/empsit_06052026.pdf","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1"],"runAt":"2026-07-21T01:13:26Z","reasoning":[{"kind":"heading","text":"July 2026 CPS transportation and material-moving employment forecast"},{"kind":"text","text":"The resolver is BLS CPS Table A-19, Transportation and material moving occupations, Total age 16+, not seasonally adjusted, first July 2026 print in thousands converted to millions. This is distinct from seasonally adjusted establishment-survey transportation and warehousing payrolls."},{"kind":"tool","tool":"official.lookup","call":"Read the current BLS CPS Table A-19 and June 2026 Employment Situation archive.","result":"BLS reports 12,010 thousand transportation and material-moving workers in June 2026 versus 11,619 thousand in June 2025; total CPS employment was 162,722 thousand in June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read archived March and April 2026 Employment Situation occupation tables.","result":"The first-print transportation and material-moving employment values were 12,214 thousand in March 2026 and 12,127 thousand in April 2026; the corresponding prior-year values were 11,958 thousand and 12,059 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read the archived May 2026 Employment Situation occupation table.","result":"The May 2026 first print was 12,120 thousand, compared with 11,742 thousand in May 2025; BLS also reported May transportation-and-warehousing payroll employment changed by +1,000."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 Employment Situation date on the official BLS release calendar and June release notice.","result":"Both official BLS sources schedule the July 2026 Employment Situation for August 7, 2026 at 8:30 a.m. ET; this is 1 day later than the registered 2026-08-06 resolutionDate."},{"kind":"text","text":"The reference class and base rate are short-horizon forecasts of this noisy NSA CPS occupation level. March-June 2026 declined 12.214 to 12.127 to 12.120 to 12.010 million, while June remained 0.391 million above June 2025. Persistence therefore deserves more weight than extrapolating the latest decline."},{"kind":"math","text":"Prior/update/interval: The model is level persistence at June's 12.010 million. Historical sample uses six successive March-to-June changes from the fetched 2025 and 2026 sequences: +0.101, -0.317, -0.123, -0.087, -0.007, and -0.110 million. Their sample dispersion is sigma = 0.139 million. The recent downward momentum adjustment (-0.04) is offset by positive year-over-year level and mean reversion (+0.04), leaving 12.010 million. The normal 80% half-width is 1.28*sigma = 1.28*0.139 = 0.178 million, rounded to 0.18, implying 11.83 to 12.19 million."},{"kind":"text","text":"A stronger-than-normal summer expansion in delivery, warehousing, or passenger transport is the upside risk and would land above the interval. Broad household-employment weakness, accelerated logistics layoffs, or an adverse CPS sampling swing is the downside risk and could land below the interval; either outcome would be outside the interval."},{"kind":"forecast","point":12.01,"ciLow":11.83,"ciHigh":12.19}]}

# Reviewer critique
{
  "summary": "Draft is broadly publication-ready, with one blocking resolver-date issue caused by a concrete ledger/calendar discrepancy.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft correctly keeps the registered resolutionDate field at 2026-08-06, but the resolutionRule says the ledger discrepancy 'should be corrected,' which conflicts with the instruction to keep the forecast tied to the registered target contract.",
      "actionRequested": "Revise the resolver text to state that the registered target uses 2026-08-06 while official BLS sources schedule the July 2026 Employment Situation for 2026-08-07, without instructing a target change inside the forecast record."
    }
  ],
  "optionalSuggestions": [
    "Clarify that the volatility sample is month-to-month changes from the cited 2025-2026 occupation sequence, not literally March-to-June endpoint changes.",
    "Consider naming the July-specific seasonal prior as ruled out or unavailable, since the current prior is June-level persistence plus recent month-to-month volatility."
  ]
}

Emit the final JSON object only.
