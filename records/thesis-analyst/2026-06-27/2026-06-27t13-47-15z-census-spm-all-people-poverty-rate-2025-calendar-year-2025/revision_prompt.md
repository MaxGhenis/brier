# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.spm.all_people_poverty_rate.2025
- period: calendar year 2025
- conditional_on: null

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
{"slug":"us-census-spm-all-people-poverty-rate-2025","country":"US","type":"data","title":"US SPM poverty rate, 2025","question":"What will the U.S. Census Bureau first report as the all-people Supplemental Poverty Measure poverty rate for calendar year 2025 in Poverty in the United States: 2025, Table B-2?","unit":"percent","pointEstimate":12.6,"ciLow":11.6,"ciHigh":13.8,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"U.S. Census Bureau Poverty in the United States: 2025 first-release tables","resolutionSourceUrl":"https://www.census.gov/topics/income-poverty/supplemental-poverty-measure/data/tables.html","resolutionRule":"Resolve to the first Census Bureau published percentage for all people using the Supplemental Poverty Measure for calendar year 2025, normally Table B-2 in Poverty in the United States: 2025. Use the initially released value rounded to one decimal percentage point; ignore later errata, benchmark updates, or revised tables unless Census labels the original first print as withdrawn before public release.","dataPointId":"census.p60.spm.all_people_poverty_rate.2025.first_print","historicalContext":[{"label":"2024 first print","value":12.9},{"label":"2023 first print","value":12.9},{"label":"2022 first print","value":12.4},{"label":"2021 first print","value":7.8}],"drivers":["Recent SPM rate was flat at 12.9 percent in 2023 and 2024","No large 2025 federal child-tax-credit expansion comparable to 2021","Labor market stayed broadly expansionary but cooler than 2024","Inflation and housing costs still pressure SPM thresholds and necessary expenses","Benefit and tax-transfer mechanics likely keep the rate near the post-pandemic plateau"],"sourceContext":["https://www.census.gov/about/event-calendar.html","https://www.census.gov/topics/income-poverty/supplemental-poverty-measure/data/tables.html","https://www.census.gov/data/tables/2025/demo/income-poverty/p60-287.html","https://www2.census.gov/programs-surveys/demo/tables/p60/287/tableB-2.xlsx"],"runAt":"2026-06-27T13:47:40Z","reasoning":[{"kind":"heading","text":"Forecast for 2025 all-people SPM poverty rate"},{"kind":"text","text":"The target is the Census Bureau first print for calendar-year 2025 all people under the Supplemental Poverty Measure, not a later revised table and not the official poverty measure."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census Bureau Event Calendar for the Income, Poverty, and Health Insurance release covering calendar-year 2025.","result":"Official Census event-calendar lookup identified the 2025 income, poverty, and health-insurance release date as 2026-09-08; the calendar page revision observed was 2026-01-29."},{"kind":"tool","tool":"official.lookup","call":"Opened the Census Bureau Supplemental Poverty Measure Data Tables page and latest Poverty in the United States table listing.","result":"Census listed Poverty in the United States: 2024 with release date 2025-09-09 and report number P60-287; the page linked Table B-2 for 2009 to 2024."},{"kind":"tool","tool":"official.lookup","call":"Used Census Table B-2 for the all-people SPM reference class.","result":"Fetched recent all-people SPM rates: 2024=12.9 percent, 2023=12.9 percent, 2022=12.4 percent, 2021=7.8 percent."},{"kind":"text","text":"Base-rate/reference-class anchor: the post-expiration transfer regime since 2022 has averaged about 12.7 percent across 2022, 2023, and 2024, making the latest plateau a better prior than the unusually low 2020 and 2021 pandemic-transfer years."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Table B-series context around official and supplemental poverty tables for the latest release.","result":"The latest Census table page showed 2024 official poverty table A-1 and SPM tables B-2 through B-7; latest official poverty context was 2024=10.6 percent while SPM all-people was 2024=12.9 percent."},{"kind":"text","text":"Level and momentum: 2025 did not have a large new anti-poverty transfer shock, but real wage and employment conditions were not recessionary, so I expect only modest movement down from 12.9 rather than a return toward 2021's 7.8."},{"kind":"text","text":"Counter-consideration: if 2025 shelter and medical out-of-pocket adjustments run hotter than cash-income gains, or if survey income measurement weakens, the rate could stay near 13.5 or above despite continued employment growth."},{"kind":"math","text":"Point estimate: start from the 2022-2024 average (12.4+12.9+12.9)/3=12.73, subtract 0.1 for mild real-income gains and 0.0 to 0.1 for cooler-but-positive employment, rounded to 12.6. The 80% interval uses roughly +/-1.1 to +1.2 points around the point, widened on the upside for threshold and expense risk, giving 11.6 to 13.8."},{"kind":"text","text":"Upside scenario: a weaker 2025 CPS ASEC income print, higher necessary expenses, or reduced effective transfers puts the first print around 13.8 to 14.3. Downside scenario: stronger lower-wage real earnings and stable transfer receipt bring it near 11.5. Outside-the-interval downside would require a broader income surprise or policy effect not evident from the baseline."},{"kind":"forecast","point":12.6,"ciLow":11.6,"ciHigh":13.8}]}

# Reviewer critique
{"summary":"Draft is broadly publishable but needs clearer cited support for the 2025 inside-view update, an explicit model-prior statement, and a defensible interval basis.","requiredFixes":[{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses a 2022-2024 average as a persistence prior but does not explicitly state whether a time-series/model prior was used or ruled out.","actionRequested":"Add one sentence naming the model prior, e.g. a persistence/three-year post-pandemic-regime mean, or explicitly state why no formal time-series model is used."},{"rubricItem":"update","severity":"warning","summary":"The movement from the 12.7 prior to 12.6 relies on claims about 2025 labor market, inflation, housing costs, transfers, and real income, but the cited public evidence is almost entirely Census release/table material rather than evidence for those 2025 conditions.","actionRequested":"Either cite public evidence for the 2025 labor/inflation/housing/transfer assumptions or reduce the inside-view adjustment and describe it as mostly persistence."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is asserted as roughly -1.0/+1.2 points but is not tied to realized volatility, backtest error, survey error, or a stated subjective uncertainty calculation.","actionRequested":"State the empirical or subjective basis for the interval width, such as recent SPM year-to-year volatility excluding pandemic-transfer outliers plus added policy/measurement uncertainty."},{"rubricItem":"resolver","severity":"warning","summary":"The resolver is mostly clear, but the resolution date evidence is described in reasoning while the resolutionSourceUrl points only to the generic SPM tables page.","actionRequested":"Add the Census event-calendar URL or exact cited release-calendar evidence to the resolver/source context so the 2026-09-08 resolution date is auditable."}],"optionalSuggestions":["Clarify that the interval is an 80% interval to match confidence=0.8.","Make the upside and downside tail scenarios mention concrete approximate values outside the central interval."]}

Emit the final JSON object only.
