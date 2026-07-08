# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.dds.initial_disability_receipts
- period: 2027-04
- conditional_on: The 2025 reconciliation law's Medicaid community-engagement compliance deadline takes effect on its statutory schedule, with no federal statutory or regulatory delay announced by 2027-03-31.

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssdi-initial-applications-april-2027-work-req-deadline-holds"
- targetUnit: "thousands"
- conditional: "The 2025 reconciliation law's Medicaid community-engagement compliance deadline takes effect on its statutory schedule, with no federal statutory or regulatory delay announced by 2027-03-31."

# Source hints
- Use the official agency data page and release calendar.
- FRED or sanctioned mirrors may be used only for history, not final resolution.
- Match the agency's published rounding precision.

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
  "type": "conditional",
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
{"slug":"ssdi-initial-applications-april-2027-work-req-deadline-holds","country":"US","type":"conditional","title":"SSDI initial applications, Apr 2027","question":"Social Security Administration State Agency Monthly Workload Data, Field I Receipts (All Initial), SSA month 2027-04, not seasonally adjusted, first print, in thousands, conditional on the 2025 reconciliation law's Medicaid community-engagement compliance deadline taking effect on its statutory schedule with no federal statutory or regulatory delay announced by 2027-03-31","unit":"thousands","pointEstimate":239.4,"ciLow":209.4,"ciHigh":269.4,"confidence":0.8,"resolutionDate":"2027-05-30","resolutionSource":"Social Security Administration State Agency Monthly Workload Data","resolutionSourceUrl":"https://www.ssa.gov/disability/data/SSA-SA-MOWL.csv","resolutionRule":"Resolve to the first official SSA State Agency Monthly Workload Data CSV print for Date Type MO and Formatted Date 2027-04, summing Field I Receipts (All Initial) across all state-agency and federal-component rows if no national row is provided; convert whole claims to thousands and round to one decimal thousand. Use the first replacement file that adds the 2027-04 period; later replacements or retroactive corrections do not change the resolved value. The conditional is satisfied only if no federal statutory or regulatory delay of the Medicaid community-engagement compliance deadline is announced by 2027-03-31.","dataPointId":"ssa.dds.initial_disability_receipts.2027-04.first_print","conditionalOn":"The 2025 reconciliation law's Medicaid community-engagement compliance deadline takes effect on its statutory schedule, with no federal statutory or regulatory delay announced by 2027-03-31.","historicalContext":[{"label":"FY2022 DI claims received, monthly equivalent","value":172.6},{"label":"FY2023 DI claims received, monthly equivalent","value":176},{"label":"FY2024 DI claims received, monthly equivalent","value":188.4},{"label":"FY2024 SSI blind or disabled claims received, monthly equivalent","value":122.4}],"drivers":["official SSA DDS monthly workload Field I first-print resolver","FY2024 disability-claim receipts above FY2022 and FY2023","April 2027 SSA month normally has five Fridays","Medicaid community-engagement deadline could pull some applicants toward disability claims","state-agency workload data are replaced as a whole file, so first-print capture matters"],"sourceContext":["https://www.ssa.gov/disability/data/ssa-sa-mowl.htm","https://www.ssa.gov/disability/data/SSA-SA-MOWL.csv","https://www.ssa.gov/disability/data/SSA_DATES1.csv","https://www.ssa.gov/policy/docs/statcomps/supplement/2025/2f.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2024/2f4-2f6.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2023/2f4-2f6.html"],"runAt":"2026-07-08T21:22:11Z","reasoning":[{"kind":"heading","text":"SSA DDS initial disability receipts, April 2027"},{"kind":"text","text":"Framing and exact resolver: this forecast targets SSA State Agency Monthly Workload Data monthly Field I, Receipts (All Initial), for SSA month 2027-04. The variant is not seasonally adjusted DDS/state-agency initial claims, not OASDI beneficiary stocks, not SSI Monthly Statistics, and not final revised annual claims workloads."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA State Agency Monthly Workload Data documentation and data dictionary.","result":"Fetched official dataset facts: monthly data start in October 2000; the expanded current file has 71 data elements; Field I is Receipts (All Initial); Fields I-M cover All Initial Claims; data are one row per State Code and Date; no summary row is provided; File Version currently has value 2."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA State Agency Monthly Workload Data timing and update-policy documentation.","result":"Fetched timing evidence: SSA counts monthly work in weekly increments, an SSA month normally ends on the last Friday of the month, the Date field maps to SSA time periods, and the dataset is updated with a new time period within 30 days of the close of the prior time period; April 2027's last Friday is 2027-04-30, so the official within-30-days by-date is 2027-05-30."},{"kind":"tool","tool":"official.lookup","call":"Opened Annual Statistical Supplement 2025 Agency Workloads, Table 2.F5 and 2.F6, for latest official claim-volume anchor.","result":"Fetched fiscal year 2024 claims workloads: Disability Insurance claims received total 2,260.6 thousand, worker 2,145.9 thousand, family members and survivors 114.7 thousand; SSI claims received total 1,683.2 thousand, aged 214.1 thousand, blind or disabled 1,469.1 thousand."},{"kind":"tool","tool":"official.lookup","call":"Opened Annual Statistical Supplement 2024 Claims Workloads, Table 2.F5 and 2.F6, for prior-year official anchor.","result":"Fetched fiscal year 2023 claims workloads: Disability Insurance claims received total 2,111.9 thousand, worker 2,000.7 thousand, family members and survivors 111.2 thousand; SSI blind or disabled claims received 1,395.6 thousand."},{"kind":"tool","tool":"official.lookup","call":"Opened Annual Statistical Supplement 2023 Claims Workloads, Table 2.F5 and 2.F6, for older official anchor.","result":"Fetched fiscal year 2022 claims workloads: Disability Insurance claims received total 2,071.7 thousand, worker 1,960.0 thousand, family members and survivors 111.7 thousand; SSI blind or disabled claims received 1,271.9 thousand."},{"kind":"text","text":"Base rate/reference class: the best fetched official-source class available in this run is recent SSA disability-related claims workload volume. DI total claims received rose from 2,071.7 thousand in FY2022 to 2,111.9 thousand in FY2023 and 2,260.6 thousand in FY2024, equal to simple monthly equivalents of 172.6, 176.0, and 188.4 thousand. The DDS Field I resolver is a monthly flow, so I anchor on a five-week April month rather than a calendar-month stock."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanism: level starts from the FY2024 monthly-equivalent DI claims volume because the raw SSA-SA-MOWL.csv was identified as the final resolver but not readable as tabular rows through this environment; momentum is upward across FY2022-FY2024; the one-off calendar effect is that April 2027 normally spans five SSA weekly closes; the conditional Medicaid community-engagement mechanism adds some near-term disability-claim filing pressure as affected adults seek disability status or disability-benefit eligibility routes, but the effect should be modest relative to national claims volume."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2024 DI claims received monthly equivalent 2,260.6/12 = 188.4 thousand; historical sample = fetched FY2022-FY2024 DI monthly equivalents converted to five-week SSA-month analogs using 5/(52/12)=1.1538, giving 199.2, 203.1, and 217.4 thousand; adjustment components = +10.0 thousand for partial continuation of the FY2022-FY2024 upward trend into 2027, +12.0 thousand for the conditional Medicaid community-engagement deadline pull-forward/channeling mechanism, and +0.0 for rounding, giving point 217.4 + 10.0 + 12.0 = 239.4 thousand. Interval method uses the values themselves for this flow series: sigma = 9.6 thousand across the three five-week analogs, so 1.28*sigma = 12.3 thousand. I widen to a 30.0 thousand half-width because the fetched annual DI workload anchors are an imperfect proxy for the exact monthly DDS Field I all-initial resolver and because the conditional policy mechanism could concentrate applications around the deadline; final implied bounds are 239.4 +/- 30.0 = 209.4 to 269.4 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is a larger Medicaid work-requirement response, outreach by advocates, or SSA/DDS intake catch-up that would land above the interval if April 2027 exceeds 269.4 thousand. Downside risk is a federal delay announced by 2027-03-31, weak disability-application response, or administrative bottlenecks shifting filings after April; under the stated condition, the outcome would land below the interval if receipts are under 209.4 thousand. An outside the interval high print would most likely require a broad policy-driven filing surge rather than normal trend."},{"kind":"forecast","point":239.4,"ciLow":209.4,"ciHigh":269.4}]}

# Reviewer critique
{
  "summary": "The draft has a clear target and resolver framing, but it relies on annual DI workload proxies instead of the actual SSA monthly Field I history and gives an insufficiently supported policy adjustment and interval.",
  "requiredFixes": [
    {
      "rubricItem": "model_prior",
      "severity": "blocking",
      "summary": "The prior is built from FY annual DI claims equivalents rather than the target monthly SSA State Agency Monthly Workload Field I series, even though the resolver CSV is cited.",
      "actionRequested": "Use or explicitly tabulate the actual SSA-SA-MOWL Field I monthly history for comparable Aprils and/or five-week SSA months; if the CSV truly cannot be parsed, state that as a limitation and downgrade the model prior rather than treating annual DI totals as the main prior."
    },
    {
      "rubricItem": "interval",
      "severity": "blocking",
      "summary": "The interval is based on only three annual-derived five-week analogs and then widened judgmentally, not on realized monthly target-series volatility.",
      "actionRequested": "Derive the half-width from realized variation in the monthly Field I target series, such as comparable April errors, five-week-month dispersion, or a simple time-series residual distribution; otherwise explicitly label the interval as judgmental and justify the 30k width."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The +12k Medicaid community-engagement adjustment is material but not supported by cited evidence on eligibility-channeling, affected population, or historical policy analogs.",
      "actionRequested": "Add a compact evidentiary bridge for the policy adjustment, or reduce/reframe it as a judgmental scenario-weighted adjustment with stated uncertainty."
    },
    {
      "rubricItem": "tails",
      "severity": "warning",
      "summary": "A federal delay is listed as a downside risk, but the forecast is conditional on no federal statutory or regulatory delay announced by 2027-03-31.",
      "actionRequested": "Remove delay as an outcome tail under the conditional forecast and replace it with conditional-consistent downside scenarios, such as weak take-up, administrative friction, or filings shifted outside April 2027."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolution date is justified as 2027-05-30 from the within-30-days rule, but that may be a deadline rather than the actual first-print date.",
      "actionRequested": "Clarify that 2027-05-30 is the resolution deadline/expected availability date under the SSA update rule, and keep the first replacement file adding 2027-04 as the operative first-print rule."
    }
  ],
  "optionalSuggestions": [
    "Show the implied prior and final bounds in one short final paragraph so the JSON point and interval are easy to audit.",
    "Distinguish DI annual claims from DDS Field I all-initial receipts wherever both are discussed, since they are not necessarily the same measurement surface."
  ]
}

Emit the final JSON object only.
