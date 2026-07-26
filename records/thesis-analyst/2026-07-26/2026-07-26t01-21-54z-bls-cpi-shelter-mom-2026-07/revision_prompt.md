# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cpi.shelter_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-shelter-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.shelter_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SAH1", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SAH1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SAH1", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-5c82767a6ab5fb1c8b9100ba47b05d629ddfb3651373d64f7772cdbd833e5ad9.json"
- targetContentHash: "5c82767a6ab5fb1c8b9100ba47b05d629ddfb3651373d64f7772cdbd833e5ad9"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"

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
{"slug":"us-cpi-shelter-mom-july-2026","country":"US","type":"data","title":"US CPI Shelter MoM, July 2026","question":"What will the first-print seasonally adjusted month-over-month percent change be for BLS CPI-U shelter in U.S. city average, series CUSR0000SAH1, for July 2026?","unit":"percent_growth","pointEstimate":0.24,"ciLow":0.03,"ciHigh":0.45,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release","resolutionSourceUrl":"https://www.bls.gov/news.release/cpi.t01.htm","resolutionRule":"Resolve to the first BLS CPI release for July 2026, published August 12, 2026, using the seasonally adjusted CPI-U shelter series for U.S. city average, CUSR0000SAH1. Compute month-over-month percent growth from the first-print July 2026 and June 2026 seasonally adjusted index levels as 100*(July/June - 1), or use the BLS first-print seasonally adjusted percent-change table if exact index levels are not exposed at resolution time. Do not revise for later seasonal-adjustment revisions or subsequent corrections unless the first-print file itself is replaced before ordinary publication.","dataPointId":"bls.cpi.shelter_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 shelter SA MoM","value":0.1},{"label":"2026-05 shelter SA MoM","value":0.3},{"label":"2026-04 shelter SA MoM","value":0.6},{"label":"2026-03 shelter SA MoM","value":0.3},{"label":"2026-02 shelter SA MoM","value":0.2},{"label":"2026-01 shelter SA MoM","value":0.2},{"label":"2025-12 shelter SA MoM","value":0.4}],"drivers":["Shelter inflation slowed sharply in June but rent and OER remained positive","Lodging away from home was a one-month drag that may partly unwind","Recent seven-month shelter reference class centers near 0.30 percent","July first print resolves from the same seasonally adjusted CPI-U shelter variant"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.bls.gov/news.release/cpi.t01.htm","https://fred.stlouisfed.org/series/CUSR0000SAH1","https://alfred.stlouisfed.org/series?seid=CUSR0000SAH1"],"runAt":"2026-07-26T01:22:14Z","reasoning":[{"kind":"heading","text":"US CPI-U shelter month-over-month forecast for July 2026"},{"kind":"text","text":"Framing and exact resolver: this targets the first-print July 2026 seasonally adjusted CPI-U shelter index for U.S. city average, series CUSR0000SAH1. The ledger uses ALFRED/FRED as the first-print binding, but the economic source is BLS; FRED/ALFRED is only a history mirror."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule for the July 2026 CPI reference month.","result":"BLS lists Consumer Price Index for July 2026 on August 12, 2026 at 08:30 AM, and the June CPI release also states the July 2026 CPI is scheduled for Wednesday, August 12, 2026 at 8:30 a.m. ET."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS current CPI release Table A for the same CPI-U shelter seasonally adjusted percent-change variant.","result":"Shelter seasonally adjusted MoM percent changes were Dec 2025 0.4, Jan 2026 0.2, Feb 2026 0.2, Mar 2026 0.3, Apr 2026 0.6, May 2026 0.3, Jun 2026 0.1; the 12-month shelter change in June 2026 was 3.3."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS CPI Table 1 component details for shelter, rent, and owners' equivalent rent.","result":"In June 2026 Table 1, shelter relative importance was 35.149, shelter SA MoM was 0.1, rent of primary residence SA MoM was 0.1, and owners' equivalent rent SA MoM was 0.2."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED/ALFRED mirror for CUSR0000SAH1 index levels and latest update timing.","result":"CUSR0000SAH1 was Jun 2026 428.501, May 2026 427.998, Apr 2026 426.642, Mar 2026 424.069, Feb 2026 422.942; FRED showed updated Jul 14, 2026 8:10 AM CDT and next release date Aug 12, 2026."},{"kind":"text","text":"Reference class/base rate: the recent same-variant BLS shelter MoM reference class is the seven printed monthly changes from Dec 2025 through Jun 2026. Its mean is 0.30 percent, but the last print was 0.1 and the exact CUSR0000SAH1 index calculation gives Jun about 0.118 and May about 0.318, so the short-term trend is below the mean."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: shelter still has positive rent and OER mechanics, with June rent at 0.1 and OER at 0.2, but the aggregate was pulled down by lodging away from home falling 2.3 percent in June. I treat that lodging move as a partial one-off drag, while keeping some disinflationary momentum from the softer rent/OER prints."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the Dec 2025-Jun 2026 BLS shelter MoM mean of 0.30 percent. Updates are -0.08 for June's soft exact 0.118 reading and lower rent/OER momentum, +0.03 for partial lodging-drag reversal, and -0.01 for core services softness, giving 0.30 - 0.08 + 0.03 - 0.01 = 0.24. Interval method uses realized dispersion of the seven BLS printed shelter MoM values themselves: sigma = 0.163; 1.28*sigma = 0.209, so the 80 percent interval is 0.24 +/- 0.21 = [0.03, 0.45] after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in lodging away from home plus firmer OER that would land above the interval, especially if July shelter returns near April's 0.6. Downside risk is another weak lodging month or sharper rent slowdown that would land outside the interval below 0.03."},{"kind":"forecast","point":0.24,"ciLow":0.03,"ciHigh":0.45}]}

# Reviewer critique
{"summary":"The draft is publication-ready with only minor source-binding clarity issues around BLS versus the canonical ALFRED first-print adapter.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The JSON resolutionSourceUrl points to BLS while the canonical ledger sourceBinding is the ALFRED first-print adapter for CUSR0000SAH1; the reasoning explains this, but the structured fields could look mismatched to the target contract.","actionRequested":"Clarify in the structured resolver fields that BLS is the official economic release and ALFRED/FRED CUSR0000SAH1 is the canonical first-print binding/mirror used for the registered target, or align the URL/source field with the ledger binding while retaining BLS in the rule text."}],"optionalSuggestions":["Consider stating explicitly that no richer time-series model was used beyond the persistence/reference-class prior because the near-term sample and component judgment are more transparent for this one-month target.","The seven-month volatility basis is acceptable, but noting the small sample size would make the interval caveat cleaner."]}

Emit the final JSON object only.
