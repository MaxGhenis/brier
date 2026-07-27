# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cpi.services_less_rent_shelter_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-services-less-rent-shelter-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.services_less_rent_shelter_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SASL2RS", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SASL2RS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SASL2RS", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-96ae13a7a4c7892280e19138755800c7274635b165ef4bad3336b4cccc78e6cf.json"
- targetContentHash: "96ae13a7a4c7892280e19138755800c7274635b165ef4bad3336b4cccc78e6cf"
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
ad0855d6f3d87a844b1d7c9dc6f9921c73009967d07f5fa43e3cb3fe936df22a

# Draft forecast response
{"slug":"us-cpi-services-less-rent-shelter-mom-july-2026","country":"US","type":"data","title":"US CPI services ex shelter MoM, July 2026","question":"What will the first-print month-over-month percent growth be for the BLS CPI-U Services Less Rent of Shelter, U.S. city average, seasonally adjusted series CUSR0000SASL2RS in July 2026?","unit":"percent_growth","pointEstimate":0.29,"ciLow":0.05,"ciHigh":0.53,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release and CPI series CUSR0000SASL2RS","resolutionSourceUrl":"https://data.bls.gov/timeseries/CUSR0000SASL2RS","resolutionRule":"Resolve to the first official BLS print for July 2026 CPI-U Services Less Rent of Shelter, U.S. city average, seasonally adjusted, series CUSR0000SASL2RS. Report the month-over-month percent growth from the June 2026 index to the July 2026 index as 100*(July index/June index - 1), rounded to two decimals for the forecast cell; do not use later revisions or corrected vintages unless the original BLS first-print release itself is withdrawn before publication.","dataPointId":"bls.cpi.services_less_rent_shelter_mom.2026_07.first_print","historicalContext":[{"label":"Jun 2026 MoM from CUSR0000SASL2RS","value":-0.175},{"label":"May 2026 MoM from CUSR0000SASL2RS","value":0.548},{"label":"Apr 2026 MoM from CUSR0000SASL2RS","value":0.385},{"label":"Mar 2026 MoM from CUSR0000SASL2RS","value":0.334},{"label":"Feb 2026 MoM from CUSR0000SASL2RS","value":0.282}],"drivers":["recent services-ex-shelter trend near 0.27 percent per month before June weakness","June one-off drags from motor vehicle insurance and communication likely partially mean-revert","core services and shelter cooled in June, limiting upside","volatile transportation services and energy services keep the interval wide"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm","https://fred.stlouisfed.org/series/CUSR0000SASL2RS"],"runAt":"2026-07-27T18:16:30Z","reasoning":[{"kind":"heading","text":"US CPI-U Services Less Rent of Shelter MoM, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: the target is the July 2026 first-print month-over-month percent growth for BLS CPI-U Services Less Rent of Shelter, U.S. city average, seasonally adjusted, series CUSR0000SASL2RS. The ledger sourceBinding points to the level index with a multiply transform, while the targetUnit and series slug specify percent_growth; I keep the ledger target and forecast the MoM percent growth computed from the exact CUSR0000SASL2RS seasonally adjusted index."},{"kind":"tool","tool":"official.lookup","call":"BLS CPI release schedule for 2026, Consumer Price Index release dates","result":"The official BLS CPI schedule lists July 2026 CPI for release on Aug. 12, 2026 at 08:30 AM; it also lists June 2026 on Jul. 14, 2026 at 08:30 AM and August 2026 on Sep. 11, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS June 2026 CPI news release context","result":"The June 2026 BLS CPI release reported all items -0.4 percent MoM, all items less food and energy 0.0 percent MoM, services less energy services 0.0 percent MoM, shelter 0.1 percent MoM, transportation services -0.3 percent MoM, medical care services -0.1 percent MoM, motor vehicle insurance -2.0 percent MoM, and communication -1.5 percent MoM."},{"kind":"tool","tool":"fred.lookup","call":"FRED mirror for BLS series CUSR0000SASL2RS latest observations","result":"FRED, sourced to BLS, shows CUSR0000SASL2RS index values of Feb. 2026 440.321, Mar. 2026 441.793, Apr. 2026 443.493, May 2026 445.925, and Jun. 2026 445.144, updated Jul. 14, 2026 8:10 AM CDT, with next release date Aug. 12, 2026."},{"kind":"tool","tool":"history.calc","call":"Compute recent adjacent MoM percent changes from fetched CUSR0000SASL2RS index values","result":"Computed adjacent MoM changes include Jul. 2025 0.347 percent, Aug. 2025 0.190 percent, Sep. 2025 0.191 percent, Dec. 2025 0.231 percent, Jan. 2026 0.348 percent, Feb. 2026 0.282 percent, Mar. 2026 0.334 percent, Apr. 2026 0.385 percent, May 2026 0.548 percent, and Jun. 2026 -0.175 percent; the gap around Oct. 2025 was excluded because the fetched FRED table showed a missing Oct. 2025 value."},{"kind":"text","text":"Base rate/reference class: the recent adjacent-change reference class centers near 0.27 percent per month for services less rent of shelter. I use that as the persistence prior, then adjust slightly upward from June's -0.175 percent because the June release identified unusually weak categories such as motor vehicle insurance and communication, while keeping the adjustment small because broad core services momentum also cooled."},{"kind":"math","text":"Prior/update/interval: persistence prior is the mean of the 10 fetched adjacent MoM changes from Jul. 2025-Sep. 2025 and Dec. 2025-Jun. 2026, about 0.268 percent; adjustment components are +0.07 for partial rebound from June one-off drags and -0.05 for soft June core-services breadth, giving 0.268 + 0.07 - 0.05 = 0.288, rounded to a 0.29 point forecast. Interval method uses realized dispersion of those MoM percent changes: sigma = 0.188 percentage points, so the 80 percent half-width is about 1.28*sigma = 1.28*0.188 = 0.241 percentage points; 0.29 +/- 0.24 gives 0.05 to 0.53."},{"kind":"text","text":"Counter-considerations: upside risk is a sharp rebound in motor vehicle insurance, airline fares, or energy services that would land above the interval; downside risk is continued declines in communication, insurance, medical care services, or transportation services that would keep July near zero or outside the interval below 0.05 percent."},{"kind":"forecast","point":0.29,"ciLow":0.05,"ciHigh":0.53}]}
