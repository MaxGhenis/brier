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
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US Initial Claims, Week Ending Jul 11","question":"What will the U.S. Department of Labor report as the first-print seasonally adjusted initial unemployment insurance claims for the week ending July 11, 2026?","unit":"thousands","pointEstimate":214,"ciLow":201,"ciHigh":227,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260716","resolutionRule":"Resolve to the advance first-print value for Initial Claims (SA), seasonally adjusted regular state program initial claims, for the week ending July 11, 2026, as published by DOL ETA in the Unemployment Insurance Weekly Claims Report released at 8:30 a.m. ET on July 16, 2026. Unit is thousands, using the report's rounded-thousand headline/table value. Do not revise for later reports or corrected historical values unless the first release itself is withdrawn before public dissemination.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"week ending 2026-07-04 Initial Claims SA","value":215},{"label":"week ending 2026-06-27 Initial Claims SA","value":217},{"label":"week ending 2026-06-20 Initial Claims SA","value":216},{"label":"week ending 2026-07-04 4-week average SA","value":218.75},{"label":"comparable week 2025 Initial Claims SA","value":228}],"drivers":["recent SA initial claims flat near 215-217 thousand","4-week average fell to 218.75 thousand","insured unemployment steady at 1.2 percent","July seasonal adjustment can leave holiday-week noise","no current official signal of abrupt labor-market break"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://www.dol.gov/newsroom/releases/eta","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-10T02:44:05Z","reasoning":[{"kind":"heading","text":"US Initial Claims SA First Print For Week Ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this forecast targets DOL ETA Unemployment Insurance Weekly Claims, Initial Claims (SA), regular state programs, for the week ending July 11, 2026. The target is the advance first print in thousands, not NSA claims, continuing claims, four-week average, FRED revisions, or later DOL revisions."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL ETA latest Unemployment Insurance Weekly Claims Report at https://www.dol.gov/ui/data.pdf.","result":"Fetched latest first-print headline: for week ending July 4, 2026, seasonally adjusted initial claims were 215,000, down 2,000 from the previous week's revised 217,000; the 4-week moving average was 218,750."},{"kind":"tool","tool":"official.lookup","call":"Read DOL ETA report table 'UNEMPLOYMENT INSURANCE DATA FOR REGULAR STATE PROGRAMS' and historical SA weekly table.","result":"Fetched same-variant Initial Claims (SA) values in thousands: July 4 2026 = 215, June 27 2026 = 217, June 20 2026 = 216, June 13 2026 = 227, June 6 2026 = 230, May 30 2026 = 225, and comparable prior year July 5 2025 = 228."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL Office of Unemployment Insurance claims archive publication schedule at https://oui.doleta.gov/unemploy/claims_arch.asp.","result":"Fetched official publication schedule: UI Weekly Claims News Release is published each week on Thursday morning at 8:30 AM EST; the listed 2026 non-Thursday exception is Wednesday, November 25, 2026 at 8:30 AM EST, so Thursday July 16, 2026 is the scheduled release date for the week ending July 11, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL ETA newsroom release listing for recent claims reports.","result":"Fetched recent release sequence and numbers: July 9 2026 report for week ending July 4 had Initial Claims SA 215,000; July 2 2026 report for week ending June 27 had 215,000 before later revision to 217,000; June 25 2026 report for week ending June 20 had 215,000 before later revision to 216,000."},{"kind":"tool","tool":"time.utc","call":"Current UTC timestamp lookup for runAt.","result":"Fetched run timestamp 2026-07-10T02:44:05Z."},{"kind":"text","text":"Reference class and base rate: for a one-week-ahead forecast of a seasonally adjusted weekly level, the strongest base rate is persistence from the latest official SA first-print/revised level. Recent same-variant values cluster tightly around 215-230 thousand, with July 4 at 215 and the 4-week average at 218.75, so the outside-view prior is roughly 215 thousand rather than a trend break."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest Initial Claims (SA) 215.0 thousand using the DOL historical sample of 26 successive 2026 weekly changes from Jan 3 through Jul 4; adjustment components = 0.25*(4-week-average momentum of -3.75 thousand) + 0.15*(insured-unemployment-rate signal around 1.2 percent, treated as +0.18 thousand) - 0.4 thousand for mild normalization after July 4 holiday noise, giving 215 - 0.94 + 0.18 - 0.4 = 213.84 thousand, rounded to 214. For the 80% interval, successive-change sigma = 10.4 thousand, so half-width = 1.28*sigma = 1.28*10.4 = 13.3 thousand; 214 +/- 13.3 gives 200.7 to 227.3, rounded to 201 to 227."},{"kind":"text","text":"Upside risk: a fresh layoff wave, auto/manufacturing claims jump, or state-processing backlog release would land above the interval, especially above 227 thousand. Downside risk: a cleaner post-holiday seasonal adjustment or catch-up reversal in large states such as California, New York, or New Jersey would land below the interval, especially below 201 thousand. Outside the interval would likely require a state-level processing or holiday-adjustment surprise rather than ordinary week-to-week noise."},{"kind":"forecast","point":214,"ciLow":201,"ciHigh":227}]}

# Reviewer critique
{
  "summary": "Draft is substantively coherent, but the resolver/source does not match the canonical ledger binding and should be reconciled before publication.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft resolves directly to a DOL ETA newsroom/PDF first print, while the canonical ledger binding names the ALFRED/FRED ICSA graph CSV with advance_vintage policy and transform factor 0.001.",
      "actionRequested": "Align the JSON resolver fields with the ledger contract, or explicitly state in reasoning that the ledger sourceBinding appears inconsistent with the official-source rule while keeping the same slug/unit/dataPointId target."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolutionSourceUrl is a future-specific DOL newsroom URL that may not be stable or guaranteed before publication.",
      "actionRequested": "Use the canonical source URL or a stable DOL claims archive/source URL unless the exact future release URL is already officially confirmed."
    }
  ],
  "optionalSuggestions": [
    "The prior/update/interval section is strong; consider making clear whether the 26-week volatility sample uses first prints or latest revised values.",
    "The tails are concrete and target-tied; no replacement forecast is needed.",
    "Check that confidence 0.8 exactly corresponds to the stated 80% interval in downstream schema expectations."
  ]
}

Emit the final JSON object only.
