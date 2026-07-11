# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.cpi.all_groups_annual_rate.australia
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "abs-cpi-all-groups-annual-rate-australia-june-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups_annual_rate.australia.june_2026.first_print"
- resolutionSourceUrl: "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["data.api.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-07-28", "start": "2026-07-20"}, "field": "CPI/3.10001.10.50.M", "releasePolicy": "first_print", "sourceSeriesId": "CPI/3.10001.10.50.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata", "table": "Monthly Consumer Price Index (complete monthly CPI, dataflow CPI: annual change, all groups, original, weighted average of eight capital cities)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-27a452d7e21646679c3fb7aaa3ae1761853c56d8fd4f34d9fcdd30adf7c9ab13.json"
- targetContentHash: "27a452d7e21646679c3fb7aaa3ae1761853c56d8fd4f34d9fcdd30adf7c9ab13"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"
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
71be504b6d5050091d8827659ed1094c9c538d7d9a2dabd2c87366b1fda89a9f

# Draft forecast response
{"slug":"abs-cpi-all-groups-annual-rate-australia-june-2026","country":"AU","type":"data","title":"Australia CPI annual rate, June 2026","question":"What will the ABS first print for the annual percentage change in the original All groups CPI, weighted average of eight capital cities, for June 2026?","unit":"percent","pointEstimate":4.2,"ciLow":3.6,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"Australian Bureau of Statistics Consumer Price Index, Australia release and Data API","resolutionSourceUrl":"https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata","resolutionRule":"Resolve to the first value published by the Australian Bureau of Statistics for June 2026 annual change in the original All groups CPI, weighted average of eight capital cities, series CPI/3.10001.10.50.M. Use the first print as displayed to one decimal percentage point; later revisions do not change resolution.","dataPointId":"abs.cpi.all_groups_annual_rate.australia.june_2026.first_print","historicalContext":[{"label":"December 2025 annual CPI","value":3.8},{"label":"January 2026 annual CPI","value":3.8},{"label":"February 2026 annual CPI","value":3.7},{"label":"March 2026 annual CPI","value":4.6},{"label":"April 2026 annual CPI","value":4.2},{"label":"May 2026 annual CPI","value":4.0}],"drivers":["Persistence near May's 4.0% annual rate","Sticky housing inflation","Reversal of May transport and travel price falls","Food and tobacco inflation remain firm","Favorable but diminishing transport base effects"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/release-calendar/future-releases-calendar/202607","https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata"],"runAt":"2026-07-11T18:12:53Z","reasoning":[{"kind":"heading","text":"Australia June 2026 annual CPI forecast"},{"kind":"text","text":"The target is the first-print June 2026 annual change in the original, not seasonally adjusted, All groups CPI for the weighted average of eight capital cities. Resolution uses ABS series CPI/3.10001.10.50.M and retains the first published one-decimal value without revision grace."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS May 2026 Consumer Price Index release and its All groups annual history.","result":"ABS reported annual All groups CPI of 3.8% in December 2025, 3.8% in January 2026, 3.7% in February, 4.6% in March, 4.2% in April, and 4.0% in May."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS May 2026 release's monthly and component movements for the exact original CPI variant.","result":"The original All groups CPI fell 0.7% in May 2026; annual Housing inflation was 6.5%, Food 3.3%, Transport 3.3%, and Alcohol and tobacco 4.7%."},{"kind":"tool","tool":"official.lookup","call":"Check the ABS July 2026 release calendar and May publication's future-release schedule.","result":"The official ABS schedule lists Consumer Price Index, Australia, June 2026 for 29 July 2026 at 11:30am Canberra time; the May release also states next release 29/07/2026."},{"kind":"text","text":"The official 29 July date conflicts with the registered sourceBinding expectedReleaseWindow ending 28 July. I retain the same target but use 29 July 2026 because it is the concrete date verified from the official calendar this run."},{"kind":"text","text":"The reference class/base rate is persistence in the same original annual series. The 14 observations from April 2025 through May 2026 were 2.4%, 2.1%, 1.9%, 3.0%, 3.2%, 3.6%, 3.8%, 3.4%, 3.8%, 3.8%, 3.7%, 4.6%, 4.2%, and 4.0%; their mean successive change was +0.12 percentage point."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms point to a modest rebound: the level remains elevated at 4.0%; recent momentum eased from March's 4.6%; May's original 0.7% monthly fall included sharp Transport and Recreation declines that may partly reverse; Housing at 6.5% and administered or indexed prices keep underlying pressure firm. No mid-2026 CPI weight update is scheduled."},{"kind":"math","text":"Prior/update/interval: persistence prior = May's 4.0%; historical sample = the 14 same-variant annual rates from April 2025 to May 2026. Add +0.12 percentage point from the historical mean successive change, about +0.10 for partial reversal of May's transport/travel weakness and sticky housing, and about -0.02 for recent disinflation, giving 4.20%, rounded to 4.2%. Across the 13 successive annual-rate changes, sigma = 0.476 percentage point. The normal 80% half-width is 1.28*sigma = 1.28*0.476 = 0.610, so 4.2% ± 0.61 rounds to implied bounds of 3.6% and 4.8%."},{"kind":"text","text":"Upside risk comes from a larger fuel, travel, or housing rebound and would land above the interval if annual CPI exceeds 4.8%. Downside risk comes from renewed fuel declines, discounting, or faster goods disinflation and would land below the interval if CPI is under 3.6%. These are the concrete outside-the-interval scenarios."},{"kind":"forecast","point":4.2,"ciLow":3.6,"ciHigh":4.8}]}
