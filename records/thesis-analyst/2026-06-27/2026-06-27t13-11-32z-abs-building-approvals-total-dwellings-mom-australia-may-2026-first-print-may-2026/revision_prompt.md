# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.building_approvals.total_dwellings_mom.australia.may_2026.first_print
- period: May 2026
- conditional_on: null

# Source hints
- Use ABS release calendar and official monthly CPI indicator pages.
- Australia CPI indicator rates print to one decimal.
- Resolution source should be the ABS release page.

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
{"slug":"abs-building-approvals-total-dwellings-mom-australia-may-2026-first-print","country":"AU","type":"data","title":"Australia building approvals May 2026 MoM","question":"ABS Building Approvals, Australia: seasonally adjusted total dwelling units approved, May 2026 monthly percent change, first print","unit":"percent_growth","pointEstimate":2.0,"ciLow":-10.0,"ciHigh":16.0,"confidence":0.8,"resolutionDate":"2026-07-01","resolutionSource":"Australian Bureau of Statistics Building Approvals, Australia release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026","resolutionRule":"Resolve to the first ABS-published May 2026 seasonally adjusted monthly change in total dwelling units approved, in percent, as shown in Building Approvals, Australia on 2026-07-01 at 11:30am AEST. Use the first print only; ignore later revisions, including the updated small-area data-cube release scheduled for 2026-07-08. If ABS reports one decimal place, resolve to that one-decimal value.","dataPointId":"abs.building_approvals.total_dwellings_mom.australia.2026-05.first_print","historicalContext":[{"label":"Apr 2026 first print total dwellings MoM percent","value":-3.4},{"label":"Mar 2026 first print total dwellings MoM percent","value":-10.5},{"label":"Feb 2026 first print total dwellings MoM percent","value":29.7},{"label":"Jan 2026 first print total dwellings MoM percent","value":-7.2},{"label":"Apr 2026 seasonally adjusted total dwellings level","value":16710}],"drivers":["April level was below trend, leaving room for partial mean reversion","Large multi-unit swings dominate month-to-month volatility","Underlying trend was close to flat after earlier 2026 gains","Housing-supply policy support is positive but unlikely to remove monthly noise","High construction costs and feasibility constraints cap upside"],"sourceContext":["https://www.abs.gov.au/release-calendar/future-releases/202607","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/mar-2026","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/feb-2026","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/jan-2026"],"runAt":"2026-06-27T13:11:37Z","reasoning":[{"kind":"heading","text":"Forecast May 2026 ABS total dwelling approvals monthly change"},{"kind":"text","text":"The resolver is the first ABS print for Building Approvals, Australia, May 2026: seasonally adjusted total dwelling units approved, monthly percent change. The July 8 updated-information item is excluded because the target is first print."},{"kind":"tool","tool":"official.lookup","call":"ABS July 2026 future release calendar for Building Approvals, Australia May 2026","result":"Fetched official schedule: Building Approvals, Australia, reference period May 2026, Wednesday 01 July 2026 at 11:30am AEST; updated information for the same May 2026 reference period is scheduled Wednesday 08 July 2026 at 11:30am AEST."},{"kind":"tool","tool":"official.lookup","call":"ABS April 2026 Building Approvals latest release key statistics and table","result":"Fetched April 2026 first-print context: total dwelling units approved fell 3.4% to 16,710; private sector houses fell 1.0% to 10,088; private sector dwellings excluding houses fell 3.6% to 6,403; trend total dwelling units were 17,363 with 0.0% monthly change."},{"kind":"tool","tool":"official.lookup","call":"ABS March 2026 Building Approvals release","result":"Fetched March 2026 first-print context: total dwellings approved fell 10.5% to 17,300; private sector dwellings excluding houses fell 26.0% to 6,632; private sector houses rose 0.9% to 10,194; trend total dwellings were 17,657 with 0.5% monthly change."},{"kind":"tool","tool":"official.lookup","call":"ABS February and January 2026 Building Approvals releases","result":"Fetched February 2026 total dwellings approved rose 29.7% to 19,022 and trend rose 1.2% to 17,566; fetched January 2026 total dwellings approved fell 7.2% to 14,564 and trend was 16,386 with -0.1% monthly change."},{"kind":"text","text":"Base-rate/reference-class anchor: recent first prints show very high realized monthly dispersion, with January -7.2, February +29.7, March -10.5, and April -3.4. The central tendency is closer to low positive or flat than to the extreme February rebound."},{"kind":"text","text":"Level and momentum split: the April level of 16,710 was about 3.8% below the April trend level of 17,363, so I allow a modest bounce. Momentum is negative over March-April, so the bounce should be smaller than the February spike."},{"kind":"text","text":"Mechanism split: detached houses were comparatively stable while multi-unit approvals drove the big 2026 swings. Policy pressure to lift housing supply is an upside force, but financing, construction costs, and project feasibility keep the near-term print noisy rather than persistently strong."},{"kind":"math","text":"Point: start from a flat-to-slightly-positive base rate near +0.5%, add about +2.0 percentage points for mean reversion from April being 3.8% below trend, subtract about -0.5 percentage points for weak March-April momentum, giving +2.0%. Interval: recent monthly changes span roughly -10.5% to +29.7%; for an 80% first-print interval, use about -12/+14 percentage points around the point, skewed upward for apartment-project lumpiness, giving -10.0% to +16.0%."},{"kind":"text","text":"Counter-consideration and scenarios: downside outside the interval would be another large apartment-project drop or delayed approvals pushing the print below -10.0%; upside outside the interval would be a renewed multi-unit approval surge like February, above +16.0%; the central case is a partial rebound with no repeat of February's one-off jump."},{"kind":"forecast","point":2.0,"ciLow":-10.0,"ciHigh":16.0}]}

# Reviewer critique
{"summary":"Draft is publishable after minor cleanup: resolver and forecast fields are mostly coherent, but the model-prior treatment and one evidence citation need tightening.","requiredFixes":[{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses recent observations and trend levels but does not clearly state whether a formal time-series/model prior was used or ruled out.","actionRequested":"Add one sentence explicitly saying the model prior is a persistence/recent-volatility prior, or that no formal time-series model was fit and why."},{"rubricItem":"resolver","severity":"warning","summary":"The cited `latest-release` URL is unstable and will later point to May 2026 or newer data, weakening the audit trail for April 2026 evidence.","actionRequested":"Replace the `latest-release` evidence URL with the stable April 2026 ABS release URL, or clearly label the captured latest-release page as April 2026 context."}],"optionalSuggestions":["State the 80% interval as derived from recent first-print volatility despite the small four-month sample.","Clarify that the unit is percentage points of month-over-month percent change, matching ABS one-decimal reporting."]}

Emit the final JSON object only.
