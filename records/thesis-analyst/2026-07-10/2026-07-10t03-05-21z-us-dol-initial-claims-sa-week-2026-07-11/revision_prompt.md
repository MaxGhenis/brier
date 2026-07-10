# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-11"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US Initial Claims, Week Ending Jul 11","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial claims for unemployment insurance for the week ending July 11, 2026, first print?","unit":"thousands","pointEstimate":216,"ciLow":202,"ciHigh":230,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print U.S. total seasonally adjusted initial claims figure, in thousands, for the week ending July 11, 2026, as published by the U.S. Department of Labor Employment and Training Administration in the Unemployment Insurance Weekly Claims release dated July 16, 2026. Use the release's rounded thousand value; ignore later revisions and ALFRED/FRED vintage updates except as mirrors of the first official print.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"latest_week_2026-07-04_sa_initial_claims","value":215},{"label":"prior_week_2026-06-27_sa_initial_claims_revised","value":217},{"label":"week_2026-06-20_sa_initial_claims","value":216},{"label":"latest_4wk_average_2026-07-04","value":218.75},{"label":"prior_year_comparable_week_sa_initial_claims","value":228}],"drivers":["Latest SA initial claims were 215 thousand, down 2 thousand from the revised prior week.","The 4-week average fell to 218.75 thousand, keeping the near-term level around the high 210s.","Seasonally adjusted continuing claims were stable at 1814 thousand for the lagged week, not signaling a fresh layoff break.","July holiday-week adjustment can create noise, but the target is the SA advance print from the same DOL variant."],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-10T03:05:28Z","reasoning":[{"kind":"heading","text":"Forecast for DOL SA Initial Claims, Week Ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the U.S. Department of Labor Employment and Training Administration advance seasonally adjusted U.S. initial claims value, series code ICSA in the ledger, for week ending July 11, 2026, first print only. The DOL release dated July 16, 2026 is the resolver; FRED/ALFRED can mirror the vintage but is not the final authority."},{"kind":"tool","tool":"official.lookup","call":"Opened the current DOL UI Weekly Claims PDF release at https://www.dol.gov/ui/data.pdf.","result":"The DOL release was embargoed until 8:30 A.M. Eastern on Thursday, July 9, 2026; for week ending July 4, 2026, advance SA initial claims were 215,000, down 2,000 from the prior week's revised 217,000."},{"kind":"tool","tool":"official.lookup","call":"Read the national summary table in the same DOL release.","result":"The table reports Initial Claims (SA) of 215,000 for July 4, 217,000 for June 27, 216,000 for June 20, and 228,000 for the comparable prior-year week; the 4-week moving average was 218,750."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL continuing-claims and OUI data-page context.","result":"The DOL release reports seasonally adjusted insured unemployment of 1,814,000 for week ending June 27, up 8,000 from 1,806,000; the OUI weekly claims data page was updated July 9, 2026."},{"kind":"text","text":"Variant check: every numeric anchor used here is the DOL seasonally adjusted U.S. initial claims variant from the weekly release, in thousands, matching the target unit and the ICSA-style target. NSA state totals such as 224,583 for July 4 are used only as qualitative context, not as target-history inputs."},{"kind":"text","text":"Reference class and base rate: for the 2026 year-to-date SA initial-claims sequence through July 4, the level mostly sat in the 201-230 thousand range, with a recent 4-week average of 218.75 thousand. A persistence base rate around the latest 215 thousand is stronger than a trend-extrapolated jump because the latest four weekly changes were +5, -3, +1, and -2 thousand."},{"kind":"math","text":"Prior/update/interval: persistence prior model on the DOL SA initial-claims level uses the January 3-July 4, 2026 historical sample of weekly changes: -6, +9, +1, +19, 0, -22, +3, +3, -1, -8, +6, -8, +15, -10, +7, -25, +9, +13, -2, +2, +13, +5, -3, -11, +1, -2 thousand. The average change is +0.3, so latest 215 + 0.3 gives 215.3; level/momentum adjustment is +0.5 for the still-low but slightly below-average latest print, one-off July-holiday noise adjustment is 0 after seasonal adjustment, and policy-mechanism adjustment is 0. Rounded point = 216. For interval sizing, sigma = 10.4 from those successive changes; 1.28*sigma = 13.3, rounded to a 14 thousand half-width, giving final implied bounds 216 - 14 = 202 and 216 + 14 = 230."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed education, transportation, or manufacturing layoff pulse like the prior large state moves, which would land above the interval if SA claims print above 230 thousand. Downside risk is another broad low-layoff week with holiday-seasonal factors absorbing NSA filings, which would land below the interval if the first print is under 202 thousand. Outside the interval would therefore require a weekly move larger than roughly the recent 80% one-week change range."},{"kind":"forecast","point":216,"ciLow":202,"ciHigh":230}]}

# Reviewer critique
{"summary":"The draft is publication-ready on resolver, prior, update logic, interval construction, tails, and JSON coherence, with no blocking fixes identified.","requiredFixes":[],"optionalSuggestions":["Clarify that the DOL release is expected on July 16, 2026 under the weekly Thursday release cadence, while the ledger sourceBinding may mirror the first print through ALFRED/FRED.","Slightly tighten the continuing-claims driver from “stable” to “up 8 thousand but broadly stable” to match the cited evidence exactly."]}

Emit the final JSON object only.
