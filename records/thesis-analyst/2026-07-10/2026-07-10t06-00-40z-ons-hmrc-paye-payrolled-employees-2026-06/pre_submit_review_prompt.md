# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.hmrc.paye_payrolled_employees
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-hmrc-paye-payrolled-employees-june-2026"
- country: "UK"
- targetUnit: "millions"
- dataPointId: "ons.hmrc.paye_payrolled_employees.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-22", "start": "2026-07-14"}, "field": "official_release:ons_hmrc:paye:2026-05:payrolled_employees", "releasePolicy": "first_print", "sourceSeriesId": "ons.hmrc.paye_payrolled_employees", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026", "table": "Earnings and employment from Pay As You Earn Real Time Information, UK: June 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-7098e22567178b5a76d97e9c124dd2dfb9868c2750d780f361151cc9bd7ae37e.json"
- targetContentHash: "7098e22567178b5a76d97e9c124dd2dfb9868c2750d780f361151cc9bd7ae37e"
- registeredAtUtc: "2026-07-10T05:58:27Z"
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
cb7f859917563fe10b8e32cc14119af30b209c48308b842f1cf93a6c0595dd24

# Draft forecast response
{"slug":"ons-hmrc-paye-payrolled-employees-june-2026","country":"UK","type":"data","title":"UK PAYE Payrolled Employees, June 2026","question":"What will the ONS/HMRC first-print early estimate of UK seasonally adjusted PAYE payrolled employees be for June 2026, in millions?","unit":"millions","pointEstimate":30.28,"ciLow":30.225,"ciHigh":30.335,"confidence":0.8,"resolutionDate":"2026-07-21","resolutionSource":"ONS/HMRC Earnings and employment from Pay As You Earn Real Time Information, UK","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026","resolutionRule":"Resolve to the first official ONS/HMRC print of seasonally adjusted UK PAYE payrolled employees for June 2026, in millions, using the headline payrolled employees series in the Earnings and employment from Pay As You Earn Real Time Information bulletin/table. Use the first published estimate only, with no later revisions. The registered ledger URL points to the June 2026 bulletin, which ONS has already used for May 2026 data; the official next-release schedule indicates the June 2026 observation should first print on 2026-07-21, so this discrepancy should be preserved for audit rather than silently changing the target.","dataPointId":"ons.hmrc.paye_payrolled_employees.june_2026.first_print","historicalContext":[{"label":"May 2026 early payrolled employees, millions","value":30.3},{"label":"May 2026 month change, millions","value":0.002},{"label":"April 2026 revised month change, millions","value":-0.053},{"label":"March 2026 revised month change, millions","value":-0.028},{"label":"May 2026 annual change, millions","value":-0.119}],"drivers":["May level was broadly flat at 30.3 million","April weakness was revised from -100,000 to -53,000","Annual growth remained negative at -119,000","Early tax-year PAYE flashes have elevated revision and imputation uncertainty","Vacancy and sector signals point to a soft but not collapsing labour market"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/june2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/earningsandemploymentfrompayasyouearnrealtimeinformationuk/may2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/realtimeinformationstatisticsreferencetableseasonallyadjusted","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/earningsandemploymentfrompayasyouearnrealtimeinformationrevisiontriangle"],"runAt":"2026-07-10T06:01:24Z","reasoning":[{"kind":"heading","text":"UK PAYE Payrolled Employees June 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: forecast the ONS/HMRC PAYE RTI seasonally adjusted UK payrolled employees early estimate for June 2026, in millions, first print only. The ledger source URL is the ONS June 2026 bulletin even though that page is already the May 2026 data release; the official next-release date for the dataset is 21 July 2026, so I keep the registered target but flag the URL-period discrepancy."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS June 2026 PAYE RTI bulletin and release header.","result":"Fetched release date 18 June 2026, next release 21 July 2026, May 2026 payrolled employees 30.3 million, May month change +2,000, May annual change -119,000."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS June 2026 PAYE RTI payrolled-employees section and main points.","result":"Fetched April 2026 growth revised from -100,000 to -53,000; May 2026 was +2,000 month on month; May 2026 annual percentage change was -0.4%."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS May 2026 PAYE RTI bulletin for the prior flash and recent reference points.","result":"Fetched April 2026 early estimate 30.2 million, April flash month change -100,000, April annual change -210,000, and March 2026 revised month change -28,000."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS seasonally adjusted dataset and revision triangle pages to verify schedule and source variant.","result":"Fetched seasonally adjusted dataset release date 18 June 2026, next release 21 July 2026, data coverage July 2014 to May 2026, and revision triangle next release 21 July 2026."},{"kind":"text","text":"Variant consistency: all anchors are the same ONS/HMRC PAYE RTI payrolled employees, seasonally adjusted, UK series used in the bulletin figure/table, not non-seasonally adjusted or regional/sector breakdowns."},{"kind":"text","text":"Reference class and base rate: recent month-to-month first/recent print changes around the target are March -28,000, April -53,000 after revision, and May +2,000. The base rate is a soft labour-market drift of roughly -25,000 to -30,000 per month, but May's flat print and April's upward revision argue against extrapolating the April flash shock one-for-one."},{"kind":"math","text":"Prior/update/interval: persistence prior is May 2026 level 30.300 million; historical sample for successive changes is [-0.028, -0.053, 0.002] million from recent ONS prints; adjustment components are level 30.300 plus momentum -0.026 million, softened by May stabilization and early-tax-year upward revision risk to -0.020 million, giving point 30.280 million. For interval, sigma = 0.0275 million from those successive changes; 1.28*sigma = 0.035 million. I widen to 0.055 million, about 1.6x, because ONS states early tax-year flash estimates have greater uncertainty and only about 85% of information is available initially, versus 98% to 99% next month. Final implied bounds: 30.280 - 0.055 = 30.225 and 30.280 + 0.055 = 30.335 million."},{"kind":"text","text":"Upside risk: a continued payrolling rebound after April revisions, especially if administrative and support services strength persists, would land above the interval. Downside risk: renewed job cuts in accommodation, retail, or small employers after wage and employer-cost pressure would land below the interval. Outside the interval would require a June move materially larger than roughly +/-55,000 from the adjusted May base."},{"kind":"forecast","point":30.28,"ciLow":30.225,"ciHigh":30.335}]}
