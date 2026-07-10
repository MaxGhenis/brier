# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.quits_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-quits-rate-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.quits_rate.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.quits_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.quits_rate", "sourceUrl": "https://www.bls.gov/news.release/jolts.t04.htm", "table": "U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-53d574820f5ef4c802754d8b06524a23672358e5dc546c4db118d3e3e5406ec7.json"
- targetContentHash: "53d574820f5ef4c802754d8b06524a23672358e5dc546c4db118d3e3e5406ec7"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

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
{"slug":"jolts-quits-rate-july-2026","country":"US","type":"data","title":"US JOLTS quits rate, July 2026","question":"BLS Job Openings and Labor Turnover Survey Table 4 total quits rate, seasonally adjusted, July 2026, first print","unit":"percent","pointEstimate":1.9,"ciLow":1.75,"ciHigh":2.05,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first-print July 2026 seasonally adjusted Total quits rate in BLS JOLTS Table 4, 'Quits levels and rates by industry and region, seasonally adjusted', using the rate value in percent as published at the September 1, 2026 10:00 AM ET release. Do not use later revisions or annual benchmark updates.","dataPointId":"bls.jolts.quits_rate.2026-07.first_print","historicalContext":[{"label":"2026-05 preliminary total quits rate, SA","value":1.9},{"label":"2026-04 total quits rate, SA","value":1.9},{"label":"2026-03 total quits rate, SA","value":2.0},{"label":"2026-02 total quits rate, SA","value":1.9},{"label":"2025-05 total quits rate, SA","value":2.1}],"drivers":["latest total quits rate was 1.9 percent","recent total quits rate changes were small","private quits rate held at 2.1 percent","government quits rate remained 0.8 percent","leisure and hospitality rebound offsets softer health care and construction"],"sourceContext":["https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/schedule/2026/09_sched.htm"],"runAt":"2026-07-10T05:20:37Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS JOLTS total quits rate"},{"kind":"text","text":"Framing and exact resolver: this is the seasonally adjusted Total quits rate in BLS JOLTS Table 4, not the quits level, not not-seasonally-adjusted data, and not a revised vintage. The series code context is BLS JOLTS total nonfarm quits rate, and the ledger source URL points to Table 4."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule by release name and the September 2026 BLS calendar for the July 2026 reference month.","result":"BLS schedule lists July 2026 Job Openings and Labor Turnover Survey for Sep. 01, 2026 at 10:00 AM; it also lists June 2026 on Aug. 04, 2026 and August 2026 on Sep. 29, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current BLS JOLTS Table 4 Total row for seasonally adjusted quits levels and rates.","result":"Fetched Total quits levels and rates: May 2025 level 3,287 and rate 2.1; Feb. 2026 level 3,046 and rate 1.9; Mar. 2026 level 3,160 and rate 2.0; Apr. 2026 level 3,043 and rate 1.9; May 2026 preliminary level 3,065 and rate 1.9; Apr.-May 2026 rate change 0.0."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Table 4 industry rows to check whether total quits pressure was broad or sector-specific.","result":"Fetched industry rates for May 2026: total private 2.1, construction 1.3, manufacturing 1.4, retail trade 2.8, professional and business services 2.0, health care and social assistance 1.7, leisure and hospitality 4.0, government 0.8."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Table 4 regional rows to check geographic dispersion in the latest quits rate print.","result":"Fetched regional May 2026 quits rates: Northeast 1.4, South 2.3, Midwest 1.9, West 1.7; the Apr.-May 2026 regional changes were +0.1, +0.1, -0.1, and -0.2 respectively."},{"kind":"text","text":"Reference class and base rate: for a monthly level/rate series this close to release, the strongest outside-view anchor is persistence in the same SA total-rate series. The recent official reference class has total rates 1.9, 2.0, 1.9, and 1.9 from February through May 2026, with May 2025 at 2.1, so the base rate is near 1.9 rather than a return toward the 2021-2022 high-quits regime."},{"kind":"text","text":"Current-release adjustment: May 2026 was flat at 1.9 despite offsetting industry moves. Leisure and hospitality rose to 4.0 and other services to 2.5, but health care and social assistance eased to 1.7 and construction fell to 1.3. That mix argues for no material level adjustment from the 1.9 persistence prior."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official SA total quits rate of 1.9 using the February-May 2026 BLS Table 4 reference class. Successive monthly changes are +0.1, -0.1, and 0.0 percentage point, so sigma = 0.08 percentage point on those changes. The one-month 80% half-width is about 1.28*sigma = 1.28*0.08 = 0.10; for a two-reference-month horizon from May to July, scale by sqrt(2), giving 0.14, rounded to a 0.15 percentage point half-width. Point = 1.9 + 0.0 level/momentum adjustment = 1.9; 80% interval = 1.9 +/- 0.15 = [1.75, 2.05]."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed rise in voluntary separations if leisure, retail, and professional services all firm together, which would land above the interval at 2.1 or higher after one-decimal BLS rounding. Downside risk is a sharper labor-demand slowdown with quits falling across private services and government staying subdued, which would land below the interval at 1.7 or lower."},{"kind":"forecast","point":1.9,"ciLow":1.75,"ciHigh":2.05}]}

# Reviewer critique
{
  "summary": "Draft is publishable with no blocking issues; the main weakness is that the interval volatility estimate rests on only three monthly changes.",
  "requiredFixes": [
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is derived from only three recent monthly changes, which is a very small realized-volatility sample for calibrating uncertainty.",
      "actionRequested": "Broaden the historical volatility sample or explicitly state that the narrow recent-change sample is being used as a judgmental short-run uncertainty proxy."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that BLS reports the target rate in percent and normally to one decimal, while the forecast interval is expressed on the underlying percent scale.",
    "Mention that the release date is tied to the BLS July 2026 JOLTS schedule entry on September 1, 2026, not inferred from monthly cadence."
  ]
}

Emit the final JSON object only.
