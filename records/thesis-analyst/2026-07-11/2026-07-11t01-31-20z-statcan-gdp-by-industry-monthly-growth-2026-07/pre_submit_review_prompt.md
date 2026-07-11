# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.gdp_by_industry.monthly_growth
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-monthly-gdp-growth-july-2026"
- country: "CA"
- targetUnit: "percent_growth"
- dataPointId: "statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-10-02", "start": "2026-09-24"}, "field": "v65201210", "releasePolicy": "first_print", "sourceSeriesId": "v65201210", "sourceUrl": "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=65201210", "table": "Statistics Canada Table 36-10-0434-01, all industries, chained 2017 dollars SA at annual rates; MoM percent change computed from levels at the release vintage", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-53b3ddc1394061e51a22b42a373fc001da9ea7198bee88023eba70524e8fb945.json"
- targetContentHash: "53b3ddc1394061e51a22b42a373fc001da9ea7198bee88023eba70524e8fb945"
- registrationCommit: "464d182153273b99932d1049c8c2b2039b6a9eba"
- registeredAtUtc: "2026-07-11T01:30:29Z"
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
2793079140bafe12a8f16359bf588dbbb331b1e910724217e21ee487fa47b534

# Draft forecast response
{"slug":"canada-monthly-gdp-growth-july-2026","country":"CA","type":"data","title":"Canada monthly GDP growth, July 2026","question":"What will Statistics Canada first report for the July 2026 month-over-month percent change in real GDP by industry at basic prices, all industries, chained 2017 dollars, seasonally adjusted at annual rates?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.26,"ciHigh":0.46,"confidence":0.8,"resolutionDate":"2026-09-29","resolutionSource":"Statistics Canada Table 36-10-0434-01","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=65201210","resolutionRule":"Resolve to the first Statistics Canada print for July 2026 using vector v65201210 in Table 36-10-0434-01, all industries, chained 2017 dollars, seasonally adjusted at annual rates. Compute the month-over-month percent change from the June and July levels at that release vintage; retain the computed value without substituting later revisions.","dataPointId":"statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-07.first_print","historicalContext":[{"label":"2025-07 MoM","value":0.6},{"label":"2025-08 MoM","value":-0.1},{"label":"2025-09 MoM","value":0.2},{"label":"2025-10 MoM","value":-0.3},{"label":"2025-11 MoM","value":0},{"label":"2025-12 MoM","value":0.2},{"label":"2026-01 MoM","value":0},{"label":"2026-02 MoM","value":0.2},{"label":"2026-03 MoM","value":-0.1},{"label":"2026-04 MoM","value":0.5}],"drivers":["recent monthly-growth base rate near 0.1%","services-sector persistence","volatile mining and oil production","manufacturing and trade uncertainty","one-off maintenance and labour disruptions"],"sourceContext":["https://www150.statcan.gc.ca/n1/daily-quotidien/260630/dq260630a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260529/dq260529b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260227/t001b-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=65201210"],"runAt":"2026-07-11T01:31:50Z","reasoning":[{"kind":"heading","text":"Canada real GDP by industry, July 2026 first print"},{"kind":"text","text":"The target is the July 2026 month-over-month change in Statistics Canada vector v65201210, Table 36-10-0434-01: all industries, chained 2017 dollars, seasonally adjusted at annual rates. It resolves from the first release vintage, not a later revision."},{"kind":"tool","tool":"official.lookup","call":"Inspect Statistics Canada's 2026–2027 official release calendar for GDP by industry.","result":"The calendar lists September 29, 2026 as the release date for the July 2026 reference period; it also lists August 28 for June and October 30 for August."},{"kind":"tool","tool":"official.lookup","call":"Inspect Statistics Canada's December 2025 GDP release table for the recent official reference class.","result":"Official all-industries monthly changes for July–December 2025 were 0.6%, -0.1%, 0.2%, -0.3%, 0.0%, and 0.2%, respectively."},{"kind":"tool","tool":"official.lookup","call":"Inspect Statistics Canada's March and April 2026 GDP by industry releases.","result":"The official monthly changes were February +0.2%, March -0.1%, and April +0.5%; the June 30 release also gave a preliminary May advance estimate of +0.1%."},{"kind":"text","text":"The reference class is the ten official monthly observations from July 2025 through April 2026: 0.6, -0.1, 0.2, -0.3, 0.0, 0.2, 0.0, 0.2, -0.1, and 0.5 percent. Their mean is 0.12%, providing the base rate before release-specific adjustments."},{"kind":"text","text":"Level and momentum effects are mildly positive: the April rebound was broad and the preliminary May signal was +0.1%. One-off effects from energy maintenance and labour disruptions can reverse quickly. Policy and trade uncertainty restrain manufacturing, while steady services activity supports growth."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate model; historical sample = the 10 July 2025–April 2026 monthly growth values. Their mean is 0.12%. Adjustments are -0.01 point for fading April energy/reopening strength, -0.02 for manufacturing and trade uncertainty, and +0.01 for services persistence, giving 0.10%. For this change series, dispersion is computed from the values themselves: sample variance = 0.696/9 = 0.0773, so sigma = 0.278%. The normal 80% half-width is 1.28*sigma = 1.28*0.278 = 0.356%, implying 0.10 ± 0.356 = [-0.256%, 0.456%], reported as [-0.26%, 0.46%]."},{"kind":"text","text":"Upside risk comes from a synchronized oil, mining, manufacturing, and services expansion; growth above 0.46% would land outside the interval. Downside risk comes from shutdowns, wildfire or maintenance disruptions, or a sharp trade-related manufacturing contraction; growth below -0.26% would land outside the interval."},{"kind":"forecast","point":0.1,"ciLow":-0.26,"ciHigh":0.46}]}
