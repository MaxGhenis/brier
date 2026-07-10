# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.cpi.all_groups.yoy
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-july-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530.json"
- targetContentHash: "fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

# Source hints
- Use ABS release calendar and official monthly CPI indicator pages.
- Australia CPI indicator rates print to one decimal.
- Resolution source should be the ABS release page.

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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"Australian Bureau of Statistics monthly Consumer Price Index Indicator, All groups CPI annual movement for July 2026, original first print, percent, rounded to one decimal.","unit":"percent","pointEstimate":4.1,"ciLow":3.2,"ciHigh":5,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values unless ABS withdraws the first print before publication. The ledger sourceBinding appears to point to a June 2026 quarterly CPI-style page, but this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and resolves on the monthly July 2026 CPI indicator page.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 all groups annual movement","value":4},{"label":"April 2026 all groups annual movement","value":4.2},{"label":"March 2026 all groups annual movement","value":4.6},{"label":"February 2026 all groups annual movement","value":3.7}],"drivers":["Latest headline monthly CPI was about 4.0 percent in May 2026 after 4.2 percent in April","Trimmed mean near 3.6 percent points to persistent underlying inflation","Fuel excise and petrol effects lower headline temporarily but can reverse by July","Housing and food inflation keep the annual rate above the RBA target band"],"sourceContext":["https://www.abs.gov.au/statistics/release-calendar","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","https://www.theguardian.com/australia-news/2026/jun/24/interest-rate-hikes-remain-on-cards-as-underlying-inflation-climbs-economists-warn"],"runAt":"2026-07-10T05:31:50Z","reasoning":[{"kind":"heading","text":"Australia July 2026 monthly CPI indicator forecast"},{"kind":"text","text":"Framing and exact resolver: the target is the ABS Monthly Consumer Price Index Indicator, All groups CPI annual movement for July 2026, original first print, percent, one-decimal published value. This is the monthly indicator variant, not quarterly CPI, not trimmed mean, and not a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"ABS release-calendar lookup for the July 2026 monthly CPI indicator release date","result":"ABS calendar check for this target window gives the July 2026 Monthly Consumer Price Index Indicator first-print release on 2026-08-26 at the usual 11:30 Australia time slot; the ledger window was 2026-08-25 to 2026-09-02."},{"kind":"tool","tool":"official.lookup","call":"ABS latest monthly CPI indicator all-groups annual movement and components","result":"Fetched latest public release context: May 2026 headline All groups annual CPI was 4.0 percent, April 2026 was 4.2 percent, and the May 2026 trimmed mean annual rate was 3.6 percent."},{"kind":"tool","tool":"official.lookup","call":"ABS recent monthly CPI indicator reference points before April-May","result":"Fetched recent annual headline points for the same monthly all-groups variant: March 2026 was 4.6 percent and February 2026 was 3.7 percent; May 2026 housing was about 6.0 percent annually and food was about 3.3 percent annually."},{"kind":"text","text":"Base rate/reference class: for a one-to-two-month-ahead forecast of a monthly year-over-year inflation rate, the outside-view base rate is recent persistence in the same ABS all-groups annual series. The latest four-point level is centered around 4.1 percent, with a high March reading of 4.6 percent and a May reading of 4.0 percent after temporary fuel relief."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level is still above target because housing and services remain firm; momentum from May is slightly down; the temporary fuel excise and petrol decline depress headline inflation; a partial rebound or base-effect reversal by July argues against projecting May's 4.0 percent mechanically lower."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the same-series recent historical sample Feb-May 2026 at 3.7, 4.6, 4.2, 4.0. Adjustment components are +0.1 pp for possible fuel/base-effect rebound by July and 0.0 pp for underlying inflation persistence because trimmed mean at 3.6 is already below headline but still elevated. Successive changes are +0.9, -0.4, -0.2, so sigma = 0.70 using sample standard deviation of those changes; the 80 percent half-width is roughly 1.28*sigma = 0.90. Point = 4.0 + 0.1 = 4.1, interval = 4.1 +/- 0.9 = [3.2, 5.0]."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed fuel-price or utility-price jump plus sticky rents, which would land above the interval if July prints over 5.0 percent. Downside risk is a larger petrol reversal or broader demand slowdown, which would land below the interval if headline falls under 3.2 percent. An outside the interval result would most likely require a sharp energy or administered-price shock rather than ordinary month-to-month noise."},{"kind":"forecast","point":4.1,"ciLow":3.2,"ciHigh":5}]}

# Reviewer critique
{
  "summary": "Draft is mostly methodologically coherent, but publication should wait until the ledger/resolver-source mismatch is reconciled and the interval evidence is strengthened.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft resolves against the July 2026 Monthly CPI Indicator page, while the canonical ledger sourceBinding points to the ABS Consumer Price Index, Australia, June 2026 release.",
      "actionRequested": "Either fix the target registration/sourceBinding before publication or keep the draft explicitly tied to the ledger contract while documenting the concrete ledger discrepancy; do not leave resolver fields and ledger fields pointing to different ABS releases."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is based on only three recent monthly changes, which is too small a realized-volatility sample to support the stated uncertainty cleanly.",
      "actionRequested": "Use a longer same-series historical sample for month-ahead or two-month-ahead changes, or state that the half-width is judgmental and explain why [3.2, 5.0] is calibrated."
    },
    {
      "rubricItem": "leakage",
      "severity": "warning",
      "summary": "The sourceContext includes the July 2026 ABS page before publication, which could look like outcome leakage even if it is only a placeholder/resolver URL.",
      "actionRequested": "Label the July 2026 URL as the intended resolver page or remove it from evidence sources until after release."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether the persistence prior is anchored on May 2026 level or the Feb-May mean, since both are mentioned.",
    "Add one sentence saying a richer time-series model was ruled out because only a short-horizon persistence forecast was needed.",
    "Make the final resolver text match the exact first-print artifact that the automated resolver will fetch."
  ]
}

Emit the final JSON object only.
