# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.job_openings_total.may_2026.first_print
- period: May 2026
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
{"slug":"bls-jolts-job-openings-total-may-2026-first-print","country":"US","type":"data","title":"US JOLTS job openings, May 2026","question":"BLS JOLTS total nonfarm job openings, seasonally adjusted level, May 2026, first print","unit":"thousands","pointEstimate":7350,"ciLow":6650,"ciHigh":8050,"confidence":0.8,"resolutionDate":"2026-06-30","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey news release","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.htm","resolutionRule":"Resolve to the first-published BLS JOLTS seasonally adjusted total nonfarm job openings level for May 2026. Use the preliminary first-print value released on June 30, 2026; ignore subsequent revisions. If the release text states the value in millions, convert to thousands and round to the nearest thousand.","dataPointId":"bls.jolts.job_openings_total.may_2026.first_print","historicalContext":[{"label":"2026-04 latest preliminary","value":7618},{"label":"2026-03","value":6887},{"label":"2026-02","value":6922},{"label":"2026-01","value":7240},{"label":"2025 average","value":7082}],"drivers":["April openings jumped to 7.618 million, above the recent 7.17 million four-month average","May payroll growth of 172,000 and unchanged 4.3 percent unemployment argue against a sharp demand drop","JOLTS openings are noisy month to month, with recent changes including plus 731 thousand and minus 318 thousand","Longer 2025 baseline near 7.08 million pulls the forecast below April","80 percent interval widened for survey volatility and possible reversal of April spike"],"sourceContext":["https://www.bls.gov/schedule/2026/home.htm","https://data.bls.gov/timeseries/JTS000000000000000JOL","https://www.bls.gov/news.release/empsit.nr0.htm"],"runAt":"2026-06-27T13:08:03Z","reasoning":[{"kind":"heading","text":"Forecast for May 2026 first-print BLS JOLTS total job openings"},{"kind":"text","text":"The resolver is the BLS first print for total nonfarm job openings, seasonally adjusted, level in thousands, for May 2026. This is a data release target, not a revision target."},{"kind":"tool","tool":"official.lookup","call":"Checked the official BLS 2026 release calendar for the May 2026 JOLTS release date.","result":"BLS calendar lists Job Openings and Labor Turnover Survey for May 2026 at 10:00 AM on Tuesday, June 30, 2026; the same calendar shows April 2026 JOLTS released June 2, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official BLS time-series page for JTS000000000000000JOL, total nonfarm job openings, seasonally adjusted, level in thousands.","result":"Fetched latest BLS values: 2026 Jan 7240, Feb 6922, Mar 6887, Apr 7618(P); 2025 monthly values included Jan 7431 and Dec 6550."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official BLS Employment Situation release for May 2026 for labor-market contemporaneous evidence.","result":"BLS reported May 2026 nonfarm payroll employment increased by 172,000, unemployment was 4.3 percent, April payroll growth was revised to 179,000, and March was revised to 214,000."},{"kind":"text","text":"Base-rate/reference-class anchor: the 2025 average from fetched BLS monthly levels is about 7,082 thousand, while the first four months of 2026 average about 7,167 thousand. That keeps the outside-view anchor around 7.1 to 7.2 million rather than treating April's 7.618 million as the new trend."},{"kind":"text","text":"Level and momentum effects point in opposite directions. April's 7.618 million level is high relative to January through March, but May payrolls were solid and unemployment was unchanged, so I expect only a partial reversal of the April jump rather than a fall back to the March trough."},{"kind":"text","text":"Counter-consideration: JOLTS openings can swing sharply on survey noise and industry composition. If April's spike was genuine vacancy rebuilding, May could print above 8.0 million; if it was sampling noise or employers pulled postings after tariff and demand uncertainty, a print near 6.6 million is plausible."},{"kind":"math","text":"Recent monthly changes from fetched levels were Feb minus Jan = -318, Mar minus Feb = -35, and Apr minus Mar = +731 thousand. I place May 268 thousand below April but above the 2026 average: 7618 - 268 = 7350. For the 80% interval, use roughly +/-700 thousand around the point, widened for JOLTS volatility: 7350 - 700 = 6650 and 7350 + 700 = 8050."},{"kind":"text","text":"Upside scenario: openings remain near or above April because May payroll growth of 172,000 and upward revisions to March and April indicate resilient labor demand. Downside scenario: April's jump reverses and openings return toward the March 6.887 million level. Outside-the-interval scenarios require either an unusually large vacancy retrenchment below 6.65 million or a broad demand reacceleration above 8.05 million."},{"kind":"forecast","point":7350,"ciLow":6650,"ciHigh":8050}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, but the first-print resolver should be tightened and the model-prior/interval rationale should be made more explicit.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"Resolver names BLS JOLTS first print, but the source/rule could still accidentally use rounded news-release prose or later-revised time-series data.","actionRequested":"Specify the exact BLS release table/series field to resolve from: May 2026 first-published seasonally adjusted Total nonfarm job openings level, in thousands, from the June 30, 2026 JOLTS release/table or archived first-print artifact; do not use later-revised series values or rounded narrative text."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft gives a persistence/base-rate prior but does not clearly state whether a time-series/model prior was used or explicitly ruled out.","actionRequested":"Add one sentence saying whether the forecast uses a simple persistence/mean-reversion model instead of a fitted time-series model, or state why a formal model was not used."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is described as roughly +/-700 thousand, but it is based mainly on a few recent monthly moves rather than a stated realized-volatility calculation or explicit subjective uncertainty scale.","actionRequested":"Tie the interval to a concrete volatility reference, such as recent absolute monthly changes or historical JOLTS month-to-month error ranges, or label it explicitly as judgmental uncertainty."}],"optionalSuggestions":["Clarify that the unit is thousands throughout, so 7350 means 7.350 million openings.","Keep the May Employment Situation evidence framed as public pre-release evidence, not as resolver evidence."]}

Emit the final JSON object only.
