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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US initial claims, week ending July 11, 2026","question":"What will the U.S. Department of Labor Employment and Training Administration advance seasonally adjusted initial claims be for the week ending July 11, 2026, in the first print?","unit":"thousands","pointEstimate":216,"ciLow":202,"ciHigh":231,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance seasonally adjusted Initial Claims figure for the week ending July 11, 2026 in the first U.S. DOL ETA Unemployment Insurance Weekly Claims release issued July 16, 2026. Convert the published count to thousands and use the first print only; do not use later revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-07-04 latest SA initial claims","value":215},{"label":"2026-06-27 SA initial claims","value":217},{"label":"2026-06-20 SA initial claims","value":216},{"label":"2026-06-13 SA initial claims","value":227},{"label":"latest 4-week average","value":218.75}],"drivers":["Latest same-variant SA initial claims were 215k, below the 218.75k four-week average.","Recent 13-week official table is centered near 214k with no sustained break higher.","Seasonally adjusted July holiday weeks can be noisy, so interval remains wider than a one-week persistence band.","Insured unemployment is stable at a 1.2% SA rate, limiting downside labor-market shock evidence."],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://www.dol.gov/newsroom/economicdata","https://fred.stlouisfed.org/series/ICSA"],"runAt":"2026-07-09T22:35:32Z","reasoning":[{"kind":"heading","text":"Forecast for US DOL SA initial claims, week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the DOL ETA advance seasonally adjusted Initial Claims figure for the week ending July 11, 2026, reported in thousands in the first Unemployment Insurance Weekly Claims release. The same-variant series is seasonally adjusted initial claims; the DOL release table is 'Seasonally Adjusted US Weekly UI Claims (in thousands)' and the FRED mirror series code is ICSA."},{"kind":"tool","tool":"official.lookup","call":"Opened the current DOL Unemployment Insurance Weekly Claims Report PDF at https://www.dol.gov/ui/data.pdf.","result":"The July 9, 2026 DOL release says week ending July 4 advance seasonally adjusted initial claims were 215,000, down 2,000 from a revised 217,000 for June 27; the 4-week moving average was 218,750."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL same-variant seasonally adjusted weekly table in the current release.","result":"Recent SA initial claims in thousands were Apr 11 208, Apr 18 215, Apr 25 190, May 2 199, May 9 212, May 16 210, May 23 212, May 30 225, Jun 6 230, Jun 13 227, Jun 20 216, Jun 27 217, Jul 4 215."},{"kind":"tool","tool":"release_calendar.lookup","call":"Checked release-date metadata for the ETA Unemployment Insurance Weekly Claims Report via the DOL economic data page and FRED ICSA release metadata.","result":"DOL identifies the Unemployment Insurance Weekly Claims Report as the ETA weekly report, the current DOL PDF was embargoed until 8:30 a.m. Eastern Thursday July 9, 2026, and FRED ICSA showed latest observation 2026-07-04 at 215,000 with next release date Jul 16, 2026."},{"kind":"text","text":"Reference class/base rate: for a one-week-ahead first print in the same SA initial-claims series, the natural base rate is persistence around the latest print and recent 4-week average. The latest value is 215k, the latest 4-week average is 218.75k, and the 13-week official-source mean is 213.54k."},{"kind":"text","text":"Level, momentum, and mechanisms: level is low-200k and stable; short momentum is roughly flat because 215k follows 217k and 216k; insured unemployment at 1.2% does not signal a sudden claims breakout; July holiday seasonal adjustment raises noise but not directional conviction."},{"kind":"math","text":"Prior/update/interval: persistence prior on the latest same-variant DOL SA print is 215k, historical sample is the 13 official weekly values 208,215,190,199,212,210,212,225,230,227,216,217,215, adjustment components are +0.94k toward the 218.75k 4-week average plus +0.5k for mild labor-market softness, giving 216.44k rounded to 216k. Interval method uses realized dispersion of these flow values: n=13, sum=2776, sumsq=594202, sigma = sqrt((594202-(2776*2776/13))/12) = 10.875 thousand, and 80% half-width = 1.28*sigma = 13.920 thousand; 216.44 +/- 13.92 gives 202.52 to 230.36, rounded outward to 202k to 231k."},{"kind":"text","text":"Counter-considerations: upside risk is a post-holiday reporting or layoff jump like the recent 230k and 227k weeks, which could land above the interval if SA factors under-adjust; downside risk is a reversal toward the late-April 190k print, which would land below the interval if July claims filings are unusually light; outside the interval would require either a renewed layoff wave above 231k or a sharp clean-week drop below 202k."},{"kind":"forecast","point":216,"ciLow":202,"ciHigh":231}]}

# Reviewer critique
{
  "summary": "The draft is publishable: resolver, prior/update/interval, tail scenarios, and JSON fields are coherent with no blocking leakage or unit issues found.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider noting that the DOL PDF URL is rolling and that the July 16 first-print artifact should be archived or captured at resolution for reproducibility.",
    "For a stronger interval justification, mention whether the 13-week level dispersion was chosen over one-week change volatility because July holiday seasonality can affect the level."
  ]
}

Emit the final JSON object only.
