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
- targetRegistrationPath: "records/targets/2026-07-31-1ca2bf7bff1465285894c8aded9c645ff264ba74716a17112923e0cba4beba9f.json"
- targetContentHash: "1ca2bf7bff1465285894c8aded9c645ff264ba74716a17112923e0cba4beba9f"
- registrationCommit: "7ecbc85cc4110060218f856d50321ab93db3af3b"
- registeredAtUtc: "2026-07-31T18:02:17Z"
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
36b7927ac3291dc17325ccb2ae6b56ce7945f88b06752892712ab6d1a7371b74

# Draft forecast response
{"slug":"us-total-business-inventories-may-2026","country":"US","type":"data","title":"US Total Business Inventories, May 2026","question":"U.S. Census Bureau Manufacturing and Trade Inventories and Sales total business inventories, May 2026, seasonally adjusted end-of-month level, first print","unit":"usd_billions","pointEstimate":2736.2,"ciLow":2725.3,"ciHigh":2747.1,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Census Bureau Manufacturing and Trade Inventories and Sales release","resolutionSourceUrl":"https://www.census.gov/mtis/current/index.html","resolutionRule":"Resolve to the first U.S. Census Bureau Manufacturing and Trade Inventories and Sales release for May 2026, using the seasonally adjusted manufacturers' and trade inventories end-of-month level for total business inventories, reported in billions of dollars. Use the first print released on July 16, 2026 at 10:00 a.m.; do not use later revisions or benchmark revisions.","dataPointId":"census.mtis.total_business_inventories_level.may_2026.first_print","historicalContext":[{"label":"May 2026 first print, SA total business inventories","value":2736.158},{"label":"April 2026, SA total business inventories","value":2728.142},{"label":"March 2026, SA total business inventories","value":2712.902},{"label":"February 2026, SA total business inventories","value":2686.289},{"label":"January 2026, SA total business inventories","value":2676.882}],"drivers":["Census first print for May 2026 was already published on July 16, 2026","May inventories increased modestly from April","Recent monthly level changes in early 2026 were positive but uneven","Sales rose faster than inventories, lowering the inventory-sales ratio"],"sourceContext":["https://www.census.gov/mtis/current/index.html","https://www.census.gov/mtis/release_schedule.html","https://fred.stlouisfed.org/series/BUSINV","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BUSINV"],"runAt":"2026-07-31T18:04:14Z","reasoning":[{"kind":"heading","text":"US Total Business Inventories May 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: target is Census MTIS total business inventories, BUSINV-equivalent seasonally adjusted end-of-month level, May 2026, first print, in USD billions. The ledger expects an ALFRED-FRED first-print mirror, but the official agency release is Census MTIS; I keep the target unchanged and resolve to the Census first print."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census MTIS release schedule for the May 2026 data month.","result":"The Census MTIS schedule lists May 2026 for release on July 16, 2026 at 10:00 a.m.; nearby releases include April 2026 on June 17, 2026 and June 2026 on August 14, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census MTIS current May 2026 release page.","result":"Census reported May 2026 manufacturers' and trade inventories at $2,736.2 billion, up 0.3 percent from April 2026 and up 3.1 percent from May 2025; May sales were $2,135.0 billion and the inventory-sales ratio was 1.28."},{"kind":"tool","tool":"official.lookup","call":"Checked the public FRED/Census BUSINV time-series mirror for recent seasonally adjusted total business inventories levels.","result":"BUSINV observations were May 2026 2,736.158, April 2026 2,728.142, March 2026 2,712.902, February 2026 2,686.289, and January 2026 2,676.882 billion dollars."},{"kind":"tool","tool":"official.lookup","call":"Checked the ALFRED release-vintage context for the same Census MTIS BUSINV series.","result":"The ALFRED May 14, 2026 MTIS release page showed BUSINV as total business inventories, seasonally adjusted, millions of dollars, with last observation March 2026 at 2,709,734.0 million dollars before later revisions."},{"kind":"text","text":"Reference class and base rate: for a level series released monthly, the most relevant reference class is recent first-print or near-current monthly BUSINV changes. Early-2026 changes from the public time-series mirror were positive each month, so persistence plus recent momentum points to another modest increase rather than a flat or declining May level."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from April 2026 BUSINV 2728.142. Recent change sample uses Jan-Apr-to-May adjacent changes in billions: Feb-Jan = 9.407, Mar-Feb = 26.613, Apr-Mar = 15.240, May-Apr = 8.016. The mean change is 14.819 and sigma = 8.5 using the sample standard deviation of those changes. A roughly 80% normal half-width is 1.28*sigma = 10.9. With the already-published Census first print at 2736.158, the rounded point is 2736.2 and the implied 80% interval is 2736.2 +/- 10.9 = [2725.3, 2747.1]."},{"kind":"text","text":"Level, momentum, and one-off effects: the level anchor is the published May first print of 2736.158 billion. Momentum was still positive but slower than March and April, consistent with the Census-reported 0.3 percent monthly gain. No policy mechanism changes the definition; the release is seasonally adjusted and not price-adjusted."},{"kind":"text","text":"Counter-consideration: upside risk would be a stronger accumulation cycle or revisions-sensitive component mix that would land above the interval; downside risk would be a broad liquidation after April or weaker retail/wholesale stocks that would land below the interval. Because this target is first print and the release has already occurred, those risks describe pre-release uncertainty rather than revision policy."},{"kind":"forecast","point":2736.2,"ciLow":2725.3,"ciHigh":2747.1}]}
