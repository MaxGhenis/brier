# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.quits_rate
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-quits-rate-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.quits_rate.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.quits_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.quits_rate", "sourceUrl": "https://www.bls.gov/news.release/jolts.t04.htm", "table": "U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-53d574820f5ef4c802754d8b06524a23672358e5dc546c4db118d3e3e5406ec7.json"
- targetContentHash: "53d574820f5ef4c802754d8b06524a23672358e5dc546c4db118d3e3e5406ec7"
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
178f88d55aa11e424303a438423a03ee8573cc2637355f450accbd6d2a443d32

# Draft forecast response
{"slug":"jolts-quits-rate-july-2026","country":"US","type":"data","title":"US JOLTS quits rate, July 2026","question":"BLS Job Openings and Labor Turnover Survey Table 4 total quits rate, seasonally adjusted, July 2026, first print","unit":"percent","pointEstimate":1.9,"ciLow":1.75,"ciHigh":2.05,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey Table 4","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t04.htm","resolutionRule":"Resolve to the first-print July 2026 seasonally adjusted Total quits rate in BLS JOLTS Table 4, 'Quits levels and rates by industry and region, seasonally adjusted', using the rate value in percent as published at the September 1, 2026 10:00 AM ET release. Do not use later revisions or annual benchmark updates.","dataPointId":"bls.jolts.quits_rate.2026-07.first_print","historicalContext":[{"label":"2026-05 preliminary total quits rate, SA","value":1.9},{"label":"2026-04 total quits rate, SA","value":1.9},{"label":"2026-03 total quits rate, SA","value":2.0},{"label":"2026-02 total quits rate, SA","value":1.9},{"label":"2025-05 total quits rate, SA","value":2.1}],"drivers":["latest total quits rate was 1.9 percent","recent total quits rate changes were small","private quits rate held at 2.1 percent","government quits rate remained 0.8 percent","leisure and hospitality rebound offsets softer health care and construction"],"sourceContext":["https://www.bls.gov/news.release/jolts.t04.htm","https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/schedule/2026/09_sched.htm"],"runAt":"2026-07-10T05:20:37Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS JOLTS total quits rate"},{"kind":"text","text":"Framing and exact resolver: this is the seasonally adjusted Total quits rate in BLS JOLTS Table 4, not the quits level, not not-seasonally-adjusted data, and not a revised vintage. The series code context is BLS JOLTS total nonfarm quits rate, and the ledger source URL points to Table 4."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule by release name and the September 2026 BLS calendar for the July 2026 reference month.","result":"BLS schedule lists July 2026 Job Openings and Labor Turnover Survey for Sep. 01, 2026 at 10:00 AM; it also lists June 2026 on Aug. 04, 2026 and August 2026 on Sep. 29, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current BLS JOLTS Table 4 Total row for seasonally adjusted quits levels and rates.","result":"Fetched Total quits levels and rates: May 2025 level 3,287 and rate 2.1; Feb. 2026 level 3,046 and rate 1.9; Mar. 2026 level 3,160 and rate 2.0; Apr. 2026 level 3,043 and rate 1.9; May 2026 preliminary level 3,065 and rate 1.9; Apr.-May 2026 rate change 0.0."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Table 4 industry rows to check whether total quits pressure was broad or sector-specific.","result":"Fetched industry rates for May 2026: total private 2.1, construction 1.3, manufacturing 1.4, retail trade 2.8, professional and business services 2.0, health care and social assistance 1.7, leisure and hospitality 4.0, government 0.8."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Table 4 regional rows to check geographic dispersion in the latest quits rate print.","result":"Fetched regional May 2026 quits rates: Northeast 1.4, South 2.3, Midwest 1.9, West 1.7; the Apr.-May 2026 regional changes were +0.1, +0.1, -0.1, and -0.2 respectively."},{"kind":"text","text":"Reference class and base rate: for a monthly level/rate series this close to release, the strongest outside-view anchor is persistence in the same SA total-rate series. The recent official reference class has total rates 1.9, 2.0, 1.9, and 1.9 from February through May 2026, with May 2025 at 2.1, so the base rate is near 1.9 rather than a return toward the 2021-2022 high-quits regime."},{"kind":"text","text":"Current-release adjustment: May 2026 was flat at 1.9 despite offsetting industry moves. Leisure and hospitality rose to 4.0 and other services to 2.5, but health care and social assistance eased to 1.7 and construction fell to 1.3. That mix argues for no material level adjustment from the 1.9 persistence prior."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official SA total quits rate of 1.9 using the February-May 2026 BLS Table 4 reference class. Successive monthly changes are +0.1, -0.1, and 0.0 percentage point, so sigma = 0.08 percentage point on those changes. The one-month 80% half-width is about 1.28*sigma = 1.28*0.08 = 0.10; for a two-reference-month horizon from May to July, scale by sqrt(2), giving 0.14, rounded to a 0.15 percentage point half-width. Point = 1.9 + 0.0 level/momentum adjustment = 1.9; 80% interval = 1.9 +/- 0.15 = [1.75, 2.05]."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed rise in voluntary separations if leisure, retail, and professional services all firm together, which would land above the interval at 2.1 or higher after one-decimal BLS rounding. Downside risk is a sharper labor-demand slowdown with quits falling across private services and government staying subdued, which would land below the interval at 1.7 or lower."},{"kind":"forecast","point":1.9,"ciLow":1.75,"ciHigh":2.05}]}
