# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.mtis.total_business_inventories_level
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-total-business-inventories-may-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "census.mtis.total_business_inventories_level.may_2026.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-21", "start": "2026-07-13"}, "field": "BUSINV", "releasePolicy": "first_print", "sourceSeriesId": "BUSINV", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BUSINV", "table": "Manufacturing and Trade Inventories and Sales", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-7983fb7b69d7ad2cf0a21a1f04c836ed2926d133d18f75ccc4435ac7e77c2fd5.json"
- targetContentHash: "7983fb7b69d7ad2cf0a21a1f04c836ed2926d133d18f75ccc4435ac7e77c2fd5"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"
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
17aa7952aad6a8ad108deff07117d0d500fc9da9596210cf9d034cc84dd6f31f

# Draft forecast response
{"slug":"us-total-business-inventories-may-2026","country":"US","type":"data","title":"US Total Business Inventories, May 2026","question":"U.S. Census Bureau Manufacturing and Trade Inventories and Sales total business inventories (BUSINV), May 2026, seasonally adjusted end-of-month level, first print, in USD billions.","unit":"usd_billions","pointEstimate":2736.158,"ciLow":2724.958,"ciHigh":2747.358,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Census Bureau Manufacturing and Trade Inventories and Sales first release, mirrored as BUSINV first vintage in ALFRED","resolutionSourceUrl":"https://www.census.gov/mtis/current/index.html","resolutionRule":"Resolve to the first official May 2026 seasonally adjusted total business inventories end-of-month level from the Census Manufacturing and Trade Inventories and Sales release. Use the first-print BUSINV value in millions of dollars converted to USD billions by multiplying by 0.001; ignore later revisions and benchmark updates.","dataPointId":"census.mtis.total_business_inventories_level.may_2026.first_print","historicalContext":[{"label":"May 2026 first print BUSINV","value":2736.158},{"label":"Apr 2026 BUSINV shown after May release","value":2728.142},{"label":"Mar 2026 BUSINV shown after May release","value":2712.902},{"label":"Feb 2026 BUSINV shown after May release","value":2686.289},{"label":"Jan 2026 BUSINV shown after May release","value":2676.882}],"drivers":["Census first print for May 2026 was already posted on July 16, 2026","Seasonally adjusted inventories rose 0.3 percent from April","Recent monthly level changes remained positive","Ledger uses ALFRED BUSINV million-dollar first-vintage transform to USD billions"],"sourceContext":["https://www.census.gov/mtis/current/index.html","https://www.census.gov/mtis/release_schedule.html","https://alfred.stlouisfed.org/series?seid=BUSINV","https://www.census.gov/economic-indicators/market-prices/"],"runAt":"2026-07-25T15:54:35Z","reasoning":[{"kind":"heading","text":"US total business inventories May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this target is Census MTIS total business inventories, seasonally adjusted, end-of-month level, May 2026, first print. The run is after the official July 16, 2026 release, so the honest forecast record notes that the first print is already observable rather than pretending it is still pre-release."},{"kind":"tool","tool":"official.lookup","call":"Checked Census MTIS release schedule for May 2026 release timing and target date.","result":"Census schedule lists May 2026 Manufacturing and Trade Inventories and Sales for release on July 16, 2026 at 10:00 a.m.; nearby rows list April 2026 on June 17, 2026 and June 2026 on August 14, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked Census May 2026 MTIS release page for headline first-print values.","result":"Census reported May 2026 manufacturers' and trade inventories at $2,736.2 billion, up 0.3 percent from April 2026 and up 3.1 percent from May 2025; sales were $2,135.0 billion and the inventory/sales ratio was 1.28."},{"kind":"tool","tool":"alfred.lookup","call":"Checked ALFRED BUSINV exact series values for the ledger's first-vintage resolving series.","result":"ALFRED BUSINV showed May 2026 = 2,736,158 million dollars, Apr 2026 = 2,728,142 million, Mar 2026 = 2,712,902 million, Feb 2026 = 2,686,289 million, and Jan 2026 = 2,676,882 million; units are millions of dollars, seasonally adjusted, monthly end of period."},{"kind":"tool","tool":"official.lookup","call":"Checked Census pre-release/current indicator context for the immediate history available around the release sequence.","result":"Census economic-indicator snapshots showed March 2026 business inventories at $2,709.7 billion, February 2026 revised at $2,686.3 billion, and April 2026 business inventories at $2,726.6 billion before the May release updated the series."},{"kind":"text","text":"Reference class and base rate: for a level series, the local reference class is month-to-month changes in the seasonally adjusted BUSINV level. The immediate 2026 history had positive changes of +9.407, +26.613, and +15.240 billion from January through April using the ALFRED values, so persistence plus a modest positive May change is the natural outside-view anchor."},{"kind":"math","text":"Prior/update/interval: persistence prior = April BUSINV plus the recent mean monthly change; historical sample = Jan-Apr 2026 ALFRED levels before the May target, with changes 9.407, 26.613, and 15.240 billion. Adjustment components = positive inventory momentum, Census reported May +0.3 percent, and post-release first-print observability. Interval method = sample standard deviation of recent level changes: mean change = 17.087, sigma = 8.75, and 80 percent half-width = 1.28*sigma = 11.20. Final point uses the ledger exact first-print BUSINV value 2,736,158 million * 0.001 = 2736.158 billion; final implied bounds are 2736.158 - 11.20 = 2724.958 and 2736.158 + 11.20 = 2747.358."},{"kind":"text","text":"Counter-considerations: upside risk would have been a larger wholesale or retail inventory accumulation pushing May above about 2747.358 billion; downside risk would have been liquidation or downward component revisions pulling the level below about 2724.958 billion. Either would land outside the interval, while the observed first print sits inside it."},{"kind":"forecast","point":2736.158,"ciLow":2724.958,"ciHigh":2747.358}]}
