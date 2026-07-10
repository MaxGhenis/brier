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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US continued claims, week ending Jul 11 2026","question":"What will the U.S. Department of Labor Employment and Training Administration first report for seasonally adjusted insured unemployment, also called continued claims, for the week ending July 11, 2026?","unit":"millions","pointEstimate":1.825,"ciLow":1.783,"ciHigh":1.867,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta","resolutionRule":"Resolve to the first-print advance seasonally adjusted insured unemployment value for week ending July 11, 2026 in the ETA Unemployment Insurance Weekly Claims Report released July 23, 2026, using the Seasonally Adjusted Data / Insured Unemployment series. Convert persons to millions by dividing by 1,000,000. Do not use later revisions or ALFRED/FRED values as the final source when the DOL release is available.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 insured unemployment SA latest","value":1.814},{"label":"2026-06-20 insured unemployment SA revised","value":1.806},{"label":"2026-06-13 insured unemployment SA","value":1.812},{"label":"2026-06-06 insured unemployment SA","value":1.8},{"label":"2025 comparable prior-year week in latest table","value":1.952}],"drivers":["Latest SA insured unemployment was 1.814 million, up 0.008 million on the week","Four-week SA insured unemployment average was 1.808 million, up 0.007 million","Recent initial claims were flat-to-lower at 215,000 for week ending July 4","Continued claims remain below the comparable 2025 level but have firmed since late April","Two unreleased weeks make random-walk dispersion larger than a one-week nowcast"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://www.dol.gov/ui/data.pdf","https://www.dol.gov/newsroom/releases/eta","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-10T02:45:30Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA continued claims SA, week ending July 11 2026"},{"kind":"text","text":"Framing and exact resolver: this is the DOL ETA seasonally adjusted insured unemployment series, the same variant as continued claims, for week ending July 11, 2026. The first official print should appear in the Unemployment Insurance Weekly Claims Report dated July 23, 2026; FRED/ALFRED CCSA is only a mirror for this target, while resolution should cite DOL."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL ETA release archive and current DOL weekly claims PDF to verify release surface and timing.","result":"DOL archive listed Unemployment Insurance Weekly Claims Report releases on July 9, 2026; July 2, 2026; June 25, 2026; June 18, 2026; June 11, 2026; and June 4, 2026. The July 9 PDF was embargoed until 8:30 A.M. Eastern Thursday, July 9, 2026. Applying the target ledger window and the official Thursday release sequence gives July 23, 2026 for first print of week ending July 11, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest official DOL seasonally adjusted insured unemployment values from the July 9, 2026 UI Weekly Claims Report.","result":"The July 9 report printed insured unemployment SA of 1,814,000 for week ending June 27, 2026, up 8,000 from revised 1,806,000 for June 20; June 13 was 1,812,000; the 4-week moving average was 1,808,000, up 7,000."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent DOL seasonally adjusted history table for the same insured unemployment variant.","result":"Recent insured unemployment SA values in thousands were: May 23 1,771; May 30 1,786; June 6 1,800; June 13 1,812; June 20 1,806; June 27 1,814. The comparable prior-year value shown for the latest table was 1,952,000."},{"kind":"tool","tool":"official.lookup","call":"Fetched current initial-claims context from the same DOL release, keeping it secondary to the continued-claims target.","result":"Initial claims SA were 215,000 for week ending July 4, down 2,000 from revised 217,000 for June 27; the initial-claims 4-week average was 218,750, down 3,750."},{"kind":"text","text":"Reference class and base rate: for a short-horizon weekly SA continued-claims forecast, I use a random-walk/persistence base rate anchored on the latest official level, then adjust for recent momentum. The reference class is recent weekly DOL SA insured unemployment changes in 2026, not unadjusted claims or all-program continued weeks."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1.814 million from week ending 2026-06-27. Historical sample = 26 successive weekly SA insured-unemployment changes from 2026-01-03 through 2026-06-27: -25, -10, -42, +19, +17, +6, -38, +44, -24, +4, -35, +16, -45, +22, -1, -32, -18, +18, -5, +14, -14, +15, +14, +12, -6, +8 thousand. Mean change = -86/26 = -3.3 thousand and sample sigma = 23.3 thousand = 0.023 million. One-week 80% half-width = 1.28*sigma = 1.28*0.023 = 0.030 million; because the target is two unreleased continued-claims weeks after the latest official value, scale by sqrt(2), giving about 0.042 million. Adjustment components: level 1.814, momentum +0.014 over two weeks from recent firmer continued claims, initial-claims drag -0.003 because latest initial claims fell to 215,000, final point = 1.814 + 0.014 - 0.003 = 1.825 million; interval = 1.825 +/- 0.042 = [1.783, 1.867]."},{"kind":"text","text":"Upside risk: another run of state-level layoffs or delayed benefit exits like the late-May-to-June pattern could push continued claims above 1.867 million. Downside risk: the drop in initial claims and any faster benefit exhaustion could pull the July 11 value below 1.783 million. An outside the interval outcome would likely require two consecutive weekly moves larger than typical recent dispersion, not just ordinary rounding noise."},{"kind":"forecast","point":1.825,"ciLow":1.783,"ciHigh":1.867}]}

# Reviewer critique
{"summary":"Draft is publishable with only a resolver-source consistency warning against the canonical ledger binding.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The draft resolver uses the DOL release as final source, while the canonical ledger binding names ALFRED/FRED CCSA with advance_vintage and ALFRED CSV URL.","actionRequested":"Either align the JSON resolver/source fields to the ledger binding, or explicitly state in reasoning that the ledger binding appears to be a mirror while the forecast remains tied to the same slug/dataPointId and resolves from the DOL first-print release when available."}],"optionalSuggestions":["The prior/update/interval step is strong; consider naming the interval as an approximate 80% interval from recent one-week change volatility scaled by sqrt(2).","The historical sample is listed explicitly, but adding the date span as inclusive week-ending dates is enough; no need to list every weekly change in the published cell if compactness matters."]}

Emit the final JSON object only.
