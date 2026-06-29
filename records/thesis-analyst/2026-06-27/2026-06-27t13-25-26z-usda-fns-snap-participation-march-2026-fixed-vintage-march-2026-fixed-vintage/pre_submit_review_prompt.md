# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review only the draft forecast, the target spec, and public evidence cited in the draft. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usda.fns.snap.participation.march_2026.fixed_vintage
- period: March 2026 fixed vintage
- conditional: null

# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. Tail scenarios are concrete and tied to the target.
7. Point, interval, final forecast step, and JSON fields are coherent.
8. No leakage, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
65a9b2aaaf9d32da76ff3e985bc5cbb113825ce6cc992a3900a3d151a290c26f

# Draft forecast response
{"slug":"usda-fns-snap-participation-march-2026-fixed-vintage","country":"US","type":"data","title":"US SNAP Participation, Mar 2026","question":"USDA Food and Nutrition Service SNAP national Average Participation for March 2026, not seasonally adjusted, first-print fixed vintage","unit":"millions","pointEstimate":41.92,"ciLow":40.95,"ciHigh":42.85,"confidence":0.8,"resolutionDate":"2026-07-10","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first USDA FNS SNAP monthly national Average Participation value published for March 2026 in the FY2026 national monthly SNAP data table. Convert persons to millions and round to three decimals. Use the first official print only; ignore later revisions or refreshed vintages.","dataPointId":"usda.fns.snap.average_participation.2026-03.first_print","historicalContext":[{"label":"FY2025 Mar","value":41.759},{"label":"FY2025 Jun","value":41.812},{"label":"FY2025 Sep","value":41.734},{"label":"FY2025 Nov latest available","value":41.687}],"drivers":["SNAP caseloads have been nearly flat around 41.7 million in recent official monthly prints","Labor-market drift and food-price pressure support a small upward tilt into early 2026","Expanded work-requirement and recertification enforcement risks pull participation lower","March has limited seasonal signal relative to administrative and policy effects","First-print uncertainty is dominated by state reporting lags and later revisions"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://www.fns.usda.gov/data-research/data-release-calendar","https://www.fns.usda.gov/snap/supplemental-nutrition-assistance-program"],"runAt":"2026-06-27T13:26:10Z","reasoning":[{"kind":"heading","text":"Forecast for USDA FNS SNAP March 2026 First-Print Participation"},{"kind":"text","text":"The resolver is the first USDA Food and Nutrition Service publication of national SNAP Average Participation for March 2026. The target is an administrative count, not seasonally adjusted, resolved from the official FNS SNAP data table rather than FRED or news mirrors."},{"kind":"tool","tool":"official.lookup","call":"Checked the USDA FNS SNAP data table page for the national monthly SNAP participation series and latest visible reference class.","result":"Fetched official monthly national Average Participation reference points: FY2025 Mar 41.759 million, FY2025 Jun 41.812 million, FY2025 Sep 41.734 million, and FY2025 Nov 41.687 million."},{"kind":"tool","tool":"official.lookup","call":"Checked the official FNS data release calendar / posting schedule for the March 2026 fixed-vintage availability date.","result":"Fetched the SNAP Program Data posting date for the March 2026 first-print fixed vintage as 2026-07-10, with the schedule entry tied to the monthly SNAP data table refresh."},{"kind":"tool","tool":"official.lookup","call":"Checked USDA FNS SNAP program context for scale and administrative mechanism.","result":"Fetched program context showing SNAP serves about 42 million people nationally and is administered through 50 states plus the District of Columbia, which explains state-reporting lag risk."},{"kind":"text","text":"Base-rate/reference-class anchor: recent official monthly first-print participation is tightly clustered around 41.7 million. A neutral outside-view forecast would therefore start near 41.75 million before adding early-2026 macro and policy adjustments."},{"kind":"text","text":"Level and momentum: the latest official points show little trend, so I keep the level close to the recent 41.7 million baseline and do not extrapolate a large increase."},{"kind":"text","text":"Current-release adjustments: mild labor-market and household-budget pressure add about 0.20 million to the baseline, while work-requirement enforcement, churn, and recertification frictions subtract about 0.05 million, yielding a small net upward adjustment."},{"kind":"math","text":"Point calculation: 41.75 million recent baseline + 0.20 million macro/need pressure - 0.03 million policy/churn adjustment = 41.92 million. Interval: recent first-print monthly dispersion is modest, but March 2026 has policy and state-reporting uncertainty, so I use an 80% range of roughly -0.97 to +0.93 million around the point, giving 40.95 to 42.85 million."},{"kind":"text","text":"Counter-consideration: a downside outside-the-interval case would be rapid enforcement of eligibility/work-rule changes or unusually high procedural churn pushing participation below 40.95 million; an upside outside-the-interval case would be a sharper labor-market deterioration or delayed disenrollment pushing participation above 42.85 million."},{"kind":"forecast","point":41.92,"ciLow":40.95,"ciHigh":42.85}]}
