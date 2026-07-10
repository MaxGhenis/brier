# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.cpi.all_groups.yoy
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-july-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- resolutionDate: "2026-08-26"
- resolutionSource: "Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release"
- resolutionSourceUrl: "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026"
- resolutionRule: "Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530.json"
- targetContentHash: "fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"
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
7defca226e328eefaadbafcff27940e0b5a83f4fe682b90228a233dd179d1ea7

# Draft forecast response
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual inflation, July 2026","question":"What will the Australian Bureau of Statistics first-print All groups CPI annual movement be for July 2026, in percent, unadjusted and rounded to one decimal?","unit":"percent","pointEstimate":3.9,"ciLow":3.3,"ciHigh":4.5,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"Jul-25","value":3},{"label":"Aug-25","value":3.2},{"label":"Sep-25","value":3.6},{"label":"Oct-25","value":3.8},{"label":"Nov-25","value":3.4},{"label":"Dec-25","value":3.8},{"label":"Jan-26","value":3.8},{"label":"Feb-26","value":3.7},{"label":"Mar-26","value":4.6},{"label":"Apr-26","value":4.2},{"label":"May-26","value":4}],"drivers":["Recent annual inflation easing from 4.6% in March to 4.0% in May","Persistent services and housing inflation","Automotive-fuel and other volatile-item base effects","Monthly CPI first-print rounding to one decimal"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release?os=0","https://www.abs.gov.au/release-calendar/future-releases/202608","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026"],"runAt":"2026-07-10T22:18:42Z","thresholdLadder":{"thresholds":[3.1,3.3,3.5,3.7,3.8,3.9,4.1,4.3,4.5,4.7,4.9],"cumulativeProbabilities":[0.05,0.1,0.2,0.35,0.45,0.55,0.7,0.82,0.9,0.95,0.97]},"reasoning":[{"kind":"heading","text":"Australia CPI annual inflation, July 2026"},{"kind":"text","text":"This targets the ABS All groups CPI annual movement for July 2026, first print, unadjusted and rounded to one decimal. The ABS release calendar verifies publication on 2026-08-26 at 11:30am AEST. The registered sourceBinding names the June 2026 CPI page, but the target remains the July 2026 first-print dataPointId and July release page specified by the ledger."},{"kind":"tool","tool":"official.lookup","call":"ABS May 2026 CPI release, All groups annual movement table","result":"Fetched official annual movements: Jul-25 3.0%, Aug-25 3.2%, Sep-25 3.6%, Oct-25 3.8%, Nov-25 3.4%, Dec-25 3.8%, Jan-26 3.8%, Feb-26 3.7%, Mar-26 4.6%, Apr-26 4.2%, May-26 4.0%."},{"kind":"tool","tool":"official.lookup","call":"ABS April 2026 CPI release, annual inflation and component data","result":"Fetched official figures: headline annual CPI was 4.2% in April 2026, down from 4.6% in March; goods inflation was 4.7%, automotive fuel inflation was 18.6%, and services inflation was 3.5%."},{"kind":"tool","tool":"official.lookup","call":"ABS May 2026 CPI release, latest headline and analytical series","result":"Fetched official figures: headline annual CPI was 4.0% in May 2026, down from 4.2% in April; trimmed mean was 3.6%, non-tradables were 4.7%, and seasonally adjusted All groups CPI annual movement was 4.0%."},{"kind":"tool","tool":"official.lookup","call":"ABS future release calendar for July 2026 CPI","result":"Fetched official schedule: Consumer Price Index, Australia, reference period July 2026 is scheduled for Wednesday 26 August 2026 at 11:30am AEST."},{"kind":"text","text":"The base rate/reference class is the recent complete monthly ABS sequence: annual inflation was 3.0% to 3.8% across July 2025 to January 2026, then 3.7%, 4.6%, 4.2%, and 4.0% from February to May 2026. The central tendency has recently eased, but the level remains above the mid-3% range."},{"kind":"text","text":"Level and momentum point modestly lower: the March spike of 4.6% has fallen by 0.6 percentage points over two releases. Persistent housing and non-tradables inflation provide an upside offset, while fuel and other volatile components can create a sizeable month-specific base effect. The target is the same gross, unadjusted All groups CPI annual movement throughout; no trimmed-mean or seasonally adjusted variant is substituted."},{"kind":"text","text":"Prior/update/interval: Starting from a persistence prior centered near the recent May 2026 reading of 4.0%, using the ABS Jul-25-to-May-26 reference class, I apply a modest easing adjustment for the March-to-May decline, retain an upside adjustment for 4.7% non-tradables inflation and housing persistence, and allow volatile fuel/base effects. The ladder-implied interval is 3.3% to 4.5%, with the rungs anchored by the fetched 3.0%, 3.2%, 3.6%, 3.8%, 4.6%, 4.2%, and 4.0% observations."},{"kind":"math","text":"Ladder: P(X <= 3.1) = 0.05; P(X <= 3.3) = 0.10; P(X <= 3.5) = 0.20; P(X <= 3.7) = 0.35; P(X <= 3.8) = 0.45; P(X <= 3.9) = 0.55; P(X <= 4.1) = 0.70; P(X <= 4.3) = 0.82; P(X <= 4.5) = 0.90; P(X <= 4.7) = 0.95; P(X <= 4.9) = 0.97. Linear interpolation gives 10th percentile at 3.3, median at 3.85, and 90th percentile at 4.5; rounding to the ABS one-decimal print precision gives ciLow 3.3, pointEstimate 3.9, and ciHigh 4.5."},{"kind":"text","text":"The main upside risk is a renewed fuel or housing-related acceleration that would land above the interval, especially at 4.6% or higher. The main downside risk is another large favorable volatile-item or base-effect move, with a result at or below 3.2% landing outside the interval."},{"kind":"forecast","point":3.9,"ciLow":3.3,"ciHigh":4.5}]}
