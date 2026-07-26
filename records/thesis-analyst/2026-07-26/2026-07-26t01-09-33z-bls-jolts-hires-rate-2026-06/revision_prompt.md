# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.jolts.hires_rate
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-hires-rate-june-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.hires_rate.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-04", "start": "2026-08-04"}, "field": "JTSHIR", "releasePolicy": "first_print", "sourceSeriesId": "JTSHIR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=JTSHIR", "table": "JOLTS news release, Table 1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-aac1aa24aa37cc74f3d987e746333ecbc85e7ba7a4c2bce674d42a0262147f03.json"
- targetContentHash: "aac1aa24aa37cc74f3d987e746333ecbc85e7ba7a4c2bce674d42a0262147f03"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"

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

Emit the final JSON object only. (agent thesis.analyst v2.4.0, prompt 7ef119647b35, tools 50a06b62f9be, promptMode fast)


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
{"slug":"jolts-hires-rate-june-2026","country":"US","type":"data","title":"US JOLTS hires rate, June 2026","question":"What will the BLS Job Openings and Labor Turnover Survey total nonfarm hires rate, seasonally adjusted, be for June 2026 in the first print?","unit":"percent","pointEstimate":3.3,"ciLow":3.12,"ciHigh":3.48,"confidence":0.8,"resolutionDate":"2026-08-04","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/jolts.t02.htm","resolutionRule":"Resolve to the first BLS-published June 2026 seasonally adjusted Total nonfarm hires rate in JOLTS news release Table 2, in percent and rounded as BLS reports it. Use the initial Aug. 4, 2026 release print only; ignore later revisions or annual updates.","dataPointId":"bls.jolts.hires_rate.2026_06.first_print","historicalContext":[{"label":"May 2026 hires rate, SA","value":3.3},{"label":"Apr 2026 hires rate, SA","value":3.3},{"label":"Mar 2026 hires rate, SA","value":3.5},{"label":"Feb 2026 hires rate, SA","value":3.1},{"label":"Jan 2026 hires rate, SA","value":3.4},{"label":"May 2025 hires rate, SA","value":3.4}],"drivers":["May first print held at 3.3 percent","Recent two-month stabilization after March volatility","2024-2026 reference class centered near 3.3-3.4 percent","JOLTS hires levels little changed in latest release","Seasonally adjusted total nonfarm variant only"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm","https://www.bls.gov/news.release/jolts.t02.htm","https://www.bls.gov/charts/job-openings-and-labor-turnover/hire-seps-rates.htm","https://fred.stlouisfed.org/series/JTSHIR","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=JTSHIR"],"runAt":"2026-07-26T01:10:09Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 BLS JOLTS hires rate"},{"kind":"text","text":"Framing: this is the BLS JOLTS Total nonfarm hires rate, seasonally adjusted, for June 2026, first print. The resolver should read Table 2 in the Aug. 4, 2026 JOLTS release and use the Total row rate, not levels, not not-seasonally-adjusted JTUHIR, and not later revised JTSHIR vintages."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule for the June 2026 reference month.","result":"BLS schedule lists June 2026 JOLTS for release on Aug. 04, 2026 at 10:00 AM; adjacent listed releases are May 2026 on Jun. 30, 2026 at 10:00 AM and July 2026 on Sep. 01, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"Read the latest BLS JOLTS Table 2 for the seasonally adjusted Total hires rate and level.","result":"BLS Table 2 Total row shows hires levels of 5,328 thousand in May 2025, 4,899 in Feb. 2026, 5,535 in Mar. 2026, 5,215 in Apr. 2026, and 5,170 in May 2026; corresponding Total hires rates are 3.4, 3.1, 3.5, 3.3, and 3.3 percent, with Apr.-May rate change 0.0."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS chart table for total nonfarm hires and separations rates, seasonally adjusted, to build the recent reference class.","result":"BLS chart gives hires rates: Jun 2024 3.3, Jul 2024 3.4, Aug 2024 3.3, Sep 2024 3.4, Oct 2024 3.3, Nov 2024 3.3, Dec 2024 3.3, Jan 2025 3.3, Feb 2025 3.3, Mar 2025 3.4, Apr 2025 3.4, May 2025 3.4, Jun 2025 3.4, Jul 2025 3.3, Aug 2025 3.2, Sep 2025 3.3, Oct 2025 3.3, Nov 2025 3.2, Dec 2025 3.3, Jan 2026 3.4, Feb 2026 3.1, Mar 2026 3.5, Apr 2026 3.3, May 2026 3.3 percent."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED/ALFRED mirror metadata for JTSHIR as a cross-check, not as the final resolution source.","result":"FRED/ALFRED JTSHIR reports May 2026 3.3, Apr 2026 3.3, Mar 2026 3.5, Feb 2026 3.1, Jan 2026 3.4; units are Rate, seasonally adjusted, monthly, and FRED lists next release date Aug. 4, 2026."},{"kind":"text","text":"Base rate/reference class: over the BLS Jun 2024-May 2026 recent expansion/cooling sample, the rate mostly sits from 3.2 to 3.4 percent, with only Feb 2026 at 3.1 and Mar 2026 at 3.5 breaking that tight range. That makes persistence around 3.3 the outside-view prior."},{"kind":"math","text":"Prior/update/interval: persistence prior model uses latest official May 2026 value 3.30 percent; historical sample is the 23 successive monthly changes from the BLS Jun 2024-May 2026 hires-rate series. Level effect 0.00 because May and Apr are both 3.3; momentum effect 0.00 after the Feb-Mar-Apr-May swings net back to 3.3; one-off/policy-mechanism effect 0.00 because this is a labor-turnover rate with no release-specific policy reset. Successive-change sum of squares is 0.41, sample sigma = sqrt(0.41/22) = 0.14 percentage point, so 80 percent half-width is about 1.28*sigma = 1.28*0.14 = 0.18. Final bounds are 3.30 - 0.18 = 3.12 and 3.30 + 0.18 = 3.48."},{"kind":"text","text":"Counter-consideration: upside risk is a rebound in gross hiring similar to Mar 2026 that would land above the interval at about 3.5 percent or higher; downside risk is a broad hiring freeze like Feb 2026 that would land below the interval near 3.1 percent or lower. The outside the interval cases are plausible but need a much sharper monthly move than the May/April stability implies."},{"kind":"forecast","point":3.3,"ciLow":3.12,"ciHigh":3.48}]}

# Reviewer critique
{"summary":"Draft is mostly coherent, but it conflicts with the canonical resolver/source binding for the target.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft resolves against BLS Table 2 at bls.gov, while the ledger contract binds this target to ALFRED/FRED adapter `alfred-fred`, allowed host `alfred.stlouisfed.org`, source series `JTSHIR`, first-print policy, and the Aug. 4, 2026 release window.","actionRequested":"Revise `resolutionSource`, `resolutionSourceUrl`, and `resolutionRule` to match the ledger source binding and first-print `JTSHIR` resolver, or explicitly note the apparent Table 1/Table 2 discrepancy in reasoning while keeping the forecast tied to the ledger target."}],"optionalSuggestions":["Keep the BLS Table 2 discussion as supporting evidence only, not as the resolver, if the published target is ALFRED first-print JTSHIR.","The interval and prior/update math are clear; no change needed there unless resolver wording changes the cited table context."]}

Emit the final JSON object only.
