# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.cpi.all_groups.yoy
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-july-2026"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1.0, "operation": "multiply"}}
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
87860f9b0954f5faf02e633c45add50b52fcbda4f2a0dec85306b173e6d27b93

# Draft forecast response
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI Annual Rate, July 2026","question":"Australian Bureau of Statistics Consumer Price Index, Australia: All groups CPI, weighted average of eight capital cities, original annual change for July 2026, first print","unit":"percent","pointEstimate":3.8,"ciLow":3.1,"ciHigh":4.5,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Consumer Price Index, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/july-2026","resolutionRule":"Resolve to the first ABS-published All groups CPI, weighted average of eight capital cities, original annual change for July 2026, printed to one decimal in Consumer Price Index, Australia. Use the first print only and do not revise for later ABS updates. The ledger sourceUrl names the June 2026 release, but the official ABS future-release list identifies the July 2026 CPI release on 26/08/2026, so this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 All groups CPI annual change","value":4.0},{"label":"April 2026 All groups CPI annual change","value":4.2},{"label":"March 2026 All groups CPI annual change","value":4.6},{"label":"February 2026 All groups CPI annual change","value":3.7},{"label":"July 2025 All groups CPI annual change","value":3.0}],"drivers":["May 2026 headline CPI annual rate was 4.0 percent","Trimmed mean rose to 3.6 percent in May 2026","Housing annual inflation was 6.5 percent in May 2026","July 2025 monthly base was high at 1.3 percent","May 2026 monthly CPI fell 0.7 percent in original terms"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release","https://www.abs.gov.au/about/key-priorities/big-data-timely-insights-phase-2/complete-monthly-measure-cpi/release-schedule","https://www.abs.gov.au/about/key-priorities/big-data-timely-insights-phase-2/complete-monthly-measure-cpi"],"runAt":"2026-07-10T04:40:23Z","reasoning":[{"kind":"heading","text":"Australia July 2026 CPI annual inflation forecast"},{"kind":"text","text":"Framing and exact resolver: target is the ABS Consumer Price Index, Australia complete monthly CPI, All groups CPI, weighted average of eight capital cities, original annual change for July 2026, first print to one decimal. This is the complete Monthly CPI series that replaced the old Monthly CPI Indicator; anchors below use that same complete CPI variant."},{"kind":"tool","tool":"official.lookup","call":"Opened ABS Consumer Price Index, Australia latest release for May 2026.","result":"Fetched May 2026 release date 24/06/2026; All groups CPI annual change was 4.0 percent in May 2026, down from 4.2 percent in April 2026; monthly original CPI fell 0.7 percent in May and seasonally adjusted fell 0.1 percent."},{"kind":"tool","tool":"official.lookup","call":"Read ABS future-release list on the Consumer Price Index, Australia May 2026 page.","result":"Fetched future releases: June 2026 CPI release 29/07/2026, July 2026 CPI release 26/08/2026, and August 2026 CPI release 30/09/2026."},{"kind":"tool","tool":"official.lookup","call":"Read ABS All groups CPI monthly and annual movement table in the May 2026 release.","result":"Fetched complete CPI annual changes: Apr-25 2.4, May-25 2.1, Jun-25 1.9, Jul-25 3.0, Aug-25 3.2, Sep-25 3.6, Oct-25 3.8, Nov-25 3.4, Dec-25 3.8, Jan-26 3.8, Feb-26 3.7, Mar-26 4.6, Apr-26 4.2, May-26 4.0; fetched monthly original changes include Jun-25 0.1, Jul-25 1.3, Mar-26 1.1, Apr-26 0.4, May-26 -0.7."},{"kind":"tool","tool":"official.lookup","call":"Read ABS group and analytical-series table in the May 2026 CPI release.","result":"Fetched May 2026 annual components: Housing 6.5 percent, Food and non-alcoholic beverages 3.3 percent, Transport 3.3 percent, Trimmed mean 3.6 percent, Weighted median 3.6 percent, Electricity 21.1 percent, Automotive fuel 7.7 percent."},{"kind":"text","text":"Base rate/reference class: the reference class is post-transition complete monthly CPI annual prints from April 2025 through May 2026. The recent base rate is around 3.8 to 4.0 percent, with the last six annual prints at 3.8, 3.7, 4.6, 4.2, and 4.0 after December 2025 at 3.8."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: headline level is still near 4 percent; trimmed mean at 3.6 percent argues underlying inflation is sticky; May's -0.7 percent original monthly fall was a downside one-off mostly through volatile categories; July faces administered price and electricity-review seasonality, but July 2025 already had a large 1.3 percent monthly base that should restrain the year-over-year rate."},{"kind":"math","text":"Prior/update/interval: persistence prior is May 2026 All groups CPI annual inflation at 4.0 percent, using the Apr-25 to May-26 official complete monthly CPI annual-rate sample. Successive annual-rate changes are -0.3, -0.2, 1.1, 0.2, 0.4, 0.2, -0.4, 0.4, 0.0, -0.1, 0.9, -0.4, -0.2, so sigma = 0.48 percentage points. The unadjusted 80 percent half-width is about 1.28*sigma = 0.61 percentage points; I use a 0.7 point half-width because the target is two prints ahead and July energy-policy/base effects are unusually important. Point update is 4.0 minus 0.2 for the high Jul-25 base partly offset by sticky trimmed mean and housing pressure, giving 3.8 with 80 percent interval 3.1 to 4.5."},{"kind":"text","text":"Counter-considerations: upside risk is a large July electricity-price reset or fuel rebound that keeps the annual rate above 4.5 percent; downside risk is a soft June CPI plus another fuel or recreation decline that would land below the interval; outside the interval would likely require either a new administered-price shock above the interval or broad monthly deflation below the interval."},{"kind":"forecast","point":3.8,"ciLow":3.1,"ciHigh":4.5}]}
