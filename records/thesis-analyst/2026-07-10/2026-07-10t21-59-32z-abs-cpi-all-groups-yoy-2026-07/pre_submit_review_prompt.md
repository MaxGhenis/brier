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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July 2026 all-groups CPI annual inflation","question":"Australian Bureau of Statistics complete monthly Consumer Price Index, Australia: All groups CPI annual movement for July 2026, original first print, percent.","unit":"percent","pointEstimate":3.8,"ciLow":3.5,"ciHigh":4.3,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"December 2025 All groups CPI annual movement","value":3.8},{"label":"January 2026 All groups CPI annual movement","value":3.8},{"label":"February 2026 All groups CPI annual movement","value":3.7},{"label":"March 2026 All groups CPI annual movement","value":4.6},{"label":"April 2026 All groups CPI annual movement","value":4.2},{"label":"May 2026 All groups CPI annual movement","value":4.0}],"drivers":["May headline disinflation from 4.2% to 4.0%","Housing annual inflation remained elevated at 6.5% in May","Volatile transport and clothing monthly movements can move the annual print","Underlying trimmed-mean inflation was 3.6% in May"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/release-calendar/future-releases/202607/rcc_economy"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[3.2,3.3,3.4,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4,4.6],"cumulativeProbabilities":[0.01,0.03,0.08,0.16,0.29,0.46,0.59,0.7,0.79,0.86,0.93,0.97,0.99]},"reasoning":[{"kind":"heading","text":"Australia July 2026 all-groups CPI annual inflation"},{"kind":"text","text":"Target framing: forecast the ABS All groups CPI annual movement for July 2026 in original terms, rounded to one decimal and resolved on the first print. The registered resolver names the ceased Monthly Consumer Price Index Indicator and its sourceBinding points to the June 2026 CPI page; the active ABS production is Consumer Price Index, Australia. I retain the supplied dataPointId, date, and first-print policy rather than changing target identity."},{"kind":"tool","tool":"official.lookup","call":"Fetched the ABS Consumer Price Index, Australia May 2026 release table for the same All groups CPI annual-movement variant.","result":"ABS reported All groups CPI annual movement of 3.8% in Dec-25, 3.8% in Jan-26, 3.7% in Feb-26, 4.6% in Mar-26, 4.2% in Apr-26, and 4.0% in May-26."},{"kind":"tool","tool":"official.lookup","call":"Fetched the May 2026 ABS CPI release overview and analytical-series table.","result":"ABS reported May All groups CPI annual movement at 4.0%, down from 4.2% in April; May trimmed mean was 3.6% after 3.4% in April, while Housing annual movement was 6.5%."},{"kind":"tool","tool":"official.lookup","call":"Fetched the ABS CPI publication future-release schedule to verify the target release date.","result":"ABS lists Consumer Price Index, Australia, July 2026 for 26/08/2026 at 11:30am AEST; adjacent listed dates are 29/07/2026 for June and 30/09/2026 for August."},{"kind":"text","text":"Reference class/base rate: the six fetched monthly annual prints span 3.7% to 4.6%, with a 4.0% latest print and a 3.9% simple average. All anchors are the same national All groups CPI annual-movement variant, not quarterly CPI or a smoothed series."},{"kind":"text","text":"Level and momentum point mildly lower after the 4.6% March spike eased to 4.2% and then 4.0%; persistent housing inflation and a 3.6% trimmed mean limit the expected decline. I therefore center July somewhat below May rather than extrapolating the March shock."},{"kind":"math","text":"Ladder: P(X <= 3.2) = 0.01; P(X <= 3.3) = 0.03; P(X <= 3.4) = 0.08; P(X <= 3.6) = 0.16; P(X <= 3.7) = 0.29; P(X <= 3.8) = 0.46; P(X <= 3.9) = 0.59; P(X <= 4.0) = 0.70; P(X <= 4.1) = 0.79; P(X <= 4.2) = 0.86; P(X <= 4.3) = 0.93; P(X <= 4.4) = 0.97; P(X <= 4.6) = 0.99. Linear interpolation gives 10th percentile at 3.45, median at 3.83, and 90th percentile at 4.26; rounded to the ABS one-decimal print precision these are 3.5%, 3.8%, and 4.3%."},{"kind":"text","text":"Prior/update/interval: persistence/reference-class prior is the fetched Dec-May All groups sequence (3.8, 3.8, 3.7, 4.6, 4.2, 4.0), centered near its 3.9% mean; adjustments are easing headline momentum, persistent 6.5% housing inflation, and uncertainty from volatile monthly components. The interval is read directly from the elicited threshold ladder, whose rung span is anchored by the fetched 3.7% trough and 4.6% March high, yielding 3.5% to 4.3% after one-decimal rounding."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed housing, fuel, or food acceleration that would land above the interval; downside risk is a broad decline in goods and services prices that would land below the interval. A July print above 4.3% or below 3.5% is outside the interval."},{"kind":"forecast","point":3.8,"ciLow":3.5,"ciHigh":4.3}]}
