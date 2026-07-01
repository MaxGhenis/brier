# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statjp.household_spending.real_yoy.two_or_more_person_households.may_2026.first_print
- period: May 2026
- conditional_on: null

# Source hints
- Use the official agency data page and release calendar.
- FRED or sanctioned mirrors may be used only for history, not final resolution.
- Match the agency's published rounding precision.

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
{"slug":"statjp-household-spending-real-yoy-two-or-more-person-households-may-2026-first-print","country":"JP","type":"data","title":"Japan household spending real YoY, May 2026","question":"Statistics Bureau of Japan Family Income and Expenditure Survey, consumption expenditures for two-or-more-person households, real year-over-year percent change, May 2026, first preliminary print","unit":"percent_growth","pointEstimate":-1.1,"ciLow":-4,"ciHigh":2.2,"confidence":0.8,"resolutionDate":"2026-07-07","resolutionSource":"Statistics Bureau of Japan Family Income and Expenditure Survey monthly preliminary report","resolutionSourceUrl":"https://www.stat.go.jp/data/kakei/sokuhou/tsuki/pdf/fies_mr.pdf","resolutionRule":"Resolve to the first preliminary Statistics Bureau of Japan Family Income and Expenditure Survey monthly report value for real consumption expenditures, two-or-more-person households, May 2026, year-over-year percent change. Use the agency-published one-decimal-percent figure from the first print released on 2026-07-07; ignore later revisions or annual recalculations.","dataPointId":"statjp.fies.consumption_expenditures.real_yoy.two_or_more_person_households.2026-05.first_print","historicalContext":[{"label":"2026-Apr first print","value":-0.5},{"label":"2026-Mar first print","value":-2.9},{"label":"2026-Feb first print","value":-1.8},{"label":"2026-Jan first print","value":-1},{"label":"2025-May first print","value":4.7}],"drivers":["Recent official real spending prints were negative through April 2026","May 2025 comparison base was high at plus 4.7 percent","April 2026 showed less weakness than March but not a clear positive run rate","Real purchasing-power pressure still limits volume growth","One-off calendar and bonus-timing effects can move the monthly household survey materially"],"sourceContext":["https://www.stat.go.jp/data/kakei/sokuhou/tsuki/pdf/fies_mr.pdf","https://www.stat.go.jp/data/kakei/index.html","https://www.stat.go.jp/data/kouhyou/index.html"],"runAt":"2026-06-27T13:17:51Z","reasoning":[{"kind":"heading","text":"Forecast for Japan May 2026 real household spending YoY first print"},{"kind":"text","text":"The resolver is the Statistics Bureau of Japan first preliminary monthly Family Income and Expenditure Survey print for consumption expenditures of two-or-more-person households, real year-over-year change, May 2026. The agency reports this series to one decimal percent, so the forecast is also stated to one decimal percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the Statistics Bureau of Japan household spending data page and current monthly preliminary report for the target series and recent official prints.","result":"The April 2026 preliminary report shows real consumption expenditures for two-or-more-person households at -0.5 percent year over year in 2026-Apr, after -2.9 percent in 2026-Mar, -1.8 percent in 2026-Feb, and -1.0 percent in 2026-Jan."},{"kind":"tool","tool":"official.lookup","call":"Read the same official monthly report table for the recent reference class of first-print real year-over-year values.","result":"The 12-month sequence from 2025-May through 2026-Apr is 4.7, 1.3, 1.4, 2.3, 1.8, -3.0, -2.3, -2.7, -1.0, -1.8, -2.9, -0.5 percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the official Statistics Bureau publication schedule page for the May 2026 household spending release date.","result":"The official schedule places the May 2026 household spending first-print release on 2026-07-07; the current report page identifies the monthly preliminary report as the release vehicle and reports April 2026 at -0.5 percent."},{"kind":"text","text":"Base-rate/reference-class anchor: the latest 12 official monthly first prints average about -0.2 percent, while the latest four average about -1.6 percent. I put more weight on the recent negative run because inflation-adjusted household spending has remained weak into 2026, but I do not extrapolate the March trough mechanically because April rebounded to -0.5 percent."},{"kind":"text","text":"Level and momentum effects point slightly negative: the January-April 2026 run is below zero, and May must compare against May 2025's high 4.7 percent print. That high base makes a positive May 2026 year-over-year result harder even if the month-to-month level is stable."},{"kind":"text","text":"Policy and one-off mechanisms are mixed. Wage gains and fiscal support can lift nominal outlays, but the target is real spending, so price levels subtract from the volume measure. Calendar, weather, and sample-composition noise can still produce a large positive or negative one-month print."},{"kind":"text","text":"Counter-consideration: April's improvement from -2.9 percent to -0.5 percent could mark a real turning point if wage settlements or durable-goods purchases pulled May up. Conversely, if the high May 2025 base and food-price pressure dominate, the print could fall below -4.0 percent."},{"kind":"math","text":"I anchor at the 12-month mean near -0.2 percent, blend toward the latest-four-month mean near -1.6 percent, then subtract a small high-base adjustment from May 2025's +4.7 percent comparison, yielding about -1.1 percent. The realized monthly dispersion in the 12 official prints supports an 80 percent interval roughly 3 percentage points wide on each side; I use -4.0 to 2.2 percent, slightly skewed downside because the base effect is adverse."},{"kind":"text","text":"Upside outside-the-interval scenario: real wage gains and delayed services or durable-goods spending lift the first print above 2.2 percent. Downside outside-the-interval scenario: food and utility inflation plus the high May 2025 base push real spending below -4.0 percent. Central scenario: still-negative but less severe real spending, close to April's weakness."},{"kind":"forecast","point":-1.1,"ciLow":-4,"ciHigh":2.2}]}

# Reviewer critique
{
  "summary": "Draft is mostly publication-ready, with one blocking issue around source specificity and several warnings where the evidence and uncertainty math should be made more explicit.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The resolver names the Statistics Bureau monthly preliminary report, but the URL is a rolling PDF and the draft does not specify the exact table/line/field to read within the report.",
      "actionRequested": "Add the exact table or field label for the May 2026 first preliminary value, e.g. the consumption expenditures, two-or-more-person households, real year-over-year percent-change line, and note that the rolling PDF must be archived or captured at first print."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a simple 12-month and latest-four-month average, but does not clearly state whether a time-series model was used or intentionally ruled out.",
      "actionRequested": "Add one sentence explicitly saying no formal ARIMA/ETS/regression model was used, and that the prior is a transparent persistence/reference-class blend."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The movement from the 12-month mean near -0.2 to the final -1.1 is plausible, but the high-base adjustment is described only qualitatively.",
      "actionRequested": "State the approximate weight or arithmetic used in the blend and the size of the high-base adjustment."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The interval is said to come from realized monthly dispersion, but the draft does not report the realized volatility or quantile calculation.",
      "actionRequested": "Add the standard deviation, mean absolute error, or empirical 80% range from the cited 12-print reference class that supports the -4.0 to 2.2 interval."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether confidence 0.8 means an 80% central interval.",
    "Use one-decimal formatting consistently for ciLow and ciHigh, e.g. -4.0 and 2.2.",
    "Make the downside tail distinguish outside-interval from interval-edge movement, since below -4.0 is also the lower bound."
  ]
}

Emit the final JSON object only.
