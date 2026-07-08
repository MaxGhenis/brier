# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.epop_persons_with_disability
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-disability-employment-population-ratio-july-2026"
- targetUnit: "percent"

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
{"slug":"us-disability-employment-population-ratio-july-2026","country":"US","type":"data","title":"Disability employment-population ratio, July 2026","question":"What will BLS first report for the not seasonally adjusted employment-population ratio for people with a disability, 16 years and over, in July 2026?","unit":"percent","pointEstimate":21.6,"ciLow":20.9,"ciHigh":22.3,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-6","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.t06.htm","resolutionRule":"Resolves to the first BLS Employment Situation Table A-6 print for July 2026, employment-population ratio for people with a disability, total 16 years and over, not seasonally adjusted, in percent, rounded to one decimal. Later revisions or historical database updates do not change resolution.","dataPointId":"bls.cps.LNU02374597.2026-07.first_print","historicalContext":[{"label":"Feb 2026","value":22.4},{"label":"Mar 2026","value":22.2},{"label":"Apr 2026","value":21.8},{"label":"May 2026","value":21.7},{"label":"Jun 2026","value":21.8}],"drivers":["Recent disability EPOP drift lower in early 2026","July non-seasonally-adjusted month effect usually slightly negative from June","Soft June labor market and lower overall participation","High month-to-month CPS sampling noise for disability subgroup"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/news.release/empsit.t06.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/data/LNU02374597"],"runAt":"2026-07-08T20:27:06Z","reasoning":[{"kind":"heading","text":"July 2026 disability employment-population ratio"},{"kind":"text","text":"Framing and exact resolver: this forecast targets BLS CPS series LNU02374597, Employment-Population Ratio - With a Disability, 16 Years and over, not seasonally adjusted, as printed in Employment Situation Table A-6 for July 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS release schedule lookup for Employment Situation July 2026 reference month","result":"BLS schedule lists July 2026 Employment Situation release date as Aug. 07, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation Table A-6 June 2026 latest official table","result":"Table A-6 shows total people with a disability employment-population ratio of 22.7 in June 2025 and 21.8 in June 2026; employed people with a disability were 8,081 thousand in June 2025 and 8,054 thousand in June 2026."},{"kind":"tool","tool":"history.lookup","call":"FRED mirror of BLS LNU02374597 recent monthly observations","result":"LNU02374597 values fetched: Feb 2026 22.4, Mar 2026 22.2, Apr 2026 21.8, May 2026 21.7, Jun 2026 21.8; units percent, not seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"BLS June 2026 Employment Situation labor-market context","result":"June 2026 nonfarm payrolls were +57,000, unemployment rate was 4.2 percent, labor force participation decreased 0.3 percentage point to 61.5 percent, and overall employment-population ratio edged down 0.2 percentage point to 59.0 percent."},{"kind":"text","text":"Reference class and base rate: for this not seasonally adjusted level series, persistence from the latest print is the base rate. The July target uses the same variant as the anchors: total people with a disability, age 16 years and over, not seasonally adjusted, percent."},{"kind":"math","text":"Prior/update/interval: persistence prior is Jun 2026 at 21.8. Historical sample is monthly LNU02374597 values from Jan 2024 through Jun 2026, excluding the missing Oct 2025 observation; successive-change dispersion gives sigma = 0.528 percentage point, so 1.28*sigma = 0.676. Adjustment components are -0.1 point for recent 2026 downward level drift, -0.1 point for typical Jun-to-Jul NSA softness, and 0.0 point for mixed labor-market context, implying 21.8 - 0.2 = 21.6. The 80% interval is 21.6 +/- 0.7, rounded to [20.9, 22.3]."},{"kind":"text","text":"Momentum: the series moved 22.6, 22.4, 22.2, 21.8, 21.7, 21.8 from Jan through Jun 2026, so the latest uptick is small relative to the earlier slide and does not fully erase the weaker level."},{"kind":"text","text":"Counter-consideration: upside risk is a rebound in disability labor-force attachment or CPS sampling that would land above the interval, roughly 22.4 or higher; downside risk is another broad participation drop or subgroup sampling swing that would land below the interval, roughly 20.8 or lower."},{"kind":"forecast","point":21.6,"ciLow":20.9,"ciHigh":22.3}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; resolver, unit, first-print rule, prior/update math, interval, tails, and JSON fields are broadly coherent.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolver uses the rolling BLS Table A-6 URL, which will later point to newer Employment Situation releases even though the rule says first print.","actionRequested":"Add an archived/first-print provenance note or state that resolution should capture the Aug. 7, 2026 first-print Table A-6 artifact when released, while retaining the ledger target."},{"rubricItem":"base_rate","severity":"warning","summary":"The persistence prior is present but appears after current-evidence tool notes and drivers, weakening the required prior-before-update structure.","actionRequested":"Reorder the reasoning so the June 2026 persistence prior of 21.8 is stated before the drift, July seasonality, and labor-market context updates."}],"optionalSuggestions":["Briefly cite the historical Jun-to-Jul NSA effect used for the -0.1 adjustment, since the current text names it but does not quantify the sample.","Mention that FRED is used only as a history mirror, not as the final resolution source."]}

Emit the final JSON object only.
