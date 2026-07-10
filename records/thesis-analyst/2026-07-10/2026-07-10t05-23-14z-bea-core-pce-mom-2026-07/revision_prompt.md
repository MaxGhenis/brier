# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.core_pce.mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-pce-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "us.bea.core_pce.mom_sa.2026-07"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bea.gov"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "bea.core_pce.mom", "releasePolicy": "first_print", "sourceSeriesId": "bea.core_pce.mom", "sourceUrl": "https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy", "table": "U.S. Bureau of Economic Analysis, Personal Income and Outlays", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-32674225cad71e81ea6b8ff485cc40f0187cf9a4186ed313499c427655355a93.json"
- targetContentHash: "32674225cad71e81ea6b8ff485cc40f0187cf9a4186ed313499c427655355a93"
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
{"slug":"us-core-pce-mom-july-2026","country":"US","type":"data","title":"US Core PCE MoM, July 2026","question":"U.S. Bureau of Economic Analysis core personal consumption expenditures price index excluding food and energy, seasonally adjusted percent change from the preceding month, July 2026 first print.","unit":"percent_growth","pointEstimate":0.28,"ciLow":0.2,"ciHigh":0.36,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays","resolutionSourceUrl":"https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy","resolutionRule":"Resolve to the first BEA publication of the seasonally adjusted monthly percent change from the preceding month for the PCE price index excluding food and energy for July 2026, as published in Personal Income and Outlays / NIPA Table 2.8.7 or its linked official BEA release table. Use the first print only; do not revise for later annual, benchmark, or routine revisions. Record in percent growth, matching BEA rounding where the first print is displayed.","dataPointId":"us.bea.core_pce.mom_sa.2026-07","historicalContext":[{"label":"2026-05 implied MoM from PCEPILFE index","value":0.3200505911295837},{"label":"2026-04 implied MoM from PCEPILFE index","value":0.25049674122294974},{"label":"2026-03 implied MoM from PCEPILFE index","value":0.29621358395170994},{"label":"2026-02 implied MoM from PCEPILFE index","value":0.3939122649955218}],"drivers":["Recent core PCE monthly index changes imply a roughly 0.32 percent four-month base rate but with May elevated versus April.","The BEA exact series page shows year-over-year core PCE inflation at 3.4 percent in May 2026, up from 3.3 percent in April and March.","Core CPI-type signals and oil-driven headline pressure argue against using headline energy strength directly because this target excludes food and energy.","Two-month-ahead uncertainty remains dominated by service-price and financial-services components rather than the release calendar."],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy","https://fred.stlouisfed.org/series/PCEPILFE"],"runAt":"2026-07-10T05:23:39Z","reasoning":[{"kind":"heading","text":"US core PCE month-over-month forecast for July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the BEA seasonally adjusted PCE price index excluding food and energy, July 2026, monthly percent change from the preceding month, first print. The relevant BEA account code visible through the FRED mirror is DPCCRG, and the BEA linked monthly table is Table 2.8.7, Percent Change From Preceding Period in Prices for Personal Consumption Expenditures by Major Type of Product."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule for the July 2026 Personal Income and Outlays release date.","result":"BEA schedule lists Personal Income and Outlays, July 2026 on August 26, 2026 at 8:30 AM; the same schedule page was last modified on 7/10/26."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA core PCE exact series page for recent published year-over-year values and release metadata.","result":"BEA exact series page reports core PCE price index excluding food and energy year-over-year values: May 2026 +3.4%, April 2026 +3.3%, March 2026 +3.3%, February 2026 +3.0%; current release June 25, 2026 and next release July 30, 2026."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED PCEPILFE, a public mirror whose source is the U.S. Bureau of Economic Analysis, for recent seasonally adjusted index values used to calculate same-variant monthly changes.","result":"PCEPILFE index values, seasonally adjusted, 2017=100: May 2026 130.082, Apr 2026 129.667, Mar 2026 129.343, Feb 2026 128.961, Jan 2026 128.455; updated Jun 25, 2026 7:43 AM CDT."},{"kind":"tool","tool":"calculator","call":"Converted recent BEA/FRED core PCE index values into monthly percent changes.","result":"Computed monthly percent changes: Feb 2026 0.3939122649955218, Mar 2026 0.29621358395170994, Apr 2026 0.25049674122294974, May 2026 0.3200505911295837; four-month mean 0.3151682953249413."},{"kind":"text","text":"Reference class/base rate: because this is a change-rate target, I use recent same-variant seasonally adjusted core PCE monthly percent changes as the base rate rather than year-over-year values or headline PCE. The four observed monthly changes average about 0.315 percent, while the latest BEA page shows the year-over-year rate rising to 3.4 percent, so the outside view is elevated but not accelerating every month."},{"kind":"math","text":"Prior/update/interval: persistence prior from recent same-variant BEA/FRED PCEPILFE monthly changes is 0.315 percent using Feb-May 2026. Adjustment components: -0.04 for mean reversion from May's elevated 0.320 percent and April's softer 0.250 percent, +0.01 for still-high 3.4 percent year-over-year core PCE and service-price stickiness, -0.005 for excluding direct food and energy pass-through, giving a rounded point of 0.28. Interval method uses the values themselves for this change-rate series: sigma = 0.060 from the four computed monthly changes; 1.28*sigma = 0.077, so 0.28 +/- 0.077 implies about [0.20, 0.36] after practical BEA-display rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a July rebound in core services, portfolio-management fees, medical services, or tariff-sensitive goods that would land above the interval near 0.37 percent or higher. Downside risk is a broad goods deflation month plus cooler rent and medical-service readings that would land below the interval near 0.19 percent or lower. A large one-month methodology or seasonal-factor surprise would be outside the interval, but I do not treat that as the central case."},{"kind":"forecast","point":0.28,"ciLow":0.2,"ciHigh":0.36}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, but the interval support is too thin and the prior/update presentation should be tightened before publication.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on the standard deviation of only four recent monthly changes, which is too small a realized-volatility sample for a two-month-ahead first-print forecast.","actionRequested":"Use a longer realized-volatility sample for core PCE MoM, or explicitly justify why the four-month sample is sufficient and add uncertainty for July being two releases ahead."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact prior/update/interval step exists, but the base-rate prior is introduced after current evidence/tool results rather than cleanly before inside-view updates.","actionRequested":"Reorder or restate the reasoning so the persistence/base-rate prior is named first, then list the evidence-based adjustments, then the interval method and implied bounds."},{"rubricItem":"update","severity":"warning","summary":"The -0.04 mean-reversion adjustment is larger than the cited evidence clearly supports, since May's 0.320 is only slightly above the 0.315 four-month average and April's softer value is already included in that average.","actionRequested":"Either reduce the mean-reversion adjustment or explain with concrete evidence why July should be materially below the recent same-series persistence prior."}],"optionalSuggestions":["State explicitly that FRED is used only as a BEA history mirror, not as the resolver.","Consider naming the longer historical sample window if used for volatility, such as pre-pandemic, post-2021, or trailing 24-60 months."]}

Emit the final JSON object only.
