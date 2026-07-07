# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.productivity.nonfarm_qoq_prelim
- period: 2026-Q2
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-nonfarm-productivity-q2-2026-prelim"
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
0aa86e140aef3aa0d8b1b924bb4cd4a2d4373fe8985d99bf7943901daa01f589

# Draft forecast response
{"slug":"us-nonfarm-productivity-q2-2026-prelim","country":"US","type":"data","title":"US nonfarm productivity Q2 2026 prelim","question":"BLS nonfarm business sector labor productivity, seasonally adjusted percent change from previous quarter at annual rate, 2026 Q2 preliminary first print","unit":"percent_growth","pointEstimate":1.4,"ciLow":-1.3,"ciHigh":4.1,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Productivity and Costs news release, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/prod2.t02.htm","resolutionRule":"Resolve to the first preliminary BLS Productivity and Costs Table 2 value for nonfarm business sector labor productivity, seasonally adjusted percent change from previous quarter at annual rate, for 2026 Q2, as published on August 6, 2026 at 08:30 ET. Use the printed one-decimal percentage value and do not revise for later revised or annual benchmark releases.","dataPointId":"bls.productivity.nonfarm_qoq_prelim.2026-Q2.first_print","historicalContext":[{"label":"2026-Q1 revised nonfarm labor productivity qoq annualized","value":0.3},{"label":"2025-Q4 nonfarm labor productivity qoq annualized","value":1.6},{"label":"2025-Q3 nonfarm labor productivity qoq annualized","value":5.2},{"label":"2025-Q2 nonfarm labor productivity qoq annualized","value":4.2},{"label":"2025-Q1 nonfarm labor productivity qoq annualized","value":-0.9}],"drivers":["Q1 productivity was weak after revision","2025 productivity trend remained solid","June payroll and hours data point to softer labor input growth","No official Q2 output print is available yet","Volatile quarterly productivity warrants a wide 80% interval"],"sourceContext":["https://www.bls.gov/schedule/news_release/prod2.htm","https://www.bls.gov/news.release/prod2.t02.htm","https://data.bls.gov/servlet/SurveyOutputServlet?graph_name=PR_lprbrief&request_action=wh","https://www.bls.gov/news.release/empsit.nr0.htm","https://www.bls.gov/news.release/empsit.t20.htm"],"runAt":"2026-07-07T14:11:49Z","reasoning":[{"kind":"heading","text":"US nonfarm business productivity Q2 2026 preliminary forecast"},{"kind":"text","text":"Framing and exact resolver: the target is BLS Productivity and Costs Table 2, nonfarm business sector labor productivity, seasonally adjusted percent change from previous quarter at an annual rate, 2026 Q2 preliminary first print. The release variant is nonfarm business, not total business, and all productivity anchors below use the same BLS nonfarm business Table 2 or PRS85006093 index variant."},{"kind":"tool","tool":"official.lookup","call":"BLS release calendar lookup for Productivity and Costs 2026 Q2 preliminary","result":"Fetched BLS schedule: Second Quarter 2026 (P) release date is Aug. 06, 2026 at 08:30 AM; Second Quarter 2026 (R) is Sep. 03, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS Productivity and Costs Table 2 current nonfarm business quarterly productivity values","result":"Fetched Table 2 values: 2026 Q1 labor productivity 0.3 r, output 1.0 r, hours worked 0.7; 2025 Q4 productivity 1.6, 2025 Q3 5.2, 2025 Q2 4.2, 2025 Q1 -0.9."},{"kind":"tool","tool":"official.lookup","call":"BLS PRS85006093 nonfarm business labor productivity index history","result":"Fetched PRS85006093 index values: 2026 Q1 119.437 r, 2025 Q4 119.350, 2025 Q3 118.884, 2025 Q2 117.385, 2025 Q1 116.187, 2024 Q4 116.445, 2024 Q3 116.035, 2024 Q2 114.990."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation June 2026 and aggregate weekly hours context","result":"Fetched June 2026 Employment Situation: total nonfarm payroll employment +57,000, unemployment rate 4.2 percent, April payroll revision -31,000 to +148,000, May revision -43,000 to +129,000; Table B-4 total private aggregate weekly hours index Apr 2026 116.6, May 2026 116.7, Jun 2026 116.8, May-to-June change 0.1 percent."},{"kind":"text","text":"Base rate / reference class: recent nonfarm business productivity prints remain volatile around a positive center. The last twelve annualized changes computed from the official PRS85006093 index are 4.07, 5.06, 3.94, 0.23, 3.71, 3.68, 1.42, -0.88, 4.19, 5.21, 1.58, and 0.29 percent, with an average of 2.71 percent; the last eight average 2.40 percent."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the recent-eight PRS85006093 annualized productivity-growth mean of 2.40 from 2024 Q2 through 2026 Q1. Adjustment components: Q1 revised productivity at 0.3 argues -0.5 from the prior, soft June payrolls and low aggregate-hours growth argue +0.2 through the hours denominator, and no official Q2 output print yet argues -0.7 for output uncertainty and weaker hiring signal, giving 2.40 - 0.5 + 0.2 - 0.7 = 1.4. Interval method: use realized dispersion of the eight same-variant annualized values; sigma = 2.11, so 80 percent half-width is roughly 1.28*sigma = 1.28*2.11 = 2.70, rounded to 2.7. Final implied bounds are 1.4 - 2.7 = -1.3 and 1.4 + 2.7 = 4.1."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger-than-expected Q2 output print with flat or falling hours, which would land above the interval if productivity exceeds 4.1. Downside risk is a weak output print combined with understated aggregate hours, which would land below the interval if productivity is below -1.3. An outside the interval outcome is plausible because quarterly productivity has frequent output and hours revisions, but the interval is anchored to the observed same-series dispersion."},{"kind":"forecast","point":1.4,"ciLow":-1.3,"ciHigh":4.1}]}
