# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.employed_people_by_occupation.healthcare_support
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-healthcare-support-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.healthcare_support.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Healthcare support occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.healthcare_support", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-e2043717570a339e4f9e280e31486229af547196d9c88d0ccdbf8936af8bb3f1.json"
- targetContentHash: "e2043717570a339e4f9e280e31486229af547196d9c88d0ccdbf8936af8bb3f1"
- registrationCommit: "36b3b6b19986083e354c0bd56b0090751cfaeba7"
- registeredAtUtc: "2026-07-21T01:00:49Z"

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
{"slug":"cps-healthcare-support-employment-july-2026","country":"US","type":"data","title":"US healthcare support employment, July 2026","question":"What will BLS first report for July 2026 employed people age 16 and over in healthcare support occupations, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":5.801,"ciLow":4.626,"ciHigh":6.976,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published for July 2026 in BLS CPS Employment Situation Table A-19, row 'Healthcare support occupations,' Total, 16 years and over, not seasonally adjusted. Multiply the published thousands value by 0.001 and retain three decimal places in millions. Ignore all later revisions; no correction or release-day grace exception applies.","dataPointId":"bls.cps.employed_people_by_occupation.healthcare_support.july_2026.first_print","historicalContext":[{"label":"July 2023 NSA CPS healthcare support employment","value":4.911},{"label":"June 2025 NSA CPS healthcare support employment","value":5.95},{"label":"June 2026 NSA CPS healthcare support employment","value":5.691}],"drivers":["June 2026 level persistence","modest July seasonal uplift","long-run healthcare labor demand","high CPS subgroup sampling volatility"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/2026/home.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/news.release/conemp.t02.htm"],"runAt":"2026-07-21T01:09:11Z","reasoning":[{"kind":"heading","text":"July 2026 healthcare support employment forecast"},{"kind":"text","text":"The resolver is the first July 2026 print for Total employed people age 16 and over in 'Healthcare support occupations' in CPS Table A-19, measured in thousands and not seasonally adjusted, then multiplied by 0.001. All anchors below use that same CPS occupation/NSA variant. The ledger expectedReleaseWindow ending 2026-08-06 conflicts with the official August 7 release date; the forecast remains tied to the registered target and uses the verified official date."},{"kind":"tool","tool":"official.lookup","call":"Read current BLS CPS Employment Situation Table A-19 for the healthcare support occupations row.","result":"BLS Table A-19 reports 5,950 thousand for June 2025 and 5,691 thousand for June 2026, equivalent to 5.950 million and 5.691 million."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS July 2023 contingent-work table as an additional public CPS occupation-level reference observation.","result":"The BLS CPS table reports 4,911 thousand total employed people in healthcare support occupations in July 2023, equivalent to 4.911 million."},{"kind":"tool","tool":"official.calendar","call":"Verify the July 2026 Employment Situation publication date using the BLS 2026 release calendar and latest release announcement.","result":"The official calendar lists Employment Situation for July 2026 on Friday, August 7, 2026 at 8:30 AM ET; the June 2026 release repeats August 7, 2026."},{"kind":"text","text":"The outside-view base rate/reference class is persistence around the latest 5.691 million level, with substantial CPS subgroup noise. The sparse same-variant official history spans 4.911 million in July 2023, 5.950 million in June 2025, and 5.691 million in June 2026."},{"kind":"text","text":"Level contributes 5.691 million. Momentum is mixed: the latest year-over-year change is -0.259 million. A July calendar/seasonal adjustment contributes +0.080 million, while continuing structural demand for healthcare support labor contributes +0.030 million; no discrete policy or one-off shock is added."},{"kind":"math","text":"Prior/update/interval: persistence model prior = 5.691 million; historical sample = 4.911, 5.950, and 5.691 million. Successive changes are +1.039 and -0.259 million; their sample standard deviation gives sigma = sqrt(((1.039-0.390)^2+(-0.259-0.390)^2)/(2-1)) = 0.918 million. Updates are +0.080 July seasonality and +0.030 structural healthcare demand, so point = 5.691+0.080+0.030 = 5.801 million. The 80% half-width is 1.28*sigma = 1.28*0.918 = 1.175 million, implying 5.801-1.175 = 4.626 and 5.801+1.175 = 6.976 million."},{"kind":"text","text":"Upside risk comes from unusually strong household-survey sampling, labor-force entry, or faster caregiving hiring and would land above the interval at more than 6.976 million. Downside risk comes from a sharp participation decline, healthcare funding disruption, or an adverse CPS sampling swing and would land below the interval at less than 4.626 million. The wide interval reflects realized occupation-level dispersion rather than a rounded hedge."},{"kind":"forecast","point":5.801,"ciLow":4.626,"ciHigh":6.976}]}

# Reviewer critique
{"summary":"The draft is publishable with one warning: its resolver and math are coherent, but the inside-view uplift is only lightly justified against the sparse prior.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The +0.080 July seasonality and +0.030 structural-demand adjustments are asserted but not backed by a concrete July seasonal comparison or recent healthcare-support-specific trend evidence.","actionRequested":"Add a short evidence sentence tying the July uplift and structural adjustment to cited A-19 history, or explicitly state that these are judgmental small adjustments and why they are limited."}],"optionalSuggestions":["Use additional archived A-19 monthly observations if available to make the realized-volatility interval less dependent on only two changes.","Keep the explicit note that the official BLS release date is August 7, 2026 despite the ledger expected-release-window discrepancy."]}

Emit the final JSON object only.
