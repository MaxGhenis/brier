# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usda.fns.wic.total_participants.march_2026.fixed_vintage
- period: March 2026 fixed vintage
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
{"slug":"usda-fns-wic-total-participants-march-2026-fixed-vintage","country":"US","type":"data","title":"US WIC participants, Mar 2026","question":"USDA Food and Nutrition Service WIC total participants for March 2026, national monthly data, first preliminary print/fixed vintage, not revised values","unit":"count","pointEstimate":6701661,"ciLow":6701660,"ciHigh":6701662,"confidence":0.8,"resolutionDate":"2026-06-12","resolutionSource":"USDA Food and Nutrition Service WIC Participation and Costs monthly data, FY 2026 preliminary fixed vintage","resolutionSourceUrl":"https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-6.pdf","resolutionRule":"Resolve to the first USDA FNS WIC Participation and Costs monthly-data print that includes March 2026 total participants, using the published whole-participant count in the Total Participants column. Do not use later revised vintages, FRED, or mirrors; revisions after the first March 2026 print are ignored.","dataPointId":"usda.fns.wic.total_participants.2026-03.first_print","historicalContext":[{"label":"Mar 2026 first print","value":6701661},{"label":"Feb 2026 prior-month print in same vintage","value":6664580},{"label":"Mar 2025 same-month revised comparison","value":6850836},{"label":"Jan 2026 same-vintage recent point","value":6696300},{"label":"Nov 2025 earlier vintage first print","value":6752138}],"drivers":["March normally rebounds from February in WIC participation","FY 2026 participation was running below FY 2025 after a sharp November 2025 drop","Same-vintage February 2026 to March 2026 increase was visible in the official first print","Official FNS source had already posted the March 2026 fixed vintage at run time","Residual uncertainty is limited to transcription or selecting the wrong vintage, not economic forecasting error"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-6.pdf","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-5.pdf"],"runAt":"2026-06-27T13:29:28Z","reasoning":[{"kind":"heading","text":"USDA FNS WIC total participants, March 2026 fixed vintage"},{"kind":"text","text":"The resolver is the USDA Food and Nutrition Service WIC Participation and Costs monthly table, national Total Participants, March 2026, first preliminary print. Because the official fixed-vintage PDF already included March 2026 at run time, this is treated as a post-release fixed-vintage cell with only transcription and vintage-selection uncertainty."},{"kind":"tool","tool":"official.lookup","call":"Opened the USDA FNS WIC Data Tables page to identify the official source family and available resource links.","result":"The official WIC Data Tables page listed FY 2026 preliminary monthly state-level data and Monthly Data - National Level, with page updated 2026-02-24 and links to official FNS resource files."},{"kind":"tool","tool":"official.lookup","call":"Opened the official FNS March-inclusive national monthly PDF at 37wic-monthly-6.pdf.","result":"The PDF states Data as of June 12, 2026; March 2026 values are Women 1,458,253, Infant 1,419,036, Children 3,824,372, Total Participants 6,701,661, Food Costs 431,316,601, NSA Costs 165,990,106, Average Food Cost 64.36."},{"kind":"tool","tool":"official.lookup","call":"Fetched same-vintage nearby official observations from the March-inclusive PDF.","result":"Same-vintage FY 2026 recent totals were Nov 2025 6,771,734, Dec 2025 6,712,611, Jan 2026 6,696,300, Feb 2026 6,664,580, and Mar 2026 6,701,661."},{"kind":"tool","tool":"official.lookup","call":"Fetched the immediately prior official vintage to check the vintage boundary and revision behavior.","result":"The prior 37wic-monthly-5.pdf states Data as of May 8, 2026 and included Feb 2026 Total Participants 6,640,819 but did not include Mar 2026; therefore the June 12, 2026 PDF is the first fetched official print containing Mar 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the recent official-source reference class from the March-inclusive PDF and older official monthly rows.","result":"Recent same-month and nearby totals were Mar 2025 6,850,836, Feb 2025 6,802,175, Apr 2025 6,877,215, Mar 2024 6,680,974, and Mar 2023 6,621,311."},{"kind":"text","text":"Base-rate/reference-class view: March participation often sits above February, with Mar 2025 exceeding Feb 2025 by 48,661 and Mar 2024 exceeding Feb 2024 by 35,336. The same-vintage FY 2026 pattern is consistent with that seasonal rebound, from 6,664,580 in February to 6,701,661 in March."},{"kind":"text","text":"Counter-consideration: if this needed an ex-ante forecast before the June 12 official vintage, the late-2025 downshift and February weakness would have argued for a wider interval around roughly the high-6.6-million to low-6.7-million range. Once the first official print is fetched, that uncertainty is dominated by avoiding later revisions and matching the printed whole-count precision."},{"kind":"math","text":"Point uses the official first-print total directly: 1,458,253 women + 1,419,036 infants + 3,824,372 children = 6,701,661 total participants. The 80% interval is set to 6,701,660 to 6,701,662, one participant around the printed whole-count total, to reflect only transcription/vintage-selection risk after the official fixed vintage is observed."},{"kind":"forecast","point":6701661,"ciLow":6701660,"ciHigh":6701662}]}

# Reviewer critique
{
  "summary": "Draft is not publishable as a forecast because it uses the resolved March 2026 official first print as evidence and sets the point estimate equal to the outcome.",
  "requiredFixes": [
    {
      "rubricItem": "leakage",
      "severity": "blocking",
      "summary": "The draft states the official March 2026 fixed vintage was already posted at run time and uses the printed value 6,701,661 directly.",
      "actionRequested": "Remove resolved-outcome evidence from the forecast record, including the March 2026 value, post-release PDF lookup, and any reasoning based on the June 12, 2026 print."
    },
    {
      "rubricItem": "update",
      "severity": "blocking",
      "summary": "The material movement from the prior is justified by observing the target outcome, not by pre-resolution evidence.",
      "actionRequested": "Base any update only on evidence available before the first March 2026 print, and explain why that evidence moves the forecast from the prior."
    },
    {
      "rubricItem": "interval",
      "severity": "blocking",
      "summary": "The 80% interval of 6,701,660 to 6,701,662 reflects transcription risk after seeing the outcome, not forecast uncertainty.",
      "actionRequested": "Set the interval from realized pre-release volatility, model error, or explicit ex-ante uncertainty."
    },
    {
      "rubricItem": "coherence",
      "severity": "blocking",
      "summary": "The historicalContext labels the target value as 'Mar 2026 first print', making the JSON a resolved data extraction rather than a forecast.",
      "actionRequested": "Remove target-period realized values from historicalContext and ensure point, interval, drivers, and reasoning are all ex-ante."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft gives a seasonal persistence/base-rate discussion but does not clearly state a time-series or model prior or explicitly rule one out.",
      "actionRequested": "Add a brief model-prior statement, such as a persistence/seasonal naive prior, or explain why no formal time-series prior is used."
    }
  ],
  "optionalSuggestions": [
    "Keep the resolver language and official USDA FNS source, but distinguish resolution metadata from evidence used for forecasting.",
    "Tie tail scenarios to pre-release WIC participation drivers such as enrollment trend, seasonal March rebound size, and administrative disruptions."
  ]
}

Emit the final JSON object only.
