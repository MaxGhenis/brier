# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.labour.vacancies_total
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-vacancies-may-jul-2026"
- country: "UK"
- targetUnit: "thousands"
- dataPointId: "ons.labour.vacancies_total.2026_07.first_print"
- expectedReleaseWindow: {"end": "2026-09-15", "start": "2026-09-15"}
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-09-15", "start": "2026-09-15"}, "field": "UK Vacancies (thousands) - Total, seasonally adjusted, value for 2026 JUL", "releasePolicy": "first_print", "sourceSeriesId": "AP2Y", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem", "table": "Claimant count and vacancies time series (UNEM)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-19-2c9ce13c4e282d7375b8e1811bdd814a314e03e873df8ba165e8d9a14efcdcf1.json"
- targetContentHash: "2c9ce13c4e282d7375b8e1811bdd814a314e03e873df8ba165e8d9a14efcdcf1"
- registrationCommit: "1a8c5d83d07cc6160ba5e11d8754092d64a2fc64"
- registeredAtUtc: "2026-08-19T15:37:16Z"
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
885b7743197dc3622119c6ae976181a801a9450287ed5d087ed03c3ac0941031

# Draft forecast response
{"slug":"uk-vacancies-may-jul-2026","country":"UK","type":"data","title":"UK Vacancies, AP2Y, 2026 JUL","question":"What will the Office for National Statistics first print for UK Vacancies (thousands) - Total, seasonally adjusted, series AP2Y, period 2026 JUL?","unit":"thousands","pointEstimate":703,"ciLow":692,"ciHigh":714,"confidence":0.8,"resolutionDate":"2026-09-15","resolutionSource":"Office for National Statistics UK Vacancies (thousands) - Total time series AP2Y","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem","resolutionRule":"Resolve to the first official ONS AP2Y value for period 2026 JUL in the UK Vacancies (thousands) - Total, seasonally adjusted, UNEM time series. Use the integer value in thousands as first published for the 15 September 2026 release; ignore later revisions or corrections unless they replace the first-print page before publication is observable.","dataPointId":"ons.labour.vacancies_total.2026_07.first_print","historicalContext":[{"period":{"type":"month","value":"2025-07"},"label":"2025-07","value":737},{"period":{"type":"month","value":"2025-08"},"label":"2025-08","value":729},{"period":{"type":"month","value":"2025-09"},"label":"2025-09","value":728},{"period":{"type":"month","value":"2025-10"},"label":"2025-10","value":730},{"period":{"type":"month","value":"2025-11"},"label":"2025-11","value":739},{"period":{"type":"month","value":"2025-12"},"label":"2025-12","value":734},{"period":{"type":"month","value":"2026-01"},"label":"2026-01","value":725},{"period":{"type":"month","value":"2026-02"},"label":"2026-02","value":718},{"period":{"type":"month","value":"2026-03"},"label":"2026-03","value":713},{"period":{"type":"month","value":"2026-04"},"label":"2026-04","value":710},{"period":{"type":"month","value":"2026-05"},"label":"2026-05","value":711},{"period":{"type":"month","value":"2026-06"},"label":"2026-06","value":707}],"drivers":["Vacancies broadly flat but still easing","Small-firm labour-cost pressure","Weak PAYE employment backdrop","Three-month average smooths monthly shocks"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/august2026","https://www.gov.uk/government/statistics/announcements/uk-labour-market-september-2026"],"runAt":"2026-08-19T15:41:51Z","reasoning":[{"kind":"heading","text":"ONS AP2Y 2026 JUL Forecast"},{"kind":"text","text":"The resolver is the ONS AP2Y series, UK Vacancies (thousands) - Total, seasonally adjusted, in the UNEM time-series page. The ledger slug says May-Jul 2026, but the ONS AP2Y page currently shows 2026 JUN as the May to July 2026 print, so I keep the target tied to the registered AP2Y 2026 JUL field and note that this appears to be a ledger label discrepancy rather than a change to the target."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS AP2Y time-series page for UK Vacancies (thousands) - Total.","result":"ONS AP2Y was released on 18 August 2026, next release 15 September 2026, and recent monthly values included 2026 JAN 725, 2026 FEB 718, 2026 MAR 713, 2026 APR 710, 2026 MAY 711, and 2026 JUN 707."},{"kind":"tool","tool":"official.lookup","call":"Read the ONS Labour market overview, UK: August 2026 bulletin.","result":"ONS said early estimates for May to July 2026 vacancies decreased by 6,000, or 0.8%, to 707,000, compared with February to April 2026, and had decreased by 11,000 since January to March 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the official September 2026 UK Labour Market announcement.","result":"The GOV.UK official statistics announcement gives UK Labour Market: September 2026 a confirmed release date of 15 September 2026 at 7:00am; the relevant latest AP2Y value checked against that release path is 707 thousand for 2026 JUN."},{"kind":"tool","tool":"official.lookup","call":"Fetched the AP2Y recent reference class from the ONS time-series table.","result":"The 18-print AP2Y sample used for changes was 2025 JAN 793, FEB 775, MAR 759, APR 738, MAY 730, JUN 727, JUL 737, AUG 729, SEP 728, OCT 730, NOV 739, DEC 734, 2026 JAN 725, FEB 718, MAR 713, APR 710, MAY 711, JUN 707."},{"kind":"text","text":"Base rate/reference class: the recent official AP2Y sequence is a low-volatility level series after the 2022 peak, with the last six prints moving 725 to 718 to 713 to 710 to 711 to 707. Persistence from 707 is the starting base rate, then I apply a small negative drift because the ONS bulletin still describes vacancies as decreasing and small firms as constrained by labour costs and operating expenses."},{"kind":"math","text":"Prior/update/interval: persistence prior = 707 from AP2Y 2026 JUN; historical sample = 18 latest official monthly AP2Y prints from 2025 JAN through 2026 JUN; adjustment components = level 707, momentum about -3 to -4 from the latest changes, one-off none, policy-mechanism effect small negative from labour-cost pressure; final point = 707 - 4 = 703. Successive changes in the sample are -18,-16,-21,-8,-3,10,-8,-1,2,9,-5,-9,-7,-5,-3,1,-4, giving sigma = 8.35 thousand. The 80% half-width is about 1.28*sigma = 1.28*8.35 = 10.69 thousand, so rounded bounds are 703 - 11 = 692 and 703 + 11 = 714."},{"kind":"text","text":"Upside risk is a rebound in hiring demand or a favorable survey rotation that would keep AP2Y near or above 715. Downside risk is a sharper hiring freeze from higher labour costs or weakening payroll employment that would land below 692. Outside the interval would likely require a move larger than the recent non-pandemic monthly dispersion, not just another flat three-month average."},{"kind":"forecast","point":703,"ciLow":692,"ciHigh":714}]}
