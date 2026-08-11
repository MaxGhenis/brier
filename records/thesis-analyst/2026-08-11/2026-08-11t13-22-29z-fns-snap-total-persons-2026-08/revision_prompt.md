# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.snap.total_persons
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.august_2026"
- expectedReleaseWindow: {"end": "2027-01-11", "start": "2027-01-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2027-01-11", "start": "2027-01-03"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-bc941c534dcbaf1f13d1b9ba88a016f9cf51fde91019bc90beea1873ced2f0a2.json"
- targetContentHash: "bc941c534dcbaf1f13d1b9ba88a016f9cf51fde91019bc90beea1873ced2f0a2"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"

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
{"slug":"snap-participation-august-2026","country":"US","type":"data","title":"US SNAP participation, August 2026","question":"What will USDA FNS first report for national SNAP participation, Persons, in August 2026, converted from persons to millions?","unit":"millions","pointEstimate":35.81,"ciLow":35.08,"ciHigh":36.55,"confidence":0.8,"resolutionDate":"2027-01-11","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first official USDA FNS SNAP Data Tables national monthly Participation Persons value for August 2026, using the national monthly table 'Persons, Households, Benefits, and Average Monthly Benefit per Person & Household'; convert the official persons count to millions by multiplying by 0.000001, equivalent to the registered thousands-to-millions transform when the table is read in thousands. Use the first print only; do not substitute later revisions.","dataPointId":"usda.fns.snap.persons.august_2026","historicalContext":[{"label":"Apr 2026 latest preliminary","value":37.011096},{"label":"Mar 2026 preliminary","value":37.438048},{"label":"Feb 2026 preliminary","value":37.875833},{"label":"Aug 2025","value":41.841272}],"drivers":["Recent official SNAP participation decline through April 2026","FY 2026 benefit and eligibility standards already in force for the target month","Policy implementation risk from 2025 SNAP eligibility and work-rule changes","Seasonal August participation is not enough to offset current downtrend"],"sourceContext":["https://fns-prod.azureedge.us/pd/supplemental-nutrition-assistance-program-snap","https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-4fymonthly7.pdf","https://fns-prod.azureedge.us/snap/allotment/cola"],"runAt":"2026-08-11T13:22:50Z","reasoning":[{"kind":"heading","text":"SNAP national participation forecast for August 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the USDA FNS national SNAP monthly table, Participation Persons, for August 2026, first print, converted to millions. The registered contract sets a resolve-by-bound resolution date of 2027-01-11 within the expected 2027-01-03 to 2027-01-11 release window; the FNA data page itself showed the monthly table and latest-data timestamp but I did not find a separate date-specific public release calendar page in this run."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA/FNA SNAP Data Tables page and identified the national monthly participation table and latest data vintage.","result":"Fetched page showed Latest Available Month = April 2026, Page updated = August 06, 2026, and the national monthly table link FY 23 through FY 26; this confirms the exact series family and a July 2026 public update."},{"kind":"tool","tool":"official.lookup","call":"Opened the USDA/FNA national SNAP monthly PDF table for FY 2023 through FY 2026 and read recent Persons values.","result":"Fetched Persons values: Aug 2025 = 41,841,272; Sep 2025 = 41,637,114; Oct 2025 = 41,096,660; Nov 2025 = 39,999,890; Dec 2025 = 39,207,898; Jan 2026 = 38,476,351; Feb 2026 = 37,875,833; Mar 2026 = 37,438,048; Apr 2026 = 37,011,096."},{"kind":"tool","tool":"official.lookup","call":"Read the USDA/FNA Program Data overview context for vintage and preliminary-status handling.","result":"Fetched overview values: latest month April 2026, data as of July 10, 2026, annual state-level data cover 2020-2025, and the page says most current numbers are preliminary and subject to revision."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA/FNA FY 2026 SNAP COLA policy page to check target-month benefit/eligibility setting.","result":"Fetched FY 2026 standards effective Oct. 1, 2025 through Sept. 30, 2026; 48-state gross monthly income limit for household size 4 = $3,483; maximum monthly allotment for household size 4 in the 48 states and DC = $994; minimum allotment for 1-2 person households = $24."},{"kind":"text","text":"Reference class/base rate: for an official-source level series with monthly administrative reporting, I start from persistence plus recent monthly change, not from the long pandemic/disaster period. The cleanest recent reference class is FY 2025 through FY 2026 national monthly Persons, with special caution that FY 2023 included unusually high and volatile values such as Aug 2023 = 53.518725 million."},{"kind":"text","text":"Level and momentum: Apr 2026 was 37.011096 million. Recent sequential changes were -0.540454, -1.096770, -0.791992, -0.731547, -0.600518, -0.437785, and -0.426952 million from Sep 2025-Apr 2026, so the decline was still large but easing by March-April."},{"kind":"text","text":"Policy and one-off effects: FY 2026 eligibility and allotment settings are already in force for August 2026, so I do not add a mechanical October COLA break. I do keep a negative adjustment because 2025-2026 policy memoranda and work-rule/eligibility implementation risk plausibly continue trimming caseloads before August, while the November 2025 disruption is partly a one-off and should not be linearly extrapolated."},{"kind":"math","text":"Prior/update/interval: persistence prior = Apr 2026 official Persons of 37.011096 million; historical sample = recent official monthly changes from Sep 2025 through Apr 2026; adjustment components = -0.25 million/month underlying caseload normalization, -0.05 million/month policy/friction drag, and no positive August seasonal offset because 2025 Apr-to-Aug was -0.515774 million. Point = 37.011096 + 4*(-0.30) = 35.811096, rounded to 35.81. Monthly change dispersion from the seven fetched changes is about 0.249 million; four-month propagated sigma = sqrt(4)*0.249 = 0.498 million, widened for policy uncertainty to sigma = 0.574 million; 1.28*sigma = 0.735 million, giving 35.811096 +/- 0.735 = [35.08, 36.55]."},{"kind":"text","text":"Counter-consideration: upside risk is a faster-than-expected halt in recertification losses or disaster-assistance additions, which would land above the interval if August participation stays above 36.55 million. Downside risk is broader eligibility/work-rule implementation or administrative churn, which would land below the interval if August participation falls below 35.08 million. A major reporting reclassification would also be outside the interval but should still resolve on the same first-print Persons field."},{"kind":"forecast","point":35.81,"ciLow":35.08,"ciHigh":36.55}]}

# Reviewer critique
{"summary":"Draft is publishable with minor clarification needed around policy evidence and unit/transform wording.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The negative policy/friction adjustment is only loosely supported; the draft mentions 2025-2026 policy memoranda and work-rule/eligibility implementation risk without naming the specific public evidence used.","actionRequested":"Name the concrete cited policy source or reduce the policy adjustment to a qualitative downside risk rather than a quantified -0.05 million/month component."},{"rubricItem":"coherence","severity":"warning","summary":"The resolver unit wording mixes persons-count conversion by 0.000001 with the ledger's registered thousands-to-millions transform of 0.001, which is mathematically reconcilable but easy to misread.","actionRequested":"State explicitly that the target resolves to the FNS table's Persons field expressed in thousands under the registered sourceBinding, then multiplied by 0.001 to millions; if reading an underlying raw persons count, this is equivalent to multiplying by 0.000001."}],"optionalSuggestions":["In the compact math step, label the seven monthly changes as Sep 2025 through Apr 2026 changes from the first-print/current FNS table to make the sample boundary unambiguous.","Replace the typo-like 'USDA/FNA' references with 'USDA FNS' for consistency with the resolver."]}

Emit the final JSON object only.
