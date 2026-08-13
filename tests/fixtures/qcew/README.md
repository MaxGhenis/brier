# BLS QCEW annual child-care fixture

`child_day_care_services_2025_annual.csv` is the byte-for-byte response from
the official BLS QCEW annual industry-slice endpoint:

https://data.bls.gov/cew/data/api/2025/a/industry/624410.csv

It was fetched live on 2026-08-12 UTC. The response was 537,503 bytes and its
SHA-256 digest was
`a4ebb81ec1159b1c3faa1670a32dc77598cf51178d9e17c630cb289ea568c3a9`.
The fixture is intentionally complete: the exact US/private/NAICS 624410 row
is the final row, so truncating the response could otherwise hide the selected
row or leave only its leading fields parseable.
