# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.telework_share
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-telework-rate-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.cps.telework_share.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "bls.cps.telework_share", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.telework_share", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea41.htm", "table": "U.S. Bureau of Labor Statistics, Employment Situation, CPS Table A-41", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-6cf0d9882448a529f400c8923c7c59cd04582d25bc948a6c7238eb38f11374f5.json"
- targetContentHash: "6cf0d9882448a529f400c8923c7c59cd04582d25bc948a6c7238eb38f11374f5"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"
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
0c91655fc6535f3f5b206dffb186ed916fc9ad2b50c0b6fa0d50f3d981d23798

# Draft forecast response
{"slug":"us-telework-rate-august-2026","country":"US","type":"data","title":"US telework rate, August 2026","question":"What will BLS CPS Table A-41 first print report as the not seasonally adjusted telework rate, percent of total people at work, for Total, 16 years and over, August 2026?","unit":"percent","pointEstimate":22.1,"ciLow":21.5,"ciHigh":22.7,"confidence":0.8,"resolutionDate":"2026-09-04","resolutionSource":"U.S. Bureau of Labor Statistics, Employment Situation, CPS Table A-41","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea41.htm","resolutionRule":"Resolve to the first official BLS Employment Situation supplemental CPS Table A-41 print for August 2026, not seasonally adjusted, row Total, 16 years and over, Percent distribution column People who teleworked or worked at home for pay. Use the value as displayed in percent, normally to one decimal place, and do not revise for later table updates or subsequent vintages.","dataPointId":"bls.cps.telework_share.2026-08.first_print","historicalContext":[{"label":"2026-07 latest","value":22.2},{"label":"2026-06","value":21.7},{"label":"2026-05","value":21.8},{"label":"2026-04","value":21.7},{"label":"2025-08 prior August","value":22.1}],"drivers":["July 2026 level was 22.2 percent","Recent 2026 readings clustered from 21.7 to 22.7 percent after January","August seasonal reference changes were modest in 2023-2025","Not seasonally adjusted CPS telework series has visible month-to-month sampling noise","Remote-work structure appears stable, with limited reason for a one-month break"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea41.htm","https://data.bls.gov/timeseries/LNU0201B46B","https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1","https://www.bls.gov/cps/telework.htm"],"runAt":"2026-08-11T13:09:27Z","reasoning":[{"kind":"heading","text":"US CPS telework share, August 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS CPS telework rate, series LNU0201B46B, for August 2026 on CPS Table A-41. The variant is not seasonally adjusted and national, measured as people who teleworked or worked at home for pay as a percent of total people at work, Total, 16 years and over."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Employment Situation CPS Table A-41 current table at https://www.bls.gov/web/empsit/cpseea41.htm.","result":"Fetched July 2026 Table A-41 row Total, 16 years and over: total people at work 153,406 thousand; people who teleworked or worked at home for pay 34,079 thousand; teleworked some hours 17,134 thousand; teleworked all hours 16,946 thousand; percent distribution teleworked 22.2, some hours 11.2, all hours 11.0, did not telework 77.8."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS public time series page for LNU0201B46B at https://data.bls.gov/timeseries/LNU0201B46B.","result":"Fetched LNU0201B46B values: 2026 Jan 23.0, Feb 22.7, Mar 22.6, Apr 21.7, May 21.8, Jun 21.7, Jul 22.2; 2025 Jul 22.1, Aug 22.1, Sep 22.3, Nov 22.9, Dec 22.5; 2024 Jul 23.0, Aug 22.8, Sep 23.7."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Schedule of Releases for the Employment Situation at https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1.","result":"Fetched official schedule: Reference Month August 2026 has Release Date Sep. 04, 2026 and Release Time 08:30 AM; July 2026 was Aug. 07, 2026 at 08:30 AM; September 2026 is scheduled Oct. 02, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS telework concepts page at https://www.bls.gov/cps/telework.htm.","result":"Fetched measurement context: BLS added CPS telework questions starting in October 2022; the telework rate is the number of people who telework or work at home for pay as a percentage of those employed and at work during the survey reference week; the published monthly estimates are not seasonally adjusted."},{"kind":"text","text":"Base rate and reference class: I use the official monthly LNU0201B46B series since October 2022, emphasizing 2024-2026 because the series has settled into a post-pandemic plateau. The base rate is persistence around the recent 21.7-22.7 percent band rather than a trend extrapolation from the 2022-2024 rise."},{"kind":"text","text":"Level and momentum: July 2026 printed 22.2 after 21.7 in June and 21.8 in May. The 2026 year-to-date average through July is about 22.24, but April-July average is about 21.85, so I center just below July at 22.1 rather than chasing the one-month rebound."},{"kind":"text","text":"Seasonal and one-off adjustment: August changes in the available official series were small: July to August was -0.4 in 2023, -0.2 in 2024, and 0.0 in 2025. Applying roughly -0.1 to -0.2 to the July 2026 reading of 22.2 gives 22.0-22.1; the stable work-from-home structure argues against a larger mechanical move."},{"kind":"math","text":"Prior/update/interval: persistence prior = July 2026 LNU0201B46B level 22.2, historical sample = official LNU0201B46B recent monthly changes Feb-Jul 2026 of -0.3, -0.1, -0.9, +0.1, -0.1, +0.5 percentage points plus August seasonal changes of -0.4, -0.2, and 0.0 from 2023-2025; adjustment components = -0.1 for August seasonality and no material structural policy shock, giving point 22.1. For interval sizing on recent successive changes, sigma = sqrt((0.09+0.01+0.81+0.01+0.01+0.25)/6) = 0.44 percentage point, so 1.28*sigma = 0.57; rounded around 22.1 gives an 80% interval of 21.5 to 22.7."},{"kind":"text","text":"Counter-considerations: upside risk is a survey mix or white-collar employment composition shift that keeps July's rebound and would land above the interval if the first print is above 22.7. Downside risk is a vacation/reference-week or composition effect similar to April 2026 that would land below the interval if the first print is below 21.5. Outside the interval would most likely indicate sampling noise or a genuine change in who was at work during the August CPS reference week, not a slow trend."},{"kind":"forecast","point":22.1,"ciLow":21.5,"ciHigh":22.7}]}
