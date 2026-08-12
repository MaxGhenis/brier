# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.gdp_by_industry.monthly_growth
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-monthly-gdp-growth-august-2026"
- country: "CA"
- targetUnit: "percent_growth"
- dataPointId: "statcan.gdp_by_industry.monthly_growth.2026_08.first_print"
- expectedReleaseWindow: {"end": "2026-10-30", "start": "2026-10-30"}
- sourceBinding: {"adapter": "statcan-wds", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-10-30", "start": "2026-10-30"}, "field": "v65201210", "releasePolicy": "first_print", "sourceSeriesId": "v65201210", "sourceUrl": "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods", "table": "GDP by industry, Table 36-10-0434-01 (all industries, chained 2017 dollars, SA at annual rates)", "transform": {"factor": 1, "operation": "percent_change_previous_period"}}
- targetRegistrationPath: "records/targets/2026-08-12-778113191d1d7e73b43cd7e74053741e8877f59bae7e55d100ed2fc1206efee3.json"
- targetContentHash: "778113191d1d7e73b43cd7e74053741e8877f59bae7e55d100ed2fc1206efee3"
- registrationCommit: "d50ffb7c957ea27fad25c6e0c6fee0aa2471bc84"
- registeredAtUtc: "2026-08-12T21:16:44Z"
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
fb8d1f61aa476f3ca85bf8d70a25f46ba90d22a4cbd9fb989f0631ec9b2be514

# Draft forecast response
{
  "slug": "canada-monthly-gdp-growth-august-2026",
  "country": "CA",
  "type": "data",
  "title": "Canada monthly GDP growth, August 2026",
  "question": "What will be the first-print month-over-month percent change in Statistics Canada Table 36-10-0434-01, vector v65201210, gross domestic product by industry for all industries, Canada, chained 2017 dollars, seasonally adjusted at annual rates, for August 2026?",
  "unit": "percent_growth",
  "pointEstimate": 0.2,
  "ciLow": -0.2,
  "ciHigh": 0.6,
  "confidence": 0.8,
  "resolutionDate": "2026-10-30",
  "resolutionSource": "Statistics Canada, Gross domestic product by industry",
  "resolutionSourceUrl": "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods",
  "resolutionRule": "Resolve to the first Statistics Canada print for August 2026 using vector v65201210 in Table 36-10-0434-01, all industries, Canada, chained 2017 dollars, seasonally adjusted at annual rates. Compute the month-over-month percent change from the July 2026 and August 2026 levels at that release vintage; retain the computed value without substituting later revisions. Round to one decimal percentage point.",
  "dataPointId": "statcan.gdp_by_industry.monthly_growth.2026_08.first_print",
  "historicalContext": [
    {
      "label": "2026-01 monthly growth from WDS levels",
      "value": -0.045
    },
    {
      "label": "2026-02 monthly growth from WDS levels",
      "value": 0.192
    },
    {
      "label": "2026-03 monthly growth from WDS levels",
      "value": -0.155
    },
    {
      "label": "2026-04 monthly growth from WDS levels",
      "value": 0.582
    },
    {
      "label": "2026-05 monthly growth from WDS levels",
      "value": 0.34
    }
  ],
  "drivers": [
    "rolling-12 mean benchmark beats persistence",
    "May first-print momentum was positive",
    "June advance estimate showed continued growth",
    "three-month-ahead target adds interval width"
  ],
  "sourceContext": [
    "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods",
    "https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/schedule-key_indicators-eng.json",
    "https://www150.statcan.gc.ca/n1/daily-quotidien/260731/dq260731a-eng.htm"
  ],
  "runAt": "2026-08-12T21:39:47Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Canada Monthly GDP Growth, August 2026"
    },
    {
      "kind": "text",
      "text": "The registered target is StatCan vector v65201210 in Table 36-10-0434-01, all industries, chained 2017 dollars, seasonally adjusted at annual rates. The forecasted value is the first-print August 2026 month-over-month percent change computed from the July and August release-vintage levels. The local public ledger target confirms slug canada-monthly-gdp-growth-august-2026, unit percent_growth, dataPointId statcan.gdp_by_industry.monthly_growth.2026_08.first_print, and resolutionDate 2026-10-30. The app specs endpoint returned a Next.js error page rather than JSON in this run, so app-side slug confirmation was not available."
    },
    {
      "kind": "tool",
      "tool": "statcan.schedule",
      "call": "curl -sS 'https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/schedule-key_indicators-eng.json' | sed -n '19578,19586p'",
      "result": "Official StatCan key-indicator schedule excerpt: date=\"2026-10-30 00:00:01\", title=\"Gross domestic product by industry\", description=\"August 2026\"."
    },
    {
      "kind": "tool",
      "tool": "statcan.wds",
      "call": "POST https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods with [{\"vectorId\":65201210,\"latestN\":24}]",
      "result": "Fetched official WDS vector v65201210 levels included 2026-01=2340022, 2026-02=2344507, 2026-03=2340869, 2026-04=2354483, 2026-05=2362482; the latest 24 levels ran from 2024-06=2294051 through 2026-05=2362482."
    },
    {
      "kind": "tool",
      "tool": "local.compute",
      "call": "Compute percent_change_previous_period from fetched WDS levels",
      "result": "Monthly percent changes from fetched WDS levels: 2026-01=-0.045%, 2026-02=0.192%, 2026-03=-0.155%, 2026-04=0.582%, 2026-05=0.340%; full 23-change distribution mean=0.128, sigma_values=0.258, p10=-0.178, p50=0.130, p90=0.520, min=-0.258, max=0.646."
    },
    {
      "kind": "tool",
      "tool": "statcan.daily",
      "call": "curl -sS 'https://www150.statcan.gc.ca/n1/daily-quotidien/260731/dq260731a-eng.htm' | rg -n -i 'May 2026|June 2026|advance|0\\.[0-9]'",
      "result": "The Daily, Gross domestic product by industry, May 2026: real GDP grew 0.3% in May; advance information indicates real GDP increased 0.2% in June 2026; the official June estimate is scheduled for August 28, 2026."
    },
    {
      "kind": "tool",
      "tool": "local.model_candidates",
      "call": "Compute thesis_model_candidate_v1 baseline candidates from the 23 WDS-derived monthly changes",
      "result": "Persistence candidate: point=0.340, p10=-0.18, p50=0.13, p90=0.52, 80%=[-0.18,0.52], 90%=[-0.24,0.61], interval_method=empirical_recent_changes, calibration_n=23, train_cutoff=2026-05, walk_forward_mae=0.340, walk_forward_rmse=0.399. Rolling-12-mean candidate: point=0.139, p10=-0.18, p50=0.13, p90=0.52, 80%=[-0.18,0.52], 90%=[-0.24,0.61], interval_method=empirical_recent_changes, calibration_n=23, train_cutoff=2026-05, walk_forward_mae=0.222, walk_forward_rmse=0.276."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: the 23 recent comparable month-over-month changes computed from the fetched WDS levels have mean 0.128%, median 0.130%, sigma 0.258%, p10 -0.178%, p90 0.520%, and range -0.258% to 0.646%. The rolling-12 mean benchmark point is 0.139%, and it outperformed last-change persistence in walk-forward MAE."
    },
    {
      "kind": "math",
      "text": "Point estimate: select the rolling-12 mean benchmark rather than raw last-print persistence because walk-forward MAE was lower, then update modestly toward the official June advance estimate. Computation: 0.75*0.139 + 0.25*0.200 = 0.154, rounded to the series precision and with recent positive May/June momentum to 0.2%."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior=rolling-12 mean model candidate from 23 WDS-derived monthly changes, historical sample=2024-07 through 2026-05 computed changes, adjustment components=+0.015 percentage point toward the official June advance estimate and recent May/June positive momentum, interval method=realized dispersion widened for a three-month-ahead August target with only May WDS level history and June advance information. For the fetched monthly growth values, sigma = 0.258; 1.28*sigma = 0.330. Widen to 0.4 percentage point half-width for horizon uncertainty: point 0.2 minus/plus 0.4 gives implied bounds [-0.2, 0.6]. This would have covered 9 of the last 10 fetched monthly growth values after rounding."
    },
    {
      "kind": "text",
      "text": "Downside risk / upside risk: the outcome would land below the interval if July-August activity reverses sharply after the May/June gains, especially through resource, manufacturing, or trade-sensitive sectors. It would land above the interval if the May resource-sector strength, construction growth, public-sector activity, and June wholesale/retail/finance gains persist into a broad August acceleration outside the recent reference class."
    },
    {
      "kind": "forecast",
      "point": 0.2,
      "ciLow": -0.2,
      "ciHigh": 0.6
    }
  ]
}
