# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.labour.vacancies_total
- period: 2026-07
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-vacancies-may-jul-2026"
- country: "UK"
- targetUnit: "thousands"
- dataPointId: "ons.labour.vacancies_total.2026_07.first_print"
- expectedReleaseWindow: {"end": "2026-09-15", "start": "2026-09-15"}
- resolutionSourceUrl: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-09-15", "start": "2026-09-15"}, "field": "UK Vacancies (thousands) - Total, seasonally adjusted, value for 2026 JUL", "releasePolicy": "first_print", "sourceSeriesId": "AP2Y", "sourceUrl": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem", "table": "Claimant count and vacancies time series (UNEM)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-19-2c9ce13c4e282d7375b8e1811bdd814a314e03e873df8ba165e8d9a14efcdcf1.json"
- targetContentHash: "2c9ce13c4e282d7375b8e1811bdd814a314e03e873df8ba165e8d9a14efcdcf1"
- registrationCommit: "1a8c5d83d07cc6160ba5e11d8754092d64a2fc64"
- registeredAtUtc: "2026-08-19T15:37:16Z"

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class: at least 6 distinct prints are MANDATORY whenever the official source exposes them.
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
  "unit": "the registered targetUnit, byte-for-byte",
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
      "period": {
        "type": "month",
        "value": "2026-04"
      },
      "label": "Human-readable period label",
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
- historicalContext must contain at least 6 distinct numeric fetched prints. Every entry needs a canonical period object: type month with YYYY-MM, quarter with YYYY-Q1..Q4, year/fiscal_year with YYYY, or week_ending with YYYY-MM-DD. Its label must unambiguously name that same period. The whole trimmed label must be one closed printable-ASCII form: YYYY-MM, Month YYYY, YYYY Month, YYYY-QN, YYYY QN, QN YYYY, YYYY, calendar year YYYY, FY2026, fiscal year YYYY, YYYY-MM-DD, or week ending YYYY-MM-DD. Never add source names, first-print or revision prose, ranges, or a second period cue to the label. Relative, contradictory, non-ASCII, and multi-period labels refuse. Alternate labels do not make duplicate canonical periods distinct. Validation refuses fewer unless the sealed checkout carries the reviewed authorization below.
- Only when the official source exposes fewer than 6 prints, fetch all available prints and add this top-level audit commentary (replace 5 with the actual count and give a nonempty detail): {"historyAvailability": {"status": "official_source_exposes_fewer_than_six_prints", "availablePrintCount": 5, "detail": "Series began recently; the official source exposes only these five prints."}}
  This model-authored commentary never authorizes an exception: a reviewed docket entry in the sealed checkout must independently list the exact target period, available count, and canonical periods.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.5.11, prompt 87db344b803f, tools 024388e49298, promptMode fast)


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
{"slug":"uk-vacancies-may-jul-2026","country":"UK","type":"data","title":"UK Vacancies, AP2Y, 2026 JUL","question":"What will the Office for National Statistics first print for UK Vacancies (thousands) - Total, seasonally adjusted, series AP2Y, period 2026 JUL?","unit":"thousands","pointEstimate":703,"ciLow":692,"ciHigh":714,"confidence":0.8,"resolutionDate":"2026-09-15","resolutionSource":"Office for National Statistics UK Vacancies (thousands) - Total time series AP2Y","resolutionSourceUrl":"https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem","resolutionRule":"Resolve to the first official ONS AP2Y value for period 2026 JUL in the UK Vacancies (thousands) - Total, seasonally adjusted, UNEM time series. Use the integer value in thousands as first published for the 15 September 2026 release; ignore later revisions or corrections unless they replace the first-print page before publication is observable.","dataPointId":"ons.labour.vacancies_total.2026_07.first_print","historicalContext":[{"period":{"type":"month","value":"2025-07"},"label":"2025-07","value":737},{"period":{"type":"month","value":"2025-08"},"label":"2025-08","value":729},{"period":{"type":"month","value":"2025-09"},"label":"2025-09","value":728},{"period":{"type":"month","value":"2025-10"},"label":"2025-10","value":730},{"period":{"type":"month","value":"2025-11"},"label":"2025-11","value":739},{"period":{"type":"month","value":"2025-12"},"label":"2025-12","value":734},{"period":{"type":"month","value":"2026-01"},"label":"2026-01","value":725},{"period":{"type":"month","value":"2026-02"},"label":"2026-02","value":718},{"period":{"type":"month","value":"2026-03"},"label":"2026-03","value":713},{"period":{"type":"month","value":"2026-04"},"label":"2026-04","value":710},{"period":{"type":"month","value":"2026-05"},"label":"2026-05","value":711},{"period":{"type":"month","value":"2026-06"},"label":"2026-06","value":707}],"drivers":["Vacancies broadly flat but still easing","Small-firm labour-cost pressure","Weak PAYE employment backdrop","Three-month average smooths monthly shocks"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/august2026","https://www.gov.uk/government/statistics/announcements/uk-labour-market-september-2026"],"runAt":"2026-08-19T15:41:51Z","reasoning":[{"kind":"heading","text":"ONS AP2Y 2026 JUL Forecast"},{"kind":"text","text":"The resolver is the ONS AP2Y series, UK Vacancies (thousands) - Total, seasonally adjusted, in the UNEM time-series page. The ledger slug says May-Jul 2026, but the ONS AP2Y page currently shows 2026 JUN as the May to July 2026 print, so I keep the target tied to the registered AP2Y 2026 JUL field and note that this appears to be a ledger label discrepancy rather than a change to the target."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS AP2Y time-series page for UK Vacancies (thousands) - Total.","result":"ONS AP2Y was released on 18 August 2026, next release 15 September 2026, and recent monthly values included 2026 JAN 725, 2026 FEB 718, 2026 MAR 713, 2026 APR 710, 2026 MAY 711, and 2026 JUN 707."},{"kind":"tool","tool":"official.lookup","call":"Read the ONS Labour market overview, UK: August 2026 bulletin.","result":"ONS said early estimates for May to July 2026 vacancies decreased by 6,000, or 0.8%, to 707,000, compared with February to April 2026, and had decreased by 11,000 since January to March 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the official September 2026 UK Labour Market announcement.","result":"The GOV.UK official statistics announcement gives UK Labour Market: September 2026 a confirmed release date of 15 September 2026 at 7:00am; the relevant latest AP2Y value checked against that release path is 707 thousand for 2026 JUN."},{"kind":"tool","tool":"official.lookup","call":"Fetched the AP2Y recent reference class from the ONS time-series table.","result":"The 18-print AP2Y sample used for changes was 2025 JAN 793, FEB 775, MAR 759, APR 738, MAY 730, JUN 727, JUL 737, AUG 729, SEP 728, OCT 730, NOV 739, DEC 734, 2026 JAN 725, FEB 718, MAR 713, APR 710, MAY 711, JUN 707."},{"kind":"text","text":"Base rate/reference class: the recent official AP2Y sequence is a low-volatility level series after the 2022 peak, with the last six prints moving 725 to 718 to 713 to 710 to 711 to 707. Persistence from 707 is the starting base rate, then I apply a small negative drift because the ONS bulletin still describes vacancies as decreasing and small firms as constrained by labour costs and operating expenses."},{"kind":"math","text":"Prior/update/interval: persistence prior = 707 from AP2Y 2026 JUN; historical sample = 18 latest official monthly AP2Y prints from 2025 JAN through 2026 JUN; adjustment components = level 707, momentum about -3 to -4 from the latest changes, one-off none, policy-mechanism effect small negative from labour-cost pressure; final point = 707 - 4 = 703. Successive changes in the sample are -18,-16,-21,-8,-3,10,-8,-1,2,9,-5,-9,-7,-5,-3,1,-4, giving sigma = 8.35 thousand. The 80% half-width is about 1.28*sigma = 1.28*8.35 = 10.69 thousand, so rounded bounds are 703 - 11 = 692 and 703 + 11 = 714."},{"kind":"text","text":"Upside risk is a rebound in hiring demand or a favorable survey rotation that would keep AP2Y near or above 715. Downside risk is a sharper hiring freeze from higher labour costs or weakening payroll employment that would land below 692. Outside the interval would likely require a move larger than the recent non-pandemic monthly dispersion, not just another flat three-month average."},{"kind":"forecast","point":703,"ciLow":692,"ciHigh":714}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; it ties the forecast to the registered AP2Y 2026 JUL first-print target, states a persistence prior, explains the update, and keeps point/interval fields coherent.","requiredFixes":[],"optionalSuggestions":["Tighten the ledger-label discrepancy sentence so it clearly distinguishes the known 2026 JUN AP2Y latest value from the registered 2026 JUL target resolving on 2026-09-15.","In the tail-risk sentence, name the rolling-vacancy target explicitly so the upside/downside scenarios are unmistakably tied to AP2Y rather than broader labour-market indicators."]}

Emit the final JSON object only.
