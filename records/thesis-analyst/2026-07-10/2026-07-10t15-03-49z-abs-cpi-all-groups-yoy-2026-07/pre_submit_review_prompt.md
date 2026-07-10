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
52244327c0f35585cac3f6546b984a8e2a706986e74d25a96d057ba28857eee3

# Draft forecast response
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"ABS All groups CPI annual movement for July 2026, original weighted-average-of-eight-capital-cities series, first print","unit":"percent","pointEstimate":4.1,"ciLow":3.6,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"Mar-26","value":4.6},{"label":"Apr-26","value":4.2},{"label":"May-26","value":4.0},{"label":"Feb-26","value":3.7}],"drivers":["recent annual-rate easing from 4.6% to 4.0%","volatile monthly movements","persistent housing and services inflation","one-decimal first-print rounding"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/release-calendar/future-releases/202608"],"runAt":"2026-07-10T15:04:02Z","thresholdLadder":{"thresholds":[3,3.2,3.4,3.6,3.8,4,4.2,4.4,4.6,4.8,5,5.2,5.4],"cumulativeProbabilities":[0.03,0.06,0.1,0.18,0.3,0.42,0.58,0.72,0.84,0.91,0.95,0.97,0.98]},"reasoning":[{"kind":"heading","text":"Australia July 2026 CPI annual movement first-print forecast"},{"kind":"text","text":"The target is the ABS All groups CPI annual movement for July 2026 in the original weighted-average-of-eight-capital-cities variant, rounded to one decimal on the first official print. The ledger sourceBinding discrepancy is retained: its URL names the June 2026 CPI page, while the registered target identity and resolver specify the July 2026 release."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent ABS All groups CPI annual movements from the May 2026 release","result":"ABS reported annual movements of 3.7% in Feb-26, 4.6% in Mar-26, 4.2% in Apr-26, and 4.0% in May-26; the same release reported May monthly movement of -0.7%."},{"kind":"tool","tool":"official.lookup","call":"Verify the official ABS release schedule for the target period","result":"ABS Release Calendar lists Consumer Price Index, Australia, reference period July 2026 for Wednesday 26 August 2026 at 11:30am AEST; the CPI publication page likewise lists July 2026 release date 26/08/2026."},{"kind":"tool","tool":"official.lookup","call":"Check the latest ABS component and analytical context","result":"ABS May 2026 release reported headline annual CPI at 4.0%, trimmed mean at 3.6%, housing annual inflation at 6.5%, food at 3.3%, and transport at 3.3%."},{"kind":"text","text":"The base rate/reference class is the recent monthly annual-rate path: 3.8%, 3.7%, 4.6%, 4.2%, and 4.0% from Jan through May 2026. The central tendency is near 4.0%-4.2%, with persistence from housing and services offset by volatile fuel and travel components."},{"kind":"text","text":"Level and momentum favor a modest rebound or stabilization rather than a large reacceleration: the latest annual rate fell 0.2 percentage points from April, while the March spike shows that monthly volatility can move the annual print materially. The forecast uses the original, non-seasonally-adjusted all-groups series consistently for anchors and history."},{"kind":"text","text":"Prior/update/interval: A persistence prior centered near the latest 4.0% rate is updated upward for persistent housing/services inflation and recent momentum volatility, while allowing reversal of the March-April spike. Using Feb-May annual rates, successive changes are -0.1, +0.9, -0.4, and -0.2 percentage points; sample dispersion gives sigma = 0.58, so the nominal 80% half-width is roughly 1.28*sigma = 0.74. The ladder-implied half-width is 0.60 percentage points, about 0.81 times that benchmark, reflecting one-decimal publication rounding and the recent mean-reverting pattern."},{"kind":"math","text":"Ladder: P(X <= 3.0) = 0.03; P(X <= 3.2) = 0.06; P(X <= 3.4) = 0.10; P(X <= 3.6) = 0.18; P(X <= 3.8) = 0.30; P(X <= 4.0) = 0.42; P(X <= 4.2) = 0.58; P(X <= 4.4) = 0.72; P(X <= 4.6) = 0.84; P(X <= 4.8) = 0.91; P(X <= 5.0) = 0.95; P(X <= 5.2) = 0.97; P(X <= 5.4) = 0.98. Linear interpolation gives the 10th percentile at 3.6, median at 4.1, and 90th percentile at 4.8, all rounded to the one-decimal print precision."},{"kind":"text","text":"Upside risk is a renewed fuel, housing, or services impulse that would land above the interval, especially above 4.8%. Downside risk is continuation of the May monthly decline or reversal of housing and transport pressure, which could produce 3.5% or lower; a print below 3.6% would be outside the interval."},{"kind":"forecast","point":4.1,"ciLow":3.6,"ciHigh":4.8}]}
