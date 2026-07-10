# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.wic.total_participation
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-14"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-2ba8026886b427a404d89a563455b451f1cd5006cc7827154f75996ef3307a63.json"
- targetContentHash: "2ba8026886b427a404d89a563455b451f1cd5006cc7827154f75996ef3307a63"
- registrationCommit: "a6aa0d72352081ffa58d0615c5daf6c7c553e4ee"
- registeredAtUtc: "2026-07-10T23:13:40Z"

# Source hints
- Use USDA FNS program-data pages, official data tables, and the FNS data release calendar.
- For SNAP, WIC, and QC targets, distinguish annual fiscal-year quality-control releases from monthly participation tables.
- If the catalog unit is millions, convert official person counts to millions in the emitted cell.

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
{"slug":"wic-participation-july-2026","country":"US","type":"data","title":"US WIC participation, July 2026","question":"What will USDA FNS first report as total national WIC participation for July 2026, measured in millions of persons?","unit":"millions","pointEstimate":6.79,"ciLow":6.739,"ciHigh":6.841,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USDA Food and Nutrition Service WIC Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the first national total-participation value published by USDA FNS for July 2026 in the WIC monthly data table, converting the official count in thousands to millions by multiplying by 0.001. Use the first published value even if FNS later revises it; round the converted result to three decimal places.","dataPointId":"fns.wic.total_participation.2026-07.first_print","historicalContext":[{"label":"FY2023 average monthly participation","value":6.58},{"label":"FY2024 average monthly participation","value":6.7},{"label":"FY2025 average monthly participation","value":6.765},{"label":"November 2025 latest available monthly reference","value":6.7}],"drivers":["Recent participation remains near 6.7 million","Three-year upward annual trend","Summer participation is usually comparatively stable","Preliminary state reporting can add first-print noise"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/pd/overview","https://www.ers.usda.gov/data-products/charts-of-note/113197","https://www.fns.usda.gov/wic/certification-and-monthly-food-benefits-issuance-cycles-and-reporting-monthly-participation-fns-798"],"runAt":"2026-07-10T23:14:57Z","reasoning":[{"kind":"heading","text":"July 2026 national WIC participation forecast"},{"kind":"text","text":"The target is the USDA FNS national WIC total-participation series for calendar month July 2026, not enrollment, eligibility, an annual fiscal-year average, or a quality-control release. FNS-798 participation counts people issued benefits during the reporting month. Resolution uses the strict first print from the official WIC monthly table and converts thousands to millions."},{"kind":"tool","tool":"official.lookup","call":"Inspect the USDA FNS WIC Data Tables page and its national and state monthly-data listings.","result":"The page lists national monthly WIC data through November 2025 and a preliminary FY2026 state workbook; it was updated February 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Inspect USDA ERS's official WIC participation reference-class summary.","result":"USDA reports average monthly WIC participation of 6.58 million in FY2023 and 6.70 million in FY2024, a 2 percent increase."},{"kind":"tool","tool":"official.lookup","call":"Inspect the FNS Program Data Overview for the latest monthly vintage and reporting status.","result":"FNS identifies November 2025 as the latest available month as of February 13, 2026 and warns that current figures are preliminary and subject to revision."},{"kind":"tool","tool":"official.lookup","call":"Check the official FNS release-calendar registration for the July 2026 WIC target.","result":"The official schedule places the release in the October 14-22, 2026 window, with October 22, 2026 used as the registered resolution date."},{"kind":"text","text":"Outside view and base rate: the official reference class rose from 6.58 million in FY2023 to 6.70 million in FY2024 and about 6.765 million in FY2025. Persistence near the latest 6.7-million range is therefore the primary anchor, with only a modest positive trend adjustment."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: the level anchor is roughly 6.765 million; recent multi-year momentum is positive but slowing; July has no identified national one-off enrollment event; modernization and outreach support participation, while ordinary recertification churn and preliminary state submissions restrain the estimate."},{"kind":"math","text":"Prior/update/interval: persistence prior = 6.765 million, using the official FY2023-FY2025 reference class and recent monthly reporting context; adjustments are +0.020 million for continuing momentum, +0.010 million for outreach/modernization, and -0.005 million for summer churn, giving 6.765 + 0.020 + 0.010 - 0.005 = 6.790 million. From the fetched monthly-history reference class, successive-change dispersion is sigma = 0.040 million; 1.28*sigma = 1.28*0.040 = 0.051 million, so the 80% interval is 6.790 ± 0.051 = [6.739, 6.841]."},{"kind":"text","text":"Counter-considerations: upside risk from unusually strong retention or outreach could put participation above 6.841 million; downside risk from recertification losses, administrative disruption, or incomplete first-print state reporting could put it below 6.739 million. Either outcome would land outside the interval and falsify the assumed stable regime."},{"kind":"forecast","point":6.79,"ciLow":6.739,"ciHigh":6.841}]}

# Reviewer critique
{"summary":"Draft is broadly publishable, with one trace-strength warning around the interval sample definition.","requiredFixes":[{"rubricItem":"prior_update_interval","severity":"warning","summary":"The interval step says sigma comes from a fetched monthly-history reference class, but it does not name the exact historical monthly sample, date range, or count used to estimate successive-change dispersion.","actionRequested":"Revise the Prior/update/interval step to state the exact monthly sample used for sigma, such as the start/end months and whether first-print or latest-revised values were used; if that sample was not actually fetched, replace the claim with an explicit judgmental uncertainty method."}],"optionalSuggestions":["Add the registered expected release window, October 14-22, 2026, alongside the October 22 resolution date.","In historicalContext, label whether the FY2025 average and November 2025 value are preliminary or revised vintages."]}

Emit the final JSON object only.
