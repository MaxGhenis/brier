# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-08-22
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-08-22"
- country: "US"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-08-22.first_print"
- expectedReleaseWindow: {"end": "2026-09-05", "start": "2026-09-01"}
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-05", "start": "2026-09-01"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-17-8aed8abb263c72b5f3047e785d78a9a285c92820da192cadb03ffcaf826ddf0c.json"
- targetContentHash: "8aed8abb263c72b5f3047e785d78a9a285c92820da192cadb03ffcaf826ddf0c"
- registrationCommit: "f3a73cbcc701b9315d3ec1d35ea05889b2c07f95"
- registeredAtUtc: "2026-08-17T16:54:17Z"

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class: at least 6 distinct prints are MANDATORY whenever the official source exposes them.
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
  "unit": "the registered targetUnit, byte-for-byte",
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
      "period": {
        "type": "month",
        "value": "2026-04"
      },
      "label": "Human-readable period label",
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
- historicalContext must contain at least 6 distinct numeric fetched prints. Every entry needs a canonical period object: type month with YYYY-MM, quarter with YYYY-Q1..Q4, year/fiscal_year with YYYY, or week_ending with YYYY-MM-DD. Its label must unambiguously name that same period. The whole trimmed label must be one closed printable-ASCII form: YYYY-MM, Month YYYY, YYYY Month, YYYY-QN, YYYY QN, QN YYYY, YYYY, calendar year YYYY, FY2026, fiscal year YYYY, YYYY-MM-DD, or week ending YYYY-MM-DD. Never add source names, first-print or revision prose, ranges, or a second period cue to the label. Relative, contradictory, non-ASCII, and multi-period labels refuse. Alternate labels do not make duplicate canonical periods distinct. Validation refuses fewer unless the sealed checkout carries the reviewed authorization below.
- Only when the official source exposes fewer than 6 prints, fetch all available prints and add this top-level audit commentary (replace 5 with the actual count and give a nonempty detail): {"historyAvailability": {"status": "official_source_exposes_fewer_than_six_prints", "availablePrintCount": 5, "detail": "Series began recently; the official source exposes only these five prints."}}
  This model-authored commentary never authorizes an exception: a reviewed docket entry in the sealed checkout must independently list the exact target period, available count, and canonical periods.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.5.11, prompt 87db344b803f, tools 024388e49298, promptMode fast)


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
{"slug":"continued-claims-week-2026-08-22","country":"US","type":"data","title":"US Continued Claims, Week Ending 2026-08-22","question":"What will the U.S. Department of Labor Employment and Training Administration first-print seasonally adjusted insured unemployment (continued claims, CCSA) be for week ending 2026-08-22?","unit":"millions","pointEstimate":1.785,"ciLow":1.749,"ciHigh":1.821,"confidence":0.8,"resolutionDate":"2026-09-03","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Use the first official ETA Unemployment Insurance Weekly Claims news release that reports seasonally adjusted insured unemployment for week ending 2026-08-22. Take the advance/first-print seasonally adjusted insured unemployment level for that week, measured in persons, and multiply by 0.000001 to express it in millions. Do not use later revisions or corrected historical vintages unless the first-print release itself is withdrawn before publication.","dataPointId":"dol.eta.continued_claims.sa.week_2026-08-22.first_print","historicalContext":[{"period":{"type":"week_ending","value":"2026-05-30"},"label":"week ending 2026-05-30","value":1.786},{"period":{"type":"week_ending","value":"2026-06-06"},"label":"week ending 2026-06-06","value":1.8},{"period":{"type":"week_ending","value":"2026-06-13"},"label":"week ending 2026-06-13","value":1.812},{"period":{"type":"week_ending","value":"2026-06-20"},"label":"week ending 2026-06-20","value":1.806},{"period":{"type":"week_ending","value":"2026-06-27"},"label":"week ending 2026-06-27","value":1.821},{"period":{"type":"week_ending","value":"2026-07-04"},"label":"week ending 2026-07-04","value":1.798},{"period":{"type":"week_ending","value":"2026-07-11"},"label":"week ending 2026-07-11","value":1.789},{"period":{"type":"week_ending","value":"2026-07-18"},"label":"week ending 2026-07-18","value":1.777},{"period":{"type":"week_ending","value":"2026-07-25"},"label":"week ending 2026-07-25","value":1.799},{"period":{"type":"week_ending","value":"2026-08-01"},"label":"week ending 2026-08-01","value":1.777}],"drivers":["recent seasonally adjusted insured unemployment centered near 1.79 million","latest first-print level below the recent four-week average","initial claims for week ending 2026-08-08 rose to 209000 but remained low","three-week forecast horizon before the 2026-09-03 release","weekly continued-claims changes recently had about 0.016 million standard deviation"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/releases/calendar?m=&ob=n&od=asc&rid=180&ve=2026-12-31&vs=2026-01-01&y=","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA"],"runAt":"2026-08-17T17:05:40Z","reasoning":[{"kind":"heading","text":"Forecast for CCSA week ending 2026-08-22"},{"kind":"text","text":"Framing and exact resolver: the target is ETA continued claims, also called seasonally adjusted insured unemployment, for week ending 2026-08-22, first print only, reported in the UI Weekly Claims News Release and converted from persons to millions. The variant used throughout is seasonally adjusted insured unemployment, not initial claims, not not-seasonally-adjusted claims, and not all-program continued weeks."},{"kind":"tool","tool":"official.lookup","call":"Checked ETA archive/schedule page and release calendar context for the UI Weekly Claims News Release timing.","result":"ETA archive states the UI Weekly Claims News Release is published each Thursday morning at 8:30 AM EST, with 1 listed 2026 non-Thursday exception: Wednesday, November 25, 2026 at 8:30 AM EST; the release calendar also lists Thursday September 03, 2026 at 7:30 AM Central for the Unemployment Insurance Weekly Claims Report."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current DOL UI Weekly Claims PDF dated Thursday, August 13, 2026.","result":"The August 13, 2026 release reported advance seasonally adjusted insured unemployment for week ending August 1, 2026 of 1,777,000, down 22,000 from the revised July 25 level of 1,799,000; the 4-week moving average was 1,785,500."},{"kind":"tool","tool":"official.lookup","call":"Read the official PDF's seasonally adjusted US weekly UI claims history table for recent insured-unemployment prints.","result":"Recent seasonally adjusted insured unemployment values in thousands were: May 30 2026 = 1,786; June 6 = 1,800; June 13 = 1,812; June 20 = 1,806; June 27 = 1,821; July 4 = 1,798; July 11 = 1,789; July 18 = 1,777; July 25 = 1,799; August 1 = 1,777."},{"kind":"tool","tool":"official.lookup","call":"Read the same DOL PDF for contemporaneous initial-claims context.","result":"Initial claims, seasonally adjusted, were 209,000 for week ending August 8, 2026, up 9,000 from the revised August 1 level of 200,000; the 4-week moving average was 199,000."},{"kind":"text","text":"Base rate/reference class: over the recent official reference class from week ending 2026-05-30 through 2026-08-01, seasonally adjusted insured unemployment stayed in a narrow 1.777 million to 1.821 million range, with the latest 1.777 million near the low end but the four-week average still 1.7855 million."},{"kind":"text","text":"Level, momentum, one-off, and policy-mechanism effects: level argues for partial reversion from 1.777 toward the 1.7855 four-week average; recent momentum is nearly flat; the 209000 initial-claims print is a small upward pressure on later continued claims; no policy rule change or special program shock is evident in the public release text."},{"kind":"math","text":"Prior/update/interval: persistence prior starts at the latest official SA insured unemployment print, 1.777 million for week ending 2026-08-01. Historical sample is the 12 successive weekly changes from 2026-05-09 through 2026-08-01 implied by the fetched official table, with mean weekly change about +0.0005 million and weekly sigma = 0.0163 million. For the three-week horizon to 2026-08-22, horizon sigma = sqrt(3)*0.0163 = 0.0283 million, and the 80% half-width is about 1.28*sigma = 0.036 million. Updates: +0.002 million trend drift, +0.004 million level reversion toward the 4-week average, and +0.002 million for the latest initial-claims uptick, giving point 1.785 million and interval 1.785 +/- 0.036 = [1.749, 1.821]."},{"kind":"text","text":"Counter-considerations: upside risk would come from the August 8, August 15, and August 22 claims cohorts translating into slower exits from UI, which would land above the interval if insured unemployment rises past about 1.821 million. Downside risk would come from rapid summer recalls or claims-processing normalization, which would land below the interval if the print falls under about 1.749 million. An outside the interval result would most likely reflect a genuine labor-market turn or a temporary reporting/seasonal-adjustment shock rather than normal week-to-week noise."},{"kind":"forecast","point":1.785,"ciLow":1.749,"ciHigh":1.821}]}

# Reviewer critique
{
  "summary": "Draft is methodologically coherent, but its resolver/source fields do not match the canonical ledger sourceBinding.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft names the DOL PDF as resolutionSourceUrl, while the canonical target contract binds resolution to the ALFRED graph CSV for CCSA with adapter alfred-fred and releasePolicy advance_vintage.",
      "actionRequested": "Change the resolver/source fields to match the ledger sourceBinding byte-for-byte in substance: ALFRED graph CSV, sourceUrl https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA, field CCSA, advance/first vintage, multiply by 1e-06. Keep the DOL PDF only as cited evidence or explanatory official-release context if desired."
    }
  ],
  "optionalSuggestions": [
    "In the reasoning, explicitly note that the underlying official ETA print is mirrored through the registered ALFRED advance-vintage resolver.",
    "The prior/update/interval step is strong; no replacement forecast is needed."
  ]
}

Emit the final JSON object only.
