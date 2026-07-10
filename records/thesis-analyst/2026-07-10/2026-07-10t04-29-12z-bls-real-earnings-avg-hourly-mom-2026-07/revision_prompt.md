# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-july-2026"
- targetUnit: "percent"
- dataPointId: "bls.real_earnings.avg_hourly_mom.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-10"}, "field": "bls.real_earnings.avg_hourly_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.real_earnings.avg_hourly_mom", "sourceUrl": "https://www.bls.gov/news.release/realer.t01.htm", "table": "U.S. Bureau of Labor Statistics Real Earnings Table A-1", "transform": {"factor": 1.0, "operation": "multiply"}}

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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real average hourly earnings MoM, July 2026","question":"What will BLS first print as the July 2026 over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, in Real Earnings Table A-1?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.7,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 print for July 2026, row 'Real average hourly earnings' under 'OVER-THE-MONTH PERCENT CHANGE' for all employees on private nonfarm payrolls, seasonally adjusted. Use the one-decimal percent value published in the initial August 12, 2026 release and ignore later revisions.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"May 2026 first/current BLS table print","value":-0.1},{"label":"April 2026 BLS table value","value":-0.5},{"label":"March 2026 BLS table value","value":-0.6},{"label":"May 2025 BLS table value","value":0.4}],"drivers":["July nominal average hourly earnings likely near recent 0.3 percent pace","July CPI-U monthly inflation likely still firm but less energy-spike-heavy than May","Real earnings MoM is approximately nominal hourly earnings growth minus CPI-U inflation","Recent real hourly earnings prints are negative because CPI inflation has outpaced wage gains"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/empsit.t19.htm","https://www.bls.gov/news.release/cpi.t01.htm","https://fred.stlouisfed.org/series/CES0500000003"],"runAt":"2026-07-10T04:30:50Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS real average hourly earnings MoM"},{"kind":"text","text":"Framing and exact resolver: this is the BLS Real Earnings Table A-1 seasonally adjusted all-employees private nonfarm payrolls real average hourly earnings over-the-month percent change, not production-worker earnings, not weekly earnings, and not a later revised database value."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Schedule of Releases for Real Earnings.","result":"Fetched official release date: reference month July 2026 is scheduled for Aug. 12, 2026 at 08:30 AM; June 2026 is scheduled for Jul. 14, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Real Earnings Table A-1 current table.","result":"Fetched target-series recent values: real average hourly earnings MoM percent changes were May 2025 0.4, March 2026 -0.6, April 2026 -0.5, and May 2026 -0.1; May 2026 real average hourly earnings level was $11.24, CPI-U was 333.979, and average hourly earnings were $37.53."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Employment Situation Table B-3 for nominal hourly earnings.","result":"Fetched nominal average hourly earnings for total private: April 2026 $37.41, May 2026 $37.51, June 2026 $37.64; June 2026 average weekly earnings were $1,291.05."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS CPI Table 1 for all-items CPI-U and components.","result":"Fetched CPI-U all-items seasonally adjusted percent changes: February to March 2026 0.9, March to April 2026 0.6, April to May 2026 0.5; May 2026 core CPI was 0.2 and energy was 3.9."},{"kind":"tool","tool":"history.lookup","call":"Opened FRED mirror page for BLS series CES0500000003 to cross-check recent nominal hourly earnings history.","result":"Fetched mirror values sourced to BLS: June 2026 37.64, May 2026 37.51, April 2026 37.41, March 2026 37.35, February 2026 37.27; page updated Jul. 2, 2026 at 8:33 AM CDT."},{"kind":"text","text":"Reference class/base rate: for this change/flow target, the latest official Real Earnings table gives a small recent reference class of MoM real hourly earnings values [0.4, -0.6, -0.5, -0.1]. Its mean is about -0.2 percent, and the newest print improved from -0.5 to -0.1 as wage growth partly offset CPI pressure."},{"kind":"text","text":"Component view: July nominal hourly earnings has a stable recent anchor around 0.3 percent because May and June nominal AHE each rose about 0.3 percent. CPI is the swing factor: May all-items CPI was 0.5 percent with energy up 3.9 percent, while core was only 0.2 percent, so a July CPI print around 0.35 to 0.40 percent would imply roughly flat to slightly negative real hourly earnings."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent official BLS Table A-1 real-AHE MoM reference class [0.4, -0.6, -0.5, -0.1], mean = -0.2. Adjustment components are +0.1 for steadier nominal AHE near 0.3, +0.0 for still-firm CPI after the May energy shock, giving point = -0.1. Interval method uses sample dispersion of the fetched change values themselves: sigma = 0.45, so 80% half-width is about 1.28*sigma = 0.58; point -0.1 plus/minus 0.58 gives -0.68 to 0.48, rounded to -0.7 to 0.5."},{"kind":"text","text":"Risks: upside risk is a soft July CPI print near 0.0 to 0.1 with wages still near 0.3, which would land above the interval if real earnings printed above 0.5. Downside risk is another gasoline or tariff-driven CPI jump near 0.9 with wages near 0.2, which would land below the interval. An outside the interval result would most likely require a large energy-price move or an unusual composition-driven wage print."},{"kind":"forecast","point":-0.1,"ciLow":-0.7,"ciHigh":0.5}]}

# Reviewer critique
{
  "summary": "The draft is publishable after tightening the model-prior explanation and strengthening the volatility basis for the interval.",
  "requiredFixes": [
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a four-observation persistence prior but does not explicitly state whether a broader time-series/model prior was used or ruled out.",
      "actionRequested": "Add one sentence saying either that no longer-history time-series model was used and why, or include a simple longer historical prior for this exact MoM series."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is based on only four observations, mixing one year-ago value with recent months, so the realized-volatility basis is thin.",
      "actionRequested": "Either compute dispersion from a longer BLS history for the same one-decimal MoM target or explicitly label the four-point sigma as a deliberately conservative/limited sample and justify why it is adequate."
    }
  ],
  "optionalSuggestions": [
    "In the resolver text, keep the exact row wording but also mention that the value is in percent, one decimal, seasonally adjusted.",
    "Clarify that the June 2026 nominal AHE evidence was already public as of runAt and is not part of the unresolved July target."
  ]
}

Emit the final JSON object only.
