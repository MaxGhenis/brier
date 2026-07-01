# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.labour.unemployment_rate.july_to_september_2026.first_print
- period: Jul-Sep 2026
- conditional_on: null

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.1.0, prompt 9435029c5fb9, tools e15bf40583f8, promptMode fast)


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
{"slug":"uk-unemployment-rate-jul-sep-2026","country":"UK","type":"data","title":"UK unemployment rate, Jul-Sep 2026","question":"Office for National Statistics Labour Force Survey unemployment rate for people aged 16 and over, seasonally adjusted, July to September 2026 rolling three-month period, first print","unit":"percent","pointEstimate":5.1,"ciLow":4.5,"ciHigh":5.8,"confidence":0.8,"resolutionDate":"2026-11-17","resolutionSource":"Office for National Statistics, UK Labour Market: November 2026","resolutionSourceUrl":"https://www.ons.gov.uk/releases/uklabourmarketnovember2026","resolutionRule":"Resolve to the first published one-decimal seasonally adjusted ONS Labour Force Survey unemployment rate for people aged 16 and over, series MGSX, for the July to September 2026 rolling three-month period in the UK Labour Market or Employment in the UK November 2026 release. Use the initial 17 November 2026 print and ignore later revisions, seasonal-adjustment updates, or dataset back revisions unless ONS corrects the same first release on release day.","dataPointId":"ons.labour.unemployment_rate.july_to_september_2026.first_print","historicalContext":[{"label":"Feb-Apr 2026 unemployment rate","value":4.9},{"label":"Nov 2025-Jan 2026 unemployment rate implied by quarter change","value":5.2},{"label":"2026 Q1 MGSX unemployment rate","value":5.0},{"label":"2025 Q4 MGSX unemployment rate","value":5.2},{"label":"2025 Q3 MGSX unemployment rate","value":5.0},{"label":"2025 annual MGSX unemployment rate","value":4.8}],"drivers":["latest LFS unemployment rate is 4.9 percent after a quarterly fall","unemployment remains up 0.3 percentage points on the year","PAYE payroll employees are falling year over year and vacancies are at their lowest since early 2021","LFS quality and seasonal-adjustment volatility argue for a wide 80 percent interval","short-run momentum is mixed, with unemployment down on the quarter but broader labour demand soft"],"sourceContext":["https://www.ons.gov.uk/releases/uklabourmarketnovember2026","https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/june2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/employmentintheuk/june2026"],"runAt":"2026-06-27T23:33:54Z","reasoning":[{"kind":"heading","text":"Forecast UK Jul-Sep 2026 first-print unemployment rate"},{"kind":"text","text":"The resolver is the ONS Labour Force Survey unemployment rate for people aged 16 and over, seasonally adjusted, for the July to September 2026 rolling three-month period. The target is the first one-decimal print in the November 2026 UK Labour Market or Employment in the UK release."},{"kind":"tool","tool":"command.date","call":"date -u +%Y-%m-%dT%H:%M:%SZ","result":"Fetched run timestamp 2026-06-27T23:33:54Z."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS release page for UK Labour Market: November 2026.","result":"Fetched official release date 2026-11-17 at 7:00am for UK Labour Market: November 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS time-series page MGSX for the unemployment rate aged 16 and over, seasonally adjusted.","result":"Fetched Series ID MGSX, units %, release date 2026-06-18, next release 2026-07-21, annual 2025 value 4.8%, quarterly values 2025 Q3 5.0%, 2025 Q4 5.2%, 2026 Q1 5.0%, and monthly rolling-period values 2025 OCT 5.1%, 2025 NOV 5.2%, 2025 DEC 5.2%, 2026 JAN 4.9%, 2026 FEB 5.0%, 2026 MAR 4.9%."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS Labour market overview, UK: June 2026 bulletin for current-release context.","result":"Fetched latest LFS unemployment rate for February to April 2026 = 4.9%, up 0.3 percentage points on the year and down 0.3 percentage points on the latest quarter; PAYE employees fell 103,000 over the year and 31,000 on the quarter for February to April 2026; March to May 2026 vacancies fell 19,000 to 707,000."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS Employment in the UK: June 2026 bulletin for level, uncertainty, and sampling context.","result":"Fetched February to April 2026 unemployment level 1.764 million, unemployment-rate sampling variability ±0.3 percentage points, quarterly change -0.3 percentage points, annual change +0.3 percentage points, and achieved LFS sample 80,078 individuals in January to March 2026."},{"kind":"text","text":"Base-rate/reference-class anchor: before inside-view adjustments, recent official MGSX history puts the rate around 5 percent. The last three quarterly values were 5.0, 5.2, and 5.0 percent, while recent monthly rolling-period prints were mostly 4.9 to 5.2 percent. That anchors the prior near 5.0 percent rather than below the 2024 average."},{"kind":"text","text":"Level, momentum, and one-off effects: the latest February to April print is lower than the prior quarter, but it is still up on the year. Payroll employment and vacancies point to weaker labour demand, while the LFS bulletin explicitly warns that short-term movements remain volatile and should be judged with other indicators."},{"kind":"text","text":"Policy and measurement mechanism: the target is a household-survey unemployment rate, not a claimant-count or payroll series. Soft PAYE and vacancies tend to lift unemployment with a lag, but seasonal-adjustment review and LFS sampling variability can move the first print by several tenths without a true labour-market break."},{"kind":"text","text":"Counter-consideration: the print could come below 4.5 if the February-April quarterly fall marks a genuine re-tightening in labour demand or if inactivity absorbs job losses. It could exceed 5.8 if payroll weakness broadens into layoffs, vacancies keep falling, and LFS volatility prints another sharp unemployment increase."},{"kind":"math","text":"Point calculation: start with a 5.0 percent outside-view anchor from recent quarterly MGSX values, blend in the latest 4.9 percent February-April level, then add about 0.15 percentage points for weak PAYE employment and vacancies over the five-month release horizon: 0.45*5.0 + 0.35*4.9 + 0.20*5.3 = 5.025, rounded and judgmentally tilted to 5.1 because labour-demand indicators are soft. For the 80% interval, begin with roughly ±0.5 percentage points around 5.1 from recent LFS movement and sampling variability, then widen the upper side for lagged unemployment risk, giving 4.5 to 5.8."},{"kind":"forecast","point":5.1,"ciLow":4.5,"ciHigh":5.8}]}

# Reviewer critique
{"summary":"The draft is publishable with only minor tightening around the interval calibration.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is directionally justified by LFS sampling variability and recent volatility, but the realized-volatility basis is only described qualitatively.","actionRequested":"Add one sentence or calculation tying the 4.5 to 5.8 interval to recent MGSX rolling-period or quarterly absolute changes, or explicitly state that the interval is a judgmental widening from the ONS ±0.3 percentage-point sampling variability."}],"optionalSuggestions":["Clarify whether the prior is an outside-view persistence prior or a simple time-series blend, since both are effectively being used.","Check the historical-context label for Nov 2025-Jan 2026 against the cited MGSX rolling-period values so it does not appear inconsistent with the fetched 2026 JAN value."]}

Emit the final JSON object only.
