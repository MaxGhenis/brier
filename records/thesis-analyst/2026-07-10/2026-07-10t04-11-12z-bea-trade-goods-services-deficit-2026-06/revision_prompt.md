# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.trade.goods_services_deficit
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-goods-services-trade-deficit-june-2026"
- targetUnit: "usd_billions"
- dataPointId: "bea.trade.goods_services_deficit.2026_06.first_print"
- resolutionSourceUrl: "https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bea.gov"], "expectedReleaseWindow": {"end": "2026-08-04", "start": "2026-08-04"}, "field": "Goods and services deficit; seasonally adjusted; not price adjusted", "releasePolicy": "first_print", "sourceSeriesId": "U.S. International Trade in Goods and Services Exhibit 1 goods and services deficit", "sourceUrl": "https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services", "table": "U.S. International Trade in Goods and Services, Exports, Imports, and Balance (exhibit 1)", "transform": {"factor": 1, "operation": "identity"}}

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
{"slug":"us-goods-services-trade-deficit-june-2026","country":"US","type":"data","title":"U.S. goods and services trade deficit, June 2026","question":"What will the first-print U.S. goods and services trade deficit be for June 2026, seasonally adjusted and not price adjusted, in Exhibit 1 of the U.S. International Trade in Goods and Services release?","unit":"usd_billions","pointEstimate":69,"ciLow":55.6,"ciHigh":82.4,"confidence":0.8,"resolutionDate":"2026-08-04","resolutionSource":"U.S. Bureau of Economic Analysis and U.S. Census Bureau, U.S. International Trade in Goods and Services release","resolutionSourceUrl":"https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services","resolutionRule":"Resolve to the first official June 2026 value for the goods and services deficit in Exhibit 1, seasonally adjusted and not price adjusted, reported in billions of dollars. Use the first print released on August 4, 2026; ignore later revisions. If the table reports balance as a negative number, convert the deficit to a positive usd_billions value using the absolute value, rounded to one decimal place.","dataPointId":"bea.trade.goods_services_deficit.2026_06.first_print","historicalContext":[{"label":"2026-05 latest first print/current release deficit","value":77.6},{"label":"2026-04 revised deficit","value":54.6},{"label":"2026-03 deficit","value":56.6},{"label":"2026-02 deficit","value":55},{"label":"2026-01 deficit","value":54.2},{"label":"2025-06 deficit","value":58.7}],"drivers":["May deficit widened sharply to $77.6 billion on lower exports and higher imports","January-April 2026 deficits clustered near $54-$57 billion before the May jump","Services surplus has been stable near $28-$29 billion, so goods volatility dominates the forecast","May import strength in consumer goods, autos, crude oil, semiconductors, and pharmaceuticals raises the June baseline","Some reversal of May's nonmonetary-gold export drag should narrow the deficit from May"],"sourceContext":["https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services","https://www.bea.gov/news/schedule","https://www.bea.gov/sites/default/files/2026-07/trad0526.pdf"],"runAt":"2026-07-10T04:11:26Z","reasoning":[{"kind":"heading","text":"U.S. goods and services trade deficit, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets the BEA/Census U.S. International Trade in Goods and Services Exhibit 1 goods and services deficit for June 2026, seasonally adjusted and not price adjusted. Exhibit 1 reports balance as negative millions of dollars; this cell resolves to the positive deficit in usd_billions on the first print."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule for the June 2026 U.S. International Trade in Goods and Services release date.","result":"BEA schedule lists U.S. International Trade in Goods and Services, June 2026 on August 4, 2026 at 8:30 AM; the schedule page was last modified 7/9/26."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA series landing page for latest release status and headline figures.","result":"The BEA page shows U.S. International Trade in Goods and Services, May 2026: May deficit -$77.6B, April deficit -$54.6B, current release July 7, 2026, next release August 4, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the July 7, 2026 full release PDF headline and components.","result":"The release states the goods and services deficit was $77.6B in May, up $23.0B from $54.6B in April; May exports were $317.7B, down $10.5B, and May imports were $395.3B, up $12.5B."},{"kind":"tool","tool":"official.lookup","call":"Read Exhibit 1 seasonally adjusted history for the same variant and table.","result":"Exhibit 1 balance totals in millions were: 2026 Jan -54,185; Feb -54,980; Mar -56,585; Apr revised -54,570; May -77,585; 2025 Jun -58,697; Jul -75,062; Aug -59,642; Sep -59,392; Oct -37,376; Nov -63,868; Dec -76,078."},{"kind":"text","text":"Base rate/reference class: using the same Exhibit 1 seasonally adjusted not price adjusted deficit variant, the last 12 available monthly deficits from June 2025 through May 2026 average about $60.7B, while the first five months of 2026 average about $59.6B and the March-May 2026 moving average is $62.9B."},{"kind":"text","text":"Level and momentum: May's $77.6B deficit is a high starting point, but January-April 2026 were tightly grouped at $54.2B, $55.0B, $56.6B, and $54.6B. I treat May as partly persistent because imports rose to $395.3B, but partly temporary because exports fell by $10.5B and nonmonetary gold alone decreased $6.2B in exports."},{"kind":"text","text":"Policy/mechanism update: tariff and sourcing uncertainty can keep goods imports lumpy, especially semiconductors, pharmaceuticals, autos, and crude oil. The services surplus is much smoother, rising only from $28.3B in April to $28.9B in May, so the June uncertainty is mostly a goods-balance question."},{"kind":"math","text":"Prior/update/interval: persistence prior is a blend of the latest deficit $77.6B, the 3-month average $62.9B, and the 12-month same-variant reference class mean $60.7B. Adjustment components: start near $67B from partial mean reversion, add about $2B for elevated imports and tariff/front-loading risk, subtract about $0B net for services stability, giving a $69.0B point. For the 80% interval, because this is a monthly flow/deficit amount, compute dispersion from the fetched 12 monthly deficit values themselves: sigma = 10.4; half-width = 1.28*sigma = 1.28*10.4 = 13.3, so $69.0B +/- $13.4B gives about $55.6B to $82.4B."},{"kind":"text","text":"Counter-considerations: upside risk is another import surge in semiconductors, pharmaceuticals, autos, or energy with weak exports, which would land above the interval. Downside risk is a reversal of May's gold/export weakness plus import payback after tariff-related front-loading, which would land below the interval. A value outside the interval would most likely require a second consecutive goods shock rather than services movement."},{"kind":"forecast","point":69,"ciLow":55.6,"ciHigh":82.4}]}

# Reviewer critique
{
  "summary": "The draft is publishable with no blocking issues; it cleanly ties the forecast to the BEA first-print Exhibit 1 target and gives a coherent prior, update, interval, and tail story.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider clarifying that the interval uses cross-sectional monthly level dispersion over June 2025-May 2026, not one-step forecast error volatility.",
    "The resolver text is slightly more explicit than the ledger by mentioning absolute value conversion; keep it because it removes sign ambiguity."
  ]
}

Emit the final JSON object only.
