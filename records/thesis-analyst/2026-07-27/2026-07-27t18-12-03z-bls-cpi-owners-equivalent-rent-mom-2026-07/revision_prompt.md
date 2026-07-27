# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cpi.owners_equivalent_rent_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-owners-equivalent-rent-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.owners_equivalent_rent_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SEHC", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SEHC", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SEHC", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-f4b72ba7dad3ac2c455b575ad60048778d8042f7b8fd1be3f386dbf34b25af80.json"
- targetContentHash: "f4b72ba7dad3ac2c455b575ad60048778d8042f7b8fd1be3f386dbf34b25af80"
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
{"slug":"us-cpi-owners-equivalent-rent-mom-july-2026","country":"US","type":"data","title":"US CPI OER MoM, July 2026","question":"What will the first-print month-over-month percent change be for BLS CPI-U Owners' equivalent rent of residences in U.S. city average, seasonally adjusted, series CUSR0000SEHC, for July 2026?","unit":"percent_growth","pointEstimate":0.25,"ciLow":0.1,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release, CPI-U series CUSR0000SEHC","resolutionSourceUrl":"https://data.bls.gov/timeseries/CUSR0000SEHC","resolutionRule":"Resolve to the first-print July 2026 seasonally adjusted CPI-U Owners' equivalent rent of residences index for U.S. city average, series CUSR0000SEHC, released by BLS on August 12, 2026. Compute percent_growth as (July 2026 index / June 2026 index - 1) * 100 using the first published index values, rounded to two decimals for this forecast cell; ignore later revisions, annual seasonal-adjustment revisions, and ALFRED/FRED backfilled vintages.","dataPointId":"bls.cpi.owners_equivalent_rent_mom.2026_07.first_print","historicalContext":[{"label":"Jun 2026 MoM from BLS index 441.741 vs 440.683","value":0.24},{"label":"May 2026 MoM from BLS index 440.683 vs 439.379","value":0.297},{"label":"Apr 2026 MoM from BLS index 439.379 vs 437.051","value":0.533},{"label":"Mar 2026 MoM from BLS index 437.051 vs 435.813","value":0.284}],"drivers":["Recent OER monthly growth slowed to 0.24% in June after a 0.53% April spike and 0.30% May reading","June CPI release said shelter rose only 0.1% while OER rose 0.2%, favoring a below-early-2026 pace","OER is a large and lagged shelter component, so month-to-month volatility is usually limited versus energy or goods","First-print target is seasonally adjusted CPI-U series CUSR0000SEHC, not NSA shelter or rent of primary residence"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://data.bls.gov/timeseries/CUSR0000SEHC","https://www.bls.gov/news.release/cpi.nr0.htm?form=MG0AV3","https://www.bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm"],"runAt":"2026-07-27T18:12:12Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 CPI-U owners' equivalent rent MoM"},{"kind":"text","text":"Framing and exact resolver: the target is BLS CPI-U Owners' equivalent rent of residences in U.S. city average, seasonally adjusted, series CUSR0000SEHC. The forecast is the July 2026 first-print month-over-month percent change, computed from the first published July and June index levels; this uses the same seasonally adjusted variant for all anchors."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Consumer Price Index release calendar for the July 2026 reference month.","result":"BLS lists Consumer Price Index for July 2026 with release date Aug. 12, 2026 and release time 08:30 AM; adjacent CPI release rows include June 2026 on Jul. 14, 2026 and August 2026 on Sep. 11, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS public time-series table for CUSR0000SEHC, seasonally adjusted CPI-U owners' equivalent rent of residences.","result":"BLS table shows CUSR0000SEHC values: Dec 2025 433.884, Jan 2026 434.837, Feb 2026 435.813, Mar 2026 437.051, Apr 2026 439.379, May 2026 440.683, Jun 2026 441.741."},{"kind":"tool","tool":"official.lookup","call":"Checked the June 2026 BLS CPI news release for contemporaneous shelter and OER context.","result":"BLS reported all-items CPI -0.4% SA in June 2026, all items less food and energy 0.0%, shelter +0.1%, and owners' equivalent rent +0.2% in June 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS rent and owners' equivalent rent factsheet for component importance and definition context.","result":"BLS relative-importance table for December 2025 lists shelter at 35.625, owners' equivalent rent of residences at 26.204, rent of primary residence at 7.840, and lodging away from home at 1.289 percent of the CPI market basket."},{"kind":"text","text":"Base rate/reference class: using the latest continuous official CUSR0000SEHC first-print style history from Dec 2025 through Jun 2026, the six observed 2026 monthly changes are 0.220%, 0.224%, 0.284%, 0.533%, 0.297%, and 0.240%, with a mean near 0.300%. The June rounded OER print of 0.2% and the softer shelter aggregate argue for a July point below that six-month mean but not a break from the positive OER trend."},{"kind":"math","text":"Prior/update/interval: persistence prior is recent official CUSR0000SEHC MoM history, with the Jan-Jun 2026 reference class above. Adjustment components: start from the six-month mean 0.300%, subtract 0.04 pp for the latest June 0.240% value being below the mean, subtract 0.01 pp because June shelter was only 0.1%, and keep 0.00 pp for one-off energy/goods effects because they do not directly drive OER. Point = 0.300 - 0.040 - 0.010 = 0.250%. Interval method: realized sample dispersion of the six monthly OER values gives sigma = 0.118 percentage points; 1.28*sigma = 0.151 pp, so the 80% interval is about 0.250 +/- 0.151 = 0.099 to 0.401, rounded to 0.10 to 0.40."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed catch-up in sampled rents after April's 0.533% jump, which would land above the interval if July OER prints above 0.40%. Downside risk is a broad shelter deceleration following June's 0.1% shelter increase, which would land below the interval if July OER is under 0.10%. Outside the interval would likely require either another April-like rotation shock or an abrupt near-zero rent-equivalence print."},{"kind":"forecast","point":0.25,"ciLow":0.1,"ciHigh":0.4}]}

# Reviewer critique
{"summary":"Draft is mostly coherent, but its resolver/source fields do not match the canonical ledger contract and should be aligned before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft uses BLS data.bls.gov as the resolutionSourceUrl, while the canonical ledger contract specifies the alfred-fred adapter, allowed host alfred.stlouisfed.org, source URL https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SEHC, and first_print policy.","actionRequested":"Update the resolver/source fields to match the ledger sourceBinding exactly, or explicitly state in reasoning that the ledger appears to use ALFRED as the first-print capture while BLS is the originating official agency; do not leave the JSON resolver URL inconsistent with the target contract."}],"optionalSuggestions":["Clarify whether the Jan-Jun 2026 history is truly first-print vintage or current BLS table history used as a close proxy.","The interval step is strong; keep the explicit sigma and rounded bounds because they support the stated 80% interval.","Tail scenarios are concrete and target-specific enough for publication once the resolver mismatch is fixed."]}

Emit the final JSON object only.
