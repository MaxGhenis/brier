# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.real_earnings.avg_hourly_mom.2026-07.first_print"
- resolutionDate: "2026-08-12"
- resolutionSource: "U.S. Bureau of Labor Statistics Real Earnings Table A-1"
- resolutionSourceUrl: "https://www.bls.gov/news.release/realer.t01.htm"
- resolutionRule: "Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-10"}, "field": "bls.real_earnings.avg_hourly_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.real_earnings.avg_hourly_mom", "sourceUrl": "https://www.bls.gov/news.release/realer.t01.htm", "table": "U.S. Bureau of Labor Statistics Real Earnings Table A-1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334.json"
- targetContentHash: "8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

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
- Size the 80% interval by reading it off your elicited threshold ladder, and SHOW the derivation in the 'Ladder:' math step: state the interpolated values literally as '10th percentile at X', 'median at Y', and '90th percentile at Z'. Ground the rung placement in the fetched reference-class history (state which fetched values anchored the rung span in the Prior/update/interval step). Never default to a round hedged band.
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

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode ladder_v2)

# Threshold-ladder elicitation (promptMode ladder_v2)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs, then states the interpolated '10th percentile at X', 'median at Y', and '90th percentile at Z' in the same step.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every other requirement above (base rate, upside/downside/outside-the-interval risks, Prior/update/interval step).
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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real hourly earnings MoM, July 2026","question":"What will the first-print BLS Real Earnings Table A-1 seasonally adjusted over-the-month percent change be for real average hourly earnings of all employees on private nonfarm payrolls in July 2026?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.5,"ciHigh":0.3,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2026-05 real average hourly earnings MoM SA first available table value","value":-0.1},{"label":"2026-04 real average hourly earnings MoM SA table value","value":-0.5},{"label":"2026-03 real average hourly earnings MoM SA table value","value":-0.6},{"label":"2025-05 real average hourly earnings MoM SA table value","value":0.4}],"drivers":["Real hourly earnings mechanically combine nominal private average hourly earnings and CPI-U inflation","Recent BLS real hourly prints were negative as CPI-U rose faster than nominal wages","June nominal average hourly earnings growth was steady near 0.3 percent","May CPI-U inflation was elevated by energy but core inflation was lower","July energy prices remain the main upside inflation risk to the deflator"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/empsit.t19.htm","https://www.bls.gov/news.release/cpi.nr0.htm"],"runAt":"2026-07-10T21:23:27Z","thresholdLadder":{"thresholds":[-0.9,-0.7,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.5,0.7],"cumulativeProbabilities":[0.02,0.06,0.1,0.17,0.26,0.38,0.52,0.65,0.76,0.84,0.9,0.97,0.99]},"reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS real average hourly earnings MoM"},{"kind":"text","text":"Framing and exact resolver: this forecast is for BLS Real Earnings Table A-1, all employees on private nonfarm payrolls, seasonally adjusted, real average hourly earnings over-the-month percent change for July 2026. The target resolves to the one-decimal first print on the BLS official release page, with no later revision used."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Real Earnings release schedule for the reference month and release date.","result":"BLS schedule lists June 2026 Real Earnings for Jul. 14, 2026 at 08:30 AM and July 2026 Real Earnings for Aug. 12, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Real Earnings Table A-1 current release for same-variant real average hourly earnings and component values.","result":"Table A-1 shows real average hourly earnings over-the-month percent changes of 0.4 for May 2025, -0.6 for Mar. 2026, -0.5 for Apr. 2026, and -0.1 for May 2026; the same row levels are $11.32, $11.31, $11.25, and $11.24."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Employment Situation Table B-3 for the latest nominal average hourly earnings anchor.","result":"BLS Table B-3 shows total private average hourly earnings of $37.41 in Apr. 2026, $37.51 in May 2026, and $37.64 in June 2026, with average weekly earnings of $1283.16, $1286.59, and $1291.05."},{"kind":"tool","tool":"official.lookup","call":"Read BLS CPI summary for the latest CPI-U inflation reference class and deflator pressure.","result":"BLS CPI summary shows CPI-U seasonally adjusted all-items changes of 0.9 in Mar. 2026, 0.6 in Apr. 2026, and 0.5 in May 2026; energy rose 10.9 in Mar., 3.8 in Apr., and 3.9 in May, while core CPI rose 0.2 in May."},{"kind":"text","text":"The same-variant rule matters: all anchors above refer either directly to BLS Table A-1 real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, or to its BLS-published nominal AHE and CPI-U inputs. I am not using FRED or local catalog estimates as evidence."},{"kind":"text","text":"Reference class and base rate: recent Table A-1 real hourly MoM prints centered below zero, with Mar.-May 2026 at -0.6, -0.5, and -0.1 after CPI-U rose 0.9, 0.6, and 0.5. A persistence prior from this reference class points negative, but the latest nominal wage input, June AHE at $37.64 after $37.51 in May, argues against another extreme negative unless July CPI-U reaccelerates."},{"kind":"text","text":"Prior/update/interval: starting from a persistence prior near the recent Table A-1 average of about -0.4 for Mar.-May 2026, I add +0.2 because June nominal AHE momentum was still about 0.3 percent, add +0.1 because May core CPI was only 0.2 despite headline energy pressure, and subtract -0.1 for July energy/geopolitical inflation risk. The threshold span is anchored by fetched real AHE rungs of -0.6, -0.5, -0.1, and +0.4, so the elicited 80 percent interval spans a negative repeat through a modest positive rebound."},{"kind":"math","text":"Ladder: P(X <= -0.9) = 0.02; P(X <= -0.7) = 0.06; P(X <= -0.5) = 0.10; P(X <= -0.4) = 0.17; P(X <= -0.3) = 0.26; P(X <= -0.2) = 0.38; P(X <= -0.1) = 0.52; P(X <= 0.0) = 0.65; P(X <= 0.1) = 0.76; P(X <= 0.2) = 0.84; P(X <= 0.3) = 0.90; P(X <= 0.5) = 0.97; P(X <= 0.7) = 0.99. Linear interpolation gives 10th percentile at -0.5, median at -0.1142857142857143, and 90th percentile at 0.3; rounded to BLS one-decimal print precision, the forecast is point -0.1 with 80 percent interval [-0.5, 0.3]."},{"kind":"text","text":"Upside risk: if July CPI-U cools sharply while nominal AHE keeps a 0.3 percent or better monthly pace, the real hourly print would land above the interval. Downside risk: renewed energy-price pressure or weak July AHE could put the deflator well above nominal wage growth and would land below the interval. An outside the interval outcome is most likely from an energy shock, a gasoline reversal, or an unusually large July payroll wage surprise."},{"kind":"forecast","point":-0.1,"ciLow":-0.5,"ciHigh":0.3}]}

# Reviewer critique
{"summary":"Draft is mostly coherent and tied to the correct BLS first-print target, but the interval and update need firmer grounding in a stated historical volatility/sample and clearer separation between June evidence and the July target inputs.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is justified mainly from four selected recent/historical rungs rather than realized volatility or an explicit uncertainty calculation.","actionRequested":"State the historical sample used for real AHE MoM volatility or explicitly justify the ladder width as a subjective uncertainty method, including why [-0.5, 0.3] is the 10th-90th range."},{"rubricItem":"update","severity":"warning","summary":"The movement from a roughly -0.4 prior to a -0.1 point estimate relies on June nominal AHE and May CPI/core CPI, but those are not direct July inputs and the July energy-risk statement is not concretely sourced.","actionRequested":"Clarify that June AHE and May CPI are momentum indicators, not target-month inputs, and add a concrete current energy/CPI rationale or reduce the claimed adjustment strength."},{"rubricItem":"model_prior","severity":"warning","summary":"A persistence prior is used, but no time-series/model prior is explicitly used or ruled out.","actionRequested":"Add one sentence saying whether a simple AR/persistence or historical mean model was considered and why the chosen persistence prior is sufficient for this forecast."}],"optionalSuggestions":["Name the Mar-May 2026 sample as intentionally short and note its limitations.","Tail scenarios are good; consider adding approximate numeric conditions, such as July nominal AHE below 0.1% or CPI above 0.5%, that would push outcomes outside the interval."]}

Emit the final JSON object only.
