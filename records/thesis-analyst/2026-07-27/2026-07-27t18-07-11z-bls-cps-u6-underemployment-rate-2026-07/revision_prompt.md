# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.u6_underemployment_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "u6-underemployment-rate-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.cps.u6_underemployment_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-07", "start": "2026-08-07"}, "field": "U6RATE", "releasePolicy": "first_print", "sourceSeriesId": "U6RATE", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=U6RATE", "table": "Employment Situation, Table A-15", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-20ec6a3c168e40892ebc5fe44743cf49c5940add207def0313de53d7f7cb8ed7.json"
- targetContentHash: "20ec6a3c168e40892ebc5fe44743cf49c5940add207def0313de53d7f7cb8ed7"
- registrationCommit: "e494ebc7a9b410a6fcffab9e5439408ff3d09413"
- registeredAtUtc: "2026-07-27T18:01:44Z"

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

Emit the final JSON object only. (agent thesis.analyst v2.4.0, prompt 7ef119647b35, tools 50a06b62f9be, promptMode fast)


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
{"slug":"u6-underemployment-rate-july-2026","country":"US","type":"data","title":"U-6 Underemployment Rate, July 2026","question":"What will the BLS first-print seasonally adjusted U-6 alternative labor underutilization rate be for July 2026 in Employment Situation Table A-15?","unit":"percent","pointEstimate":7.9,"ciLow":7.7,"ciHigh":8.1,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-15","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.t15.htm","resolutionRule":"Resolve to the first BLS-published July 2026 seasonally adjusted U-6 value in Employment Situation Table A-15, in percent, as released on August 7, 2026. Use the first print rounded to one decimal place; do not apply later revisions or same-day correction exceptions unless BLS explicitly republishes the first release before normal public access.","dataPointId":"bls.cps.u6_underemployment_rate.2026_07.first_print","historicalContext":[{"label":"2026-06 U-6 SA","value":7.9},{"label":"2026-05 U-6 SA","value":8.1},{"label":"2026-04 U-6 SA","value":8.2},{"label":"2026-03 U-6 SA","value":8.0},{"label":"2026-02 U-6 SA","value":7.9},{"label":"2026-01 U-6 SA","value":8.1}],"drivers":["June 2026 U-6 first print was 7.9 percent after May 8.1 and April 8.2","recent seasonally adjusted U-6 moves are small, with five 2026 monthly changes of -0.2, +0.1, +0.2, -0.1, and -0.2 percentage points","June official U-3 unemployment was 4.2 percent, down from 4.3 percent in May, limiting near-term U-6 upside","July first print resolves on the August 7, 2026 Employment Situation release"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/news.release/empsit.t15.htm?source=news_body_link","https://fred.stlouisfed.org/series/U6RATE","https://alfred.stlouisfed.org/series?seid=U6RATE"],"runAt":"2026-07-27T18:07:25Z","reasoning":[{"kind":"heading","text":"Forecast for BLS July 2026 U-6 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS CPS household-survey U-6 alternative labor underutilization rate, seasonally adjusted, Table A-15, source code LNS13327709 mirrored by FRED/ALFRED as U6RATE. The ledger uses ALFRED for first-print capture, but the substantive resolver is the BLS Employment Situation Table A-15 first print."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Schedule of Releases for the Employment Situation for the July 2026 reference month.","result":"BLS lists July 2026 Employment Situation release date as Aug. 07, 2026 at 08:30 AM; the same schedule lists June 2026 on Jul. 02, 2026 and August 2026 on Sep. 04, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS CPS release calendar for the July 2026 reference period.","result":"BLS CPS calendar lists Aug. 07, 2026 for July 2026 Employment Situation, with nearby entries Jul. 02, 2026 for June 2026 and Sep. 04, 2026 for August 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current official BLS Employment Situation Table A-15 for recent seasonally adjusted U-6 values.","result":"BLS Table A-15 reports U-6 seasonally adjusted values of Feb. 2026 7.9, Mar. 2026 8.0, Apr. 2026 8.2, May 2026 8.1, and June 2026 7.9; the same table reports June 2025 seasonally adjusted U-6 at 7.7."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED/ALFRED U6RATE as a public history mirror for the same BLS series LNS13327709.","result":"FRED/ALFRED U6RATE shows Jun 2026 7.9, May 2026 8.1, Apr 2026 8.2, Mar 2026 8.0, and Feb 2026 7.9, updated Jul 2, 2026 at 8:31 AM CDT, with next release date Aug 7, 2026."},{"kind":"text","text":"Base rate/reference class: for a monthly labor-underutilization rate already near 8 percent, the strongest reference class is persistence plus small one-month CPS sampling and composition movement. The 2026 official/mirror history gives recent one-month moves of -0.2, +0.1, +0.2, -0.1, and -0.2 percentage points from Jan through Jun, so unchanged or a one-tenth move is the modal case."},{"kind":"text","text":"Level, momentum, and mechanism: the latest level is 7.9 percent, down from 8.2 in April and 8.1 in May, while June U-3 in the same Table A-15 was 4.2 after 4.3 in May. That argues against a sharp U-6 rise, but U-6 is broader than U-3 and can move with marginal attachment and part-time-for-economic-reasons even when unemployment is steady."},{"kind":"math","text":"Prior/update/interval: persistence prior = June 2026 U-6 at 7.9 percent; historical sample = Jan-Jun 2026 seasonally adjusted U-6 values 8.1, 7.9, 8.0, 8.2, 8.1, 7.9, with successive changes -0.2, +0.1, +0.2, -0.1, -0.2. Sample sigma = 0.18 percentage point. 80% normal half-width is about 1.28*sigma = 1.28*0.18 = 0.23 percentage point. Adjustment components: level 0.00, recent downward momentum -0.05, mean-reversion from June drop +0.05, policy/mechanism one-off 0.00, leaving point 7.9. Implied continuous 80% bounds are 7.9 +/- 0.23 = 7.67 to 8.13, rounded to 7.7 to 8.1 for the printed one-decimal series."},{"kind":"text","text":"Counter-considerations: upside risk is a July jump in part-time-for-economic-reasons or marginal attachment that lifts U-6 to 8.2 or higher, which would land above the 80% interval. Downside risk is a broad household-survey improvement that pushes U-6 to 7.6 or lower, which would land below the interval. Outside the interval would most likely require a larger-than-recent move in the broader underemployment components rather than just a small U-3 change."},{"kind":"forecast","point":7.9,"ciLow":7.7,"ciHigh":8.1}]}

# Reviewer critique
{
  "summary": "Draft is mostly publication-ready, but the resolver/source fields should be aligned with the canonical ledger binding before publication.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "Draft JSON uses BLS Table A-15 URL as resolutionSourceUrl, while the ledger sourceBinding resolves mechanically through ALFRED U6RATE first-print capture.",
      "actionRequested": "Make the resolver text explicitly match the target contract: July 2026 first-print U6RATE via the ledger ALFRED binding, while noting BLS Table A-15 is the underlying official release."
    }
  ],
  "optionalSuggestions": [
    "The Jan-Jun-only volatility sample is compact but very short; consider stating that the narrow 80% interval is based on recent monthly realized moves and rounded first-print granularity.",
    "The tail scenarios are adequate; adding explicit example values such as 8.2+ and 7.6 or lower already makes them concrete.",
    "Check that sourceContext does not imply FRED, rather than ALFRED first vintage or BLS Table A-15, is the final resolver."
  ]
}

Emit the final JSON object only.
