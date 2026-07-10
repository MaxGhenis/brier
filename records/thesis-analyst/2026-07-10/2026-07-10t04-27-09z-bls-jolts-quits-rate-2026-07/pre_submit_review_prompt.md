# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.quits_rate
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-quits-rate-july-2026"
- targetUnit: "percent"
- dataPointId: "bls.jolts.quits_rate.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.quits_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.quits_rate", "sourceUrl": "https://www.bls.gov/news.release/jolts.t04.htm", "table": "U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4", "transform": {"factor": 1.0, "operation": "multiply"}}
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
650c0538ee3ed5cedbdc39800ebeead6dd73bc99d3bc6bdb6caa8e81c5179db3

# Draft forecast response
{"slug":"jolts-quits-rate-july-2026","country":"US","type":"data","title":"US JOLTS Quits Rate, July 2026","question":"What will the BLS JOLTS total nonfarm quits rate, seasonally adjusted, be for July 2026 in the first print?","unit":"percent","pointEstimate":1.9,"ciLow":1.73,"ciHigh":2.07,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first-print July 2026 seasonally adjusted Total quits rate in BLS JOLTS Table 4, in percent/rate units as published to one decimal place; ignore later revisions or annual benchmark updates.","dataPointId":"bls.jolts.quits_rate.2026-07.first_print","historicalContext":[{"label":"May 2026 preliminary","value":1.9},{"label":"Apr 2026","value":1.9},{"label":"Mar 2026","value":2},{"label":"Feb 2026","value":1.9},{"label":"May 2025","value":2.1}],"drivers":["Recent quits rate flat at 1.9-2.0 percent","Job openings rate firmer at 4.6 percent but hires rate steady at 3.3 percent","First-print monthly noise around one tenth","Labor-market churn remains below 2021-2022 highs"],"sourceContext":["https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/schedule/news_release/jolts.htm","https://fred.stlouisfed.org/series/JTSQUR","https://www.bls.gov/news.release/jolts.t01.htm","https://www.bls.gov/news.release/jolts.t02.htm"],"runAt":"2026-07-10T04:27:20Z","reasoning":[{"kind":"heading","text":"July 2026 BLS JOLTS total nonfarm quits-rate forecast"},{"kind":"text","text":"Framing and exact resolver: this is the BLS Job Openings and Labor Turnover Survey Table 4 Total quits rate, seasonally adjusted, for July 2026, first print only. The BLS JOLTS release schedule lists reference month July 2026 for release on Sep. 01, 2026 at 10:00 AM, so I set resolutionDate to 2026-09-01 rather than inferring from cadence."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Table 4, quits levels and rates by industry and region, seasonally adjusted, current May 2026 release.","result":"Fetched Total quits rates: May 2025 2.1, Feb 2026 1.9, Mar 2026 2.0, Apr 2026 1.9, May 2026 preliminary 1.9; Total quits levels were 3,287k, 3,046k, 3,160k, 3,043k, and 3,065k respectively."},{"kind":"tool","tool":"public.history_mirror","call":"Check FRED JTSQUR mirror for the same BLS-sourced seasonally adjusted total nonfarm quits-rate series.","result":"Fetched JTSQUR recent observations: Jan 2026 2.0, Feb 2026 1.9, Mar 2026 2.0, Apr 2026 1.9, May 2026 1.9; FRED says units are Rate, seasonally adjusted, monthly, source U.S. Bureau of Labor Statistics, updated Jun 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS JOLTS Tables 1 and 2 for adjacent labor-demand indicators from the same release vintage.","result":"Fetched Total job openings rates: May 2025 4.4, Feb 2026 4.2, Mar 2026 4.2, Apr 2026 4.6, May 2026 4.6; Total hires rates: May 2025 3.4, Feb 2026 3.1, Mar 2026 3.5, Apr 2026 3.3, May 2026 3.3."},{"kind":"text","text":"Reference class and base rate: for this level/rate series I use the recent same-variant BLS seasonally adjusted Total quits-rate values as the base rate, because the target is also SA Total first print. The latest official rate is 1.9 and the five-point recent range is 1.9 to 2.1, with no evidence in the fetched data of a break away from roughly 2.0."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest same-series BLS/FRED value, 1.9. Historical sample = fetched SA Total quits rates May 2025, Feb 2026, Mar 2026, Apr 2026, May 2026: 2.1, 1.9, 2.0, 1.9, 1.9. Adjustment components: level 0.00 from latest 1.9, momentum 0.00 from Apr-to-May change 0.0, openings/hires mix +0.02 because openings rate is firm at 4.6 while hires is flat at 3.3, rounded back to the one-decimal first-print center of 1.9. For interval, successive changes are -0.2, +0.1, -0.1, 0.0; sample sigma = 0.13, so 80% half-width = 1.28*0.13 = 0.17. Final implied bounds: 1.90 - 0.17 = 1.73 and 1.90 + 0.17 = 2.07."},{"kind":"text","text":"Upside risk: July could land above the interval if the firmer openings rate translates into materially stronger quits in leisure/hospitality or retail, or if June data, not yet available at run time, jumps above 2.1. Downside risk: it would land below the interval if labor-market caution suppresses voluntary quits and total quits slip toward 1.7 or less. Outside the interval is mainly a regime-change case rather than normal one-month noise."},{"kind":"forecast","point":1.9,"ciLow":1.73,"ciHigh":2.07}]}
