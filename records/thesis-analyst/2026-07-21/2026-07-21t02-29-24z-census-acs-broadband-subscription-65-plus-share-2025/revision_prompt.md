# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.acs.broadband_subscription_65_plus.share
- period: 2025
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "broadband-subscription-65-plus-2025"
- country: "US"
- targetUnit: "percent"
- dataPointId: "census.acs.broadband_subscription_65_plus.share.2025.first_print"
- resolutionDate: "2026-09-10"
- resolutionSource: "U.S. Census Bureau American Community Survey 1-Year Estimates Detailed Table B28005"
- resolutionSourceUrl: "https://data.census.gov/table/ACSDT1Y2025.B28005?q=B28005"
- resolutionRule: "Resolve to 100 * B28005_017E / B28005_014E for geography United States in the first public 2025 ACS 1-Year Estimates Detailed Table B28005 print, rounded to one decimal percentage point. Use the original Census first-posted estimate and ignore later revisions or corrections unless Census replaces the first public file before the public release completes."

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

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
{"slug":"broadband-subscription-65-plus-2025","country":"US","type":"data","title":"ACS 65+ Broadband Subscription Share, 2025","question":"U.S. Census Bureau American Community Survey 2025 ACS 1-Year Estimates Detailed Table B28005, population 65 years and over in households with a computer and a broadband Internet subscription divided by total population 65 years and over in households, first print, percent.","unit":"percent","pointEstimate":86.0,"ciLow":83.6,"ciHigh":88.4,"confidence":0.8,"resolutionDate":"2026-09-10","resolutionSource":"U.S. Census Bureau American Community Survey 1-Year Estimates Detailed Table B28005","resolutionSourceUrl":"https://data.census.gov/table/ACSDT1Y2025.B28005?q=B28005","resolutionRule":"Resolve to 100 * B28005_017E / B28005_014E for geography United States in the first public 2025 ACS 1-Year Estimates Detailed Table B28005 print, rounded to one decimal percentage point. Use the original Census first-posted estimate and ignore later revisions or corrections unless Census replaces the first public file before the public release completes.","dataPointId":"census.acs.broadband_subscription_65_plus.share.2025.first_print","historicalContext":[{"label":"2021 ACS 1-year U.S. B28005 65+ broadband share","value":79.4},{"label":"2022 ACS 1-year U.S. B28005 65+ broadband share","value":81.6},{"label":"2023 ACS 1-year U.S. B28005 65+ broadband share","value":83.5},{"label":"2024 ACS 1-year U.S. B28005 65+ broadband share","value":84.8},{"label":"2024 ACS all-household broadband subscription share","value":91.0},{"label":"2024 ACS 65+ no-computer share","value":8.7}],"drivers":["Aging-cohort replacement raises 65+ internet adoption","Broadband definition includes cellular data, satellite, fixed wireless, and other non-dial-up service","Adoption gains should slow as the remaining offline 65+ population is more selected","Affordable Connectivity Program expiration creates affordability drag for low-income older households","ACS first-print sampling and weighting noise can move this national age subgroup around one percentage point"],"sourceContext":["https://data.census.gov/table/ACSDT1Y2025.B28005?q=B28005","https://api.census.gov/data/2024/acs/acs1/groups/B28005.html","https://data.census.gov/table/ACSDT1Y2024.B28005?g=010XX00US&q=B28005","https://data.census.gov/table/ACSDT1Y2023.B28005?g=010XX00US&q=B28005","https://data.census.gov/table/ACSDT1Y2022.B28005?g=010XX00US&q=B28005","https://data.census.gov/table/ACSDT1Y2021.B28005?g=010XX00US&q=B28005","https://www.census.gov/programs-surveys/acs/news/data-releases/2024/release-schedule.html","https://www.census.gov/data/what-is-data-census-gov/upcoming-releases.html"],"runAt":"2026-07-21T02:29:30Z","reasoning":[{"kind":"heading","text":"Forecast for 2025 ACS 65+ Broadband Subscription Share"},{"kind":"text","text":"Framing and exact resolver: the target is Census ACS Detailed Table B28005, universe population in households, United States, 2025 ACS 1-year first print. The numerator is B28005_017E, 65 years and over, has a computer, with a broadband Internet subscription; the denominator is B28005_014E, total 65 years and over. The resolution source URL is the exact data.census.gov table page for ACSDT1Y2025.B28005."},{"kind":"tool","tool":"official.lookup","call":"Inspect Census API variable metadata for 2024 ACS 1-year B28005","result":"Fetched variable definitions: B28005 has 78 variables; B28005_014E is total 65 years and over; B28005_017E is 65 years and over with a computer and a broadband Internet subscription; B28005_001E is the total table population count."},{"kind":"tool","tool":"official.lookup","call":"Inspect published Thesis record derived from Census data.census.gov 2021 and 2022 ACS 1-year B28005 United States rows","result":"Fetched 2021 ACS 1-year United States B28005 counts: 65 years and over total 55,086,561 and 65+ with broadband subscription 43,757,048, computed share 79.4 percent. Fetched 2022 ACS 1-year counts: 65 years and over total 56,337,585 and 65+ with broadband subscription 45,989,221, computed share 81.6 percent."},{"kind":"tool","tool":"official.lookup","call":"Inspect published Thesis record derived from Census data.census.gov 2023 and 2024 ACS 1-year B28005 United States rows","result":"Fetched 2023 ACS 1-year United States B28005 counts: 65 years and over total 57,740,580 and 65+ with broadband subscription 48,245,700, computed share 83.5 percent. Fetched 2024 ACS 1-year counts: 65 years and over total 59,125,675 and 65+ with broadband subscription 50,144,228, computed share 84.8 percent."},{"kind":"tool","tool":"official.lookup","call":"Inspect Census ACS computer-and-internet use official results summarized in the published Thesis record","result":"Fetched latest ACS summary measures for the United States: households with a computer 95.5 percent; households with a broadband Internet subscription 91.0 percent; population 65+ with no computer in household 8.7 percent."},{"kind":"tool","tool":"official.lookup","call":"Inspect Census ACS release schedule and data.census.gov upcoming releases pages","result":"Fetched 2024 ACS release schedule showing the 2024 ACS 1-year Data Release on September 11, 2025 with Detailed Tables and Summary File for geographies of 65,000+ population. Fetched data.census.gov upcoming releases page last revised July 20, 2026 showing 9/10/2026 and 9/24/2026 September entries, but the 9/10/2026 listed item is August 2026 Current Population Survey Basic Monthly rather than ACS; this is a ledger-date discrepancy, so I keep the target's 2026-09-10 date while flagging that I did not find an official 2025 ACS 1-year schedule page verifying ACS on that date."},{"kind":"text","text":"Base rate/reference class: the best reference class is the same U.S. ACS 1-year B28005 age-65-plus series, which rose from 79.4 percent in 2021 to 84.8 percent in 2024. The 2024 all-household broadband measure at 91.0 percent is an upper-adoption context, while the 8.7 percent 65+ no-computer measure constrains how fast the B28005 broadband share can close the remaining gap."},{"kind":"text","text":"Level, momentum, one-off, and mechanism: level starts from the 2024 same-series first-print value of 84.8 percent. Momentum is positive because each entering 65-year-old cohort is more connected than the oldest cohorts leaving the population, and the broadband category includes cellular data plans. One-off BEAD deployment effects are limited by timing because many funded projects will not materially change 2025 ACS collection-year subscriptions. ACP expiration before 2025 adds affordability drag for some low-income older households."},{"kind":"math","text":"Prior/update/interval: persistence prior is the latest same-series 2024 U.S. ACS 1-year B28005 share of 84.8 percent. Historical sample is the same-series annual changes 2021-2022: 81.6 - 79.4 = +2.2, 2022-2023: 83.5 - 81.6 = +1.9, and 2023-2024: 84.8 - 83.5 = +1.3 percentage points, giving sigma = sqrt((2.2^2 + 1.9^2 + 1.3^2) / 3) = 1.8 percentage points. Mechanism update adds +1.4 points for cohort replacement and continued mobile/fixed-wireless subscription diffusion, minus 0.2 for affordability drag and saturation, yielding point 86.0. The 80% half-width is about 1.28*sigma = 1.28*1.8 = 2.3, rounded to 2.4 for first-print sampling and table-noise risk, so bounds are 86.0 - 2.4 = 83.6 and 86.0 + 2.4 = 88.4."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger-than-expected jump in cellular-data-plan reporting or older-adult smartphone adoption, which would land above the interval if the 2025 share exceeds 88.4 percent. Downside risk is affordability churn after subsidy expiration, survey-composition noise, or a stall among the oldest and lowest-income households, which would land below the interval if the first print is under 83.6 percent. An outside the interval result would most likely reflect either a definitional/table change or a large one-year ACS sampling/weighting move rather than ordinary trend continuation."},{"kind":"text","text":"Prior run update: I inspected an existing published Thesis run for the same target only for official-source-derived history and target identity, not as ground truth. Its point and interval were already consistent with the same-series 2021-2024 history, so the update from that run is no change to the central forecast and only an explicit note that the 2026-09-10 ledger date was not independently confirmed as an ACS release date on the current Census upcoming-releases page."},{"kind":"forecast","point":86.0,"ciLow":83.6,"ciHigh":88.4}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready, with one warning about avoiding circular reliance on a prior Thesis forecast for the same target.","requiredFixes":[{"rubricItem":"leakage","severity":"warning","summary":"The reasoning says an existing published Thesis run for the same target was inspected and that its point and interval were consistent, which risks catalog/prior-forecast circularity even if the official-source history was the intended use.","actionRequested":"Remove the comparison to the prior run's point and interval, or restate that only official Census-derived historical values and target metadata were used and that no prior forecast estimate influenced the point or interval."}],"optionalSuggestions":["Keep the note that the 2026-09-10 ACS release date was not independently confirmed, since the ledger contract still controls resolution.","Consider saying the interval uses annual-change RMS as an uncertainty proxy rather than pure residual volatility."]}

Emit the final JSON object only.
