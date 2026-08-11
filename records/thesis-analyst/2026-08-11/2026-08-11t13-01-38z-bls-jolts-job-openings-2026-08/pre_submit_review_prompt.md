# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.job_openings
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-openings-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.jolts.job_openings.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-10-05", "start": "2026-09-27"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-10-05", "start": "2026-09-27"}, "field": "bls.jolts.job_openings", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.job_openings", "sourceUrl": "https://www.bls.gov/news.release/jolts.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-66a38cce6c472dec90f4d80d7b32fa5be061746652b89c5733473d64ef4b6218.json"
- targetContentHash: "66a38cce6c472dec90f4d80d7b32fa5be061746652b89c5733473d64ef4b6218"
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
3be90fa6be5e448f47329afdfdfcef5ec939e667d46b951bed0e47aea53c39eb

# Draft forecast response
{"slug":"jolts-openings-august-2026","country":"US","type":"data","title":"US JOLTS Job Openings, August 2026","question":"What will the U.S. Bureau of Labor Statistics first report for seasonally adjusted total nonfarm job openings in the Job Openings and Labor Turnover Survey for August 2026, in millions?","unit":"millions","pointEstimate":7.1,"ciLow":6.45,"ciHigh":7.75,"confidence":0.8,"resolutionDate":"2026-09-29","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t01.htm","resolutionRule":"Resolve to the first official BLS Job Openings and Labor Turnover Survey release for August 2026, Table 1, seasonally adjusted Total job openings level. Use the level in thousands multiplied by 0.001 to report millions, rounded to three decimals if needed. Do not use later revisions or corrected subsequent releases unless BLS replaces the first-print page before ordinary revisions.","dataPointId":"bls.jolts.job_openings.august_2026.first_print","historicalContext":[{"label":"2026-06 SA total job openings","value":7.359},{"label":"2026-05 SA total job openings","value":7.537},{"label":"2026-04 SA total job openings","value":7.585},{"label":"2026-03 SA total job openings","value":6.887},{"label":"2026-02 SA total job openings","value":6.882}],"drivers":["June openings fell 178,000 to 7.359 million","July payroll employment was -23,000 with unemployment at 4.1 percent","Recent openings remain volatile around 7.0-7.6 million","Low-hire low-fire labor market argues for drift lower rather than collapse"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.nr0.htm","https://www.bls.gov/news.release/jolts.t01.htm","https://www.bls.gov/news.release/archives/jolts_03312026.htm","https://www.bls.gov/news.release/archives/jolts_05052026.htm","https://www.bls.gov/news.release/empsit.nr0.htm"],"runAt":"2026-08-11T13:02:49Z","reasoning":[{"kind":"heading","text":"US JOLTS job openings for August 2026"},{"kind":"text","text":"Resolver framing: this is BLS JOLTS Table 1 seasonally adjusted Total job openings, levels in thousands converted to millions. The ledger window ends 2026-10-05, but the official BLS JOLTS release schedule fetched this run lists August 2026 for September 29, 2026 at 10:00 AM, so I use 2026-09-29 as the verified release-calendar resolution date while keeping the registered slug and dataPointId."},{"kind":"tool","tool":"official.lookup","call":"BLS JOLTS release schedule lookup for reference month August 2026","result":"Fetched official schedule: July 2026 JOLTS release date Sep. 01, 2026 at 10:00 AM; August 2026 JOLTS release date Sep. 29, 2026 at 10:00 AM; September 2026 release date Nov. 03, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS current JOLTS summary and Table 1 for June 2026","result":"Fetched June 2026 release: total job openings 7.4 million in text; Table 1 Total levels were June 2025 7,204 thousand, March 2026 6,887 thousand, April 2026 7,585 thousand, May 2026 7,537 thousand, June 2026 7,359 thousand; June change from May was -178 thousand and the openings rate was 4.4 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS archived JOLTS release for February 2026","result":"Fetched February 2026 archive: Total job openings were 7,240 thousand in January 2026 and 6,882 thousand in February 2026; hires were 5,347 thousand in January and 4,849 thousand in February."},{"kind":"tool","tool":"official.lookup","call":"BLS archived JOLTS release for March 2026","result":"Fetched March 2026 archive: Total job openings were 6,922 thousand in February 2026 and 6,866 thousand in March 2026 first print; Table A also showed March 2025 at 6,952 thousand."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation for July 2026 as labor-market context","result":"Fetched July 2026 Employment Situation: nonfarm payroll employment was -23,000; unemployment rate was 4.1 percent; May payrolls were revised to +63,000 and June to +20,000, a combined 103,000 lower than previously reported."},{"kind":"text","text":"Base rate/reference class: for a two-month-ahead forecast of a level series, the strongest outside-view prior is persistence around the latest official JOLTS level. The recent official reference class is January-June 2026 total job openings around 6.9-7.6 million, with a current value of 7.359 million and no evidence of a large layoff shock."},{"kind":"math","text":"Prior/update/interval: persistence prior starts at June 2026 current-vintage 7.359 million. Updates are -0.18 million for the June down move continuing, -0.12 million for weak July payrolls and downward revisions, +0.04 million because openings are noisy and layoffs remain contained, giving 7.359 - 0.18 - 0.12 + 0.04 = 7.099, rounded to 7.10 million. Historical sample uses successive changes in current/official 2026 levels: Jan 7.240, Feb 6.882, Mar 6.887, Apr 7.585, May 7.537, Jun 7.359 million, so changes are -0.358, +0.005, +0.698, -0.048, -0.178 and sigma = 0.40 million. The one-month 80% half-width is 1.28*sigma = 1.28*0.40 = 0.51 million; I widen to 0.65 million for the two-month horizon to August, giving 7.10 +/- 0.65 = [6.45, 7.75]."},{"kind":"text","text":"Upside risk: a rebound in professional services, retail, or transportation postings after June's drop would land above the interval if openings print above 7.75 million. Downside risk: the July payroll contraction and weak revisions could mark a sharper employer retrenchment, and an August openings fall below 6.45 million would land outside the interval on the low side."},{"kind":"forecast","point":7.1,"ciLow":6.45,"ciHigh":7.75}]}
