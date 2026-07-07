# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-04
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-04"
- targetUnit: "millions"

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
{"slug":"continued-claims-week-2026-07-04","country":"US","type":"data","title":"US continued claims, Jul 4 2026","question":"What will the U.S. Department of Labor Employment and Training Administration first print show for seasonally adjusted insured unemployment, also called continued claims, for the week ending July 4, 2026?","unit":"millions","pointEstimate":1.82,"ciLow":1.783,"ciHigh":1.858,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor, Employment and Training Administration, Unemployment Insurance Weekly Claims news release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print seasonally adjusted insured unemployment number for the week ending July 4, 2026 in the DOL ETA Unemployment Insurance Weekly Claims release scheduled for July 16, 2026. Use the regular state programs Seasonally Adjusted Insured Unemployment / Continued Claims variant, convert persons to millions, and ignore later revisions or historical restatements.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-04.first_print","historicalContext":[{"label":"latest SA insured unemployment, week ending 2026-06-20","value":1.814},{"label":"previous SA insured unemployment, week ending 2026-06-13","value":1.812},{"label":"SA insured unemployment, week ending 2026-06-06","value":1.8},{"label":"latest 4-week average SA insured unemployment, week ending 2026-06-20","value":1.803},{"label":"prior-year comparable SA insured unemployment","value":1.954}],"drivers":["Latest official SA continued claims were 1.814 million, up 0.002 million on the week","Recent four-week average rose to 1.803 million, showing mild upward momentum","Initial claims eased to 215,000 and the initial-claims four-week average fell to 222,000, limiting expected further increases","First-print target is the DOL ETA SA insured-unemployment variant, not NSA all-program continued weeks claimed"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/series/CCSA"],"runAt":"2026-07-07T17:40:20Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA SA continued claims, week ending July 4, 2026"},{"kind":"text","text":"Framing and exact resolver: this forecasts the DOL ETA first-print regular-state-program seasonally adjusted insured unemployment series, also called continued claims, for the week ending July 4, 2026. The target is in millions; the agency release table reports the same SA variant in thousands/persons, so all anchors here use that same variant."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL UI Weekly Claims latest news release at https://www.dol.gov/ui/data.pdf and read the release header and seasonally adjusted data text.","result":"The July 2, 2026 DOL release reported advance seasonally adjusted insured unemployment of 1,814,000 for week ending June 20, 2026, up 2,000 from the revised 1,812,000 for week ending June 13, 2026; the latest 4-week average was 1,803,000."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL regular state programs table in the July 2, 2026 UI Weekly Claims release.","result":"The table showed Insured Unemployment (SA) of 1,814,000 for June 20, 1,812,000 for June 13, 1,800,000 for June 6, and prior-year comparable 1,954,000; Insured Unemployment Rate (SA) was 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL publication schedule on the official claims archive page https://oui.doleta.gov/unemploy/claims_arch.asp.","result":"The official schedule says the UI Weekly Claims News Release is published each Thursday at 8:30 AM EST, with the listed 2026 exception Wednesday November 25, 2026; July 16, 2026 is the Thursday first release that contains week ending July 4 continued claims."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED CCSA public mirror for recent values and source metadata.","result":"FRED series CCSA listed 2026-06-20 at 1,814,000, 2026-06-13 at 1,812,000, 2026-06-06 at 1,800,000, 2026-05-30 at 1,786,000, and next release date July 9, 2026; FRED identifies the source as U.S. Employment and Training Administration and the unit as Number, Seasonally Adjusted."},{"kind":"text","text":"Base rate / reference class: over recent official weekly SA continued-claims changes, a persistence or local-random-walk prior is usually hard to beat for two weeks ahead. The recent level is near 1.81 million, below the comparable 2025 level of 1.954 million but rising modestly through June 2026."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest 1.814 million for week ending June 20. Historical sample = last 13 one-week SA insured-unemployment changes from DOL release table: -45, +22, -1, -32, -18, +18, -5, +14, -14, +15, +14, +12, +2 thousand, with mean about -1.4 thousand and sigma = 20.7 thousand per week. Adjustment components: level +0.000 million, recent momentum +0.012 million over two weeks, easing initial-claims inflow -0.006 million, no special policy effect +0.000 million, giving 1.814 + 0.006 = 1.820 million. For a two-week-ahead level forecast, sigma = sqrt(2) * 0.0207 = 0.0293 million, and 1.28*sigma = 0.0375 million, so the 80% interval is about 1.820 +/- 0.038 = [1.783, 1.858] million."},{"kind":"text","text":"Counter-considerations: upside risk is that continued claims keep drifting higher from benefit-duration persistence or state-level school-year layoffs, which would land above the interval if July 4 SA insured unemployment is above 1.858 million. Downside risk is that recent lower initial claims feed through faster than usual or June increases are revised away, which would land below the interval if the first print is under 1.783 million. Outside the interval would most likely require either a two-week jump above about 44,000 from the June 20 level or a drop of more than about 31,000."},{"kind":"forecast","point":1.82,"ciLow":1.783,"ciHigh":1.858}]}

# Reviewer critique
{"summary":"The draft is publication-ready: resolver, timing, unit conversion, prior/update logic, volatility-based interval, tails, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Clarify that the release prose reports persons while the historical table reports thousands, with both converted to millions in the forecast.","Consider naming the 13-week sample window dates explicitly in the compact Prior/update/interval step."]}

Emit the final JSON object only.
