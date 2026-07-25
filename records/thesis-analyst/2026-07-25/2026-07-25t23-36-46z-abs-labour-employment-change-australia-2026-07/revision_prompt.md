# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.labour.employment_change.australia
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "abs-labour-employment-change-australia-july-2026"
- country: "AU"
- targetUnit: "thousands"
- dataPointId: "abs.labour.employment_change.australia.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["data.api.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "LF/M3.3.1599.20.AUS.M", "releasePolicy": "first_print", "sourceSeriesId": "LF/M3.3.1599.20.AUS.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata", "table": "Labour Force, Australia (dataflow LF: employed persons, seasonally adjusted, Australia; month-over-month change)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-25-a8757927ffb64fa7d106a7b1d738ad0b0ca995229848a7271482d80b828bac1a.json"
- targetContentHash: "a8757927ffb64fa7d106a7b1d738ad0b0ca995229848a7271482d80b828bac1a"
- registrationCommit: "6d2b1a2c61155c88851ab8dad6099ae6f9ef5823"
- registeredAtUtc: "2026-07-25T23:27:53Z"

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
{"slug":"abs-labour-employment-change-australia-july-2026","country":"AU","type":"data","title":"Australia Employment Change, July 2026","question":"What will the Australian Bureau of Statistics first print for seasonally adjusted employed people month-over-month change in Australia be for July 2026, in thousands, in Labour Force, Australia?","unit":"thousands","pointEstimate":24,"ciLow":-27,"ciHigh":75,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Australian Bureau of Statistics Labour Force, Australia, July 2026","resolutionSourceUrl":"https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/jul-2026","resolutionRule":"Resolve to the first ABS print for Labour Force, Australia, July 2026, series LF/M3.3.1599.20.AUS.M: seasonally adjusted employed persons, Australia, month-over-month change, in thousands. Use the value published in the first release/API observation on 2026-08-20, rounded to one decimal thousand if the source presents one decimal; ignore later revisions.","dataPointId":"abs.labour.employment_change.australia.july_2026.first_print","historicalContext":[{"label":"Apr-2026 SA employment change","value":-38.6},{"label":"May-2026 SA employment change","value":44},{"label":"Jun-2026 SA employment change","value":76.3},{"label":"last-24-month mean SA employment change","value":20.9},{"label":"last-24-month sigma","value":39.7}],"drivers":["June employment spike likely partly unwinds after waiting-to-start-job effect","trend employment growth near 32 thousand remains positive","high participation and 4.4 percent unemployment imply labour demand still firm","survey transition and rotation-group adjustment increase month-to-month noise"],"sourceContext":["https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/jun-2026","https://www.abs.gov.au/about/key-priorities/data-acquisition-modernisation-program/modernising-labour-force-survey","https://www.abs.gov.au/media-centre/media-releases/unemployment-rate-remains-44-june","https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata"],"runAt":"2026-07-25T23:36:52Z","reasoning":[{"kind":"heading","text":"Australia July 2026 employment change first-print forecast"},{"kind":"text","text":"Framing and exact resolver: this is the ABS Labour Force, Australia first print for July 2026, seasonally adjusted employed people, Australia, month-over-month change in thousands. The ledger source series is LF/M3.3.1599.20.AUS.M, so anchors and the final resolver all use the same seasonally adjusted employed-persons variant rather than trend, original, hours, unemployment, or participation series."},{"kind":"tool","tool":"official.lookup","call":"ABS Labour Force, Australia June 2026 release page and future-release listing","result":"Fetched release timing and latest print: June 2026 was released 23/07/2026 at 11:30am AEST; the page lists Next Release 20/08/2026 for Labour Force, Australia, July 2026; seasonally adjusted employed people rose from 14,746,900 in May 2026 to 14,823,300 in June 2026, a monthly change of 76,300 or 76.3 thousand."},{"kind":"tool","tool":"official.lookup","call":"ABS Modernising the Labour Force Survey updated release schedule","result":"Fetched official schedule: Labour Force, Australia July 2026 release date is 20/08/2026; April 2026 was 21/05/2026, May 2026 was 25/06/2026, June 2026 was 23/07/2026, and August 2026 is scheduled for 24/09/2026."},{"kind":"tool","tool":"official.lookup","call":"ABS June 2026 release employment table, seasonally adjusted employed people levels","result":"Fetched recent SA employed-person levels in thousands: Mar-2026 14,741.551774, Apr-2026 14,702.952844, May-2026 14,746.946935, Jun-2026 14,823.289454; implied changes are Apr -38.6, May 44.0, and Jun 76.3 thousand."},{"kind":"tool","tool":"official.lookup","call":"ABS June 2026 release labour-market context and media release","result":"Fetched current context: unemployment rate was 4.4 percent in June 2026, participation rate rose 0.3 percentage points to 67.0 percent, monthly hours worked rose 5 million or 0.2 percent, full-time employment rose 29.3 thousand, and part-time employment rose 47.0 thousand."},{"kind":"text","text":"Reference class/base rate: I used the last 24 official seasonally adjusted monthly employment changes from Jul-2024 through Jun-2026 as the base rate, because the target is a monthly change/flow series and the ABS itself cautions that short-term changes are volatile. That sample has a mean of 20.9 thousand and contains large positive and negative prints, including -74.8 thousand in Feb-2025, 104.0 thousand in Apr-2025, -38.6 thousand in Apr-2026, 44.0 thousand in May-2026, and 76.3 thousand in Jun-2026."},{"kind":"math","text":"Prior/update/interval: persistence prior is the last-24-month official SA employment-change reference class mean of 20.9 thousand; historical sample is Jul-2024 through Jun-2026 values from ABS employed-person levels; adjustment components are +8 thousand for still-positive trend employment growth near 32.3 thousand in Jun-2026, -7 thousand for likely payback after the June waiting-to-start-job and rotation/sample effects, and +2 thousand for firm participation/labour-demand context, giving point 20.9+8-7+2 = 23.9, rounded to 24.0 thousand. Interval method uses the values themselves for this change/flow series: sigma = 39.7 thousand over the last 24 changes, so 1.28*sigma = 50.8 thousand; centered on 24.0 gives -26.8 to 74.8, rounded to an 80 percent interval of -27.0 to 75.0 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is that elevated participation and the June waiting-to-start-job comment were not just timing noise, in which case another broad hiring month would land above the interval. Downside risk is that the June surge borrowed from July or that survey-transition volatility reverses sharply, which would land below the interval. A material outside the interval print would most likely require either another rotation/sample shock or a sudden labour-demand break not visible in the June official data."},{"kind":"forecast","point":24,"ciLow":-27,"ciHigh":75}]}

# Reviewer critique
{"summary":"Draft is broadly publishable, but the resolver URL should be aligned to the canonical ABS API source binding rather than the human ABS release page.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The forecast's resolutionSourceUrl points to an ABS human release page, while the ledger contract names the canonical resolver as the ABS Data API URL for LF/M3.3.1599.20.AUS.M.","actionRequested":"Set or add the canonical resolver URL to https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata and make clear the human ABS July 2026 page is supporting context, not the final resolver."}],"optionalSuggestions":["In the resolver text, explicitly say the resolved value is the first observed July 2026 API observation for LF/M3.3.1599.20.AUS.M, with later revisions ignored.","The compact prior/update/interval step is strong; keep it as the core audit trail."]}

Emit the final JSON object only.
