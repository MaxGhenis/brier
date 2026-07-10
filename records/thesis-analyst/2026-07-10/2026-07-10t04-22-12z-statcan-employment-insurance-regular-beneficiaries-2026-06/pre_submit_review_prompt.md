# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.employment_insurance.regular_beneficiaries
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-ei-regular-beneficiaries-june-2026"
- targetUnit: "thousands"
- dataPointId: "statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "statcan.employment_insurance.regular_beneficiaries", "releasePolicy": "first_print", "sourceSeriesId": "statcan.employment_insurance.regular_beneficiaries", "sourceUrl": "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101", "table": "Statistics Canada Employment Insurance Statistics, Table 14-10-0011-01 and The Daily release for May 2026", "transform": {"factor": 0.001, "operation": "multiply"}}
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
40b1d111df22e4515825e1b2cf8310b350c95c6801eb5e35e8a0ca0dea4d332a

# Draft forecast response
{"slug":"canada-ei-regular-beneficiaries-june-2026","country":"CA","type":"data","title":"Canada EI Regular Beneficiaries, June 2026","question":"What will Statistics Canada first report for Canada regular Employment Insurance beneficiaries, seasonally adjusted, June 2026, in Table 14-10-0011-01?","unit":"thousands","pointEstimate":550.4,"ciLow":539.6,"ciHigh":561.2,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","resolutionRule":"Resolve to the first Statistics Canada print for Canada, regular Employment Insurance beneficiaries, monthly, seasonally adjusted, June 2026, from Table 14-10-0011-01 or the linked The Daily data-availability release. Use the initially published count of persons converted to thousands by multiplying by 0.001 and do not use later revisions or corrections unless the first-print page itself is replaced before resolution capture.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print","historicalContext":[{"label":"2026-04","value":544.44},{"label":"2026-03","value":548},{"label":"2026-02","value":542.11},{"label":"2026-01","value":554.83},{"label":"2025-11 recent peak","value":569}],"drivers":["April level was 544.44 thousand after a small monthly decline","March-to-April change was -3.56 thousand, but March had risen from February","Labour-market softness keeps upward pressure on EI inflows with a lag","Recent beneficiary levels remain below the November 2025 peak of about 569 thousand","First-print target is seasonally adjusted Canada regular benefits only"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260522/dq260522b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260423/dq260423c-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260325/dq260325a-eng.htm","https://www150.statcan.gc.ca/n1/dai-quo/cal3-eng.htm"],"runAt":"2026-07-10T04:22:38Z","reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast is for Statistics Canada Table 14-10-0011-01, Canada geography, regular Employment Insurance beneficiaries, monthly and seasonally adjusted, June 2026 first print, expressed in thousands. The table page identifies Table 14-10-0011-01 as monthly, seasonally adjusted regular-benefit EI beneficiaries by province and territory."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada Table 14-10-0011-01 metadata page for the target series and latest table release status.","result":"Fetched table metadata: Table 14-10-0011-01, monthly frequency, release date 2026-06-18, geography includes Canada, and latest displayed reference range includes 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened The Daily Employment Insurance, April 2026 release for the latest official Canada value before this run.","result":"Fetched Canada regular EI beneficiaries for April 2026: 544,440 persons = 544.44 thousand, monthly change -0.5%, year-over-year change 3.5%; release says May 2026 EI data will be released July 23."},{"kind":"tool","tool":"official.lookup","call":"Opened The Daily Employment Insurance, March 2026 release for recent official history and labour-market context.","result":"Fetched Canada regular EI beneficiaries for March 2026: 548,000 persons = 548.00 thousand, monthly change +0.4%, year-over-year change 8.7%; the text says March rose by 2,300 after February fell by 8,700 and the November 2025 recent peak was 569,000."},{"kind":"tool","tool":"official.lookup","call":"Opened The Daily Employment Insurance, February 2026 and January 2026 releases for additional recent official history.","result":"Fetched February 2026: 542,110 persons = 542.11 thousand, monthly change -1.6%, year-over-year change 8.1%; fetched January 2026: 554,830 persons = 554.83 thousand, monthly change -1.9%, year-over-year change 13.4%."},{"kind":"tool","tool":"official.lookup","call":"Checked Statistics Canada The Daily release schedule surface for the resolution date.","result":"Fetched the official schedule surface current to 2026 with 2026 release dates; for this target contract I use the scheduled June 2026 EI first-print release date 2026-08-20, within the official expected window 2026-08-19 to 2026-08-27."},{"kind":"text","text":"Reference class and base rate: for this seasonally adjusted level series, the most relevant reference class is month-to-month Canada regular EI beneficiary changes in the current 2026 release sequence. The base rate is mild mean reversion around the 540s-to-550s thousand range rather than a return to the November 2025 peak of 569 thousand."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from April 2026 at 544.44 thousand; recent fetched monthly changes used for dispersion are approximately Dec-Jan -11.0, Jan-Feb -8.7, Feb-Mar +2.3, and Mar-Apr -3.6 thousand, giving sigma = 5.9 thousand. I add +3.0 thousand for May and +3.0 thousand for June because labour-market softness should lift regular-benefit caseloads with a lag but recent first-print EI data have not shown a sustained surge. Point = 544.44 + 3.0 + 3.0 = 550.44, rounded to 550.4. A one-step 80% half-width is 1.28*sigma = 1.28*5.9 = 7.6; because this is two monthly transitions from April to June, I widen by sqrt(2) to about 10.8, so the 80% interval is 550.4 +/- 10.8 = 539.6 to 561.2."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: the level is still high versus early 2025 but below the late-2025 peak; momentum is mixed after January-February declines, a March bounce, and an April dip; no new rule change is included beyond the continuing temporary EI measures noted by StatCan; the policy and administrative mechanism mainly affects eligibility and timing rather than a directional shock this month."},{"kind":"text","text":"Counter-considerations: upside risk is a sharper June claims pickup from tariff-sensitive goods, construction, transport, or education-related layoffs, which would land above the interval if the Canada count exceeds 561.2 thousand. Downside risk is faster re-employment or benefit exhaustion after the winter caseload, which would land below the interval if the first print is under 539.6 thousand."},{"kind":"forecast","point":550.4,"ciLow":539.6,"ciHigh":561.2}]}
