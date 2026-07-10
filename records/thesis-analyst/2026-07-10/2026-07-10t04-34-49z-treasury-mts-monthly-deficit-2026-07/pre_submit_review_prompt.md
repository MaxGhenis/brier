# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: treasury.mts.monthly_deficit
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-mts-deficit-july-2026"
- targetUnit: "usd_billions"
- dataPointId: "treasury.mts.monthly_deficit.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["fiscaldata.treasury.gov"], "expectedReleaseWindow": {"end": "2026-08-17", "start": "2026-08-09"}, "field": "treasury.mts.monthly_deficit", "releasePolicy": "first_print", "sourceSeriesId": "treasury.mts.monthly_deficit", "sourceUrl": "https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/", "table": "U.S. Department of the Treasury, Monthly Treasury Statement (Table 1)", "transform": {"factor": 1.0, "operation": "multiply"}}
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
e4a0c8cce31b16066b1fc04eae771728d8e8c3406e4cf7dfebd8dd39dada2670

# Draft forecast response
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. July 2026 MTS Deficit","question":"U.S. Department of the Treasury Monthly Treasury Statement Table 1 current-month deficit for July 2026, first print, not seasonally adjusted, in billions of nominal dollars.","unit":"usd_billions","pointEstimate":320,"ciLow":267,"ciHigh":373,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","resolutionRule":"Resolve to the first-print July 2026 current-month Surplus or Deficit (-) entry in U.S. Treasury Monthly Treasury Statement Table 1. Report deficits as positive usd_billions, rounded to the nearest 1 billion. Do not use later revisions or fiscal-year-to-date amounts.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"2025-07 first print deficit","value":291},{"label":"2024-07 first print deficit","value":244},{"label":"2023-07 first print deficit","value":221},{"label":"2022-07 first print deficit","value":211},{"label":"2021-07 first print deficit","value":302}],"drivers":["July deficits have recently clustered in the low-to-high $200 billions","Rising net interest and benefit outlays lift the 2026 level","Tariff/customs revenue offsets part of the widening","First-print Table 1 current-month balance can move sharply with calendar timing"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://apnews.com/article/us-budget-deficit-trump-tariffs-treasury-992949ccc115fddbf3838a6213cf2c94"],"runAt":"2026-07-10T04:34:56Z","reasoning":[{"kind":"heading","text":"Forecast July 2026 U.S. Monthly Treasury Statement Deficit"},{"kind":"text","text":"Framing and exact resolver: this targets the U.S. Treasury Monthly Treasury Statement Table 1 current-month Surplus or Deficit (-) for July 2026, first print only, not the fiscal-year-to-date deficit. I treat the Table 1 deficit sign convention as a reporting convention and express the forecast as a positive deficit in usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Checked the Fiscal Data Monthly Treasury Statement Table 1 target page and release-calendar context for the July 2026 statement.","result":"The ledger expected release window is 2026-08-09 to 2026-08-17, and the scheduled first-print date used here is 2026-08-12; the prior July 2025 statement was released on 2025-08-12."},{"kind":"text","text":"Variant control: every historical anchor below is the same non-seasonally-adjusted MTS Table 1 current-month deficit concept, not receipts, outlays, refunds, or fiscal-year-to-date balance."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent July current-month deficit reference class from Treasury MTS Table 1 history.","result":"July deficits used: 2021 = 302, 2022 = 211, 2023 = 221, 2024 = 244, 2025 = 291, all in usd_billions as positive deficit amounts."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest available July 2025 release report and public Treasury-linked coverage for current-policy mechanisms.","result":"July 2025 deficit was about 291 versus 244 in July 2024, a 20% year-over-year increase; customs revenue in July 2025 rose 273%, or 21 billion, from a year earlier."},{"kind":"text","text":"Base rate/reference class: the outside-view base rate is the recent July MTS distribution, with 2021-2025 values of 302, 211, 221, 244, and 291; the five-year mean is 253.8 and the median is 244, but the latest two years point to a higher post-2024 level."},{"kind":"math","text":"Prior/update/interval: persistence prior is July 2025 = 291 from the same first-print Table 1 monthly-deficit variant; adjustment components are +24 for rising benefit, interest, and appropriated outlays, +11 for policy-driven deficit pressure, and -6 for tariff/customs revenue offset, giving 291 + 24 + 11 - 6 = 320. For the 80% interval, use the realized dispersion of July flow values themselves: sample values 302, 211, 221, 244, 291 have sigma = 41.0, so half-width is roughly 1.28*sigma = 52.5; rounding to whole billions gives 320 - 53 = 267 and 320 + 53 = 373."},{"kind":"text","text":"Counter-considerations: upside risk is a larger deficit if July benefit payments, defense/homeland spending, or net interest run hotter than expected; downside risk is stronger-than-expected tariff and income-tax collections or calendar timing that shifts payments out of July; a deficit below 267 or above 373 would land outside the interval."},{"kind":"forecast","point":320,"ciLow":267,"ciHigh":373}]}
