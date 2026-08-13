# FSA CRP source-recovery fixtures

These are byte-for-byte responses fetched from the official USDA Farm Service
Agency site on 2026-08-13 at 18:06 UTC. They archive the recovered three-hop
publication chain used by the `fsa-crp-monthly-summary` adapter: statistics
landing page, dated document page, and Monthly Summary PDF.

| Fixture | Official URL | HTTP result / vintage | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `recovery_2026_08_13/stale-statistics-301.html` | `https://www.fsa.usda.gov/resources/programs/conservation-reserve-program/statistics` | 301 to the recovered landing path; response body archived without following the redirect | 470 | `4187ac28fa28499314920d3beb9cd5774b51727bbbefa888a972328c96616a91` |
| `recovery_2026_08_13/crp-statistics.html` | `https://www.fsa.usda.gov/tools/informational/reports/conservation-statistics/crp` | 200; HTTP Last-Modified 2026-08-13 17:46:12 GMT | 121,040 | `f0e572b484359368042634d7413937acd174d53434667f55b092382b8a73c181` |
| `recovery_2026_08_13/april-2026-document.html` | `https://www.fsa.usda.gov/documents/april-2026-crp-monthly-summary` | 200; HTTP Last-Modified 2026-08-13 17:56:53 GMT | 62,639 | `6b076bd7e94e13bc3d32ddf9663c80201c2c94f6a1c3eebf6ce4a5ce064df695` |
| `recovery_2026_08_13/CRPMonthlyApril2026WithPageNumbers.pdf` | `https://www.fsa.usda.gov/sites/default/files/2026-07/CRPMonthlyApril2026WithPageNumbers.pdf` | 200; April 2026 observation vintage; HTTP Last-Modified 2026-07-16 21:14:44 GMT | 5,356,828 | `03ac66bd80f263cdaa221295eb17963fbb9be0574b846fd11f6024ca0ee4e373` |

The PDF identifies itself as `MONTHLY SUMMARY – APRIL 2026`, says its tables
use CRP contract data through the end of April 2026, and prints Total CRP acres
of 26,182,019. Its embedded metadata records creation on 2026-07-15 and
modification on 2026-07-16. The `/2026-07/` storage path is a publication
vintage, not the observation month.

The stale URL is evidence of recovery and lineage, not an accepted adapter
entry point. Production resolution must begin at the exact recovered landing
URL and refuses redirects and unreviewed same-host paths.
