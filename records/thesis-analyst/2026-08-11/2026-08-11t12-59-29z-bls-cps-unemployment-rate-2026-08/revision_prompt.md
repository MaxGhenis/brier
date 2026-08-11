# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.unemployment_rate
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "unemployment-rate-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.cps.unemployment_rate.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "bls.cps.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.unemployment_rate", "sourceUrl": "https://www.bls.gov/news.release/empsit.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Employment Situation (Current Population Survey)", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-ee40ca45dbbd92d41117ea4d5d678fe815ae3a21d5db698050b009e0f27fa0e4.json"
- targetContentHash: "ee40ca45dbbd92d41117ea4d5d678fe815ae3a21d5db698050b009e0f27fa0e4"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"

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
  "unit": "percent|count|thousands|millions|usd|usd_millions|usd_billions|gbp_billions|ratio|percent_growth",
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

Emit the final JSON object only. (agent thesis.analyst v2.5.7, prompt a954cfd8c691, tools 024388e49298, promptMode fast)


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
{"slug":"unemployment-rate-august-2026","country":"US","type":"data","title":"US unemployment rate, August 2026","question":"What will the BLS Current Population Survey U-3 unemployment rate, seasonally adjusted, be for August 2026 in the first Employment Situation print?","unit":"percent","pointEstimate":4.2,"ciLow":4,"ciHigh":4.3,"confidence":0.8,"resolutionDate":"2026-09-04","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.t01.htm","resolutionRule":"Resolve to the first-print BLS Employment Situation Table A-1 total unemployment rate, seasonally adjusted, for August 2026, reported in percent to one decimal place. Use the initial release value only; do not use later monthly revisions, annual population-control revisions, or corrected values unless the first posted release itself is replaced before ordinary public access.","dataPointId":"bls.cps.unemployment_rate.august_2026.first_print","historicalContext":[{"label":"July 2026","value":4.1},{"label":"June 2026","value":4.2},{"label":"May 2026","value":4.3},{"label":"April 2026","value":4.3},{"label":"March 2026","value":4.3}],"drivers":["July unemployment rate was 4.1 percent after a falling labor force participation rate","Recent CPS rate changes are small, with 2026 readings clustered between 4.1 and 4.4 percent","July payroll employment fell by 23,000, a soft-labor-market signal that offsets pure downward unemployment momentum","Initial claims remained low near 199,000 in the latest public report, limiting the case for a sharp August unemployment jump"],"sourceContext":["https://www.bls.gov/news.release/empsit.nr0.htm","https://www.bls.gov/news.release/empsit.t01.htm","https://www.bls.gov/charts/employment-situation/civilian-unemployment-rate.htm","https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1"],"runAt":"2026-08-11T12:59:56Z","reasoning":[{"kind":"heading","text":"US CPS unemployment rate forecast for August 2026"},{"kind":"text","text":"Resolver framing: this targets the BLS Current Population Survey total U-3 unemployment rate, seasonally adjusted, series LNS14000000 as displayed in Employment Situation Table A-1 for August 2026, first print only."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Employment Situation release schedule for the August 2026 reference month.","result":"BLS lists August 2026 Employment Situation release date Sep. 04, 2026 at 08:30 AM; the same schedule lists July 2026 on Aug. 07, 2026 and September 2026 on Oct. 02, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the current BLS Employment Situation Summary for July 2026.","result":"The July 2026 summary reports nonfarm payroll employment -23,000, unemployment rate 4.1 percent, unemployed people 6.9 million, labor force participation rate 61.4 percent, and prior May/June payroll revisions totaling -103,000."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Table A-1 for the seasonally adjusted total unemployment rate and labor-force details.","result":"Table A-1 reports total unemployment rate 4.3 in Mar. 2026, 4.3 in Apr. 2026, 4.3 in May 2026, 4.2 in June 2026, and 4.1 in July 2026; it also reports July 2026 labor force 169,094 thousand, employed 162,177 thousand, unemployed 6,916 thousand, and participation rate 61.4."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS civilian unemployment rate chart table for recent reference-class history.","result":"The BLS chart shows seasonally adjusted total unemployment rates of Jan. 2026 4.3, Feb. 2026 4.4, Mar. 2026 4.3, Apr. 2026 4.3, May 2026 4.3, June 2026 4.2, and July 2026 4.1; it also shows June 2025 4.1, July 2025 4.3, Aug. 2025 4.3, Sept. 2025 4.4, Nov. 2025 4.5, and Dec. 2025 4.4."},{"kind":"text","text":"Base rate/reference class: for a one-month-ahead level forecast of a rounded unemployment rate, the strongest base rate is persistence plus the empirical monthly-change distribution. Recent values have sat in a narrow 4.1 to 4.4 percent range in 2026, so large moves are possible but not the central case."},{"kind":"math","text":"Prior/update/interval: persistence prior is July 2026 unemployment rate 4.1. Historical sample is monthly changes from the BLS chart from Jan. 2024 through July 2026, skipping the missing Oct. 2025 observation; sigma = 0.11 percentage point from successive monthly changes. Update components: +0.06 for weak July payrolls and downward payroll revisions, +0.03 for the participation-rate decline being unlikely to keep lowering U-3 at the same pace, and -0.04 for still-low claims/no layoff surge context, giving an unrounded mean near 4.15. Interval method: 80 percent half-width is roughly 1.28*sigma = 1.28*0.11 = 0.14, so 4.15 +/- 0.14 gives about 4.01 to 4.29, rounded to the target display as 4.0 to 4.3 with point 4.2."},{"kind":"text","text":"Counter-considerations: upside risk is an August household-survey employment drop or rebound in participation that would push unemployment to 4.4 or higher, outside the interval. Downside risk is another participation decline or noisy drop in unemployed workers that would keep the rate at 3.9 or below, also outside the interval."},{"kind":"forecast","point":4.2,"ciLow":4,"ciHigh":4.3}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, but it has a target-contract source mismatch and one unsupported evidence driver that should be fixed before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The draft resolutionSourceUrl points to Table A-1 directly, while the ledger sourceBinding uses the Employment Situation summary URL https://www.bls.gov/news.release/empsit.nr0.htm with the generic-url adapter and resolver table text.","actionRequested":"Align the resolver/source fields with the ledger contract, or explicitly state why Table A-1 is only the extracting table while the registered resolving source remains the Employment Situation first-print release."},{"rubricItem":"update","severity":"warning","summary":"The initial-claims driver is material to the -0.04 update but no public claims source is included in sourceContext.","actionRequested":"Add the official initial-claims source used, or remove/downweight that update component so every material evidence move is backed by cited public evidence."}],"optionalSuggestions":["State the exact BLS schedule evidence for September 4, 2026 in sourceContext if keeping resolutionDate 2026-09-04.","Clarify the historical volatility sample by listing whether October 2025 is actually unavailable or was omitted for another reason."]}

Emit the final JSON object only.
