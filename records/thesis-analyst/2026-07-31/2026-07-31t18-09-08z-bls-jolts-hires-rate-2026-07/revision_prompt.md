# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.hires_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-hires-rate-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.hires_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "JTSHIR", "releasePolicy": "first_print", "sourceSeriesId": "JTSHIR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=JTSHIR", "table": "JOLTS news release, Table 1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-e671b0edb90aafc5fc73877f6a8d96e8c7fcb0a1580cbaa97f206d4e787cc5d8.json"
- targetContentHash: "e671b0edb90aafc5fc73877f6a8d96e8c7fcb0a1580cbaa97f206d4e787cc5d8"
- registrationCommit: "7ecbc85cc4110060218f856d50321ab93db3af3b"
- registeredAtUtc: "2026-07-31T18:02:17Z"

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
{"slug":"jolts-hires-rate-july-2026","country":"US","type":"data","title":"US JOLTS hires rate, July 2026","question":"What will the BLS first-print seasonally adjusted total nonfarm hires rate be for July 2026 in the Job Openings and Labor Turnover Survey?","unit":"percent","pointEstimate":3.3,"ciLow":3.1,"ciHigh":3.5,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey","resolutionSourceUrl":"https://data.bls.gov/timeseries/JTS000000000000000HIR","resolutionRule":"Resolve to the first value published by BLS for the seasonally adjusted total nonfarm hires rate, series JTS000000000000000HIR / FRED mirror JTSHIR, for July 2026 in the JOLTS release. The unit is percent, rounded to one decimal. Use the first official print only; ignore later monthly revisions, annual benchmark revisions, and later vintage changes except as archival evidence of the first print.","dataPointId":"bls.jolts.hires_rate.2026_07.first_print","historicalContext":[{"label":"May 2026 latest SA total nonfarm hires rate","value":3.3},{"label":"April 2026 SA total nonfarm hires rate","value":3.3},{"label":"March 2026 SA total nonfarm hires rate","value":3.5},{"label":"February 2026 SA total nonfarm hires rate","value":3.1},{"label":"January 2026 SA total nonfarm hires rate","value":3.4},{"label":"July 2025 SA total nonfarm hires rate","value":3.3}],"drivers":["Recent hires rate has been pinned near 3.3 percent","May 2026 BLS release described hires as unchanged at 5.2 million and 3.3 percent","Low labor-market churn keeps the persistence prior strong","Two-month forecast horizon allows June and July volatility but not a regime-break assumption","First-print rounded-to-one-decimal target makes 3.3 the modal bin"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm?stream=business","https://www.bls.gov/schedule/2026/","https://www.bls.gov/news.release/archives/jolts_06302026.htm","https://fred.stlouisfed.org/data/JTSHIR","https://data.bls.gov/timeseries/JTS000000000000000HIR"],"runAt":"2026-07-31T18:09:36Z","reasoning":[{"kind":"heading","text":"US JOLTS total nonfarm hires rate, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast is for the BLS JOLTS seasonally adjusted total nonfarm hires rate, series JTS000000000000000HIR, mirrored as JTSHIR, for reference month July 2026. The release variant is seasonally adjusted, total nonfarm, rate, first print, in percent rounded to one decimal."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule page for the reference-month release date.","result":"The BLS schedule lists July 2026 JOLTS for Sep. 01, 2026 at 10:00 AM, June 2026 JOLTS for Aug. 04, 2026 at 10:00 AM, and August 2026 JOLTS for Sep. 29, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS 2026 selected-release calendar as an official date cross-check.","result":"The September 2026 calendar lists Tuesday, September 1, 2026 at 10:00 AM for Job Openings and Labor Turnover Survey for July 2026; the August 2026 calendar lists Tuesday, August 04, 2026 at 10:00 AM for June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS May 2026 JOLTS release archive and Table A / Table 1 text for the latest official print available before this run.","result":"For May 2026, BLS reported hires unchanged at 5.2 million and the hires rate unchanged at 3.3 percent; Table A showed total hires of 5,170 thousand in May 2026, 5,215 thousand in April 2026, and 5,328 thousand in May 2025, with rates of 3.3, 3.3, and 3.4 percent respectively."},{"kind":"tool","tool":"history.lookup","call":"Read FRED/ALFRED public JTSHIR history as a mirror of BLS series JTS000000000000000HIR.","result":"Recent JTSHIR values were May 2026 3.3, Apr 2026 3.3, Mar 2026 3.5, Feb 2026 3.1, Jan 2026 3.4, Dec 2025 3.3, Nov 2025 3.2, Oct 2025 3.3, Sep 2025 3.3, and Aug 2025 3.2 percent."},{"kind":"tool","tool":"history.lookup","call":"Pulled a recent reference-class window from the FRED JTSHIR table for realized dispersion and persistence checks.","result":"The 2024-01 through 2026-05 rate path included 2024-01 3.6, 2024-06 3.3, 2024-12 3.3, 2025-06 3.4, 2025-07 3.3, 2025-12 3.3, 2026-01 3.4, 2026-02 3.1, 2026-03 3.5, 2026-04 3.3, and 2026-05 3.3 percent."},{"kind":"text","text":"Reference class and base rate: since early 2024 the total nonfarm seasonally adjusted hires rate has mostly sat in a narrow 3.2 to 3.6 percent band, with July 2025 at 3.3 percent and the latest May 2026 print also 3.3 percent. That makes a persistence base rate around 3.3 percent the right starting point."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest May 2026 value of 3.3 percent, with a small level adjustment of 0.0 because BLS described hires as unchanged and recent churn indicators were stable; momentum adjustment = 0.0 because Apr-to-May was 0.0 and the recent 3-month average is about (3.5+3.3+3.3)/3 = 3.37, which rounds near 3.3; one-off/policy adjustment = 0.0 because there is no official-source evidence of a July hiring regime break. For the 2024-01 to 2026-05 fetched window, successive monthly changes have sample sigma = 0.13 percentage point; 80 percent half-width = 1.28*sigma = 1.28*0.13 = 0.166 percentage point, rounded to the one-decimal target as about 0.2. Final implied bounds: 3.3 - 0.2 = 3.1 and 3.3 + 0.2 = 3.5."},{"kind":"text","text":"Counter-considerations: upside risk would come from summer leisure, retail, or government hiring rebounding enough to push the rounded first print to 3.6 or higher, which would land above the interval. Downside risk would come from a broad hiring freeze or sharp payroll slowdown pushing the first print to 3.0 or lower, which would land outside the interval below. The middle case is that low churn persists and July rounds to 3.3."},{"kind":"forecast","point":3.3,"ciLow":3.1,"ciHigh":3.5}]}

# Reviewer critique
{
  "summary": "Draft is publishable after aligning the resolver/source fields to the canonical ALFRED first-print binding and tightening the interval method for the two-month horizon.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "Resolution source fields do not match the canonical ledger binding: the draft uses a BLS timeseries URL while the target contract binds first-print resolution to ALFRED/FRED series JTSHIR at the ALFRED CSV URL.",
      "actionRequested": "Set the resolver/source text and URL to the canonical ALFRED first-print binding for JTSHIR while preserving the explanation that it mirrors the BLS JOLTS Table 1 hires-rate first print."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The interval uses one-month change sigma even though the forecast horizon is effectively May-to-July with June still unknown.",
      "actionRequested": "Either compute realized two-month changes for the historical sample or explicitly justify why the one-month sigma is adequate for a two-month-ahead rounded first-print target."
    }
  ],
  "optionalSuggestions": [
    "In the Prior/update/interval step, name the historical sample as 2024-01 through 2026-05 and clarify whether sigma is from one-month or target-horizon changes.",
    "Keep the BLS schedule evidence for the 2026-09-01 release date; it is coherent with the target."
  ]
}

Emit the final JSON object only.
