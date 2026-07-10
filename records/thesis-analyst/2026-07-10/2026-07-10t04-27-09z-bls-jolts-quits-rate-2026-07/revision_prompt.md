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
- targetUnit: "percent"
- dataPointId: "bls.jolts.quits_rate.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.quits_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.quits_rate", "sourceUrl": "https://www.bls.gov/news.release/jolts.t04.htm", "table": "U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4", "transform": {"factor": 1.0, "operation": "multiply"}}

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
{"slug":"jolts-quits-rate-july-2026","country":"US","type":"data","title":"US JOLTS Quits Rate, July 2026","question":"What will the BLS JOLTS total nonfarm quits rate, seasonally adjusted, be for July 2026 in the first print?","unit":"percent","pointEstimate":1.9,"ciLow":1.73,"ciHigh":2.07,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first-print July 2026 seasonally adjusted Total quits rate in BLS JOLTS Table 4, in percent/rate units as published to one decimal place; ignore later revisions or annual benchmark updates.","dataPointId":"bls.jolts.quits_rate.2026-07.first_print","historicalContext":[{"label":"May 2026 preliminary","value":1.9},{"label":"Apr 2026","value":1.9},{"label":"Mar 2026","value":2},{"label":"Feb 2026","value":1.9},{"label":"May 2025","value":2.1}],"drivers":["Recent quits rate flat at 1.9-2.0 percent","Job openings rate firmer at 4.6 percent but hires rate steady at 3.3 percent","First-print monthly noise around one tenth","Labor-market churn remains below 2021-2022 highs"],"sourceContext":["https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/schedule/news_release/jolts.htm","https://fred.stlouisfed.org/series/JTSQUR","https://www.bls.gov/news.release/jolts.t01.htm","https://www.bls.gov/news.release/jolts.t02.htm"],"runAt":"2026-07-10T04:27:20Z","reasoning":[{"kind":"heading","text":"July 2026 BLS JOLTS total nonfarm quits-rate forecast"},{"kind":"text","text":"Framing and exact resolver: this is the BLS Job Openings and Labor Turnover Survey Table 4 Total quits rate, seasonally adjusted, for July 2026, first print only. The BLS JOLTS release schedule lists reference month July 2026 for release on Sep. 01, 2026 at 10:00 AM, so I set resolutionDate to 2026-09-01 rather than inferring from cadence."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 4, quits levels and rates by industry and region, seasonally adjusted, current May 2026 release.","result":"Fetched Total quits rates: May 2025 2.1, Feb 2026 1.9, Mar 2026 2.0, Apr 2026 1.9, May 2026 preliminary 1.9; Total quits levels were 3,287k, 3,046k, 3,160k, 3,043k, and 3,065k respectively."},{"kind":"tool","tool":"public.history_mirror","call":"Check FRED JTSQUR mirror for the same BLS-sourced seasonally adjusted total nonfarm quits-rate series.","result":"Fetched JTSQUR recent observations: Jan 2026 2.0, Feb 2026 1.9, Mar 2026 2.0, Apr 2026 1.9, May 2026 1.9; FRED says units are Rate, seasonally adjusted, monthly, source U.S. Bureau of Labor Statistics, updated Jun 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Tables 1 and 2 for adjacent labor-demand indicators from the same release vintage.","result":"Fetched Total job openings rates: May 2025 4.4, Feb 2026 4.2, Mar 2026 4.2, Apr 2026 4.6, May 2026 4.6; Total hires rates: May 2025 3.4, Feb 2026 3.1, Mar 2026 3.5, Apr 2026 3.3, May 2026 3.3."},{"kind":"text","text":"Reference class and base rate: for this level/rate series I use the recent same-variant BLS seasonally adjusted Total quits-rate values as the base rate, because the target is also SA Total first print. The latest official rate is 1.9 and the five-point recent range is 1.9 to 2.1, with no evidence in the fetched data of a break away from roughly 2.0."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest same-series BLS/FRED value, 1.9. Historical sample = fetched SA Total quits rates May 2025, Feb 2026, Mar 2026, Apr 2026, May 2026: 2.1, 1.9, 2.0, 1.9, 1.9. Adjustment components: level 0.00 from latest 1.9, momentum 0.00 from Apr-to-May change 0.0, openings/hires mix +0.02 because openings rate is firm at 4.6 while hires is flat at 3.3, rounded back to the one-decimal first-print center of 1.9. For interval, successive changes are -0.2, +0.1, -0.1, 0.0; sample sigma = 0.13, so 80% half-width = 1.28*0.13 = 0.17. Final implied bounds: 1.90 - 0.17 = 1.73 and 1.90 + 0.17 = 2.07."},{"kind":"text","text":"Upside risk: July could land above the interval if the firmer openings rate translates into materially stronger quits in leisure/hospitality or retail, or if June data, not yet available at run time, jumps above 2.1. Downside risk: it would land below the interval if labor-market caution suppresses voluntary quits and total quits slip toward 1.7 or less. Outside the interval is mainly a regime-change case rather than normal one-month noise."},{"kind":"forecast","point":1.9,"ciLow":1.73,"ciHigh":2.07}]}

# Reviewer critique
{
  "summary": "Publishable after tightening the uncertainty justification; the resolver, first-print rule, date, unit, and JSON fields are otherwise coherent with the ledger target.",
  "requiredFixes": [
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval uses only four changes, including a May 2025 to February 2026 gap treated like a one-month move, and does not adjust for the May-to-July forecast horizon.",
      "actionRequested": "Recompute or justify the interval using a contiguous monthly realized-volatility sample, or explicitly state why the sparse/non-contiguous sample and one-step half-width are adequate for July 2026."
    }
  ],
  "optionalSuggestions": [
    "Mention that the BLS schedule currently lists July 2026 JOLTS for September 1, 2026 at 10:00 AM and that later schedule changes should not alter the first-print target unless the official release date changes before publication.",
    "Clarify whether the persistence prior is being used as the time-series model prior, since no separate model is estimated."
  ]
}

Emit the final JSON object only.
