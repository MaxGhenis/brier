# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.dds.initial_disability_receipts
- period: 2027-04
- conditional_on: A federal statutory or regulatory delay of the 2025 reconciliation law's Medicaid community-engagement compliance deadline is announced on or before 2027-03-31, pushing the effective date beyond April 2027.

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssdi-initial-applications-april-2027-work-req-deadline-delayed"
- targetUnit: "thousands"
- conditional: "A federal statutory or regulatory delay of the 2025 reconciliation law's Medicaid community-engagement compliance deadline is announced on or before 2027-03-31, pushing the effective date beyond April 2027."

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
{"slug":"ssdi-initial-applications-april-2027-work-req-deadline-delayed","country":"US","type":"conditional","title":"SSDI initial applications, Apr 2027, delay branch","question":"Social Security Administration State Agency Monthly Workload Data, Field I Receipts (All Initial), SSA month 2027-04, not seasonally adjusted, first print, in thousands, conditional on a federal statutory or regulatory delay of the 2025 reconciliation law's Medicaid community-engagement compliance deadline being announced on or before 2027-03-31 and pushing the effective date beyond April 2027","unit":"thousands","pointEstimate":227.4,"ciLow":193.4,"ciHigh":261.4,"confidence":0.8,"resolutionDate":"2027-05-30","resolutionSource":"Social Security Administration State Agency Monthly Workload Data","resolutionSourceUrl":"https://www.ssa.gov/disability/data/SSA-SA-MOWL.csv","resolutionRule":"Resolve to the first official SSA State Agency Monthly Workload Data CSV print for Date Type MO and Formatted Date 2027-04, summing Field I Receipts (All Initial) across all state-agency and federal-component rows if no national row is provided; convert whole claims to thousands and round to one decimal thousand. Use the first replacement file that adds the 2027-04 period; later replacements or retroactive corrections do not change the resolved value. The resolutionDate is the official within-30-days availability deadline implied by SSA's update rule after the 2027-04 SSA month closes. The conditional is satisfied only if a federal statutory or regulatory delay of the Medicaid community-engagement compliance deadline is announced by 2027-03-31 and pushes the effective date beyond April 2027.","dataPointId":"ssa.dds.initial_disability_receipts.2027-04.first_print","conditionalOn":"A federal statutory or regulatory delay of the 2025 reconciliation law's Medicaid community-engagement compliance deadline is announced on or before 2027-03-31, pushing the effective date beyond April 2027.","historicalContext":[{"label":"FY2022 DI claims received, monthly equivalent","value":172.6},{"label":"FY2023 DI claims received, monthly equivalent","value":176},{"label":"FY2024 DI claims received, monthly equivalent","value":188.4},{"label":"FY2024 SSI blind or disabled claims received, monthly equivalent","value":122.4}],"drivers":["official SSA DDS monthly workload Field I first-print resolver","FY2024 DI claims received above FY2022 and FY2023","April 2027 SSA month normally ends on Friday 2027-04-30 and is treated as a five-week operating month","delay branch removes the near-deadline Medicaid community-engagement filing-pressure adjustment","annual DI workload anchors are a proxy for exact monthly DDS Field I history","state-agency workload data are replaced as a whole file, so first-print capture matters"],"sourceContext":["https://www.ssa.gov/disability/data/ssa-sa-mowl.htm","https://www.ssa.gov/disability/data/SSA-SA-MOWL.csv","https://www.ssa.gov/disability/data/ssa-dates1.htm","https://www.ssa.gov/policy/docs/statcomps/supplement/2025/2f.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2024/2f4-2f6.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2023/2f4-2f6.html"],"runAt":"2026-07-08T21:28:26Z","reasoning":[{"kind":"heading","text":"SSA DDS initial disability receipts, April 2027 delay branch"},{"kind":"text","text":"Framing and exact resolver: this forecast targets SSA State Agency Monthly Workload Data monthly Field I, Receipts (All Initial), for SSA month 2027-04. The variant is not seasonally adjusted DDS/state-agency initial claims, not OASDI beneficiary stocks, not SSI Monthly Statistics, and not final revised annual claims workloads."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA State Agency Monthly Workload Data documentation and data dictionary.","result":"Fetched official dataset facts: monthly data start in October 2000; the dataset covers 54 state agencies plus federal components; the expanded file has 71 data elements; Field I is Receipts (All Initial); fields I-M cover All Initial Claims; no summary row is provided; File Version currently has value 2."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA workload time-period and update-policy documentation.","result":"Fetched timing evidence: SSA counts work in weekly increments as of Friday close; an SSA month may have 4 or 5 weeks and normally ends on the last Friday of the month; the dataset is updated within 30 days of the close of the prior time period; April 2027's last Friday is 2027-04-30, so the within-30-days availability date is 2027-05-30."},{"kind":"tool","tool":"official.lookup","call":"Opened Annual Statistical Supplement 2025 Agency Workloads, Tables 2.F5 and 2.F6.","result":"Fetched fiscal year 2024 claims workloads: Disability Insurance claims received total 2,260.6 thousand, worker 2,145.9 thousand, family members and survivors 114.7 thousand; SSI claims received total 1,683.2 thousand, aged 214.1 thousand, blind or disabled 1,469.1 thousand."},{"kind":"tool","tool":"official.lookup","call":"Opened Annual Statistical Supplement 2024 Claims Workloads, Tables 2.F5 and 2.F6.","result":"Fetched fiscal year 2023 claims workloads: Disability Insurance claims received total 2,111.9 thousand, worker 2,000.7 thousand, family members and survivors 111.2 thousand; SSI blind or disabled claims received 1,395.6 thousand."},{"kind":"tool","tool":"official.lookup","call":"Opened Annual Statistical Supplement 2023 Claims Workloads, Tables 2.F5 and 2.F6.","result":"Fetched fiscal year 2022 claims workloads: Disability Insurance claims received total 2,071.7 thousand, worker 1,960.0 thousand, family members and survivors 111.7 thousand; SSI blind or disabled claims received 1,271.9 thousand."},{"kind":"text","text":"Base rate/reference class: the best official-source reference class fetched in this run is recent SSA disability-related claims workload volume. DI total claims received rose from 2,071.7 thousand in FY2022 to 2,111.9 thousand in FY2023 and 2,260.6 thousand in FY2024, equal to simple monthly equivalents of 172.6, 176.0, and 188.4 thousand. The DDS Field I resolver is a monthly flow, so I convert the annual base to a five-week SSA-month analog for April."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanism: level starts from the FY2024 DI claims monthly equivalent, because the official SSA-SA-MOWL.csv is the final resolver but this run could not stream its tabular rows through the sandbox. Momentum is upward across FY2022-FY2024; the one-off calendar effect is that April 2027 normally has five Friday workload closes; under this delayed-deadline condition, I remove the filing-pressure adjustment used for the no-delay branch because the Medicaid community-engagement deadline would no longer bind in April 2027."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2024 DI claims received monthly equivalent 2,260.6/12 = 188.4 thousand; historical sample = fetched FY2022-FY2024 DI monthly equivalents converted to five-week SSA-month analogs using 5/(52/12)=1.1538, giving 199.2, 203.1, and 217.4 thousand; adjustment components = +10.0 thousand for partial continuation of the FY2022-FY2024 upward trend into 2027, +0.0 thousand for the delayed Medicaid community-engagement deadline because the April 2027 deadline pressure is absent, and +0.0 for rounding, giving point 217.4 + 10.0 + 0.0 = 227.4 thousand. Interval method uses the values themselves for this flow proxy: sigma = 9.6 thousand across the three five-week analogs, so 1.28*sigma = 12.3 thousand. I widen to a 34.0 thousand half-width, beyond 1.75x, because the fetched annual DI workload anchors are not the exact monthly DDS Field I target and monthly SSA operating flows can vary more than annual averages; final implied bounds are 227.4 +/- 34.0 = 193.4 to 261.4 thousand."},{"kind":"text","text":"Prior run update: the public prior run for the opposite no-delay condition used the same official annual anchors and a +6.0 thousand Medicaid deadline filing-pressure adjustment, producing 233.4 thousand. For this delayed branch I keep the baseline trend but remove that +6.0 thousand policy mechanism, lowering the point to 227.4 thousand and trimming the upper tail."},{"kind":"text","text":"Counter-considerations: upside risk is that disability-claim filing momentum continues independently of the Medicaid deadline, DDS intake backlogs are cleared into April, or outreach tied to the earlier policy debate still boosts applications; that would land above the interval if receipts exceed 261.4 thousand. Downside risk is that delayed work-requirement timing reduces urgency, applications shift outside April, or non-disability eligibility screens prevent referrals to DDS; the result would land below the interval if receipts are under 193.4 thousand. An outside the interval print would most likely reflect exact monthly DDS Field I seasonality that the annual proxy did not capture."},{"kind":"forecast","point":227.4,"ciLow":193.4,"ciHigh":261.4}]}

# Reviewer critique
{"summary":"The draft is close structurally, but it should not be published until the prior and interval are rebuilt from the exact SSA-SA-MOWL Field I monthly history rather than annual DI workload proxies.","requiredFixes":[{"rubricItem":"model_prior","severity":"blocking","summary":"The final resolver is the public SSA-SA-MOWL Field I monthly series, but the forecast rules it out because the run could not stream rows and instead uses annual DI claims received as a proxy.","actionRequested":"Use the exact historical SSA-SA-MOWL Field I monthly receipts series, or document a concrete data-access failure and provide a defensible fallback that maps DI/SSI workload totals to Field I receipts."},{"rubricItem":"base_rate","severity":"warning","summary":"The stated base rate uses DI annual claims only, while Field I Receipts (All Initial) is a DDS workload measure and may include a different mix than DI claims received alone.","actionRequested":"State a base-rate prior from historical Field I April or recent monthly Field I receipts; if retaining the proxy, explain the coverage gap and why SSI/other DDS receipts are not included in the level."},{"rubricItem":"interval","severity":"blocking","summary":"The interval is based on three annual DI proxy values plus judgmental widening, not realized monthly Field I volatility or a clearly calibrated forecast-error distribution.","actionRequested":"Calibrate the 80% interval using realized month-to-month, April-specific, or forecast-horizon residual volatility from the SSA-SA-MOWL Field I history; keep any extra policy uncertainty as an explicit additive component."},{"rubricItem":"update","severity":"warning","summary":"The +10 thousand trend adjustment to 2027 is only loosely justified from FY2022-FY2024 annual DI growth and not checked against more recent monthly Field I behavior.","actionRequested":"Tie the trend update to exact recent Field I observations, or reduce/relabel it as judgmental and explain why annual DI momentum should carry into April 2027 DDS initial receipts."},{"rubricItem":"leakage","severity":"warning","summary":"The reasoning references the opposite no-delay run as a public prior run; this is not outcome leakage, but it risks making the forecast look anchored to another catalog forecast rather than independent evidence.","actionRequested":"Keep the comparison only as a consistency check, and make clear the point estimate is derived from source data and stated adjustments, not from the prior catalog/no-delay forecast."}],"optionalSuggestions":["Clarify whether the cited timing file URL should be SSA_DATES1.csv rather than ssa-dates1.htm.","State that 2027-05-30 is a by-date for availability and that the operative resolution is the first file version containing 2027-04, in case SSA posts earlier.","Make the tail cases quantify what combination of trend, month timing, and policy spillover would push the print below 193.4 or above 261.4."]}

Emit the final JSON object only.
