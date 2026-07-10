# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statcan.lfs.employment_change.canada
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "statcan-lfs-employment-change-canada-june-2026"
- targetUnit: "thousands"
- dataPointId: "statcan.lfs.employment_change.canada.june_2026.first_print"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-07-09", "start": "2026-07-01"}, "field": "official_release:statcan:dq260605a:employment_change", "releasePolicy": "first_print", "sourceSeriesId": "statcan.lfs.employment_change", "sourceUrl": "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm", "table": "Labour Force Survey, May 2026", "transform": {"factor": 1, "operation": "identity"}}

# Source hints
- Use Statistics Canada The Daily and release schedule.
- Canada CPI annual rates print to one decimal.
- Resolution source should be the Statistics Canada release/table.

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
{"slug":"statcan-lfs-employment-change-canada-june-2026","country":"CA","type":"data","title":"Canada LFS Employment Change, June 2026","question":"What will Statistics Canada first print as the month-over-month change in seasonally adjusted Labour Force Survey employment for Canada in June 2026, in thousands?","unit":"thousands","pointEstimate":15,"ciLow":-62,"ciHigh":92,"confidence":0.8,"resolutionDate":"2026-07-10","resolutionSource":"Statistics Canada, The Daily - Labour Force Survey, June 2026","resolutionSourceUrl":"https://www150.statcan.gc.ca/n1/daily-quotidien/260710/dq260710a-eng.htm","resolutionRule":"Resolve to the first-print Statistics Canada The Daily Labour Force Survey, June 2026 headline or table value for seasonally adjusted employment change, Canada, excluding territories, measured as June 2026 employment minus May 2026 employment. Use the first official print only; do not incorporate later revisions or same-day corrections unless Statistics Canada replaces the first Daily page before public release. If the release reports persons, divide by 1,000 and report in thousands, preserving the sign.","dataPointId":"statcan.lfs.employment_change.canada.june_2026.first_print","historicalContext":[{"label":"2026-05 first print employment change","value":88},{"label":"2026-04 first print employment change","value":-18},{"label":"2026-03 first print employment change","value":14},{"label":"2026-02 first print employment change","value":-84},{"label":"2026-01 first print employment change","value":-25},{"label":"2025-12 first print employment change","value":8.2}],"drivers":["May rebound after weak January-April creates some mean-reversion risk","Unemployment rate remained elevated but improved to 6.6% in May","Layoff rate near pre-pandemic norms argues against a large negative shock","LFS monthly sampling volatility keeps the 80% interval wide","Wholesale and retail weakness offsets construction and services gains"],"sourceContext":["https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260508/dq260508a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260410/dq260410a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260313/dq260313a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260206/dq260206a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260109/dq260109a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/251205/dq251205a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/251107/dq251107a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/251010/dq251010a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/250905/dq250905a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/250808/dq250808a-eng.htm"],"runAt":"2026-07-10T04:03:21Z","reasoning":[{"kind":"heading","text":"Forecast for Canada LFS employment change, June 2026"},{"kind":"text","text":"Framing and exact resolver: this is the Statistics Canada Labour Force Survey seasonally adjusted employment change for Canada in June 2026, first print, in thousands. Statistics Canada identifies the LFS Canada employment series on The Daily pages as sourced from Table 14-10-0287-01. The supplied ledger URL points to the May 2026 page, 260605/dq260605a-eng.htm, even though the target dataPointId is June 2026; I keep the same target identity and note that the appropriate first-print resolver for June 2026 is the July 10, 2026 LFS Daily page."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada 2026-2027 major economic release dates PDF and checked the Labour Force Survey schedule.","result":"Fetched official schedule: Labour Force Survey release date July 10, 2026 for reference period June 2026; May 2026 was scheduled June 5, 2026 and July 2026 was scheduled August 7, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily, Labour Force Survey, May 2026.","result":"Fetched latest official LFS print before the target: employment increased by 88,000 (+0.4%) in May 2026, employment level was 21,122,000, unemployment rate was 6.6%, and the next release was stated as July 10, 2026 for June 2026 data."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily releases for January-April 2026.","result":"Fetched recent first-print employment changes: April 2026 -18,000, March 2026 +14,000, February 2026 -84,000, January 2026 -25,000; January-April net was -112,000 before the May +88,000 rebound."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily releases for July-December 2025.","result":"Fetched earlier first-print employment changes: December 2025 +8,200, November 2025 +54,000, October 2025 +67,000, September 2025 +60,000, August 2025 -66,000, July 2025 -41,000; July-August cumulative decline was -106,000 and September-November cumulative gain was +181,000."},{"kind":"text","text":"Reference class and base rate: for the same official variant, seasonally adjusted LFS employment change for Canada, the 12 fetched first-print changes from June 2025 through May 2026 were +83, -41, -66, +60, +67, +54, +8.2, -25, -84, +14, -18, and +88 thousand. That reference class has a mean of +11.7 thousand; recent five-month momentum through May is weaker at -4.8 thousand per month because the May rebound only partly reversed the January-April decline."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate model starts at the 12-month first-print mean of +11.7 thousand using the fetched historical sample [+83, -41, -66, +60, +67, +54, +8.2, -25, -84, +14, -18, +88]. Adjustment components: +8 thousand for May's broad-based rebound and improved job-finding, -6 thousand for likely give-back after an +88 thousand month, and +1 thousand for stable layoff conditions despite elevated unemployment, giving about +14.7 thousand, rounded to +15 thousand. For a change/flow series, sigma is computed from the values themselves: sigma = 59.8 thousand; 80% half-width = 1.28*sigma = 76.5 thousand, so +15 +/- 76.5 gives -61.5 to +91.5, rounded to [-62, 92]."},{"kind":"text","text":"Variant control: all anchors are the same LFS seasonally adjusted Canada employment-change variant used by Statistics Canada The Daily and Table 14-10-0287-01; I do not mix in payroll employment, unadjusted student measures, provincial subtotals, or later revised table vintages."},{"kind":"text","text":"Counter-considerations: upside risk would come from another broad services and construction gain plus continued Ontario and British Columbia strength, which would land above the interval if June prints above +92 thousand. Downside risk would come from a reversal of May's full-time jump, renewed wholesale and retail losses, or tariff-sensitive Ontario manufacturing weakness; that would land below the interval if June prints below -62 thousand. Outside the interval is most plausible if LFS sampling noise compounds a true sector shock."},{"kind":"forecast","point":15,"ciLow":-62,"ciHigh":92}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, with one blocking target-contract mismatch around resolver fields versus the canonical ledger.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft JSON sets resolutionDate to 2026-07-10 and resolutionSourceUrl to the June 2026 Daily page, while the canonical ledger contract supplied for this review gives resolutionSourceUrl as the 2026-06-05 May 2026 page and sourceBinding text/table for May 2026.","actionRequested":"Either align the JSON resolver fields to the canonical ledger exactly, or explicitly route this back as a ledger correction before publication; do not publish a cell whose resolver fields conflict with the catalog contract."}],"optionalSuggestions":["Add the implied 80% bounds directly in the final forecast prose as -62 to 92 thousand, not only in the math block and JSON.","Mention that the July 10, 2026 run time is before the official release time, if known, to make non-leakage clearer."]}

Emit the final JSON object only.
