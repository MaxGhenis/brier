# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.ssi.recipients.colorado.aged_65_plus
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "colorado-ssi-recipients-65-plus-july-2026"
- country: "US"
- targetUnit: "count"
- dataPointId: "ssa.ssi.recipients.colorado.aged_65_plus.2026-07.first_print"
- resolutionDate: "2026-08-31"

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
{"slug":"colorado-ssi-recipients-65-plus-july-2026","country":"US","type":"data","title":"Colorado SSI Recipients 65+ July 2026","question":"SSA SSI Monthly Statistics Table 4, Colorado recipients age 65 or older, July 2026, all federally administered payments, first print","unit":"count","pointEstimate":23060,"ciLow":23024,"ciHigh":23096,"confidence":0.8,"resolutionDate":"2026-08-31","resolutionSource":"Social Security Administration SSI Monthly Statistics, July 2026, Table 4","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table04.html","resolutionRule":"Resolve to the first posted July 2026 SSA SSI Monthly Statistics Table 4 value for Colorado in the Age 65 or older column under All Federally Administered Payments. Use the whole-count first print as published by SSA from the Supplemental Security Record, 100 percent data; do not revise for later table changes.","dataPointId":"ssa.ssi.recipients.colorado.aged_65_plus.2026-07.first_print","historicalContext":[{"label":"2026-06","value":23063},{"label":"2026-05","value":23036},{"label":"2026-04","value":23062},{"label":"2026-03","value":23039},{"label":"2026-02","value":23060},{"label":"2026-01","value":23102},{"label":"2025-12","value":23101}],"drivers":["Colorado 65+ SSI count has been nearly flat around 23.0k since December 2025","Recent monthly changes are small relative to the level","No identified July-specific policy mechanism that should shift Colorado aged recipients sharply","All anchors use SSA SSI Monthly Statistics Table 4, all federally administered payments, not federal-only or payment-dollar tables"],"sourceContext":["https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-06/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-05/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-04/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-03/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-02/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-01/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2025-12/table04.html","https://www.ssa.gov/policy/pub_schedule.html"],"runAt":"2026-07-21T09:29:19Z","reasoning":[{"kind":"heading","text":"Colorado SSI aged 65+ recipients, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the SSA SSI Monthly Statistics Table 4 Colorado row, Age 65 or older column, All Federally Administered Payments. The variant is a whole-person count from the Supplemental Security Record, 100 percent data, not payments, federal-only recipients, state-supplement-only recipients, or a smoothed series."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics June 2026 Table 4 for the latest official Colorado age-row anchor.","result":"Fetched June 2026 Colorado total 66,417; aged eligibility category 12,127; blind and disabled 54,290; under 18 6,657; age 18-64 36,697; age 65 or older 23,063."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May 2026 Table 4 for one-month-back official history.","result":"Fetched May 2026 Colorado total 66,403; aged eligibility category 12,120; blind and disabled 54,283; under 18 6,649; age 18-64 36,718; age 65 or older 23,036."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics April and March 2026 Table 4 for recent reference-class history.","result":"Fetched April 2026 Colorado age 65 or older 23,062 and March 2026 Colorado age 65 or older 23,039."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics February 2026, January 2026, and December 2025 Table 4 for a longer local official history window.","result":"Fetched February 2026 Colorado age 65 or older 23,060; January 2026 23,102; December 2025 23,101."},{"kind":"tool","tool":"official.lookup","call":"Checked SSA Research, Statistics & Policy Analysis Publishing Schedule for the release-calendar basis.","result":"Fetched official schedule page listing SSI Monthly Statistics with Monthly frequency and publication release dates; canonical target contract supplies the July 2026 first-print resolution date 2026-08-31 for this monthly release target."},{"kind":"text","text":"Reference class and base rate: the official Colorado 65+ recipient count over December 2025 through June 2026 is 23,101, 23,102, 23,060, 23,039, 23,062, 23,036, and 23,063. The level base rate is a stable 23.0k count series, with no month in this window outside 23,036 to 23,102."},{"kind":"text","text":"Level, momentum, one-off, and mechanism split: the level anchor is the latest 23,063; six-month momentum is mildly negative at -38 from December to June, while the latest move was +27 from May to June. I apply a small -3 net adjustment because the broader drift offsets the latest rebound. I found no July-specific policy mechanism in the official series definition that would materially change only Colorado aged 65+ recipients."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official June 2026 value 23,063 using the December 2025-June 2026 official SSA Table 4 reference class; adjustment components are level 23,063, momentum -6 from the mean monthly change, and recent stabilization +3, giving point 23,060. Successive changes are +1, -42, -21, +23, -26, +27; sigma = 27.9 recipients from the sample standard deviation of those changes; 80% half-width = 1.28*sigma = 1.28*27.9 = 35.7, rounded to 36, so bounds are 23,060-36 = 23,024 and 23,060+36 = 23,096."},{"kind":"text","text":"Counter-consideration: upside risk is a continued rebound in aged and disabled recipients after the spring decline, which would land above the interval if Colorado age 65+ exceeds 23,096. Downside risk is a renewed administrative or eligibility-driven drop like January-February, which would land below the interval if the first print is under 23,024. Outside the interval would require a move larger than the recent realized month-to-month dispersion."},{"kind":"forecast","point":23060,"ciLow":23024,"ciHigh":23096}]}

# Reviewer critique
{"summary":"Draft is publication-ready against the rubric, with coherent resolver details, prior/update/interval math, tails, and JSON fields tied to the ledger target.","requiredFixes":[],"optionalSuggestions":["Consider explicitly saying the July 2026 URL may be unresolved until first publication, while the resolver remains the first posted SSA Table 4 value."]}

Emit the final JSON object only.
