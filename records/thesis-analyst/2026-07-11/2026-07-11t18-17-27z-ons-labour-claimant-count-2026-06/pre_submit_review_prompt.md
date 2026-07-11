# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.labour.claimant_count
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-claimant-count-june-2026"
- country: "UK"
- targetUnit: "thousands"
- dataPointId: "ons.labour.claimant_count.2026_06.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/claimantcountandvacanciesdataset"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-14", "start": "2026-07-14"}, "field": "People claiming unemployment related benefits: United Kingdom: all aged 16+: seasonally adjusted", "releasePolicy": "first_print", "sourceSeriesId": "CLA01/BCJD", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/claimantcountandvacanciesdataset", "table": "CLA01: Claimant Count and Vacancies", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-f35bec853a4c4fc4fe2a96f113938b208bd62e270f3c2c5268aa82dc7aab89e4.json"
- targetContentHash: "f35bec853a4c4fc4fe2a96f113938b208bd62e270f3c2c5268aa82dc7aab89e4"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"
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
8431c043aa964efe43e74215e2ffeb22cdb2509e3d77faeea1fa3595e2197492

# Draft forecast response
{"slug":"uk-claimant-count-june-2026","country":"UK","type":"data","title":"UK claimant count, June 2026","question":"What will ONS first report for the UK Claimant Count, people aged 16+, seasonally adjusted, in June 2026?","unit":"thousands","pointEstimate":1725,"ciLow":1709.1,"ciHigh":1740.9,"confidence":0.8,"resolutionDate":"2026-07-14","resolutionSource":"Office for National Statistics, CLA01: Claimant Count and Vacancies","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/claimantcountandvacanciesdataset","resolutionRule":"Resolve to the first value published by ONS for June 2026 for series BCJD, People claiming unemployment-related benefits: United Kingdom: all aged 16+: seasonally adjusted, expressed in thousands and recorded to one decimal place. Ignore subsequent revisions. The registered target specifies 14 July 2026, although the ONS release calendar inspected during this run schedules UK Labour Market: July 2026 for 21 July 2026 at 7:00am; this forecast retains the registered resolutionDate rather than silently altering the target.","dataPointId":"ons.labour.claimant_count.2026_06.first_print","historicalContext":[{"label":"January 2026","value":1650.3},{"label":"February 2026","value":1667.4},{"label":"March 2026","value":1672.4},{"label":"April 2026","value":1680.6},{"label":"May 2026","value":1711.9}],"drivers":["Recent claimant-count acceleration","Weak vacancy demand","Flat payroll employment","Administrative-record volatility"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/timeseries/bcjd/unem","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/june2026/pdf","https://www.ons.gov.uk/releases/uklabourmarketjuly2026"],"runAt":"2026-07-11T18:17:58Z","reasoning":[{"kind":"heading","text":"UK claimant count, June 2026 first print"},{"kind":"text","text":"The resolver is ONS series BCJD in table CLA01: UK people, seasonally adjusted, thousands. The target is the June 2026 first print, so later administrative revisions do not count."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest observations from the ONS BCJD time-series page.","result":"ONS BCJD reports January 2026 1650.3, February 1667.4, March 1672.4, April 1680.6, and May 1711.9 thousand."},{"kind":"tool","tool":"official.lookup","call":"Fetched the pre-release labour-market summary from the ONS June 2026 bulletin.","result":"ONS described May 2026 claimant count as 1.712 million; February-April unemployment was 4.9%, and March-May vacancies fell by 19,000 to 707,000."},{"kind":"tool","tool":"official.lookup","call":"Checked the official ONS release page and dataset schedule.","result":"The ONS July 2026 labour-market page schedules release for 21 July 2026 at 7:00am, while the registered ledger date is 14 July 2026; the latest dataset release was 18 June 2026 and its next release is 21 July 2026."},{"kind":"text","text":"The recent reference class is the 16 monthly BCJD changes from January 2025 through May 2026: 0.3, -1.3, -11.5, -2.7, -5.0, -26.5, -5.5, -3.7, -1.7, -4.1, -2.5, -0.1, 17.1, 5.0, 8.2, and 31.3 thousand. Its base rate is close to persistence overall, but the last four changes are all positive."},{"kind":"text","text":"Level: May starts at 1711.9 thousand. Momentum: the recent three-month median change is 8.2 thousand. One-off: May's 31.3-thousand jump is unlikely to repeat fully. Policy/mechanism: claimant records can shift as work-capability assessments conclude, while low vacancies and weak payroll growth modestly favor a further rise."},{"kind":"math","text":"Prior/update/interval: The model is a persistence prior at 1711.9 using the 16-change historical sample. Add 8.2 for recent median momentum and 4.9 for weakening labour-demand and administrative-mechanism effects, giving 1711.9 + 8.2 + 4.9 = 1725.0. The sample standard deviation of those successive changes is sigma = 12.4 thousand; the normal 80% half-width is 1.28*sigma = 1.28*12.4 = 15.9, implying 1725.0 - 15.9 = 1709.1 and 1725.0 + 15.9 = 1740.9."},{"kind":"text","text":"Upside risk comes from another May-sized administrative inflow or sharper layoffs and would land above the interval. Downside risk comes from reversal of May's provisional increase or faster completion of work-capability assessments and could land below the interval."},{"kind":"forecast","point":1725,"ciLow":1709.1,"ciHigh":1740.9}]}
