# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.ppi.final_demand_monthly_change
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-ppi-final-demand-monthly-change-june-2026"
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
{"slug":"bls-ppi-final-demand-monthly-change-june-2026","country":"US","type":"data","title":"US PPI Final Demand Monthly Change, June 2026","question":"What will the first-print seasonally adjusted monthly percent change be for the BLS Producer Price Index for final demand in June 2026?","unit":"percent_growth","pointEstimate":0.7,"ciLow":0.2,"ciHigh":1.2,"confidence":0.8,"resolutionDate":"2026-07-15","resolutionSource":"U.S. Bureau of Labor Statistics Producer Price Index news release","resolutionSourceUrl":"https://www.bls.gov/news.release/ppi.nr0.htm","resolutionRule":"Resolve to the first-print seasonally adjusted month-over-month percent change for the Producer Price Index for final demand for June 2026 as reported in the BLS Producer Price Indexes news release released on July 15, 2026. Use the rounded one-decimal percent value in the release text or Table A; ignore later revisions.","dataPointId":"bls.wp.WPSFD4.2026-06.first_print","historicalContext":[{"label":"2026-05 final demand m/m SA","value":1.1},{"label":"2026-04 final demand m/m SA","value":1.1},{"label":"2026-03 final demand m/m SA","value":0.7},{"label":"2026-02 final demand m/m SA","value":0.5},{"label":"2026-01 final demand m/m SA","value":0.6},{"label":"2025-12 final demand m/m SA","value":0.4}],"drivers":["April-May headline PPI persistence was very strong at 1.1 percent in both months","May final demand goods rose 2.8 percent and energy rose 10.7 percent","Services inflation slowed to 0.3 percent, limiting full carry-through","Reference-class mean for May 2025-May 2026 final demand monthly changes was 0.51 percent","Energy and gasoline shock likely persists partly into June but mean-reverts from May's jump"],"sourceContext":["https://www.bls.gov/schedule/news_release/ppi.htm","https://www.bls.gov/news.release/ppi.nr0.htm","https://download.bls.gov/pub/time.series/wp/wp.item","https://download.bls.gov/pub/time.series/wp/wp.series"],"runAt":"2026-07-08T02:56:23Z","thresholdLadder":{"thresholds":[-0.4,-0.2,0,0.2,0.4,0.5,0.7,0.8,1,1.2,1.4,1.6],"cumulativeProbabilities":[0.03,0.06,0.08,0.1,0.24,0.35,0.5,0.6,0.76,0.9,0.96,0.98]},"reasoning":[{"kind":"heading","text":"Forecast for June 2026 BLS PPI Final Demand"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS Producer Price Index for final demand, seasonally adjusted, month-over-month percent change for June 2026, resolved on the first official print in the Producer Price Index news release. The variant is the headline final demand SA monthly percent change, not NSA 12-month change, not core, and not final demand goods or services."},{"kind":"tool","tool":"official.lookup","call":"BLS Producer Price Index release schedule lookup for the June 2026 reference month","result":"Fetched official schedule: reference month June 2026, release date Jul. 15, 2026, release time 08:30 AM; May 2026 was released Jun. 11, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS current PPI news release headline and recent monthly total final demand values","result":"Fetched BLS May 2026 release: final demand rose 1.1 percent in May, 1.1 percent in April, and 0.7 percent in March; unadjusted 12-month final demand change was 6.5 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS Table A reference class for total final demand monthly percent changes","result":"Fetched total final demand monthly changes: 2025 May 0.3, Jun 0.2, Jul 0.8, Aug -0.2, Sep 0.6, Oct 0.1, Nov 0.4, Dec 0.4, 2026 Jan 0.6, Feb 0.5, Mar 0.7, Apr 1.1, May 1.1."},{"kind":"tool","tool":"official.lookup","call":"BLS Table A component context for May 2026 final demand","result":"Fetched May 2026 components: final demand goods 2.8 percent, final demand foods 0.6 percent, final demand energy 10.7 percent, final demand goods less foods and energy 0.8 percent, final demand services 0.3 percent, final demand less foods, energy, and trade services 0.8 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS item and series metadata check for target identity","result":"Fetched BLS metadata: WP item code 4 is Final demand; series WPSFD4 is the seasonally adjusted final-demand PPI series, with metadata current through 2026 M05."},{"kind":"text","text":"Base rate and reference class: the outside-view anchor is the May 2025-May 2026 BLS Table A sample of headline final-demand monthly changes, with mean 0.51 percent, before updating for the latest two 1.1 percent prints and component mix."},{"kind":"text","text":"Current-release update: the two-month headline run rate argues above the base rate, but May's goods shock was heavily energy and gasoline driven, so I do not carry the full April-May pace into June."},{"kind":"text","text":"Level, momentum, one-off, and policy-mechanism split: level is elevated because the 12-month final demand change reached 6.5 percent; momentum is strong in headline and core-ex-trade; the main one-off is May gasoline and energy; monetary-policy pressure is more likely to restrain future demand than the first June input-cost print."},{"kind":"math","text":"Ladder: P(X <= -0.4) = 0.03; P(X <= -0.2) = 0.06; P(X <= 0.0) = 0.08; P(X <= 0.2) = 0.10; P(X <= 0.4) = 0.24; P(X <= 0.5) = 0.35; P(X <= 0.7) = 0.50; P(X <= 0.8) = 0.60; P(X <= 1.0) = 0.76; P(X <= 1.2) = 0.90; P(X <= 1.4) = 0.96; P(X <= 1.6) = 0.98. Linear interpolation gives p10 = 0.2, p50 = 0.7, and p90 = 1.2, rounded to one decimal."},{"kind":"math","text":"Prior/update/interval: model is a 13-month historical base-rate plus two-month persistence prior. Historical sample is BLS Table A May 2025-May 2026 total final demand values [0.3, 0.2, 0.8, -0.2, 0.6, 0.1, 0.4, 0.4, 0.6, 0.5, 0.7, 1.1, 1.1], mean = 0.51 and sigma = 0.37. Adjustment components: +0.20 for April-May persistence and broad goods/core firmness, -0.05 for expected partial energy/gasoline mean reversion, +0.04 for services/core carry-through, giving 0.70. 80% interval method: values themselves are the change-series dispersion, so 80% half-width is roughly 1.28*sigma = 1.28*0.37 = 0.47; the ladder-implied half-width is about 0.5, effectively the same after one-decimal rounding, with final implied bounds 0.2 and 1.2."},{"kind":"text","text":"Counter-consideration: upside risk is another large June energy or gasoline pass-through plus firm portfolio-management and transportation services, which would land above the interval if headline final demand prints above 1.2 percent. Downside risk is a sharp reversal in gasoline, crude, or trade-service margins, which would land below the interval if headline final demand prints below 0.2 percent."},{"kind":"forecast","point":0.7,"ciLow":0.2,"ciHigh":1.2}]}

# Reviewer critique
{"summary":"Draft is publication-ready with no blocking issues; it clearly defines the BLS first-print resolver, uses an outside-view prior, explains updates, derives an 80% interval, and keeps point/interval/JSON fields coherent.","requiredFixes":[],"optionalSuggestions":["Consider naming the official schedule URL directly in the resolver evidence, since ppi.nr0.htm is mutable after later releases.","The historical sample is short at 13 months; noting why longer pre-2025 volatility was not used would make the interval rationale stronger."]}

Emit the final JSON object only.
