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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI Annual Rate, July 2026","question":"What will the Australian Bureau of Statistics first print for All groups CPI, Australia, original annual change for July 2026?","unit":"percent","pointEstimate":3.8,"ciLow":3.0,"ciHigh":4.6,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jul-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Consumer Price Index, Australia All groups CPI original annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger resolver names the ceased Monthly CPI Indicator and its sourceBinding points to a June 2026 CPI page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print while documenting that the official scheduled July 2026 ABS publication is Consumer Price Index, Australia.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 annual CPI","value":4.0},{"label":"April 2026 annual CPI","value":4.2},{"label":"March 2026 annual CPI","value":4.6},{"label":"February 2026 annual CPI","value":3.7},{"label":"July 2025 annual CPI","value":3.0},{"label":"July 2025 monthly CPI","value":1.3}],"drivers":["May 2026 headline CPI was 4.0%, below April's 4.2% but still elevated","Trimmed mean inflation rose to 3.6% in May 2026","July 2025 base month had a high 1.3% monthly rise","Housing remained a large contributor at 6.5% annual inflation in May","Transport inflation cooled from March spike but remained volatile"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/sep-2025","https://www.abs.gov.au/about/key-priorities/big-data-timely-insights-phase-2/complete-monthly-measure-cpi","https://www.abs.gov.au/media-centre/media-statements/abs-announces-monthly-cpi-start-november-2025"],"runAt":"2026-07-10T16:00:29Z","thresholdLadder":{"thresholds":[2.6,2.9,3.1,3.3,3.5,3.7,3.8,3.9,4.1,4.3,4.5,4.6,4.9],"cumulativeProbabilities":[0.04,0.08,0.13,0.20,0.30,0.43,0.50,0.58,0.70,0.80,0.88,0.92,0.97]},"reasoning":[{"kind":"heading","text":"Australia July 2026 All Groups CPI Annual Inflation"},{"kind":"text","text":"Framing and exact resolver: the target is the ABS first print for All groups CPI, Australia, original annual change for July 2026, rounded to one decimal. The ledger calls this the Monthly CPI Indicator, but ABS official pages say the Monthly CPI Indicator ceased after September 2025 and the complete Monthly CPI is now published under Consumer Price Index, Australia; I keep the ledger dataPointId and document the discrepancy."},{"kind":"tool","tool":"official.lookup","call":"ABS Consumer Price Index, Australia latest release page and future-release schedule lookup","result":"Fetched May 2026 CPI release: annual CPI 4.0%, April 2026 annual CPI 4.2%, May original monthly CPI -0.7%, May seasonally adjusted monthly CPI -0.1%, trimmed mean annual inflation 3.6%, and official future release date for Consumer Price Index, Australia, July 2026 of 26/08/2026 11:30am AEST."},{"kind":"tool","tool":"official.lookup","call":"ABS All groups CPI monthly and annual movement table","result":"Fetched annual All groups CPI history: Apr-25 2.4%, May-25 2.1%, Jun-25 1.9%, Jul-25 3.0%, Aug-25 3.2%, Sep-25 3.6%, Oct-25 3.8%, Nov-25 3.4%, Dec-25 3.8%, Jan-26 3.8%, Feb-26 3.7%, Mar-26 4.6%, Apr-26 4.2%, May-26 4.0%; monthly changes included Jun-25 0.1%, Jul-25 1.3%, Mar-26 1.1%, Apr-26 0.4%, May-26 -0.7%."},{"kind":"tool","tool":"official.lookup","call":"ABS CPI groups and contributions tables for current-release drivers","result":"Fetched May 2026 group annual rates: Housing 6.5%, Food and non-alcoholic beverages 3.3%, Transport 3.3%, Clothing and footwear 5.0%, Education 4.8%; contribution table showed May 2026 Housing contribution 1.4071 percentage points and Transport contribution 0.3722 percentage points."},{"kind":"tool","tool":"official.lookup","call":"ABS transition and final Monthly CPI Indicator pages","result":"Fetched ABS transition evidence: September 2025 was the final Monthly CPI Indicator release with annual indicator 3.5%, July 2025 indicator 2.8%, August 2025 indicator 3.0%, and the first complete Monthly CPI publication began with October 2025 on 26/11/2025."},{"kind":"text","text":"Variant consistency: all anchors and calculations use the ABS complete Monthly CPI, All groups CPI, Australia, original annual movement from the page table 'All groups CPI, Australia, monthly and annual movement (%)'; I do not mix in seasonally adjusted, trimmed mean, or the old Monthly CPI Indicator as the target series."},{"kind":"math","text":"Prior/update/interval: base rate/reference class prior is persistence in the complete Monthly CPI annual rate from Apr-25 to May-26. The latest annual rate is 4.0%; the high Jul-25 base month (+1.3% m/m after Jun-25 +0.1%) mechanically pulls July 2026 annual inflation down unless Jun-Jul 2026 monthly gains repeat the rebate/fuel spike, while sticky trimmed mean at 3.6%, housing at 6.5%, and broad services pressure offset some downside. Successive annual-rate changes from Apr-25..May-26 were -0.3, -0.2, +1.1, +0.2, +0.4, +0.2, -0.4, +0.4, 0.0, -0.1, +0.9, -0.4, -0.2 percentage points; sample sigma = 0.48, so 1.28*sigma = 0.62 percentage points. I widen to a ladder-implied 80% half-width of 0.8 points, about 1.29x the sigma half-width, because June and July are both still unknown and July base/rebate effects are unusually lumpy."},{"kind":"math","text":"Ladder: P(X <= 2.6) = 0.04; P(X <= 2.9) = 0.08; P(X <= 3.1) = 0.13; P(X <= 3.3) = 0.20; P(X <= 3.5) = 0.30; P(X <= 3.7) = 0.43; P(X <= 3.8) = 0.50; P(X <= 3.9) = 0.58; P(X <= 4.1) = 0.70; P(X <= 4.3) = 0.80; P(X <= 4.5) = 0.88; P(X <= 4.6) = 0.92; P(X <= 4.9) = 0.97. Linear interpolation gives p10 between 2.9 and 3.1 at 2.98, rounded to 3.0; p50 at 3.8; p90 between 4.5 and 4.6 at 4.55, rounded to 4.6."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed fuel or electricity/rebate shock plus sticky housing that would land above the interval. Downside risk is further fuel reversal and weak discretionary prices pushing the July print toward the low 3s. Outside the interval below 3.0 would likely require very soft June-July monthly CPI despite the known sticky components; outside the interval above 4.6 would likely require another March-like energy or administered-price jump."},{"kind":"forecast","point":3.8,"ciLow":3.0,"ciHigh":4.6}]}
