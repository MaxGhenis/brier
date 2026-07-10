# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-11"
- targetUnit: "millions"

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US continued claims, week ending Jul 11","question":"What will the U.S. Department of Labor report as the first-print advance number for seasonally adjusted insured unemployment, also called continued claims, for the week ending July 11, 2026?","unit":"millions","pointEstimate":1.824,"ciLow":1.786,"ciHigh":1.862,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor, Employment and Training Administration, Unemployment Insurance Weekly Claims news release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print number for seasonally adjusted insured unemployment during the week ending July 11, 2026 in the UI Weekly Claims news release first published July 23, 2026, converted from persons to millions and rounded to the nearest 0.001 million. Ignore later revisions or archive updates after the first official print.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 SA insured unemployment latest official advance","value":1.814},{"label":"2026-06-20 SA insured unemployment revised","value":1.806},{"label":"2026-06-13 SA insured unemployment","value":1.812},{"label":"2026-06-27 four-week average","value":1.808},{"label":"2025-06-28 comparable prior-year SA insured unemployment","value":1.952}],"drivers":["Recent continued-claims level near 1.81 million","Four-week average rising modestly","Initial claims eased to 215,000 for week ending July 4","Two unpublished weeks add short-horizon uncertainty","No Extended Benefits trigger in latest official release"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/series/CCSA"],"runAt":"2026-07-09T22:38:29Z","reasoning":[{"kind":"heading","text":"Forecast for DOL continued claims, week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this targets the DOL ETA UI Weekly Claims Report series for seasonally adjusted insured unemployment, also called continued claims, for the week ending July 11, 2026. The variant is SA insured unemployment from regular state programs, not NSA state totals and not all-program continued weeks claimed."},{"kind":"tool","tool":"official.lookup","call":"Opened the DOL ETA UI Weekly Claims archive and publication schedule page.","result":"The DOL page says the UI Weekly Claims News Release is published each week on Thursday at 8:30 AM EST, lists Wednesday November 25, 2026 as the 2026 non-Thursday exception, and shows the page was updated July 9, 2026. For the continued-claims week ending July 11, 2026, the first Thursday release after the normal two-week lag is July 23, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the current DOL UI Weekly Claims news release PDF dated July 9, 2026.","result":"The release reports advance seasonally adjusted insured unemployment of 1,814,000 for the week ending June 27, 2026, up 8,000 from the revised 1,806,000 for June 20, with a four-week average of 1,808,000."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL seasonally adjusted weekly claims history table in the same July 9, 2026 release.","result":"Recent SA insured unemployment values were 1,786,000 for May 30, 1,800,000 for June 6, 1,812,000 for June 13, 1,806,000 for June 20, and 1,814,000 for June 27; the comparable June 28, 2025 value was 1,952,000."},{"kind":"tool","tool":"history.lookup","call":"Opened FRED CCSA as a public history mirror for DOL ETA continued claims.","result":"FRED CCSA shows 2026-06-27 at 1,814,000, 2026-06-20 at 1,806,000, 2026-06-13 at 1,812,000, 2026-06-06 at 1,800,000, and 2026-05-30 at 1,786,000, updated July 9, 2026 7:34 AM CDT, with next release date July 16, 2026."},{"kind":"text","text":"Reference class and base rate: for one- to two-week-ahead SA continued-claims forecasts, the strongest base rate is persistence in the recent DOL SA level plus the recent average weekly change. The last five published levels rose from 1.786 million to 1.814 million, but initial claims for July 4 were 215,000 and the four-week initial-claims average was 218,750, so the near-term pressure is mild rather than a breakout."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official SA insured unemployment of 1.814 million; historical sample = 53 fetched weekly changes from the DOL table, June 28, 2025 through June 27, 2026; adjustment components = +0.010 million for two weeks of modest recent upward momentum, 0.000 million for policy mechanics because no Extended Benefits trigger was on, and 0.000 million for variant conversion because all anchors use the same SA insured-unemployment variant. Point = 1.814 + 0.010 = 1.824 million. For the fetched weekly changes, sigma = 0.0208 million, so one-week 80% half-width is 1.28*sigma = 0.0266 million. Because the target is two unpublished weeks ahead, I scale by sqrt(2), giving about 0.0376 million, rounded to 0.038 million; interval = 1.824 +/- 0.038 = [1.786, 1.862] million."},{"kind":"text","text":"Level and momentum effects: the latest 1.814 million is above the May 30 level by 0.028 million but still below the comparable prior-year value of 1.952 million. Momentum argues for a small increase, while the latest initial-claims easing to 215,000 limits the upward adjustment."},{"kind":"text","text":"Counter-considerations: upside risk would come from a delayed follow-through from late-June layoffs or seasonal-adjustment miss that lifts continued claims above 1.862 million. Downside risk would come from faster exits from UI rolls or lower July initial claims that pull the print below 1.786 million. A holiday-week reporting distortion or a large state-level administrative revision would be the main outside the interval scenario."},{"kind":"forecast","point":1.824,"ciLow":1.786,"ciHigh":1.862}]}

# Reviewer critique
{"summary":"Draft is publishable after one small methodological clarification; resolver, unit, first-print rule, resolution date, and point/interval coherence are otherwise sound.","requiredFixes":[{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact step says the historical sample contains 53 weekly changes from June 28, 2025 through June 27, 2026, but that date range appears to contain 53 weekly observations and 52 week-to-week changes unless an additional prior observation was included.","actionRequested":"Clarify whether the interval sigma used 53 observations/52 changes or included one earlier week to produce 53 changes, and adjust the sample-count wording or sigma if needed."}],"optionalSuggestions":["State that FRED is used only as a history mirror, not as the resolution source, to avoid any ambiguity.","Mention the July 16 intermediate release as future evidence not used in this forecast, or omit it from the source summary to keep the resolver focus on July 23."]}

Emit the final JSON object only.
