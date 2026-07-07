# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.telework_share
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-telework-rate-july-2026"

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
{"slug":"us-telework-rate-july-2026","country":"US","type":"data","title":"US telework share, July 2026","question":"What will BLS CPS Table A-41 first report for July 2026 as the not seasonally adjusted percent of people at work, age 16 years and over, who teleworked or worked at home for pay?","unit":"percent","pointEstimate":21.8,"ciLow":17.8,"ciHigh":25.8,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics, Employment Situation, CPS Table A-41","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea41.htm","resolutionRule":"Resolve to the first BLS Employment Situation release for July 2026, Table A-41, not seasonally adjusted, row 'Total, 16 years and over', column 'People who teleworked or worked at home for pay' under percent distribution. Use the one-decimal percentage printed at initial release; do not use later revisions or corrected same-day replacements unless BLS explicitly withdraws the initial table before publication.","dataPointId":"bls.cps.telework_share.2026-07.first_print","historicalContext":[{"label":"2026-06 BLS A-41 total telework share","value":21.7},{"label":"2024-08 reported total telework share","value":22.8},{"label":"2023-08 reported total telework share","value":19.5}],"drivers":["June 2026 level was 21.7 percent","Hybrid work share remains near post-pandemic plateau","July seasonality is possible because series is not seasonally adjusted","Weak labor-market conditions may reduce worker bargaining power for telework","White-collar occupational mix supports persistence"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/web/empsit/cpseea41.htm","https://www.bls.gov/web/empsit/cpseea43.htm","https://www.marketwatch.com/story/the-job-market-is-getting-tougher-for-workers-but-they-may-be-gaining-in-the-battle-over-remote-work-64fd9408"],"runAt":"2026-07-07T14:07:57Z","reasoning":[{"kind":"heading","text":"US CPS telework share for July 2026"},{"kind":"text","text":"The resolver is BLS CPS Table A-41, not seasonally adjusted, row Total, 16 years and over, percent distribution column for people who teleworked or worked at home for pay. This is the share of people at work, not the share of all employed people, and the table id is A-41."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Employment Situation release schedule for 2026 and checked the July 2026 reference-month row.","result":"BLS schedule lists July 2026 Employment Situation release date as Aug. 07, 2026 at 08:30 AM; June 2026 was Jul. 02, 2026 and August 2026 is Sep. 04, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened current BLS CPS Table A-41 for June 2026 and read the Total, 16 years and over row.","result":"BLS A-41 June 2026 reports total people at work 155,218 thousand, people who teleworked or worked at home for pay 33,701 thousand, teleworked some hours 17,161 thousand, teleworked all hours 16,540 thousand, and percent distribution 21.7 total, 11.1 some hours, 10.7 all hours, 78.3 did not telework."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS CPS Table A-43 to cross-check the same June 2026 telework concept against hours data.","result":"BLS A-43 June 2026 reports total people at work 155,218 thousand, average telework/work-at-home hours for all people at work 5.8, average weekly hours worked 38.3, hours teleworked as 15.1 percent of hours worked, and 33,701 thousand teleworkers with average 26.7 telework hours."},{"kind":"tool","tool":"public.lookup","call":"Checked a public report quoting BLS telework-rate values from the August 2024 jobs report and prior-year comparison.","result":"MarketWatch reported BLS August 2024 telework share 22.8 percent, up from 19.5 percent in August 2023; within August 2024, some-time telework was 11.7 percent and all-time work from home was 11.1 percent."},{"kind":"text","text":"Reference class/base rate: post-2023 BLS CPS telework shares appear centered in the low-20s percent range. The latest official A-41 value, 21.7 percent in June 2026, is below the August 2024 public report of 22.8 percent but above the August 2023 19.5 percent level, so persistence near 22 percent is a stronger prior than a pandemic-style trend extrapolation."},{"kind":"text","text":"Level, momentum, and mechanism split: the level anchor is 21.7. Momentum is weakly flat to slightly positive because June is not unusually high relative to the 2024 reference. One-off effects are limited; July vacations and school schedules can move not-seasonally-adjusted work-at-home status, but the target is broad enough that occupational composition and hybrid policies dominate. Labor-market softening is a mild downside mechanism if employers enforce office attendance more aggressively."},{"kind":"math","text":"Prior/update/interval: persistence prior uses latest BLS A-41 June 2026 = 21.7, with sparse fetched reference-class values Aug 2023 = 19.5, Aug 2024 = 22.8, Jun 2026 = 21.7. Successive changes are +3.3 and -1.1 percentage points; sigma = 3.11 from the sample standard deviation of those changes. I add +0.1 point for mild July/hybrid persistence, giving 21.8. The 80% half-width is roughly 1.28*sigma = 1.28*3.11 = 3.98, rounded to 4.0, so the interval is 21.8 +/- 4.0 = 17.8 to 25.8."},{"kind":"text","text":"Counter-consideration and falsification: upside risk would be a July jump in remote-capable professional work or summer scheduling that pushes the A-41 share above 25.8. Downside risk would be broad return-to-office enforcement or a July shift toward onsite service work that pulls the print below 17.8. Values outside the interval would imply a larger not-seasonally-adjusted or composition shock than seen in the fetched post-2023 reference class."},{"kind":"forecast","point":21.8,"ciLow":17.8,"ciHigh":25.8}]}

# Reviewer critique
{"summary":"Publishable with one main weakness: the interval is mechanically coherent but rests on a very sparse, mismatched volatility sample rather than realized A-41 monthly or July-specific variation.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval half-width is derived from only two changes across sparse August 2023, August 2024, and June 2026 reference points, not realized month-to-month or July-relevant A-41 volatility.","actionRequested":"Either replace the volatility estimate with a small official A-41 monthly or same-month historical sample, or explicitly label the current sigma as a sparse proxy and justify why a 4.0 percentage-point 80% half-width is still appropriate."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact prior/update/interval step names the inputs and math, but the historical sample is too sparse to support the phrase 'larger shock than seen' with much force.","actionRequested":"Qualify the final sentence to say values outside the interval would exceed the limited fetched reference-class variation, or add a broader official-history sample."}],"optionalSuggestions":["Consider removing or downweighting the MarketWatch citation in favor of official archived BLS A-41 values if available.","The +0.1 point July/hybrid persistence adjustment is small enough to keep, but naming it as judgmental rather than model-estimated would improve clarity."]}

Emit the final JSON object only.
