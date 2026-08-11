# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.core_pce.mom
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-pce-mom-august-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "us.bea.core_pce.mom_sa.2026-08"
- expectedReleaseWindow: {"end": "2026-09-30", "start": "2026-09-22"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bea.gov"], "expectedReleaseWindow": {"end": "2026-09-30", "start": "2026-09-22"}, "field": "bea.core_pce.mom", "releasePolicy": "first_print", "sourceSeriesId": "bea.core_pce.mom", "sourceUrl": "https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy", "table": "U.S. Bureau of Economic Analysis, Personal Income and Outlays", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-a162b3fdd12be774124e5f6642c79a345a457223eb3326eb6766a70d0ba6920c.json"
- targetContentHash: "a162b3fdd12be774124e5f6642c79a345a457223eb3326eb6766a70d0ba6920c"
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
{"slug":"us-core-pce-mom-august-2026","country":"US","type":"data","title":"US Core PCE MoM, Aug 2026","question":"What will the first-print seasonally adjusted month-over-month percent change in the BEA PCE price index excluding food and energy be for August 2026?","unit":"percent_growth","pointEstimate":0.27,"ciLow":0.13,"ciHigh":0.41,"confidence":0.8,"resolutionDate":"2026-09-30","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays, August 2026","resolutionSourceUrl":"https://www.bea.gov/news/2026/personal-income-and-outlays-august-2026","resolutionRule":"Resolve to the first official BEA Personal Income and Outlays release for August 2026, using the seasonally adjusted percent change from the preceding month for the PCE price index excluding food and energy. Use the initially published one-decimal percent value for the first print; ignore later revisions or annual-update back revisions after that first print.","dataPointId":"us.bea.core_pce.mom_sa.2026-08","historicalContext":[{"label":"2026-06 core PCE MoM SA first print","value":0.1},{"label":"2026-05 core PCE MoM SA first print","value":0.3},{"label":"2026-04 core PCE MoM SA first print","value":0.3},{"label":"2026-03 core PCE MoM SA first print","value":0.3},{"label":"2026-02 core PCE MoM SA first print","value":0.4},{"label":"2026-01 core PCE MoM SA first print","value":0.4}],"drivers":["recent core PCE first prints slowed from 0.3-0.4 to 0.1 in June","June core CPI was flat while shelter rose only 0.1","two-month horizon leaves room for July and August services rebound","September 30 BEA annual update raises first-print process risk but not the resolver"],"sourceContext":["https://www.bea.gov/news/schedule/full","https://www.bea.gov/node/43001","https://www.bea.gov/news/2026/personal-income-and-outlays-june-2026","https://www.bea.gov/index.php/news/2026/personal-income-and-outlays-may-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-march-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-january-2026","https://www.bls.gov/news.release/cpi.htm?lv=true","https://www.bea.gov/information-updates-national-regional-economic-accounts","https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy"],"runAt":"2026-08-11T13:11:33Z","reasoning":[{"kind":"heading","text":"US core PCE month-over-month forecast for August 2026"},{"kind":"text","text":"The target is the BEA PCE price index excluding food and energy, seasonally adjusted, percent change from the preceding month, for August 2026. All historical anchors below use that same core PCE MoM SA variant, not headline PCE, CPI, market-based PCE, year-over-year inflation, or later revised vintages."},{"kind":"tool","tool":"official.lookup","call":"Checked the BEA full release schedule and BEA 26-34 schedule node for the August 2026 Personal Income and Outlays release.","result":"BEA schedule fetched: Personal Income and Outlays, August 2026 is scheduled for September 30, 2026 at 8:30 AM; the preceding July 2026 PIO release is scheduled for August 26, 2026 at 8:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent BEA Personal Income and Outlays releases for core PCE percent change from preceding month.","result":"BEA fetched core PCE MoM SA values: January 2026 0.4, February 2026 0.4, March 2026 0.3, April 2026 0.3, May 2026 0.3, June 2026 0.1; June headline PCE was -0.1 and June core PCE year-over-year was 3.3."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS June 2026 CPI release for contemporaneous price momentum relevant to PCE source data.","result":"BLS fetched June 2026 values: CPI-U all items -0.4 month-over-month, all items less food and energy 0.0, shelter 0.1, owners' equivalent rent 0.2, energy -5.7, and 12-month core CPI 2.6."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's 2026 annual update notice because the August 2026 first print is scheduled on the same day as the annual update.","result":"BEA fetched annual-update timing: 2026 annual updates begin September 30, 2026; the National Economic Accounts annual update open revision period is first quarter 2021 through first quarter 2026; the reference year remains 2017."},{"kind":"text","text":"Reference class/base rate: the Jan-Jun 2026 official first-print core PCE MoM SA sample has values 0.4, 0.4, 0.3, 0.3, 0.3, and 0.1, with a mean base rate of 0.30 percent growth. The latest June print is below that base rate, but a two-month-ahead August forecast should not fully chase one soft month."},{"kind":"math","text":"Prior/update/interval: persistence prior is the Jan-Jun 2026 BEA first-print mean of 0.30 from the historical sample 0.4, 0.4, 0.3, 0.3, 0.3, 0.1; adjustment components are -0.02 for June core CPI at 0.0 and soft shelter at 0.1, -0.02 for latest BEA core PCE momentum at 0.1, and +0.01 for sticky services and two-month mean reversion, giving 0.30 - 0.02 - 0.02 + 0.01 = 0.27. Interval method uses realized dispersion of the fetched core PCE MoM values themselves: sample sigma = 0.11 percentage point, so 1.28*sigma = 0.14; final 80% bounds are 0.27 - 0.14 = 0.13 and 0.27 + 0.14 = 0.41."},{"kind":"text","text":"Upside risk is that July and August services prices rebound after June's flat CPI core reading, pushing core PCE to 0.4 or higher; downside risk is another month of weak medical, apparel, vehicles, or communication prices plus soft shelter, which would land below the interval near 0.1 or less. An outside the interval high outcome would likely require broad services acceleration rather than energy, because food and energy are excluded."},{"kind":"forecast","point":0.27,"ciLow":0.13,"ciHigh":0.41}]}

# Reviewer critique
{"summary":"The draft is publication-ready under the rubric, with clear resolver handling, prior/update/interval math, concrete tails, and no evident leakage or unit ambiguity.","requiredFixes":[],"optionalSuggestions":["Consider noting that the interval is based on only six one-decimal first-print observations, so the realized-sigma estimate is fragile.","Consider aligning the resolutionSourceUrl with the canonical BEA data page if the publication pipeline expects the registered sourceBinding URL rather than the future release URL."]}

Emit the final JSON object only.
