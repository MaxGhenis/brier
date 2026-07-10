# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.disposable_personal_income.level
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-disposable-personal-income-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.disposable_personal_income.level.june_2026.first_print"
- resolutionDate: "2026-07-30"
- resolutionSource: "ALFRED DSPI CSV source binding for BEA disposable personal income first print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25"
- resolutionRule: "Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "DSPI", "releasePolicy": "first_print", "sourceSeriesId": "DSPI", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3.json"
- targetContentHash: "123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3"
- registrationCommit: "0d80683b051be25572f40ea4731fa5062af6d211"
- registeredAtUtc: "2026-07-10T12:36:34Z"

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

# Threshold-ladder elicitation (promptMode ladder)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every fast-mode requirement above (sigma arithmetic, base rate, upside/downside/outside-the-interval risks). In the Prior/update/interval step, also state how the ladder-implied 80% width compares to the 1.28*sigma width.
- Add this top-level field to the cell JSON, with your actual rungs as two equal-length numeric arrays:
{
  "thresholdLadder": {
    "thresholds": [
      "strictly increasing numeric rungs"
    ],
    "cumulativeProbabilities": [
      "non-decreasing, within [0.01, 0.99]"
    ]
  }
}


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
{"slug":"bea-disposable-personal-income-level-june-2026","country":"US","type":"data","title":"US disposable personal income, June 2026","question":"BEA disposable personal income (DSPI / account code A067RC), June 2026, billions of dollars at a seasonally adjusted annual rate, first print.","unit":"usd_billions","pointEstimate":23730.0,"ciLow":23606.5,"ciHigh":23853.5,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"BEA Personal Income and Outlays, Table 2.6 (DSPI / account code A067RC), first release","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25","resolutionRule":"Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding.","dataPointId":"bea.disposable_personal_income.level.june_2026.first_print","historicalContext":[{"label":"January 2026 DSPI","value":23395.9},{"label":"February 2026 DSPI","value":23382.4},{"label":"March 2026 DSPI","value":23510.4},{"label":"April 2026 DSPI","value":23486.9},{"label":"May 2026 DSPI","value":23651.7}],"drivers":["May's unusually large farm-payment contribution should fade","June payroll and wage growth support a continued nominal-income gain","Personal-current-tax and transfer-receipt movements remain the main residual uncertainty"],"sourceContext":["https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026","https://www.bea.gov/news/schedule/full","https://fred.stlouisfed.org/series/DSPI","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-10T15:31:54Z","reasoning":[{"kind":"heading","text":"June 2026 BEA disposable personal income first-print forecast"},{"kind":"text","text":"The target is current-dollar disposable personal income, BEA Table 2.6 line 27 / account code A067RC, in billions of dollars at a seasonally adjusted annual rate. The official BEA schedule verifies that Personal Income and Outlays for June 2026 is scheduled for July 30, 2026 at 8:30 a.m. EDT. The retained ledger resolver uses an ALFRED DSPI URL whose 2026-06-25 vintage is the prior May print; I retain that binding and its strict first_print, no-later-revisions rule."},{"kind":"tool","tool":"history.lookup","call":"Fetched the DSPI history mirror for the BEA series, using the same monthly SAAR current-dollar variant as the target.","result":"FRED, sourced to BEA and identifying account code A067RC, reports DSPI of 23,395.9 in Jan 2026, 23,382.4 in Feb, 23,510.4 in Mar, 23,486.9 in Apr, and 23,651.7 billion dollars SAAR in May."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest official BEA Personal Income and Outlays release and its Table 2.6-linked figures.","result":"BEA's May release reports DPI increased $164.9 billion (0.7 percent) in May; its release table reports May DSPI 23,651.7, April 23,486.9, May personal income 26,916.4, and May personal saving 704.2 billion dollars SAAR."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official BLS June Employment Situation as a contemporaneous input to June wage income.","result":"BLS reports June nonfarm payroll employment rose 57,000, private average hourly earnings rose $0.13 (0.3 percent) to $37.64, aggregate weekly payrolls rose 0.4 percent, and the unemployment rate was 4.2 percent."},{"kind":"text","text":"The reference class/base rate is the latest four successive monthly DSPI changes: -13.5, +128.0, -23.5, and +164.8 billion dollars SAAR. May's large gain reflected farm proprietors' income and a second round of USDA Supplemental Disaster Relief Program payments, an explicitly identified one-off component rather than a stable monthly trend."},{"kind":"math","text":"Prior/update/interval: I use a persistence-plus-mean-change prior from the Jan-May 2026 same-variant DSPI history. The four successive changes have mean +63.95 and sample sigma = 96.5 billion; 1.28*sigma = 123.5 billion. Starting at May's 23,651.7, the prior implies 23,715.7. I add about 14.3 for June's positive wage/payroll signal, but do not carry forward May's farm-payment surge, giving 23,730.0. The 80% interval is 23,730.0 +/- 123.5 = [23,606.5, 23,853.5], exactly the historical-dispersion width."},{"kind":"text","text":"Counter-consideration: upside risk is a further large farm-payment or transfer-receipt increase, or unexpectedly low personal current taxes, which could put June DSPI above 23,853.5. Downside risk is a sharper reversal of farm proprietors' income, weaker compensation, or higher taxes; a combined reversal would land below 23,606.5 and outside the interval."},{"kind":"forecast","point":23730.0,"ciLow":23606.5,"ciHigh":23853.5}]}

# Reviewer critique
{"summary":"The forecast is internally coherent and evidence-based, but it needs source-contract and ordering corrections before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft's `resolutionSource` names “BEA Personal Income and Outlays, Table 2.6,” which does not match the canonical ledger resolver text/source binding (ALFRED DSPI CSV, Table 1); the target description also calls the measure Table 2.6 line 27 without reconciling that discrepancy.","actionRequested":"Set `resolutionSource` exactly to the canonical ledger source description, retain the supplied ALFRED URL/rule unchanged, and remove or explicitly qualify unsupported Table 2.6 references."},{"rubricItem":"base_rate","severity":"warning","summary":"The base-rate/persistence prior is stated only after the BEA and BLS inside-view evidence.","actionRequested":"Reorder the reasoning so the historical reference class, mean-change prior, and model/dispersion assumptions appear before contemporary evidence and its adjustment."},{"rubricItem":"interval","severity":"warning","summary":"The interval is mechanically calculated from realized monthly-change dispersion, but it relies on only four changes and does not acknowledge the resulting estimation uncertainty.","actionRequested":"State that the four-change sample is sparse and explain why the chosen 80% normal-width interval remains appropriate, or use a broader explicitly justified uncertainty method."}],"optionalSuggestions":["Explain how the June payroll signal maps quantitatively to the +$14.3 billion adjustment.","Use the canonical resolver terminology consistently in the title/question context as well as the JSON resolver fields."]}

Emit the final JSON object only.
