# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-may-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-05.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-08-15", "start": "2026-08-07"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9.json"
- targetContentHash: "d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9"
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
16748bec7ae5911f2e0bb4471fceff68611bfc0e813667ebcd23a9514cea939b

# Draft forecast response
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"USDA FNS WIC Program total participants for May 2026, national total, not seasonally adjusted, first official print","unit":"millions","pointEstimate":6.96,"ciLow":6.806,"ciHigh":7.114,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the official person count to millions by dividing by 1,000,000 and round to 0.001 million for the cell. Use the first posted value only; ignore later preliminary/final revisions or annual-summary revisions. The ledger binding says transform factor 0.001, but the fetched FNS monthly PDF displays total participants as person counts such as 6,894,610 for May 2025, so the emitted forecast uses the catalog unit millions from person counts.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"latest Nov 2025 initial","value":6.752138},{"label":"Oct 2025 preliminary","value":6.90905},{"label":"May 2025","value":6.89461},{"label":"May 2024","value":6.76371},{"label":"May 2023","value":6.696739}],"drivers":["Recent FNS first-available total fell sharply in November 2025 versus October 2025","May participation has been above the preceding November in the last three fetched fiscal-year histories","FY2025 annual average participation was higher than FY2024 and FY2023","No core FY2026 WIC eligibility or benefit mechanism points to a May 2026 collapse before the FY2027 budget year"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf","https://www.fns.usda.gov/data-research/data-visualization/program-data-release-dates"],"runAt":"2026-07-10T05:04:47Z","reasoning":[{"kind":"heading","text":"USDA FNS WIC total participation, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the USDA FNS WIC national Total Participants series for May 2026, not seasonally adjusted, resolved on the first official print from the WIC monthly program-data tables. The FNS WIC page is the exact series page; the target is a first-print value, so later revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS WIC Data Tables page and identified the monthly national and latest-month WIC data resources.","result":"The FNS WIC page lists Monthly Data - National Level as FY 2022 through November 2025, links FY 2026 preliminary state-level participation, and shows page updated February 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the FNS WIC monthly national PDF for annual and monthly totals through FY2026-to-date.","result":"The monthly national PDF reports FY2025 annual Total Participants 6,866,095, FY2024 6,704,329, FY2023 6,575,977, May 2023 6,696,739, May 2024 6,763,710, May 2025 6,894,610, Oct 2025 6,909,050, and Nov 2025 6,752,138."},{"kind":"tool","tool":"official.lookup","call":"Fetched the FNS latest-month participation PDF to check the first-available/recent-release format.","result":"The latest-month PDF is dated data as of February 13, 2025 and reports TOTAL participation of 6,829,321 for November 2024, 6,909,050 for October 2025 preliminary, and 6,752,138 for November 2025 initial, a -2.3% monthly change and -1.1% year-over-year change."},{"kind":"tool","tool":"official.lookup","call":"Checked the official FNS program-data release calendar for the May 2026 WIC monthly release date.","result":"The FNS program-data release calendar gives the May 2026 WIC monthly program-data release date as 2026-08-14, within the registered expected release window 2026-08-07 to 2026-08-15."},{"kind":"text","text":"Base rate/reference class: for the same WIC total-participation variant, the three fetched May observations were 6.696739 million in 2023, 6.763710 million in 2024, and 6.894610 million in 2025. The three historical November-to-May moves were +0.300006 million from Nov 2022 to May 2023, +0.139673 million from Nov 2023 to May 2024, and +0.065289 million from Nov 2024 to May 2025."},{"kind":"text","text":"Level and momentum: the clean May-to-May trend points upward, with May 2025 above May 2024 by 0.130900 million and May 2024 above May 2023 by 0.066971 million. The latest initial November 2025 level is unusually low relative to October 2025, so I discount a pure Nov 2025 persistence forecast and treat part of the drop as reporting/timing or temporary churn risk rather than a permanent level shift."},{"kind":"text","text":"Policy and mechanism: WIC participation is driven by categorical eligibility, income eligibility, state administration, births/young-child caseload, and take-up. I do not see a May 2026 core-program policy change in the fetched official tables; proposed FY2027 benefit changes would begin after this May target, so they are not a direct level cut for this observation."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the historical Nov-to-May reference class from fetched FNS monthly totals: changes were 0.300006, 0.139673, and 0.065289 million, average = 0.168323, so Nov 2025 initial 6.752138 + 0.168323 = 6.920461 million. May-trend prior uses May 2025 plus average of the two May-to-May gains: 6.894610 + ((0.066971 + 0.130900)/2) = 6.993546 million. I weight these to 6.960 million after a small caution for the weak Nov 2025 first print. Horizon-matched dispersion from those Nov-to-May changes gives sigma = 0.119953 million; 1.28*sigma = 0.1535 million, rounded to 0.154, so the 80% interval is 6.960 - 0.154 = 6.806 and 6.960 + 0.154 = 7.114 million."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound from the depressed November 2025 initial count plus stronger child caseload growth, which would land above the interval if May first print exceeds 7.114 million. Downside risk is a persistent administrative or funding disruption carrying through spring 2026, or a genuine caseload drop rather than a temporary November print, which would land below the interval if May first print is under 6.806 million. Outside the interval would therefore require either a larger-than-historical spring rebound or a continuation of the November 2025 shock."},{"kind":"forecast","point":6.96,"ciLow":6.806,"ciHigh":7.114}]}
