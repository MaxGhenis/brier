# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.marts.adv44x72.monthly_change
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "census-marts-adv44x72-monthly-change-june-2026"
- targetUnit: "percent_growth"
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
c402291e68a3730fda8f18946a2a0ed8cbed042278fdbde96018f4a33c568a69

# Draft forecast response
{"slug":"census-marts-adv44x72-monthly-change-june-2026","country":"US","type":"data","title":"US advance retail sales monthly change, June 2026","question":"What will the U.S. Census Bureau first print for the seasonally adjusted advance monthly percent change in retail and food services sales, total NAICS 44X72, from May 2026 to June 2026?","unit":"percent_growth","pointEstimate":0.3,"ciLow":-1.0,"ciHigh":1.6,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Census Bureau Advance Monthly Sales for Retail and Food Services release","resolutionSourceUrl":"https://www.census.gov/retail/marts/www/marts_current.pdf","resolutionRule":"Resolve to the first Census Bureau Advance Monthly Sales for Retail and Food Services PDF released for June 2026, Table 2, Retail & food services total, percent change for June 2026 Advance from May 2026, seasonally adjusted and not price-adjusted. Use the printed value rounded to 0.1 percentage point and ignore all later revisions or benchmark updates.","dataPointId":"census.marts.adv44x72.monthly_change.2026-06.first_print","historicalContext":[{"label":"2026-05 advance from 2026-04","value":0.9},{"label":"2026-04 revised from 2026-03","value":0.4},{"label":"2025-05 adjusted from 2025-04, computed from Table 1 levels","value":-1.1}],"drivers":["May advance print was strong at +0.9% after revised April +0.4%","Total retail and food services sales level was $763.7 billion in May 2026","Recent same-series monthly changes show high noise, with a small positive central tendency","Gasoline and motor-vehicle categories boosted May and could fade in June","First-print advance estimate is based on an early subsample and is revision-prone"],"sourceContext":["https://www.census.gov/retail/release_schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html","https://www.census.gov/retail/marts/www/marts_current.pdf","https://www.census.gov/retail/index.html","https://www.census.gov/econ/currentdata/?programCode=MARTS"],"runAt":"2026-07-07T22:14:55Z","reasoning":[{"kind":"heading","text":"June 2026 advance retail sales monthly-change forecast"},{"kind":"text","text":"Framing and exact resolver: this target is Census MARTS/Advance Monthly Sales for Retail and Food Services, total retail and food services NAICS 44X72, seasonally adjusted and not adjusted for price changes. The first-print value is the Table 2 percent change for June 2026 Advance from May 2026, not the later MRTS preliminary revision."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Monthly Retail Trade release schedule and Economic Indicator calendar for June 2026 Advance Monthly Retail Trade Report.","result":"Census lists the Advance Monthly Retail Trade Report data month June 2026 for release on July 16, 2026 at 8:30 am; the calendar separately lists Advance Monthly Sales for Retail and Food Services on July 16, 2026 at 8:30 AM for period June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the May 2026 Census advance retail sales release PDF text and headline values.","result":"The May 2026 release says adjusted retail and food services sales were $763.7 billion, up 0.9 percent from April 2026 and up 6.9 percent from May 2025; March 2026 to April 2026 was revised from +0.5 percent to +0.4 percent."},{"kind":"tool","tool":"official.lookup","call":"Read Census Table 1 and Table 2 for recent same-series adjusted total retail and food services values.","result":"Table 1 adjusted total retail and food services levels were 763705 million for May 2026, 757036 million for April 2026, 754013 million for March 2026, 714568 million for May 2025, and 722442 million for April 2025; Table 2 prints May 2026 from April 2026 at +0.9 and April 2026 from March 2026 at +0.4."},{"kind":"text","text":"Base rate/reference class: using the same Census advance total retail and food services monthly-change variant, the recent fetched values are +0.9, +0.4, and the Table 1 April-to-May 2025 adjusted-level change of roughly -1.1. That small sample centers near zero but with material month-to-month volatility."},{"kind":"text","text":"Variant consistency: all anchors are Census Advance Monthly Sales for Retail and Food Services total retail and food services, seasonally adjusted, not price-adjusted, and expressed as month-over-month percent changes for the same total 44X72 concept."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior uses recent same-variant monthly changes [0.9, 0.4, -1.1], mean = (0.9 + 0.4 - 1.1)/3 = 0.07. Current-release adjustment adds +0.25 for May momentum and still-solid ex-gas/ex-auto breadth, subtracts -0.05 for possible payback from gasoline/vehicle strength, giving point about 0.27 rounded to 0.3. For the interval, sample sigma = 1.04 from [0.9, 0.4, -1.1]; 1.28*sigma = 1.33, so 0.3 +/- 1.3 gives about -1.0 to 1.6."},{"kind":"text","text":"Upside risk: a stronger June auto rebound, continued nonstore strength, or gasoline-price/category lift would land above the interval. Downside risk: a June reversal in gasoline stations plus weaker vehicle and discretionary categories would land below the interval. A broad nominal-spending shock or seasonal-adjustment surprise is the main outside the interval scenario."},{"kind":"forecast","point":0.3,"ciLow":-1.0,"ciHigh":1.6}]}
