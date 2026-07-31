# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.construction_spending.total_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-construction-spending-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.construction_spending.total_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-07", "start": "2026-08-30"}, "field": "TTLCONS", "releasePolicy": "first_print", "sourceSeriesId": "TTLCONS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS", "table": "Value of Construction Put in Place Survey", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-ad912c7b624a6bf7eceafefd874d2906976c63698e7d5ad68b9741aa2a778d7e.json"
- targetContentHash: "ad912c7b624a6bf7eceafefd874d2906976c63698e7d5ad68b9741aa2a778d7e"
- registrationCommit: "0249a6f266d1d202c43782056e77403612358765"
- registeredAtUtc: "2026-07-31T14:48:09Z"
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
ecba5db041f79d4b15d01be036436474dbdd7686b780a392fdc509331ec6c6cf

# Draft forecast response
{"slug":"us-construction-spending-mom-july-2026","country":"US","type":"data","title":"US construction spending MoM, July 2026","question":"What will the U.S. Census Bureau first print show for July 2026 total construction spending, month-over-month percent change, seasonally adjusted annual rate, for total construction?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.8,"ciHigh":1.0,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Census Bureau Construction Spending release, mirrored through the registered ALFRED TTLCONS first-vintage binding","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS","resolutionRule":"Resolve to the first official print for July 2026 total construction spending, seasonally adjusted annual rate, as the percent change from June 2026 to July 2026 implied by TTLCONS in the registered ALFRED first-vintage source. Use the first posted vintage only; do not incorporate later Census/FRED/ALFRED revisions or same-day corrections unless they are part of the initially posted release vintage. Round to one decimal percentage point, matching the Census/FRED percent-change display convention.","dataPointId":"census.construction_spending.total_mom.2026_07.first_print","historicalContext":[{"label":"May 2026 first/current print percent change","value":0.1},{"label":"Apr 2026 current percent change","value":0.3},{"label":"Mar 2026 current percent change","value":0.4},{"label":"Feb 2026 current percent change","value":-0.3},{"label":"Jan 2026 current percent change","value":-0.9}],"drivers":["recent total construction spending is near flat","private residential was positive in May","private nonresidential and manufacturing remain drags","public construction was positive in May","monthly construction spending changes have wide revision-prone dispersion"],"sourceContext":["https://www.census.gov/construction/c30/release.html","https://www.census.gov/construction/c30/current/index.html","https://fred.stlouisfed.org/series/MPCTXXXXS","https://fred.stlouisfed.org/data/MPCTXXXXS","https://fred.stlouisfed.org/release/tables?eid=22348&rid=229","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS"],"runAt":"2026-07-31T15:07:10Z","reasoning":[{"kind":"heading","text":"July 2026 U.S. construction spending MoM first print"},{"kind":"text","text":"Framing and exact resolver: the target is the U.S. Census Bureau Value of Construction Put in Place Survey total construction series, seasonally adjusted annual rate, for July 2026. The canonical ledger binds resolution to ALFRED TTLCONS first_print even though Census is the official agency source; I use Census pages for schedule and release context, and keep the resolver tied to the registered ALFRED TTLCONS first-vintage rule."},{"kind":"tool","tool":"official.lookup","call":"Census Construction Spending release schedule lookup for the July 2026 reporting period","result":"Fetched schedule says Monthly Value of Construction Put in Place July releases on September 1, 2026 at 10:00 a.m.; June releases on August 3, 2026 and August releases on October 1, 2026."},{"kind":"tool","tool":"official.lookup","call":"Census current Construction Spending release lookup for the latest official context","result":"Fetched May 2026 release: total construction spending was $2,210.2 billion SAAR, 0.1 percent above revised April $2,207.1 billion, and 1.5 percent below May 2025 $2,244.4 billion."},{"kind":"tool","tool":"official.lookup","call":"FRED/Census MPCTXXXXS percent-change series lookup for recent monthly values","result":"Fetched MPCTXXXXS values: May 2026 0.1, Apr 2026 0.3, Mar 2026 0.4, Feb 2026 -0.3, Jan 2026 -0.9 percent change from preceding period, seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"FRED release table lookup for total construction levels behind the percent-change target","result":"Fetched release table levels: total construction May 2026 2,210,214 million dollars, Apr 2026 2,207,051 million dollars, May 2025 2,244,426 million dollars."},{"kind":"text","text":"The release variant is total construction, seasonally adjusted annual rate, converted to month-over-month percent growth. The target is first print for July 2026, so later revisions to June or July should not be used when resolving."},{"kind":"text","text":"Reference class and base rate: recent monthly percent changes in total construction spending are centered close to zero. The 2024-08 through 2026-05 fetched/cached MPCTXXXXS sequence used for dispersion was 0.2, -0.3, 0.0, -0.2, -0.7, -0.3, -0.2, -0.7, 0.1, -0.2, 0.5, 0.4, 0.4, -0.4, -0.1, 0.6, 1.8, -1.9, -0.8, 0.2, 0.4, 0.1, giving a near-zero mean around -0.05 percentage point."},{"kind":"text","text":"Level, momentum, one-off, and policy-mechanism effects: the latest Census release shows nominal total spending barely positive, public construction positive, private residential positive, and private nonresidential soft. I do not see a clear one-off mechanism that should dominate the base rate by July; July is therefore anchored near flat rather than extrapolating the revised January drop or the December spike."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is near 0.0 from the recent MPCTXXXXS reference class, with a small positive update from May total spending at +0.1 percent, private residential +0.3 percent, and public construction +0.5 percent, offset by private nonresidential -0.3 percent. I set point = 0.1. For the 22 recent percent-change observations listed above, mean is about -0.05 and sample sigma = 0.69 percentage point; 1.28*sigma = 0.88 percentage point, so an 80% interval around 0.1 is roughly -0.8 to 1.0 after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in manufacturing, data centers, public infrastructure, or residential improvements that would land above the interval if July prints above 1.0 percent. Downside risk is a renewed private nonresidential/manufacturing pullback or sharper residential decline that would land below the interval if July prints below -0.8 percent."},{"kind":"forecast","point":0.1,"ciLow":-0.8,"ciHigh":1.0}]}
