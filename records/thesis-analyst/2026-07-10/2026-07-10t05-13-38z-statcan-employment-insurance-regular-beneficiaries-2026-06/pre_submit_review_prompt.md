# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.employment_insurance.regular_beneficiaries
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-ei-regular-beneficiaries-june-2026"
- country: "CA"
- targetUnit: "thousands"
- dataPointId: "statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "statcan.employment_insurance.regular_beneficiaries", "releasePolicy": "first_print", "sourceSeriesId": "statcan.employment_insurance.regular_beneficiaries", "sourceUrl": "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101", "table": "Statistics Canada Employment Insurance Statistics, Table 14-10-0011-01 and The Daily release for May 2026", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-2071f24c9311aaa43cd5bf3d2af243438c9d0aa1124763f0d51d599364e0d06b.json"
- targetContentHash: "2071f24c9311aaa43cd5bf3d2af243438c9d0aa1124763f0d51d599364e0d06b"
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
df927ddae38bcdc964381ec55f3e297872cc57f56a8439ed2974075a5d015980

# Draft forecast response
{"slug":"canada-ei-regular-beneficiaries-june-2026","country":"CA","type":"data","title":"Canada regular EI beneficiaries, June 2026","question":"What will Statistics Canada first print for Canada regular Employment Insurance beneficiaries, seasonally adjusted, for June 2026, in Table 14-10-0011-01?","unit":"thousands","pointEstimate":535,"ciLow":519,"ciHigh":551,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","resolutionRule":"Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only; ignore later revisions or table corrections unless the first-print rule itself is changed by Statistics Canada before release.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print","historicalContext":[{"label":"2026-04 latest official Table 14-10-0011-01 print","value":544.44},{"label":"2026-03 The Daily print","value":548},{"label":"2026-02 The Daily print","value":542.11},{"label":"2026-05 Labour Force Survey unemployment rate, percent","value":6.6}],"drivers":["April regular EI level was 544.44 thousand after a 0.5% monthly decline","January and February EI declines were only partly reversed in March","May Labour Force Survey showed employment up 88,000 and unemployment down to 6.6%, pointing to lower near-term EI inflow pressure","EI benefits lag labour-market conditions, so the strong May LFS is a downward adjustment for both May and June EI","Temporary EI measures and tariff-sensitive sectors keep upside risk from a sharper claims build"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260522/dq260522b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260423/dq260423c-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf"],"runAt":"2026-07-10T05:15:31Z","reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets Statistics Canada Table 14-10-0011-01, Canada, regular Employment Insurance beneficiaries, monthly, seasonally adjusted, June 2026, first print, converted from persons to thousands. The table page identifies Table 14-10-0011-01, monthly frequency, Canada/province geography, and release date 2026-06-18 for the latest available table update."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada Table 14-10-0011-01 and the April 2026 The Daily Employment Insurance release.","result":"Fetched latest same-series values: April 2026 regular EI beneficiaries Canada = 544,440 persons = 544.44 thousand; monthly change = -0.5%; year-over-year change = +3.5%; The Daily states May 2026 EI data will be released 2026-07-23."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily Employment Insurance, March 2026.","result":"Fetched March 2026 regular EI beneficiaries Canada = 548,000 persons = 548.0 thousand; monthly change = +0.4%; year-over-year change = +8.7%; text says March increased by 2,300 after a February decline of 8,700 and remained below the November 2025 peak of 569,000."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily Employment Insurance, February 2026.","result":"Fetched February 2026 regular EI beneficiaries Canada = 542,110 persons = 542.11 thousand; monthly change = -1.6%; year-over-year change = +8.1%; text says February declined by 8,700 after a January decline of 17,000."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada Labour Force Survey, May 2026, as a public leading labour-market indicator for EI inflows.","result":"Fetched May 2026 Canada employment = 21,122,000; employment monthly change = +0.4%; unemployment rate = 6.6%; unemployment rate monthly change = -0.3 percentage points; highlights say employment increased by 88,000 in May after a net decline of 112,000 over January-April 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada release schedule material for 2026-2027 and checked the target release window against the official calendar context and the latest EI release notice.","result":"Fetched official schedule context with 2026 dates including July 23, 2026 for May-reference releases on the same schedule page and the EI April release's numeric next-release statement: May 2026 EI data release date = 2026-07-23; I use 2026-08-20 for the June 2026 first-print resolution within the registered 2026-08-19 to 2026-08-27 release window."},{"kind":"text","text":"Reference class and base rate: for a two-month-ahead level forecast of a seasonally adjusted EI beneficiary count, the base rate is persistence from the latest available level with recent official monthly changes. Same-variant anchors are all Canada regular EI beneficiaries, seasonally adjusted, from the same Statistics Canada EI series, not gross claims, LFS unemployment, or unadjusted counts."},{"kind":"math","text":"Prior/update/interval: persistence prior starts at April 2026 = 544.44 thousand. Recent official EI changes used for dispersion are January -17.0 thousand, February -8.7 thousand, March +2.3 thousand, and April about -2.7 thousand from -0.5% of roughly 547.2 thousand; mean change = -6.5 thousand and sample sigma = 8.3 thousand. Base two-month persistence would be about 544.4 - 2*6.5 = 531.4 thousand; I adjust +3.6 thousand because the March/April levels stabilized and EI can lag the strong May LFS improvement, giving point = 535.0 thousand. The one-month 80% half-width is 1.28*sigma = 1.28*8.3 = 10.6 thousand; because June is two unpublished EI months beyond April, I widen to about 16.0 thousand, within 1.5x the one-month half-width, so interval = 535.0 +/- 16.0 = [519.0, 551.0]."},{"kind":"text","text":"Upside risk: tariff-sensitive layoffs, administrative backlogs, or slower exits from regular benefits would land above the interval if May and June together add more than about 6.6 thousand from April rather than falling. Downside risk: a broad job-finding improvement after the May LFS rebound would land below the interval if regular beneficiaries fall more than 25.4 thousand from April by June. Outside the interval would be most plausible if the May LFS employment gain carries directly into EI exits or if a sudden sectoral shock reverses it before the June EI reference week."},{"kind":"forecast","point":535,"ciLow":519,"ciHigh":551}]}
