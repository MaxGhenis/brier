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
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-11.first_print"
- sourceBinding: {"adapter": "alfred-fred", "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US continued claims, week ending Jul 11 2026","question":"What will the U.S. Department of Labor Employment and Training Administration report as the first-print seasonally adjusted insured unemployment (continued claims) for regular state programs for the week ending July 11, 2026, in millions?","unit":"millions","pointEstimate":1.82,"ciLow":1.782,"ciHigh":1.858,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260723","resolutionRule":"Resolve to the first DOL ETA Unemployment Insurance Weekly Claims Report print for seasonally adjusted insured unemployment, also called continued claims, for regular state programs for the week ending July 11, 2026. Convert the reported number of persons to millions using factor 0.000001 and round to three decimals for display. Ignore later revisions or later-vintage ALFRED/FRED updates.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 latest SA insured unemployment","value":1.814},{"label":"2026-06-20 prior SA insured unemployment","value":1.806},{"label":"2026-06-13 SA insured unemployment","value":1.812},{"label":"2026-06-06 SA insured unemployment","value":1.8},{"label":"2026-05-30 SA insured unemployment","value":1.786}],"drivers":["latest DOL first-print SA insured unemployment was 1.814m for week ending 2026-06-27","recent six-week SA continued-claims drift has been upward but uneven","initial claims eased to 215000 for week ending 2026-07-04, limiting a large near-term continued-claims jump","July seasonal-adjustment noise around education and auto-related timing remains a material one-week risk","resolution is strict first print for the seasonally adjusted CCSA variant, not NSA continued weeks claimed"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://www.dol.gov/newsroom/economicdata","https://fred.stlouisfed.org/series/CCSA","https://fred.stlouisfed.org/releases/calendar?rid=180&y=2026"],"runAt":"2026-07-10T02:29:47Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA continued claims, week ending 2026-07-11"},{"kind":"text","text":"Framing and exact resolver: the target is DOL ETA seasonally adjusted insured unemployment, also labeled continued claims and mirrored as FRED/ALFRED series CCSA, for week ending Saturday 2026-07-11. This uses the SA regular-state-program variant throughout; NSA continued weeks claimed and all-program totals are not anchors for this forecast."},{"kind":"tool","tool":"release_calendar.lookup","call":"Checked the 2026 Unemployment Insurance Weekly Claims Report release calendar mirror and the DOL economic-data page for the claims report cadence.","result":"The 2026 release calendar lists Unemployment Insurance Weekly Claims Report releases at 7:30 am Central on Thursday 2026-07-16 and Thursday 2026-07-23; the DOL current report is embargoed until 8:30 am Eastern Thursday 2026-07-09, and the DOL economic-data page says the UI weekly claims PDF is updated each week."},{"kind":"tool","tool":"official.lookup","call":"Read the July 9, 2026 DOL UI Weekly Claims Report first-print text and table for the latest SA insured unemployment values.","result":"DOL reported advance seasonally adjusted insured unemployment of 1,814,000 for week ending 2026-06-27, up 8,000 from a revised 1,806,000 for 2026-06-20; the four-week moving average was 1,808,000, up 7,000."},{"kind":"tool","tool":"official.history_table","call":"Extracted recent same-variant SA insured unemployment history from the DOL release table.","result":"Recent SA insured unemployment values in thousands were 1,786 on 2026-05-30, 1,800 on 2026-06-06, 1,812 on 2026-06-13, 1,806 on 2026-06-20, and 1,814 on 2026-06-27."},{"kind":"tool","tool":"fred.mirror","call":"Checked FRED CCSA as a public mirror for source identity, units, and latest observations, without using it as final resolution source.","result":"FRED CCSA showed 2026-06-27: 1,814,000, 2026-06-20: 1,806,000, 2026-06-13: 1,812,000, 2026-06-06: 1,800,000, and updated on Jul 9, 2026 with next release date Jul 16, 2026."},{"kind":"text","text":"Base rate/reference class: the relevant outside-view class is weekly first-print movement in seasonally adjusted insured unemployment over the last year in the same DOL table. From 2025-06-28 at 1.952m to 2026-06-27 at 1.814m, the average weekly change was -2.65k, but the latest six reported changes averaged about +7.2k per week."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: the level anchor is 1.814m; momentum argues modestly higher into early July; lower initial claims at 215000 for week ending 2026-07-04 argue against a breakout; July education and auto seasonal factors can still move the SA print by several tens of thousands."},{"kind":"math","text":"Prior/update/interval: persistence prior from latest DOL SA insured unemployment is 1.814m; historical sample is the 52 one-week same-variant changes from 2025-06-28 through 2026-06-27. Base-rate drift was -2.65k/week, implying 1.809m two weeks ahead, while recent-momentum adjustment adds about +11k versus that drift, giving point 1.820m. From the fetched history, sigma = 21.0k for one-week changes; two-week sigma = sqrt(2)*21.0k = 29.7k; 80% half-width = 1.28*29.7k = 38.1k = 0.038m, so 1.820 +/- 0.038 gives 1.782 to 1.858."},{"kind":"text","text":"Counter-considerations: upside risk is a sharper-than-usual July SA rise if education-related layoffs and slow reemployment lift continued claims, which would land above the interval if the first print exceeds 1.858m. Downside risk is a quick reversal in the latest insured-unemployment rise plus low initial claims feeding through, which would land below the interval if the print is under 1.782m; outside the interval would likely require a weekly move larger than the recent one-year two-week dispersion."},{"kind":"forecast","point":1.82,"ciLow":1.782,"ciHigh":1.858}]}

# Reviewer critique
{
  "summary": "The draft is publishable after clarifying that its historical prior/volatility sample appears to use current or revised same-series observations rather than true first-print vintages.",
  "requiredFixes": [
    {
      "rubricItem": "prior_update_interval",
      "severity": "warning",
      "summary": "The reasoning calls the 52-week sample 'first-print movement,' but the cited DOL/FRED history likely includes revised prior-week values, while the target resolves to the first print.",
      "actionRequested": "Either recompute the prior and interval from ALFRED advance-vintage/first-print CCSA history, or explicitly label the DOL/FRED history as a revised-history proxy and state why it is acceptable for this forecast."
    }
  ],
  "optionalSuggestions": [
    "Mention that 2026-07-23 is the expected first report containing continued claims for week ending 2026-07-11, not merely the next UI release.",
    "If available, cite the ALFRED advance vintage source alongside the DOL release because the ledger binding uses the ALFRED CCSA advance-vintage adapter."
  ]
}

Emit the final JSON object only.
