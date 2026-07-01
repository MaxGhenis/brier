# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statjp.lfs.unemployment_rate
- period: 2026-05
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
{"slug":"jp-lfs-unemployment-rate-2026-05","country":"JP","type":"data","title":"Japan May 2026 unemployment rate","question":"Japan Statistics Bureau Labour Force Survey Basic Tabulation, May 2026 seasonally adjusted unemployment rate, first print","unit":"percent","pointEstimate":2.5,"ciLow":2.3,"ciHigh":2.8,"confidence":0.8,"resolutionDate":"2026-06-30","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.stat.go.jp/data/roudou/sokuhou/tsuki/index.html","resolutionRule":"Resolve to the first-print seasonally adjusted complete unemployment rate for May 2026 in the Statistics Bureau of Japan Labour Force Survey Basic Tabulation, published at the agency's stated precision of one decimal percentage point. Use the initial June 30, 2026 print and ignore later revisions or seasonal-adjustment updates.","dataPointId":"statjp.lfs.unemployment_rate.2026-05.first_print","historicalContext":[{"label":"2026-04 seasonally adjusted unemployment rate","value":2.5},{"label":"2026-03 seasonally adjusted unemployment rate","value":2.7},{"label":"2026-02 seasonally adjusted unemployment rate","value":2.6},{"label":"2026-01 seasonally adjusted unemployment rate","value":2.7},{"label":"2025 annual unemployment rate","value":2.5},{"label":"2024 annual unemployment rate","value":2.5},{"label":"2023 annual unemployment rate","value":2.6}],"drivers":["latest unemployment rate fell to 2.5 percent","recent 2026 monthly range is narrow at 2.5 to 2.7 percent","employment up year over year but unemployed persons also up year over year","Japan labor market level remains near the 2024-2025 average","one-month rounded moves are usually small but 0.2 point reversals are possible"],"sourceContext":["https://www.stat.go.jp/data/roudou/sokuhou/tsuki/index.html","https://www.stat.go.jp/data/roudou/pdf/kohyo26.pdf","https://www.stat.go.jp/data/roudou/sokuhou/tsuki/pdf/gaiyou.pdf","https://www.e-stat.go.jp/stat-search/files?cycle=0&tclass=000001226526"],"runAt":"2026-06-27T12:57:12Z","reasoning":[{"kind":"heading","text":"Forecast Japan May 2026 first-print unemployment rate"},{"kind":"text","text":"The resolver is the Statistics Bureau of Japan Labour Force Survey Basic Tabulation complete unemployment rate, seasonally adjusted, for May 2026, taken from the first official monthly release and rounded as the agency publishes it to one decimal percentage point."},{"kind":"tool","tool":"official.lookup","call":"Opened the Statistics Bureau monthly Labour Force Survey results page for the latest official release.","result":"Latest official page is the 2026 April release, published 2026-05-29, with seasonally adjusted complete unemployment rate 2.5%, down 0.2 percentage point from the prior month."},{"kind":"tool","tool":"official.lookup","call":"Opened the official 2026 Labour Force Survey release schedule PDF.","result":"The schedule lists the 2026年5月分 Basic Tabulation release date as 2026-06-30 and notes Basic Tabulation releases at 8:30."},{"kind":"tool","tool":"official.lookup","call":"Read the latest official monthly summary table for recent values and annual context.","result":"The page reports 2023 annual 2.6%, 2024 annual 2.5%, 2025 annual 2.5%, and 2026 monthly values of Jan 2.7%, Feb 2.6%, Mar 2.7%, Apr 2.5%."},{"kind":"tool","tool":"official.lookup","call":"Read the latest official PDF summary for labor-market level and momentum details.","result":"The April 2026 PDF reports employed persons 68.60 million, up 0.64 million year over year; unemployed persons 1.93 million, up 0.05 million year over year; labor force 70.53 million, up 0.69 million year over year; seasonally adjusted unemployment rate 2.5%."},{"kind":"text","text":"Base-rate/reference-class anchor: the recent official-source reference class is a low-volatility range around 2.5 to 2.7 percent. The 2024 and 2025 annual rates were both 2.5 percent, so the outside-view anchor is 2.5 percent rather than a trend extrapolation away from the recent mean."},{"kind":"text","text":"Level, momentum, and one-off effects: the latest 2.5 percent level is already at the two-year annual average. The month-to-month momentum is downward from March to April, but the year-over-year unemployed count is still positive, which argues against a confident break below 2.5 percent. No policy-mechanism or calendar event points to a large May discontinuity."},{"kind":"text","text":"Counter-consideration: April's 0.2 point drop could partially reverse if labor-force participation rose or if the unemployed count continued its year-over-year increase; an upside print of 2.7 to 2.8 percent is plausible. The downside scenario is continued strong employment absorption pushing the rounded rate to 2.3 or 2.4 percent. Outside the interval would likely require an unusually sharp one-month labor-force or employment shock."},{"kind":"math","text":"Point calculation: start from the official April level 2.5, blend with the 2026 Jan-Apr average (2.7+2.6+2.7+2.5)/4 = 2.625 and the 2024-2025 annual anchor 2.5, then give most weight to the latest level because the target is one month ahead and rounded to 0.1; resulting latent forecast is about 2.55, rounded forecast 2.5. The 80% interval uses recent rounded monthly dispersion of about 0.1-0.2 point, widened for release noise to 2.3-2.8."},{"kind":"forecast","point":2.5,"ciLow":2.3,"ciHigh":2.8}]}

# Reviewer critique
{
  "summary": "Draft is mostly publishable but needs fixes to prior ordering, model-prior treatment, interval grounding, and point-calculation coherence.",
  "requiredFixes": [
    {
      "rubricItem": "base_rate",
      "severity": "warning",
      "summary": "The base-rate/reference-class anchor is stated only after the current-release evidence and inside-view discussion.",
      "actionRequested": "Move the outside-view prior before current-evidence updates, explicitly naming the prior value or range before discussing April 2026 movement."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "A simple blend of latest value, 2026 average, and annual anchor is used, but no time-series/model prior is clearly specified or explicitly ruled out.",
      "actionRequested": "State the model prior explicitly, such as persistence or short moving average, or say why no formal time-series model is used."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is justified by recent rounded dispersion of about 0.1-0.2 points, but the cited evidence only shows a very short Jan-Apr 2026 window and does not substantiate the 2.3-2.8 range.",
      "actionRequested": "Tie the interval to a stated volatility sample or explicitly label the extra width as judgmental uncertainty around rounded one-month moves."
    },
    {
      "rubricItem": "coherence",
      "severity": "blocking",
      "summary": "The math says the latent forecast is about 2.55 but then rounds it to 2.5, which is not coherent with ordinary one-decimal rounding.",
      "actionRequested": "Revise the final forecast step so the latent calculation and published point estimate agree, or explain that 2.5 is a judgmental point estimate rather than a mechanical rounding of 2.55."
    }
  ],
  "optionalSuggestions": [
    "Replace the generic resolutionSource label with the specific Statistics Bureau of Japan Labour Force Survey Basic Tabulation first monthly release.",
    "Clarify whether confidence means an 80% central interval."
  ]
}

Emit the final JSON object only.
