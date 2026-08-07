# BEA current-release resolver fixtures

Fetched unmodified from the official BEA hosts on 2026-08-07 UTC, while the
2026 Q2 advance estimate was still the current GDP print and before the second
estimate scheduled for 2026-08-26. These are parser fixtures, not a claim that
Thesis witnessed the files on their 2026-07-30 release day.

- `gdp-advance-2026-q2.html`: GET
  `https://www.bea.gov/news/2026/gdp-advance-estimate-2nd-quarter-2026`;
  52,640 bytes; SHA-256
  `4636dc341d7cd1a53196fdf0ad529143b0e8b2d0db874f6086ca9b8ebf23cf5d`.
- `nipa-table-5-3-5-2026-q2.json`: POST (raw double-encoded response: a JSON string wrapping the object)
  `https://apps.bea.gov/iTablecore/data/app/GetStep` with app 19, step 3,
  category `Survey`, table key `145`, first/last year `2026`, scale `-6`,
  series `Q`, and select-all-years `0`; 46,905 bytes; SHA-256
  `59e5f1ab0eeaa76cdca566383c66eab7787214216ffcbe35aa4c1793a894750d`.

The response prints 2026 Q2 in millions at 4,623,657 on Table 5.3.5 line 2
(`Nonresidential`) and 937,772 on line 18 (`Research and development`), which
the registered 0.001 transform converts to 4,623.657 and 937.772 USD billions.
The resolver archives both fetched responses together; ALFRED remains only the
dated-vintage mirror used for history and anchor pins.
