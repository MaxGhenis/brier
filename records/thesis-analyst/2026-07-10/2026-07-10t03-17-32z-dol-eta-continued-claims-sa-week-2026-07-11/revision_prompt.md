# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-11"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-11.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US continued claims, week ending Jul 11","question":"What will the U.S. Department of Labor report as the first-print advance number of seasonally adjusted insured unemployment, also called continued claims, for the week ending July 11, 2026?","unit":"millions","pointEstimate":1.826,"ciLow":1.788,"ciHigh":1.864,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor, Employment and Training Administration, Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260723","resolutionRule":"Resolve to the first DOL ETA Unemployment Insurance Weekly Claims Report advance number for seasonally adjusted Insured Unemployment (Continued Claims), regular state programs, for week ending July 11, 2026, converted from persons to millions and rounded to three decimals. Do not use later revisions or all-programs unadjusted continued weeks claimed.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 latest CCSA SA insured unemployment","value":1.814},{"label":"2026-06-20 CCSA SA insured unemployment","value":1.806},{"label":"2026-06-13 CCSA SA insured unemployment","value":1.812},{"label":"2026-06-06 CCSA SA insured unemployment","value":1.8},{"label":"2026-05-30 CCSA SA insured unemployment","value":1.786}],"drivers":["latest SA insured unemployment was 1.814 million","four-week average rose to 1.808 million","recent weekly changes were modest but positive on balance","initial claims for July 4 were 215,000, suggesting no layoff spike","target is two reported continued-claims weeks beyond the latest official print"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://oui.doleta.gov/unemploy/claims_arch.asp","https://alfred.stlouisfed.org/series?seid=CCSA"],"runAt":"2026-07-10T03:18:56Z","reasoning":[{"kind":"heading","text":"Forecast for DOL CCSA week ending 2026-07-11"},{"kind":"text","text":"Framing and exact resolver: this targets DOL ETA regular state-program Insured Unemployment, seasonally adjusted, also mirrored as ALFRED/FRED series CCSA, for the week ending July 11, 2026. It is not the unadjusted all-programs continued-weeks total."},{"kind":"tool","tool":"official.lookup","call":"Opened the DOL ETA Unemployment Insurance Weekly Claims Report released July 9, 2026.","result":"Fetched latest SA insured unemployment: 1,814,000 for week ending June 27, 2026; prior revised level 1,806,000 for June 20; June 13 level 1,812,000; 4-week average 1,808,000; insured unemployment rate 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read the same DOL report's seasonally adjusted weekly history table.","result":"Fetched recent CCSA-compatible values in thousands: May 30 2026 = 1,786; June 6 = 1,800; June 13 = 1,812; June 20 = 1,806; June 27 = 1,814; July 4 initial claims = 215."},{"kind":"tool","tool":"alfred.lookup","call":"Opened ALFRED series page for CCSA as the ledger mirror and checked recent observations and metadata.","result":"Fetched ALFRED CCSA latest observation 2026-06-27 = 1,814,000, with prior observations 2026-06-20 = 1,806,000, 2026-06-13 = 1,812,000, 2026-06-06 = 1,800,000, and 2026-05-30 = 1,786,000; units are Number, Seasonally Adjusted, Weekly Ending Saturday."},{"kind":"tool","tool":"official.schedule","call":"Opened DOL OUI claims archive publication schedule and latest-release archive page.","result":"Fetched publication schedule text: UI Weekly Claims News Release is published each week on Thursday morning at 8:30 AM EST; listed 2026 exception is Wednesday, November 25, 2026 at 8:30 AM EST; archive was updated July 9, 2026. With no July 23 exception listed, the week ending July 11 insured-unemployment first print resolves in the Thursday July 23, 2026 release."},{"kind":"text","text":"Reference class/base rate: for the 52 latest DOL weekly SA insured-unemployment changes from June 28, 2025 through June 27, 2026, the level drifted from 1.952 million to 1.814 million, a mean weekly change of about -0.0027 million. The last four available changes were +0.014, +0.012, -0.006, and +0.008 million, so near-term momentum is slightly positive despite a lower year-over-year level."},{"kind":"text","text":"Level and mechanisms: the current level is 1.814 million, the four-week average is 1.808 million, and the July 4 initial-claims print of 215,000 argues against a sudden inflow shock. Continued claims can still edge up if hiring/outflows remain slow, so I add a small two-week net increase rather than reverting immediately to the one-year downward drift."},{"kind":"math","text":"Prior/update/interval: persistence prior on latest first-print/revised DOL CCSA level = 1.814 million; historical sample = 52 successive weekly changes in the DOL SA insured-unemployment history from June 28, 2025 to June 27, 2026; adjustment components = +0.008 million for recent continued-claims momentum and +0.004 million for slower outflows with no initial-claims spike, giving point = 1.814 + 0.008 + 0.004 = 1.826 million. Using successive changes, sum of squared changes = 22932 thousand^2, sum of changes = -138 thousand, n = 52, sigma = sqrt((22932 - 138^2/52)/51) = 21.0 thousand = 0.021 million. One-week 80% half-width is about 1.28*sigma = 0.027 million; for the two-report horizon I scale by sqrt(2), giving 0.038 million, so bounds are 1.826 - 0.038 = 1.788 and 1.826 + 0.038 = 1.864."},{"kind":"text","text":"Counter-considerations: upside risk is a material drop in benefit exhaustion or a sharp rebound in hiring that would push continued claims below the interval; downside risk is a layoff or school-seasonal adjustment miss that persists into continued claims and would land above the interval. Outside the interval would most plausibly require a weekly move larger than about 38,000 over the two-week horizon."},{"kind":"forecast","point":1.826,"ciLow":1.788,"ciHigh":1.864}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; resolver, unit, timing, prior, update, interval math, and JSON fields are broadly coherent.","requiredFixes":[],"optionalSuggestions":["Clarify the tail wording so lower continued claims are described as downside for the target value and higher continued claims as upside, avoiding directional ambiguity.","Tighten the interval/tail sentence: outside the interval means more than about 38k away from the 1.826m point, not necessarily a 38k move from the latest 1.814m observation.","The +0.004m slower-outflows adjustment would be stronger if tied explicitly to a named observed indicator or described as judgmental."]}

Emit the final JSON object only.
