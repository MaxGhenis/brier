# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.telework_share
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-telework-rate-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.cps.telework_share.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "bls.cps.telework_share", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.telework_share", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea41.htm", "table": "U.S. Bureau of Labor Statistics, Employment Situation, CPS Table A-41", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-6cf0d9882448a529f400c8923c7c59cd04582d25bc948a6c7238eb38f11374f5.json"
- targetContentHash: "6cf0d9882448a529f400c8923c7c59cd04582d25bc948a6c7238eb38f11374f5"
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
{"slug":"us-telework-rate-august-2026","country":"US","type":"data","title":"US telework rate, August 2026","question":"What will BLS CPS Table A-41 first print report as the not seasonally adjusted telework rate, percent of total people at work, for Total, 16 years and over, August 2026?","unit":"percent","pointEstimate":22.1,"ciLow":21.5,"ciHigh":22.7,"confidence":0.8,"resolutionDate":"2026-09-04","resolutionSource":"U.S. Bureau of Labor Statistics, Employment Situation, CPS Table A-41","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea41.htm","resolutionRule":"Resolve to the first official BLS Employment Situation supplemental CPS Table A-41 print for August 2026, not seasonally adjusted, row Total, 16 years and over, Percent distribution column People who teleworked or worked at home for pay. Use the value as displayed in percent, normally to one decimal place, and do not revise for later table updates or subsequent vintages.","dataPointId":"bls.cps.telework_share.2026-08.first_print","historicalContext":[{"label":"2026-07 latest","value":22.2},{"label":"2026-06","value":21.7},{"label":"2026-05","value":21.8},{"label":"2026-04","value":21.7},{"label":"2025-08 prior August","value":22.1}],"drivers":["July 2026 level was 22.2 percent","Recent 2026 readings clustered from 21.7 to 22.7 percent after January","August seasonal reference changes were modest in 2023-2025","Not seasonally adjusted CPS telework series has visible month-to-month sampling noise","Remote-work structure appears stable, with limited reason for a one-month break"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea41.htm","https://data.bls.gov/timeseries/LNU0201B46B","https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1","https://www.bls.gov/cps/telework.htm"],"runAt":"2026-08-11T13:09:27Z","reasoning":[{"kind":"heading","text":"US CPS telework share, August 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS CPS telework rate, series LNU0201B46B, for August 2026 on CPS Table A-41. The variant is not seasonally adjusted and national, measured as people who teleworked or worked at home for pay as a percent of total people at work, Total, 16 years and over."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Employment Situation CPS Table A-41 current table at https://www.bls.gov/web/empsit/cpseea41.htm.","result":"Fetched July 2026 Table A-41 row Total, 16 years and over: total people at work 153,406 thousand; people who teleworked or worked at home for pay 34,079 thousand; teleworked some hours 17,134 thousand; teleworked all hours 16,946 thousand; percent distribution teleworked 22.2, some hours 11.2, all hours 11.0, did not telework 77.8."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS public time series page for LNU0201B46B at https://data.bls.gov/timeseries/LNU0201B46B.","result":"Fetched LNU0201B46B values: 2026 Jan 23.0, Feb 22.7, Mar 22.6, Apr 21.7, May 21.8, Jun 21.7, Jul 22.2; 2025 Jul 22.1, Aug 22.1, Sep 22.3, Nov 22.9, Dec 22.5; 2024 Jul 23.0, Aug 22.8, Sep 23.7."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Schedule of Releases for the Employment Situation at https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1.","result":"Fetched official schedule: Reference Month August 2026 has Release Date Sep. 04, 2026 and Release Time 08:30 AM; July 2026 was Aug. 07, 2026 at 08:30 AM; September 2026 is scheduled Oct. 02, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS telework concepts page at https://www.bls.gov/cps/telework.htm.","result":"Fetched measurement context: BLS added CPS telework questions starting in October 2022; the telework rate is the number of people who telework or work at home for pay as a percentage of those employed and at work during the survey reference week; the published monthly estimates are not seasonally adjusted."},{"kind":"text","text":"Base rate and reference class: I use the official monthly LNU0201B46B series since October 2022, emphasizing 2024-2026 because the series has settled into a post-pandemic plateau. The base rate is persistence around the recent 21.7-22.7 percent band rather than a trend extrapolation from the 2022-2024 rise."},{"kind":"text","text":"Level and momentum: July 2026 printed 22.2 after 21.7 in June and 21.8 in May. The 2026 year-to-date average through July is about 22.24, but April-July average is about 21.85, so I center just below July at 22.1 rather than chasing the one-month rebound."},{"kind":"text","text":"Seasonal and one-off adjustment: August changes in the available official series were small: July to August was -0.4 in 2023, -0.2 in 2024, and 0.0 in 2025. Applying roughly -0.1 to -0.2 to the July 2026 reading of 22.2 gives 22.0-22.1; the stable work-from-home structure argues against a larger mechanical move."},{"kind":"math","text":"Prior/update/interval: persistence prior = July 2026 LNU0201B46B level 22.2, historical sample = official LNU0201B46B recent monthly changes Feb-Jul 2026 of -0.3, -0.1, -0.9, +0.1, -0.1, +0.5 percentage points plus August seasonal changes of -0.4, -0.2, and 0.0 from 2023-2025; adjustment components = -0.1 for August seasonality and no material structural policy shock, giving point 22.1. For interval sizing on recent successive changes, sigma = sqrt((0.09+0.01+0.81+0.01+0.01+0.25)/6) = 0.44 percentage point, so 1.28*sigma = 0.57; rounded around 22.1 gives an 80% interval of 21.5 to 22.7."},{"kind":"text","text":"Counter-considerations: upside risk is a survey mix or white-collar employment composition shift that keeps July's rebound and would land above the interval if the first print is above 22.7. Downside risk is a vacation/reference-week or composition effect similar to April 2026 that would land below the interval if the first print is below 21.5. Outside the interval would most likely indicate sampling noise or a genuine change in who was at work during the August CPS reference week, not a slow trend."},{"kind":"forecast","point":22.1,"ciLow":21.5,"ciHigh":22.7}]}

# Reviewer critique
{"summary":"The draft is publication-ready on the substantive forecast rubric, with a clear first-print BLS resolver, persistence prior, modest update, volatility-based 80% interval, coherent JSON fields, and no apparent leakage.","requiredFixes":[],"optionalSuggestions":["Confirm the registered target's stored resolutionDate matches the cited BLS release-calendar date of 2026-09-04, since the provided ledger context shows only a 2026-09-03 to 2026-09-11 expectedReleaseWindow.","Consider naming the interval method as RMS recent monthly change volatility rather than generic sigma, because the calculation divides by n and is not a sample standard deviation."]}

Emit the final JSON object only.
