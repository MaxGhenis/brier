# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: eurostat.hicp.all_items_annual_rate.euro_area.june_2026.flash
- period: June 2026 flash
- conditional_on: null

# Source hints
- Use Eurostat euro-indicators release calendar and official HICP/IP pages.
- Euro-area HICP rates print to one decimal.
- Resolution source should be the Eurostat release/data page.

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
{"slug":"eurostat-hicp-ea-annual-rate-june-2026-flash","country":"EA","type":"data","title":"Euro area HICP inflation, June 2026 flash","question":"Eurostat euro area HICP all-items annual inflation rate for June 2026, flash first print, not seasonally adjusted, rounded to one decimal percent.","unit":"percent","pointEstimate":2.0,"ciLow":1.7,"ciHigh":2.3,"confidence":0.8,"resolutionDate":"2026-07-01","resolutionSource":"Eurostat euro-indicators release and HICP monthly data page","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_manr/default/table?lang=en","resolutionRule":"Resolve to the first Eurostat flash estimate for euro area all-items HICP annual inflation for June 2026, in percent year over year, rounded to one decimal. Use the first official Eurostat euro-indicators release or first posted Eurostat HICP dataset value for June 2026 flash; ignore later revisions or final HICP updates.","dataPointId":"eurostat.prc_hicp_manr.CP00.EA20.2026-06.flash_first_print","historicalContext":[{"label":"May 2026 flash all-items annual rate","value":1.9},{"label":"April 2026 all-items annual rate","value":2.2},{"label":"March 2026 all-items annual rate","value":2.2},{"label":"February 2026 all-items annual rate","value":2.4},{"label":"January 2026 all-items annual rate","value":2.3}],"drivers":["Recent euro-area headline HICP has been close to the ECB target but drifting lower into May.","Services inflation remains the main upside source because it is stickier than energy or goods.","Energy base effects and monthly fuel volatility can move the rounded headline by a tenth or two.","Food inflation is still positive enough to prevent a broad undershoot below 1.7 without a large energy drag.","Flash estimates print to one decimal, so rounding compresses small signal differences."],"sourceContext":["https://ec.europa.eu/eurostat/web/main/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_manr/default/table?lang=en","https://ec.europa.eu/eurostat/cache/metadata/en/prc_hicp_esms.htm"],"runAt":"2026-06-27T13:13:42Z","reasoning":[{"kind":"heading","text":"Euro area June 2026 HICP flash forecast"},{"kind":"text","text":"The target is the first Eurostat flash print for euro area all-items HICP annual inflation in June 2026. The resolver is the official Eurostat euro-indicators HICP flash release or its first-posted HICP data value, rounded to one decimal, with subsequent revisions ignored."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat euro-indicators release calendar for the June 2026 euro area inflation flash estimate.","result":"Calendar showed the June 2026 euro area annual inflation flash estimate scheduled for 2026-07-01, with release timing tied to the euro-indicators calendar."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent Eurostat all-items HICP annual rates for EA20 from prc_hicp_manr, CP00, annual rate.","result":"Fetched recent headline values: 2026-05 flash 1.9, 2026-04 2.2, 2026-03 2.2, 2026-02 2.4, 2026-01 2.3 percent."},{"kind":"text","text":"Reference-class base rate: the latest five official monthly prints average 2.2 percent, while the latest value is 1.9 percent. I anchor slightly above the latest print because one low month does not fully reset the annual-rate process, but below the five-month mean because the recent direction is lower."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat component context for the latest flash inflation composition.","result":"Latest component readings used for direction: services 3.2, food alcohol and tobacco 3.3, non-energy industrial goods 0.6, energy -3.6 percent."},{"kind":"text","text":"Level and momentum: the headline level is already near 2 percent. Momentum from January to May is negative by 0.4 percentage point, but the last observation at 1.9 is close enough to target that a large further fall would need another downside surprise in energy or package holidays."},{"kind":"text","text":"Mechanisms: services persistence and food keep upside pressure in the core-like part of the basket, while energy remains the main downside and volatility channel. ECB policy works with a lag and is more relevant to medium-term demand than to this one-month flash print."},{"kind":"text","text":"Counter-consideration: the forecast could be too high if June fuel and electricity effects are sharply negative or if services repricing fades abruptly; it could be too low if travel, accommodation, or food prices rebound and energy base effects stop dragging."},{"kind":"math","text":"Starting from the latest print of 1.9, add 0.1 for mean reversion toward the five-month official average of 2.2, add 0.0 for mixed energy/core pressures after offsetting services persistence against energy drag, giving 2.0 after one-decimal rounding. Recent realized monthly first-print dispersion around this target supports an 80 percent interval of about plus or minus 0.3 percentage point, so 1.7 to 2.3."},{"kind":"text","text":"Upside scenario: services and food remain sticky and energy stops subtracting, producing a rounded 2.3 or slightly higher. Downside scenario: energy and goods weaken together, pulling the rounded print to 1.7 or below. Outside-interval scenarios require a broad energy shock or a surprisingly synchronized rebound across services, food, and energy."},{"kind":"forecast","point":2.0,"ciLow":1.7,"ciHigh":2.3}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the first-print resolver and making the model/interval basis more explicit.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"Resolver allows either the euro-indicators flash release or the first posted dataset value, but the data browser may later show revised/final HICP rather than preserving the first flash print.","actionRequested":"State that the Eurostat euro-indicators June 2026 flash release is the primary resolver, with the dataset only usable if it demonstrably records the same first flash value; ignore later final/revised prc_hicp_manr values."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses a latest-print/five-month-mean prior but does not explicitly state whether a time-series model prior was used or ruled out.","actionRequested":"Add one sentence explicitly naming the model prior, e.g. persistence/random-walk from the latest flash plus light mean reversion, or explicitly rule out a fitted model due to short-horizon flash-data constraints."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is justified by 'recent realized monthly first-print dispersion' but no realized-volatility sample or calculation is shown.","actionRequested":"Add the sample basis for the +/-0.3 pp interval, or rephrase it as explicit judgmental uncertainty rather than a volatility-derived interval."}],"optionalSuggestions":["Clarify whether all historicalContext values are first flash prints or later official monthly values.","Name the release timezone for the 2026-07-01 resolution date if the catalog supports it."]}

Emit the final JSON object only.
