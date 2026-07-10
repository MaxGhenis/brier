# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.pusf.j5ii.public_sector_net_borrowing_ex_banks
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-pusf-j5ii-public-sector-net-borrowing-ex-banks-june-2026"
- country: "UK"
- targetUnit: "gbp_billions"
- dataPointId: "ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:public_sector_finances:2026-05:j5ii", "releasePolicy": "first_print", "sourceSeriesId": "ons.pusf.j5ii", "sourceUrl": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026", "table": "Public sector finances, UK: May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-d5d0a8776dcdb7739f0aa1d0a24ecbdecf6cbbe3593a2c616a571c1f091ec4e8.json"
- targetContentHash: "d5d0a8776dcdb7739f0aa1d0a24ecbdecf6cbbe3593a2c616a571c1f091ec4e8"
- registeredAtUtc: "2026-07-10T05:58:27Z"

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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
{"slug":"ons-pusf-j5ii-public-sector-net-borrowing-ex-banks-june-2026","country":"UK","type":"data","title":"UK PSNB ex Banks, June 2026","question":"ONS Public sector finances series J5II / bulletin -J5II, public sector net borrowing excluding public sector banks, June 2026, current-price not seasonally adjusted, first print","unit":"gbp_billions","pointEstimate":24.8,"ciLow":13.8,"ciHigh":35.8,"confidence":0.8,"resolutionDate":"2026-07-21","resolutionSource":"Office for National Statistics Public sector finances, UK","resolutionSourceUrl":"https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026","resolutionRule":"Resolve on the first ONS print for June 2026 public sector net borrowing excluding public sector banks. Use the Public sector finances June 2026 bulletin/table value for code -J5II, or equivalently convert raw J5II time-series £m to £ billions with the bulletin borrowing sign convention, where positive means borrowing/deficit. Do not use later revisions, superseded versions, or same-day corrections unless the first-print bulletin itself is replaced before release publication is complete.","dataPointId":"ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.june_2026.first_print","historicalContext":[{"label":"latest_may_2026_bulletin_borrowing","value":23.3},{"label":"april_2026_j5ii_converted","value":23.033},{"label":"june_2025_first_print_borrowing","value":20.7},{"label":"june_2024_first_print_borrowing","value":14.1},{"label":"june_2023_current_timeseries_converted","value":19.085}],"drivers":["May 2026 borrowing was already elevated at GBP 23.3bn versus an OBR forecast of GBP 17.7bn","Financial year to May 2026 borrowing was GBP 46.3bn, GBP 7.7bn above OBR forecast","June is exposed to volatile index-linked gilt debt-interest accruals","Recent June reference class has shifted higher than the pre-pandemic norm","Receipts growth partly offsets higher debt interest, benefits, and departmental spending"],"sourceContext":["https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/j5ii/pusf","https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026","https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/june2025","https://obr.uk/efo/economic-and-fiscal-outlook-march-2026/"],"runAt":"2026-07-10T06:04:37Z","reasoning":[{"kind":"heading","text":"June 2026 UK Public Sector Net Borrowing Forecast"},{"kind":"text","text":"Framing and exact resolver: the target is ONS public sector net borrowing excluding public sector banks for June 2026, first print, in GBP billions. The ONS time-series page is J5II in GBP millions with the raw accounting sign, while bulletin charts/tables use -J5II so positive numbers indicate a deficit; I forecast the registered borrowing concept in the bulletin convention, positive = borrowing. The ledger URL points to the May 2026 bulletin even though the target month is June 2026; I keep that registered URL, and use its official next-release statement plus the J5II series page to tie the target to the 21 July 2026 first print."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS J5II time-series page for PUSF and read metadata and latest values.","result":"Fetched: release date 19 June 2026, next release 21 July 2026, Series ID J5II, units GBP m, 2026 APR raw J5II -23033 and 2026 MAY raw J5II -23294, which convert to GBP 23.033bn and GBP 23.294bn borrowing under the bulletin -J5II convention."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Public sector finances, UK: May 2026 bulletin for current-release drivers and forecast comparison.","result":"Fetched: May 2026 borrowing was GBP 23.3bn, GBP 5.4bn more than May 2025 and GBP 5.6bn above the OBR forecast of GBP 17.7bn; central government debt interest payable was GBP 11.7bn; financial-year-to-May borrowing was GBP 46.3bn versus OBR forecast GBP 38.6bn."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Public sector finances, UK: June 2025 bulletin for the prior same-month first-print and debt-interest mechanics.","result":"Fetched: June 2025 borrowing was GBP 20.7bn, GBP 6.6bn more than June 2024 and GBP 3.5bn above the OBR forecast of GBP 17.1bn; June 2025 central government debt interest was GBP 16.4bn; capital uplift was GBP 10.9bn reflecting a 1.7% RPI rise between March and April 2025."},{"kind":"tool","tool":"official.lookup","call":"Read ONS J5II monthly history for June reference class and converted raw J5II signs to positive borrowing.","result":"Fetched June converted values, GBP bn: 2013 8.310, 2014 7.930, 2015 7.705, 2016 4.876, 2017 6.458, 2018 4.103, 2019 6.791, 2020 32.165, 2021 18.721, 2022 18.871, 2023 19.085, 2024 14.617, 2025 23.878."},{"kind":"text","text":"The reference class base rate is same-month June borrowing. The full 2013-2025 June sample averages about GBP 13.35bn, but the post-2021 regime averages about GBP 19.0bn and the 2025 first print was GBP 20.7bn. Because May 2026 is already GBP 5.6bn above the OBR monthly profile and FY-to-May is GBP 7.7bn above profile, I weight the recent June regime and current-year miss more heavily than the long pre-pandemic base rate."},{"kind":"math","text":"Prior/update/interval: persistence prior = June 2025 first print GBP 20.7bn and 2021-2025 June reference-class mean about GBP 19.0bn; adjustments = +GBP 3.0bn for the current FY-to-May overshoot and higher May run rate, +GBP 1.1bn for June debt-interest and spending risk after May debt interest of GBP 11.7bn, giving point GBP 24.8bn. Interval method uses the 2013-2025 June converted values themselves because this is a monthly flow series: sample sigma = 8.6, so 80% half-width is about 1.28*sigma = 1.28*8.6 = 11.0. Final implied bounds are 24.8 - 11.0 = 13.8 and 24.8 + 11.0 = 35.8."},{"kind":"text","text":"Counter-considerations: upside risk would come from another large index-linked gilt capital-uplift month, weaker PAYE/VAT/corporation tax receipts, or local-government/public-corporation estimates adding to central-government borrowing; a repeat of June 2020-style stress would land above the interval. Downside risk would come from a sharp fall in RPI-linked debt interest, stronger accrued receipts, or unusually low net investment; a clean reversal toward the 2016-2019 June range would land below the interval."},{"kind":"forecast","point":24.8,"ciLow":13.8,"ciHigh":35.8}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; it identifies the registered resolver discrepancy, states a same-month/persistence prior, justifies the upward adjustment, and keeps point/interval/JSON fields coherent.","requiredFixes":[],"optionalSuggestions":["Add the exact ONS next-release wording or release-calendar citation beside the 2026-07-21 resolution date if available.","Clarify in one phrase that the 2025 value differs between first print and current revised time-series, since both appear in the reasoning."]}

Emit the final JSON object only.
