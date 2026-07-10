# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.job_openings
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-openings-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.jolts.job_openings.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "bls.jolts.job_openings", "releasePolicy": "first_print", "sourceSeriesId": "bls.jolts.job_openings", "sourceUrl": "https://www.bls.gov/news.release/jolts.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-21e06e0656e420fc38e5db6513825baad3becf73234e1df0a074fcadcc13535f.json"
- targetContentHash: "21e06e0656e420fc38e5db6513825baad3becf73234e1df0a074fcadcc13535f"
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
821d5c291887a405807226bf5659b5d40c8796f56d3bf84d3157920af9bab75d

# Draft forecast response
{"slug":"jolts-openings-july-2026","country":"US","type":"data","title":"US JOLTS job openings, July 2026","question":"What will BLS first report for total nonfarm job openings, seasonally adjusted, in the July 2026 Job Openings and Labor Turnover Survey release?","unit":"millions","pointEstimate":7.29,"ciLow":6.74,"ciHigh":7.84,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover Survey","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.nr0.htm","resolutionRule":"Resolve to the first BLS Job Openings and Labor Turnover Survey news-release print for total nonfarm job openings, seasonally adjusted, for July 2026, reported in thousands and converted to millions by multiplying by 0.001. Use the value first published in the September 1, 2026 10:00 AM ET release; ignore later revisions and database updates after the first print.","dataPointId":"bls.jolts.job_openings.july_2026.first_print","historicalContext":[{"label":"2026-05 job openings SA total nonfarm, preliminary","value":7.594},{"label":"2026-04 job openings SA total nonfarm","value":7.585},{"label":"2026-03 job openings SA total nonfarm","value":6.887},{"label":"2026-02 job openings SA total nonfarm","value":6.922},{"label":"2026-01 job openings SA total nonfarm","value":7.24}],"drivers":["May JOLTS openings held near the April rebound at 7.594 million","June payroll employment rose only 57 thousand, arguing against a sustained openings surge","Unemployment was 4.2 percent in June, still consistent with a cooler labor market than 2022-2023","Two-month-ahead JOLTS prints are volatile, so the interval is wider than a one-month persistence band"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://data.bls.gov/timeseries/JTS000000000000000JOL","https://data.bls.gov/timeseries/CES0000000001","https://data.bls.gov/timeseries/LNS14000000"],"runAt":"2026-07-10T05:17:14Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 first-print JOLTS job openings"},{"kind":"text","text":"Framing: the target is BLS series JTS000000000000000JOL, total nonfarm job openings, seasonally adjusted, level in thousands, converted to millions. The BLS schedule page verifies that the July 2026 JOLTS reference month is scheduled for release on 2026-09-01 at 10:00 AM, so the ledger resolutionDate is consistent with the official calendar."},{"kind":"tool","tool":"official.lookup","call":"BLS data page for JTS000000000000000JOL, total nonfarm job openings, seasonally adjusted, level in thousands","result":"Fetched recent JOLTS levels: Jan 2026 7240 thousand, Feb 2026 6922 thousand, Mar 2026 6887 thousand, Apr 2026 7585 thousand, May 2026 7594(P) thousand; also 2025 Dec 6550 thousand and 2025 Nov 6846 thousand."},{"kind":"tool","tool":"official.lookup","call":"BLS CES data page for CES0000000001, total nonfarm payroll employment, seasonally adjusted, thousands","result":"Fetched payroll employment levels: Apr 2026 158798 thousand, May 2026 158927(P) thousand, Jun 2026 158984(P) thousand, implying May-to-Jun payroll growth of 57 thousand."},{"kind":"tool","tool":"official.lookup","call":"BLS CPS data page for LNS14000000, unemployment rate, seasonally adjusted","result":"Fetched unemployment rates: Apr 2026 4.3 percent, May 2026 4.3 percent, Jun 2026 4.2 percent; 2025 Dec was 4.4 percent and 2026 Jan was 4.3 percent."},{"kind":"text","text":"Reference class and base rate: for the same SA total nonfarm JOLTS level series, the 2024-01 through 2026-05 monthly path moved from 8.378 million to 7.594 million, with large month-to-month noise and no stable acceleration. A persistence/random-walk base rate from the latest official JOLTS print starts at 7.594 million."},{"kind":"text","text":"Variant control: all anchors above use seasonally adjusted total nonfarm job openings, level, not rates, not not-seasonally-adjusted values, and not revised FRED mirrors. The resolution will use the first BLS JOLTS print for that same variant."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest JTS000000000000000JOL May 2026 preliminary level 7.594 million; historical sample = fetched monthly JOLTS values from Jan 2024 through May 2026; successive-change sigma = 0.33 million from the 28 monthly changes; adjustment components = -0.20 million for weak June payroll growth of 57 thousand, -0.08 million for mean reversion after the Apr-May jump from 6.887 million to 7.594 million, -0.02 million for still-elevated unemployment near 4.2 percent; point = 7.594 - 0.20 - 0.08 - 0.02 = 7.294, rounded to 7.29 million. One-step 80 percent half-width is roughly 1.28*sigma = 1.28*0.33 = 0.42 million; I widen to 0.55 million, about 1.67*sigma, because the forecast is two reference months beyond the latest JOLTS print and the April rebound introduced regime uncertainty. Final implied bounds: 7.29 - 0.55 = 6.74 and 7.29 + 0.55 = 7.84 million."},{"kind":"text","text":"Upside risk: if July labor demand remains close to the Apr-May rebound and employers keep vacancies open despite soft payroll growth, the first print could land above the interval, especially above 7.84 million. Downside risk: if the May level was a temporary rebound and weak payroll hiring reflects broad demand cooling, July openings could fall back toward early-2026 levels and land below the interval. Outside the interval would require either a renewed vacancy surge above roughly 7.84 million or a sharp retracement below roughly 6.74 million."},{"kind":"forecast","point":7.29,"ciLow":6.74,"ciHigh":7.84}]}
