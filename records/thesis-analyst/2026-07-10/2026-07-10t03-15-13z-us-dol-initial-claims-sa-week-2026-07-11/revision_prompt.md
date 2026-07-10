# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-11"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US initial claims, week ending July 11","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial unemployment claims for the week ending July 11, 2026, in the first print?","unit":"thousands","pointEstimate":216,"ciLow":204,"ciHigh":228,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260716","resolutionRule":"Resolve to the advance seasonally adjusted initial claims figure for the week ending July 11, 2026, reported in the first U.S. Department of Labor Unemployment Insurance Weekly Claims release issued for that week, in thousands of claims. Use the first print only; do not incorporate later revisions, corrected later vintages, or FRED/ALFRED revisions. If the exact newsroom URL differs, use the DOL UI Weekly Claims release/archive for the July 16, 2026 release.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"2026-07-04 advance SA initial claims","value":215},{"label":"2026-06-27 advance SA initial claims","value":215},{"label":"2026-06-20 advance SA initial claims","value":215},{"label":"2026-06-13 advance SA initial claims","value":226},{"label":"2026-06-06 advance SA initial claims","value":229},{"label":"2026-07-04 SA 4-week average","value":218.75}],"drivers":["latest advance SA print held at 215 thousand","four-week average near 219 thousand","late-June pullback from the early-June 229 thousand local high","holiday and auto-retooling seasonal residual risk around early July","continued claims rate steady at 1.2 percent"],"sourceContext":["https://oui.doleta.gov/unemploy/claims_arch.asp","https://www.dol.gov/newsroom/releases/eta","https://www.dol.gov/newsroom/releases/eta/eta20260709","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA"],"runAt":"2026-07-10T03:15:36Z","reasoning":[{"kind":"heading","text":"US advance seasonally adjusted initial claims for week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this is the DOL Employment and Training Administration advance seasonally adjusted initial claims series, ICSA-equivalent, for the week ending July 11, 2026, in thousands, resolved on the first official DOL weekly claims release and not from later revised vintages."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL Office of Unemployment Insurance claims archive publication schedule.","result":"The archive page says the UI Weekly Claims News Release is published each week Thursday morning at 8:30 AM EST, lists Wednesday November 25, 2026 at 8:30 AM EST as the only non-Thursday exception shown, and was updated July 9, 2026; for the week ending Saturday July 11, 2026, the scheduled Thursday release date is July 16, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the July 9, 2026 DOL UI Weekly Claims release for the latest official print.","result":"For week ending July 4, 2026, advance seasonally adjusted initial claims were 215,000, down 2,000 from the previous week's revised 217,000; the 4-week moving average was 218,750, down 3,750; advance insured unemployment for week ending June 27 was 1,814,000 and the insured unemployment rate was 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read recent DOL ETA weekly claims release snippets on the DOL newsroom releases page for same-variant advance SA initial claims.","result":"Recent advance SA first prints were: July 4 215,000; June 27 215,000; June 20 215,000; June 13 226,000; June 6 229,000; May 30 225,000; May 23 215,000; May 16 209,000; May 9 211,000; May 2 200,000; April 25 189,000."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest DOL PDF table for same-release context and prior-year comparison.","result":"The July 9 release table labeled Seasonally Adjusted Data shows Initial Claims (SA) 215,000 for July 4, 217,000 for June 27, change -2,000, June 20 at 216,000, and prior-year comparable week 228,000; the same table shows Initial Claims (NSA) 224,583 for July 4 and 214,616 for June 27."},{"kind":"text","text":"Base rate/reference class: for the same advance SA variant, the near-term reference class is weekly first prints from late April through early July 2026, which moved from 189 thousand to 229 thousand before flattening at 215 thousand for three straight advance prints."},{"kind":"text","text":"Level and momentum: the latest level is 215 thousand, the latest DOL 4-week average is 218.75 thousand, and the local momentum has cooled from early-June highs of 229 thousand and 226 thousand to the mid-210s. A pure persistence forecast is 215, while a 4-week-average pull is about 219."},{"kind":"text","text":"Mechanism adjustment: early July can be noisy because holiday timing and auto-plant retooling interact with seasonal factors, but the SA series already adjusts for normal July layoffs. I give only a small upward adjustment from persistence because the last three advance readings are flat at 215 thousand and continuing-claims context is not signaling a sharp layoff break."},{"kind":"math","text":"Prior/update/interval: persistence prior = 215 from the latest advance SA first print; historical sample = the last 11 fetched advance SA first prints in thousands, 189, 200, 211, 209, 215, 225, 229, 226, 215, 215, 215; adjustment components = +2 toward the 218.75 four-week average, -1 for the late-June downshift, +0 holiday residual after seasonal adjustment, giving point 216. Weekly changes in the fetched sample are +11, +11, -2, +6, +10, +4, -3, -11, 0, 0, so sigma = 7.2 thousand and 1.28*sigma = 9.2 thousand; I widen to a 12 thousand half-width, within 1.75x, because early-July seasonal residuals can create larger one-week misses, yielding 204 to 228."},{"kind":"text","text":"Counter-consideration: upside risk is a seasonal-adjustment miss or state-level layoff spike that would push the first print above 228 thousand; downside risk is another broad decline in filings after the June pullback that would land below 204 thousand. Outside the interval would require a move larger than the recent ordinary week-to-week dispersion, not just another 215 thousand plateau print."},{"kind":"forecast","point":216,"ciLow":204,"ciHigh":228}]}

# Reviewer critique
{"summary":"The draft is publishable with one minor source-binding clarification: its resolver is precise, prior/update/interval are explicit, and point/interval/JSON fields are coherent.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The draft resolves from the DOL first-print release, while the ledger sourceBinding names the ALFRED-FRED ICSA CSV with an advance-vintage policy and DOL as an allowed host.","actionRequested":"Clarify in reasoning that the DOL first-print release is the authoritative first-print source and that ALFRED/FRED is only a bound adapter or mirror for the same ICSA value, not a later-revision resolver."}],"optionalSuggestions":["State explicitly that 216, 204, and 228 are all in thousands to remove any residual unit ambiguity.","The interval method is good; consider naming it as an approximately 80% interval since confidence is 0.8."]}

Emit the final JSON object only.
