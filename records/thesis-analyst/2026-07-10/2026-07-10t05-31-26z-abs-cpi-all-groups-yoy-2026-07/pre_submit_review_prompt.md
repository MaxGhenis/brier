# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.cpi.all_groups.yoy
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-july-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530.json"
- targetContentHash: "fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530"
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
302063fcad1c3e7f7835fbb57c0446f934349758c9516a172a8406eb8cbd1f91

# Draft forecast response
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"Australian Bureau of Statistics monthly Consumer Price Index Indicator, All groups CPI annual movement for July 2026, original first print, percent, rounded to one decimal.","unit":"percent","pointEstimate":4.1,"ciLow":3.2,"ciHigh":5,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values unless ABS withdraws the first print before publication. The ledger sourceBinding appears to point to a June 2026 quarterly CPI-style page, but this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and resolves on the monthly July 2026 CPI indicator page.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 all groups annual movement","value":4},{"label":"April 2026 all groups annual movement","value":4.2},{"label":"March 2026 all groups annual movement","value":4.6},{"label":"February 2026 all groups annual movement","value":3.7}],"drivers":["Latest headline monthly CPI was about 4.0 percent in May 2026 after 4.2 percent in April","Trimmed mean near 3.6 percent points to persistent underlying inflation","Fuel excise and petrol effects lower headline temporarily but can reverse by July","Housing and food inflation keep the annual rate above the RBA target band"],"sourceContext":["https://www.abs.gov.au/statistics/release-calendar","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","https://www.theguardian.com/australia-news/2026/jun/24/interest-rate-hikes-remain-on-cards-as-underlying-inflation-climbs-economists-warn"],"runAt":"2026-07-10T05:31:50Z","reasoning":[{"kind":"heading","text":"Australia July 2026 monthly CPI indicator forecast"},{"kind":"text","text":"Framing and exact resolver: the target is the ABS Monthly Consumer Price Index Indicator, All groups CPI annual movement for July 2026, original first print, percent, one-decimal published value. This is the monthly indicator variant, not quarterly CPI, not trimmed mean, and not a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"ABS release-calendar lookup for the July 2026 monthly CPI indicator release date","result":"ABS calendar check for this target window gives the July 2026 Monthly Consumer Price Index Indicator first-print release on 2026-08-26 at the usual 11:30 Australia time slot; the ledger window was 2026-08-25 to 2026-09-02."},{"kind":"tool","tool":"official.lookup","call":"ABS latest monthly CPI indicator all-groups annual movement and components","result":"Fetched latest public release context: May 2026 headline All groups annual CPI was 4.0 percent, April 2026 was 4.2 percent, and the May 2026 trimmed mean annual rate was 3.6 percent."},{"kind":"tool","tool":"official.lookup","call":"ABS recent monthly CPI indicator reference points before April-May","result":"Fetched recent annual headline points for the same monthly all-groups variant: March 2026 was 4.6 percent and February 2026 was 3.7 percent; May 2026 housing was about 6.0 percent annually and food was about 3.3 percent annually."},{"kind":"text","text":"Base rate/reference class: for a one-to-two-month-ahead forecast of a monthly year-over-year inflation rate, the outside-view base rate is recent persistence in the same ABS all-groups annual series. The latest four-point level is centered around 4.1 percent, with a high March reading of 4.6 percent and a May reading of 4.0 percent after temporary fuel relief."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level is still above target because housing and services remain firm; momentum from May is slightly down; the temporary fuel excise and petrol decline depress headline inflation; a partial rebound or base-effect reversal by July argues against projecting May's 4.0 percent mechanically lower."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the same-series recent historical sample Feb-May 2026 at 3.7, 4.6, 4.2, 4.0. Adjustment components are +0.1 pp for possible fuel/base-effect rebound by July and 0.0 pp for underlying inflation persistence because trimmed mean at 3.6 is already below headline but still elevated. Successive changes are +0.9, -0.4, -0.2, so sigma = 0.70 using sample standard deviation of those changes; the 80 percent half-width is roughly 1.28*sigma = 0.90. Point = 4.0 + 0.1 = 4.1, interval = 4.1 +/- 0.9 = [3.2, 5.0]."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed fuel-price or utility-price jump plus sticky rents, which would land above the interval if July prints over 5.0 percent. Downside risk is a larger petrol reversal or broader demand slowdown, which would land below the interval if headline falls under 3.2 percent. An outside the interval result would most likely require a sharp energy or administered-price shock rather than ordinary month-to-month noise."},{"kind":"forecast","point":4.1,"ciLow":3.2,"ciHigh":5}]}
