# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.housing.permits_saar
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-building-permits-july-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "census.housing.permits_saar.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-18"}, "field": "PERMIT", "releasePolicy": "first_print", "sourceSeriesId": "PERMIT", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PERMIT", "table": "New Residential Construction, seasonally adjusted annual rates", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-c7a4e40bb0cd9b0e5c28fbfbb3441e05bf8245b1c02cc5b13590b8e7d0f72cd2.json"
- targetContentHash: "c7a4e40bb0cd9b0e5c28fbfbb3441e05bf8245b1c02cc5b13590b8e7d0f72cd2"
- registrationCommit: "e494ebc7a9b410a6fcffab9e5439408ff3d09413"
- registeredAtUtc: "2026-07-27T18:01:44Z"
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
b4064112da3320d7b11ffa627229471ab94f4e8be1bb5ef241c77f9ffac5e049

# Draft forecast response
{"slug":"us-building-permits-july-2026","country":"US","type":"data","title":"US Building Permits, July 2026","question":"What will the U.S. Census Bureau first report for privately owned housing units authorized by building permits in July 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":1375,"ciLow":1295,"ciHigh":1455,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"ALFRED/FRED PERMIT first vintage, mirroring the Census New Residential Construction first print","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PERMIT","resolutionRule":"Resolve to the first ALFRED vintage for FRED series PERMIT for observation month 2026-07, in thousands of privately owned housing units authorized by building permits at a seasonally adjusted annual rate. Use the first print released with the Census New Residential Construction report on 2026-08-18; ignore later revisions, benchmarks, and revised-building-permits releases.","dataPointId":"census.housing.permits_saar.2026_07.first_print","historicalContext":[{"label":"2026-06 first print","value":1367},{"label":"2026-05 first print","value":1413},{"label":"2026-04 first print","value":1442},{"label":"2026-03 first print","value":1372}],"drivers":["June total permits fell to 1367 thousand SAAR","Recent first-print permits remain near the 1370-1440 thousand range","Mortgage rates and Treasury yields were elevated in late July","June starts rebounded, limiting downside from the latest permit drop","Multifamily permits are volatile and dominate month-to-month interval width"],"sourceContext":["https://www.census.gov/construction/bps/schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html","https://www.census.gov/construction/nrc/current/index.html","https://www.census.gov/construction/nrc/current/","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PERMIT","https://myhome.freddiemac.com/buying/mortgage-rates","https://www.federalreserve.gov/releases/h15/default.htm"],"runAt":"2026-07-27T18:23:27Z","reasoning":[{"kind":"heading","text":"US July 2026 Building Permits First Print"},{"kind":"text","text":"Framing and exact resolver: the target is total privately owned housing units authorized by building permits, seasonally adjusted annual rate, measured in thousands, for July 2026. The ledger binds resolution to PERMIT first print via ALFRED; the agency source behind the print is Census/HUD New Residential Construction, and I am using the total SAAR variant throughout rather than single-family, multifamily-only, revised permits, or not-seasonally-adjusted permits."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Building Permits Survey and Economic Indicators release calendars for New Residential Construction July 2026.","result":"Fetched release schedule: July 2026 New Residential Construction is scheduled for August 18, 2026 at 8:30 AM, with revised building permits scheduled for August 25, 2026; the Economic Indicators list view also shows New Residential Construction on August 18, 2026 at 8:30 AM for July 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked Census New Residential Construction current June 2026 release for latest total permits and related components.","result":"Fetched June 2026 first-print permits of 1,367,000 SAAR, 3.0 percent below revised May 2026 at 1,410,000 and 2.3 percent below June 2025 at 1,399,000; single-family authorizations were 871,000 and buildings with 5 units or more were 445,000; June starts were 1,427,000, up 19.0 percent from revised May."},{"kind":"tool","tool":"official.lookup","call":"Checked prior Census New Residential Construction releases and archived/search-indexed release text for the recent first-print reference class.","result":"Fetched May 2026 first-print permits of 1,413,000 SAAR, April 2026 first-print permits of 1,442,000 SAAR, and March 2026 first-print permits of 1,372,000 SAAR; April's release also cited March revised at 1,363,000, while the first-print March value used here is 1,372,000."},{"kind":"tool","tool":"market.lookup","call":"Checked public rate context from Freddie Mac PMMS and Federal Reserve H.15 because permits are interest-rate sensitive.","result":"Fetched Freddie Mac average 30-year fixed mortgage rate of 6.58 percent as of July 23, 2026 and 15-year fixed rate of 5.96 percent; fetched Federal Reserve H.15 10-year Treasury constant maturity values of 4.55 on July 17, 4.60 on July 20, and 4.63 on July 21, 2026."},{"kind":"text","text":"Base rate/reference class: for this monthly level series, the starting base rate is persistence from the latest same-variant first print, 1367 thousand, cross-checked against the recent four-month first-print average of (1372 + 1442 + 1413 + 1367) / 4 = 1398.5 thousand. The recent range is narrow by housing-cycle standards but month-to-month multifamily swings make the next print noisy."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1367 from June 2026 first print; historical sample = first-print total SAAR permits for March-June 2026 of 1372, 1442, 1413, 1367; adjustment components = +8 thousand partial mean reversion toward the 1398.5 four-month average, -5 thousand for elevated mortgage/Treasury rates, +5 thousand because June starts strength and multifamily volatility argue against extrapolating the full June drop; final point = 1367 + 8 = 1375. Successive changes are +70, -29, -46; sample standard deviation of these changes gives sigma = 62.6 thousand, and 1.28*sigma = 80.2 thousand, so the rounded 80 percent interval is 1375 +/- 80 = [1295, 1455]."},{"kind":"text","text":"Upside risk: a rebound in multifamily applications similar to April's jump, easing local bottlenecks, or builders pulling permits before financing costs rise further would land above the interval. Downside risk: another leg up in mortgage rates, weak single-family demand, or a large reversal in five-plus-unit permits would land below the interval. Outside the interval would require roughly an 80 thousand move from the 1375 center, which is larger than two of the last three monthly changes but still plausible in this series."},{"kind":"forecast","point":1375,"ciLow":1295,"ciHigh":1455}]}
