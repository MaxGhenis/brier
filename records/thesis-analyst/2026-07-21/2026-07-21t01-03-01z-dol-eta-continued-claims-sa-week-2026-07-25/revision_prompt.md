# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-25
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-25"
- country: "US"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-25.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-08", "start": "2026-08-04"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-20-82a45fed9df897ee19347cc693acb49e6673d01de85ae86071b718f3815b01c5.json"
- targetContentHash: "82a45fed9df897ee19347cc693acb49e6673d01de85ae86071b718f3815b01c5"
- registrationCommit: "134572ec0e53debeec96716bf346510a889628ee"
- registeredAtUtc: "2026-07-20T18:27:38Z"

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
{"slug":"continued-claims-week-2026-07-25","country":"US","type":"data","title":"US continued claims, July 25","question":"What will the first reported seasonally adjusted US continued unemployment claims level be for the week ending July 25, 2026?","unit":"millions","pointEstimate":1.81,"ciLow":1.792,"ciHigh":1.828,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Department of Labor, Employment and Training Administration, Unemployment Insurance Weekly Claims","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260806","resolutionRule":"Resolve to the advance (first-print) seasonally adjusted insured unemployment level for the week ending July 25, 2026, in the ETA release scheduled for August 6, 2026, converted from thousands to millions and rounded to 0.001 million. Ignore all subsequent revisions.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-25.first_print","historicalContext":[{"label":"2026-04-18","value":1.776},{"label":"2026-04-25","value":1.758},{"label":"2026-05-02","value":1.776},{"label":"2026-05-09","value":1.771},{"label":"2026-05-16","value":1.785},{"label":"2026-05-23","value":1.771},{"label":"2026-05-30","value":1.786},{"label":"2026-06-06","value":1.8},{"label":"2026-06-13","value":1.812},{"label":"2026-06-20","value":1.806},{"label":"2026-06-27","value":1.821},{"label":"2026-07-04","value":1.805}],"drivers":["Near-term persistence around 1.8 million","Recent initial-claims decline","Weak but still positive payroll growth","Weekly seasonal-adjustment noise"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260716","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/releases/calendar?m=&ob=n&od=asc&rid=180&ve=2026-12-31&vs=2026-01-01&y=","https://www.dol.gov/newsroom/economicdata/empsit_07022026.pdf"],"runAt":"2026-07-21T01:03:34Z","reasoning":[{"kind":"heading","text":"Continued claims for the week ending July 25, 2026"},{"kind":"text","text":"The target is ETA insured unemployment (continued claims), seasonally adjusted, for the week ending July 25—not initial claims, unadjusted claims, or all-program continued weeks. Resolution uses only the advance first print in the August 6 release; later revisions do not alter the outcome. The corresponding mirror series is CCSA."},{"kind":"tool","tool":"official.lookup","call":"Read the July 16, 2026 ETA Unemployment Insurance Weekly Claims release.","result":"For the week ending July 4, advance seasonally adjusted insured unemployment was 1,805,000, down 16,000; the prior week was revised to 1,821,000, and the four-week average was 1,811,000."},{"kind":"tool","tool":"official.history","call":"Extract the seasonally adjusted insured-unemployment history from the ETA release table.","result":"Fetched levels in thousands for April 18 through July 4 were 1,776, 1,758, 1,776, 1,771, 1,785, 1,771, 1,786, 1,800, 1,812, 1,806, 1,821, and 1,805."},{"kind":"tool","tool":"official.calendar","call":"Verify the publication schedule using the ETA claims archive and the 2026 Unemployment Insurance Weekly Claims release calendar.","result":"ETA states publication is Thursday at 8:30 a.m. ET except federal-holiday adjustments, and the 2026 calendar lists Thursday, August 6, 2026 for the weekly claims release."},{"kind":"tool","tool":"official.lookup","call":"Read the June 2026 BLS Employment Situation release for broader labor-market context.","result":"June payroll employment increased 57,000, the unemployment rate was 4.2%, and average payroll growth over the prior 12 months was 36,000."},{"kind":"text","text":"The reference class/base rate is short-horizon persistence in this slow-moving stock series. Its latest level was 1.805 million and four-week average 1.811 million. Level and momentum therefore favor roughly 1.81 million. Falling initial claims reduce near-term inflow, while modest payroll growth and a still-low 4.2% unemployment rate argue against a sharp accumulation. Holiday-related seasonal noise is the main one-off risk."},{"kind":"math","text":"Prior/update/interval: persistence model prior = 1.805 million, using the 12 fetched ETA levels from April 18 through July 4. The 11 successive changes were -18, +18, -5, +14, -14, +15, +14, +12, -6, +15, and -16 thousand; their sample standard deviation gives sigma = 14.4 thousand. Add 0.005 million for reversion toward the 1.811 million four-week average and broadly stable labor conditions, yielding 1.810 million. The 80% half-width is 1.28*sigma = 1.28*0.0144 = 0.0184 million, rounded to 0.018, implying 1.792 to 1.828 million."},{"kind":"text","text":"Upside risk is slower benefit exits or an unexpected layoff wave, which could land above 1.828 million. Downside risk is faster reemployment combined with continued low initial claims, which could land below 1.792 million. Either outcome would be outside the interval and falsify the persistence-centered view."},{"kind":"forecast","point":1.81,"ciLow":1.792,"ciHigh":1.828}]}

# Reviewer critique
{
  "summary": "The draft is publication-ready apart from a source-binding mismatch with the canonical ledger resolver.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft names a future DOL release URL as the resolutionSourceUrl, while the canonical ledger sourceBinding resolves via ALFRED/FRED CCSA advance vintage at alfred.stlouisfed.org with the first-print rule.",
      "actionRequested": "Align the resolver fields to the ledger contract: use the ALFRED CCSA graph CSV/source binding for the machine resolver, while keeping DOL ETA as the underlying agency source in reasoning if desired."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that 2026-08-06 is the expected ETA release date within the ledger's 2026-08-04 to 2026-08-08 expected release window.",
    "Mention that the 0.005 million upward adjustment is small relative to the 0.018 million 80% half-width, so the forecast remains mostly persistence-driven."
  ]
}

Emit the final JSON object only.
