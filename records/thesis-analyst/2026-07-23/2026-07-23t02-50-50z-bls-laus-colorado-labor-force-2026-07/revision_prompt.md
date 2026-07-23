# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.laus.colorado.labor_force
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "colorado-labor-force-july-2026"
- targetUnit: "thousands"

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
{"slug":"colorado-labor-force-july-2026","country":"US","type":"data","title":"Colorado labor force, July 2026","question":"BLS Local Area Unemployment Statistics, Colorado civilian labor force, seasonally adjusted, July 2026, first print","unit":"thousands","pointEstimate":3182.2,"ciLow":3179.8,"ciHigh":3184.6,"confidence":0.8,"resolutionDate":"2026-08-21","resolutionSource":"U.S. Bureau of Labor Statistics State Employment and Unemployment, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/laus.t01.htm","resolutionRule":"Resolve to the first BLS State Employment and Unemployment Table 1 print for July 2026, Colorado row, seasonally adjusted civilian labor force. Use the BLS-published persons value for the July 2026 preliminary print, convert to thousands by dividing by 1,000, and round to one decimal thousand. Ignore later LAUS revisions, annual benchmark revisions, FRED mirror updates, and later archived revised tables.","dataPointId":"bls.laus.colorado.labor_force.2026-07.first_print","historicalContext":[{"label":"Jan 2026 Colorado labor force SA","value":3248.8},{"label":"Feb 2026 Colorado labor force SA","value":3238.5},{"label":"Mar 2026 Colorado labor force SA","value":3227.9},{"label":"Apr 2026 Colorado labor force SA","value":3215.6},{"label":"May 2026 Colorado labor force SA revised","value":3206.2},{"label":"Jun 2026 Colorado labor force SA preliminary","value":3193.3}],"drivers":["Colorado LAUS labor force has declined for five straight observed months","Recent seasonally adjusted monthly declines cluster around 9.4 to 12.9 thousand","July target is BLS LAUS Table 1 seasonally adjusted civilian labor force, not the not-seasonally-adjusted COLFN series","June unemployment rate stayed 3.9 percent, so the latest labor-force decline did not come from a visible unemployment-rate jump","First-print risk is dominated by state CPS sampling and LAUS model noise"],"sourceContext":["https://www.bls.gov/news.release/laus.t01.htm","https://www.bls.gov/eag/eag.co.htm","https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/news.release/empsit.a.htm"],"runAt":"2026-07-23T02:51:01Z","reasoning":[{"kind":"heading","text":"Forecast for Colorado July 2026 labor force"},{"kind":"text","text":"Framing and exact resolver: this target is the BLS LAUS Colorado civilian labor force, seasonally adjusted, for July 2026, first print, in State Employment and Unemployment Table 1. The relevant BLS series code is LASST080000000000006: state 08, measure 06 labor force, seasonally adjusted. The target unit is thousands, so BLS person counts are divided by 1,000."},{"kind":"tool","tool":"official.lookup","call":"Checked the official BLS August 2026 release calendar for the State Employment and Unemployment publication date.","result":"Fetched the verified release slot: State Employment and Unemployment (Monthly) for July 2026 is scheduled for August 21, 2026 at 10:00 AM Eastern; the same calendar page also lists Employment Situation for July 2026 on August 7, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest official BLS State Employment and Unemployment Table 1 for seasonally adjusted state labor force data.","result":"Fetched Colorado seasonally adjusted labor force values in persons: June 2025 = 3,258,203, April 2026 = 3,215,558, May 2026 revised = 3,206,175, and June 2026 preliminary = 3,193,263; June 2026 unemployed = 124,750 and unemployment rate = 3.9 percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Colorado Economy at a Glance page for the recent monthly sequence in the same seasonally adjusted variant.","result":"Fetched Colorado civilian labor force in thousands: January 2026 = 3,248.8, February 2026 = 3,238.5, March 2026 = 3,227.9, April 2026 = 3,215.6, May 2026 = 3,206.2, and June 2026 preliminary = 3,193.3; the page says these labor-force values are number of persons in thousands, seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS national Employment Situation household table for a contemporaneous labor-force participation backdrop.","result":"Fetched U.S. seasonally adjusted civilian labor force in thousands: April 2026 = 169,995, May 2026 = 170,078, and June 2026 = 169,358; U.S. participation rate fell from 61.8 percent in May 2026 to 61.5 percent in June 2026."},{"kind":"text","text":"Base rate/reference class: the cleanest base rate is Colorado's own recent seasonally adjusted LAUS labor-force path, because state labor-force levels are highly persistent and this is a one-month-ahead first-print target. The January through June 2026 sequence moved from 3,248.8 thousand to 3,193.3 thousand, a five-month decline of about 55.5 thousand."},{"kind":"text","text":"Level, momentum, one-off, and mechanism: the latest level is around 3.193 million and momentum is sharply negative but smooth. The mechanism is state CPS/LAUS model movement and labor-force participation, not payroll jobs. I use the same seasonally adjusted LAUS variant throughout; I do not mix in not-seasonally-adjusted COLFN anchors."},{"kind":"text","text":"Prior/update/interval: prior model is one-month persistence plus recent-change continuation using January-June 2026 Colorado seasonally adjusted labor-force history. Successive changes in thousands were -10.3, -10.6, -12.3, -9.4, and -12.9; the mean monthly change is -11.1 thousand and sigma = 1.46 thousand. The point is 3,193.3 - 11.1 = 3,182.2 thousand. The normal 80% half-width is 1.28*sigma = 1.87 thousand; I widen to 2.4 thousand, about 1.3x, for first-print state CPS noise, the preliminary June anchor, and the small five-change sample, giving final implied bounds 3,179.8 to 3,184.6 thousand."},{"kind":"math","text":"Point and interval arithmetic in thousands: latest official June 2026 preliminary value 3,193.263 plus mean recent change -11.105 = 3,182.158, rounded to 3,182.2. Realized-change sigma = 1.462, so 1.28*sigma = 1.872; widened half-width 2.4 gives ciLow = 3,182.2 - 2.4 = 3,179.8 and ciHigh = 3,182.2 + 2.4 = 3,184.6."},{"kind":"text","text":"Counter-consideration: upside risk is a July participation rebound, a reversal of the June state-model drop, or stronger household employment that would land above the interval near 3,185 thousand or higher. Downside risk is another unusually large LAUS model decline, weaker household employment, or out-migration/participation slippage that would land below the interval near 3,180 thousand. Outside the interval would most likely reflect state CPS sampling/model noise rather than a clean real-time Colorado labor-market signal."},{"kind":"forecast","point":3182.2,"ciLow":3179.8,"ciHigh":3184.6}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the interval justification; resolver, unit, first-print rule, release date, and forecast fields are otherwise coherent with the target contract.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on only five recent month-to-month changes during a monotonic decline, so the realized-volatility estimate may understate normal one-month LAUS first-print uncertainty.","actionRequested":"Either justify why the five-change Jan-Jun 2026 sample is adequate for this target, or add a broader historical one-month change/forecast-error volatility check and adjust or defend the 3179.8-3184.6 interval."}],"optionalSuggestions":["State explicitly that the BLS Table 1 URL is mutable and that resolution should use the first July 2026 print as captured/released on August 21, 2026, not whatever later appears at the same URL.","The prior/update/interval step is strong; consider naming the historical sample as 'Jan-Jun 2026 only' in the final prose to make the narrow sample choice unmistakable."]}

Emit the final JSON object only.
