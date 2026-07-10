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
- country: "UK"
- targetUnit: "millions"
- dataPointId: "ons.hmrc.paye_payrolled_employees.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-22", "start": "2026-07-14"}, "field": "official_release:ons_hmrc:paye:2026-05:payrolled_employees", "releasePolicy": "first_print", "sourceSeriesId": "ons.hmrc.paye_payrolled_employees", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026", "table": "Earnings and employment from Pay As You Earn Real Time Information, UK: June 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-7098e22567178b5a76d97e9c124dd2dfb9868c2750d780f361151cc9bd7ae37e.json"
- targetContentHash: "7098e22567178b5a76d97e9c124dd2dfb9868c2750d780f361151cc9bd7ae37e"
- registeredAtUtc: "2026-07-10T05:58:27Z"

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
{"slug":"ons-hmrc-paye-payrolled-employees-june-2026","country":"UK","type":"data","title":"UK PAYE Payrolled Employees, June 2026","question":"What will the ONS/HMRC first-print early estimate of UK seasonally adjusted PAYE payrolled employees be for June 2026, in millions?","unit":"millions","pointEstimate":30.28,"ciLow":30.225,"ciHigh":30.335,"confidence":0.8,"resolutionDate":"2026-07-21","resolutionSource":"ONS/HMRC Earnings and employment from Pay As You Earn Real Time Information, UK","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026","resolutionRule":"Resolve to the first official ONS/HMRC print of seasonally adjusted UK PAYE payrolled employees for June 2026, in millions, using the headline payrolled employees series in the Earnings and employment from Pay As You Earn Real Time Information bulletin/table. Use the first published estimate only, with no later revisions. The registered ledger URL points to the June 2026 bulletin, which ONS has already used for May 2026 data; the official next-release schedule indicates the June 2026 observation should first print on 2026-07-21, so this discrepancy should be preserved for audit rather than silently changing the target.","dataPointId":"ons.hmrc.paye_payrolled_employees.june_2026.first_print","historicalContext":[{"label":"May 2026 early payrolled employees, millions","value":30.3},{"label":"May 2026 month change, millions","value":0.002},{"label":"April 2026 revised month change, millions","value":-0.053},{"label":"March 2026 revised month change, millions","value":-0.028},{"label":"May 2026 annual change, millions","value":-0.119}],"drivers":["May level was broadly flat at 30.3 million","April weakness was revised from -100,000 to -53,000","Annual growth remained negative at -119,000","Early tax-year PAYE flashes have elevated revision and imputation uncertainty","Vacancy and sector signals point to a soft but not collapsing labour market"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/may2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/realtimeinformationstatisticsreferencetableseasonallyadjusted","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/earningsandemploymentfrompayasyouearnrealtimeinformationrevisiontriangle"],"runAt":"2026-07-10T06:01:24Z","reasoning":[{"kind":"heading","text":"UK PAYE Payrolled Employees June 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: forecast the ONS/HMRC PAYE RTI seasonally adjusted UK payrolled employees early estimate for June 2026, in millions, first print only. The ledger source URL is the ONS June 2026 bulletin even though that page is already the May 2026 data release; the official next-release date for the dataset is 21 July 2026, so I keep the registered target but flag the URL-period discrepancy."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS June 2026 PAYE RTI bulletin and release header.","result":"Fetched release date 18 June 2026, next release 21 July 2026, May 2026 payrolled employees 30.3 million, May month change +2,000, May annual change -119,000."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS June 2026 PAYE RTI payrolled-employees section and main points.","result":"Fetched April 2026 growth revised from -100,000 to -53,000; May 2026 was +2,000 month on month; May 2026 annual percentage change was -0.4%."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS May 2026 PAYE RTI bulletin for the prior flash and recent reference points.","result":"Fetched April 2026 early estimate 30.2 million, April flash month change -100,000, April annual change -210,000, and March 2026 revised month change -28,000."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS seasonally adjusted dataset and revision triangle pages to verify schedule and source variant.","result":"Fetched seasonally adjusted dataset release date 18 June 2026, next release 21 July 2026, data coverage July 2014 to May 2026, and revision triangle next release 21 July 2026."},{"kind":"text","text":"Variant consistency: all anchors are the same ONS/HMRC PAYE RTI payrolled employees, seasonally adjusted, UK series used in the bulletin figure/table, not non-seasonally adjusted or regional/sector breakdowns."},{"kind":"text","text":"Reference class and base rate: recent month-to-month first/recent print changes around the target are March -28,000, April -53,000 after revision, and May +2,000. The base rate is a soft labour-market drift of roughly -25,000 to -30,000 per month, but May's flat print and April's upward revision argue against extrapolating the April flash shock one-for-one."},{"kind":"math","text":"Prior/update/interval: persistence prior is May 2026 level 30.300 million; historical sample for successive changes is [-0.028, -0.053, 0.002] million from recent ONS prints; adjustment components are level 30.300 plus momentum -0.026 million, softened by May stabilization and early-tax-year upward revision risk to -0.020 million, giving point 30.280 million. For interval, sigma = 0.0275 million from those successive changes; 1.28*sigma = 0.035 million. I widen to 0.055 million, about 1.6x, because ONS states early tax-year flash estimates have greater uncertainty and only about 85% of information is available initially, versus 98% to 99% next month. Final implied bounds: 30.280 - 0.055 = 30.225 and 30.280 + 0.055 = 30.335 million."},{"kind":"text","text":"Upside risk: a continued payrolling rebound after April revisions, especially if administrative and support services strength persists, would land above the interval. Downside risk: renewed job cuts in accommodation, retail, or small employers after wage and employer-cost pressure would land below the interval. Outside the interval would require a June move materially larger than roughly +/-55,000 from the adjusted May base."},{"kind":"forecast","point":30.28,"ciLow":30.225,"ciHigh":30.335}]}

# Reviewer critique
{"summary":"Draft is publishable with minor warnings: it handles the ledger/source discrepancy transparently and keeps units, point, interval, and first-print rule coherent.","requiredFixes":[{"rubricItem":"model_prior","severity":"warning","summary":"The model prior is effectively a persistence-plus-three-month momentum rule, but it does not explicitly say whether a broader time-series model was considered or ruled out.","actionRequested":"Add one sentence that either labels the persistence/momentum calculation as the chosen time-series prior or states why no broader model was used."},{"rubricItem":"interval","severity":"warning","summary":"The interval uses only three recent monthly changes for sigma, which is a very small realized-volatility sample even though it is widened for flash uncertainty.","actionRequested":"Either justify the three-observation volatility sample as intentionally local to the current labour-market regime or add a broader historical volatility anchor if available."}],"optionalSuggestions":["State explicitly that the JSON `resolutionDate` of 2026-07-21 is the expected first-print publication date despite the retained ledger URL discrepancy.","The upside/downside tails are useful; tying them to approximate monthly changes in thousands would make them easier to audit."]}

Emit the final JSON object only.
