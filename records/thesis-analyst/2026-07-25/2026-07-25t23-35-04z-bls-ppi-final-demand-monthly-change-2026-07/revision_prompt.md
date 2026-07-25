# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.ppi.final_demand_monthly_change
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-ppi-final-demand-monthly-change-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.wp.WPSFD4.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-19", "start": "2026-08-11"}, "field": "PPIFIS", "releasePolicy": "first_print", "sourceSeriesId": "PPIFIS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PPIFIS", "table": "Producer Price Index, final demand, seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-7753f0f1a5d658edcefcd448d480f21171af349f95e6902b968abb25deb8d3b4.json"
- targetContentHash: "7753f0f1a5d658edcefcd448d480f21171af349f95e6902b968abb25deb8d3b4"
- registrationCommit: "6d2b1a2c61155c88851ab8dad6099ae6f9ef5823"
- registeredAtUtc: "2026-07-25T23:27:53Z"

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
{"slug":"bls-ppi-final-demand-monthly-change-july-2026","country":"US","type":"data","title":"US PPI Final Demand MoM, July 2026","question":"What will the U.S. Bureau of Labor Statistics first report for the seasonally adjusted one-month percent change in the Producer Price Index for final demand for July 2026?","unit":"percent_growth","pointEstimate":0.35,"ciLow":-0.16,"ciHigh":0.86,"confidence":0.8,"resolutionDate":"2026-08-13","resolutionSource":"U.S. Bureau of Labor Statistics Producer Price Index news release, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/ppi.t01.htm","resolutionRule":"Resolve to the first BLS-published seasonally adjusted 1-month percent change for Final demand, group code FD item code 4, in the Producer Price Index news release for July 2026, scheduled for August 13, 2026 at 8:30 a.m. ET. Use the first print as published, in percent, rounded to the BLS one-decimal release value; do not replace it with later revisions.","dataPointId":"bls.wp.WPSFD4.2026-07.first_print","historicalContext":[{"label":"2026-06 final demand MoM SA first/current release","value":-0.3},{"label":"2026-05 final demand MoM SA","value":0.6},{"label":"2026-04 final demand MoM SA","value":1.1},{"label":"2026-03 final demand MoM SA","value":0.8},{"label":"2026-02 final demand MoM SA","value":0.5},{"label":"2026-01 final demand MoM SA","value":0.6},{"label":"2025-07 final demand MoM SA","value":0.8}],"drivers":["Recent final-demand PPI base rate is positive but volatile","June decline was energy-led and unlikely to repeat at the same size","Services inflation remained positive in June","July gasoline readings were rising by late month but still near or below the June monthly average","High 12-month PPI inflation keeps upside pressure on non-energy components"],"sourceContext":["https://www.bls.gov/schedule/news_release/ppi.htm","https://www.bls.gov/news.release/archives/ppi_07152026.htm","https://www.bls.gov/news.release/ppi.t01.htm","https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epm0_pte_dpgal_w.htm","https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epmr_pte_dpgal_m.htm"],"runAt":"2026-07-25T23:35:19Z","reasoning":[{"kind":"heading","text":"US PPI final demand monthly change for July 2026"},{"kind":"text","text":"Framing and exact resolver: this forecast targets the BLS Producer Price Index for final demand, seasonally adjusted, one-month percent change for July 2026, group code FD item code 4. The variant is the headline final-demand SA monthly percent change in Table 1, first print only, not the unadjusted 12-month change and not later revised data."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Producer Price Index release schedule for the July 2026 reference month.","result":"BLS lists Producer Price Index for July 2026 with release date Aug. 13, 2026 and release time 08:30 AM; the full 2026 selected-release calendar also shows Producer Price Index for July 2026 on Thursday, August 13, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest BLS PPI news release for June 2026 and Table A recent history for the same SA final-demand monthly-change variant.","result":"BLS reported final demand fell -0.3 percent in June 2026, advanced 0.6 percent in May 2026, and advanced 1.1 percent in April 2026; Table A also shows Jan. 2026 0.6, Feb. 2026 0.5, Mar. 2026 0.8, and July 2025 0.8."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Table 1 component details for the latest release to separate energy, goods, and services mechanisms.","result":"For June 2026, Table 1 shows final demand -0.3, final demand goods -1.4, final demand energy -6.4, final demand foods -0.6, goods less foods and energy 0.2, final demand services 0.2, and final demand less foods, energy, and trade services 0.1."},{"kind":"tool","tool":"official.lookup","call":"Checked EIA gasoline data as a public energy-price cross-check for July conditions before the PPI release.","result":"EIA all-grades U.S. gasoline was 4.187 on 06/15/26, 4.048 on 06/22/26, 3.964 on 06/29/26, 3.911 on 07/06/26, 3.987 on 07/13/26, and 4.131 on 07/20/26 dollars per gallon; EIA monthly regular gasoline was 4.050 in Jun-26 after 4.479 in May-26."},{"kind":"text","text":"Reference class/base rate: using the same BLS final-demand SA monthly percent-change series from June 2025 through June 2026 gives values 0.2, 0.8, -0.2, 0.6, 0.1, 0.4, 0.4, 0.6, 0.5, 0.8, 1.1, 0.6, -0.3, a base rate mean of about 0.43 percentage point per month. The recent reference class is hot but very energy-sensitive."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the Jun. 2025-Jun. 2026 BLS Table A history with mean 0.43. Adjustment components: -0.15 for June's large energy drop not fully reversing because partial July gasoline is below the June monthly average despite a late-month rise, +0.05 for still-positive services and core final-demand pressure, and +0.02 for high 5.5 percent 12-month headline PPI momentum, giving 0.43 - 0.15 + 0.05 + 0.02 = 0.35. For the 80% interval, the sample standard deviation of the 13 monthly changes is sigma = 0.40 percentage point, so half-width is roughly 1.28*sigma = 1.28*0.40 = 0.51; 0.35 +/- 0.51 gives -0.16 to 0.86."},{"kind":"text","text":"Counter-considerations: upside risk is a larger July pass-through from renewed gasoline, diesel, crude, trade-margin, or tariff-related cost pressure, which would land above the interval if headline final-demand energy and services both spike. Downside risk is a second month of falling fuels or a reversal in trade margins, which would land below the interval if final-demand goods repeat a June-like decline. An outside the interval outcome would likely require another energy shock or a broad services-margin reversal rather than ordinary monthly noise."},{"kind":"forecast","point":0.35,"ciLow":-0.16,"ciHigh":0.86}]}

# Reviewer critique
{
  "summary": "Draft is publishable with only minor clarification needed around the model-prior framing.",
  "requiredFixes": [
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a persistence/reference-class prior but does not explicitly say whether a separate time-series model was used or ruled out.",
      "actionRequested": "Add one sentence stating that no separate AR/forecasting model was used beyond the 13-month persistence/reference-class prior, or briefly describe the time-series prior if one was used."
    }
  ],
  "optionalSuggestions": [
    "Consider noting that EIA retail gasoline is only a directional energy proxy, not the PPI energy component itself.",
    "Consider explaining that the decimal point estimate and interval are forecast values even though resolution will use the BLS one-decimal first print."
  ]
}

Emit the final JSON object only.
