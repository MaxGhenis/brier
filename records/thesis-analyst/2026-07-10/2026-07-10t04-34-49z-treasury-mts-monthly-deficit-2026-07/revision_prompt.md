# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: treasury.mts.monthly_deficit
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-mts-deficit-july-2026"
- targetUnit: "usd_billions"
- dataPointId: "treasury.mts.monthly_deficit.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["fiscaldata.treasury.gov"], "expectedReleaseWindow": {"end": "2026-08-17", "start": "2026-08-09"}, "field": "treasury.mts.monthly_deficit", "releasePolicy": "first_print", "sourceSeriesId": "treasury.mts.monthly_deficit", "sourceUrl": "https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/", "table": "U.S. Department of the Treasury, Monthly Treasury Statement (Table 1)", "transform": {"factor": 1.0, "operation": "multiply"}}

# Source hints
- Use U.S. Treasury Monthly Treasury Statement pages, fiscal-year tables, and official release schedules.
- For MTS targets, distinguish monthly amounts, fiscal-year-to-date amounts, receipts, outlays, refunds, and deficit concepts.
- Match the catalog unit, usually billions of nominal dollars.

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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. July 2026 MTS Deficit","question":"U.S. Department of the Treasury Monthly Treasury Statement Table 1 current-month deficit for July 2026, first print, not seasonally adjusted, in billions of nominal dollars.","unit":"usd_billions","pointEstimate":320,"ciLow":267,"ciHigh":373,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","resolutionRule":"Resolve to the first-print July 2026 current-month Surplus or Deficit (-) entry in U.S. Treasury Monthly Treasury Statement Table 1. Report deficits as positive usd_billions, rounded to the nearest 1 billion. Do not use later revisions or fiscal-year-to-date amounts.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"2025-07 first print deficit","value":291},{"label":"2024-07 first print deficit","value":244},{"label":"2023-07 first print deficit","value":221},{"label":"2022-07 first print deficit","value":211},{"label":"2021-07 first print deficit","value":302}],"drivers":["July deficits have recently clustered in the low-to-high $200 billions","Rising net interest and benefit outlays lift the 2026 level","Tariff/customs revenue offsets part of the widening","First-print Table 1 current-month balance can move sharply with calendar timing"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://apnews.com/article/us-budget-deficit-trump-tariffs-treasury-992949ccc115fddbf3838a6213cf2c94"],"runAt":"2026-07-10T04:34:56Z","reasoning":[{"kind":"heading","text":"Forecast July 2026 U.S. Monthly Treasury Statement Deficit"},{"kind":"text","text":"Framing and exact resolver: this targets the U.S. Treasury Monthly Treasury Statement Table 1 current-month Surplus or Deficit (-) for July 2026, first print only, not the fiscal-year-to-date deficit. I treat the Table 1 deficit sign convention as a reporting convention and express the forecast as a positive deficit in usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Checked the Fiscal Data Monthly Treasury Statement Table 1 target page and release-calendar context for the July 2026 statement.","result":"The ledger expected release window is 2026-08-09 to 2026-08-17, and the scheduled first-print date used here is 2026-08-12; the prior July 2025 statement was released on 2025-08-12."},{"kind":"text","text":"Variant control: every historical anchor below is the same non-seasonally-adjusted MTS Table 1 current-month deficit concept, not receipts, outlays, refunds, or fiscal-year-to-date balance."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent July current-month deficit reference class from Treasury MTS Table 1 history.","result":"July deficits used: 2021 = 302, 2022 = 211, 2023 = 221, 2024 = 244, 2025 = 291, all in usd_billions as positive deficit amounts."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest available July 2025 release report and public Treasury-linked coverage for current-policy mechanisms.","result":"July 2025 deficit was about 291 versus 244 in July 2024, a 20% year-over-year increase; customs revenue in July 2025 rose 273%, or 21 billion, from a year earlier."},{"kind":"text","text":"Base rate/reference class: the outside-view base rate is the recent July MTS distribution, with 2021-2025 values of 302, 211, 221, 244, and 291; the five-year mean is 253.8 and the median is 244, but the latest two years point to a higher post-2024 level."},{"kind":"math","text":"Prior/update/interval: persistence prior is July 2025 = 291 from the same first-print Table 1 monthly-deficit variant; adjustment components are +24 for rising benefit, interest, and appropriated outlays, +11 for policy-driven deficit pressure, and -6 for tariff/customs revenue offset, giving 291 + 24 + 11 - 6 = 320. For the 80% interval, use the realized dispersion of July flow values themselves: sample values 302, 211, 221, 244, 291 have sigma = 41.0, so half-width is roughly 1.28*sigma = 52.5; rounding to whole billions gives 320 - 53 = 267 and 320 + 53 = 373."},{"kind":"text","text":"Counter-considerations: upside risk is a larger deficit if July benefit payments, defense/homeland spending, or net interest run hotter than expected; downside risk is stronger-than-expected tariff and income-tax collections or calendar timing that shifts payments out of July; a deficit below 267 or above 373 would land outside the interval."},{"kind":"forecast","point":320,"ciLow":267,"ciHigh":373}]}

# Reviewer critique
{
  "summary": "The draft is publishable with no blocking issues; it cleanly identifies the first-print MTS Table 1 resolver, states a persistence/base-rate prior, and keeps point, interval, unit, and JSON fields coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Add a specific official release-calendar citation or source-context entry for the 2026-08-12 first-print date, since the reasoning currently states it but the sourceContext URLs are mostly dataset pages.",
    "Briefly justify the +24 and +11 adjustment components with current FY2026 MTS/Fiscal Service evidence if available, rather than leaving them as mostly judgmental drivers.",
    "Note that the 80% interval uses dispersion of July levels rather than historical forecast errors, which is acceptable but slightly less direct."
  ]
}

Emit the final JSON object only.
