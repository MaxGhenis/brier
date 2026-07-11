# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.building_approvals.total_dwellings_mom.australia
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "abs-building-approvals-total-dwellings-mom-australia-june-2026"
- country: "AU"
- targetUnit: "percent_growth"
- dataPointId: "abs.building_approvals.total_dwellings_mom.australia.june_2026.first_print"
- resolutionSourceUrl: "https://web.archive.org/web/20260701030516/https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["web.archive.org"], "expectedReleaseWindow": {"end": "2026-08-05", "start": "2026-07-28"}, "field": "building-approvals-australia release page", "releasePolicy": "first_print", "sourceSeriesId": "building-approvals-australia release page", "sourceUrl": "https://web.archive.org/web/20260701030516/https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026", "table": "Building Approvals, Australia (release page, key statistics)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-86249570a0f4c11f073c381a4d7ae422d3e1b1a8fd8a9ad4a151e0b6fd3dabe4.json"
- targetContentHash: "86249570a0f4c11f073c381a4d7ae422d3e1b1a8fd8a9ad4a151e0b6fd3dabe4"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"

# Source hints
- Use ABS release calendar and official monthly CPI indicator pages.
- Australia CPI indicator rates print to one decimal.
- Resolution source should be the ABS release page.

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
{"slug":"abs-building-approvals-total-dwellings-mom-australia-june-2026","country":"AU","type":"data","title":"Australia June building approvals","question":"What will be the June 2026 month-over-month percentage change in Australia's seasonally adjusted total dwelling units approved, in the ABS first print?","unit":"percent_growth","pointEstimate":1.5,"ciLow":-22,"ciHigh":25,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"Australian Bureau of Statistics, Building Approvals, Australia","resolutionSourceUrl":"https://web.archive.org/web/20260701030516/https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026","resolutionRule":"Resolve to the month-over-month percentage change for seasonally adjusted total dwelling units approved for June 2026 shown on the first ABS Building Approvals, Australia release scheduled for 30 July 2026 at 11:30am AEST. Use the published one-decimal percentage value without incorporating later revisions or the 6 August additional-information release.","dataPointId":"abs.building_approvals.total_dwellings_mom.australia.june_2026.first_print","historicalContext":[{"label":"March 2026 month-over-month change, current May-release vintage","value":-13},{"label":"April 2026 month-over-month change, current May-release vintage","value":-0.2},{"label":"May 2026 month-over-month change, first print","value":-1.1},{"label":"May 2026 total dwellings approved","value":17019},{"label":"May 2026 trend month-over-month change","value":-0.5}],"drivers":["volatile multi-unit approvals after February's spike","May weakness creates modest rebound potential","house approvals rose while non-house approvals fell sharply","underlying trend was mildly negative"],"sourceContext":["https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/feb-2026"],"runAt":"2026-07-11T18:11:50Z","reasoning":[{"kind":"heading","text":"Australia June 2026 total dwelling approvals growth"},{"kind":"text","text":"The target is the first-print June 2026 month-over-month change in seasonally adjusted total dwelling units approved for Australia. The ABS release page is the resolver; this is the seasonally adjusted total series, not trend, original, private-house, or small-area data."},{"kind":"tool","tool":"official.lookup","call":"Inspect the ABS May 2026 Building Approvals release for the latest national seasonally adjusted total-dwellings observations.","result":"ABS reported 17,019 total dwellings approved in May 2026, down 1.1% month over month and up 5.3% year over year; the corresponding trend change was -0.5%."},{"kind":"tool","tool":"official.lookup","call":"Inspect recent ABS releases for the national seasonally adjusted reference class.","result":"The current May-release levels for June 2025 through May 2026 were 16,885, 16,003, 15,314, 18,267, 16,261, 18,904, 15,974, 13,725, 19,817, 17,245, 17,207, and 17,019 dwellings; these imply monthly changes of about -5.2%, -4.3%, 19.3%, -11.0%, 16.3%, -15.5%, -14.1%, 44.4%, -13.0%, -0.2%, and -1.1%."},{"kind":"tool","tool":"official.lookup","call":"Check the ABS component split and state detail in the May 2026 release.","result":"Private-sector houses rose 2.8% to 10,537 while private-sector dwellings excluding houses fell 10.4% to 6,034; state total approvals ranged from -8.8% in Queensland to 10.9% in South Australia."},{"kind":"tool","tool":"official.calendar","call":"Verify the June 2026 publication date from the ABS future-releases schedule.","result":"The ABS schedule lists the June 2026 main Building Approvals release for 30/07/2026 at 11:30am AEST and an additional-information release for 06/08/2026 at 11:30am AEST."},{"kind":"text","text":"The outside-view base rate is modestly positive: the mean of the 11 latest same-vintage monthly changes is about 1.4%, but the reference class is extremely dispersed because lumpy multi-unit projects drive large reversals."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms point in different directions. The 17,019 May level is near the recent range's middle and May's -1.1% offers limited rebound pressure; two weak months suggest soft momentum, while February's multi-unit spike has largely unwound. Firm house approvals provide support, but the volatile non-house component dominates tail risk."},{"kind":"math","text":"Prior/update/interval: use a 12-month same-series persistence/base-rate model built from the 11 successive changes in the ABS June 2025-May 2026 seasonally adjusted total-dwellings levels. Their mean is 1.4% and sample sigma = 18.3 percentage points. Starting from that 1.4% historical mean, apply roughly +1.0 point for rebound after May weakness, -0.5 point for the mildly negative trend, and -0.4 point for continued multi-unit normalization, yielding 1.5% after rounding. The normal-reference 80% half-width is 1.28*sigma = 1.28*18.3 = 23.4 points, so 1.5 ± 23.4 gives -21.9% to 24.9%, rounded outward to final bounds of -22% and 25%."},{"kind":"text","text":"Upside risk comes from several large apartment projects being approved together; a repeat of February's concentrated multi-unit surge would land above the interval. Downside risk comes from another broad state-level pullback or reversal in non-house approvals; a fall comparable to the sharpest recent contractions could approach the lower bound, while an unusually synchronized collapse would land outside the interval."},{"kind":"forecast","point":1.5,"ciLow":-22,"ciHigh":25}]}

# Reviewer critique
{"summary":"Draft is publication-ready against the rubric, with resolver, prior, update, interval, tails, and JSON fields internally coherent.","requiredFixes":[],"optionalSuggestions":["Clarify that the interval sample is 12 monthly levels producing 11 month-over-month changes.","Consider noting that the archived May release URL is the registered source placeholder and the June first-print value is the resolving ABS page/content under that release series."]}

Emit the final JSON object only.
