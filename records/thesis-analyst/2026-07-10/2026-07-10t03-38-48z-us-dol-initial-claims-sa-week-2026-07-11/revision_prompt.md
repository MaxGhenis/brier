# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-11"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US initial claims, week ending Jul 11 2026","question":"U.S. Department of Labor advance seasonally adjusted initial unemployment insurance claims for the week ending July 11, 2026, first print","unit":"thousands","pointEstimate":216,"ciLow":203,"ciHigh":229,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims news release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance seasonally adjusted Initial Claims figure for the week ending July 11, 2026 in the first U.S. Department of Labor Unemployment Insurance Weekly Claims release published July 16, 2026 at 8:30 a.m. ET. Convert persons to thousands and ignore later revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"latest_week_2026-07-04_sa_initial_claims_thousands","value":215},{"label":"week_2026-06-27_sa_initial_claims_thousands","value":217},{"label":"week_2026-06-20_sa_initial_claims_thousands","value":216},{"label":"week_2026-06-13_sa_initial_claims_thousands","value":227},{"label":"latest_4wk_average_thousands","value":218.75},{"label":"latest_nsa_initial_claims_persons","value":224583}],"drivers":["latest SA claims at 215k","four-week average near 219k","recent June spike has faded","continuing claims stable near 1.81 million","July seasonal adjustment volatility remains material"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-10T03:39:13Z","reasoning":[{"kind":"heading","text":"US initial claims SA forecast for week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this targets the DOL advance seasonally adjusted Initial Claims figure for the week ending July 11, 2026, reported in persons in the Unemployment Insurance Weekly Claims release and expressed here in thousands. The variant is SA initial claims, matching source series ICSA; anchors below use the same SA variant except where explicitly flagged as NSA context."},{"kind":"tool","tool":"official.lookup","call":"Opened the current U.S. Department of Labor UI Weekly Claims news release PDF and read the headline SA release table.","result":"For week ending July 4, 2026, advance seasonally adjusted initial claims were 215,000, down 2,000 from the revised prior week of 217,000; the 4-week moving average was 218,750, down 3,750."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL release table of seasonally adjusted U.S. weekly UI claims history.","result":"Recent SA initial claims in thousands were May 30 2026: 225, June 6: 230, June 13: 227, June 20: 216, June 27: 217, and July 4: 215."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL release unadjusted-data and state-detail sections for one-off context.","result":"Latest NSA initial claims were 224,583 for week ending July 4, up 9,967 from 214,616; seasonal factors had expected an increase of 11,478; the comparable 2025 week had 241,361 NSA claims."},{"kind":"text","text":"Official release-date check: the ETA archive page says the UI Weekly Claims News Release is published each week on Thursday morning at 8:30am EST, with one listed 2026 exception, Wednesday November 25, 2026. July 16, 2026 is the Thursday following the July 11 claims week and is not the listed exception, so the first print resolves on July 16, 2026."},{"kind":"text","text":"Base rate/reference class: over the DOL table's 54 latest reported week-to-week SA initial-claims changes from June 28, 2025 through July 4, 2026, the average move was about -0.4 thousand and the series usually moved by roughly 10 thousand week to week; this supports a persistence-centered forecast rather than a large directional adjustment."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest SA level 215.0 thousand; historical sample = 54 successive DOL weekly SA changes from June 28, 2025 through July 4, 2026; adjustment components = +1.5 thousand level pull toward the 218.75 thousand four-week average, -0.5 thousand recent downward momentum, +0.0 one-off/NSA surprise adjustment, +0.0 policy-mechanism adjustment, giving point = 216.0 thousand. Interval method uses realized successive-change dispersion: mean change = -0.4, sigma = 10.3, half-width = 1.28*sigma = 1.28*10.3 = 13.2 thousand, so 216.0 +/- 13.2 gives 202.8 to 229.2, rounded to 203 to 229 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is another July seasonal-adjustment miss or renewed education/auto layoffs that would land above the interval, especially if the SA print returns to the late-May/early-June 225k-230k range. Downside risk is faster normalization after the June bulge or unusually low filings around the holiday week, which would land below the interval near or under 203k. Outside the interval would require a weekly move larger than about one recent sigma from the latest level."},{"kind":"forecast","point":216,"ciLow":203,"ciHigh":229}]}

# Reviewer critique
{"summary":"Draft is publication-ready with no blocking issues; resolver, prior, update, interval, tails, and JSON fields are coherent with the target.","requiredFixes":[],"optionalSuggestions":["Consider naming the ALFRED ICSA advance vintage alongside the DOL PDF in the resolver text to mirror the canonical sourceBinding more explicitly.","If space allows, note that the 203-229 interval is an 80% interval derived from 1.28 times recent weekly-change sigma."]}

Emit the final JSON object only.
