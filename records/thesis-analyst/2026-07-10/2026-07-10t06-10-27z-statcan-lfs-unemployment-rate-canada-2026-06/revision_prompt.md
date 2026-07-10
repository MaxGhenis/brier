# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statcan.lfs.unemployment_rate.canada
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "statcan-lfs-unemployment-rate-canada-june-2026"
- country: "CA"
- targetUnit: "percent"
- dataPointId: "statcan.lfs.unemployment_rate.canada.june_2026.first_print"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-07-09", "start": "2026-07-01"}, "field": "official_release:statcan:dq260605a:unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "statcan.lfs.unemployment_rate", "sourceUrl": "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm", "table": "Labour Force Survey, May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-1dc4bca9a92ad6b923c9155ad1d3fa905989007a4818cd6a1316820bf70ea0a8.json"
- targetContentHash: "1dc4bca9a92ad6b923c9155ad1d3fa905989007a4818cd6a1316820bf70ea0a8"
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
{"slug":"statcan-lfs-unemployment-rate-canada-june-2026","country":"CA","type":"data","title":"Canada unemployment rate, June 2026","question":"Statistics Canada Labour Force Survey unemployment rate for Canada, June 2026, seasonally adjusted, first print","unit":"percent","pointEstimate":6.7,"ciLow":6.3,"ciHigh":7,"confidence":0.8,"resolutionDate":"2026-07-09","resolutionSource":"Statistics Canada The Daily, Labour Force Survey first print","resolutionSourceUrl":"https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","resolutionRule":"Resolve to the first-print Statistics Canada Labour Force Survey unemployment rate for Canada, seasonally adjusted, in percent and rounded to one decimal place, from The Daily release/table 14-10-0287-01. Do not use later revisions. Ledger discrepancy noted: the target contract gives 2026-07-09 and dq260605a, while the official 2026-2027 release-date PDF lists Labour Force Survey June 2026 for July 10, 2026 and dq260605a is the May 2026 release.","dataPointId":"statcan.lfs.unemployment_rate.canada.june_2026.first_print","historicalContext":[{"label":"May 2026 unemployment rate, Canada SA","value":6.6},{"label":"April 2026 unemployment rate, Canada SA","value":6.9},{"label":"March 2026 unemployment rate, Canada SA","value":6.7},{"label":"February 2026 unemployment rate, Canada SA","value":6.7},{"label":"January 2026 unemployment rate, Canada SA","value":6.5},{"label":"December 2025 unemployment rate, Canada SA","value":6.8}],"drivers":["May unemployment fell to 6.6 after April's 6.9, so persistence starts near 6.6","Recent monthly changes are noisy but centered near zero over Dec-May","May employment gain of 88,000 lowers near-term upside pressure on unemployment","Spring 2024 onward unemployment remains above the 2017-2019 average of 6.0, consistent with soft hiring","Tariff-related uncertainty and weak job-finding keep upside risk to unemployment alive"],"sourceContext":["https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260508/dq260508a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260410/dq260410a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260313/dq260313a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260206/dq260206a-eng.htm","https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701"],"runAt":"2026-07-10T06:10:42Z","reasoning":[{"kind":"heading","text":"Canada LFS unemployment-rate forecast for June 2026"},{"kind":"text","text":"Framing and exact resolver: forecast the Statistics Canada Labour Force Survey unemployment rate for Canada, seasonally adjusted, first print, percent rounded to one decimal. Table 14-10-0287-01 is the release table used by The Daily. I keep the ledger top-level resolutionSourceUrl and resolutionDate as supplied, but the official schedule and the dq260605a page show a concrete discrepancy: dq260605a is Labour Force Survey, May 2026, released 2026-06-05, while the official release schedule lists Labour Force Survey, June 2026, for 2026-07-10."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada 2026-2027 major economic releases PDF and read the Labour Force Survey schedule.","result":"Fetched official schedule numbers: Labour Force Survey release dates/reference periods include 2026-06-05 for May 2026, 2026-07-10 for June 2026, 2026-08-07 for July 2026, 2026-09-04 for August 2026, and 2026-10-09 for September 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily Labour Force Survey, May 2026, dq260605a.","result":"Fetched latest official LFS numbers: Canada unemployment rate 6.6% in May 2026, monthly change -0.3 percentage points; employment 21,122,000 in May 2026, monthly change +0.4%; employment increased by 88,000 in May; job-finding rate 26.3%; layoff rate 0.6%; 2017-2019 unemployment-rate average cited as 6.0%."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily Labour Force Survey, April 2026, dq260508a.","result":"Fetched April official LFS numbers: Canada unemployment rate 6.9% in April 2026, monthly change +0.2 percentage points; employment 21,034,000, monthly change -0.1%; labour force participation rate 65.0%; long-term unemployment share 22.5%; layoff rate 0.6%."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily Labour Force Survey, March and February 2026 releases.","result":"Fetched earlier official LFS numbers: March 2026 Canada unemployment rate 6.7%, monthly change 0.0 points, employment 21,051,000; February 2026 Canada unemployment rate 6.7%, monthly change +0.2 points, employment 21,037,000."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily Labour Force Survey, January 2026 and December 2025 releases.","result":"Fetched earlier official LFS numbers: January 2026 Canada unemployment rate 6.5%, monthly change -0.3 points, employment 21,121,000; December 2025 Canada unemployment rate 6.8%, monthly change +0.3 points, employment 21,144,000."},{"kind":"text","text":"Base rate/reference class: for this same seasonally adjusted Canada LFS unemployment-rate variant, the recent first-print reference class is Dec 2025-May 2026 values of 6.8, 6.5, 6.7, 6.7, 6.9, and 6.6. The level base rate is persistence near the latest 6.6 rather than the older 2017-2019 average of 6.0, because StatCan says unemployment has remained above that pre-pandemic average since spring 2024."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 first-print unemployment rate 6.6. Historical sample = successive monthly changes from Dec 2025 to May 2026: -0.3, +0.2, 0.0, +0.2, -0.3 percentage points. sigma = 0.25 using sample standard deviation of those changes. 80% normal half-width = 1.28*sigma = 1.28*0.25 = 0.32 percentage points. Adjustment components: level +0.00 from persistence, momentum +0.05 because the May drop partly reversed April's jump, one-off -0.05 because May employment rose 88,000 and job-finding improved, policy/mechanism +0.05 for still-soft hiring and tariff uncertainty. Combined mean = 6.6 + 0.05 = 6.65, rounded first-print point = 6.7; 6.65 +/- 0.32 gives 6.33 to 6.97, rounded interval = 6.3 to 7.0."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed participation rise or tariff-linked hiring freeze that pushes unemployment back to April's 6.9 or above; downside risk is another broad May-like employment gain, especially in Ontario, British Columbia, construction, or services, that pulls the rate toward 6.3. A June print at or below 6.2 or at or above 7.1 would land outside the interval."},{"kind":"forecast","point":6.7,"ciLow":6.3,"ciHigh":7}]}

# Reviewer critique
{
  "summary": "Draft is methodologically coherent, but publication should be blocked until the target ledger resolver/date/source mismatch for June 2026 is handled explicitly at the target level.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The canonical resolver URL/table points to dq260605a and 'Labour Force Survey, May 2026' while the target is June 2026; the draft notes this, but the published target would still resolve against the wrong first-print page.",
      "actionRequested": "Keep this forecast tied to the same dataPointId, but register or document a target correction path before publication: June 2026 LFS should resolve to the official June 2026 first-print release, with the ledger discrepancy preserved in reasoning."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft keeps resolutionDate as 2026-07-09 even while its own cited official schedule says the June 2026 LFS release date is 2026-07-10.",
      "actionRequested": "Clarify in the forecast metadata or publication notes that 2026-07-09 is a ledger-supplied field and that the official schedule discrepancy is known, rather than presenting 2026-07-09 as the verified release date."
    },
    {
      "rubricItem": "leakage",
      "severity": "warning",
      "summary": "runAt is 2026-07-10T06:10:42Z, which is after the ledger resolutionDate of 2026-07-09, even though it appears before the official July 10 LFS release time.",
      "actionRequested": "Add a short no-leakage note that the run used only information available before the official June 2026 release and did not use the June outcome."
    }
  ],
  "optionalSuggestions": [
    "The prior/update/interval step is strong; keep the sigma sample and rounded implied bounds.",
    "Consider naming the normal interval assumption as approximate because the historical sample is only five monthly changes.",
    "Tail scenarios are concrete, but could be slightly more target-specific by tying participation and employment shocks directly to unemployment-rate arithmetic."
  ]
}

Emit the final JSON object only.
