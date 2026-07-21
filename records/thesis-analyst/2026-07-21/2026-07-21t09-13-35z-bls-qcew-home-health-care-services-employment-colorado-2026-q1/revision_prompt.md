# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.qcew.home_health_care_services.employment.colorado
- period: 2026_q1
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "colorado-home-health-employment-2026q1"
- country: "US"
- targetUnit: "count"
- dataPointId: "bls.qcew.home_health_care_services.employment.colorado.2026_q1.first_print"

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Include one public reasoning step beginning "Prior/update/interval:" that names the model or persistence prior, historical sample, adjustment components, interval method, and final implied bounds.
- For strict first-print or original-vintage targets, keep the ledger resolver in substance and do not add same-day correction or release-day grace exceptions unless the target rule includes them.
- Size the 80% interval from realized dispersion and SHOW the arithmetic in the Prior/update/interval step: compute sigma from the fetched history (successive changes for level/rate series; the values themselves for change/flow series), state it literally as "sigma = X", and derive the half-width as roughly 1.28*sigma. If you widen or narrow beyond about 0.75x-1.75x of that half-width, state the regime or mechanism reason in the same step. Never default to a round hedged band.
- When a release has variants (gross vs smoothed/synthetic, SA vs NSA, flash vs final), the resolution rule must name the variant and every anchor and historical value must come from that same variant; say so once in a text step.
- resolutionSourceUrl must be the most specific stable page for the exact series (release page, table, or databrowser query with the series code), never a portal or theme landing page; state the series code or table id in a text step when one exists.
- Name concrete upside, downside, and outside-the-interval scenarios, using the literal phrases "upside risk", "downside risk", and "outside the interval" (or "would land above/below the interval") so the falsification step is machine-checkable.

# Required JSON shape
{
  "slug": "kebab-case-unique-vs-catalog",
  "country": "US|UK|CA|AU|EA|JP",
  "type": "data",
  "title": "Short display title",
  "question": "Exact agency series, period, adjustment, first print",
  "unit": "percent|count|thousands|millions|usd|usd_billions|gbp_billions|ratio|percent_growth",
  "pointEstimate": 0,
  "ciLow": 0,
  "ciHigh": 0,
  "confidence": 0.8,
  "resolutionDate": "YYYY-MM-DD",
  "resolutionSource": "Official agency release",
  "resolutionSourceUrl": "https://official-source.example",
  "resolutionRule": "First-print rule with rounding and revision policy",
  "dataPointId": "agency.dataset.concept.period.first_print",
  "historicalContext": [
    {
      "label": "latest",
      "value": 0
    }
  ],
  "drivers": [
    "short driver phrases"
  ],
  "sourceContext": [
    "https://urls-actually-used"
  ],
  "runAt": "date -u +%Y-%m-%dT%H:%M:%SZ",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Forecast title"
    },
    {
      "kind": "text",
      "text": "Framing and exact resolver"
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "source lookup description",
      "result": "fetched numbers"
    },
    {
      "kind": "math",
      "text": "point and 80% interval calculation"
    },
    {
      "kind": "forecast",
      "point": 0,
      "ciLow": 0,
      "ciHigh": 0
    }
  ]
}

# Validation rules
- Use confidence 0.8 exactly.
- ciLow < pointEstimate < ciHigh, except discrete policy-rate targets may put the modal point at an interval edge if needed.
- historicalContext must contain at least 3 numeric fetched points.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode fast)


# Pre-submit review loop

You already drafted the response below. A reviewer then checked the draft against the Thesis rubric. Produce the final JSON forecast now.

Rules for the final submission:
- Return exactly one JSON object and no Markdown.
- Use only pre-resolution public evidence available to the draft.
- Accept reviewer fixes only when they improve resolver clarity, source grounding, base-rate discipline, uncertainty calibration, or internal coherence.
- Add a public reasoning text step beginning with "Review disposition:" that states which critique items were accepted or rejected. Keep this concise; do not reveal hidden chain-of-thought.
- Put the Review disposition text step before the final forecast step.
- The final reasoning step must be the forecast step, and its numbers must exactly match pointEstimate, ciLow, and ciHigh.

# Draft forecast response
{"slug":"colorado-home-health-employment-2026q1","country":"US","type":"data","title":"Colorado Home Health Employment, 2026 Q1","question":"U.S. Bureau of Labor Statistics QCEW Colorado private ownership NAICS 621610 Home Health Care Services not seasonally adjusted quarterly average monthly employment for 2026 Q1, first print.","unit":"count","pointEstimate":29600,"ciLow":28400,"ciHigh":30800,"confidence":0.8,"resolutionDate":"2026-08-28","resolutionSource":"U.S. Bureau of Labor Statistics Quarterly Census of Employment and Wages, NAICS-based quarterly CSV industry slice","resolutionSourceUrl":"https://data.bls.gov/cew/data/api/2026/1/industry/621610.csv","resolutionRule":"Resolve to the Colorado statewide private-ownership NAICS 621610 Home Health Care Services row in the first public BLS QCEW 2026 Q1 quarterly CSV industry slice, using area_fips=08000, own_code=5, industry_code=621610, size_code=0. Compute quarterly average monthly employment as round((month1_emplvl + month2_emplvl + month3_emplvl) / 3) to the nearest whole count. Use the first print released with the 2026 Q1 QCEW full data update and ignore later revisions.","dataPointId":"bls.qcew.home_health_care_services.employment.colorado.2026_q1.first_print","historicalContext":[{"label":"2024-04 Colorado private NAICS 621610 employment","value":26626},{"label":"2024-05 Colorado private NAICS 621610 employment","value":26845},{"label":"2024-06 Colorado private NAICS 621610 employment","value":26683},{"label":"2024-07 Colorado private NAICS 621610 employment","value":27176},{"label":"2024-08 Colorado private NAICS 621610 employment","value":27419}],"drivers":["Aging-in-place demand supports continued home health hiring","Colorado 2024 monthly QCEW readings rose from 25927 in January to 27419 in August","National NAICS 621610 employment rose from 1820.6 thousand in 2024 to 1911.4 thousand in 2025","Medicaid and Medicare payment constraints limit an unlimited hiring acceleration","Small state-industry cell creates disclosure, reclassification, and month-to-month volatility risk"],"sourceContext":["https://www.bls.gov/cew/release-calendar.htm","https://www.bls.gov/cew/additional-resources/open-data/csv-data-slices.htm","https://data.bls.gov/cew/data/api/2026/1/industry/621610.csv","https://beautifydata.com/economics/united-states/qcew-employment/by-industry/private/naics-621610-home-health-care-services/by-state-per-month/2024/july","https://beautifydata.com/economics/united-states/qcew-employment/by-industry/private/naics-621610-home-health-care-services/by-state-per-month/2024/august","https://fred.stlouisfed.org/series/IPURN621610W200000000"],"runAt":"2026-07-21T09:13:51Z","reasoning":[{"kind":"heading","text":"Forecast for Colorado QCEW Home Health Employment, 2026 Q1"},{"kind":"text","text":"Framing and exact resolver: the target is the BLS QCEW first-print 2026 Q1 Colorado statewide private-ownership NAICS 621610 Home Health Care Services employment count. Because QCEW quarterly files provide month1_emplvl, month2_emplvl, and month3_emplvl rather than a single quarterly employment field, I resolve the quarterly target as the rounded average of January, February, and March 2026 employment in the same row."},{"kind":"tool","tool":"official.lookup","call":"Inspect BLS QCEW release calendar for the 2026 Q1 County Employment and Wages release date.","result":"Fetched BLS QCEW calendar: 1st Quarter 2026 release date is Friday, Aug. 28, 2026 at 10:00 AM; 2nd Quarter 2026 is Wednesday, Dec. 2, 2026 at 10:00 AM; 4th Quarter 2025 was Tuesday, June 2, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"Inspect BLS QCEW Open Data CSV slice documentation for row and field mechanics.","result":"Fetched BLS CSV layout: area_fips is field 1, own_code field 2, industry_code field 3, size_code field 5, qtr field 7, qtrly_estabs field 9, month1_emplvl field 10, month2_emplvl field 11, and month3_emplvl field 12."},{"kind":"tool","tool":"public.lookup","call":"Inspect indexed BLS QCEW-derived state-by-month data for Colorado private NAICS 621610 in 2024.","result":"Fetched Colorado private payroll employment for NAICS 621610: January 2024 25927, April 2024 26626, May 2024 26845, June 2024 26683, July 2024 27176, and August 2024 27419."},{"kind":"tool","tool":"public.lookup","call":"Inspect FRED mirror of BLS national NAICS 621610 employment as a broad outside-view growth check.","result":"Fetched national Home Health Care Services employment from BLS/FRED: 2021 1585.0 thousand, 2022 1605.7 thousand, 2023 1686.3 thousand, 2024 1820.6 thousand, and 2025 1911.4 thousand."},{"kind":"text","text":"Base rate/reference class: the same-industry national series grew 90.8 thousand from 2024 to 2025, which is 90.8 / 1820.6 = 5.0 percent. Colorado's observed 2024 same-series monthly path rose 1492 jobs from January to August, or 5.8 percent over seven months, so a continued gain into early 2026 is more likely than a flat or declining print, but I temper the state pace toward the national base rate."},{"kind":"text","text":"Variant discipline: all anchors for the state path are not seasonally adjusted private payroll employment in NAICS 621610, matching the own_code=5 and industry_code=621610 resolver. The national FRED series is only an outside-view growth check and is not the resolution source."},{"kind":"math","text":"Prior/update/interval: persistence prior is the latest fetched Colorado level, August 2024 = 27419, with a national reference-class trend of +5.0 percent per year from 2024 to 2025 and a Colorado short-run signal of +5.8 percent from January to August 2024. I project roughly 5.1 percent annual growth from August 2024 to the 2026 Q1 average, so 27419 * (1.051^1.6) = about 29650, rounded to point 29600. Historical sample for dispersion uses successive fetched Colorado monthly changes: 26845 - 26626 = 219, 26683 - 26845 = -162, 27176 - 26683 = 493, and 27419 - 27176 = 243; sigma = sqrt((219^2 + 162^2 + 493^2 + 243^2) / 4) = 306.6 monthly jobs. Scaling across about five quarters gives sigma = 306.6 * sqrt(5) = 685.6, and the 80% half-width is roughly 1.28*sigma = 1.28*685.6 = 877.6. I widen to 1200 jobs, about 1.37x that half-width, for state-industry disclosure/reclassification and reimbursement-policy risk, giving 29600 - 1200 = 28400 and 29600 + 1200 = 30800."},{"kind":"text","text":"Level, momentum, one-off, and mechanism: level is near the upper-20-thousands based on the 2024 Colorado QCEW readings. Momentum is positive from aging-in-place demand and national industry expansion. One-off effects from Colorado Medicaid home-health rules and the new 2025 care-worker credit could support staffing, but payment-rate pressure and agency margin constraints keep the point below an extrapolation of the fastest 2024 Colorado months."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger agency hiring response to home- and community-based care demand or payer-rate support, which would land above the interval if Q1 2026 average employment exceeds 30800. Downside risk is reimbursement pressure, worker shortages, provider consolidation, or industry-code reclassification, which would land below the interval if the first print is under 28400. An outside the interval result would most likely come from a state-specific policy shock, a large employer recoding, or a disclosure/reclassification event rather than ordinary trend noise."},{"kind":"forecast","point":29600,"ciLow":28400,"ciHigh":30800}]}

# Reviewer critique
{"summary":"Draft is close on resolver mechanics but needs stronger use of available same-series history and a defensible interval before publication.","requiredFixes":[{"rubricItem":"update","severity":"blocking","summary":"The forecast relies on Colorado observations only through August 2024 even though later same-series QCEW Colorado data should be available before the 2026-07-21 run date.","actionRequested":"Use the latest available official BLS/QCEW Colorado private NAICS 621610 observations before the run date, or explicitly state that they were unavailable and why; revise the prior/update accordingly."},{"rubricItem":"model_prior","severity":"warning","summary":"The time-series prior is a latest-level plus growth extrapolation, but it does not compare against a same-state year-over-year or quarterly-average persistence model.","actionRequested":"Add a compact time-series prior such as latest available quarterly average, same-quarter seasonal persistence, or YoY growth from official Colorado QCEW; if rejecting it, explain why."},{"rubricItem":"interval","severity":"blocking","summary":"The 80% interval is based on only four within-2024 monthly changes and a sqrt(5) scaling that is not clearly tied to realized forecast-horizon volatility for a 2026 Q1 quarterly average.","actionRequested":"Re-estimate interval width from a larger historical sample of same-series monthly/quarterly changes or forecast errors, or explicitly justify the uncertainty model and horizon scaling."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The Prior/update/interval step is present but the historical sample is too narrow and the adjustment components are not separated from the trend calculation.","actionRequested":"Rewrite the compact step to name the baseline prior, latest official Colorado sample, trend/inside-view adjustments in count or percent terms, interval method, and final implied 80% bounds."},{"rubricItem":"resolver","severity":"warning","summary":"The resolver correctly names BLS QCEW, first print, row filters, unit, and 2026-08-28 release date, but the live CSV URL could later reflect a revised/final file unless the first-print capture rule is explicit operationally.","actionRequested":"Clarify that the resolving value is the CSV value captured from the first public 2026 Q1 full data update on 2026-08-28, with later file changes ignored."}],"optionalSuggestions":["Prefer official BLS/QCEW data for historical Colorado inputs; third-party mirrors can be cited only as convenience checks.","Make the tail scenarios more numeric by tying upside/downside examples to approximate growth rates or employer recoding magnitudes."]}

Emit the final JSON object only.
