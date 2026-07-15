# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.ecec.private_total_compensation.hourly_cost
- period: 2026-Q2
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-ecec-private-total-compensation-hourly-cost-q2-2026"
- country: "US"
- targetUnit: "usd"
- dataPointId: "bls.ecec.private_total_compensation.hourly_cost.2026_q2.first_print"
- resolutionSourceUrl: "https://www.bls.gov/news.release/ecec.toc.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-09", "start": "2026-09-09"}, "field": "Private industry workers; Total compensation; Cost per hour worked", "releasePolicy": "first_print", "sourceSeriesId": "BLS ECEC Table 1", "sourceUrl": "https://www.bls.gov/news.release/ecec.toc.htm", "table": "Employer Costs for Employee Compensation, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-f07de9fdb95478f14b96f101504b1e5d0404742bc86d896b9b296cd124bcc7f5.json"
- targetContentHash: "f07de9fdb95478f14b96f101504b1e5d0404742bc86d896b9b296cd124bcc7f5"
- registrationCommit: "4ca8bf2478e8cea37b8112b8821dc9865efdce9c"
- registeredAtUtc: "2026-07-15T21:20:34Z"
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
c4e8ab8083d525132c65265f3714c19cd97df7a113f591f07e2f6a94155908fe

# Draft forecast response
{"slug":"bls-ecec-private-total-compensation-hourly-cost-q2-2026","country":"US","type":"data","title":"US private compensation cost, Q2 2026","question":"What will BLS first report for private industry workers’ total compensation cost per hour worked in June 2026 (2026 Q2), in current US dollars, ECEC Table 1?","unit":"usd","pointEstimate":46.95,"ciLow":46.7,"ciHigh":47.2,"confidence":0.8,"resolutionDate":"2026-09-09","resolutionSource":"U.S. Bureau of Labor Statistics Employer Costs for Employee Compensation release","resolutionSourceUrl":"https://www.bls.gov/news.release/ecec.toc.htm","resolutionRule":"Resolve to the first value published on September 9, 2026 for “Private industry workers; Total compensation; Cost per hour worked” in Employer Costs for Employee Compensation Table 1 for June 2026. Use the current-dollar value as printed to the nearest cent; ignore all later revisions.","dataPointId":"bls.ecec.private_total_compensation.hourly_cost.2026_q2.first_print","historicalContext":[{"label":"March 2024","value":43.78},{"label":"June 2024","value":43.94},{"label":"September 2024","value":44.4},{"label":"December 2024","value":44.67},{"label":"March 2025","value":45.38},{"label":"June 2025","value":45.65},{"label":"September 2025","value":46.05},{"label":"December 2025","value":46.15},{"label":"March 2026","value":46.6}],"drivers":["Recent quarterly compensation-cost momentum","Private-industry wage growth","Benefits-cost growth","ECEC sampling and employment-weight variation"],"sourceContext":["https://www.bls.gov/news.release/ecec.t01.htm","https://www.bls.gov/schedule/news_release/ecec.htm","https://www.bls.gov/news.release/archives/ecec_03202026.htm","https://www.bls.gov/news.release/archives/ecec_02242026.htm","https://www.bls.gov/news.release/archives/ecec_09122025.htm","https://www.bls.gov/news.release/archives/ecec_06132025.htm","https://www.bls.gov/news.release/archives/ecec_03142025.htm","https://www.bls.gov/news.release/archives/ecec_12172024.htm","https://www.bls.gov/news.release/archives/ecec_09102024.htm","https://www.bls.gov/news.release/archives/ecec_06182024.htm"],"runAt":"2026-07-15T21:23:39Z","reasoning":[{"kind":"heading","text":"Forecast: private-industry total compensation cost in June 2026"},{"kind":"text","text":"The target is the first-print current-dollar cost per hour for private industry workers’ total compensation in BLS ECEC Table 1, June 2026. This is the published ECEC level rather than the seasonally adjusted Employment Cost Index; later revisions do not count."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest BLS ECEC Table 1 release.","result":"BLS Table 1 reports March 2026 private-industry total compensation of $46.60 per hour, comprising $32.60 in wages and salaries and $14.01 in benefits."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent first-published BLS ECEC private-industry total-compensation levels from archived releases.","result":"The fetched quarterly levels were $44.67 in December 2024, $45.38 in March 2025, $45.65 in June 2025, $46.05 in September 2025, $46.15 in December 2025, and $46.60 in March 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch the official BLS ECEC release schedule for June 2026 data.","result":"The BLS calendar schedules Employer Costs for Employee Compensation for June 2026 for September 9, 2026 at 10:00 AM ET; it also lists the prior March 2026 release on June 12, 2026 at 10:00 AM."},{"kind":"text","text":"The outside-view base rate is persistent quarterly growth: across the eight changes from March 2024 through March 2026, the increases were $0.16, $0.46, $0.27, $0.71, $0.27, $0.40, $0.10, and $0.45, averaging about $0.35 per quarter. The level effect starts at $46.60; momentum contributes about $0.35. Wage and benefit inflation support continued growth, while no specific one-off or policy mechanism warrants a separate adjustment."},{"kind":"math","text":"Prior/update/interval: a persistence model uses the latest $46.60 level plus the $0.35 mean change from the eight-quarter historical sample, with adjustment components of $0.00 for one-offs and $0.00 for policy mechanisms, yielding $46.95. The sample standard deviation of successive changes is sigma = $0.195; 1.28*sigma = $0.250, so the realized-dispersion 80% interval is $46.95 ± $0.25 = [$46.70, $47.20]."},{"kind":"text","text":"Upside risk comes from unusually strong wage growth, benefits inflation, or a composition shift toward high-compensation jobs and would land above the interval. Downside risk comes from weak hours-adjusted compensation growth or a composition shift toward lower-cost jobs and would land below the interval; either outcome outside the interval would falsify the recent-change reference class."},{"kind":"forecast","point":46.95,"ciLow":46.7,"ciHigh":47.2}]}
