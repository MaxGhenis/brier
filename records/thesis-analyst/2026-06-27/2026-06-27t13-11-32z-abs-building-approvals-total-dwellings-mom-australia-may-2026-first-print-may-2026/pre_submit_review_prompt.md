# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review only the draft forecast, the target spec, and public evidence cited in the draft. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.building_approvals.total_dwellings_mom.australia.may_2026.first_print
- period: May 2026
- conditional: null

# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. Tail scenarios are concrete and tied to the target.
7. Point, interval, final forecast step, and JSON fields are coherent.
8. No leakage, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
0f009e067467b33abe8af615ace94f57fa1e9145df338934cd7a5ec1005f174b

# Draft forecast response
{"slug":"abs-building-approvals-total-dwellings-mom-australia-may-2026-first-print","country":"AU","type":"data","title":"Australia building approvals May 2026 MoM","question":"ABS Building Approvals, Australia: seasonally adjusted total dwelling units approved, May 2026 monthly percent change, first print","unit":"percent_growth","pointEstimate":2.0,"ciLow":-10.0,"ciHigh":16.0,"confidence":0.8,"resolutionDate":"2026-07-01","resolutionSource":"Australian Bureau of Statistics Building Approvals, Australia release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/may-2026","resolutionRule":"Resolve to the first ABS-published May 2026 seasonally adjusted monthly change in total dwelling units approved, in percent, as shown in Building Approvals, Australia on 2026-07-01 at 11:30am AEST. Use the first print only; ignore later revisions, including the updated small-area data-cube release scheduled for 2026-07-08. If ABS reports one decimal place, resolve to that one-decimal value.","dataPointId":"abs.building_approvals.total_dwellings_mom.australia.2026-05.first_print","historicalContext":[{"label":"Apr 2026 first print total dwellings MoM percent","value":-3.4},{"label":"Mar 2026 first print total dwellings MoM percent","value":-10.5},{"label":"Feb 2026 first print total dwellings MoM percent","value":29.7},{"label":"Jan 2026 first print total dwellings MoM percent","value":-7.2},{"label":"Apr 2026 seasonally adjusted total dwellings level","value":16710}],"drivers":["April level was below trend, leaving room for partial mean reversion","Large multi-unit swings dominate month-to-month volatility","Underlying trend was close to flat after earlier 2026 gains","Housing-supply policy support is positive but unlikely to remove monthly noise","High construction costs and feasibility constraints cap upside"],"sourceContext":["https://www.abs.gov.au/release-calendar/future-releases/202607","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/mar-2026","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/feb-2026","https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/jan-2026"],"runAt":"2026-06-27T13:11:37Z","reasoning":[{"kind":"heading","text":"Forecast May 2026 ABS total dwelling approvals monthly change"},{"kind":"text","text":"The resolver is the first ABS print for Building Approvals, Australia, May 2026: seasonally adjusted total dwelling units approved, monthly percent change. The July 8 updated-information item is excluded because the target is first print."},{"kind":"tool","tool":"official.lookup","call":"ABS July 2026 future release calendar for Building Approvals, Australia May 2026","result":"Fetched official schedule: Building Approvals, Australia, reference period May 2026, Wednesday 01 July 2026 at 11:30am AEST; updated information for the same May 2026 reference period is scheduled Wednesday 08 July 2026 at 11:30am AEST."},{"kind":"tool","tool":"official.lookup","call":"ABS April 2026 Building Approvals latest release key statistics and table","result":"Fetched April 2026 first-print context: total dwelling units approved fell 3.4% to 16,710; private sector houses fell 1.0% to 10,088; private sector dwellings excluding houses fell 3.6% to 6,403; trend total dwelling units were 17,363 with 0.0% monthly change."},{"kind":"tool","tool":"official.lookup","call":"ABS March 2026 Building Approvals release","result":"Fetched March 2026 first-print context: total dwellings approved fell 10.5% to 17,300; private sector dwellings excluding houses fell 26.0% to 6,632; private sector houses rose 0.9% to 10,194; trend total dwellings were 17,657 with 0.5% monthly change."},{"kind":"tool","tool":"official.lookup","call":"ABS February and January 2026 Building Approvals releases","result":"Fetched February 2026 total dwellings approved rose 29.7% to 19,022 and trend rose 1.2% to 17,566; fetched January 2026 total dwellings approved fell 7.2% to 14,564 and trend was 16,386 with -0.1% monthly change."},{"kind":"text","text":"Base-rate/reference-class anchor: recent first prints show very high realized monthly dispersion, with January -7.2, February +29.7, March -10.5, and April -3.4. The central tendency is closer to low positive or flat than to the extreme February rebound."},{"kind":"text","text":"Level and momentum split: the April level of 16,710 was about 3.8% below the April trend level of 17,363, so I allow a modest bounce. Momentum is negative over March-April, so the bounce should be smaller than the February spike."},{"kind":"text","text":"Mechanism split: detached houses were comparatively stable while multi-unit approvals drove the big 2026 swings. Policy pressure to lift housing supply is an upside force, but financing, construction costs, and project feasibility keep the near-term print noisy rather than persistently strong."},{"kind":"math","text":"Point: start from a flat-to-slightly-positive base rate near +0.5%, add about +2.0 percentage points for mean reversion from April being 3.8% below trend, subtract about -0.5 percentage points for weak March-April momentum, giving +2.0%. Interval: recent monthly changes span roughly -10.5% to +29.7%; for an 80% first-print interval, use about -12/+14 percentage points around the point, skewed upward for apartment-project lumpiness, giving -10.0% to +16.0%."},{"kind":"text","text":"Counter-consideration and scenarios: downside outside the interval would be another large apartment-project drop or delayed approvals pushing the print below -10.0%; upside outside the interval would be a renewed multi-unit approval surge like February, above +16.0%; the central case is a partial rebound with no repeat of February's one-off jump."},{"kind":"forecast","point":2.0,"ciLow":-10.0,"ciHigh":16.0}]}
