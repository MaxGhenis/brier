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
- country: "CA"
- targetUnit: "thousands"
- dataPointId: "statcan.lfs.employment_change.canada.june_2026.first_print"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-07-09", "start": "2026-07-01"}, "field": "official_release:statcan:dq260605a:employment_change", "releasePolicy": "first_print", "sourceSeriesId": "statcan.lfs.employment_change", "sourceUrl": "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm", "table": "Labour Force Survey, May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-bda39d092a2948ed23e301f6ef88f11a000cdcd01f6236e5fc50227ed5dcb5f1.json"
- targetContentHash: "bda39d092a2948ed23e301f6ef88f11a000cdcd01f6236e5fc50227ed5dcb5f1"
- registeredAtUtc: "2026-07-10T05:58:27Z"

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
{"slug":"statcan-lfs-employment-change-canada-june-2026","country":"CA","type":"data","title":"Canada LFS Employment Change, June 2026","question":"Statistics Canada Labour Force Survey employment change, Canada, June 2026, seasonally adjusted, first print","unit":"thousands","pointEstimate":18,"ciLow":-54,"ciHigh":90,"confidence":0.8,"resolutionDate":"2026-07-10","resolutionSource":"Statistics Canada The Daily, Labour Force Survey first-print release","resolutionSourceUrl":"https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","resolutionRule":"Resolve to the first Statistics Canada Labour Force Survey print for seasonally adjusted Canada employment monthly change for the June 2026 reference period, in thousands of persons, as published in The Daily/Table 14-10-0287-01. Use the initially released value only; ignore later revisions. Note: the ledger-provided URL points to the May 2026 LFS release dated 2026-06-05, while the official release schedule verifies the June 2026 LFS release date as 2026-07-10.","dataPointId":"statcan.lfs.employment_change.canada.june_2026.first_print","historicalContext":[{"label":"May 2026 employment change","value":88},{"label":"April 2026 employment change","value":-18},{"label":"March 2026 employment change","value":14},{"label":"February 2026 employment change","value":-84},{"label":"January 2026 employment change","value":-25}],"drivers":["recent May rebound after weak early-2026 employment","unemployment rate still elevated at 6.6% in May","job-finding below pre-pandemic average","retail/manufacturing softness and tariff uncertainty","possible temporary services demand during June events"],"sourceContext":["https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260508/dq260508a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260410/dq260410a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260313/dq260313a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260206/dq260206a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260109/dq260109a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/251205/dq251205a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/251107/dq251107a-eng.htm","https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701"],"runAt":"2026-07-10T06:09:14Z","reasoning":[{"kind":"heading","text":"Canada LFS employment change forecast for June 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the first-print, seasonally adjusted Canada employment monthly change from Statistics Canada's Labour Force Survey, in thousands. Table 14-10-0287-01 is the same variant used for the anchors. The provided ledger URL is a concrete mismatch because it points to the May 2026 release dated 2026-06-05, but I keep the forecast tied to the registered target and state that discrepancy rather than changing the target URL."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada 2026-2027 major economic release dates PDF, Labour Force Survey rows","result":"Fetched release calendar: Labour Force Survey release date for reference period June 2026 is July 10, 2026; May 2026 was June 5, 2026; July 2026 is August 7, 2026."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada The Daily Labour Force Survey May 2026 release","result":"Fetched latest pre-target LFS numbers: employment increased by 88,000 (+0.4%) in May 2026; employment level was 21,122,000; unemployment rate was 6.6%; January-April 2026 net employment decline was 112,000."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada The Daily Labour Force Survey April and March 2026 releases","result":"Fetched prior monthly changes: April 2026 employment was little changed at -18,000 (-0.1%) with unemployment 6.9%; March 2026 employment was +14,000 (+0.1%) with unemployment 6.7%."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada The Daily Labour Force Survey February and January 2026 releases","result":"Fetched early-2026 weakness: February 2026 employment declined by 84,000 (-0.4%) and January 2026 employment edged down by 25,000 (-0.1%); February unemployment was 6.7% and January unemployment was 6.5%."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada The Daily Labour Force Survey October-December 2025 releases","result":"Fetched reference-class sequence: October 2025 employment +67,000; November 2025 +54,000; December 2025 +8,200; the September-November 2025 cumulative increase was 181,000."},{"kind":"text","text":"Base rate/reference class: using recent first-print monthly LFS employment changes for the same seasonally adjusted Canada series gives Oct 2025 through May 2026 values of +67, +54, +8.2, -25, -84, +14, -18, and +88 thousand. The simple mean is about +13 thousand, a reasonable outside-view prior for a noisy monthly employment-change target."},{"kind":"text","text":"Current-release update: May's +88,000 rebound and lower 6.6% unemployment argue against extrapolating the February-April weakness directly. But the May report also said the job-finding rate remained below its 2017-2019 average and that wholesale/retail and manufacturing had soft spots, so I only move modestly above the +13 thousand base rate."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate model on recent same-variant first prints (+67, +54, +8.2, -25, -84, +14, -18, +88) gives mean = 104.2/8 = 13.0 thousand; adjustment components are +8 for May momentum and services/event demand, -3 for elevated unemployment and weak job-finding, giving point = 18 thousand. For a change/flow series, sigma is computed from the values themselves: sigma = 56.1 thousand using the sample standard deviation; 80% half-width is roughly 1.28*sigma = 1.28*56.1 = 71.8 thousand, rounded to 72. Final interval is 18 - 72 = -54 and 18 + 72 = 90 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger services and youth hiring month, possibly helped by June travel/event activity, which would land above the interval if gains exceed about +90,000. Downside risk is renewed private-sector weakness, tariff-sensitive manufacturing cuts, or reversal after May's full-time surge, which would land below the interval if losses exceed about -54,000."},{"kind":"forecast","point":18,"ciLow":-54,"ciHigh":90}]}

# Reviewer critique
{"summary":"Publishable with no blocking fixes; the draft clearly identifies the ledger URL mismatch while keeping the registered target fields and has a coherent prior, update, interval, tails, and JSON forecast.","requiredFixes":[],"optionalSuggestions":["Make the release-time/no-leakage boundary explicit because the run occurred on 2026-07-10 before the scheduled first print.","The services/event-demand upside driver is plausible but lightly supported; either cite a concrete June hiring/event indicator or keep it as a small qualitative adjustment only."]}

Emit the final JSON object only.
