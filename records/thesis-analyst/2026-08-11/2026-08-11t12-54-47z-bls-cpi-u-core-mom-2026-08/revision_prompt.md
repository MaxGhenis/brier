# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cpi.u.core_mom
- period: 2026-08
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-cpi-mom-august-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.u.core_mom.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-16", "start": "2026-09-08"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-16", "start": "2026-09-08"}, "field": "bls.cpi.u.core_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.cpi.u.core_mom", "sourceUrl": "https://www.bls.gov/news.release/cpi.nr0.htm", "table": "U.S. Bureau of Labor Statistics Consumer Price Index news release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-7f06e063b1a3cfb4fc7b99061e8dd2223e358084787c4cee16f470e22eaf5e12.json"
- targetContentHash: "7f06e063b1a3cfb4fc7b99061e8dd2223e358084787c4cee16f470e22eaf5e12"
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
{"slug":"us-core-cpi-mom-august-2026","country":"US","type":"data","title":"US Core CPI MoM, Aug. 2026","question":"What will the BLS first print report for seasonally adjusted CPI-U all items less food and energy month-over-month percent change in August 2026?","unit":"percent_growth","pointEstimate":0.24,"ciLow":0.08,"ciHigh":0.40,"confidence":0.8,"resolutionDate":"2026-09-11","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index news release","resolutionSourceUrl":"https://www.bls.gov/news.release/cpi.nr0.htm","resolutionRule":"Resolve to the first BLS Consumer Price Index news release print for August 2026, Table A, CPI-U U.S. city average, seasonally adjusted percent change from preceding month for all items less food and energy, in percent, using the initially published value and not later seasonal-factor revisions.","dataPointId":"bls.cpi.u.core_mom.august_2026.first_print","historicalContext":[{"label":"2026-06 core CPI-U SA m/m","value":0.0},{"label":"2026-05 core CPI-U SA m/m","value":0.2},{"label":"2026-04 core CPI-U SA m/m","value":0.4},{"label":"2026-03 core CPI-U SA m/m","value":0.2},{"label":"2026-06 core CPI-U 12-month NSA","value":2.6}],"drivers":["June core CPI zero looks partly one-off and likely mean-reverts","Shelter slowed to 0.1 percent in June, limiting upside","Core goods and vehicle categories were soft in June","Services ex-energy were flat in June after 0.3 percent in May","Tariff or import-cost pass-through remains an upside risk"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm"],"runAt":"2026-08-11T12:55:31Z","reasoning":[{"kind":"heading","text":"US core CPI-U month-over-month forecast for August 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is CPI-U U.S. city average, all items less food and energy, seasonally adjusted, percent change from the preceding month for August 2026. The ledger window is 2026-09-08 to 2026-09-16; the BLS CPI release calendar gives the concrete August 2026 CPI release date as September 11, 2026 at 08:30 ET, so I use 2026-09-11 as the resolution date."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule page for the August 2026 reference month.","result":"Fetched official schedule: August 2026 Consumer Price Index release date is Sep. 11, 2026 and release time is 08:30 AM; July 2026 is Aug. 12, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read the current BLS CPI news release for June 2026 and Table A.","result":"Fetched Table A core CPI-U seasonally adjusted monthly changes: Dec. 2025 0.2, Jan. 2026 0.3, Feb. 2026 0.2, Mar. 2026 0.2, Apr. 2026 0.4, May 2026 0.2, Jun. 2026 0.0; 12-month core CPI through Jun. 2026 was 2.6."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS June 2026 release narrative for component momentum.","result":"Fetched June 2026 details: all items less food and energy was 0.0; shelter rose 0.1; owners' equivalent rent rose 0.2; rent rose 0.1; lodging away from home fell 2.3; motor vehicle insurance fell 2.0; communication fell 1.5; apparel fell 0.6; used cars and trucks fell 0.2."},{"kind":"text","text":"Reference class and base rate: for this change-flow target I anchor on the recent official BLS core CPI-U SA monthly changes themselves. The seven-month reference class average from Dec. 2025 through Jun. 2026 is 1.5 / 7 = 0.214 percent, and the 12-month core rate of 2.6 percent is consistent with a monthly pace near 0.21 percent."},{"kind":"text","text":"The target is the seasonally adjusted CPI-U core variant, not NSA CPI, chained CPI, all-items CPI, or a later revised seasonal-adjustment vintage; all anchors above are from the same BLS CPI-U core seasonally adjusted Table A variant except the separately labeled 12-month core context."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent BLS Table A reference class, Dec. 2025-Jun. 2026 core monthly values [0.2, 0.3, 0.2, 0.2, 0.4, 0.2, 0.0], mean 0.214. Adjustment components: +0.04 for mean reversion after June's unusually soft 0.0 and several one-off category declines, -0.02 for shelter cooling to 0.1 and soft core goods, net point about 0.24. Interval method uses the sample dispersion of those fetched monthly change values: sigma = 0.12, so 1.28*sigma = 0.15. Applying a roughly symmetric 80% band around 0.24 gives 0.24 - 0.16 = 0.08 and 0.24 + 0.16 = 0.40."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in motor vehicle insurance, lodging, communication, or tariff-sensitive core goods that would land above the interval if August core runs over 0.40. Downside risk is another month of shelter deceleration plus falling medical care, apparel, or used vehicles that would land below the interval if August core is under 0.08. An outside the interval outcome is most likely from broad services reacceleration or a second unusually weak one-off month."},{"kind":"forecast","point":0.24,"ciLow":0.08,"ciHigh":0.40}]}

# Reviewer critique
{
  "summary": "Draft is publishable with one minor clarification recommended around the model prior; resolver, first-print rule, interval math, tails, and JSON fields are coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Add one sentence explicitly stating that no separate formal time-series model was used beyond the short BLS Table A persistence prior, or briefly describe why that prior is preferred for this cell.",
    "Consider noting that the exact 2026-09-11 release date is inside the ledger expectedReleaseWindow of 2026-09-08 to 2026-09-16."
  ]
}

Emit the final JSON object only.
