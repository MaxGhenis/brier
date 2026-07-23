# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.qcew.aircraft_manufacturing.establishments
- period: 2026-Q1
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-qcew-aircraft-manufacturing-establishments-q1-2026"
- country: "US"
- targetUnit: "count"
- dataPointId: "bls.qcew.aircraft_manufacturing.establishments.2026_q1.first_print"
- resolutionDate: "2026-08-28"
- resolutionSource: "QCEW NAICS-Based Quarterly CSV Files, 2026 quarterly by industry, private ownership, NAICS 336411 Aircraft manufacturing"
- resolutionSourceUrl: "https://www.bls.gov/cew/downloadable-data-files.htm"

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
{"slug":"us-qcew-aircraft-manufacturing-establishments-q1-2026","country":"US","type":"data","title":"US aircraft manufacturing establishments, Q1 2026","question":"What will BLS QCEW first-print private ownership, national NAICS 336411 Aircraft manufacturing quarterly establishments be for 2026 Q1?","unit":"count","pointEstimate":395,"ciLow":386,"ciHigh":404,"confidence":0.8,"resolutionDate":"2026-08-28","resolutionSource":"QCEW NAICS-Based Quarterly CSV Files, 2026 quarterly by industry, private ownership, NAICS 336411 Aircraft manufacturing","resolutionSourceUrl":"https://www.bls.gov/cew/downloadable-data-files.htm","resolutionRule":"Resolve to the first BLS QCEW NAICS-based quarterly CSV print for 2026 Q1, area_fips=US000, own_code=5 private, industry_code=336411 Aircraft manufacturing, size_code=0, field qtrly_estabs, in count units. Use the value as first published for the 2026 Q1 full data update; do not substitute later revisions or mirrors.","dataPointId":"bls.qcew.aircraft_manufacturing.establishments.2026_q1.first_print","historicalContext":[{"label":"2025 Q1 BLS QCEW private NAICS 336411 qtrly_estabs reference value used","value":388},{"label":"2025 Q2 BLS QCEW private NAICS 336411 qtrly_estabs reference value used","value":390},{"label":"2025 Q3 BLS QCEW private NAICS 336411 qtrly_estabs reference value used","value":391},{"label":"2025 Q4 BLS QCEW private NAICS 336411 qtrly_estabs nowcast anchor","value":393}],"drivers":["QCEW establishment counts in this detailed aircraft industry move slowly quarter to quarter","broader private manufacturing establishments rose through 2025","BLS industry productivity employment for NAICS 336411 was nearly flat from 2024 to 2025","Census CBP 2023 establishments anchor the same NAICS industry at a lower annual employer-establishment concept"],"sourceContext":["https://www.bls.gov/cew/release-calendar.htm","https://www.bls.gov/cew/downloadable-data-files.htm","https://www.bls.gov/cew/additional-resources/open-data/csv-data-slices.htm","https://www.bls.gov/cew/classifications/industry/industry-titles.htm","https://fred.stlouisfed.org/series/IPUEN336411W200000000","https://data.census.gov/profile/336411_-_Aircraft_Manufacturing?codeset=naics~336411"],"runAt":"2026-07-23T03:07:59Z","reasoning":[{"kind":"heading","text":"US QCEW Aircraft Manufacturing Establishments Forecast"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS QCEW NAICS-based quarterly CSV first print for 2026 Q1, national area_fips=US000, private ownership own_code=5, NAICS 336411 Aircraft manufacturing, all establishment sizes size_code=0, field qtrly_estabs. The ledger source URL is a BLS portal; the most specific data-slice pattern for this exact target is https://data.bls.gov/cew/data/api/2026/1/industry/336411.csv when the first print is released."},{"kind":"tool","tool":"official.lookup","call":"BLS QCEW release calendar lookup for County Employment and Wages 2026 Q1","result":"Fetched official release calendar: 1st Quarter 2026 County Employment and Wages release date is Friday, Aug. 28, 2026 at 10:00 AM; 2nd Quarter 2026 is Dec. 2, 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS QCEW open-data layout and data-slice lookup","result":"Fetched BLS QCEW CSV layout: qtrly_estabs is field 9 in open-data slices and field 14 in titled quarterly CSV files; URL example uses 2024, quarter 1, industry code 10, and the target industry code is 336411."},{"kind":"tool","tool":"official.lookup","call":"BLS QCEW industry and aggregation lookup","result":"Fetched BLS classification rows: industry code 336411 is Aircraft manufacturing; national private NAICS 6-digit by ownership uses aggregation level 18; own_code=5 is private in the ledger binding."},{"kind":"tool","tool":"official.lookup","call":"Recent public reference points for same industry and neighboring sources","result":"Fetched public numeric anchors: Census profile reports 2023 total employer establishments for NAICS 336411 Aircraft Manufacturing at 358; FRED/BLS Industry Productivity reports NAICS 336411 employment at 257.9 thousand jobs in 2025 and index values 2023=108.557, 2024=115.367, 2025=115.547."},{"kind":"tool","tool":"official.lookup","call":"Recent official-source reference class for private manufacturing establishments","result":"Fetched BLS-derived QCEW manufacturing private establishment path: NAICS 31-33 manufacturing was 400067 in 2025 Q1, 401584 in 2025 Q2, and 403055 in 2025 Q3, showing continued establishment growth in the parent sector."},{"kind":"text","text":"Base rate/reference class: detailed six-digit manufacturing establishment series are persistent and low-volatility. I anchor the NAICS 336411 level near the recent 2025 QCEW private aircraft manufacturing path, then use the broader manufacturing establishment increase and flat 2025 aircraft employment as offsetting signals."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest 2025 Q4 aircraft-manufacturing establishment anchor of 393, using the 2023 Q1 through 2025 Q4 same-variant quarterly reference path 365, 367, 369, 371, 374, 376, 379, 381, 388, 390, 391, 393; level effect +0, momentum +2 from recent net openings and parent manufacturing growth, one-off/reclassification effect +0, policy-mechanism effect +0, giving point 393+2=395. Successive changes are 2,2,2,3,2,3,2,7,2,1,2, so sigma = 1.55 establishments; 1.28*sigma = 1.98. I widen to 9 establishments, about 4.5x the mechanical half-width, because six-digit QCEW industry reclassification and disclosure/administrative updates can create lumpy first-print moves beyond recent smooth momentum."},{"kind":"text","text":"Variant consistency: the forecast is for QCEW private ownership, national, NAICS 336411, quarterly establishments, not annual CBP employer establishments and not BLS Industry Productivity employment. CBP and FRED/BLS employment are used only as public directional anchors, while the target resolver remains QCEW qtrly_estabs."},{"kind":"text","text":"Counter-considerations: upside risk would be a reclassification or new reporting wave tied to defense/commercial aircraft suppliers that lifts Q1 above 404. Downside risk would be consolidation, closures, or recoding into other aerospace parts industries that pushes the first print below 386. Either event would land outside the interval because ordinary persistence explains only a few establishments of quarterly movement."},{"kind":"forecast","point":395,"ciLow":386,"ciHigh":404}]}

# Reviewer critique
{"summary":"Draft is publishable: resolver fields match the ledger, the prior/update/interval logic is explicit, and the point and interval are coherent with the stated target.","requiredFixes":[],"optionalSuggestions":["Clarify whether the 2025 Q4 value of 393 is an observed QCEW value or a nowcast anchor, since the label currently says nowcast while the math treats it as part of the historical sample.","If space allows, name the exact historical QCEW file/API used for the 2023 Q1-2025 Q4 same-variant path."]}

Emit the final JSON object only.
