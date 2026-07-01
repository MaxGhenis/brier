# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.labour.unemployment_rate.april_to_june_2026.first_print
- period: Apr-Jun 2026
- conditional_on: null

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Size the 80% interval from realized first-print dispersion, then widen or skew only for stated reasons.
- Name concrete upside, downside, and outside-the-interval scenarios.

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
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step, one math step, one counter-consideration, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.1.0, prompt 3a08d7c397df, tools e15bf40583f8, promptMode fast)


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
{"slug":"uk-ons-unemployment-rate-apr-jun-2026-first-print","country":"UK","type":"data","title":"UK unemployment Apr-Jun 2026","question":"ONS UK unemployment rate for people aged 16 years and over, seasonally adjusted Labour Force Survey estimate, April to June 2026, first print","unit":"percent","pointEstimate":5.1,"ciLow":4.7,"ciHigh":5.5,"confidence":0.8,"resolutionDate":"2026-08-11","resolutionSource":"Office for National Statistics Labour market overview, UK: August 2026","resolutionSourceUrl":"https://www.ons.gov.uk/releases/labourmarketoverviewukaugust2026","resolutionRule":"Resolve to the first ONS-published UK unemployment rate for people aged 16 years and over for April to June 2026, seasonally adjusted, in the August 2026 Labour market overview or linked ONS time-series page. Use the one-decimal percent first print only; ignore later revisions or reweighting changes published after the first print.","dataPointId":"ons.lms.unemployment_rate_16plus.apr_jun_2026.first_print","historicalContext":[{"label":"Nov 2025-Jan 2026","value":5.2},{"label":"Dec 2025-Feb 2026","value":4.9},{"label":"Jan-Mar 2026","value":5.0},{"label":"Feb-Apr 2026","value":4.9},{"label":"Mar-May 2026 vacancies","value":707},{"label":"May 2026 claimant count","value":1.712}],"drivers":["recent LFS unemployment has held near 5 percent","vacancies are at a five-year low","PAYE payroll has weakened into spring","claimant count is rising","LFS volatility argues for a wider interval"],"sourceContext":["https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/june2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/may2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/april2026","https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/march2026","https://www.ons.gov.uk/releasecalendar?highlight=true&limit=10&page=8&release-type=type-upcoming&sort=date-newest"],"runAt":"2026-06-27T13:34:32Z","reasoning":[{"kind":"heading","text":"Forecast UK Apr-Jun 2026 unemployment first print"},{"kind":"text","text":"The resolver is the first ONS print of the seasonally adjusted UK unemployment rate for people aged 16 years and over covering April to June 2026. ONS labour-market rates are reported to one decimal percent, and later revisions should not change the resolved value."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Labour market overview, UK: June 2026 for the latest LFS and labour-market indicators.","result":"Fetched February to April 2026 unemployment rate 4.9%, employment rate 75.0%, economic inactivity rate 21.0%, May 2026 claimant count 1.712 million, vacancies 707,000, payrolled employees down 31,000 over the comparable quarter and May payroll up 2,000 on the month."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Labour market overview, UK: May 2026 for the prior first-print LFS reference point.","result":"Fetched January to March 2026 unemployment rate 5.0%, employment rate 75.0%, economic inactivity rate 20.9%, April 2026 claimant count 1.699 million, vacancies 705,000, and April payrolled employees down 100,000 on the month."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Labour market overview, UK: April 2026 and March 2026 for the recent reference class.","result":"Fetched December 2025 to February 2026 unemployment rate 4.9%, January to March 2026 vacancies 711,000, November 2025 to January 2026 unemployment rate 5.2%, and December 2025 to February 2026 vacancies 721,000."},{"kind":"tool","tool":"official.lookup","call":"Checked ONS publication timing surfaces for labour-market releases and upcoming calendar context.","result":"Fetched June 2026 labour-market release date 18 June 2026, next release 21 July 2026, and upcoming calendar page around August 2026 showing confirmed releases including 5 August 2026 and 12 August 2026 entries; I use the August labour-market calendar slot for the Apr-Jun first print."},{"kind":"text","text":"Base-rate/reference-class anchor: the last four available rolling three-month first prints are 5.2, 4.9, 5.0, and 4.9, averaging 5.0. Month-to-month realized moves in this short reference class are about 0.1 to 0.3 percentage points, so a neutral outside view starts near 5.0 with an 80% band around plus or minus 0.4."},{"kind":"text","text":"Level and momentum: unemployment is already near 5%, vacancies have fallen from 721,000 to 711,000 to 705,000 to 707,000, and claimant count rose to 1.712 million. That pushes the Apr-Jun estimate modestly above the recent LFS average despite the latest headline dip to 4.9."},{"kind":"text","text":"Counter-consideration: LFS estimates remain volatile and ONS warns against over-reading short-term movements; May payroll was nearly flat after the April drop, so a continuation at 4.9 or a dip to 4.8 remains plausible if survey composition offsets payroll weakness."},{"kind":"math","text":"Start with recent first-print mean (5.2+4.9+5.0+4.9)/4 = 5.0. Add 0.1 percentage point for weak vacancies, rising claimant count, and spring PAYE weakness, giving 5.1. Use an 80% interval of 4.7 to 5.5: roughly the 5.1 center plus or minus 0.4, widened for LFS volatility and possible seasonal-adjustment/reweighting noise."},{"kind":"text","text":"Upside scenario: April-June layoffs and hiring freezes show through clearly in the LFS and unemployment prints 5.4 or 5.5. Downside scenario: April payroll weakness is revised away and survey volatility holds unemployment near 4.8 or 4.9. Outside-the-interval scenarios require either a sharp labour-market break above 5.5 or a strong participation/employment surprise below 4.7."},{"kind":"forecast","point":5.1,"ciLow":4.7,"ciHigh":5.5}]}

# Reviewer critique
{
  "summary": "The forecast is mostly coherent, but the resolution date is not supported by the cited calendar evidence and the model-prior step should be made more explicit.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft sets resolutionDate to 2026-08-11, but its cited calendar check only mentions August entries including 2026-08-05 and 2026-08-12, not 2026-08-11.",
      "actionRequested": "Verify the official ONS August 2026 labour-market release placeholder or calendar entry and set resolutionDate to the exact confirmed first-print publication date, with the cited source supporting that date."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a recent rolling mean/persistence anchor, but does not clearly say whether this is the intended time-series prior or whether a fuller model prior was ruled out.",
      "actionRequested": "Add one explicit sentence stating that the model prior is a persistence/recent-mean time-series prior, or explain why a separate time-series model is not used."
    }
  ],
  "optionalSuggestions": [
    "Clarify units in historicalContext for vacancies and claimant count so they cannot be mistaken for percent values.",
    "Tie the plus 0.1 inside-view adjustment more directly to expected movement in the Apr-Jun LFS unemployment target rather than general labour-market weakness."
  ]
}

Emit the final JSON object only.
