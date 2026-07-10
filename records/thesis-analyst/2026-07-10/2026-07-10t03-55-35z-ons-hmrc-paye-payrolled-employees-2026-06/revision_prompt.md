# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.hmrc.paye_payrolled_employees
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-hmrc-paye-payrolled-employees-june-2026"
- targetUnit: "millions"
- dataPointId: "ons.hmrc.paye_payrolled_employees.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-22", "start": "2026-07-14"}, "field": "official_release:ons_hmrc:paye:2026-05:payrolled_employees", "releasePolicy": "first_print", "sourceSeriesId": "ons.hmrc.paye_payrolled_employees", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026", "table": "Earnings and employment from Pay As You Earn Real Time Information, UK: June 2026", "transform": {"factor": 1, "operation": "identity"}}

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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
{"slug":"ons-hmrc-paye-payrolled-employees-june-2026","country":"UK","type":"data","title":"UK PAYE Payrolled Employees, June 2026","question":"ONS/HMRC Pay As You Earn Real Time Information seasonally adjusted UK payrolled employees for June 2026, first print","unit":"millions","pointEstimate":30.274,"ciLow":30.224,"ciHigh":30.324,"confidence":0.8,"resolutionDate":"2026-07-21","resolutionSource":"ONS/HMRC Earnings and employment from Pay As You Earn Real Time Information, UK","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026","resolutionRule":"Resolve to the first official ONS/HMRC PAYE RTI seasonally adjusted UK payrolled employees estimate for June 2026, in millions, from the first print only; do not use later revisions or same-day corrections unless the official first-print table itself is replaced before publication completes.","dataPointId":"ons.hmrc.paye_payrolled_employees.june_2026.first_print","historicalContext":[{"label":"May 2026 early level, seasonally adjusted","value":30.3},{"label":"April 2026 early level, seasonally adjusted","value":30.2},{"label":"March 2026 early level, seasonally adjusted","value":30.3},{"label":"May 2026 first-print monthly change, millions","value":0.002},{"label":"April 2026 first-print monthly change, millions","value":-0.1}],"drivers":["Recent PAYE employment first prints are weak but not steadily collapsing","May 2026 flash estimate was nearly flat after a sharp April first print","Annual PAYE employee growth remains negative","Early tax-year PAYE flash estimates carry larger revision uncertainty","Accommodation and food service employment is a visible drag"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/realtimeinformationstatisticsreferencetableseasonallyadjusted","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/may2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/april2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/march2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/february2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/january2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/december2025"],"runAt":"2026-07-10T03:56:29Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 UK PAYE payrolled employees"},{"kind":"text","text":"Exact resolver is the ONS/HMRC PAYE RTI UK payrolled employees level, seasonally adjusted, first print for June 2026, in millions. The relevant table is the seasonally adjusted Earnings and employment from Pay As You Earn Real Time Information dataset; all anchors below use the same seasonally adjusted UK payrolled-employees variant."},{"kind":"text","text":"Ledger discrepancy noted: the canonical URL supplied for this target is the June 2026 bulletin, which is already published and contains the May 2026 early estimate, while the June 2026 data period should first appear in the next bulletin scheduled for 21 July 2026. I keep the forecast tied to the supplied slug, dataPointId, resolver, and URL rather than silently changing the target."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS/HMRC June 2026 PAYE RTI bulletin and seasonally adjusted dataset page.","result":"Fetched latest release date 18 June 2026, next release 21 July 2026, May 2026 payrolled employees 30.3 million, May monthly change +2,000 employees, May annual change -119,000 employees, and April monthly change revised to -53,000 employees."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS/HMRC May 2026 PAYE RTI bulletin for the prior first-print April estimate.","result":"Fetched April 2026 first-print payrolled employees 30.2 million, April monthly change -100,000 employees, April annual change -210,000 employees, and March monthly change revised to -28,000 employees."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS/HMRC April 2026 and March 2026 PAYE RTI bulletins for earlier first-print changes.","result":"Fetched March 2026 first-print payrolled employees 30.3 million with monthly change -11,000 employees and annual change -65,000 employees; fetched February 2026 first-print payrolled employees 30.3 million with monthly change +20,000 employees and annual change -49,000 employees."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS/HMRC February 2026, January 2026, and December 2025 PAYE RTI bulletins for the recent first-print reference class.","result":"Fetched January 2026 first-print change -11,000 employees, December 2025 first-print change -43,000 employees, and November 2025 first-print change -38,000 employees; the corresponding early levels were January 30.3 million, December 30.2 million, and November 30.3 million."},{"kind":"text","text":"The base rate is the recent first-print monthly-change reference class: Nov -38k, Dec -43k, Jan -11k, Feb +20k, Mar -11k, Apr -100k, May +2k. That averages about -26k per month, with the latest print improving after a weak April but still in a negative annual-growth regime."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from the May 2026 first-print level of 30.300 million; historical sample is recent first-print monthly changes [-0.038, -0.043, -0.011, 0.020, -0.011, -0.100, 0.002] million; adjustment components are level 30.300, momentum/base-rate change -0.026, one-off April weakness partly faded, and no separate policy-mechanism add-on. sigma = 0.039 million from the sample standard deviation of those successive changes, so 80% half-width is roughly 1.28*sigma = 0.050 million. Point = 30.300 - 0.026 = 30.274; interval = 30.274 +/- 0.050 = [30.224, 30.324]."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound from April tax-year imputation weakness or late RTI submissions, which would land above the interval if June is above 30.324 million. Downside risk is renewed payroll shedding in retail, hospitality, or administrative services, which would land below the interval if June is below 30.224 million."},{"kind":"forecast","point":30.274,"ciLow":30.224,"ciHigh":30.324}]}

# Reviewer critique
{"summary":"Draft is mostly coherent, but the resolver/source binding is materially confused because the supplied URL/field appear to identify the May 2026 first print while the forecast targets June 2026.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft notes a ledger discrepancy, but the JSON still uses the supplied June 2026 bulletin URL while saying the June 2026 data period first appears in the 21 July 2026 release; sourceBinding also names 2026-05, not 2026-06.","actionRequested":"Keep the target slug/dataPointId as instructed, but make the resolver section explicitly state that the forecast target is the June 2026 payrolled-employees first print and flag that the canonical URL/sourceBinding appear to point to the prior-period May 2026 first print; do not leave the reader unsure which release page resolves the target."},{"rubricItem":"coherence","severity":"warning","summary":"Historical context rounds recent levels to one decimal million, which makes April 30.2 and May 30.3 look inconsistent with the stated +0.002 million May monthly change and point calculation from 30.300.","actionRequested":"Use more precise level anchors where available, or state that displayed historical levels are rounded ONS bulletin figures while the monthly-change arithmetic is in thousands/millions."}],"optionalSuggestions":["Clarify whether the 80% interval uses sample standard deviation over recent first-print monthly changes only, and whether no extra June-specific release uncertainty was added.","Tail scenarios are adequate, but could name approximate monthly-change thresholds implied by the interval: about +24k upside or -76k downside from the 30.300 million May anchor."]}

Emit the final JSON object only.
