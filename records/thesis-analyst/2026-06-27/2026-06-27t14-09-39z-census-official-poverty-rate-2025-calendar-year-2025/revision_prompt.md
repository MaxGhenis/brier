# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.official_poverty_rate.2025
- period: calendar year 2025
- conditional_on: null

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Size the 80% interval from realized first-print dispersion, then widen or skew only for stated reasons.
- Name concrete upside, downside, and outside-the-interval scenarios.

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
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step, one math step, one counter-consideration, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.1.0, prompt 3a08d7c397df, tools e15bf40583f8, promptMode fast)


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
{"slug":"census-official-poverty-rate-2025","country":"US","type":"data","title":"US official poverty rate, 2025","question":"U.S. Census Bureau official poverty measure, percentage of people in poverty in calendar year 2025, United States, first print in the Poverty in the United States: 2025 report/Table A-1 from the CPS ASEC; not the Supplemental Poverty Measure.","unit":"percent","pointEstimate":11.0,"ciLow":10.3,"ciHigh":11.8,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"U.S. Census Bureau Poverty in the United States: 2025 first-release report and Table A-1","resolutionSourceUrl":"https://www.census.gov/library/publications/2026/demo.html","resolutionRule":"Resolve to the first Census Bureau published official poverty measure rate for calendar year 2025, percentage of people in poverty, in the Poverty in the United States: 2025 report or its Table A-1. Use the value as published in percent to one decimal place. Do not use SPM, ACS poverty, later revised tables, FRED mirrors, news reports, or post-release corrections unless Census withdraws and replaces the first print on the same release day.","dataPointId":"census.cps_asec.official_poverty_rate.people.2025.first_print","historicalContext":[{"label":"2024 official poverty rate","value":10.6},{"label":"2023 official poverty rate","value":11.1},{"label":"2022 official poverty rate","value":11.5},{"label":"2024 people in poverty, millions","value":35.9},{"label":"2023 people in poverty, millions","value":36.8},{"label":"2022 people in poverty, millions","value":37.9}],"drivers":["Official measure uses pretax cash income, so SNAP, tax credits, noncash transfers, housing adjustments, medical expenses, and taxes are not counted in the resolver","2024 first print was low by recent standards at 10.6 percent after a 0.4 point decline from 2023","Weak 2025 payroll growth and a higher late-2025 unemployment rate raise risk of some reversal","Nominal wage growth above inflation limits the size of the poverty-rate increase","Threshold inflation mechanically raises the income cutoff but 2025 inflation was much lower than 2021-2022","Migration, family composition, and CPS ASEC sampling error can move the first print by several tenths"],"sourceContext":["https://www.census.gov/library/publications/2025/demo/p60-287.html","https://www.census.gov/library/publications/2024/demo/p60-283.html","https://www.census.gov/library/publications/2023/demo/p60-280.html","https://www.census.gov/newsroom/releases/calendar.html","https://www.bls.gov/news.release/archives/empsit_02112026.htm"],"runAt":"2026-06-27T14:09:56Z","reasoning":[{"kind":"heading","text":"Forecast for the 2025 U.S. official poverty rate first print"},{"kind":"text","text":"The resolver is the Census Bureau official poverty measure for calendar year 2025, reported as the percentage of people in poverty in the first Poverty in the United States: 2025 release/Table A-1 from CPS ASEC. This is not the SPM: taxes, refundable credits, SNAP, housing-cost adjustments, work expenses, medical expenses, and geographic threshold adjustments do not define this official-poverty target."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Poverty in the United States: 2024 report page and highlights.","result":"Fetched 2024 official poverty rate 10.6 percent, 35.9 million people in poverty, 0.4 percentage point decrease from 2023, SPM 12.9 percent, Social Security moved 28.7 million people out of SPM poverty, report date 2025-09-09."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Poverty in the United States: 2023 report page and highlights.","result":"Fetched 2023 official poverty rate 11.1 percent, 36.8 million people in poverty, 0.4 percentage point decrease from 2022, SPM 12.9 percent, child SPM 13.7 percent, report date 2024-09-10."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Poverty in the United States: 2022 report page and highlights.","result":"Fetched 2022 official poverty rate 11.5 percent, 37.9 million people in poverty, SPM 12.4 percent, child SPM 12.4 percent, report date 2023-09-12."},{"kind":"tool","tool":"official.lookup","call":"Checked Census release-calendar path and recent first-release dates for the same report series.","result":"Fetched recent same-series release dates 2023-09-12, 2024-09-10, and 2025-09-09; used the Census release calendar/schedule path for the 2026 first-release target date 2026-09-08."},{"kind":"tool","tool":"official.lookup","call":"Checked labor-market release context for 2025 from the February 2026 Employment Situation reporting cycle.","result":"Fetched January 2026 unemployment rate 4.3 percent, December 2025 unemployment rate 4.4 percent, January 2026 payroll gain 130000, and revised 2025 payroll gain 181000."},{"kind":"text","text":"Reference class/base rate: the last three first-print official poverty rates are 11.5, 11.1, and 10.6 percent. A simple recent average is 11.07 percent, while the latest level is 10.6 percent. The outside view therefore starts near 10.9 to 11.1, with year-to-year changes of -0.4 and -0.5 points in the last two releases but a low current level relative to much of the post-2000 history."},{"kind":"text","text":"Level and momentum: 2024 was already low, so further large declines are harder. The weak 2025 labor-market signal pushes up from 10.6, but not toward recessionary levels because unemployment around the low-to-mid 4s and continued wage growth are still consistent with only a moderate poverty increase."},{"kind":"text","text":"Policy mechanism: because the official measure is pretax cash income, many 2025 changes to taxes, credits, SNAP, medical costs, and housing costs matter less directly than they would for the SPM. Cash earnings, Social Security cash income, unemployment, and threshold inflation are the main channels for this resolver."},{"kind":"text","text":"Counter-consideration: a downside-to-poverty scenario is that wage gains among lower-paid workers and Social Security COLA income keep pretax cash income ahead of thresholds, leaving the rate near 10.5. An upside poverty scenario is that weak hiring, reduced hours, and CPS sampling produce a sharper reversal to 11.7 or more. Outside the interval would likely require either a surprisingly broad cash-income gain below the median or a much worse late-2025 labor shock than the annual averages imply."},{"kind":"math","text":"Base recent mean = (10.6 + 11.1 + 11.5) / 3 = 11.07. Latest-level anchor = 10.6. Apply +0.3 point for weaker 2025 labor market and threshold pressure, partly offset by still-positive nominal wage growth: 10.6 + 0.4 = 11.0 after rounding to one decimal. Size 80% interval at roughly +/-0.75 points from recent first-print dispersion and sampling/policy uncertainty, rounded to 10.3 to 11.8."},{"kind":"forecast","point":11.0,"ciLow":10.3,"ciHigh":11.8}]}

# Reviewer critique
{
  "summary": "The draft is close, but it needs tighter support for the model/interval/update logic and one arithmetic coherence fix before publication.",
  "requiredFixes": [
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft gives a recent average and persistence anchor, but does not use or explicitly rule out a time-series/model prior.",
      "actionRequested": "Add a sentence either specifying a simple model prior, such as persistence or recent mean with realized one-year changes, or explicitly state why a richer time-series model is not used."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The +0.4 point move from the 2024 level relies on weak labor market, wage, and inflation claims, but the cited evidence only clearly supports some labor-market context.",
      "actionRequested": "Tie the update more directly to cited public evidence, or weaken the update language if wage growth and inflation evidence are not cited in the draft."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval of 10.3 to 11.8 is described as based on recent dispersion and uncertainty, but the realized-volatility calculation is not shown.",
      "actionRequested": "Add the realized year-to-year volatility or a clear uncertainty decomposition explaining why roughly +/-0.75 points is appropriate for an 80% interval."
    },
    {
      "rubricItem": "coherence",
      "severity": "blocking",
      "summary": "The final math step says apply +0.3 points, then calculates 10.6 + 0.4 = 11.0.",
      "actionRequested": "Make the update size internally consistent, either +0.4 from 10.6 or a +0.3 update yielding 10.9 before any rounding adjustment."
    }
  ],
  "optionalSuggestions": [
    "Use a more exact Census release-calendar citation or placeholder page for the September 8, 2026 resolution date if available.",
    "Clarify whether the cited 2025 payroll gain is an annual average, annual total, or revision figure."
  ]
}

Emit the final JSON object only.
