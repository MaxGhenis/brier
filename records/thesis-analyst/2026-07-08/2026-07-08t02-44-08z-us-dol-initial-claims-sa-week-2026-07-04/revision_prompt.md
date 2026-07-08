# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-04
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-04"
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
{"slug":"initial-claims-week-2026-07-04","country":"US","type":"data","title":"US initial claims, week ending Jul 4 2026","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial unemployment insurance claims for the week ending July 4, 2026, in the first print?","unit":"thousands","pointEstimate":217,"ciLow":204,"ciHigh":231,"confidence":0.8,"resolutionDate":"2026-07-09","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims news release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print seasonally adjusted Initial Claims figure for regular state programs, reported in thousands, for the week ending July 4, 2026 in the U.S. Department of Labor Unemployment Insurance Weekly Claims release published July 9, 2026. Use the first published print only; do not revise for later revisions or same-day corrections unless DOL republishes the first release before the public 8:30 a.m. ET embargo lift.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-04.first_print","historicalContext":[{"label":"2026-06-27 initial claims SA","value":215},{"label":"2026-06-20 initial claims SA","value":216},{"label":"2026-06-13 initial claims SA","value":227},{"label":"2026-06-06 initial claims SA","value":230},{"label":"2025-07-05 initial claims SA","value":228}],"drivers":["Latest first-print level was low at 215k after a revised 216k prior week","Four-week average of 222k points modestly above the latest weekly print","Recent 2026 changes are volatile but centered near flat","Early-July seasonal adjustment risk is material around holiday weeks","No release-calendar exception applies before July 9, 2026"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-08T02:44:47Z","thresholdLadder":{"thresholds":[198,203,208,212,215,218,221,224,228,232,236,242],"cumulativeProbabilities":[0.04,0.09,0.18,0.3,0.42,0.53,0.64,0.74,0.84,0.91,0.96,0.98]},"reasoning":[{"kind":"heading","text":"Forecast for DOL seasonally adjusted initial claims, week ending July 4, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the DOL Unemployment Insurance Weekly Claims advance seasonally adjusted Initial Claims figure for regular state programs, in thousands, for the week ending July 4, 2026, first print only. The variant is seasonally adjusted, not NSA, and all anchors below use the same SA initial-claims variant unless explicitly described as release-schedule context."},{"kind":"tool","tool":"official.lookup","call":"Opened current DOL UI Weekly Claims news release PDF at https://www.dol.gov/ui/data.pdf","result":"Fetched latest SA initial claims: week ending June 27, 2026 = 215 thousand; previous revised week ending June 20, 2026 = 216 thousand; change = -1 thousand; 4-week moving average = 222 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read DOL historical SA claims table in the same weekly claims PDF","result":"Fetched recent SA initial claims history: June 6, 2026 = 230 thousand; June 13, 2026 = 227 thousand; June 20, 2026 = 216 thousand; June 27, 2026 = 215 thousand; comparable July 5, 2025 = 228 thousand."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL Office of Unemployment Insurance weekly claims archive publication schedule at https://oui.doleta.gov/unemploy/claims_arch.asp","result":"Fetched publication schedule: weekly UI Claims News Release is published each Thursday at 8:30 AM EST, with listed 2026 exception Wednesday November 25, 2026 at 8:30 AM EST; therefore Thursday July 9, 2026 is the verified release date for the July 4, 2026 week."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL UI Weekly Claims Data page at https://oui.doleta.gov/unemploy/claims.asp to confirm the current official data surface","result":"Fetched page metadata: Unemployment Insurance Weekly Claims Data page updated July 7, 2026; page describes initial claims as measuring emerging unemployment and continued weeks claimed as the number of persons claiming unemployment benefits."},{"kind":"text","text":"Reference class and base rate: for a one-week-ahead SA initial-claims print, the most relevant reference class is the DOL weekly SA history in the current release table. Over the fetched 54 weekly values from June 21, 2025 through June 27, 2026, levels mostly sit around 200k-236k, with the latest four weeks 230k, 227k, 216k, and 215k and the latest 4-week average at 222k. The base rate is therefore a near-flat next print around the latest level to recent average, before holiday-week and noise adjustments."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level anchors at 215k latest and 222k four-week average; momentum is slightly down over the last two weeks, from 227k to 216k to 215k; one-off risk is elevated because the target week includes the July 4 holiday and seasonal factors can be imperfect; policy mechanisms do not point to an abrupt claims regime change by this release."},{"kind":"math","text":"Prior/update/interval: persistence prior model starts from latest SA initial claims of 215k with the 4-week-average anchor at 222k and comparable 2025 early-July value of 228k; historical sample is the fetched DOL SA weekly table from June 21, 2025 through June 27, 2026. Adjustment components: +2k toward the recent average, -1k for short-term downward momentum, +1k for early-July seasonal-noise skew, giving a center near 217k. From successive weekly changes in the fetched table, sample sigma = 10.4 thousand, so 1.28*sigma = 13.3 thousand. A symmetric 80% interval around 217k would be about 204k to 230k; the ladder-implied 80% bounds are 204k to 231k, essentially the same width and not widened beyond the realized-dispersion reference."},{"kind":"math","text":"Ladder: P(X <= 198) = 0.04; P(X <= 203) = 0.09; P(X <= 208) = 0.18; P(X <= 212) = 0.30; P(X <= 215) = 0.42; P(X <= 218) = 0.53; P(X <= 221) = 0.64; P(X <= 224) = 0.74; P(X <= 228) = 0.84; P(X <= 232) = 0.91; P(X <= 236) = 0.96; P(X <= 242) = 0.98. Linear interpolation gives the 10th percentile between 203 and 208 at 203.6, rounded to 204; the median between 215 and 218 at 217.2, rounded to 217; and the 90th percentile between 228 and 232 at 231.4, rounded to 231."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in filings after holiday timing or state processing backlogs, especially if the latest 215k print understated the run rate; that would land above the interval if the print exceeds 231k. Downside risk is another unusually clean SA print with broad state declines, which would land below the interval if the print is under 204k. Outside the interval is most likely from seasonal-adjustment error around the July 4 week rather than from a true labor-market break."},{"kind":"forecast","point":217,"ciLow":204,"ciHigh":231}]}

# Reviewer critique
{"summary":"Draft is publishable with only minor provenance tightening around the mutable DOL PDF URL.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolver is otherwise exact, but resolutionSourceUrl uses DOL's mutable latest-release PDF URL, which can change after July 9, 2026.","actionRequested":"Add the DOL claims archive page or a dated archived release URL in sourceContext/resolution evidence so the July 9, 2026 first print can be retrieved after data.pdf rolls forward."}],"optionalSuggestions":["Clarify whether the 2025 early-July comparison is the July 5, 2025 week from the historical table, distinct from the latest release's prior-year comparable value for June 27.","The tail scenarios are adequate, but naming one concrete state-processing or holiday-week mechanism on each side would make them slightly stronger."]}

Emit the final JSON object only.
