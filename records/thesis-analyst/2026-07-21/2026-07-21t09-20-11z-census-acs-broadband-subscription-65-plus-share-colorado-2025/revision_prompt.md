# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.acs.broadband_subscription_65_plus.share.colorado
- period: 2025
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "colorado-broadband-subscription-65-plus-2025"
- country: "US"
- targetUnit: "percent"
- dataPointId: "census.acs.broadband_subscription_65_plus.share.colorado.2025.first_print"
- resolutionDate: "2026-09-10"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

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
{"slug":"colorado-broadband-subscription-65-plus-2025","country":"US","type":"data","title":"Colorado ACS 65+ Broadband Share, 2025","question":"U.S. Census Bureau American Community Survey 2025 ACS 1-Year Estimates Detailed Table B28005, Colorado, population 65 years and over in households with a computer and a broadband Internet subscription divided by total population 65 years and over in households, first print, percent.","unit":"percent","pointEstimate":87.7,"ciLow":85.3,"ciHigh":90.1,"confidence":0.8,"resolutionDate":"2026-09-10","resolutionSource":"U.S. Census Bureau American Community Survey 1-Year Estimates Detailed Table B28005","resolutionSourceUrl":"https://data.census.gov/table/ACSDT1Y2025.B28005?g=040XX00US08&q=B28005","resolutionRule":"Resolve to 100 * B28005_017E / B28005_014E for geography Colorado in the first public 2025 ACS 1-Year Estimates Detailed Table B28005 print, rounded to one decimal percentage point. Use the original Census first-posted estimate and ignore later revisions or corrections unless Census replaces the first public file before the public release completes.","dataPointId":"census.acs.broadband_subscription_65_plus.share.colorado.2025.first_print","historicalContext":[{"label":"2021 ACS 1-year U.S. B28005 65+ broadband share","value":79.4},{"label":"2022 ACS 1-year U.S. B28005 65+ broadband share","value":81.6},{"label":"2023 ACS 1-year U.S. B28005 65+ broadband share","value":83.5},{"label":"2024 ACS 1-year U.S. B28005 65+ broadband share","value":84.8},{"label":"2024 ACS 1-year California B28005 65+ broadband share","value":91.4},{"label":"2024 ACS 1-year Colorado population","value":5957494},{"label":"2024 ACS 1-year Colorado senior poverty share","value":9.0}],"drivers":["Colorado has higher income and lower poverty than the U.S. average, supporting above-national older-adult broadband adoption","Aging-cohort replacement raises 65+ internet adoption as more-connected cohorts enter age 65","Broadband definition includes cellular data, satellite, fixed wireless, and other non-dial-up service","Adoption gains slow as the remaining offline 65+ population is more selected by age, disability, income, and rurality","Affordable Connectivity Program expiration creates affordability drag for low-income older households","ACS first-print sampling and weighting noise can move a state age subgroup by more than the national series"],"sourceContext":["https://data.census.gov/table/ACSDT1Y2025.B28005?g=040XX00US08&q=B28005","https://api.census.gov/data/2024/acs/acs1/groups/B28005.html","https://data.census.gov/table/ACSDT1Y2024.B28005?q=B28005","https://data.census.gov/table/ACSDT1Y2024.B28005?g=040XX00US06&q=Telephone%2C+Computer%2C+and+Internet+Access","https://censusreporter.org/profiles/04000US08-colorado/","https://www.census.gov/programs-surveys/acs/news/data-releases/2024/release-schedule.html","https://www.census.gov/data/what-is-data-census-gov/upcoming-releases.html"],"runAt":"2026-07-21T09:20:34Z","reasoning":[{"kind":"heading","text":"Forecast for Colorado 2025 ACS 65+ Broadband Subscription Share"},{"kind":"text","text":"Framing and exact resolver: the target is Census ACS Detailed Table B28005, universe population in households, Colorado, 2025 ACS 1-year first print. The numerator is B28005_017E, 65 years and over, has a computer, with a broadband Internet subscription; the denominator is B28005_014E, total 65 years and over. The variant is ACS 1-Year Estimates Detailed Tables, not 5-year, supplemental, PUMS, or later revised tables."},{"kind":"tool","tool":"official.lookup","call":"Inspect Census API variable metadata for 2024 ACS 1-year B28005","result":"Fetched variable definitions: B28005 has 78 variables; B28005_014E is total 65 years and over; B28005_017E is 65 years and over with a computer and a broadband Internet subscription; B28005_001E is the total table population count."},{"kind":"tool","tool":"official.lookup","call":"Inspect public Census data.census.gov 2021 and 2022 ACS 1-year B28005 United States rows from published public Census-derived artifacts","result":"Fetched 2021 ACS 1-year United States B28005 counts: 65 years and over total 55,086,561 and 65+ with broadband subscription 43,757,048, computed share 79.4 percent. Fetched 2022 ACS 1-year counts: 65 years and over total 56,337,585 and 65+ with broadband subscription 45,989,221, computed share 81.6 percent."},{"kind":"tool","tool":"official.lookup","call":"Inspect public Census data.census.gov 2023 and 2024 ACS 1-year B28005 United States rows from published public Census-derived artifacts","result":"Fetched 2023 ACS 1-year United States B28005 counts: 65 years and over total 57,740,580 and 65+ with broadband subscription 48,245,700, computed share 83.5 percent. Fetched 2024 ACS 1-year counts: 65 years and over total 59,125,675 and 65+ with broadband subscription 50,144,228, computed share 84.8 percent."},{"kind":"tool","tool":"official.lookup","call":"Inspect Census data.census.gov 2024 ACS 1-year B28005 California row as high-adoption state benchmark","result":"Fetched California 2024 ACS 1-year B28005 counts: total population in households 38,537,958; 65 years and over total 6,333,225; 65+ with broadband subscription 5,786,620; computed share 91.4 percent."},{"kind":"tool","tool":"official.lookup","call":"Inspect Census-derived 2024 ACS 1-year Colorado profile and ACS release schedule pages","result":"Fetched Colorado 2024 ACS 1-year profile measures: population 5,957,494; median household income 97,113 dollars; poverty 9.6 percent; senior poverty 9 percent; households 2,479,892. Fetched 2024 ACS release schedule showing 1-Year Data Release with Detailed Tables and Summary File on September 11, 2025; current Census pages did not expose a separate 2025 ACS schedule confirming 2026-09-10, so I keep the ledger date and flag that release-calendar discrepancy rather than silently changing the target."},{"kind":"text","text":"Base rate/reference class: the best same-series reference class I could verify is the U.S. ACS 1-year B28005 age-65-plus series, which rose from 79.4 percent in 2021 to 84.8 percent in 2024. Colorado should sit above that national level because its 2024 median household income was 97,113 dollars and total poverty was 9.6 percent, while California's 2024 same-table high-adoption state benchmark was 91.4 percent."},{"kind":"text","text":"Level, momentum, one-off, and mechanism: level starts from a national 2025 prior near 86.0 percent, then adds a Colorado premium for higher income, lower poverty, and educated/urban Front Range composition, while holding below California's 91.4 percent benchmark because Colorado has more rural mountain and plains geography. Momentum remains positive from cohort replacement and cellular-data-plan inclusion. BEAD deployments are unlikely to move 2025 ACS collection much, and ACP expiration is a small downside drag."},{"kind":"math","text":"Prior/update/interval: persistence prior is the 2024 same-series U.S. ACS 1-year B28005 share of 84.8 percent. Historical sample is the same-series annual changes 2021-2022: 81.6 - 79.4 = +2.2, 2022-2023: 83.5 - 81.6 = +1.9, and 2023-2024: 84.8 - 83.5 = +1.3 percentage points, giving sigma = sqrt((2.2^2 + 1.9^2 + 1.3^2) / 3) = 1.8 percentage points as an annual-change RMS uncertainty proxy. National mechanism update adds +1.2 points to 86.0 for cohort replacement and continued subscription diffusion net of affordability drag; Colorado adjustment adds +1.7 points for income/poverty/composition but stays below the 91.4 California benchmark, yielding point 87.7. The 80% half-width is about 1.28*sigma = 1.28*1.8 = 2.3, widened slightly to 2.4 for state-level ACS sampling and first-print table noise, so bounds are 87.7 - 2.4 = 85.3 and 87.7 + 2.4 = 90.1."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger-than-expected jump in older-adult cellular-data-plan reporting or high-income retiree adoption in Colorado, which would land above the interval if the 2025 first print exceeds 90.1 percent. Downside risk is affordability churn after subsidy expiration, rural non-adoption, survey-composition noise, or a stall among the oldest households, which would land below the interval if the first print is under 85.3 percent. An outside the interval result would most likely reflect either a large ACS sampling/weighting move or a genuine state-level adoption break."},{"kind":"text","text":"Prior run update: I found only a prompt stub for this Colorado target in local records, not a completed prior same-target forecast. Existing catalog point estimates and intervals were not used as evidence; the only local artifacts used were public Census-derived history and target metadata."},{"kind":"forecast","point":87.7,"ciLow":85.3,"ciHigh":90.1}]}

# Reviewer critique
{"summary":"The draft has a sound resolver and coherent final numbers, but it relies on U.S. and California history while omitting the directly available Colorado same-series history needed for the prior, update, and interval.","requiredFixes":[{"rubricItem":"base_rate","severity":"blocking","summary":"The stated persistence prior is the 2024 U.S. 65+ broadband share rather than Colorado's own prior value for the same Census ACS B28005 target.","actionRequested":"Fetch and state Colorado B28005_017E / B28005_014E for recent ACS 1-year years, at minimum 2024 and preferably 2021-2024, and use that as the main persistence/base-rate prior or explicitly justify why it is unusable."},{"rubricItem":"model_prior","severity":"blocking","summary":"The time-series prior is based on national annual changes, not the target state's same-series time path.","actionRequested":"Use Colorado's own same-series annual changes as the model prior if available; if still using the national series, state that it is only a supplemental benchmark and explain why it dominates Colorado history."},{"rubricItem":"update","severity":"warning","summary":"The +1.7 Colorado premium is qualitatively justified by income, poverty, and composition but is not anchored to observed Colorado B28005 levels.","actionRequested":"Quantify the Colorado-vs-U.S. gap in the latest available same-table year and use that to justify any movement from the prior."},{"rubricItem":"interval","severity":"warning","summary":"The interval uses national annual-change RMS and then a small ad hoc widening for state ACS noise; this may understate or mischaracterize target-specific uncertainty.","actionRequested":"Base the interval on Colorado realized annual changes, ACS margin-of-error behavior for the state 65+ subgroup, or an explicit blend of national trend volatility plus state sampling uncertainty."},{"rubricItem":"prior_update_interval","severity":"blocking","summary":"The compact prior/update/interval step names a historical sample, adjustment, and sigma, but the sample is not the target history and the Colorado adjustment is not decomposed from observed Colorado data.","actionRequested":"Rewrite that step to name the Colorado historical sample, the starting Colorado prior, any national-trend or demographic adjustment components, the interval method, and the resulting bounds."}],"optionalSuggestions":["Keep the ledger resolution date while noting that the public 2025 ACS release calendar was not independently confirmed yet.","Add the latest Colorado ACS B28005 count pair to historicalContext so reviewers can audit the computed share directly.","Leave the no-catalog-circularity statement; it is useful and clear."]}

Emit the final JSON object only.
