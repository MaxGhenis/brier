# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: cms.nursing_home_compare.reported_total_nurse_staffing_hprd_us
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "nursing-home-staffing-hprd-july-2026"
- country: "US"
- targetUnit: "ratio"
- dataPointId: "cms.nursing_home_compare.reported_total_nurse_staffing_hprd_us.2026-07.first_print"
- resolutionDate: "2026-07-29"
- resolutionSource: "CMS Care Compare nursing home provider data, State US Averages file (NH_StateUSAverages), NATION row, Reported Total Nurse Staffing Hours per Resident per Day"
- resolutionSourceUrl: "https://data.cms.gov/provider-data/dataset/xcdc-v8bm"
- resolutionRule: "Resolve to the NATION row value of 'Reported Total Nurse Staffing Hours per Resident per Day' in the first NH_StateUSAverages file CMS posts at the Care Compare refresh scheduled for 2026-07-29 (the July 2026 quarterly staffing update; schedule per the dataset metastore next-update field), rounded to three decimals. The refresh carries nurse staffing measures onto the next Payroll-Based Journal quarter. If CMS posts the refresh on a different calendar day, resolve to the first file posted at that refresh; ignore later monthly refreshes and revisions."

# Source hints
- Use Medicaid.gov enrollment and eligibility-report pages plus data.medicaid.gov datasets.
- For fixed-vintage Medicaid/CHIP targets, name the reporting period, preliminary/updated status, and whether the target is a national total, weighted average, or state row.
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
{"slug":"nursing-home-staffing-hprd-july-2026","country":"US","type":"data","title":"US nursing home nurse staffing HPRD, July 2026","question":"What will CMS Care Compare State US Averages report for the NATION row, Reported Total Nurse Staffing Hours per Resident per Day, in the first July 2026 quarterly staffing update?","unit":"ratio","pointEstimate":3.89,"ciLow":3.82,"ciHigh":3.96,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"CMS Care Compare nursing home provider data, State US Averages file (NH_StateUSAverages), NATION row, Reported Total Nurse Staffing Hours per Resident per Day","resolutionSourceUrl":"https://data.cms.gov/provider-data/dataset/xcdc-v8bm","resolutionRule":"Resolve to the NATION row value of 'Reported Total Nurse Staffing Hours per Resident per Day' in the first NH_StateUSAverages file CMS posts at the Care Compare refresh scheduled for 2026-07-29 (the July 2026 quarterly staffing update; schedule per the dataset metastore next-update field), rounded to three decimals. The refresh carries nurse staffing measures onto the next Payroll-Based Journal quarter. If CMS posts the refresh on a different calendar day, resolve to the first file posted at that refresh; ignore later monthly refreshes and revisions.","dataPointId":"cms.nursing_home_compare.reported_total_nurse_staffing_hprd_us.2026-07.first_print","historicalContext":[{"label":"2026-06 national average, rounded display","value":3.9},{"label":"2026-05 national average, rounded display","value":3.9},{"label":"2026-04 national average, rounded display","value":3.9},{"label":"2026-02 national average, rounded display","value":3.9},{"label":"2025-11 national average, rounded display","value":3.9},{"label":"CMS final-rule total staffing standard","value":3.48}],"drivers":["recent national average has been flat at 3.9 in rounded public CMS-derived displays","July refresh is a quarterly staffing vintage update, so more movement risk than a non-staffing monthly refresh","minimum staffing rule repeal removes a strong near-term compliance push","labor supply and facility census mix can move HPRD modestly","official first print should ignore later monthly revisions"],"sourceContext":["https://data.cms.gov/provider-data/dataset/xcdc-v8bm","https://data.cms.gov/provider-data/archived-data/nursing-homes","https://projects.propublica.org/nursing-homes/affiliate/a-573","https://projects.propublica.org/nursing-homes/affiliate/a-111","https://projects.propublica.org/nursing-homes/affiliate/a-182","https://projects.propublica.org/nursing-homes/affiliate/a-300","https://www.cms.gov/newsroom/fact-sheets/medicare-and-medicaid-programs-minimum-staffing-standards-long-term-care-facilities-and-medicaid-0","https://www.reginfo.gov/public/do/eAgendaViewRule?RIN=0938-AV25&pubId=202510"],"runAt":"2026-07-21T08:21:29Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 CMS nursing home total nurse staffing HPRD"},{"kind":"text","text":"Framing and exact resolver: use the CMS Care Compare Provider Data Catalog State US Averages dataset xcdc-v8bm, file family NH_StateUSAverages, NATION row, and the Reported Total Nurse Staffing Hours per Resident per Day measure. This is the reported total nurse staffing HPRD variant, not case-mix adjusted staffing, weekend staffing, RN-only staffing, or turnover."},{"kind":"tool","tool":"official.lookup","call":"Opened the CMS Provider Data Catalog State US Averages dataset page for xcdc-v8bm and read current metadata.","result":"CMS lists State US Averages identifier xcdc-v8bm with Last Modified June 1, 2026, Released June 24, 2026, and Planned Update July 29, 2026; the dataset page says each row displays a state or territory average plus the national average."},{"kind":"tool","tool":"official.lookup","call":"Checked the CMS Provider Data Catalog nursing homes archive page for recent refresh history.","result":"The archive page lists nursing-homes snapshots dated 2026-06-24, 2026-05-27, 2026-04-29, 2026-03-25, 2026-02-25, and 2026-01-14, plus 2025 snapshots including 2025-12-15, 2025-11-20, 2025-09-24, and 2025-07-30."},{"kind":"tool","tool":"public.lookup","call":"Checked ProPublica Nursing Home Inspect pages that mirror CMS nursing home public data for rounded national-average staffing context across vintages.","result":"ProPublica pages show National average reported nurse hours/resident/day of 3.9 for June 2026, 3.9 for May 2026, 3.9 for April 2026, 3.9 for February 2026, and 3.9 for November 2025; the same June 2026 pages show national average nurse turnover near 46.1%."},{"kind":"tool","tool":"official.lookup","call":"Checked CMS final-rule and current regulatory status sources for staffing policy mechanism context.","result":"CMS's 2024 final-rule fact sheet set a total nurse staffing standard of 3.48 HPRD, including 0.55 RN HPRD and 2.45 nurse-aide HPRD, with non-rural Phase 2 within 2 years and rural Phase 2 within 3 years; the 2026 Unified Agenda entry for RIN 0938-AV25 says OBBBA precludes implementation, administration, or enforcement until September 30, 2034."},{"kind":"text","text":"Reference class and base rate: for a national average level series with monthly/quarterly CMS Care Compare refreshes, the strongest prior is the recent same-series national level. The rounded public CMS-derived history is flat at 3.9 from November 2025 through June 2026, so the base rate is just under 3.9 rather than a trend extrapolation toward the repealed 3.48 policy threshold."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: the level anchor is 3.9 rounded; momentum is essentially flat; the July quarterly staffing update can incorporate a new Payroll-Based Journal quarter and therefore deserves a little more dispersion than the monthly snapshots; the policy mechanism is slightly downward because the 3.48 HPRD enforcement push was delayed/repealed, but 3.48 is below the observed national average, so it is not a strong downward level target."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest rounded national average of 3.9 using the CMS-derived November 2025, February 2026, April 2026, May 2026, and June 2026 reference class. Adjustment components: -0.01 for repeal/removal of near-term compliance pressure, +0.00 for flat recent momentum, +0.00 for national aggregation, giving 3.90 - 0.01 = 3.89. Successive changes in the rounded fetched history are 0.0, 0.0, 0.0, and 0.0, so observed rounded sigma = 0.000; because one-decimal displays mask exact CMS row movement, I use a display-granularity floor with sigma = 0.045. 1.28*sigma = 1.28*0.045 = 0.058; widening modestly for a quarterly staffing vintage gives an 80% half-width of 0.070, so 3.89 +/- 0.07 = [3.82, 3.96]."},{"kind":"text","text":"Counter-consideration and falsification: upside risk would be a surprisingly high-acuity or high-staffing PBJ quarter, post-acute census mix shift, or facilities maintaining staffing above pre-repeal plans, which would land above the interval if the national row prints above 3.96. Downside risk is workforce loosening, margin pressure, or a lower-census denominator change reversing, which would land below the interval if the first print is under 3.82. Outside the interval would require a larger exact national movement than is visible in the recent rounded reference class."},{"kind":"forecast","point":3.89,"ciLow":3.82,"ciHigh":3.96}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, with one blocking concern that the interval is built from rounded proxy values rather than exact same-series first-print volatility.","requiredFixes":[{"rubricItem":"interval","severity":"blocking","summary":"The interval method says observed rounded sigma is 0.000 and then substitutes a 0.045 display-granularity floor, but the target resolves to a three-decimal CMS row value, so rounded 3.9 proxy history is too weak to justify the 80% interval.","actionRequested":"Use exact NH_StateUSAverages NATION values from archived CMS files if available, or explicitly state that exact historical first-print values were unavailable and justify the 0.045 sigma floor from one-decimal rounding error plus quarterly refresh risk."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact step names the prior and adjustments, but the historical sample is described as rounded public CMS-derived displays rather than exact CMS first-print observations.","actionRequested":"Clarify whether the listed November 2025 through June 2026 values are exact CMS row values, one-decimal mirror displays, or mixed proxies; if proxies, say that directly in the compact step."}],"optionalSuggestions":["Consider replacing affiliate-level ProPublica page citations with a direct national-average or CMS archive citation if one exists, since affiliate pages are an indirect way to support a national row prior.","State whether the -0.01 policy adjustment is directional judgment rather than estimated from history, because the rule threshold is below the current national average.","Tail scenarios are adequate, but could be tightened by naming PBJ quarter composition and census-denominator changes as the mechanisms most likely to move this exact HPRD row."]}

Emit the final JSON object only.
