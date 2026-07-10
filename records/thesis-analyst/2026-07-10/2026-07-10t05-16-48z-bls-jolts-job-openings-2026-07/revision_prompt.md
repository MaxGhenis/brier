# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.job_openings
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-openings-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.jolts.job_openings.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.job_openings", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.job_openings", "sourceUrl": "https://www.bls.gov/news.release/jolts.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-21e06e0656e420fc38e5db6513825baad3becf73234e1df0a074fcadcc13535f.json"
- targetContentHash: "21e06e0656e420fc38e5db6513825baad3becf73234e1df0a074fcadcc13535f"
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
{"slug":"jolts-openings-july-2026","country":"US","type":"data","title":"US JOLTS job openings, July 2026","question":"What will BLS first report for total nonfarm job openings, seasonally adjusted, in the July 2026 Job Openings and Labor Turnover Survey release?","unit":"millions","pointEstimate":7.29,"ciLow":6.74,"ciHigh":7.84,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.nr0.htm","resolutionRule":"Resolve to the first BLS Job Openings and Labor Turnover Survey news-release print for total nonfarm job openings, seasonally adjusted, for July 2026, reported in thousands and converted to millions by multiplying by 0.001. Use the value first published in the September 1, 2026 10:00 AM ET release; ignore later revisions and database updates after the first print.","dataPointId":"bls.jolts.job_openings.july_2026.first_print","historicalContext":[{"label":"2026-05 job openings SA total nonfarm, preliminary","value":7.594},{"label":"2026-04 job openings SA total nonfarm","value":7.585},{"label":"2026-03 job openings SA total nonfarm","value":6.887},{"label":"2026-02 job openings SA total nonfarm","value":6.922},{"label":"2026-01 job openings SA total nonfarm","value":7.24}],"drivers":["May JOLTS openings held near the April rebound at 7.594 million","June payroll employment rose only 57 thousand, arguing against a sustained openings surge","Unemployment was 4.2 percent in June, still consistent with a cooler labor market than 2022-2023","Two-month-ahead JOLTS prints are volatile, so the interval is wider than a one-month persistence band"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://data.bls.gov/timeseries/JTS000000000000000JOL","https://data.bls.gov/timeseries/CES0000000001","https://data.bls.gov/timeseries/LNS14000000"],"runAt":"2026-07-10T05:17:14Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 first-print JOLTS job openings"},{"kind":"text","text":"Framing: the target is BLS series JTS000000000000000JOL, total nonfarm job openings, seasonally adjusted, level in thousands, converted to millions. The BLS schedule page verifies that the July 2026 JOLTS reference month is scheduled for release on 2026-09-01 at 10:00 AM, so the ledger resolutionDate is consistent with the official calendar."},{"kind":"tool","tool":"official.lookup","call":"BLS data page for JTS000000000000000JOL, total nonfarm job openings, seasonally adjusted, level in thousands","result":"Fetched recent JOLTS levels: Jan 2026 7240 thousand, Feb 2026 6922 thousand, Mar 2026 6887 thousand, Apr 2026 7585 thousand, May 2026 7594(P) thousand; also 2025 Dec 6550 thousand and 2025 Nov 6846 thousand."},{"kind":"tool","tool":"official.lookup","call":"BLS CES data page for CES0000000001, total nonfarm payroll employment, seasonally adjusted, thousands","result":"Fetched payroll employment levels: Apr 2026 158798 thousand, May 2026 158927(P) thousand, Jun 2026 158984(P) thousand, implying May-to-Jun payroll growth of 57 thousand."},{"kind":"tool","tool":"official.lookup","call":"BLS CPS data page for LNS14000000, unemployment rate, seasonally adjusted","result":"Fetched unemployment rates: Apr 2026 4.3 percent, May 2026 4.3 percent, Jun 2026 4.2 percent; 2025 Dec was 4.4 percent and 2026 Jan was 4.3 percent."},{"kind":"text","text":"Reference class and base rate: for the same SA total nonfarm JOLTS level series, the 2024-01 through 2026-05 monthly path moved from 8.378 million to 7.594 million, with large month-to-month noise and no stable acceleration. A persistence/random-walk base rate from the latest official JOLTS print starts at 7.594 million."},{"kind":"text","text":"Variant control: all anchors above use seasonally adjusted total nonfarm job openings, level, not rates, not not-seasonally-adjusted values, and not revised FRED mirrors. The resolution will use the first BLS JOLTS print for that same variant."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest JTS000000000000000JOL May 2026 preliminary level 7.594 million; historical sample = fetched monthly JOLTS values from Jan 2024 through May 2026; successive-change sigma = 0.33 million from the 28 monthly changes; adjustment components = -0.20 million for weak June payroll growth of 57 thousand, -0.08 million for mean reversion after the Apr-May jump from 6.887 million to 7.594 million, -0.02 million for still-elevated unemployment near 4.2 percent; point = 7.594 - 0.20 - 0.08 - 0.02 = 7.294, rounded to 7.29 million. One-step 80 percent half-width is roughly 1.28*sigma = 1.28*0.33 = 0.42 million; I widen to 0.55 million, about 1.67*sigma, because the forecast is two reference months beyond the latest JOLTS print and the April rebound introduced regime uncertainty. Final implied bounds: 7.29 - 0.55 = 6.74 and 7.29 + 0.55 = 7.84 million."},{"kind":"text","text":"Upside risk: if July labor demand remains close to the Apr-May rebound and employers keep vacancies open despite soft payroll growth, the first print could land above the interval, especially above 7.84 million. Downside risk: if the May level was a temporary rebound and weak payroll hiring reflects broad demand cooling, July openings could fall back toward early-2026 levels and land below the interval. Outside the interval would require either a renewed vacancy surge above roughly 7.84 million or a sharp retracement below roughly 6.74 million."},{"kind":"forecast","point":7.29,"ciLow":6.74,"ciHigh":7.84}]}

# Reviewer critique
{"summary":"Draft is publication-ready with the resolver, unit, first-print rule, prior/update structure, interval, tails, and JSON fields aligned to the ledger target.","requiredFixes":[],"optionalSuggestions":["Briefly quantify why weak June payroll growth warrants a -0.20 million openings adjustment, since that is the largest inside-view move from persistence.","Consider noting that the 0.55 million half-width is close to a two-step random-walk volatility band to make the interval calibration more transparent."]}

Emit the final JSON object only.
