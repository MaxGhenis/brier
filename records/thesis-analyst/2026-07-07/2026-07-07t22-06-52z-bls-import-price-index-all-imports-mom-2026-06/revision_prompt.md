# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.import_price_index.all_imports_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-import-price-index-all-imports-mom-june-2026"
- targetUnit: "percent_growth"

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"bls-import-price-index-all-imports-mom-june-2026","country":"US","type":"data","title":"US import prices MoM, Jun 2026","question":"BLS U.S. Import Price Index for all imports, all commodities, seasonally unadjusted monthly percent change for June 2026, first print","unit":"percent_growth","pointEstimate":1.1,"ciLow":0,"ciHigh":2.2,"confidence":0.8,"resolutionDate":"2026-07-17","resolutionSource":"U.S. Bureau of Labor Statistics U.S. Import and Export Price Indexes","resolutionSourceUrl":"https://www.bls.gov/news.release/ximpim.t01.htm","resolutionRule":"Resolve to the first-published BLS U.S. Import Price Indexes Table 1 value for All commodities, monthly percent change from May 2026 to June 2026, in percent rounded to one decimal as published. Ignore later revisions; if Table 1 and the release summary disagree, use the first-print Table 1 All commodities monthly percent change.","dataPointId":"bls.import_price_index.all_imports_mom.2026-06.first_print","historicalContext":[{"label":"2026-05 all imports MoM first/current release table","value":1.9},{"label":"2026-04 all imports MoM revised in May release","value":2},{"label":"2026-03 all imports MoM revised in May release","value":0.9},{"label":"2026-02 all imports MoM","value":1},{"label":"2026-01 all imports MoM","value":0.5}],"drivers":["fuel-import surge likely cools but remains supportive","nonfuel import prices running firm","recent all-imports momentum well above 2025 base rate","June forecast resolves before later revisions"],"sourceContext":["https://www.bls.gov/news.release/ximpim.nr0.htm","https://www.bls.gov/news.release/ximpim.t01.htm","https://www.bls.gov/schedule/news_release/ximpim.htm"],"runAt":"2026-07-07T22:07:42Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 BLS all-import import-price MoM"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS Import/Export Price Indexes first print for June 2026, Table 1 All commodities monthly percent change, which is the all-imports end-use aggregate. The release is not seasonally adjusted in this table, and the target uses the first-published one-decimal percent change, not later revised values."},{"kind":"tool","tool":"official.calendar","call":"Opened BLS schedule page for U.S. Import and Export Price Indexes release dates.","result":"BLS schedule lists Reference Month June 2026, Release Date Jul. 17, 2026, Release Time 08:30 AM; it also lists May 2026 released Jun. 16, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened current BLS U.S. Import and Export Price Indexes summary for May 2026.","result":"BLS reported U.S. import prices increased 1.9 percent in May 2026 after a 2.0 percent rise in April and a 0.9 percent increase in March; over the year May 2025 to May 2026, import prices rose 6.7 percent."},{"kind":"tool","tool":"official.table","call":"Opened BLS Table 1, U.S. import price indexes and percent changes for End Use categories of goods.","result":"Table 1 All commodities shows relative importance 100.000, April 2026 index 147.7, May 2026 index 150.5, annual change 6.7, and monthly changes 1.0 for Jan-Feb 2026, 0.9 for Feb-Mar 2026, 2.0 for Mar-Apr 2026, 1.9 for Apr-May 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS release text and Table A component detail for recent all-import, fuel, and nonfuel import prices.","result":"Table A all imports monthly values were -0.5 in May 2025, -0.1 in June 2025, 0.3 in July 2025, -0.1 in August 2025, -0.1 in September 2025, 0.1 in December 2025, 0.5 in January 2026, 1.0 in February 2026, 0.9 in March 2026, 2.0 in April 2026, and 1.9 in May 2026; fuel imports were 10.2 in March, 18.6 in April, and 12.5 in May, while nonfuel imports were 0.2 in March, 0.6 in April, and 0.8 in May."},{"kind":"tool","tool":"clock.lookup","call":"Fetched current UTC time for run timestamp after local date command was unavailable in the sandbox.","result":"UTC time fetched for this run was Jul. 7, 2026 at 22:07:42, formatted as 2026-07-07T22:07:42Z."},{"kind":"text","text":"The reference class and base rate are the available BLS Table A all-import monthly percent changes from May 2025 through May 2026, excluding unavailable October and November 2025 entries. The simple mean of those 11 fetched changes is about 0.54 percent, while the latest 3-month average is about 1.60 percent, so the current release environment is much hotter than the base rate."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the 11 available BLS Table A all-import MoM values [-0.5, -0.1, 0.3, -0.1, -0.1, 0.1, 0.5, 1.0, 0.9, 2.0, 1.9], whose mean is 0.54 and sample sigma = 0.83 for this change series; update components are +0.40 for recent momentum above the base rate, +0.25 for firm nonfuel import prices, and -0.10 for likely partial cooling after extreme fuel gains, giving 0.54 + 0.40 + 0.25 - 0.10 = 1.09, rounded to 1.1. The 80% half-width is roughly 1.28*sigma = 1.28*0.83 = 1.06, so 1.1 +/- 1.06 gives about 0.0 to 2.2 after one-decimal target rounding."},{"kind":"text","text":"Counter-considerations: upside risk is another large fuel-import increase or broader tariff/pass-through pressure that would land above the interval, especially if fuels again add double-digit monthly growth. Downside risk is a June reversal in petroleum or natural gas import prices, or a sudden weakening in nonfuel goods prices, which would land outside the interval below 0.0."},{"kind":"forecast","point":1.1,"ciLow":0,"ciHigh":2.2}]}

# Reviewer critique
{
  "summary": "Draft is publishable after minor clarifications; the main gaps are resolver-source mutability and making the model-prior/base-rate ordering explicit.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolver rule correctly names BLS Table 1 and first print, but the current-release URL is mutable and may later show a different reference month.",
      "actionRequested": "Add that resolution must use the July 17, 2026 first-published June 2026 BLS Table 1 snapshot/archive or captured first-print artifact, not whatever ximpim.t01.htm shows after later releases."
    },
    {
      "rubricItem": "base_rate",
      "severity": "warning",
      "summary": "The base-rate/persistence prior is present, but it appears after the current-evidence tool summaries rather than before inside-view updates.",
      "actionRequested": "Move or restate the 0.54 percent historical/base-rate prior before the momentum, fuel, and nonfuel evidence adjustments."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a simple persistence/base-rate prior and recent 3-month average, but does not explicitly say whether a formal time-series model was used or ruled out.",
      "actionRequested": "Add one sentence identifying the model prior as a simple historical/persistence model, or explicitly state that no AR/ETS/regression model was used because the usable first-print sample is short and disrupted by missing 2025 data."
    }
  ],
  "optionalSuggestions": [
    "Label the interval as an 80% interval derived from the 11-observation sample sigma so it matches confidence 0.8.",
    "Clarify that revised March/April values are acceptable as current historical context, while June itself resolves only to the first print."
  ]
}

Emit the final JSON object only.
