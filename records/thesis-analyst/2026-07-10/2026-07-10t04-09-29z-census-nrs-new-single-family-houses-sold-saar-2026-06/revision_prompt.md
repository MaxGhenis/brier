# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.nrs.new_single_family_houses_sold_saar
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-new-home-sales-saar-june-2026"
- targetUnit: "thousands"
- dataPointId: "census.nrs.new_single_family_houses_sold_saar.2026_06.first_print"
- resolutionSourceUrl: "https://www.census.gov/construction/nrs/current/index.html"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.census.gov"], "expectedReleaseWindow": {"end": "2026-07-24", "start": "2026-07-24"}, "field": "Sales of new single-family houses; United States; seasonally adjusted annual rate", "releasePolicy": "first_print", "sourceSeriesId": "NRS new single-family houses sold United States seasonally adjusted annual rate", "sourceUrl": "https://www.census.gov/construction/nrs/current/index.html", "table": "Monthly New Residential Sales, Table 1. New Houses Sold and For Sale", "transform": {"factor": 1, "operation": "identity"}}

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
{"slug":"us-new-home-sales-saar-june-2026","country":"US","type":"data","title":"US New Home Sales SAAR, June 2026","question":"What will the U.S. Census Bureau/HUD first-print estimate be for sales of new single-family houses in the United States in June 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":603,"ciLow":517,"ciHigh":689,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"U.S. Census Bureau and HUD Monthly New Residential Sales release, Table 1a","resolutionSourceUrl":"https://www.census.gov/construction/nrs/current/index.html","resolutionRule":"Resolve to the first-print United States value for Sales of new single-family houses, seasonally adjusted annual rate, in Monthly New Residential Sales Table 1a for June 2026, rounded as Census reports it in thousands of units. Use the July 24, 2026 first release only; ignore later revisions or historical-table updates.","dataPointId":"census.nrs.new_single_family_houses_sold_saar.2026_06.first_print","historicalContext":[{"label":"2026-05 latest first print SAAR","value":580},{"label":"2026-04 revised SAAR in May release","value":626},{"label":"2026-03 revised SAAR in May release","value":664},{"label":"2025-06 revised SAAR in May release","value":665},{"label":"2026 year-to-date NSA sales through May","value":275}],"drivers":["May 2026 new-home sales fell to 580 thousand SAAR from 626 thousand in April","High 10.3 months' supply points to weak builder absorption","2026 year-to-date not seasonally adjusted sales were 275 thousand, 7.0 percent below 2025","Single-family starts and permits were roughly stable in May, limiting downside from construction flow","Large monthly sampling and revision noise supports a wide interval"],"sourceContext":["https://www.census.gov/construction/nrs/current/index.html","https://www.census.gov/construction/nrs/pdf/newressales.pdf","https://www.census.gov/construction/soc/schedule.html","https://www.census.gov/construction/nrc/current/index.html"],"runAt":"2026-07-10T04:09:45Z","reasoning":[{"kind":"heading","text":"June 2026 US New Home Sales SAAR Forecast"},{"kind":"text","text":"Framing and exact resolver: this forecasts the Census/HUD Monthly New Residential Sales first print for June 2026, Table 1a seasonally adjusted annual rate, United States sales of new single-family houses, in thousands. This uses the same SAAR variant for every anchor and historical value."},{"kind":"tool","tool":"official.lookup","call":"Opened Census New Residential Sales current release page for May 2026.","result":"Fetched May 2026 new single-family houses sold at 580,000 SAAR, April 2026 at 626,000 SAAR, May 2025 at 622,000 SAAR, inventory at 496,000, and months' supply at 10.3."},{"kind":"tool","tool":"official.lookup","call":"Opened Census/HUD May 2026 New Residential Sales PDF, Table 1a.","result":"Fetched Table 1a SAAR United States sales history: 2025 May 622, June 665, July 648, August 698, September 714, October 652, November 757, December 723; 2026 January 576, February 630, March 664, April 626, May 580, all in thousands."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Survey of Construction release schedule.","result":"Fetched official schedule showing June 2026 survey month: New Residential Construction release July 17, 2026 and New Residential Sales release July 24, 2026 at 10:00 a.m."},{"kind":"tool","tool":"official.lookup","call":"Opened Census New Residential Construction May 2026 release for related builder-flow indicators.","result":"Fetched May 2026 building permits at 1,413,000 SAAR, total housing starts at 1,177,000 SAAR, single-family starts at 882,000 SAAR, and single-family permits at 886,000 SAAR."},{"kind":"text","text":"Base rate/reference class: recent same-series SAAR levels from May 2025 through May 2026 averaged about 659 thousand before the latest drop, while the first five months of 2026 averaged 615 thousand. The latest 580 thousand print is below both, so persistence alone looks too low but the elevated 10.3 months' supply argues against full reversion toward the 2025 average."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest same-variant SAAR of 580. Historical sample is the 13 fetched monthly Table 1a SAAR values from 2025-05 through 2026-05. Adjustment components: +25 for partial rebound after a 46 thousand May decline and mean reversion toward the 2026 year-to-date SAAR average near 615, +8 for June 2025 being 43 above May 2025 in the same series, -10 for high 10.3 months' supply and weak year-to-date NSA sales, giving 580 + 25 + 8 - 10 = 603. Successive changes are +43, -17, +50, +16, -62, +105, -34, -147, +54, +34, -38, -46; sample sigma = 67.4 thousand, so 80% half-width is roughly 1.28*sigma = 86.3 thousand. Rounded interval: 603 - 86 = 517 and 603 + 86 = 689."},{"kind":"text","text":"Counter-consideration: upside risk is a builder-incentive rebound like February-March 2026 or November 2025, which would land above the interval if June prints above 689 thousand. Downside risk is another demand shock from mortgage-rate pressure or cancellations, which would land below the interval if sales fall below 517 thousand."},{"kind":"forecast","point":603,"ciLow":517,"ciHigh":689}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, but the resolver/table naming should be aligned with the canonical ledger and the model-prior treatment should be explicit.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"Draft uses \"Table 1a\" in resolutionSource and resolutionRule, while the canonical ledger binds the target to \"Monthly New Residential Sales, Table 1. New Houses Sold and For Sale\" and the specified field.","actionRequested":"Align resolver text to the ledger table/field wording, or explicitly state that the Census PDF label differs while preserving the ledger-bound target and first-print June 2026 SAAR United States field."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses persistence and recent monthly changes but does not explicitly say whether a formal time-series/model prior was used or ruled out.","actionRequested":"Add one sentence in the prior/update section stating that no separate statistical time-series model was fit, and that the model prior is latest-value persistence plus realized month-to-month volatility from the cited sample."}],"optionalSuggestions":["Clarify whether the 2025-05 through 2026-05 values are first-print, revised as of the May release, or mixed, since the target itself is first-print.","In the tail scenarios, name approximate numeric thresholds already implied by the interval, such as upside above 689 and downside below 517."]}

Emit the final JSON object only.
