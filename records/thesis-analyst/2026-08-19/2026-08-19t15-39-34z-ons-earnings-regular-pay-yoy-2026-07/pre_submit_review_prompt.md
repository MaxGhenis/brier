# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.earnings.regular_pay_yoy
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-regular-pay-growth-may-jul-2026"
- country: "UK"
- targetUnit: "percent"
- dataPointId: "ons.earnings.regular_pay_yoy.2026_07.first_print"
- expectedReleaseWindow: {"end": "2026-09-15", "start": "2026-09-15"}
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/kai9/lms"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-09-15", "start": "2026-09-15"}, "field": "AWE: Whole Economy Year on Year Three Month Average Growth (%): Seasonally Adjusted Regular Pay Excluding Arrears, value for 2026 JUL", "releasePolicy": "first_print", "sourceSeriesId": "KAI9", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/kai9/lms", "table": "Labour market statistics time series (LMS)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-19-b5e60c946429e3044f6145c5e79929649ce3f717336154df75101aed572a2c5e.json"
- targetContentHash: "b5e60c946429e3044f6145c5e79929649ce3f717336154df75101aed572a2c5e"
- registrationCommit: "1a8c5d83d07cc6160ba5e11d8754092d64a2fc64"
- registeredAtUtc: "2026-08-19T15:37:16Z"
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
57225ccc6f1945d0575e0ccd9bba9f5c4e84e92cdf24de98ee58012d4b38be7d

# Draft forecast response
{"slug":"uk-regular-pay-growth-may-jul-2026","country":"UK","type":"data","title":"UK regular pay growth, May-Jul 2026","question":"ONS KAI9 AWE whole economy year-on-year three-month average growth, seasonally adjusted regular pay excluding arrears, value for 2026 JUL, first print","unit":"percent","pointEstimate":3.5,"ciLow":2.8,"ciHigh":4.2,"confidence":0.8,"resolutionDate":"2026-09-15","resolutionSource":"Office for National Statistics Labour market statistics time series (LMS), KAI9","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/kai9/lms","resolutionRule":"Resolve to the first ONS-published KAI9 value for 2026 JUL in the Labour market statistics time series: AWE whole economy year-on-year three-month average growth (%), seasonally adjusted regular pay excluding arrears. Use the first print published for UK Labour Market: September 2026 on 15 September 2026, as displayed on the KAI9 time-series page, in percent and rounded as ONS publishes it; ignore later revisions or historical restatements.","dataPointId":"ons.earnings.regular_pay_yoy.2026_07.first_print","historicalContext":[{"period":{"type":"month","value":"2025-07"},"label":"July 2025","value":4.8},{"period":{"type":"month","value":"2025-08"},"label":"August 2025","value":4.7},{"period":{"type":"month","value":"2025-09"},"label":"September 2025","value":4.7},{"period":{"type":"month","value":"2025-10"},"label":"October 2025","value":4.6},{"period":{"type":"month","value":"2025-11"},"label":"November 2025","value":4.4},{"period":{"type":"month","value":"2025-12"},"label":"December 2025","value":4.1},{"period":{"type":"month","value":"2026-01"},"label":"January 2026","value":3.8},{"period":{"type":"month","value":"2026-02"},"label":"February 2026","value":3.6},{"period":{"type":"month","value":"2026-03"},"label":"March 2026","value":3.4},{"period":{"type":"month","value":"2026-04"},"label":"April 2026","value":3.4},{"period":{"type":"month","value":"2026-05"},"label":"May 2026","value":3.4},{"period":{"type":"month","value":"2026-06"},"label":"June 2026","value":3.5}],"drivers":["latest KAI9 print was 3.5 percent","recent six-print plateau near 3.5 percent","private-sector wage cooling restrains upside","public-sector pay awards support the aggregate","three-month averaging smooths one-month July movement"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/kai9/lms","https://www.ons.gov.uk/releases/uklabourmarketseptember2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/averageweeklyearningsingreatbritain/latest"],"runAt":"2026-08-19T15:39:59Z","reasoning":[{"kind":"heading","text":"UK regular pay growth first-print forecast"},{"kind":"text","text":"Framing and exact resolver: the target is ONS series KAI9, AWE whole economy year-on-year three-month average growth (%), seasonally adjusted regular pay excluding arrears, value for 2026 JUL. The official ONS UK Labour Market: September 2026 page verifies the release date as 15 September 2026 at 7:00am; I use the first KAI9 print and ignore later revisions."},{"kind":"text","text":"Variant discipline: all anchors below are from the same KAI9 variant named in the resolver: regular pay excluding arrears, seasonally adjusted, whole economy, year-on-year three-month average growth in percent."},{"kind":"tool","tool":"official.lookup","call":"ONS KAI9 time-series page, latest observed target-variant prints","result":"Fetched KAI9 recent values: 2026 JAN 3.8, 2026 FEB 3.6, 2026 MAR 3.4, 2026 APR 3.4, 2026 MAY 3.4, 2026 JUN 3.5 percent."},{"kind":"tool","tool":"official.lookup","call":"ONS KAI9 time-series page, prior six monthly prints for the same variant","result":"Fetched KAI9 prior values: 2025 JUL 4.8, 2025 AUG 4.7, 2025 SEP 4.7, 2025 OCT 4.6, 2025 NOV 4.4, 2025 DEC 4.1 percent."},{"kind":"tool","tool":"official.lookup","call":"ONS KAI9 metadata and ONS September 2026 labour-market release page","result":"Fetched metadata and schedule: KAI9 release date 18 August 2026, next release 15 September 2026, latest observed KAI9 value 2026 JUN 3.5, and UK Labour Market: September 2026 release time 7:00am."},{"kind":"text","text":"Base rate/reference class: the 12 fetched KAI9 prints from 2025 JUL through 2026 JUN average 4.03 percent, but the last six average 3.52 percent and the last four sit at 3.4, 3.4, 3.4, and 3.5, so persistence around 3.5 is the base rate for a one-month-ahead three-month-average target."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest KAI9 = 3.5 using the historical sample 2025 JUL-2026 JUN. Level adjustment is 0.0 because the latest six-print mean is 3.52 and the latest print is 3.5; momentum adjustment is 0.0 because the series flattened at 3.4-3.5; one-off adjustment is +0.0 to +0.1 from public-sector pay-award support offset by private-sector cooling; policy-mechanism adjustment is 0.0 because this is a labour-market survey print, not a policy decision. For this change/flow series I size uncertainty from the values themselves: sample sigma = 0.577 from [4.8, 4.7, 4.7, 4.6, 4.4, 4.1, 3.8, 3.6, 3.4, 3.4, 3.4, 3.5], so 1.28*sigma = 0.739. Rounding the point to 3.5 and the 80% interval to ONS-style one decimal gives 3.5 +/- about 0.7, or 2.8 to 4.2."},{"kind":"text","text":"Upside risk: a stronger July single-month pay reading, renewed public-sector award effects, or composition shifts toward higher-paid employment would land above the interval if they push KAI9 above 4.2. Downside risk: sharper private-sector wage cooling, weaker paid-hours composition, or survey reweighting would land below the interval if they push KAI9 below 2.8. Outside the interval would require a break from the recent 3.4-3.5 plateau rather than ordinary month-to-month noise."},{"kind":"forecast","point":3.5,"ciLow":2.8,"ciHigh":4.2}]}
