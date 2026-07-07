# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.housing_starts.saar
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "census-housing-starts-saar-june-2026"
- targetUnit: "millions"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"census-housing-starts-saar-june-2026","country":"US","type":"data","title":"US housing starts SAAR, June 2026","question":"What will the U.S. Census Bureau and HUD first report for privately owned housing starts, seasonally adjusted annual rate, United States total, June 2026?","unit":"millions","pointEstimate":1.237,"ciLow":1.092,"ciHigh":1.382,"confidence":0.8,"resolutionDate":"2026-07-17","resolutionSource":"U.S. Census Bureau and HUD Monthly New Residential Construction release","resolutionSourceUrl":"https://www.census.gov/construction/nrc/pdf/newresconst.pdf","resolutionRule":"Resolve to the first Census/HUD Monthly New Residential Construction print for June 2026, Table 3a, New Privately-Owned Housing Units Started, United States total, seasonally adjusted annual rate. Use the preliminary first-print value in thousands divided by 1,000 to convert to millions; ignore subsequent revisions or historical-table backfills.","dataPointId":"census.housing_starts.saar.2026-06.first_print","historicalContext":[{"label":"May 2026 housing starts SAAR","value":1.177},{"label":"April 2026 housing starts SAAR","value":1.392},{"label":"March 2026 housing starts SAAR","value":1.522},{"label":"May 2026 building permits SAAR","value":1.413},{"label":"May 2025 housing starts SAAR","value":1.289}],"drivers":["May 2026 total starts fell to 1.177 million SAAR, mainly from multifamily weakness","Single-family starts and permits were comparatively stable near 0.88 million SAAR","Multifamily starts are volatile and likely to partially mean-revert after May's drop","May permits at 1.413 million SAAR provide a higher near-term construction pipeline than May starts","High mortgage rates and weak builder sentiment cap the rebound"],"sourceContext":["https://www.census.gov/construction/nrc/current/index.html","https://www.census.gov/construction/nrc/pdf/newresconst.pdf","https://www.census.gov/construction/nrc/data/series.html","https://www.census.gov/construction/soc/schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html"],"runAt":"2026-07-07T22:13:30Z","reasoning":[{"kind":"heading","text":"June 2026 U.S. housing starts SAAR forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast targets the Census/HUD New Residential Construction first print for privately owned housing units started, United States total, seasonally adjusted annual rate, June 2026. The table variant is Table 3a, seasonally adjusted annual rate, not not-seasonally-adjusted starts and not permits or completions."},{"kind":"tool","tool":"official.lookup","call":"Open Census Economic Indicator Release Schedule and Survey of Construction release schedule for June 2026 New Residential Construction.","result":"The Census schedule lists New Residential Construction for June 2026 at 8:30 AM on July 17, 2026; the SOC schedule also lists June 2026 New Residential Construction on July 17, 2026 and New Residential Sales on July 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Open the Census/HUD May 2026 New Residential Construction press release page.","result":"For May 2026, housing starts were 1,177,000 SAAR, down 15.4% from revised April 2026 at 1,392,000 and down 8.7% from May 2025 at 1,289,000; May building permits were 1,413,000 SAAR and single-family permits were 886,000."},{"kind":"tool","tool":"official.lookup","call":"Open the Census/HUD current press release PDF, Table 3a, housing units started, seasonally adjusted annual rate.","result":"Recent United States total starts in thousands SAAR were May 2025 1,289, June 2025 1,379, July 2025 1,432, August 2025 1,291, September 2025 1,319, October 2025 1,273, November 2025 1,319, December 2025 1,378, January 2026 1,385, February 2026 1,346, March 2026 1,522, April 2026 1,392, and May 2026 1,177."},{"kind":"tool","tool":"official.lookup","call":"Read component detail from the May 2026 Census/HUD release for starts and permits.","result":"May 2026 single-family starts were 882,000 SAAR versus revised April 2026 at 899,000; May 2026 starts in buildings with 5 units or more were 284,000; May 2026 authorizations in buildings with 5 units or more were 474,000."},{"kind":"text","text":"Reference class and base rate: over the latest official 13-month starts sequence, the level has mostly run between 1.27 million and 1.43 million SAAR before the May 2026 drop to 1.177 million. A persistence base rate from the latest print would be 1.177 million, but the component mix suggests May was unusually weak in multifamily rather than a broad collapse."},{"kind":"text","text":"Level, momentum, and mechanisms: single-family starts were only 17,000 below April and single-family permits were 886,000, so I keep that component near 0.88 million. Multifamily starts at 0.284 million were far below recent starts and below May 5-plus-unit permits at 0.474 million, so I add a partial rebound of about 0.060 million rather than a full snapback."},{"kind":"math","text":"Prior/update/interval: persistence prior is May 2026 starts at 1.177 million SAAR using the official Table 3a reference class from May 2025 through May 2026; adjustments are +0.000 million for single-family level, +0.060 million for partial multifamily mean reversion, and +0.000 million for policy/timing effects, giving 1.177 + 0.060 = 1.237. Successive monthly changes in millions are +0.090, +0.053, -0.141, +0.028, -0.046, +0.046, +0.059, +0.007, -0.039, +0.176, -0.130, -0.215, so sigma = 0.113; 1.28*sigma = 0.145, giving 1.237 - 0.145 = 1.092 and 1.237 + 0.145 = 1.382."},{"kind":"text","text":"Counter-considerations: upside risk is a faster multifamily rebound toward the 0.40-0.48 million area implied by recent starts and permits, which would land above the interval if single-family also improves. Downside risk is that high mortgage rates and builder caution keep starts near May's depressed multifamily level, which would land below the interval if single-family starts also break below 0.85 million."},{"kind":"forecast","point":1.237,"ciLow":1.092,"ciHigh":1.382}]}

# Reviewer critique
{"summary":"Draft is publication-ready with no blocking issues; resolver, prior, update logic, interval, tails, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["State explicitly that the 80% interval uses approximately a normal 80% half-width, 1.28 times recent monthly-change sigma, to make the confidence mapping self-contained.","Consider naming whether the 13-month sample is first-print or current-vintage Table 3a history; this is not fatal because the resolver itself is clearly first-print June 2026."]}

Emit the final JSON object only.
