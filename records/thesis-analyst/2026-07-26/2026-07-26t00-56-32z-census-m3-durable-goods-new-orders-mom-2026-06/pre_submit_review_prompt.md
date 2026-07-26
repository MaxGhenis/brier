# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.m3.durable_goods_new_orders_mom
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-durable-goods-orders-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.m3.durable_goods_new_orders_mom.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-27", "start": "2026-07-27"}, "field": "DGORDER", "releasePolicy": "first_print", "sourceSeriesId": "DGORDER", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER", "table": "Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-270b7d2d593a239ac3373efdb5ec9fa3809df3e9eb60f5b3e1bc8120e239921b.json"
- targetContentHash: "270b7d2d593a239ac3373efdb5ec9fa3809df3e9eb60f5b3e1bc8120e239921b"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"
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
8f4bb7a3026d8243d436cb78bd1b549f2a1f86c61f6a95f5637a97f044a17f95

# Draft forecast response
{"slug":"us-durable-goods-orders-mom-june-2026","country":"US","type":"data","title":"US durable goods orders MoM, June 2026","question":"What will the U.S. Census Bureau first report for seasonally adjusted manufacturers' new orders for durable goods (DGORDER), month-over-month percent growth, for June 2026?","unit":"percent_growth","pointEstimate":1.8,"ciLow":-4.8,"ciHigh":8.4,"confidence":0.8,"resolutionDate":"2026-07-27","resolutionSource":"ALFRED/FRED vintage mirror of the U.S. Census Bureau M3 Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER","resolutionRule":"Use the first-print June 2026 seasonally adjusted DGORDER observation released with the Census M3 Advance Report on July 27, 2026. Convert the first-print level to month-over-month percent growth versus the May 2026 first-print DGORDER level as 100*(June/May - 1), reported in percentage points. Later M3 full-report values, benchmark revisions, and subsequent ALFRED vintages do not replace the first print.","dataPointId":"census.m3.durable_goods_new_orders_mom.2026_06.first_print","historicalContext":[{"label":"May 2026 first advance MoM","value":-4.5},{"label":"April 2026 MoM","value":8.5},{"label":"March 2026 MoM from DGORDER levels","value":1.3},{"label":"February 2026 MoM from DGORDER levels","value":-1.2},{"label":"January 2026 MoM from DGORDER levels","value":-0.4}],"drivers":["May transport drop leaves rebound risk","June ISM new orders still expanding","Manufacturing output flat in June","Aircraft orders make headline series volatile","Exports and prices temper the upside"],"sourceContext":["https://www.census.gov/manufacturing/m3/release_schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html?sec_ak_reference=18.52333b8.1542589455.5b7ef1e9","https://www.census.gov/manufacturing/m3/adv/current/index.html","https://fred.stlouisfed.org/series/DGORDER","https://www.ismworld.org/supply-management-news-and-reports/reports/ism-pmi-reports/pmi/june/","https://www.federalreserve.gov/Releases/g17/current/default.htm?mod=article_inline","https://boeing.mediaroom.com/2026-07-14-Boeing-Announces-Second-Quarter-Deliveries","https://flightplan.forecastinternational.com/2026/07/14/airbus-and-boeing-report-june-2026-commercial-aircraft-orders-and-deliveries/"],"runAt":"2026-07-26T00:57:04Z","reasoning":[{"kind":"heading","text":"US durable goods orders MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the Census M3 Advance Report headline series for manufacturers' new orders for durable goods, seasonally adjusted, FRED/ALFRED series code DGORDER. The ledger source binding points to ALFRED DGORDER; I am forecasting the first-print month-over-month percent growth for June 2026, not the later full M3 revision."},{"kind":"tool","tool":"official.lookup","call":"Checked Census M3 release schedule and Census economic indicators calendar for the June 2026 advance durable goods release date.","result":"Census lists Survey Month June 2026 with Advance Report on Durable Goods and Advance Total Manufacturing on 7/27/2026 at 8:30 a.m.; the full report is listed for 8/4/2026. The calendar-list view also lists Advance Report on Durable Goods--Manufacturers' Shipments, Inventories, and Orders on July 27, 2026 at 8:30 AM for period June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the current Census M3 advance durable goods release for the latest first-print reference point.","result":"The June 25, 2026 Census advance report said May 2026 new orders for manufactured durable goods decreased $15.6 billion, or 4.5 percent, to $332.1 billion; April increased 8.5 percent; excluding transportation, new orders increased 1.3 percent; transportation equipment decreased $18.5 billion, or 14.0 percent, to $113.5 billion."},{"kind":"tool","tool":"fred.lookup","call":"Checked DGORDER recent levels from the public FRED/ALFRED mirror of Census M3.","result":"FRED DGORDER showed May 2026 = 332,050 million dollars, April 2026 = 347,618, March 2026 = 320,485, February 2026 = 316,233, and January 2026 = 319,975; these imply approximate MoM changes of May -4.5 percent, April +8.5 percent, March +1.3 percent, February -1.2 percent, and January -0.4 percent."},{"kind":"tool","tool":"survey.lookup","call":"Checked June manufacturing demand indicators before the durable goods release.","result":"ISM's June 2026 Manufacturing PMI was 53.3 percent, down 0.7 point from May 54.0; the New Orders Index was 56.0, down 0.8 point from May 56.8; Production was 52.2, down 2.1 points from May 54.3; Backlog of Orders was 50.5, down 1.7 points from May 52.2."},{"kind":"tool","tool":"official.lookup","call":"Checked June industrial production and aircraft-related public data for transport and production context.","result":"The Federal Reserve G.17 release reported June 2026 industrial production +0.1 percent and manufacturing output unchanged at 0.0 percent. Boeing reported 171 commercial airplane deliveries in Q2 2026 and 314 year-to-date; public June aircraft order coverage reported Boeing booked 121 gross commercial aircraft orders and delivered 64 jets in June."},{"kind":"text","text":"Base rate / reference class: using the recent DGORDER monthly percent changes from January 2024 through May 2026 gives a volatile 29-observation reference class with mean about +0.47 percentage point and sigma about 5.15 percentage points. The series is dominated by aircraft and other transportation swings, so the May transportation drop and June aircraft order rebound matter more than a smooth manufacturing trend."},{"kind":"math","text":"Prior/update/interval: persistence prior is the 2024-01 to 2026-05 DGORDER MoM base rate mean of +0.47 pp. I add +1.3 pp for transport/aircraft rebound after May's -14.0 percent transportation drop and June Boeing order strength, +0.4 pp for ISM new orders at 56.0, subtract 0.2 pp for flat Fed manufacturing output, and subtract 0.2 pp for softer exports/prices drag, giving +1.8 percent. Interval method uses realized dispersion of DGORDER MoM values themselves: sigma = 5.15, so 80 percent half-width is roughly 1.28*sigma = 1.28*5.15 = 6.59 pp; +1.8 +/- 6.6 gives [-4.8, 8.4] after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a much larger-than-assumed aircraft booking print or defense capital-goods jump, which would land above the interval if total orders rise more than about 8.4 percent. Downside risk is that June aircraft orders do not translate into Census M3 timing, or nontransport durable categories reverse despite ISM breadth, which would land below the interval if total orders fall more than about 4.8 percent."},{"kind":"forecast","point":1.8,"ciLow":-4.8,"ciHigh":8.4}]}
