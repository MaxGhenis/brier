# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.transportation_material_moving
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-transport-material-moving-employment-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.transportation_material_moving.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-10", "start": "2026-09-02"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-10", "start": "2026-09-02"}, "field": "Transportation and material moving occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.transportation_material_moving", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-5e45cb7c24096d5bf9d923f4e6c376d3ef8f27cdc78f26616b90e35848c3bb7d.json"
- targetContentHash: "5e45cb7c24096d5bf9d923f4e6c376d3ef8f27cdc78f26616b90e35848c3bb7d"
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
727c780a9ce2df98c7366d521962679e0e8c960fd5df92625caa6d98847e57b6

# Draft forecast response
{
  "slug": "cps-transport-material-moving-employment-august-2026",
  "country": "US",
  "type": "data",
  "title": "US transportation and material-moving employment, August 2026",
  "question": "What will BLS first report for August 2026 employed people in transportation and material moving occupations, total age 16 years and over, not seasonally adjusted, in CPS Employment Situation Table A-19, converted from thousands to millions?",
  "unit": "millions",
  "pointEstimate": 12.26,
  "ciLow": 11.85,
  "ciHigh": 12.67,
  "confidence": 0.8,
  "resolutionDate": "2026-09-10",
  "resolutionSource": "U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19",
  "resolutionSourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm",
  "resolutionRule": "Resolve to the first value published for August 2026 in BLS CPS Employment Situation Table A-19, row 'Transportation and material moving occupations,' Total, 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Retain that first print despite later revisions, rounded to three decimals in millions. The registered target binds resolutionDate 2026-09-10; the checked BLS July 2026 release notice schedules the August 2026 Employment Situation for September 4, 2026, so this date discrepancy is stated without changing the registered target identity.",
  "dataPointId": "bls.cps.employed_people_by_occupation.transportation_material_moving.august_2026.first_print",
  "historicalContext": [
    {
      "label": "January 2026 first print, NSA millions",
      "value": 12.202
    },
    {
      "label": "February 2026 first print, NSA millions",
      "value": 11.737
    },
    {
      "label": "March 2026 first print, NSA millions",
      "value": 12.214
    },
    {
      "label": "April 2026 first print, NSA millions",
      "value": 12.127
    },
    {
      "label": "May 2026 first print, NSA millions",
      "value": 12.12
    },
    {
      "label": "June 2026 first print, NSA millions",
      "value": 12.01
    },
    {
      "label": "July 2026 first print, NSA millions",
      "value": 12.223
    }
  ],
  "drivers": [
    "July 2026 first-print persistence at 12.223 million",
    "mixed recent monthly CPS occupation volatility",
    "small August seasonal pull from 2024-2025 history",
    "July payroll release showed transportation and warehousing little changed",
    "registered date differs from BLS release notice"
  ],
  "sourceContext": [
    "https://www.bls.gov/web/empsit/cpseea19.htm",
    "https://www.bls.gov/news.release/empsit.nr0.htm",
    "https://www.bls.gov/news.release/empsit.t13.htm",
    "https://www.bls.gov/news.release/archives/empsit_02112026.htm",
    "https://www.bls.gov/news.release/archives/empsit_03062026.htm",
    "https://www.bls.gov/news.release/archives/empsit_04032026.htm",
    "https://www.bls.gov/news.release/archives/empsit_05082026.htm",
    "https://www.bls.gov/news.release/archives/empsit_06052026.htm",
    "https://www.bls.gov/news.release/archives/empsit_08022024.htm",
    "https://www.bls.gov/news.release/archives/empsit_09062024.htm",
    "https://www.bls.gov/news.release/archives/empsit_08012025.htm",
    "https://www.bls.gov/news.release/archives/empsit_09052025.htm"
  ],
  "runAt": "2026-08-13T17:02:19Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "August 2026 CPS transportation and material-moving employment forecast"
    },
    {
      "kind": "text",
      "text": "The resolver is the BLS CPS occupation table row 'Transportation and material moving occupations,' total age 16 years and over, not seasonally adjusted, first August 2026 print, reported in thousands and converted to millions. The ledger binds cpseea19/Table A-19; current BLS release navigation exposes the same occupation table as Table A-13, so I keep the registered source URL and target identity."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Checked the current BLS Employment Situation release notice and registered target context.",
      "result": "BLS says the July 2026 Employment Situation was released August 7, 2026 and that the Employment Situation for August 2026 is scheduled for Friday, September 4, 2026 at 8:30 a.m. ET; the registered target context binds resolutionDate 2026-09-10."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetched BLS CPS occupation table first-print values for January-April 2026.",
      "result": "Transportation and material moving occupations employment was 12,202 thousand in January 2026, 11,737 thousand in February 2026, 12,214 thousand in March 2026, and 12,127 thousand in April 2026."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetched BLS CPS occupation table first-print values for May-July 2026.",
      "result": "Transportation and material moving occupations employment was 12,120 thousand in May 2026, 12,010 thousand in June 2026, and 12,223 thousand in July 2026; July 2026 total employment in Table A-13 was 162,800 thousand."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetched recent August seasonal reference values from BLS archived Employment Situation occupation tables.",
      "result": "The July-to-August first-print change was 11,977 to 12,322 thousand in 2024, or +0.345 million, and 11,659 to 11,647 thousand in 2025, or -0.012 million; the two-year August seasonal average is +0.166 million."
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "Fetched current labor-market context from the July 2026 Employment Situation release.",
      "result": "BLS reported total nonfarm payroll employment changed -23,000 in July 2026, unemployment was 4.1 percent, and employment showed little change in transportation and warehousing."
    },
    {
      "kind": "tool",
      "tool": "model_candidates",
      "call": "Generated thesis_model_candidate_v1 candidates from fetched Jan-Jul 2026 first-print levels.",
      "result": "Candidate persistence: point 12.223, p10 11.815, p50 12.223, p90 12.631, 80% interval [11.815, 12.631], 90% interval [11.698, 12.748], interval_method recent_change_normal_sigma_0.319, calibration_n 6, train_cutoff 2026-07, walk_forward_score unavailable. Candidate seasonal-shrunken persistence: point 12.265, p10 11.856, p50 12.265, p90 12.673, 80% interval [11.856, 12.673], 90% interval [11.739, 12.790], interval_method recent_change_normal_sigma_0.319, calibration_n 6, train_cutoff 2026-07, walk_forward_score unavailable."
    },
    {
      "kind": "text",
      "text": "Base rate/reference class: the strongest benchmark is July-level persistence because this is a noisy not-seasonally-adjusted CPS occupation level and no walk-forward evidence here beats persistence. Recent fetched levels run 12.202, 11.737, 12.214, 12.127, 12.120, 12.010, and 12.223 million, with a range of 11.737 to 12.223 million; the two observed July-to-August seasonal changes are mixed at +0.345 and -0.012 million."
    },
    {
      "kind": "text",
      "text": "Inside-view update: the August seasonal sample points up on average, but it is only two years and highly dispersed. July 2026 already rebounded +0.213 million from June, and the establishment-survey transportation and warehousing context was little changed, so I use only 25 percent of the +0.166 million seasonal average rather than a full seasonal add."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: persistence prior = July 2026 first print 12.223 million; historical sample = fetched January-July 2026 first-print levels plus 2024-2025 July-to-August same-row reference class; adjustment components = +0.25*0.166 = +0.042 million August seasonal pull and 0.000 million for current payroll context, giving 12.223 + 0.042 = 12.265 million, rounded to point 12.26. Successive fetched 2026 changes are -0.465, +0.477, -0.087, -0.007, -0.110, and +0.213 million; sample sigma = 0.319 million. The 80% half-width is 1.28*sigma = 1.28*0.319 = 0.408 million, so 12.26 - 0.408 = 11.852 and 12.26 + 0.408 = 12.668, rounded to 11.85 to 12.67."
    },
    {
      "kind": "text",
      "text": "Upside risk: another August seasonal gain like 2024's +0.345 million, combined with sampling noise after July's rebound, would land above the interval. Downside risk: a reversal of July's CPS jump, weak household employment, or logistics-sector weakness would land below the interval; either tail would be outside the interval."
    },
    {
      "kind": "forecast",
      "point": 12.26,
      "ciLow": 11.85,
      "ciHigh": 12.67
    }
  ]
}
