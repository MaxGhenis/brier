# Census SPM workbook fixtures

These are byte-for-byte copies of official Census Table B-2 workbooks. They
exercise the parser against two real P60 layouts and pin the legacy transition
values that must not arm the corrected-methodology adapter.

| Fixture | Official source | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `p60-283-tableB-2.xlsx` | [P60-283 Table B-2](https://www2.census.gov/programs-surveys/demo/tables/p60/283/tableB-2.xlsx) | 41,756 | `c5938c06302e547583d35fc8d1480b6b726b288501c46b99d5965f517b4a245e` |
| `p60-287-tableB-2.xlsx` | [P60-287 Table B-2](https://www2.census.gov/programs-surveys/demo/tables/p60/287/tableB-2.xlsx) | 43,484 | `8cdb688380c543c1bd3bc47e2124ec6872511eff8c03c8340b1adacdbd1525fe` |

Both vintages contain two ALL RACES rows labeled 2019. The row whose footnote
states that it implements revised Supplemental Poverty Measure methodology has
the child rate 12.6%; the plain earlier-methodology row has 12.5%. The parser
must authenticate that footnote before choosing between them. Both workbooks
also report 9.7% for 2020.

These historical values are rejection evidence, not the corrected 2019–2024
anchors promised by Census in 2026. The production adapter remains
`PENDING_REVISED_PRINT` until an integrator records all six corrected official
prints, with 2019 and 2020 values that discriminate them from these legacy
vintages.
