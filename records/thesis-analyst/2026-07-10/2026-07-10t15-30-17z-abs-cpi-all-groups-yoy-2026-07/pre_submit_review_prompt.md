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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July CPI annual rate","question":"Australian Bureau of Statistics All groups CPI annual movement, Australia, July 2026, original (not seasonally adjusted), first print","unit":"percent","pointEstimate":3.2,"ciLow":2.6,"ciHigh":3.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 annual CPI","value":4},{"label":"April 2026 annual CPI","value":4.2},{"label":"March 2026 annual CPI","value":4.6},{"label":"February 2026 annual CPI","value":3.7},{"label":"January 2026 annual CPI","value":3.8},{"label":"July 2025 annual CPI","value":3}],"drivers":["July 2025's 1.3% monthly rise creates a favourable annual base effect","The expiry of electricity-rebate effects should reduce the annual rate as comparisons roll forward","Housing, food, and services inflation remain persistent offsets"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/release-calendar/future-releases-calendar/202608"],"runAt":"2026-07-10T15:30:28Z","reasoning":[{"kind":"heading","text":"Australia July 2026 all-groups CPI annual movement"},{"kind":"text","text":"The resolver is the original ABS first print of All groups CPI annual movement in percent, original rather than seasonally adjusted, rounded to one decimal. ABS now labels the release Consumer Price Index, Australia; the registered sourceBinding points to the June 2026 Consumer Price Index page rather than the specified July Monthly CPI Indicator page, so I retain the ledger dataPointId and rule rather than changing target identity."},{"kind":"tool","tool":"official.lookup","call":"ABS future-release listing and August 2026 official release calendar lookup for the July 2026 CPI publication date.","result":"ABS lists Consumer Price Index, Australia, July 2026 for 26/08/2026 at 11:30am AEST; its latest May release reports all-groups annual CPI at 4.0%."},{"kind":"tool","tool":"official.lookup","call":"ABS May 2026 Consumer Price Index, Australia release, table 'All groups CPI, Australia, monthly and annual movement (%)'.","result":"Fetched matched-variant annual all-groups CPI rates: Apr-25 2.4%, May-25 2.1%, Jun-25 1.9%, Jul-25 3.0%, Aug-25 3.2%, Sep-25 3.6%, Oct-25 3.8%, Nov-25 3.4%, Dec-25 3.8%, Jan-26 3.8%, Feb-26 3.7%, Mar-26 4.6%, Apr-26 4.2%, May-26 4.0%."},{"kind":"tool","tool":"official.lookup","call":"ABS May 2026 release component and analytical-series lookup.","result":"Fetched May component evidence: electricity annual inflation was 21.1%, housing 6.5%, food and non-alcoholic beverages 3.3%, transport 3.3%, services 3.7%, and trimmed mean 3.6%; May all-groups CPI fell 0.7% in original monthly terms."},{"kind":"text","text":"The reference class/base rate is the 14 monthly all-groups annual prints from Apr-2025 to May-2026, centred near the recent 4.0% level. The same original all-groups annual-movement variant is used for every anchor and historical value; no seasonally adjusted or quarterly value is mixed in."},{"kind":"math","text":"Prior/update/interval: A persistence prior starts from May's 4.0%; the Apr-2025--May-2026 historical sample has successive annual-rate changes with sample standard deviation sigma = 0.48 percentage points. July 2025's 1.3% monthly increase and the roll-forward of electricity-rebate comparisons imply a -0.6 point base-effect adjustment, while persistent housing, food, and services leave a further -0.2 point net adjustment, giving 4.0 - 0.6 - 0.2 = 3.2%. The realized-dispersion interval method gives 1.28*sigma = 0.61 points, rounded to an implied 80% range of 2.6% to 3.8%."},{"kind":"text","text":"Upside risk is a larger July annual electricity-price reset or renewed food and fuel pressure, which would land above the interval if it pushed the annual rate above 3.8%. Downside risk is a sharper reversal of the earlier rebate-related price level plus broad discretionary-price falls; a sufficiently large fall would land below the interval at under 2.6%."},{"kind":"forecast","point":3.2,"ciLow":2.6,"ciHigh":3.8}]}
