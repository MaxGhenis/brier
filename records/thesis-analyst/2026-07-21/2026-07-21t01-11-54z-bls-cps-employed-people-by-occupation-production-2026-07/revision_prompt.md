# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.employed_people_by_occupation.production
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-production-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.production.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Production occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.production", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-e6122e1a77edbc28a7204a5b63f7b17fc1f4147009df5e69f180e83c7894b601.json"
- targetContentHash: "e6122e1a77edbc28a7204a5b63f7b17fc1f4147009df5e69f180e83c7894b601"
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
{"slug":"cps-production-employment-july-2026","country":"US","type":"data","title":"US production employment, July 2026","question":"What will BLS first report for people employed in production occupations in July 2026, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":7.559,"ciLow":7.368,"ciHigh":7.75,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-13/A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first BLS-published July 2026 total employed value for Production occupations in CPS Employment Situation Table A-13/A-19, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Preserve the first print despite later revisions; round to three decimal places. The registered 2026-08-06 resolutionDate conflicts with the official BLS calendar and June release, which schedule publication for 2026-08-07; the forecast remains tied to the registered target date.","dataPointId":"bls.cps.employed_people_by_occupation.production.july_2026.first_print","historicalContext":[{"label":"January 2026 first print","value":7.905},{"label":"February 2026 first print","value":7.742},{"label":"March 2026 first print","value":7.685},{"label":"April 2026 first print","value":7.883},{"label":"May 2026 first print","value":7.912},{"label":"June 2026 first print","value":7.759},{"label":"July 2025 first print","value":7.662}],"drivers":["Recent CPS production-employment level","Typical July seasonal decline in NSA data","Household-survey sampling volatility","Soft year-over-year production employment"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/news.release/archives/empsit_06052026.htm","https://www.bls.gov/news.release/archives/empsit_05082026.htm","https://www.bls.gov/news.release/archives/empsit_08012025.pdf","https://www.bls.gov/schedule/2026/home.htm"],"runAt":"2026-07-21T01:12:14Z","reasoning":[{"kind":"heading","text":"July 2026 CPS production-occupation employment forecast"},{"kind":"text","text":"The target is the first BLS print for total people employed in Production occupations, July 2026, not seasonally adjusted, from CPS Employment Situation Table A-13/A-19. BLS reports thousands; the resolver multiplies by 0.001. Later revisions do not replace the first print."},{"kind":"tool","tool":"official.lookup","call":"Read BLS archived Employment Situation releases for January through March 2026, Table A-13.","result":"Fetched first-print production-occupation employment of 7,905 thousand in January 2026, 7,742 thousand in February, and 7,685 thousand in March."},{"kind":"tool","tool":"official.lookup","call":"Read BLS archived Employment Situation releases for April through June 2026, Table A-13.","result":"Fetched first-print production-occupation employment of 7,883 thousand in April 2026, 7,912 thousand in May, and 7,759 thousand in June."},{"kind":"tool","tool":"official.lookup","call":"Read the archived July 2025 Employment Situation, Table A-13, for a same-month seasonal comparison.","result":"Fetched July production-occupation employment of 7,889 thousand in 2024 and 7,662 thousand in 2025; the June 2025 official table value was 7,938 thousand, implying a 276-thousand June-to-July decline in 2025."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 Employment Situation publication date using the official BLS release calendar and June 2026 release.","result":"The official calendar lists Friday, August 7, 2026 at 8:30 AM ET, and the June release repeats August 7, 2026; this is 1 day after the ledger resolutionDate of August 6."},{"kind":"text","text":"The reference class/base rate is persistence around the latest NSA CPS occupation level with a negative July seasonal update. The January-June sequence is choppy but centered near 7.8 million, while July 2025 fell 0.276 million from June and remained 0.227 million below July 2024."},{"kind":"math","text":"Prior/update/interval: persistence prior = June 2026 first print of 7.759 million; historical sample = January-June 2026 first prints [7.905, 7.742, 7.685, 7.883, 7.912, 7.759]. Successive changes are [-0.163, -0.057, +0.198, +0.029, -0.153] million, whose sample standard deviation is sigma = 0.149 million. Apply a -0.200 million update for July seasonality and weak year-over-year level momentum, with no separate policy adjustment: 7.759 - 0.200 = 7.559. The normal 80% half-width is 1.28*sigma = 1.28*0.149 = 0.191 million, implying bounds 7.559 +/- 0.191 = [7.368, 7.750]."},{"kind":"text","text":"Upside risk is an abrupt rebound like April 2026, which could put the print above 7.750 million. Downside risk is a July seasonal drop materially larger than 2025's 0.276 million or renewed manufacturing weakness; a decline exceeding 0.391 million from June would land below the interval. Either outcome would be outside the interval."},{"kind":"forecast","point":7.559,"ciLow":7.368,"ciHigh":7.75}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, but it should tighten resolver wording to the canonical Table A-19 target and better support the large July seasonal adjustment with a broader or explicitly limited seasonal sample.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolver/source text says Table A-13/A-19 even though the ledger binding is cpseea19.htm, CPS Employment Situation Table A-19, field Production occupations; the official release date also appears to be 2026-08-07 while the ledger resolutionDate is 2026-08-06.","actionRequested":"State the resolver as canonical Table A-19/cpseea19.htm and first-print July 2026 value, keep resolutionDate tied to the registered 2026-08-06 ledger date, and keep the official-calendar discrepancy as an explicit note rather than blending A-13/A-19 in the resolver."},{"rubricItem":"update","severity":"warning","summary":"The -0.200 million movement from June persistence is material and is mainly justified by one June-to-July comparison from 2025 plus a qualitative weak-momentum claim.","actionRequested":"Either add a short multi-year June-to-July NSA production-occupation seasonal sample, or explicitly say the update is mostly a judgmental shrinkage from the single 2025 seasonal drop and recent soft year-over-year context."}],"optionalSuggestions":["Include the June 2025 value in historicalContext if it remains central to the seasonal update.","Clarify that archived A-13 references are evidence lookups only if older releases used different table numbering, while the target resolver remains Table A-19."]}

Emit the final JSON object only.
