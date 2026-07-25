# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.new_residential_sales.new_single_family_houses_sold_saar
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-new-home-sales-saar-july-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "census.new_residential_sales.new_single_family_houses_sold_saar.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.census.gov"], "expectedReleaseWindow": {"end": "2026-08-28", "start": "2026-08-20"}, "field": "HSN1F", "releasePolicy": "first_print", "sourceSeriesId": "HSN1F", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=HSN1F", "table": "New Residential Sales, Table 1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-0f2d2e4dcfee851ef8eef4f673d139bc9935d1db55456076f8a6694d439db399.json"
- targetContentHash: "0f2d2e4dcfee851ef8eef4f673d139bc9935d1db55456076f8a6694d439db399"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.
- For ACS table targets, fetch each history year's values from the keyless JSON endpoint https://data.census.gov/api/access/data/table?id=<PRODUCT><YEAR>.<TABLE>&g=010XX00US (for example ACSDT1Y2024.B28005) and read the cited variable columns from the returned JSON.
- api.census.gov requires an API key (keyless requests redirect to missing_key.html); never rely on it in keyless runs, and never present remembered values as fetched ones.
- ACS vintage discipline: never mix 5-year estimates into a 1-year series — 5-year values lag the 1-year series by roughly two years; the product id in the fetch URL (ACSDT1Y vs ACSDT5Y) is the vintage authority.

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

Emit the final JSON object only. (agent thesis.analyst v2.3.0, prompt 7ef119647b35, tools 5d0da8127872, promptMode fast)


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
{"slug":"us-new-home-sales-saar-july-2026","country":"US","type":"data","title":"US New Home Sales SAAR, July 2026","question":"What will the U.S. Census Bureau and HUD first report for sales of new single-family houses in July 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":620,"ciLow":538,"ciHigh":702,"confidence":0.8,"resolutionDate":"2026-08-25","resolutionSource":"U.S. Census Bureau and HUD New Residential Sales, Table 1, first print archived for HSN1F","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=HSN1F","resolutionRule":"Resolve to the first published July 2026 value for New Houses Sold, United States, seasonally adjusted annual rate, Table 1a/New Residential Sales series HSN1F, in thousands. Use the first official print only; ignore later revisions and seasonal-revision changes unless the original release is formally withdrawn before publication.","dataPointId":"census.new_residential_sales.new_single_family_houses_sold_saar.2026_07.first_print","historicalContext":[{"label":"2026-06 latest preliminary SAAR","value":628},{"label":"2026-05 revised SAAR","value":618},{"label":"2026-04 revised SAAR","value":646},{"label":"2026-03 revised SAAR","value":659},{"label":"2025-07 SAAR","value":648}],"drivers":["June sales rebounded modestly from revised May but stayed below June 2025","High months' supply and elevated for-sale inventory lean against a large upside move","Single-family permits softened in June, pointing to cautious builder conditions","Large month-to-month noise in new-home sales keeps the interval wide"],"sourceContext":["https://www.census.gov/construction/soc/schedule.html","https://www.census.gov/construction/nrs/current/index.html","https://www.census.gov/construction/nrs/pdf/newressales.pdf","https://www.census.gov/construction/nrc/current/index.html"],"runAt":"2026-07-25T16:04:22Z","reasoning":[{"kind":"heading","text":"US July 2026 New Single-Family Home Sales SAAR"},{"kind":"text","text":"Framing and exact resolver: the target is Census/HUD New Residential Sales Table 1a, United States new single-family houses sold, seasonally adjusted annual rate, in thousands, first print for July 2026. The Census release schedule verifies the July 2026 New Residential Sales release for August 25, 2026 at 10:00 AM; the June release also says the July report is scheduled for August 25, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read Census New Residential Sales current release for latest headline and revision context.","result":"Fetched New Residential Sales June 2026: sales 628,000 SAAR; May 2026 rate 618,000; June 2025 rate 665,000; for-sale inventory 485,000; months' supply 9.3."},{"kind":"tool","tool":"official.lookup","call":"Read Census New Residential Sales PDF Table 1a for recent seasonally adjusted history in the same variant.","result":"Fetched Table 1a United States SAAR values, thousands: 2025-06 665, 2025-07 648, 2025-08 698, 2025-09 714, 2025-10 652, 2025-11 757, 2025-12 723, 2026-01 576, 2026-02 630, 2026-03 659, 2026-04 646, 2026-05 618, 2026-06 628."},{"kind":"tool","tool":"official.lookup","call":"Read Census New Residential Construction current release for leading construction indicators.","result":"Fetched June 2026 construction indicators: total permits 1,367,000 SAAR, revised May permits 1,410,000, single-family authorizations 871,000, revised May single-family authorizations 892,000, single-family starts 895,000."},{"kind":"text","text":"Base rate/reference class: recent same-variant monthly SAAR changes are very noisy. A persistence prior from the latest 628 thousand is the natural base rate, with recent changes of -17, +50, +16, -62, +105, -34, -147, +54, +29, -13, -28, and +10 thousand across the fetched 2025-06 to 2026-06 sequence."},{"kind":"text","text":"Level and momentum: the latest print improved only 10 thousand from May and remained 37 thousand below June 2025. The May-to-June rebound argues against extrapolating the May weakness, but the year-over-year decline and high 9.3 months' supply argue against a strong July acceleration."},{"kind":"text","text":"Mechanism adjustment: June single-family permits fell to 871 thousand from 892 thousand, and total permits fell to 1,367 thousand from 1,410 thousand. That does not mechanically determine sales, but it supports a small downward adjustment from pure 628 persistence rather than an upward continuation."},{"kind":"math","text":"Prior/update/interval: persistence prior = 628. Adjustment components: -5 for soft single-family permits, -3 for elevated 9.3 months' supply and below-year-ago sales, giving point = 628 - 8 = 620. Historical sample = same-variant monthly SAAR changes from 2025-06 through 2026-06. The sample standard deviation of successive changes is sigma = 64.25 thousand. 80% half-width = 1.28*sigma = 1.28*64.25 = 82.24 thousand, rounded to 82. Interval = 620 - 82 to 620 + 82 = 538 to 702."},{"kind":"text","text":"Counter-consideration: upside risk is a July demand rebound from rate relief or builder incentives that would land above the interval, especially if the South recovers from June weakness. Downside risk is a renewed sales drop from high mortgage rates, cancellations, or excess inventory that would land below the interval. Values outside the interval are plausible because this series has large sampling and month-to-month volatility."},{"kind":"forecast","point":620,"ciLow":538,"ciHigh":702}]}

# Reviewer critique
{"summary":"The draft is publishable: resolver, prior/update logic, volatility-based interval, tail scenarios, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Name the numeric tail thresholds explicitly, e.g. upside above 702 and downside below 538.","Consider adding the official Census schedule URL directly to the resolver/source text alongside the ALFRED first-print archive."]}

Emit the final JSON object only.
