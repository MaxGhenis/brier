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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US initial claims, week ending Jul 11","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial unemployment insurance claims for the week ending July 11, 2026, in the first print?","unit":"thousands","pointEstimate":216,"ciLow":202.5,"ciHigh":229.5,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the first-print advance figure for seasonally adjusted initial claims for regular state programs for the week ending July 11, 2026, as published in the U.S. Department of Labor Unemployment Insurance Weekly Claims Report released July 16, 2026. Use the Initial Claims (SA) figure, convert persons to thousands, and ignore all later revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"latest_week_2026-07-04_sa_initial_claims","value":215},{"label":"prior_week_2026-06-27_sa_initial_claims_revised","value":217},{"label":"week_2026-06-20_sa_initial_claims","value":216},{"label":"latest_4wk_average","value":218.75},{"label":"latest_nsa_initial_claims","value":224.583}],"drivers":["recent SA claims clustered near 215 thousand","four-week average at 218.75 thousand","latest weekly change only -2 thousand","holiday-week NSA rise mostly expected by seasonal factors","no broad layoff shock evident in state comments"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://www.dol.gov/newsroom/releases/eta","https://www.dol.gov/newsroom/economicdata"],"runAt":"2026-07-10T02:53:43Z","reasoning":[{"kind":"heading","text":"US initial claims SA forecast for week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this is the U.S. Department of Labor Unemployment Insurance Weekly Claims Report, Initial Claims (SA), regular state programs, advance first print, for the week ending July 11, 2026. All anchors below use the same seasonally adjusted initial-claims variant; NSA figures are used only as diagnostics."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL economic-data page and current weekly UI claims PDF for release source and timing.","result":"DOL economic-data page says the Office of Unemployment Insurance publishes the Unemployment Insurance Weekly Claims Report and that the PDF is updated each week; the current PDF is embargoed until 8:30 A.M. Eastern on Thursday, July 9, 2026, for week ending July 4, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL ETA release index for recent official weekly release sequence around the target window.","result":"DOL ETA release index shows Unemployment Insurance Weekly Claims Report releases dated July 9, 2026; July 2, 2026; June 25, 2026; June 18, 2026; June 11, 2026; and June 4, 2026. With the ledger release window of July 14-18, 2026, the scheduled first print for week ending July 11 is Thursday, July 16, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest DOL headline seasonally adjusted claims figures from the July 9, 2026 weekly release.","result":"For week ending July 4, 2026, advance SA initial claims were 215,000, down 2,000 from the revised prior week of 217,000; the 4-week moving average was 218,750, down 3,750 from the revised prior average of 222,500."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent DOL historical SA initial-claims table from the current weekly release.","result":"Recent SA initial claims in thousands: May 30 225, June 6 230, June 13 227, June 20 216, June 27 217, July 4 215; recent weekly changes were +13, +5, -3, -11, +1, -2."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest DOL unadjusted diagnostic data and state comments from the current weekly release.","result":"For week ending July 4, 2026, unadjusted initial claims were 224,583, up 9,967 from 214,616; seasonal factors expected an increase of 11,478. Comparable 2025 unadjusted claims were 241,361. State comments included New York +4,855 advance NSA claims, Michigan +4,401, Tennessee +2,310, and Texas 13,625 advance NSA claims."},{"kind":"text","text":"Reference class and base rate: one-week-ahead SA initial claims are highly persistent. The recent official reference class is a 12-week band from 190 to 230 thousand, with the last six prints at 225, 230, 227, 216, 217, and 215. The base rate forecast is therefore close to the latest 215 thousand, with a modest pull toward the 218.75 thousand four-week average."},{"kind":"math","text":"Prior/update/interval: persistence prior = 215.0 from the July 4 first-print SA initial-claims level. Historical sample = 11 successive weekly changes from April 18 through July 4: -25,+9,+13,-2,+2,+13,+5,-3,-11,+1,-2 thousand; mean = 0.0 and sigma = sqrt(1212/11) = 10.5. Adjustments: level +1.0 toward the 218.75 four-week average, momentum 0.0 after the latest -2 change, one-off +0.0 because the July holiday NSA rise was already largely expected by seasonal factors, and policy mechanism +0.0 with no Extended Benefits trigger. Point = 215.0 + 1.0 = 216.0. 80% half-width = 1.28*sigma = 13.4, rounded to 13.5, giving 202.5 to 229.5 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is a larger education, transportation, manufacturing, or state-processing layoff wave that would land above the interval; downside risk is faster reversal of holiday filings or fewer broad layoffs that would land below the interval. Outside the interval would likely require a fresh state-specific reporting shock or a genuine layoff shock comparable to the recent -25 or +23 thousand weekly moves."},{"kind":"forecast","point":216,"ciLow":202.5,"ciHigh":229.5}]}

# Reviewer critique
{
  "summary": "The draft is publishable with no blocking issues, but it should tighten the resolver wording against the canonical ALFRED/DOL source binding.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft names the DOL PDF as the resolution URL, while the canonical ledger source binding specifies the ALFRED graph CSV for ICSA with DOL also allowed as an official host.",
      "actionRequested": "Clarify that the target resolves to the first available advance vintage for ICSA under the ledger binding, with DOL Weekly Claims as the official first-print source and ALFRED ICSA advance vintage as the mechanical resolver when used by the catalog."
    }
  ],
  "optionalSuggestions": [
    "State that the 80% interval is in thousands throughout, since the DOL release is in persons and the ledger applies a 0.001 transform.",
    "The tail scenarios are adequate, but could name the approximate threshold moves implied by the interval: below 202.5 or above 229.5 thousand."
  ]
}

Emit the final JSON object only.
