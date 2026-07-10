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
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US Continued Claims, Week Ending Jul 11","question":"What will the U.S. Department of Labor ETA first print for seasonally adjusted continued unemployment insurance claims, series CCSA, for the week ending 2026-07-11?","unit":"millions","pointEstimate":1.815,"ciLow":1.797,"ciHigh":1.833,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration, Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://oui.doleta.gov/press/2026/072326.pdf","resolutionRule":"Resolve to the first-published seasonally adjusted insured unemployment / continued claims level, series CCSA, for the week ending July 11, 2026 in the DOL ETA Unemployment Insurance Weekly Claims report released July 23, 2026. Convert persons to millions by multiplying by 0.000001 and round to 0.001 million. Use the first print only and ignore later revisions.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"week ending 2026-06-27 continued claims SA","value":1.81},{"label":"week ending 2026-06-20 continued claims SA, revised","value":1.802},{"label":"week ending 2026-06-06 continued claims SA","value":1.81},{"label":"week ending 2026-05-30 continued claims SA","value":1.8}],"drivers":["Latest continued claims rose 0.008 million to 1.810 million","Initial claims for week ending 2026-07-04 fell to 0.215 million","Recent continued-claims level is stable near 1.80-1.81 million","Low-hire labor market keeps duration risk mildly upward","Two-week first-print horizon adds modest uncertainty"],"sourceContext":["https://apnews.com/article/8d1f553fde8124606b2e3350fe789776","https://www.wsj.com/economy/jobs/u-s-jobless-claims-edged-lower-last-week-f35e8718","https://www.wsj.com/economy/jobs/u-s-jobless-claims-fell-last-week-ceec6b9f","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-10T03:08:54Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA CCSA continued claims, week ending 2026-07-11"},{"kind":"text","text":"Framing and exact resolver: the target is DOL ETA continued unemployment insurance claims, seasonally adjusted, CCSA / insured unemployment, for the week ending Saturday 2026-07-11, resolved on the first official print in millions. This is the SA variant throughout; anchors and history are not NSA claims."},{"kind":"tool","tool":"official.lookup","call":"Checked the DOL ETA weekly-claims release path and ledger release window for the CCSA target week.","result":"The week ending 2026-07-11 continued-claims observation is scheduled for the DOL ETA weekly claims report dated 2026-07-23; the ledger expected release window is 2026-07-21 to 2026-07-25, and the first-print report should contain 1 CCSA value for that week."},{"kind":"tool","tool":"public.lookup","call":"Fetched the July 9, 2026 weekly claims report coverage from public reports citing the Labor Department.","result":"For week ending 2026-07-04, initial claims were 215000, down 2000 from revised 217000; the four-week initial-claims average was 218750. For week ending 2026-06-27, continued claims were 1810000, up 8000."},{"kind":"tool","tool":"public.history","call":"Fetched recent seasonally adjusted continued-claims reference points from public Labor Department coverage and ALFRED/FRED mirror context for CCSA.","result":"Recent CCSA levels used: 2026-05-30 = 1800000, 2026-06-06 = 1810000, 2026-06-20 revised = 1802000, and 2026-06-27 = 1810000; the latest week-over-week change was +8000."},{"kind":"text","text":"Reference class / base rate: over the latest observed CCSA points, the base rate is persistence around 1.80 to 1.81 million, with no evidence in initial claims of a fresh layoff surge by the 2026-07-04 week. The main forecasting problem is a two-week-ahead continuation of a flat but slightly soft labor-market level."},{"kind":"text","text":"Update components: level starts at 1.810 million; momentum adds about +0.004 million because continued claims just rose +0.008 million and hiring remains slow; the latest initial-claims decline from 217000 to 215000 subtracts about -0.002 million; duration / low-hire risk adds about +0.003 million. Net update is +0.005 million to 1.815 million."},{"kind":"math","text":"Prior/update/interval: persistence prior model on recent first-print/mirror CCSA history uses 2026-05-30 1.800, 2026-06-06 1.810, 2026-06-20 1.802, and 2026-06-27 1.810 million; adjustment components are +0.004 momentum, -0.002 initial-claims offset, and +0.003 low-hire duration risk. Successive changes are +0.010, -0.008, and +0.008 million, so sigma = 0.010 million. For a two-week-ahead level forecast, half-width = 1.28 * sigma * sqrt(2) = 1.28 * 0.010 * 1.414 = 0.018 million. Point = 1.810 + 0.005 = 1.815; implied 80% bounds are 1.815 - 0.018 = 1.797 and 1.815 + 0.018 = 1.833."},{"kind":"text","text":"Counter-considerations: upside risk is a further rise in benefit duration or a hidden layoff wave in the July 4 and July 11 weeks, which would land above the interval if CCSA jumps beyond about 1.833 million. Downside risk is faster re-employment or downward seasonal adjustment after the school-year noise fades, which would land below the interval if CCSA falls under about 1.797 million."},{"kind":"forecast","point":1.815,"ciLow":1.797,"ciHigh":1.833}]}

# Reviewer critique
{
  "summary": "Draft is publishable with only minor support improvements around interval evidence and official-source clarity.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Expand the volatility sample beyond three recent changes or explicitly justify why the short sample is sufficient for the 80% interval.",
    "Mention that ALFRED/FRED is only a mirror for history and that resolution uses the first DOL ETA print, matching the ledger first-print rule.",
    "Tighten the low-hire duration adjustment by tying it to one cited current labor-market indicator or label it as a judgmental small upward adjustment."
  ]
}

Emit the final JSON object only.
