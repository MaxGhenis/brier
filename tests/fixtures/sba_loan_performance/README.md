# SBA Loan Program Performance PDF fixtures

These are the three real PDF members extracted from the official SBA bundle
linked on 2026-08-07 by:

`https://www.sba.gov/document/report-small-business-administration-loan-program-performance`

The page redirected to `legacy.sba.gov` and linked
`https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip`.
That ZIP was 1,296,419 bytes with SHA-256
`51d5571d03d028d5efd4b8b9c8d7984f55285d36202eb8f67afe8a3476bb1242`.
The tests pin each extracted member's byte length and SHA-256 independently.

- `WDS_ChargeOffAmount_Report_20250630.pdf`: 107,076 bytes;
  `b3f352425adcc3304cbcc406d63a2ced149bc8224f3b604c2b47403edc9070f3`.
- `WDS_ChargeOffRates_Report_20250630.pdf`: 167,134 bytes;
  `23ab3dc1d37dc08be200b8076d07371b1ac901730e1828a697278bf279a1d762`.
- `WDS_PostChargeOffRecovery_Report_20250630.pdf`: 109,817 bytes;
  `09616e8af327a6ea8e3bbc340e44392bbead98e581a9f85a7de99ef8b81e380f`.

These files are parser anchors only. They are not witnessed captures, do not
establish when any value first appeared, and must never be used as resolution
evidence. Admissibility requires the dedicated custody run and externally
witnessed first-print selection defined in
`docs/lanes/2026-08-07-sba-pdf-custody-family.md`.

`adversarial-ungridded.pdf.b64` is Sol's 2,481-byte synthetic negative probe,
stored as base64 so its four non-UTF-8 PDF-comment bytes can remain exact in a
text fixture. The decoded SHA-256 is
`5c8a3b33d13154b13c66a102490db767780f4f603ed3e7bb2f8621c674a442dd`.
It reproduces the reviewed attack: all required words and an FY2024 value of
`$999,999,999` appear as untagged text at one x-coordinate, with no table grid.
It is not an official SBA artifact and must be rejected before value parsing.
