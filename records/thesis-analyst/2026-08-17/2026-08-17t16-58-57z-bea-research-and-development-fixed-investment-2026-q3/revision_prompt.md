# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.research_and_development_fixed_investment
- period: 2026-Q3
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-private-research-development-fixed-investment-q3-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.research_and_development_fixed_investment.2026_q3.first_print"
- expectedReleaseWindow: {"end": "2026-10-29", "start": "2026-10-29"}
- sourceBinding: {"adapter": "bea-release", "allowedHosts": ["apps.bea.gov", "www.bea.gov"], "expectedReleaseWindow": {"end": "2026-10-29", "start": "2026-10-29"}, "field": "Line 18: Research and development", "releasePolicy": "first_print", "sourceSeriesId": "T50305:L18", "sourceUrl": "https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey", "table": "Gross Domestic Product advance release, NIPA Table 5.3.5, line 18 (Research and development)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-17-a80665069544aa19303c03ea1fb560eba0b15bc2443c19c8b09bfe4d9f0f3ac1.json"
- targetContentHash: "a80665069544aa19303c03ea1fb560eba0b15bc2443c19c8b09bfe4d9f0f3ac1"
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
{"slug":"us-private-research-development-fixed-investment-q3-2026","country":"US","type":"data","title":"US private R&D fixed investment, Q3 2026","question":"What will BEA report as the first-print nominal seasonally adjusted annual-rate value for private fixed investment in research and development, NIPA Table 5.3.5 line 18, in 2026-Q3?","unit":"usd_billions","pointEstimate":964,"ciLow":934,"ciHigh":994,"confidence":0.8,"resolutionDate":"2026-10-29","resolutionSource":"U.S. Bureau of Economic Analysis GDP advance release, NIPA Table 5.3.5 line 18","resolutionSourceUrl":"https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey","resolutionRule":"Resolve to the first official BEA GDP advance-release print for 2026-Q3, NIPA Table 5.3.5, line 18 Research and development, nominal seasonally adjusted annual rate. Use the published table value transformed by multiplying the table's millions-of-dollars value by 0.001 to usd_billions, retaining the precision implied by the official table; do not use later second, third, annual-update, or comprehensive-revision values except insofar as BEA has already incorporated them into the first Q3 advance-release table on 2026-10-29.","dataPointId":"bea.research_and_development_fixed_investment.2026_q3.first_print","historicalContext":[{"period":{"type":"quarter","value":"2025-Q1"},"label":"2025-Q1","value":817.78},{"period":{"type":"quarter","value":"2025-Q2"},"label":"2025-Q2","value":829.769},{"period":{"type":"quarter","value":"2025-Q3"},"label":"2025-Q3","value":855.584},{"period":{"type":"quarter","value":"2025-Q4"},"label":"2025-Q4","value":881.507},{"period":{"type":"quarter","value":"2026-Q1"},"label":"2026-Q1","value":909.507},{"period":{"type":"quarter","value":"2026-Q2"},"label":"2026-Q2","value":937.772}],"drivers":["recent nominal R&D investment level rose in each listed quarter","Q2 advance release reported current-dollar GDP up 7.9 percent SAAR","BEA said Q2 intellectual property products growth included research and development","September 2026 annual update can rebase the level before the Q3 advance print","advance GDP estimates use partial source data and BEA projections"],"sourceContext":["https://www.bea.gov/news/schedule/full","https://www.bea.gov/news/2026/gdp-advance-estimate-2nd-quarter-2026","https://fred.stlouisfed.org/series/Y006RC1Q027SBEA","https://alfred.stlouisfed.org/release?et=&ob=pv&od=desc&pageID=1&rd=2025-06-26&rid=53&t=nonresidential","https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey"],"runAt":"2026-08-17T16:59:05Z","reasoning":[{"kind":"heading","text":"US private research and development fixed investment, 2026-Q3 first print"},{"kind":"text","text":"Resolver framing: this is BEA NIPA Table 5.3.5 line 18, Research and development, nominal seasonally adjusted annual rate. The registered target unit is usd_billions, so the resolver multiplies BEA's table value in millions by 0.001. The exact source concept is T50305:L18, mirrored by FRED/ALFRED series Y006RC1Q027SBEA."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's 2026 release schedule and the current GDP advance-release page for the release date and current macro context.","result":"BEA's schedule lists GDP (Advance Estimate), 3rd Quarter 2026 on October 29, 2026 at 8:30 AM; the Q2 2026 advance release reported real GDP +1.5 percent SAAR, current-dollar GDP +7.9 percent SAAR, real final sales to private domestic purchasers +3.9 percent, and PCE prices +5.1 percent."},{"kind":"text","text":"Variant check: all historical anchors are the same nominal seasonally adjusted annual-rate R&D fixed-investment variant as the target, not real growth rates, not annual data, and not government R&D."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest FRED public BEA mirror for Y006RC1Q027SBEA, the BEA R&D fixed-investment series corresponding to NIPA Table 5.3.5 line 18.","result":"The fetched recent values were 2025-Q2 829.769, 2025-Q3 855.584, 2025-Q4 881.507, 2026-Q1 909.507, and 2026-Q2 937.772 usd_billions; FRED identifies the source as BEA, release Gross Domestic Product, units billions of dollars SAAR, quarterly."},{"kind":"tool","tool":"official.lookup","call":"Checked ALFRED's GDP release history for the same BEA/FRED series to extend the recent reference class back one additional distinct quarter.","result":"The ALFRED GDP release page for the nonresidential tag shows Y006RC1Q027SBEA, Gross Private Domestic Investment: Fixed Investment: Nonresidential: Intellectual Property Products: Research and Development, with Q1 2025 at 817.780 usd_billions on the 2025-06-26 release page."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's Q2 2026 advance-release technical notes for source-data mechanisms relevant to the next advance print.","result":"BEA reported that Q2 investment increased while imports increased; within investment, intellectual property products increased and BEA explicitly attributed the R&D component to a judgmental trend and BLS Current Employment Statistics, while nonresidential structures decreased."},{"kind":"text","text":"Base rate/reference class: over the six fetched quarterly levels from 2025-Q1 through 2026-Q2, the five one-quarter changes were +11.989, +25.815, +25.923, +28.000, and +28.265 usd_billions, for a mean base rate of about +23.998 usd_billions per quarter."},{"kind":"math","text":"Prior/update/interval: persistence prior is the last fetched level, 937.772, plus the 2025-Q1 to 2026-Q2 mean quarterly change of 23.998, giving 961.770. I add about 2.2 for continued Q2 nominal momentum and R&D support from software, AI, and professional payroll trends, giving a point estimate of 964. For interval sizing, sigma is computed from the fetched successive quarterly level changes: sigma = 6.809 usd_billions, so 1.28*sigma = 8.715. I widen to a 30 usd_billions half-width because the Q3 first print follows BEA's September 30, 2026 annual update and the advance estimate uses partial source data plus projections; final bounds are 964-30=934 and 964+30=994."},{"kind":"text","text":"Upside risk: a stronger AI/software capex wave, stronger Q3 nominal GDP, or an upward annual-update level revision would land above the interval. Downside risk: weaker professional and technical payroll inputs, slower corporate R&D capitalization, or a downward annual-update rebasing would land below the interval. An outside the interval outcome would most likely require both a large annual-update level shift and an unusually large Q3 R&D source-data surprise."},{"kind":"forecast","point":964,"ciLow":934,"ciHigh":994}]}

# Reviewer critique
{
  "summary": "Draft is publishable with no blocking issues; resolver, unit, first-print rule, prior/update/interval structure, and JSON fields are coherent.",
  "requiredFixes": [
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The +2.2 inside-view adjustment cites software, AI, and professional payroll trends, but the shown evidence only directly supports recent BEA R&D/IPP strength and Q2 macro context.",
      "actionRequested": "Either tie the +2.2 adjustment only to the cited BEA/FRED evidence or add a cited public source for the software/AI/professional-payroll claim."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that FRED/ALFRED are mirrors only and BEA is the resolving source.",
    "Clarify whether the 30 billion half-width is judgmental widening beyond realized recent-quarter volatility rather than mechanically implied by the five-change sample."
  ]
}

Emit the final JSON object only.
