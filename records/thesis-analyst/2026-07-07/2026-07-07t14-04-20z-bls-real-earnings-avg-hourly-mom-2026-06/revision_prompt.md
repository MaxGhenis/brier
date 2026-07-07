# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-june-2026"

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
{"slug":"us-real-avg-hourly-earnings-mom-june-2026","country":"US","type":"data","title":"US Real Avg Hourly Earnings MoM, Jun 2026","question":"BLS Table A-1 real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, over-the-month percent change, June 2026 first print","unit":"percent","pointEstimate":0.1,"ciLow":-0.5,"ciHigh":0.7,"confidence":0.8,"resolutionDate":"2026-07-14","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first public BLS Real Earnings Table A-1 print for June 2026 real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, over-the-month percent change. Use the published one-decimal percent value for June 2026(p) as released on July 14, 2026; ignore later revisions or benchmark updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-06.first_print","historicalContext":[{"label":"2026-03","value":-0.6},{"label":"2026-04","value":-0.5},{"label":"2026-05","value":-0.1},{"label":"2025-05","value":0.4}],"drivers":["June nominal average hourly earnings already rose about 0.35 percent","June CPI-U deflator is the main remaining swing factor","Recent CPI prints were elevated by energy, especially May gasoline","Real earnings recent base rate is slightly negative but noisy"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/empsit.t19.htm","https://www.bls.gov/news.release/cpi.nr0.htm"],"runAt":"2026-07-07T14:05:24Z","reasoning":[{"kind":"heading","text":"June 2026 BLS Real Average Hourly Earnings MoM Forecast"},{"kind":"text","text":"Framing and exact resolver: this targets BLS Real Earnings Table A-1, real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, over-the-month percent change for June 2026 first print. The variant is the BLS Real Earnings SA all-employees private nonfarm series deflated by CPI-U, not production-worker earnings, weekly earnings, NSA CPI, or a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Real Earnings release schedule for June 2026 reference month.","result":"BLS schedule lists June 2026 Real Earnings release date Jul. 14, 2026 and release time 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read current BLS Real Earnings Table A-1 for recent target-series history and the deflator definition.","result":"Table A-1 reports real average hourly earnings over-the-month percent changes of 0.4 for May 2025, -0.6 for Mar. 2026, -0.5 for Apr. 2026, and -0.1 for May 2026; it also shows CPI-U levels 330.293, 332.407, 333.979 and average hourly earnings $37.35, $37.41, $37.53 for Mar-May 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Employment Situation Table B-3 for June nominal average hourly earnings input.","result":"Table B-3 reports Total private average hourly earnings of $37.41 in Apr. 2026, $37.51 in May 2026(p), and $37.64 in June 2026(p), making June nominal AHE growth about 0.3466 percent versus revised May."},{"kind":"tool","tool":"official.lookup","call":"Read BLS CPI May 2026 release for current CPI momentum before the June CPI print.","result":"BLS CPI summary reports May 2026 CPI-U all items +0.5 percent SA, April +0.6 percent, March +0.9 percent, core CPI +0.2 percent in May, food +0.2 percent, energy +3.9 percent, and gasoline +7.0 percent."},{"kind":"text","text":"Base rate/reference class: the fetched recent official target history is weakly negative, with Mar-May 2026 real hourly earnings changes of -0.6, -0.5, and -0.1 percent after energy-driven CPI pressure; the four fetched target observations including May 2025 average -0.2 percent. Current-release information should move above that base rate because June nominal AHE is already known to be stronger than May and the CPI energy impulse is unlikely to repeat at May's 3.9 percent energy pace."},{"kind":"math","text":"Known nominal wage momentum is (37.64/37.51 - 1)*100 = 0.3466 percent. A June CPI-U all-items assumption near +0.25 percent gives real hourly earnings growth ((1.0034657/1.0025)-1)*100 = 0.0963 percent, which rounds to +0.1 percent in the BLS one-decimal release table."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent official Table A-1 target-value reference class [0.4, -0.6, -0.5, -0.1], mean = -0.2; update components are +0.3466 percent known nominal AHE, about -0.25 percent assumed June CPI-U, and no separate hours effect because the target is hourly earnings; interval method is realized dispersion of the fetched change-series values, sigma = 0.4546, so 1.28*sigma = 0.5819 percentage point. Centering the final at +0.1 gives mechanical 80 percent bounds near -0.48 to +0.68, rounded to -0.5 to +0.7."},{"kind":"text","text":"Counter-consideration: upside risk is a soft or negative June CPI print combined with unchanged nominal wage data, which would land above the interval if CPI fell sharply enough to put real hourly earnings above +0.7 percent. Downside risk is another energy-led CPI jump around May's magnitude or a BLS nominal earnings correction, which would land below the interval if real hourly earnings fell under -0.5 percent. An outside the interval result would mainly falsify the assumed June CPI moderation, not the already-published nominal wage anchor."},{"kind":"forecast","point":0.1,"ciLow":-0.5,"ciHigh":0.7}]}

# Reviewer critique
{"summary":"The draft is publishable: resolver, first-print rule, prior/update math, interval construction, tails, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Use a longer historical target sample for the base-rate and volatility estimate if available; the current four-observation sample is transparent but thin.","Consider naming the CPI June release timing explicitly as unresolved at run time, since CPI is the main swing factor and releases the same morning as Real Earnings."]}

Emit the final JSON object only.
