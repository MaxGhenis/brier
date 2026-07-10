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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July 2026 annual CPI","question":"What will the first ABS print of the national All groups Consumer Price Index annual movement for July 2026, in percent and rounded to one decimal, be?","unit":"percent","pointEstimate":4.0,"ciLow":3.3,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Consumer Price Index, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 national All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered sourceBinding points to the June 2026 page and retains the former Monthly CPI Indicator naming, while the ABS calendar identifies the applicable release as Consumer Price Index, Australia, July 2026; the target remains dataPointId abs.cpi.all_groups.yoy.2026-07.first_print.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"December 2025 annual CPI","value":3.8},{"label":"January 2026 annual CPI","value":3.8},{"label":"February 2026 annual CPI","value":3.7},{"label":"March 2026 annual CPI","value":4.6},{"label":"April 2026 annual CPI","value":4.2},{"label":"May 2026 annual CPI","value":4.0}],"drivers":["Recent annual CPI momentum eased from 4.6% in March to 4.0% in May","Housing inflation remained elevated at 6.5% in May","Food and transport each rose 3.3% annually in May","Electricity-rebate unwinding can keep headline inflation volatile","July base effects create two-sided risk"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/feb-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jan-2026","https://www.abs.gov.au/media-centre/media-releases/cpi-rose-42-year-april-2026","https://www.abs.gov.au/release-calendar/future-releases/202608"],"runAt":"2026-07-10T17:05:29Z","reasoning":[{"kind":"heading","text":"Australia July 2026 annual CPI forecast"},{"kind":"text","text":"The target is the first national All groups CPI annual movement for July 2026, printed to one decimal. It is the weighted-average-of-eight-capital-cities headline series, not trimmed mean, a seasonally adjusted monthly change, or a later quarterly replacement. The ledger's Monthly CPI Indicator label and June-page sourceBinding are stale after the complete monthly CPI transition, but the target identity is unchanged."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS January and February 2026 Consumer Price Index releases for the headline All groups annual series.","result":"ABS reported annual CPI of 3.8% in January 2026 and 3.7% in February 2026; December 2025 was 3.8%."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS March, April, and May 2026 headline annual CPI observations.","result":"ABS reported annual CPI of 4.6% in March 2026, 4.2% in April 2026, and 4.0% in May 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch May 2026 ABS component details for current-release mechanisms.","result":"In May 2026 headline CPI was 4.0%; Housing rose 6.5%, Food and non-alcoholic beverages 3.3%, Transport 3.3%, and trimmed mean CPI 3.6% annually."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 CPI publication date in the ABS future-release calendar.","result":"The ABS calendar schedules Consumer Price Index, Australia, reference period July 2026, for 26 August 2026 at 11:30am AEST."},{"kind":"text","text":"The reference class/base rate is the six first-published annual observations from December 2025 through May 2026: 3.8%, 3.8%, 3.7%, 4.6%, 4.2%, and 4.0%. Persistence around the latest 4.0% is the outside-view anchor; the 4.0% six-observation median reinforces it."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms are separated as follows: the level remains near 4%; momentum eased by 0.6 percentage point from March to May; volatile fuel, travel, and food can move individual months; and electricity-rebate exhaustion keeps Housing inflation elevated. These effects support a central value near 4.0% without extrapolating March's spike."},{"kind":"math","text":"Prior/update/interval: persistence prior = May annual CPI of 4.0%, using the December-May historical sample 3.8, 3.8, 3.7, 4.6, 4.2, 4.0. Successive changes are 0.0, -0.1, +0.9, -0.4, and -0.2 percentage point; their sample sigma = 0.50. The empirical 80% half-width is roughly 1.28*sigma = 1.28*0.50 = 0.64 point. Adjustments are -0.1 for recent easing, +0.1 for persistent Housing/electricity pressure, and 0.0 net for other one-offs, leaving 4.0%. The ladder implies 10th/90th bounds of 3.3% and 4.8%, total width 1.5 points versus the sigma-based total width of about 1.28 points, a modest 1.17x widening for rebate and base-effect volatility."},{"kind":"math","text":"Ladder: P(X <= 3.0) = 0.04; P(X <= 3.2) = 0.08; P(X <= 3.4) = 0.12; P(X <= 3.6) = 0.20; P(X <= 3.8) = 0.30; P(X <= 3.9) = 0.40; P(X <= 4.0) = 0.50; P(X <= 4.2) = 0.62; P(X <= 4.4) = 0.73; P(X <= 4.6) = 0.82; P(X <= 4.8) = 0.90; P(X <= 5.2) = 0.95. Linear interpolation gives the median at 4.0, the 10th percentile at 3.3, and the 90th percentile at 4.8, each rounded to one decimal."},{"kind":"text","text":"Upside risk comes from further electricity-rebate unwinding, fuel disruption, or unusually strong rents and services; a combined shock would land above the interval. Downside risk comes from fuel reversal, discounting, or favorable July base effects; synchronized declines across volatile and core components would land below the interval. Outside the interval therefore requires a broader or larger shock than ordinary month-to-month variation."},{"kind":"forecast","point":4.0,"ciLow":3.3,"ciHigh":4.8}],"thresholdLadder":{"thresholds":[3.0,3.2,3.4,3.6,3.8,3.9,4.0,4.2,4.4,4.6,4.8,5.2],"cumulativeProbabilities":[0.04,0.08,0.12,0.2,0.3,0.4,0.5,0.62,0.73,0.82,0.9,0.95]}}
