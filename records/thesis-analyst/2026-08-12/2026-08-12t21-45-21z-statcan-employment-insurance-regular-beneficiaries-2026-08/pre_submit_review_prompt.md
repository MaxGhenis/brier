# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.employment_insurance.regular_beneficiaries
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-ei-regular-beneficiaries-august-2026"
- country: "CA"
- targetUnit: "thousands"
- dataPointId: "statcan.employment_insurance.regular_beneficiaries.canada.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-10-21", "start": "2026-10-13"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-10-21", "start": "2026-10-13"}, "field": "v64549350", "releasePolicy": "first_print", "sourceSeriesId": "v64549350", "sourceUrl": "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=64549350", "table": "Statistics Canada Table 14-10-0011-01, EI regular beneficiaries, Canada, seasonally adjusted (persons)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-12-344f246b5a7e25a6522342402468dc23cbb2592215d9c743b69b27c43600ffae.json"
- targetContentHash: "344f246b5a7e25a6522342402468dc23cbb2592215d9c743b69b27c43600ffae"
- registrationCommit: "d50ffb7c957ea27fad25c6e0c6fee0aa2471bc84"
- registeredAtUtc: "2026-08-12T21:16:44Z"
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
30bc33181ee409bae1eb5aa3ee7148f0295f7179b9e628537fa8276497e31c8a

# Draft forecast response
{"slug":"canada-ei-regular-beneficiaries-august-2026","country":"CA","type":"data","title":"Canada EI regular beneficiaries, August 2026","question":"Statistics Canada Table 14-10-0011-01, vector v64549350: Employment Insurance regular beneficiaries, Canada, seasonally adjusted, August 2026 reference month, first print, converted from persons to thousands.","unit":"thousands","pointEstimate":537.69,"ciLow":519.76,"ciHigh":555.62,"confidence":0.8,"resolutionDate":"2026-10-21","resolutionSource":"Statistics Canada, Employment Insurance Statistics","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=64549350","resolutionRule":"Resolve to the first Statistics Canada publication for Table 14-10-0011-01, vector v64549350, Canada regular Employment Insurance beneficiaries, seasonally adjusted, August 2026 reference month. Use the first print only, ignore later table revisions, read the published value in persons, multiply by 0.001 to express in thousands, and round to two decimals in thousands. The canonical registered target fixes resolutionDate at 2026-10-21; a fetched StatCan calendar PDF text extract did not expose an Employment Insurance label beside the date row, so this forecast preserves the supplied ledger contract rather than inferring a different day.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.august_2026.first_print","historicalContext":[{"label":"May 2026 regular EI beneficiaries, Canada SA, thousands","value":543.69},{"label":"Apr 2026 regular EI beneficiaries, Canada SA, thousands","value":543.96},{"label":"Mar 2026 regular EI beneficiaries, Canada SA, thousands","value":550.42},{"label":"Feb 2026 regular EI beneficiaries, Canada SA, thousands","value":550.35},{"label":"Jan 2026 regular EI beneficiaries, Canada SA, thousands","value":559.02}],"drivers":["Last-print persistence is 543.69 thousand","Recent EI series momentum has been flat to down since January","July LFS unemployment rate fell to 6.4%","Three-month horizon widens the persistence interval","Ledger date retained despite calendar-label extraction limits"],"sourceContext":["https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods","https://www150.statcan.gc.ca/n1/daily-quotidien/260807/dq260807a-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf","https://app.thesisinstitute.org/specs.json"],"runAt":"2026-08-12T21:45:32Z","reasoning":[{"kind":"heading","text":"Forecast Canada regular Employment Insurance beneficiaries for August 2026"},{"kind":"text","text":"The resolver is Statistics Canada Table 14-10-0011-01, vector v64549350: Canada regular Employment Insurance beneficiaries, seasonally adjusted, first print for August 2026, transformed from persons to thousands by multiplying by 0.001. The registered target supplies slug, unit, dataPointId, sourceBinding, expected window ending 2026-10-21, and first-print policy."},{"kind":"tool","tool":"statcan.wds","call":"POST getDataFromVectorsAndLatestNPeriods with vectorId 64549350 and latestN 24","result":"Fetched official WDS vector v64549350 values in thousands: 2024-06 479.80, 2024-07 489.32, 2024-08 494.67, 2024-09 486.84, 2024-10 489.08, 2024-11 487.51, 2024-12 487.64, 2025-01 489.06, 2025-02 501.49, 2025-03 504.11, 2025-04 526.28, 2025-05 528.00, 2025-06 547.70, 2025-07 555.09, 2025-08 555.27, 2025-09 554.27, 2025-10 561.48, 2025-11 568.72, 2025-12 567.62, 2026-01 559.02, 2026-02 550.35, 2026-03 550.42, 2026-04 543.96, 2026-05 543.69; latest releaseTime entries include 2026-07-23T08:30 for March, April, and May 2026."},{"kind":"tool","tool":"statcan.calendar","call":"Downloaded and extracted Statistics Canada 2026-2027 release-date PDF, plus checked target registration fields","result":"Fetched release-date PDF text with 2026-2027 dates and multiple August 2026 rows including October 21, 2026 August 2026 and October 23, 2026 August 2026; the text extraction did not expose an Employment Insurance label. The target registration contains expectedReleaseWindow start 2026-10-13, end 2026-10-21, dataPointId statcan.employment_insurance.regular_beneficiaries.canada.august_2026.first_print, and sourceSeriesId v64549350, so I retain 2026-10-21 as the canonical ledger resolutionDate while flagging the extraction limitation."},{"kind":"tool","tool":"statcan.daily","call":"Fetched The Daily, Labour Force Survey, July 2026","result":"Fetched current labour-market signal: July 2026 employment increased by 75,000 (+0.4%), employment rate rose 0.1 percentage points to 60.9%, unemployment rate declined 0.1 percentage points to 6.4%, and the unemployment rate had fallen 0.5 percentage points since April."},{"kind":"tool","tool":"thesis.specs","call":"GET https://app.thesisinstitute.org/specs.json and search slug","result":"Fetched app specs endpoint before finalizing; HTTP status was 404 and response length was 11289 bytes, so no published specs entry for canada-ei-regular-beneficiaries-august-2026 was found in that endpoint during this run."},{"kind":"text","text":"Base rate/reference class: the last 24 official WDS values for the exact vector averaged 525.89 thousand, ranged from 479.80 to 568.72 thousand, and the last print was 543.69 thousand for May 2026. For this repeated level series, last-print persistence at 543.69 thousand is the default prior, with recent monthly changes rather than level dispersion used for the interval."},{"kind":"text","text":"Model candidates under thesis_model_candidate_v1: persistence candidate has point 543.69, p10 525.76, p50 543.69, p90 561.62, 80% interval [525.76, 561.62], 90% interval [520.64, 566.74], interval method residual monthly-change sigma over the latest 12 changes scaled by sqrt(3), calibration_n 12, train cutoff 2026-05. A six-month drift candidate would point lower near 531.18, but it overweights the January-May downshift relative to the 12- and 24-month history and lacks direct EI data for June-August."},{"kind":"math","text":"Prior/update/interval: prior = last-print persistence 543.69 thousand from May 2026; historical sample = latest 12 successive WDS monthly changes +19.70, +7.39, +0.18, -1.00, +7.21, +7.24, -1.10, -8.60, -8.67, +0.07, -6.46, -0.27 thousand. Adjustment components = -6.00 thousand for current LFS evidence that unemployment fell to 6.4% in July and was down 0.5 points since April, partly offset by EI administrative lag and the still-elevated 543.69 thousand May level. Point = 543.69 - 6.00 = 537.69 thousand. For the three-unpublished-month horizon, sigma = 8.09 thousand from the latest 12 monthly changes; 80% half-width = 1.28*sigma*sqrt(3) = 1.28*8.09*1.732 = 17.93 thousand, giving 537.69 - 17.93 = 519.76 and 537.69 + 17.93 = 555.62."},{"kind":"text","text":"Counter-consideration: downside risk outside the interval would be continued job-finding gains and falling unemployment causing June-August EI rolls to fall below 519.76 thousand. Upside risk outside the interval would be renewed layoffs, tariff-sensitive sector weakness, or an EI processing/backlog jump pushing the August first print above 555.62 thousand."},{"kind":"forecast","point":537.69,"ciLow":519.76,"ciHigh":555.62}]}
