# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cpi.services_less_energy_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-services-less-energy-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.services_less_energy_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SASLE", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SASLE", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SASLE", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-d4cbafc02be2045165c04afda95ee8ed75921c46bf61e22e936098333d04f69a.json"
- targetContentHash: "d4cbafc02be2045165c04afda95ee8ed75921c46bf61e22e936098333d04f69a"
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
bcbe31e9be6ae6210f3cfe18c96d082d0b513592877e7cc338266c0569ff501c

# Draft forecast response
{"slug":"us-cpi-services-less-energy-mom-july-2026","country":"US","type":"data","title":"US CPI Services Less Energy MoM, July 2026","question":"BLS Consumer Price Index for All Urban Consumers: Services Less Energy Services in U.S. City Average, seasonally adjusted, month-over-month percent change for July 2026, first print","unit":"percent_growth","pointEstimate":0.27,"ciLow":0.09,"ciHigh":0.45,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release","resolutionSourceUrl":"https://data.bls.gov/timeseries/CUSR0000SASLE","resolutionRule":"Resolve to the first official BLS July 2026 CPI release value for CUSR0000SASLE, Consumer Price Index for All Urban Consumers: Services Less Energy Services in U.S. City Average, seasonally adjusted, expressed as the month-over-month percent change from the preceding month. Use the first print published on August 12, 2026; do not use later revised seasonally adjusted indexes. BLS Table A reports changes to one decimal, while an index-derived first-print calculation may be retained at higher precision if the resolver computes from the first-published index values.","dataPointId":"bls.cpi.services_less_energy_mom.2026_07.first_print","historicalContext":[{"label":"Jun 2026 services less energy MoM, BLS Table A","value":0.0},{"label":"May 2026 services less energy MoM, BLS Table A","value":0.3},{"label":"Apr 2026 services less energy MoM, BLS Table A","value":0.5},{"label":"Mar 2026 services less energy MoM, BLS Table A","value":0.2},{"label":"Jun 2026 CUSR0000SASLE index level, FRED/ALFRED","value":444.602},{"label":"May 2026 CUSR0000SASLE index level, FRED/ALFRED","value":444.46},{"label":"Apr 2026 CUSR0000SASLE index level, FRED/ALFRED","value":443.154}],"drivers":["recent services-less-energy base rate near 0.3 percent","June weakness likely partly one-off in insurance and communication","shelter still positive but cooling","medical and recreation services keep upside risk alive","ledger sourceBinding appears to expose the index series, so MoM must be computed or read from BLS Table A"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm?trk=public_post_comment-text","https://www.bls.gov/cpi/","https://www.bls.gov/news.release/archives/cpi_07142026.htm","https://www.bls.gov/news.release/archives/cpi_06102026.htm","https://www.bls.gov/news.release/archives/cpi_05122026.htm","https://www.bls.gov/news.release/archives/cpi_04102026.htm","https://www.bls.gov/news.release/archives/cpi_03112026.htm","https://www.bls.gov/news.release/archives/cpi_02132026.htm","https://fred.stlouisfed.org/series/CUSR0000SASLE","https://alfred.stlouisfed.org/series?seid=CUSR0000SASLE"],"runAt":"2026-07-27T18:14:57Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS CPI Services Less Energy MoM"},{"kind":"text","text":"Framing and exact resolver: the target is the BLS CPI-U Services Less Energy Services series, CUSR0000SASLE, U.S. city average, seasonally adjusted, for July 2026, first print. The ledger sourceBinding points to ALFRED/FRED CUSR0000SASLE index levels with only a multiply transform, which looks inconsistent with the targetUnit percent_growth and MoM slug; I keep the ledger target and forecast the official first-print MoM percent change, using BLS Table A or first-published index levels without later revisions."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS CPI release schedule page for the July 2026 reference month.","result":"BLS schedule lists July 2026 CPI release date as Aug. 12, 2026 at 08:30 AM; it also lists June 2026 as Jul. 14, 2026 and August 2026 as Sep. 11, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS CPI home page for the next CPI release and latest aggregate CPI context.","result":"BLS CPI home says CPI for July 2026 is scheduled for August 12, 2026 at 8:30 A.M. Eastern Time; latest CPI was -0.4% in Jun 2026 and core CPI was 0.0% in Jun 2026, 2.6% over the year."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS June 2026 CPI Table A for the same seasonally adjusted variant.","result":"For Services less energy services, BLS Table A shows Dec 2025 0.3, Jan 2026 0.4, Feb 2026 0.3, Mar 2026 0.2, Apr 2026 0.5, May 2026 0.3, Jun 2026 0.0, and 12-month change 3.2."},{"kind":"tool","tool":"official.lookup","call":"Fetched earlier BLS CPI archived Table A rows for the same series to build the recent reference class.","result":"BLS archived releases show Services less energy services MoM values of Jul 2025 0.4, Aug 2025 0.3, Sep 2025 0.2, Dec 2025 0.3, Jan 2026 0.4, Feb 2026 0.3, Mar 2026 0.2, Apr 2026 0.5, May 2026 0.3, Jun 2026 0.0."},{"kind":"tool","tool":"official.lookup","call":"Checked FRED and ALFRED CUSR0000SASLE pages as public mirrors for current index levels and source identity.","result":"FRED/ALFRED show CUSR0000SASLE Jun 2026 index 444.602, May 2026 444.460, Apr 2026 443.154, Mar 2026 440.951, Feb 2026 439.959; units are Index 1982-1984=100, seasonally adjusted, monthly, source U.S. Bureau of Labor Statistics."},{"kind":"text","text":"Base rate/reference class: the recent same-series, same-seasonally-adjusted reference class clusters around 0.3 percent MoM. The rounded BLS Table A sequence since mid-2025 has a 0.29 percent mean across the 10 usable non-missing observations, while the first half of 2026 alone averages about 0.28 percent."},{"kind":"text","text":"Current-release adjustment: June's 0.0 percent print was pulled down by broad core weakness, including motor vehicle insurance at -2.0 percent and communication at -1.5 percent in the BLS June discussion, while shelter still rose 0.1 percent. I treat that as a downside signal but not a new zero-growth regime for services less energy."},{"kind":"math","text":"Prior/update/interval: persistence prior is the same-series recent BLS Table A base rate, sample Jul 2025, Aug 2025, Sep 2025, Dec 2025, Jan 2026, Feb 2026, Mar 2026, Apr 2026, May 2026, Jun 2026 = [0.4, 0.3, 0.2, 0.3, 0.4, 0.3, 0.2, 0.5, 0.3, 0.0]. Mean = 0.29; current-release adjustment is -0.04 for June cooling and shelter moderation plus +0.02 for likely partial reversal of one-off service drags, giving point = 0.27. Values are themselves percent-growth observations, so sigma = 0.14 from the sample standard deviation; 1.28*sigma = 0.18, giving an 80% interval of 0.27 +/- 0.18 = [0.09, 0.45]."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in motor vehicle insurance, airfares, medical care, or shelter that would land above the interval if services less energy prints near 0.5 percent or higher. Downside risk is another broad services decline, especially communication, insurance, lodging, and medical care, which would land below the interval if the print is near 0.0 percent or negative. Outside the interval would most likely reflect a concentrated component shock rather than normal monthly noise."},{"kind":"forecast","point":0.27,"ciLow":0.09,"ciHigh":0.45}]}
