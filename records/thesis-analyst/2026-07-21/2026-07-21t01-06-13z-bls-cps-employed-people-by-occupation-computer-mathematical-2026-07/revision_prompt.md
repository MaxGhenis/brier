# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.employed_people_by_occupation.computer_mathematical
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-computer-math-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.computer_mathematical.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Computer and mathematical occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.computer_mathematical", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-9008e5bd3c60b6d015f5989bcf403009c9ea1156c41007faec60f49194626eca.json"
- targetContentHash: "9008e5bd3c60b6d015f5989bcf403009c9ea1156c41007faec60f49194626eca"
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
{"slug":"cps-computer-math-employment-july-2026","country":"US","type":"data","title":"US computer and math employment, July 2026","question":"How many people were employed in computer and mathematical occupations in July 2026, not seasonally adjusted, in the BLS CPS first print?","unit":"millions","pointEstimate":6.98,"ciLow":6.68,"ciHigh":7.28,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the total number of employed people age 16 and over in the 'Computer and mathematical occupations' row of CPS Employment Situation Table A-19 for July 2026, not seasonally adjusted, as first published by BLS on August 7, 2026. Convert thousands to millions by multiplying by 0.001 and retain three decimal places. Ignore subsequent revisions. The registered source window ending August 6 conflicts with the official BLS calendar and June release notice, both of which specify August 7.","dataPointId":"bls.cps.employed_people_by_occupation.computer_mathematical.july_2026.first_print","historicalContext":[{"label":"2021 annual average","value":5.688},{"label":"2022 annual average","value":6.171},{"label":"2023 annual average","value":6.502},{"label":"2024 annual average","value":6.386},{"label":"2025 annual average","value":6.711},{"label":"June 2025","value":6.602},{"label":"June 2026","value":6.95}],"drivers":["June 2026 level of 6.950 million","positive longer-run occupational employment trend","CPS sampling volatility","weak tech hiring versus resilient incumbent employment"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/cps/cpsaat09.htm","https://www.bls.gov/cps/data/aa2023/cpsaat09.htm","https://www.bls.gov/cps/aa2022/cpsaat09.htm","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf"],"runAt":"2026-07-21T01:06:38Z","reasoning":[{"kind":"heading","text":"July 2026 computer and mathematical employment forecast"},{"kind":"text","text":"The target is the total, age 16 and over, for Computer and mathematical occupations in CPS Table A-19, reported in thousands and not seasonally adjusted. Resolution uses the strict August 7 first print and the table's 0.001 conversion to millions."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest BLS CPS Table A-19 observation and matched year-earlier value.","result":"BLS Table A-19 reports 6,950 thousand employed in June 2026 and 6,602 thousand in June 2025 for Computer and mathematical occupations."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent BLS annual-average occupation levels from CPS Table 9.","result":"BLS CPS Table 9 reports 6,386 thousand in 2024 and 6,711 thousand in 2025; the 2025 figure is an 11-month average because October data were not collected."},{"kind":"tool","tool":"official.lookup","call":"Fetch earlier official CPS annual-average reference-class observations.","result":"Official CPS Table 9 archives report 5,688 thousand in 2021, 6,171 thousand in 2022, and 6,502 thousand in 2023."},{"kind":"tool","tool":"official.lookup","call":"Verify the official release date from the BLS CPS calendar and latest Employment Situation notice.","result":"The BLS calendar lists the July 2026 Employment Situation for August 7, 2026, and the June release specifies August 7, 2026 at 8:30 a.m. ET; this is 1 day after the registered expected window end."},{"kind":"text","text":"The outside-view base rate is gradual growth with substantial CPS noise: annual-average employment rose from 5.688 million in 2021 to 6.711 million in 2025, while June 2026 was 0.348 million above June 2025."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: the 6.950 million June level supplies the persistence anchor; positive multi-year growth adds 0.05 million; weak technology hiring subtracts 0.02 million; no identified July-specific policy or classification change warrants another adjustment."},{"kind":"math","text":"Prior/update/interval: persistence model prior = June 2026's 6.950 million; historical sample = 2021-2025 annual averages of 5.688, 6.171, 6.502, 6.386, and 6.711 million; successive changes are +0.483, +0.331, -0.116, and +0.325 million, giving sigma = 0.236 million. Adjustments are +0.050 million for longer-run momentum and -0.020 million for soft hiring, yielding 6.950 + 0.050 - 0.020 = 6.980 million. The normal 80% half-width is 1.28*sigma = 1.28*0.236 = 0.302 million, implying 6.678 to 7.282 million, rounded to 6.68 to 7.28 million."},{"kind":"text","text":"Upside risk comes from faster AI-related hiring, labor-force re-entry, or favorable CPS sampling and would land above the interval if employment exceeds 7.28 million. Downside risk comes from layoffs, weak hiring, or adverse sampling and would land below the interval if employment is under 6.68 million; either outcome would be outside the interval."},{"kind":"forecast","point":6.98,"ciLow":6.68,"ciHigh":7.28}]}

# Reviewer critique
{"summary":"Draft is mostly publishable on target identity and reasoning structure, but the interval method needs a stronger target-relevant volatility basis before publication.","requiredFixes":[{"rubricItem":"interval","severity":"blocking","summary":"The 80% interval is based on four changes in annual-average employment, which is a smoothed trend sample and does not directly measure month-to-month CPS Table A-19 first-print volatility for a July level forecast.","actionRequested":"Recompute or justify the interval using target-relevant realized volatility, preferably recent month-to-month or June-to-July changes for the same Table A-19 occupation series; if annual changes are retained, explicitly add a sampling/monthly-noise component and show the resulting 80% bounds."}],"optionalSuggestions":["Keep the August 7 official release-date discrepancy explicit because it conflicts with the registered expectedReleaseWindow ending August 6.","Tie the weak-tech-hiring adjustment to a cited public labor-market indicator or state that it is a judgmental small offset."]}

Emit the final JSON object only.
