# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.quits_rate
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-quits-rate-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.quits_rate.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-10-05", "start": "2026-09-27"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-10-05", "start": "2026-09-27"}, "field": "bls.jolts.quits_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.quits_rate", "sourceUrl": "https://www.bls.gov/news.release/jolts.t04.htm", "table": "U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-918146c0e3bb21526c56eb23c225d8c6f3541e00414806667c0a943eb10a6b6f.json"
- targetContentHash: "918146c0e3bb21526c56eb23c225d8c6f3541e00414806667c0a943eb10a6b6f"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"

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
  "unit": "percent|count|thousands|millions|usd|usd_millions|usd_billions|gbp_billions|ratio|percent_growth",
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

Emit the final JSON object only. (agent thesis.analyst v2.5.7, prompt a954cfd8c691, tools 024388e49298, promptMode fast)


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
{"slug":"jolts-quits-rate-august-2026","country":"US","type":"data","title":"US JOLTS quits rate, Aug. 2026","question":"What will the U.S. Bureau of Labor Statistics JOLTS Table 4 seasonally adjusted Total nonfarm quits rate be for August 2026 in the first print?","unit":"percent","pointEstimate":1.9,"ciLow":1.7,"ciHigh":2.1,"confidence":0.8,"resolutionDate":"2026-09-29","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first BLS-published seasonally adjusted Total nonfarm quits rate in JOLTS Table 4 for August 2026, reported as a percent and rounded as BLS publishes it. Use the first print only; ignore later revisions.","dataPointId":"bls.jolts.quits_rate.2026-08.first_print","historicalContext":[{"label":"June 2025 SA Total quits rate","value":2.1},{"label":"March 2026 SA Total quits rate","value":2},{"label":"April 2026 SA Total quits rate","value":1.9},{"label":"May 2026 SA Total quits rate","value":2},{"label":"June 2026 SA Total quits rate","value":2}],"drivers":["Recent BLS Table 4 Total nonfarm quits rate is stable around 2.0 percent","July payroll employment weakness lowers worker-confidence and voluntary-quit pressure","June JOLTS openings and hires were little changed, arguing against a sharp break","Resolution is the seasonally adjusted Total nonfarm rate, not the Total private or not seasonally adjusted variant"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/news.release/jolts.nr0.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/series/JTSQUR"],"runAt":"2026-08-11T13:04:34Z","reasoning":[{"kind":"heading","text":"Forecast for BLS JOLTS quits rate, August 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is BLS JOLTS Table 4, seasonally adjusted Total nonfarm quits rate, series JTSQUR in FRED mirror terms, for August 2026. The resolver is the BLS first print on the Table 4 release page, not FRED, not Total private, and not the not-seasonally-adjusted Table 11 variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule page for the August 2026 reference month.","result":"The BLS schedule lists August 2026 JOLTS for Sep. 29, 2026 at 10:00 AM, with July 2026 on Sep. 1, 2026 and September 2026 on Nov. 3, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched current BLS JOLTS Table 4, seasonally adjusted quits levels and rates by industry and region.","result":"For Total, BLS Table 4 shows quits rates of 2.1 in June 2025, 2.0 in March 2026, 1.9 in April 2026, 2.0 in May 2026, and 2.0 in June 2026; levels were 3,254 thousand, 3,160 thousand, 3,043 thousand, 3,153 thousand, and 3,232 thousand respectively."},{"kind":"tool","tool":"official.lookup","call":"Fetched the BLS JOLTS June 2026 summary for broader turnover conditions.","result":"The June 2026 JOLTS summary reported job openings at 7.4 million, hires at 5.3 million, total separations at 5.4 million, quits at 3.2 million, and the quits rate at 2.0 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetched the BLS Employment Situation for July 2026 as a contemporaneous labor-market signal before the August JOLTS period.","result":"The July 2026 Employment Situation reported nonfarm payroll employment of -23,000, unemployment rate of 4.1 percent, May and June payroll revisions totaling -103,000, labor-force participation at 61.4 percent, and average hourly earnings up 3.2 percent over the year."},{"kind":"text","text":"Reference class and base rate: for a low-volatility rate series like Total nonfarm quits, the strongest base rate is persistence around the latest official BLS Table 4 level. The recent official reference class averages about 2.0 percent across June 2025 and March-June 2026, with the sequential 2026 observations centered just under 2.0."},{"kind":"math","text":"Prior/update/interval: persistence model prior = latest official June 2026 rate of 2.0 percent, historical sample = BLS Table 4 seasonally adjusted Total rates for March-June 2026 of 2.0, 1.9, 2.0, 2.0; adjustment components = -0.05 for weaker July payrolls and downward revisions, -0.02 for lower participation/worker-confidence pressure, +0.02 for still-stable JOLTS openings and hires, rounded to a -0.1 point net forecast adjustment over July-August; interval method = sample sigma of monthly changes from March-June changes (-0.1, +0.1, 0.0) is sigma = 0.10 for one month, two-month sigma = sqrt(2)*0.10 = 0.14, 80 percent half-width = 1.28*0.14 = 0.18, rounded to 0.2; final implied bounds are 1.9 - 0.2 = 1.7 and 1.9 + 0.2 = 2.1."},{"kind":"text","text":"Counter-considerations: upside risk would come from a July or August rebound in labor demand that lifts quits back above 2.1, especially in leisure, retail, or professional services. Downside risk would come from a clearer labor-market break after the -23,000 July payroll print; a broad pullback in voluntary separations would land below the interval if the first-print rate is under 1.7."},{"kind":"forecast","point":1.9,"ciLow":1.7,"ciHigh":2.1}]}

# Reviewer critique
{
  "summary": "Draft is publishable with no blocking issues; resolver, prior/update/interval logic, tails, and JSON fields are coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider making the resolution-date note explicitly say Sep. 29, 2026 is within the registered expected release window of Sep. 27-Oct. 5, 2026.",
    "The inside-view adjustment is directionally plausible but small; keeping it rounded to -0.1 is acceptable."
  ]
}

Emit the final JSON object only.
