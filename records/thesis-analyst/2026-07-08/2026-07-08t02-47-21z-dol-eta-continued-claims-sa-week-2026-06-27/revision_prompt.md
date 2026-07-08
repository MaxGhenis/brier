# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-06-27
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-06-27"
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
{"slug":"continued-claims-week-2026-06-27","country":"US","type":"data","title":"US continued claims, Jun 27 2026","question":"What will the U.S. Department of Labor Employment and Training Administration first print show for seasonally adjusted insured unemployment, also called continued claims, for regular state programs for the week ending June 27, 2026?","unit":"millions","pointEstimate":1.817,"ciLow":1.79,"ciHigh":1.85,"confidence":0.8,"resolutionDate":"2026-07-09","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260709","resolutionRule":"Resolve to the advance first-print seasonally adjusted insured unemployment number for regular state programs for the week ending June 27, 2026 in the DOL ETA Unemployment Insurance Weekly Claims release scheduled for July 9, 2026. Convert persons or thousands to millions, round to 0.001 million, and ignore later revisions or historical restatements.","dataPointId":"dol.eta.continued_claims.sa.week_2026-06-27.first_print","historicalContext":[{"label":"2026-06-20 SA insured unemployment","value":1.814},{"label":"2026-06-13 SA insured unemployment","value":1.812},{"label":"2026-06-06 SA insured unemployment","value":1.8},{"label":"2026-05-30 SA insured unemployment","value":1.786},{"label":"2025 comparable June 28 SA insured unemployment","value":1.952}],"drivers":["Latest official SA continued claims were 1.814 million, up 0.002 million on the week","Recent SA continued-claims momentum is mildly upward: 1.786 million on May 30 to 1.814 million on June 20","Initial claims for June 27 were 215,000, down 1,000, arguing against a sharp further jump","Unadjusted insured unemployment rose 34,778 in the June 20 week, broadly in line with seasonal-factor expectations","Target is the DOL ETA regular state programs seasonally adjusted insured unemployment variant, not all-program unadjusted continued weeks claimed"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260702","https://oui.doleta.gov/unemploy/claims_arch.asp","https://www.dol.gov/newsroom/releases/eta"],"runAt":"2026-07-08T02:47:27Z","thresholdLadder":{"thresholds":[1.78,1.79,1.8,1.81,1.815,1.82,1.83,1.84,1.85,1.86,1.875],"cumulativeProbabilities":[0.06,0.1,0.2,0.36,0.46,0.56,0.72,0.84,0.9,0.95,0.98]},"reasoning":[{"kind":"heading","text":"Forecast for DOL ETA continued claims, week ending June 27, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the DOL ETA regular state programs seasonally adjusted insured unemployment series, also called continued claims, for the week ending June 27, 2026. The resolution is the advance first print in the weekly claims release, in millions of persons, ignoring later revisions."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL ETA claims archive publication schedule at https://oui.doleta.gov/unemploy/claims_arch.asp","result":"The official schedule says the UI Weekly Claims News Release is published each week on Thursday at 8:30 AM EST, with 1 listed 2026 exception: Wednesday, November 25, 2026 at 8:30 AM EST; therefore Thursday, July 9, 2026 is the verified release date for the June 27 continued-claims first print."},{"kind":"tool","tool":"official.lookup","call":"Opened the July 2, 2026 DOL ETA Unemployment Insurance Weekly Claims release at https://www.dol.gov/newsroom/releases/eta/eta20260702","result":"Fetched latest same-variant figures: advance SA insured unemployment for week ending June 20 was 1,814,000; week ending June 13 was revised to 1,812,000; the 4-week moving average was 1,803,000; the SA insured unemployment rate was 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read the July 2, 2026 DOL release table for regular state programs and unadjusted state-program insured unemployment","result":"Fetched table values: Insured Unemployment (SA) was 1,814,000 for June 20, 1,812,000 for June 13, and 1,800,000 for June 6; Insured Unemployment (NSA) was 1,755,714 for June 20, up 34,778 from 1,720,936."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL release table of Seasonally Adjusted US Weekly UI Claims, using the insured unemployment column in thousands","result":"Fetched reference-class history from June 21, 2025 through June 20, 2026: 53 weekly SA insured unemployment observations; recent values included 1,786,000 on May 30, 1,800,000 on June 6, 1,812,000 on June 13, and 1,814,000 on June 20."},{"kind":"text","text":"Base rate/reference class: for a one-week-ahead continued-claims level forecast, the best outside-view anchor is persistence from the latest first-print/revised DOL SA insured unemployment level plus the empirical distribution of recent weekly changes in the same DOL variant. The latest level is 1.814 million, and the last three weekly changes were +0.014, +0.012, and +0.002 million."},{"kind":"text","text":"Variant control: every anchor above is the regular state programs Seasonally Adjusted Insured Unemployment series from the DOL weekly claims release, not NSA insured unemployment and not continued weeks claimed in all programs."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1.814 million from the latest DOL same-variant print; historical sample = 52 successive weekly changes from the June 21, 2025 to June 20, 2026 DOL table; adjustment components = +0.004 million for recent upward continued-claims momentum, -0.001 million because initial claims for June 27 were only 215,000 and down 1,000, +0.000 million for policy mechanism because no UI rule change is needed for the first print; point before ladder = 1.817 million. From the fetched history, sigma = 0.020987 million for successive SA insured-unemployment changes, so 1.28*sigma = 0.026863 million. The ladder-implied 80% half-width is about 0.030 million, 1.12x the 1.28*sigma half-width, modestly wider because holiday/seasonal adjustment around late June can move continued claims even when initial claims are flat."},{"kind":"math","text":"Ladder: P(X <= 1.780) = 0.06; P(X <= 1.790) = 0.10; P(X <= 1.800) = 0.20; P(X <= 1.810) = 0.36; P(X <= 1.815) = 0.46; P(X <= 1.820) = 0.56; P(X <= 1.830) = 0.72; P(X <= 1.840) = 0.84; P(X <= 1.850) = 0.90; P(X <= 1.860) = 0.95; P(X <= 1.875) = 0.98. Linear interpolation gives p10 = 1.790, p50 = 1.817, and p90 = 1.850 million after rounding to 0.001 million."},{"kind":"text","text":"Counter-considerations: upside risk would be a repeat of broad unadjusted insured-unemployment increases like the +34,778 NSA move in the latest release, which could lift the SA print toward or above 1.850 million. Downside risk would be a reversal in benefit duration after initial claims held at 215,000, which could pull the SA level below 1.790 million. A sudden state reporting distortion or seasonal-factor miss would land outside the interval."},{"kind":"forecast","point":1.817,"ciLow":1.79,"ciHigh":1.85}]}

# Reviewer critique
{
  "summary": "The draft is publication-ready on the main rubric: resolver, prior, update, volatility-based interval, tails, units, and JSON fields are coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Clarify that the July 9 DOL URL is the expected release URL and that the DOL archive/latest-release page is the fallback if the URL pattern changes.",
    "If keeping the 2025 comparable value, cite the exact comparable-week source because it differs slightly from the prior-year value shown in the July 2 table."
  ]
}

Emit the final JSON object only.
