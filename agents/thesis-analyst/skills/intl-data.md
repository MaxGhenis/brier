# Skill: international statistical data — sources and calendars

## United Kingdom
- ONS series + release calendar: `https://www.ons.gov.uk/releasecalendar`
  CPI annual rate series D7G7 (CPIH L55O); monthly bulletin page carries the
  first print. ONS API: `https://api.ons.gov.uk/timeseries/<id>/dataset/mm23/data`.
- Bank Rate: `https://www.bankofengland.co.uk/monetary-policy` — MPC decision
  dates published in advance; the resolvable number is Bank Rate after the
  announcement.

## Canada
- Statistics Canada The Daily (first prints + schedule):
  `https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/schedule-horaire-eng.htm`
  CPI YoY headline from The Daily CPI release (table 18-10-0004).

## Japan
- Statistics Bureau CPI (e-Stat): national CPI ex fresh food ("core") YoY,
  released ~the 3rd Friday; schedule at
  `https://www.stat.go.jp/english/data/cpi/`.

## Euro area
- Eurostat flash HICP: ~1st of the following month;
  `https://ec.europa.eu/eurostat/web/euro-indicators/release-calendar`.

## Australia
- ABS monthly CPI indicator: `https://www.abs.gov.au/release-calendar`
  (YoY, first print in the monthly release).

## Gotchas
- Each agency's first print is the resolver; later vintages are irrelevant.
- Time zones: for release-calendar targets, resolutionDate is the local
  release date. Resolve-by-bound targets use the registered Thesis
  lab-committed outer bound; their announcement does not establish the bound
  or window.
- UK/EA prints publish to one decimal; Canada to one decimal; match precision.
