# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statcan.employment_insurance.regular_beneficiaries
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-ei-regular-beneficiaries-july-2026"
- country: "CA"
- targetUnit: "thousands"
- dataPointId: "statcan.employment_insurance.regular_beneficiaries.canada.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-09-24", "start": "2026-09-16"}, "field": "v64549350", "releasePolicy": "first_print", "sourceSeriesId": "v64549350", "sourceUrl": "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=64549350", "table": "Statistics Canada Table 14-10-0011-01, EI regular beneficiaries, Canada, seasonally adjusted (persons)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-f79e329aa4df0ee4abe1cc340829573fdfb069213c3fd3a6d4d5dbdec932cb40.json"
- targetContentHash: "f79e329aa4df0ee4abe1cc340829573fdfb069213c3fd3a6d4d5dbdec932cb40"
- registrationCommit: "464d182153273b99932d1049c8c2b2039b6a9eba"
- registeredAtUtc: "2026-07-11T01:30:29Z"

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
{"slug":"canada-ei-regular-beneficiaries-july-2026","country":"CA","type":"data","title":"Canada EI regular beneficiaries, July 2026","question":"What will Statistics Canada first report for the number of regular Employment Insurance beneficiaries in Canada in July 2026, seasonally adjusted, in thousands of persons?","unit":"thousands","pointEstimate":529.0,"ciLow":521.7,"ciHigh":536.3,"confidence":0.8,"resolutionDate":"2026-09-17","resolutionSource":"Statistics Canada Table 14-10-0011-01","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=64549350","resolutionRule":"Resolve to the first Statistics Canada publication for July 2026 of vector v64549350 in Table 14-10-0011-01: regular Employment Insurance beneficiaries, Canada, both sexes, age 15 years and over, seasonally adjusted, persons. Multiply the first-published persons value by 0.001 to express thousands. Ignore all subsequent revisions or corrections and apply no release-day grace exception.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.july_2026.first_print","historicalContext":[{"label":"December 2025","value":567.62},{"label":"January 2026","value":559.02},{"label":"February 2026","value":550.35},{"label":"March 2026","value":547.44},{"label":"April 2026","value":544.44},{"label":"July 2025","value":551.87}],"drivers":["Recent EI-beneficiary downtrend","May and June labour-market improvement","Lagged eligibility and benefit exhaustion","Possible July occupational composition rebound"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260710/dq260710a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/250918/dq250918a-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf"],"runAt":"2026-07-11T01:33:19Z","reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries for July 2026"},{"kind":"text","text":"The target is the first July 2026 print for Statistics Canada vector v64549350 in Table 14-10-0011-01: Canada, regular benefits, both sexes, age 15 years and over, seasonally adjusted persons. The ledger conversion to thousands is persons × 0.001; later revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest Canada observations from Statistics Canada Table 14-10-0011-01.","result":"The official seasonally adjusted series was 567.62 thousand in December 2025, 559.02 thousand in January 2026, 550.35 thousand in February, 547.44 thousand in March, and 544.44 thousand in April."},{"kind":"tool","tool":"official.release","call":"Fetched Statistics Canada's April 2026 Employment Insurance release.","result":"The April first release reported 544.44 thousand regular beneficiaries, down 3.00 thousand or 0.5% from revised March; the 12-month change was +3.5%."},{"kind":"tool","tool":"official.reference_class","call":"Fetched Statistics Canada's July 2025 Employment Insurance release as a same-month reference class observation.","result":"July 2025 registered 551.87 thousand beneficiaries, a monthly increase of 6.60 thousand or 1.2%; December 2024 to July 2025 rose 64.00 thousand or 13.2%."},{"kind":"text","text":"The outside-view base rate is recent persistence: four successive monthly changes from December 2025 through April 2026 were -8.60, -8.67, -2.91, and -3.00 thousand, averaging -5.80 thousand. Applying that mean for three months gives a raw July level of 544.44 - 3×5.80 = 527.04 thousand."},{"kind":"tool","tool":"official.lookup","call":"Fetched the June 2026 Labour Force Survey for current labour-market momentum.","result":"Employment increased 88,000 or 0.4% in May and 18,000 or 0.1% in June; unemployment fell from 6.9% in April to 6.6% in May and 6.5% in June, while June's job-finding rate was 24.3% and layoff rate 0.6%."},{"kind":"text","text":"Level is anchored at April's 544.44 thousand. Momentum is downward because employment strengthened and unemployment declined in May and June. The one-off adjustment is +2.0 thousand relative to the raw trend because July 2025 showed a 6.6-thousand increase concentrated in occupational composition, while the policy mechanism remains lagged: EI entry, return to work, benefit exhaustion, and eligibility need not move contemporaneously with the LFS."},{"kind":"math","text":"Prior/update/interval: The model is a three-step average-change persistence prior using the December 2025-April 2026 official history. Baseline = 544.44 + 3×(-5.80) = 527.04 thousand; adjustment components are +2.0 thousand for July composition/lag effects and approximately 0 for policy changes, giving 529.0 thousand. The sample standard deviation of the four successive changes (-8.60, -8.67, -2.91, -3.00) is sigma = 3.3 thousand. For a three-month horizon, the 80% half-width is 1.28×sigma×sqrt(3) = 1.28×3.3×1.732 = 7.3 thousand, implying 529.0±7.3 = 521.7 to 536.3 thousand."},{"kind":"text","text":"Upside risk comes from renewed layoffs, particularly in manufacturing, or another education-related July composition jump and would land above the interval. Downside risk comes from faster job finding, benefit exhaustion, or delayed claims entry and could land below the interval. A sharp administrative or eligibility change would also place the result outside the interval."},{"kind":"tool","tool":"official.calendar","call":"Checked Statistics Canada's official 2026 release-date publication for Employment Insurance.","result":"The official calendar lists Employment Insurance for September 17, 2026; the ledger's expected window is September 16-24, so resolution is set to 2026-09-17."},{"kind":"forecast","point":529.0,"ciLow":521.7,"ciHigh":536.3}]}

# Reviewer critique
{"summary":"The draft is publishable with no blocking issues; the main weakness is that the interval is based on a very short four-change volatility sample.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval uses the sample standard deviation of only four recent monthly changes, all from the same downtrend regime, so the realized-volatility basis may understate wider historical or seasonal risk.","actionRequested":"Either justify why the December 2025-April 2026 four-change sample is the intended volatility sample, or widen/support the interval with a longer historical monthly-change reference class."}],"optionalSuggestions":["Name the official 2026 StatCan release-calendar source more specifically in the reasoning, since the resolution date is a key contract field.","Make the +2.0 thousand July composition/lag adjustment slightly more explicit by separating same-month seasonal/composition evidence from EI-flow lag evidence."]}

Emit the final JSON object only.
