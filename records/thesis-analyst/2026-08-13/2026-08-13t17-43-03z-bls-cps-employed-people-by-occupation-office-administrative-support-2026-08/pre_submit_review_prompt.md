# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.office_administrative_support
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-office-admin-employment-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.office_administrative_support.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "Office and administrative support occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.office_administrative_support", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-97182edc98810caf5f7cc705f823bcd9a54c5944671d801e01b57605272a7458.json"
- targetContentHash: "97182edc98810caf5f7cc705f823bcd9a54c5944671d801e01b57605272a7458"
- registrationCommit: "27d485d528684bbe8281fa349cfbb9587169dd5b"
- registeredAtUtc: "2026-08-13T16:32:19Z"
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
165734c715b3e669f246517034f2c60109fcc7a32626e892372d8f36d688c150

# Draft forecast response
{
  "slug": "cps-office-admin-employment-august-2026",
  "country": "US",
  "type": "data",
  "title": "US office and administrative support employment, August 2026",
  "question": "What will BLS first publish for August 2026 in CPS Employment Situation Table A-19, row 'Office and administrative support occupations,' Total, 16 years and over, not seasonally adjusted, reported in thousands and converted to millions?",
  "unit": "millions",
  "pointEstimate": 16.457,
  "ciLow": 16.112,
  "ciHigh": 16.802,
  "confidence": 0.8,
  "resolutionDate": "2026-09-11",
  "resolutionSource": "BLS, Employment Situation Table A-19",
  "resolutionSourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm",
  "resolutionRule": "Resolve to the first value published by BLS for August 2026 in CPS Employment Situation Table A-19, row 'Office and administrative support occupations,' Total, 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Use the first official print only, with no later revisions or later correction exceptions. BLS's Employment Situation release calendar fetched this run lists the August 2026 Employment Situation for September 4, 2026 at 08:30 AM ET; the registered Thesis target contract sets resolutionDate to 2026-09-11, so this cell preserves the registered date and records the discrepancy.",
  "dataPointId": "bls.cps.employed_people_by_occupation.office_administrative_support.august_2026.first_print",
  "historicalContext": [
    { "label": "2026-07 BLS LNU02032207", "value": 16.457 },
    { "label": "2026-06 BLS LNU02032207", "value": 16.184 },
    { "label": "2026-05 BLS LNU02032207", "value": 16.335 },
    { "label": "2026-04 BLS LNU02032207", "value": 16.471 },
    { "label": "2026-03 BLS LNU02032207", "value": 16.563 },
    { "label": "2025-08 BLS LNU02032207", "value": 16.415 }
  ],
  "drivers": [
    "last-print persistence",
    "mixed recent monthly changes",
    "weak August seasonal signal",
    "CPS occupation sampling volatility"
  ],
  "sourceContext": [
    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
    "https://data.bls.gov/timeseries/LNU02032207",
    "https://www.bls.gov/web/empsit/cpseea19.htm",
    "https://www.bls.gov/schedule/news_release/empsit.htm",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-13T17:43:16Z",
  "activityLog": [],
  "reasoning": [
    { "kind": "heading", "text": "August 2026 office/admin CPS employment forecast" },
    { "kind": "text", "text": "Framing: this target resolves to the BLS CPS Employment Situation Table A-19 row 'Office and administrative support occupations,' Total, 16 years and over, not seasonally adjusted, for August 2026, first print, with the BLS thousands value converted to millions by multiplying by 0.001. The registered target binds slug cps-office-admin-employment-august-2026, unit millions, and dataPointId bls.cps.employed_people_by_occupation.office_administrative_support.august_2026.first_print." },
    { "kind": "tool", "tool": "bls.calendar", "call": "Open https://www.bls.gov/schedule/news_release/empsit.htm during this run.", "result": "The BLS Employment Situation schedule lists August 2026 with release date Sep. 04, 2026 and release time 08:30 AM. The ledger target context supplied here has expectedReleaseWindow 2026-09-03 to 2026-09-11 and registered resolutionDate 2026-09-11, so I preserve 2026-09-11 and note the official-calendar discrepancy." },
    { "kind": "tool", "tool": "bls.table", "call": "Open https://www.bls.gov/web/empsit/cpseea19.htm during this run.", "result": "BLS Table A-19, Last Modified Date August 07, 2026, row 'Office and administrative support occupations' reports July 2025 Total 16 years and over = 16,565 thousand and July 2026 Total 16 years and over = 16,457 thousand; converted values are 16.565 million and 16.457 million." },
    { "kind": "tool", "tool": "bls.api", "call": "curl -sS -H 'Content-type: application/json' -d '{\"seriesid\":[\"LNU02032207\"],\"startyear\":\"2024\",\"endyear\":\"2026\"}' https://api.bls.gov/publicAPI/v2/timeseries/data/", "result": "BLS API series LNU02032207 values fetched this run include 2026-07 16,457 thousand, 2026-06 16,184, 2026-05 16,335, 2026-04 16,471, 2026-03 16,563, 2026-02 16,380, 2026-01 16,291, 2025-12 16,344, 2025-11 17,102, 2025-09 16,608, 2025-08 16,415, and 2025-07 16,565; 2025-10 is '-' because data were unavailable due to the 2025 lapse in appropriations." },
    { "kind": "tool", "tool": "bls.metadata", "call": "Open https://data.bls.gov/timeseries/LNU02032207 during this run.", "result": "BLS time-series metadata for LNU02032207 says Series title = '(Unadj) Employment Level - Office and Administrative Support Occupations' and Not Seasonally Adjusted; the July 2026 API/table value is 16,457 thousand." },
    { "kind": "tool", "tool": "thesis.slug_check", "call": "curl -sS -L https://app.thesisinstitute.org/specs.json", "result": "The requested slug-check URL returned HTTP 404 with a Next.js not-found page during this run. I therefore checked the provided registered target context and local public repo target file, which both name catalogSlug cps-office-admin-employment-august-2026 and targetContentHash 97182edc98810caf5f7cc705f823bcd9a54c5944671d801e01b57605272a7458." },
    { "kind": "text", "text": "Base rate / reference class: using the last 24 available BLS LNU02032207 monthly values from 2024-07 through 2026-07, excluding the missing 2025-10 print, the levels are 15.814 to 17.102 million with mean 16.316, median 16.362, and latest 16.457. For this repeated level series the benchmark prior is last-print persistence at 16.457 million; the two fetched July-to-August moves are mixed, +0.088 million in 2024 and -0.150 million in 2025, so they do not justify a material move from persistence." },
    { "kind": "text", "text": "Model candidates under thesis_model_candidate_v1: persistence candidate point 16.457, p10 16.112, p50 16.457, p90 16.802, 80% interval [16.112, 16.802], 90% interval [16.013, 16.901], interval_method recent consecutive-change residual sigma, calibration_n 22, train_cutoff 2026-07, walk_forward_mae 0.202 million, walk_forward_rmse 0.264 million. I select persistence because no direct August-specific signal beats it." },
    { "kind": "math", "text": "Using consecutive month-to-month changes in the last 24 available observations, excluding the Sep-to-Nov 2025 gap as non-consecutive, changes in millions are +0.088, -0.057, +0.069, +0.152, +0.401, -0.260, +0.286, +0.034, -0.485, +0.073, +0.354, +0.096, -0.150, +0.193, -0.758, -0.053, +0.089, +0.183, -0.092, -0.136, -0.151, +0.273. Their sample sigma = 0.270 million, so the normal 80% half-width is 1.28*sigma = 1.28*0.270 = 0.345 million. Persistence point 16.457 gives 16.457 - 0.345 = 16.112 and 16.457 + 0.345 = 16.802." },
    { "kind": "math", "text": "Prior/update/interval: prior = last-print persistence from July 2026 BLS LNU02032207 at 16.457 million; historical sample = last 24 available official monthly values and 22 consecutive monthly changes through 2026-07; adjustment components = 0.000 million because July-to-August history is mixed (+0.088, -0.150) and no current official signal was fetched that clears the update test; interval method = recent first-print/contemporaneous BLS monthly change residuals, sigma = 0.270 million, half-width = 1.28*sigma = 0.345 million, implying 80% bounds 16.112 to 16.802 million." },
    { "kind": "text", "text": "Counter-consideration: upside risk would land above the interval if the August CPS sample reverses the May-June softness and clerical employment jumps by more than about 345 thousand from July. Downside risk would land below the interval if the July rebound was sampling noise and office/admin employment falls by more than about 345 thousand, as happened in several recent large negative monthly moves." },
    { "kind": "forecast", "point": 16.457, "ciLow": 16.112, "ciHigh": 16.802 }
  ]
}
