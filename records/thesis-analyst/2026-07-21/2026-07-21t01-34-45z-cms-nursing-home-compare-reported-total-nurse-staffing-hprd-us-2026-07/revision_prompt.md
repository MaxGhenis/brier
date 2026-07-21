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
{"slug":"nursing-home-staffing-hprd-july-2026","country":"US","type":"data","title":"US nursing-home total nurse staffing HPRD, July 2026 first print","question":"What will the NATION row value for Reported Total Nurse Staffing Hours per Resident per Day be in CMS Care Compare State US Averages at the July 2026 first print?","unit":"ratio","pointEstimate":3.92,"ciLow":3.84,"ciHigh":4.0,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"CMS Care Compare nursing home provider data, State US Averages file (NH_StateUSAverages), NATION row, Reported Total Nurse Staffing Hours per Resident per Day","resolutionSourceUrl":"https://data.cms.gov/provider-data/dataset/xcdc-v8bm","resolutionRule":"Resolve to the NATION row value of 'Reported Total Nurse Staffing Hours per Resident per Day' in the first NH_StateUSAverages file CMS posts at the Care Compare refresh scheduled for 2026-07-29 (the July 2026 quarterly staffing update; schedule per the dataset metastore next-update field), rounded to three decimals. The refresh carries nurse staffing measures onto the next Payroll-Based Journal quarter. If CMS posts the refresh on a different calendar day, resolve to the first file posted at that refresh; ignore later monthly refreshes and revisions.","dataPointId":"cms.nursing_home_compare.reported_total_nurse_staffing_hprd_us.2026-07.first_print","historicalContext":[{"label":"Oct 2023 CMS-based national row mirror","value":3.76},{"label":"Jan 2024 State US Averages value cited in Illinois statute","value":3.79},{"label":"State US Averages public preview value","value":3.83737},{"label":"June 2026 CMS-based national mirror","value":3.9}],"drivers":["latest public national average near 3.9 HPRD","slow upward drift in fetched national staffing anchors","July refresh rolls staffing measures onto the next PBJ quarter","federal staffing policy pressure is gradual rather than a discrete July step"],"sourceContext":["https://data.cms.gov/provider-data/dataset/xcdc-v8bm","https://data.cms.gov/provider-data/topics/nursing-homes/data-sources","https://www.medicare.gov/care-compare/resources/nursing-home/staffing","https://www.beckershospitalreview.com/post-acute/average-patients-nurse-staffing-hours-by-state/","https://www.ilga.gov/Documents/legislation/ilcs/documents/030500050K5-5.2.htm","https://www.johnsnowlabs.com/marketplace/nursing-home-compare-state-averages/","https://projects.propublica.org/nursing-homes/affiliate/a-78"],"runAt":"2026-07-21T01:35:07Z","reasoning":[{"kind":"heading","text":"CMS State US Averages staffing HPRD forecast"},{"kind":"text","text":"Framing and exact resolver: this target is CMS Provider Data Catalog dataset xcdc-v8bm, State US Averages/NH_StateUSAverages, NATION row, Reported Total Nurse Staffing Hours per Resident per Day. I keep the ledger first-print rule and do not add a same-day correction or revision grace rule."},{"kind":"tool","tool":"official.lookup","call":"CMS Provider Data Catalog State US Averages dataset page lookup","result":"Fetched official dataset metadata: identifier xcdc-v8bm, Last Modified June 1 2026, Released June 24 2026, Planned Update July 29 2026, publisher CMS, and public access level public."},{"kind":"tool","tool":"official.lookup","call":"CMS Provider Data Catalog nursing-homes data-source page lookup","result":"Fetched official source context: PBJ staffing data are collected quarterly, the nursing-home topic covers more than 15,000 nationwide facilities, and staffing measures include total staffing, RN staffing, physical therapist hours, and staff turnover."},{"kind":"tool","tool":"official.lookup","call":"Medicare Care Compare staffing methodology page lookup","result":"Fetched official measure definition: staffing hours per resident per day equals total hours worked divided by total residents, and total nurse staffing includes 3 staff groups: RNs, LPNs/LVNs, and CNAs/nurse aides in training."},{"kind":"tool","tool":"public.lookup","call":"Becker summary of CMS State US Averages table","result":"Fetched CMS-based historical national row: NATION average number of residents per day 80.8 and Reported Total Nurse Staffing Hours per Resident per Day 3.76, published October 10 2023."},{"kind":"tool","tool":"public.lookup","call":"Illinois statutory text citing federal State US Averages staffing values","result":"Fetched statutory citation to federal staffing reports: January 2024 State US Averages file NATION Reported Total Nurse Staffing Hours Per Resident Per Day 3.79 and January 2024 Provider Information resident-days weighted mean 3.662."},{"kind":"tool","tool":"public.lookup","call":"State US Averages preview and current CMS-based mirror checks","result":"Fetched field-specific context: State US Averages preview includes Reported Total Nurse Staffing Hours Per Resident Per Day value 3.83737; ProPublica CMS-based June 2026 nursing-home pages report national average nurse hours per resident per day 3.9."},{"kind":"text","text":"Base rate/reference class: this is a slow-moving national average level series. The fetched public anchors are 3.76, 3.79, 3.83737, and about 3.9; that reference class supports persistence near the latest level plus only a small July-quarterly drift adjustment."},{"kind":"text","text":"Variant discipline: all numeric anchors are reported total nurse staffing hours per resident per day or direct public mirrors of that concept, not adjusted total staffing, RN-only staffing, weekend staffing, turnover, or facility-level Provider Information rows. The target variant is the State US Averages NATION row."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest CMS-based national mirror 3.90; historical sample is fetched levels 3.76, 3.79, 3.83737, 3.90. Successive changes are +0.03000, +0.04737, and +0.06263, so sigma = 0.016 for recent change dispersion and 1.28*sigma = 0.021. I add +0.02 for upward momentum into the July quarterly staffing refresh, giving point 3.92. I widen the 80% half-width to 0.08, about 3.8x the mechanical 0.021, because the sample is sparse, irregularly spaced, partly rounded or mirrored, and the PBJ-quarter rollover can create a larger first-print step than the limited anchor history implies."},{"kind":"text","text":"Policy/mechanism effects: CMS minimum-staffing and SNF VBP attention create mild upside pressure, but implementation and reporting responses are gradual, so I treat policy as roughly +0.00 to +0.02 rather than a discrete July level shift."},{"kind":"text","text":"Prior-run check: an inspected published Thesis run for the same target had point 3.92 and interval 3.84 to 4.00; I treated it as strategy context only and did not use its catalog values as official outcome evidence."},{"kind":"text","text":"Counter-considerations: upside risk is a clean PBJ quarter, compliance-driven staffing gains, or sample mix improvement that would land above the interval, especially above 4.00. Downside risk is weaker staffing, facility exits, reporting issues, or a methodological change that would land below the interval, especially below 3.84."},{"kind":"forecast","point":3.92,"ciLow":3.84,"ciHigh":4.0}]}

# Reviewer critique
{"summary":"The draft is mostly target-coherent, but it should remove or quarantine same-target prior-run/circularity context before publication.","requiredFixes":[{"rubricItem":"leakage","severity":"blocking","summary":"The reasoning says it inspected a published Thesis run for the same target with the same point and interval; even if described as strategy context, this creates catalog/peer-forecast circularity risk.","actionRequested":"Remove the prior-run check from the reasoning and source context, or explicitly state it was excluded before numeric estimation and show the point/interval derivation without relying on that same-target forecast."},{"rubricItem":"interval","severity":"warning","summary":"The interval is ultimately judgment-widened from only three irregular, partly rounded or mirrored changes, so the realized-volatility basis is thin.","actionRequested":"Clarify that the 3.84-4.00 interval is an explicit uncertainty interval rather than a robust realized-volatility estimate, and name the sparse/irregular anchor limitation in the final compact interval step."}],"optionalSuggestions":["Date the 'State US Averages public preview value' anchor or identify which file/month it reflects.","Keep CMS as the resolver and treat ProPublica/Becker/Illinois only as historical mirrors or citations, not resolution authorities."]}

Emit the final JSON object only.
