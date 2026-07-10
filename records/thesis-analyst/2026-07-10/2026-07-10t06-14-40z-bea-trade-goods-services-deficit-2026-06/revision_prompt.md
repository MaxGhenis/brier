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
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.trade.goods_services_deficit.2026_06.first_print"
- resolutionSourceUrl: "https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bea.gov"], "expectedReleaseWindow": {"end": "2026-08-04", "start": "2026-08-04"}, "field": "Goods and services deficit, seasonally adjusted, not price adjusted", "releasePolicy": "first_print", "sourceSeriesId": "U.S. International Trade in Goods and Services, Exhibit 1, goods and services balance", "sourceUrl": "https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services", "table": "U.S. International Trade in Goods and Services, Exhibit 1: Exports, Imports, and Balance", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-6471ea9c088e896db68e0a949ed2b485372cb4e7c9b99f97d8dc5f8e422d0926.json"
- targetContentHash: "6471ea9c088e896db68e0a949ed2b485372cb4e7c9b99f97d8dc5f8e422d0926"
- registeredAtUtc: "2026-07-10T05:58:27Z"

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
{"slug":"us-goods-services-trade-deficit-june-2026","country":"US","type":"data","title":"US goods and services trade deficit, June 2026","question":"What will the first-print U.S. goods and services trade deficit be for June 2026, seasonally adjusted and not price adjusted, in billions of dollars?","unit":"usd_billions","pointEstimate":67.0,"ciLow":39.7,"ciHigh":94.3,"confidence":0.8,"resolutionDate":"2026-08-04","resolutionSource":"U.S. Bureau of Economic Analysis and U.S. Census Bureau, U.S. International Trade in Goods and Services, Exhibit 1","resolutionSourceUrl":"https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services","resolutionRule":"Resolve on the first official August 4, 2026 print for June 2026 from U.S. International Trade in Goods and Services, Exhibit 1. Use the seasonally adjusted, not price adjusted total goods and services balance; convert the balance to a positive deficit in USD billions, rounded to one decimal from the first release. Ignore later revisions.","dataPointId":"bea.trade.goods_services_deficit.2026_06.first_print","historicalContext":[{"label":"May 2026 first print deficit","value":77.6},{"label":"April 2026 revised deficit","value":54.6},{"label":"March 2026 deficit","value":56.6},{"label":"2026 Jan-May average deficit","value":59.6},{"label":"May 2026 three-month average deficit","value":62.9}],"drivers":["May deficit jumped to 77.6 billion on lower exports and higher imports","2026 Jan-May deficit average remains much lower at 59.6 billion","three-month average deficit is 62.9 billion, below the May level","services surplus is stable near 28.9 billion, so goods swings dominate","partial reversal of May gold and goods-import volatility is likely but not certain"],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services","https://www.bea.gov/sites/default/files/2026-07/trad0526.pdf"],"runAt":"2026-07-10T06:16:00Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 U.S. goods and services trade deficit"},{"kind":"text","text":"Framing and exact resolver: the target is the first-print June 2026 U.S. goods and services deficit, seasonally adjusted and not price adjusted, from BEA/Census U.S. International Trade in Goods and Services, Exhibit 1. I use the same variant for every anchor: total goods and services balance on a BOP basis, expressed as a positive deficit in USD billions."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule for U.S. International Trade in Goods and Services, June 2026.","result":"BEA schedule lists U.S. International Trade in Goods and Services, June 2026 for August 4, 2026 at 8:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA International Trade in Goods and Services current page for latest headline values and next release.","result":"BEA current page reports May 2026 deficit -$77.6 billion, April 2026 deficit -$54.6 billion, current release July 7, 2026, next release August 4, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read July 7, 2026 BEA/Census PDF full release, Exhibit 1 and text.","result":"The release states May exports $317.7 billion, May imports $395.3 billion, May deficit $77.6 billion, April revised deficit $54.6 billion, goods deficit $106.5 billion, services surplus $28.9 billion."},{"kind":"tool","tool":"official.lookup","call":"Extracted same-variant Exhibit 1 monthly balance history for the recent reference class.","result":"Exhibit 1 total balances in millions imply positive deficits of 2026 January 54.185, February 54.980, March 56.585, April 54.570, May 77.585; 2025 June was 58.697; May 2026 three-month average deficit was 62.913."},{"kind":"text","text":"Base rate / reference class: over Jan 2024-May 2026 same-variant monthly deficit values, the mean is 72.9 billion, but that sample includes the early-2025 tariff/gold surge. The cleaner near-term base rate is the 2026 Jan-May average of 59.6 billion and the latest three-month average of 62.9 billion."},{"kind":"text","text":"Current-release update: May's 77.6 billion deficit is a high starting point, but the release attributes the jump to a goods deficit increase, lower goods exports including nonmonetary gold, and higher goods imports including pharmaceuticals, autos, computer accessories, and semiconductors. Those categories argue for some persistence from strong import demand but also partial one-month reversal risk."},{"kind":"math","text":"Prior/update/interval: persistence prior = May deficit 77.6; reference class = Jan 2024-May 2026 same-variant Exhibit 1 monthly deficit values (n=29, mean 72.9, 2026 Jan-May mean 59.6). Adjustment components: -8.0 for partial reversal of May gold/export/import spike and -2.6 toward the 2026 YTD base rate, giving point = 77.6 - 8.0 - 2.6 = 67.0. For this change/flow target I used the values themselves: sigma = 21.3; 80% half-width = 1.28*sigma = 1.28*21.3 = 27.3; final implied bounds = 67.0 +/- 27.3 = 39.7 to 94.3."},{"kind":"text","text":"Counter-consideration: upside risk is a June import surge in semiconductors, pharmaceuticals, autos, or crude oil while exports stay depressed, which would land above the interval if the deficit exceeds 94.3 billion. Downside risk is a reversal in nonmonetary gold and goods imports plus steady services surplus, which would land below the interval if the deficit falls under 39.7 billion."},{"kind":"forecast","point":67.0,"ciLow":39.7,"ciHigh":94.3}]}

# Reviewer critique
{"summary":"Draft is publishable with only minor clarity improvements; the resolver, first-print rule, units, interval, tails, and JSON fields are coherent with the ledger target.","requiredFixes":[],"optionalSuggestions":["Clarify that no separate formal time-series model was fit; the model prior is persistence plus same-variant reference-class levels.","In the prior/update step, reconcile the wording between the 'cleaner near-term base rate' and the named 'persistence prior' so readers know which anchor is primary.","Briefly justify why the level standard deviation, rather than month-to-month change volatility, is the chosen interval basis."]}

Emit the final JSON object only.
