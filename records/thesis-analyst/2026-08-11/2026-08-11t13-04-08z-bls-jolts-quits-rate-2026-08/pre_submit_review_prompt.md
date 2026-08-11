# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.quits_rate
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-quits-rate-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.quits_rate.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-10-05", "start": "2026-09-27"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-10-05", "start": "2026-09-27"}, "field": "bls.jolts.quits_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.quits_rate", "sourceUrl": "https://www.bls.gov/news.release/jolts.t04.htm", "table": "U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-918146c0e3bb21526c56eb23c225d8c6f3541e00414806667c0a943eb10a6b6f.json"
- targetContentHash: "918146c0e3bb21526c56eb23c225d8c6f3541e00414806667c0a943eb10a6b6f"
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
e45d9933d45b1f247dd44b5a0f6186ee3350607ea7018791919ed5f183d96f93

# Draft forecast response
{"slug":"jolts-quits-rate-august-2026","country":"US","type":"data","title":"US JOLTS quits rate, Aug. 2026","question":"What will the U.S. Bureau of Labor Statistics JOLTS Table 4 seasonally adjusted Total nonfarm quits rate be for August 2026 in the first print?","unit":"percent","pointEstimate":1.9,"ciLow":1.7,"ciHigh":2.1,"confidence":0.8,"resolutionDate":"2026-09-29","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first BLS-published seasonally adjusted Total nonfarm quits rate in JOLTS Table 4 for August 2026, reported as a percent and rounded as BLS publishes it. Use the first print only; ignore later revisions.","dataPointId":"bls.jolts.quits_rate.2026-08.first_print","historicalContext":[{"label":"June 2025 SA Total quits rate","value":2.1},{"label":"March 2026 SA Total quits rate","value":2},{"label":"April 2026 SA Total quits rate","value":1.9},{"label":"May 2026 SA Total quits rate","value":2},{"label":"June 2026 SA Total quits rate","value":2}],"drivers":["Recent BLS Table 4 Total nonfarm quits rate is stable around 2.0 percent","July payroll employment weakness lowers worker-confidence and voluntary-quit pressure","June JOLTS openings and hires were little changed, arguing against a sharp break","Resolution is the seasonally adjusted Total nonfarm rate, not the Total private or not seasonally adjusted variant"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/news.release/jolts.nr0.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/series/JTSQUR"],"runAt":"2026-08-11T13:04:34Z","reasoning":[{"kind":"heading","text":"Forecast for BLS JOLTS quits rate, August 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is BLS JOLTS Table 4, seasonally adjusted Total nonfarm quits rate, series JTSQUR in FRED mirror terms, for August 2026. The resolver is the BLS first print on the Table 4 release page, not FRED, not Total private, and not the not-seasonally-adjusted Table 11 variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule page for the August 2026 reference month.","result":"The BLS schedule lists August 2026 JOLTS for Sep. 29, 2026 at 10:00 AM, with July 2026 on Sep. 1, 2026 and September 2026 on Nov. 3, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched current BLS JOLTS Table 4, seasonally adjusted quits levels and rates by industry and region.","result":"For Total, BLS Table 4 shows quits rates of 2.1 in June 2025, 2.0 in March 2026, 1.9 in April 2026, 2.0 in May 2026, and 2.0 in June 2026; levels were 3,254 thousand, 3,160 thousand, 3,043 thousand, 3,153 thousand, and 3,232 thousand respectively."},{"kind":"tool","tool":"official.lookup","call":"Fetched the BLS JOLTS June 2026 summary for broader turnover conditions.","result":"The June 2026 JOLTS summary reported job openings at 7.4 million, hires at 5.3 million, total separations at 5.4 million, quits at 3.2 million, and the quits rate at 2.0 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetched the BLS Employment Situation for July 2026 as a contemporaneous labor-market signal before the August JOLTS period.","result":"The July 2026 Employment Situation reported nonfarm payroll employment of -23,000, unemployment rate of 4.1 percent, May and June payroll revisions totaling -103,000, labor-force participation at 61.4 percent, and average hourly earnings up 3.2 percent over the year."},{"kind":"text","text":"Reference class and base rate: for a low-volatility rate series like Total nonfarm quits, the strongest base rate is persistence around the latest official BLS Table 4 level. The recent official reference class averages about 2.0 percent across June 2025 and March-June 2026, with the sequential 2026 observations centered just under 2.0."},{"kind":"math","text":"Prior/update/interval: persistence model prior = latest official June 2026 rate of 2.0 percent, historical sample = BLS Table 4 seasonally adjusted Total rates for March-June 2026 of 2.0, 1.9, 2.0, 2.0; adjustment components = -0.05 for weaker July payrolls and downward revisions, -0.02 for lower participation/worker-confidence pressure, +0.02 for still-stable JOLTS openings and hires, rounded to a -0.1 point net forecast adjustment over July-August; interval method = sample sigma of monthly changes from March-June changes (-0.1, +0.1, 0.0) is sigma = 0.10 for one month, two-month sigma = sqrt(2)*0.10 = 0.14, 80 percent half-width = 1.28*0.14 = 0.18, rounded to 0.2; final implied bounds are 1.9 - 0.2 = 1.7 and 1.9 + 0.2 = 2.1."},{"kind":"text","text":"Counter-considerations: upside risk would come from a July or August rebound in labor demand that lifts quits back above 2.1, especially in leisure, retail, or professional services. Downside risk would come from a clearer labor-market break after the -23,000 July payroll print; a broad pullback in voluntary separations would land below the interval if the first-print rate is under 1.7."},{"kind":"forecast","point":1.9,"ciLow":1.7,"ciHigh":2.1}]}
