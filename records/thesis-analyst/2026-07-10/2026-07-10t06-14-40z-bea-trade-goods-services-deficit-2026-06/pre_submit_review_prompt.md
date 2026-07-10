# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.trade.goods_services_deficit
- period: 2026-06
- conditional: null


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
# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. A compact Prior/update/interval step names the prior, historical sample, adjustment components, interval method, and implied bounds.
7. Tail scenarios are concrete and tied to the target.
8. Point, interval, final forecast step, and JSON fields are coherent.
9. No leakage, catalog point/interval circularity, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|prior_update_interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
e81bab0cdc913348ba7996c7172c5a7644579a3fc749722eced51918503ed48c

# Draft forecast response
{"slug":"us-goods-services-trade-deficit-june-2026","country":"US","type":"data","title":"US goods and services trade deficit, June 2026","question":"What will the first-print U.S. goods and services trade deficit be for June 2026, seasonally adjusted and not price adjusted, in billions of dollars?","unit":"usd_billions","pointEstimate":67.0,"ciLow":39.7,"ciHigh":94.3,"confidence":0.8,"resolutionDate":"2026-08-04","resolutionSource":"U.S. Bureau of Economic Analysis and U.S. Census Bureau, U.S. International Trade in Goods and Services, Exhibit 1","resolutionSourceUrl":"https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services","resolutionRule":"Resolve on the first official August 4, 2026 print for June 2026 from U.S. International Trade in Goods and Services, Exhibit 1. Use the seasonally adjusted, not price adjusted total goods and services balance; convert the balance to a positive deficit in USD billions, rounded to one decimal from the first release. Ignore later revisions.","dataPointId":"bea.trade.goods_services_deficit.2026_06.first_print","historicalContext":[{"label":"May 2026 first print deficit","value":77.6},{"label":"April 2026 revised deficit","value":54.6},{"label":"March 2026 deficit","value":56.6},{"label":"2026 Jan-May average deficit","value":59.6},{"label":"May 2026 three-month average deficit","value":62.9}],"drivers":["May deficit jumped to 77.6 billion on lower exports and higher imports","2026 Jan-May deficit average remains much lower at 59.6 billion","three-month average deficit is 62.9 billion, below the May level","services surplus is stable near 28.9 billion, so goods swings dominate","partial reversal of May gold and goods-import volatility is likely but not certain"],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services","https://www.bea.gov/sites/default/files/2026-07/trad0526.pdf"],"runAt":"2026-07-10T06:16:00Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 U.S. goods and services trade deficit"},{"kind":"text","text":"Framing and exact resolver: the target is the first-print June 2026 U.S. goods and services deficit, seasonally adjusted and not price adjusted, from BEA/Census U.S. International Trade in Goods and Services, Exhibit 1. I use the same variant for every anchor: total goods and services balance on a BOP basis, expressed as a positive deficit in USD billions."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule for U.S. International Trade in Goods and Services, June 2026.","result":"BEA schedule lists U.S. International Trade in Goods and Services, June 2026 for August 4, 2026 at 8:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA International Trade in Goods and Services current page for latest headline values and next release.","result":"BEA current page reports May 2026 deficit -$77.6 billion, April 2026 deficit -$54.6 billion, current release July 7, 2026, next release August 4, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read July 7, 2026 BEA/Census PDF full release, Exhibit 1 and text.","result":"The release states May exports $317.7 billion, May imports $395.3 billion, May deficit $77.6 billion, April revised deficit $54.6 billion, goods deficit $106.5 billion, services surplus $28.9 billion."},{"kind":"tool","tool":"official.lookup","call":"Extracted same-variant Exhibit 1 monthly balance history for the recent reference class.","result":"Exhibit 1 total balances in millions imply positive deficits of 2026 January 54.185, February 54.980, March 56.585, April 54.570, May 77.585; 2025 June was 58.697; May 2026 three-month average deficit was 62.913."},{"kind":"text","text":"Base rate / reference class: over Jan 2024-May 2026 same-variant monthly deficit values, the mean is 72.9 billion, but that sample includes the early-2025 tariff/gold surge. The cleaner near-term base rate is the 2026 Jan-May average of 59.6 billion and the latest three-month average of 62.9 billion."},{"kind":"text","text":"Current-release update: May's 77.6 billion deficit is a high starting point, but the release attributes the jump to a goods deficit increase, lower goods exports including nonmonetary gold, and higher goods imports including pharmaceuticals, autos, computer accessories, and semiconductors. Those categories argue for some persistence from strong import demand but also partial one-month reversal risk."},{"kind":"math","text":"Prior/update/interval: persistence prior = May deficit 77.6; reference class = Jan 2024-May 2026 same-variant Exhibit 1 monthly deficit values (n=29, mean 72.9, 2026 Jan-May mean 59.6). Adjustment components: -8.0 for partial reversal of May gold/export/import spike and -2.6 toward the 2026 YTD base rate, giving point = 77.6 - 8.0 - 2.6 = 67.0. For this change/flow target I used the values themselves: sigma = 21.3; 80% half-width = 1.28*sigma = 1.28*21.3 = 27.3; final implied bounds = 67.0 +/- 27.3 = 39.7 to 94.3."},{"kind":"text","text":"Counter-consideration: upside risk is a June import surge in semiconductors, pharmaceuticals, autos, or crude oil while exports stay depressed, which would land above the interval if the deficit exceeds 94.3 billion. Downside risk is a reversal in nonmonetary gold and goods imports plus steady services surplus, which would land below the interval if the deficit falls under 39.7 billion."},{"kind":"forecast","point":67.0,"ciLow":39.7,"ciHigh":94.3}]}
