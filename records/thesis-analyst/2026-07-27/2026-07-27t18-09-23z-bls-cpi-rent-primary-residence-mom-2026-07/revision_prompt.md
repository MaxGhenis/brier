# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cpi.rent_primary_residence_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-primary-rent-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.rent_primary_residence_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SEHA", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SEHA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SEHA", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-68ada9204070c13b03e259eb171ac8fc62e5b065f182f8ae9d1f736b2483025b.json"
- targetContentHash: "68ada9204070c13b03e259eb171ac8fc62e5b065f182f8ae9d1f736b2483025b"
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
{"slug":"us-cpi-primary-rent-mom-july-2026","country":"US","type":"data","title":"US CPI Primary Rent MoM, July 2026","question":"BLS CPI-U Rent of Primary Residence in U.S. city average (CUSR0000SEHA), July 2026, seasonally adjusted month-over-month percent growth, first official print","unit":"percent_growth","pointEstimate":0.22,"ciLow":0.09,"ciHigh":0.35,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release","resolutionSourceUrl":"https://data.bls.gov/timeseries/CUSR0000SEHA","resolutionRule":"Resolve to the first official BLS print for July 2026 CPI-U rent of primary residence, U.S. city average, seasonally adjusted series CUSR0000SEHA. Compute percent growth as 100*(July 2026 first-vintage index / June 2026 first-vintage index - 1), in percentage points, with no later revisions or same-day correction grace unless BLS replaces the first print before publication.","dataPointId":"bls.cpi.rent_primary_residence_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 exact derived MoM from FRED level","value":0.1495},{"label":"2026-05 exact derived MoM from FRED level","value":0.3619},{"label":"2026-04 exact derived MoM from FRED level","value":0.5451},{"label":"2026-03 exact derived MoM from FRED level","value":0.1901},{"label":"BLS rounded 2026-06 SA MoM table value","value":0.1}],"drivers":["Latest rounded BLS table shows primary rent slowing to 0.1 percent SA MoM in June after 0.4 in May and 0.5 in April","Exact index-derived June growth was 0.1495 percent, below the recent valid-change mean of 0.2674 percent","Rent inflation is sticky and lagged, so one low month should pull the forecast down but not to zero","Recent dispersion from valid one-month changes supports an 80 percent band of about plus or minus 0.13 percentage point"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.t02.htm","https://fred.stlouisfed.org/data/CUSR0000SEHA","https://alfred.stlouisfed.org/series?seid=CUSR0000SEHA"],"runAt":"2026-07-27T18:09:42Z","reasoning":[{"kind":"heading","text":"US CPI primary rent MoM forecast for July 2026"},{"kind":"text","text":"Framing and exact resolver: this targets the seasonally adjusted CPI-U rent of primary residence index for the U.S. city average, series CUSR0000SEHA, converted to month-over-month percent growth for July 2026 on the first official BLS print. The variant is seasonally adjusted, U.S. city average, not regional, not unadjusted, and not owners' equivalent rent."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule for the July 2026 reference month.","result":"BLS lists Consumer Price Index for July 2026 with release date Aug. 12, 2026 and release time 08:30 AM; the adjacent June 2026 CPI release is listed for Jul. 14, 2026 at 08:30 AM."},{"kind":"tool","tool":"fred.lookup","call":"Fetched the latest CUSR0000SEHA seasonally adjusted index levels from the public FRED table, a BLS-sourced history mirror.","result":"CUSR0000SEHA levels: Feb 2026 441.865, Mar 2026 442.705, Apr 2026 445.118, May 2026 446.729, Jun 2026 447.397; source labels the series as Index 1982-1984=100, Seasonally Adjusted, Monthly, last updated 2026-07-14 8:10 AM CDT."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS CPI Table 2 for the latest same-variant rounded percent-change row.","result":"BLS Table 2 for June 2026 shows Rent of primary residence relative importance 7.680, Jun 2025-Jun 2026 unadjusted percent change 2.8, May 2026-Jun 2026 unadjusted percent change 0.1, and seasonally adjusted percent changes Mar-Apr 0.5, Apr-May 0.4, May-Jun 0.1."},{"kind":"tool","tool":"fred.history","call":"Computed recent exact one-month percent changes from fetched CUSR0000SEHA levels, excluding the missing Oct 2025 FRED observation for the change calculation.","result":"Exact derived MoM values used for the reference class include Feb 2025 0.2869, Mar 2025 0.3084, Apr 2025 0.3239, May 2025 0.2298, Jun 2025 0.2292, Jul 2025 0.2338, Aug 2025 0.2853, Sep 2025 0.2156, Dec 2025 0.2704, Jan 2026 0.2490, Feb 2026 0.1314, Mar 2026 0.1901, Apr 2026 0.5451, May 2026 0.3619, Jun 2026 0.1495 percent."},{"kind":"text","text":"Base rate/reference class: the 15 valid recent exact index-derived monthly changes average 0.2674 percent. The latest rounded BLS table and exact June calculation point lower than that base rate, while the April and May prints argue against assuming the series has fully reset to a very low monthly pace."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent valid-change mean from CUSR0000SEHA, 0.2674 percent. Adjustment components: -0.06 pp for June's low exact 0.1495 percent and rounded BLS 0.1 percent signal, +0.01 pp for sticky rent renewal inertia, and +0.00 pp for no identified July-specific policy break, giving 0.2674 - 0.06 + 0.01 = 0.2174, rounded to 0.22. Interval method uses the sample standard deviation of the 15 valid recent exact MoM values: sigma = 0.099 percentage point. The 80 percent normal half-width is roughly 1.28*sigma = 1.28*0.099 = 0.127 percentage point, so 0.22 +/- 0.13 gives 0.09 to 0.35 after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a repeat of the April-May rebound in sampled rents or seasonal adjustment that would land above the interval, above 0.35 percent. Downside risk is another very soft rent sample or a correction in lagged market rents that would land below the interval, below 0.09 percent. Outside the interval would most likely reflect a data-processing or sampling surprise rather than a visible release-calendar issue."},{"kind":"forecast","point":0.22,"ciLow":0.09,"ciHigh":0.35}]}

# Reviewer critique
{
  "summary": "Draft is mostly coherent, but it should align the resolver/source fields to the canonical ledger source binding before publication.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft uses BLS/data.bls.gov as the resolution source URL, while the ledger contract binds this target to the ALFRED-FRED adapter, allowed host alfred.stlouisfed.org, source URL alfredgraph.csv?id=CUSR0000SEHA, and first-print policy.",
      "actionRequested": "Change the resolution source/source URL and resolver wording to explicitly match the ledger sourceBinding, while preserving that the target is the first official print for CUSR0000SEHA and noting any BLS-vs-ALFRED discrepancy in reasoning if needed."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a recent-change persistence prior, but it does not clearly state whether a formal time-series/model prior was used or deliberately ruled out.",
      "actionRequested": "Add one compact sentence saying the model prior is a simple persistence/recent-mean prior, or explicitly state that no AR/ETS/time-series model was used and why."
    }
  ],
  "optionalSuggestions": [
    "Clarify that ALFRED/FRED history is used only to recover the first-vintage CUSR0000SEHA index levels for the ledger resolver, not as a subjective alternate resolver.",
    "In the final JSON, ensure resolutionDate, dataPointId, unit, point, interval, and confidence remain exactly consistent with the stated forecast step."
  ]
}

Emit the final JSON object only.
