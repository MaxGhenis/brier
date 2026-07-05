# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statjp.cpi.tokyo_all_items_yoy
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "japan-tokyo-cpi-annual-rate-july-2026-prelim"

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"japan-tokyo-cpi-annual-rate-july-2026-prelim","country":"JP","type":"data","title":"Tokyo CPI annual inflation, July 2026 prelim","question":"Statistics Bureau of Japan Consumer Price Index for Ku-area of Tokyo, all items, July 2026, change over the year, first preliminary print","unit":"percent","pointEstimate":3.4,"ciLow":2.7,"ciHigh":4.1,"confidence":0.8,"resolutionDate":"2026-07-31","resolutionSource":"Statistics Bureau of Japan Consumer Price Index, Ku-area of Tokyo preliminary release","resolutionSourceUrl":"https://www.e-stat.go.jp/en/dbview?sid=0003427113","resolutionRule":"Resolve to the first published Ku-area of Tokyo preliminary all-items CPI change-over-the-year percentage for July 2026 in the Statistics Bureau of Japan/e-Stat Consumer Price Index release, using the agency's one-decimal percent rounding. Later revisions, corrections, or base-change restatements do not change the resolved value unless they are incorporated in the first July 2026 preliminary print itself.","dataPointId":"statjp.cpi.tokyo_all_items_annual_rate.july_2026.preliminary","historicalContext":[{"label":"Jun 2026 Tokyo all-items YoY preliminary","value":3.4},{"label":"May 2026 Tokyo all-items YoY preliminary","value":3.4},{"label":"Apr 2026 Tokyo all-items YoY preliminary","value":3.5},{"label":"Mar 2026 Tokyo all-items YoY preliminary","value":2.9},{"label":"Feb 2026 Tokyo all-items YoY preliminary","value":2.9}],"drivers":["Tokyo headline CPI has persisted around the low-to-mid 3 percent range","food and rice prices keep upside pressure in all-items CPI","energy and utility subsidy timing can pull headline inflation down or up","services persistence supports a forecast above 3 percent","July first print precedes the August 2025-base CPI revision schedule"],"sourceContext":["https://www.stat.go.jp/english/data/cpi/1582.html","https://www.stat.go.jp/english/data/cpi/1581-z.html","https://www.stat.go.jp/english/data/cpi/index.html","https://www.e-stat.go.jp/en/dbview?sid=0003427113"],"runAt":"2026-07-05T13:48:51Z","reasoning":[{"kind":"heading","text":"Forecast Tokyo all-items CPI YoY for July 2026"},{"kind":"text","text":"The resolver is the first preliminary Statistics Bureau of Japan/e-Stat Ku-area of Tokyo CPI print for July 2026, all items, change over the year, rounded to one decimal percent. This uses the same all-items, non-seasonally-adjusted, change-over-year variant for the target, anchors, and history."},{"kind":"tool","tool":"official.lookup","call":"Checked the Statistics Bureau of Japan CPI schedule page for the July 2026 Ku-area of Tokyo preliminary release date.","result":"Fetched official release schedule last updated 23 January 2026: Japan June 2026 CPI releases July 24, 2026; Ku-area of Tokyo July 2026 preliminary releases July 31, 2026; August 2026 line notes revision to 2025-base Consumer Price Index."},{"kind":"tool","tool":"official.lookup","call":"Checked the Statistics Bureau CPI landing and latest-results pages for official target source and base-revision context.","result":"Fetched official CPI page information: 2025-base item information release is 10 July 2026, historical 2025-base data release is 7 August 2026, and monthly reports begin 2025-base on 21 August 2026; latest-results page links Japan / Ku-area of Tokyo CPI to e-Stat."},{"kind":"tool","tool":"official.lookup","call":"Checked the e-Stat dbview for the exact CPI table and latest available time entries.","result":"Fetched e-Stat table metadata: sid 0003427113, Consumer Price Index 2020-Base, table number 1, published date and time 2026-06-26 08:30, with time entries including Jun. 2026, May 2026, Apr. 2026, Mar. 2026, Feb. 2026, and Jan. 2026."},{"kind":"tool","tool":"official.lookup","call":"Read recent official Tokyo all-items change-over-year context from the public Thesis run record tied to the same Statistics Bureau/e-Stat source and June database update.","result":"Fetched recent Tokyo all-items YoY values: Jun. 2026 3.4 percent, May 2026 3.4 percent, Apr. 2026 3.5 percent, Mar. 2026 2.9 percent, Feb. 2026 2.9 percent."},{"kind":"text","text":"Base-rate/reference class: for one-month-ahead Tokyo all-items YoY CPI, persistence around the latest official Tokyo prints is the base rate. The recent reference class is clustered at 2.9, 2.9, 3.5, 3.4, and 3.4 percent rather than showing a sustained break away from the low-to-mid 3 percent range."},{"kind":"text","text":"Level, momentum, and mechanism split: the level is elevated by Japan's pre-2022 standards, but momentum is roughly flat after April-June held near 3.4 to 3.5. Food and rice inflation are the main upside mechanism, while energy, gasoline, and utility subsidy/base effects are the main downside mechanism."},{"kind":"math","text":"Prior/update/interval: persistence prior from recent official Tokyo all-items YoY prints uses Feb-Jun 2026 values 2.9, 2.9, 3.5, 3.4, 3.4; latest-value prior = 3.4 and five-month average = 3.22, so I keep the point at 3.4 after a small food/services upside offset to flat momentum. Successive changes are 0.0, +0.6, -0.1, 0.0, so sample sigma = 0.32 percentage point; 1.28*sigma = 0.41. I widen to a 0.7-point half-width because headline all-items CPI has fresh-food and energy/subsidy risk beyond the tiny five-print sample, giving 2.7 to 4.1."},{"kind":"text","text":"Counter-consideration and scenarios: downside risk outside the interval would be a sharp energy-subsidy or gasoline-base-effect drop plus softer fresh food, pushing July below 2.7. Upside risk outside the interval would be renewed rice/food acceleration or utility pass-through pushing the first print above 4.1. The central case is persistence near 3.4."},{"kind":"forecast","point":3.4,"ciLow":2.7,"ciHigh":4.1}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; it states the official first-print resolver, July 31 2026 resolution date, persistence prior, update logic, interval method, tails, and coherent JSON fields.","requiredFixes":[],"optionalSuggestions":["Consider citing the direct official e-Stat observations for the Feb-Jun 2026 values instead of relying on a public Thesis run record for that historical context.","If the canonical ledger has a different dataPointId naming convention for this series, note that discrepancy explicitly in reasoning while keeping the catalog slug unchanged."]}

Emit the final JSON object only.
