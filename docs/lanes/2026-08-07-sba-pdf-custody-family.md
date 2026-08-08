# SBA Loan Program Performance PDF custody family

## Status and scope

This note defines the custody contract for the three annual Disaster program
series ranked first in the [wave-1 next-work list](../../drafts/ledger-ingestion/WAVE1-REPORT.md):

- `sba.disaster.loan_program.charge_off_amount` (USD);
- `sba.disaster.loan_program.charge_off_rate_upb` (percent); and
- `sba.disaster.loan_program.post_charge_off_recovery` (USD).

All three provide context for `stress-119hr1021ih`. This is a design decision,
not a series admission. The family remains ineligible for the registry until
the capture path described below has produced a custody-rooted run that the
verified record timeline shows as externally witnessed.

For this family, **first print means the earliest externally witnessed,
hash-pinned capture whose archived SBA bundle strictly parses the requested
completed fiscal-year cell**. It does not mean the SBA's historically first
publication unless Thesis actually witnessed that publication. This narrower
definition must appear in the series and observation provenance.

## Official source and exact cells

The authoritative entry point is:

`https://www.sba.gov/document/report-small-business-administration-loan-program-performance`

On the 2026-08-07 live check, that URL redirected to:

`https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance`

The final page exposed exactly one download, a relative link whose working
absolute URL was:

`https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip`

The corresponding `www.sba.gov` asset URL returned HTTP 404. The legacy asset
returned HTTP 200 with 1,296,419 bytes, ETag
`"13c823-63edafb473b30"`, Last-Modified `2025-09-15T18:14:59Z`, and SHA-256
`51d5571d03d028d5efd4b8b9c8d7984f55285d36202eb8f67afe8a3476bb1242`.
The byte hash matches the independent wave-1 fetch on 2026-08-06.

The current bundle is FY2025 Q3, with data through 2025-06-30. The requested
anchor cells are completed FY2024 values; the FY2025 column is a partial-year
column and is not an admissible FY2025 annual observation.

| Series | ZIP member and SHA-256 | Exact cell | Current printed value |
|---|---|---|---:|
| Charge-off amount | `WebsiteReports_FY25Q3/WDS_ChargeOffAmount_Report_20250630.pdf`; `b3f352425adcc3304cbcc406d63a2ced149bc8224f3b604c2b47403edc9070f3` | Page 1, `Table 5 - Charge Off Amount by Program`, section/row `Disaster` / `Disaster`, column `Fiscal Year 2024` | `$299,971,326` |
| Charge-off rate / UPB | `WebsiteReports_FY25Q3/WDS_ChargeOffRates_Report_20250630.pdf`; `23ab3dc1d37dc08be200b8076d07371b1ac901730e1828a697278bf279a1d762` | Page 1, `Table 9 - Charge Off Rates as a Percent of Unpaid Principal Balance (UPB) Amount by Program`, section/row `Disaster` / `Disaster`, column `Fiscal Year 2024` | `3.06%` |
| Post-charge-off recovery | `WebsiteReports_FY25Q3/WDS_PostChargeOffRecovery_Report_20250630.pdf`; `09616e8af327a6ea8e3bbc340e44392bbead98e581a9f85a7de99ef8b81e380f` | Page 1, `Table 7 - Post-Charge Off Recovery Amount by Program`, section/row `Disaster` / `Disaster`, column `Fiscal Year 2024` | `$126,510,000` |

These values and hashes reproduce the three request artifacts. They are parser
anchors only; neither the request JSON nor a test fixture is custody evidence.

## Observed revision behavior

The live surface has all the properties of a rolling, revisable product:

- The landing page exposes one current ZIP and no historical versions.
- Each table carries ten fiscal-year columns, so later bundles replace the
  displayed history rather than adding an immutable annual artifact.
- Table 5 says charge-off amounts for a fiscal year may be adjusted because of
  data updates.
- Table 9 says prior-fiscal-year rates are updated when charge-off amounts
  change.
- Table 7 says post-charge-off recovery amounts for a fiscal year may be
  adjusted because of data updates.
- The page describes January, April, and July quarter-end releases, but the
  live FY2025 Q3 bundle was last updated on September 15, 2025. Those nominal
  months are not an exact release calendar or a safe polling schedule.

The unchanged 2026-08-06 and 2026-08-07 hashes establish only one day of
stability. The live page supplies no older official bytes from which to measure
a historical numeric revision. Last-Modified, ETag, ZIP timestamps, and PDF
metadata are useful diagnostics, but none independently authenticates when a
particular value first appeared.

It is therefore impossible to establish the actual first publication of the
FY2024 cells retroactively. Freezing today's files in parser fixtures will not
repair that gap. A later witness of today's bundle would prove only that these
bytes existed no later than that witness time.

## Capture and custody contract

The capture implementation must use a dedicated SBA run schema and custody
mode, rather than treating the ZIP as a generic `--extra` on
[`witness_upstream_ledger.py`](../../scripts/witness_upstream_ledger.py).
Generic extras preserve bytes but do not enforce the SBA page-to-asset
relationship, required member set, or parser identity.

Each attempt lives permanently at
`records/YYYY-MM-DD/<utc-stamp>-sba-pdf-witness/`, uses
`schemaVersion: thesis_sba_pdf_witness_run_v1` and
`runMode: sba_pdf_witness`, and contains `manifest.json`,
`custody_root.json`, and a structured fetch-event artifact. Successful changed
or bootstrap attempts retain the landing-page and ZIP bytes under that run
directory. A successfully fetched ZIP reached through a recognized SBA bundle
link retains those bytes and its filename-derived period coverage even when
strict bundle or PDF validation fails. The timestamp in the path is
organizational metadata, not the trusted clock.

Each never-overwritten capture run must:

1. Fetch the exact authoritative entry URL. It must archive the response body
   when one is received and a structured fetch event containing the requested
   URL, redirect chain, final URL, status, content type, response headers, and
   fetch outcome. Retained headers are limited to `Date`, `Location`,
   `Content-Type`, `Content-Length`, `ETag`, and `Last-Modified`. HTTPS is
   mandatory, and every landing-page redirect hop and the final page must remain
   on `www.sba.gov` or `legacy.sba.gov`.
2. Resolve the download from that archived page. The final asset must be HTTPS,
   every asset redirect hop must remain on `www.sba.gov` or `legacy.sba.gov`,
   and the final asset must be linked by that page; a guessed URL, search
   result, mirror, or operator-supplied local file is not admissible.
3. Require HTTP 200 and ZIP bytes, then archive the exact ZIP. The manifest must
   record raw and deterministic-gzip SHA-256 and byte length.
4. Inventory every ZIP member and record its path, uncompressed size, and
   SHA-256. It must reject duplicate paths, traversal paths, encrypted members,
   malformed ZIPs, and duplicate or missing required report members.
5. Record the bundle label and report as-of date derived from strict report
   content, not merely from the URL or HTTP headers. Parsed cells are useful
   audit output, but the archived bytes remain the authority and must replay.
   Parser contract v2 requires the exact page and crop bounds, only reviewed
   full-page clipping paths, reviewed light table backgrounds, the opaque gray
   table-grid paint phase, and exactly one black tagged token in every aligned
   header/value cell for all ten year labels and all ten `Disaster` values. It
   rejects annotations, optional content, transparency groups, and any path,
   image, or shading that could paint over the grid or text. The parser maps a
   value to a year through the shared geometric column, never through
   whitespace-token position.
6. Seal the exact run inventory in `custody_root.json`, write the manifest once
   with its custody-root hash, and immediately pass `verify_custody.py`. The
   dedicated verifier must enforce artifact cardinality, paths, URLs, hashes,
   sizes, and absence of unreferenced files.

Every scheduled invocation must also leave a durable, never-overwritten attempt
run, including when the asset is unchanged or the fetch fails. Its outcome is
one of `bootstrap`, `changed`, `unchanged`, or `failed`. A bootstrap or changed
attempt contains the complete page and ZIP archives above. An unchanged attempt
contains the fresh structured fetch event, the observed full-byte hash and
size, and an exact custody-root/hash reference to the prior complete capture.
A failed attempt contains the structured error/status/redirect evidence that
was available. When fetch and asset validation reached a recognized ZIP, it
also contains the exact ZIP and pre-parse coverage identity; that retained run
participates in earliest-capture selection so its parse failure can block a
later revision. All four outcomes are custody-rooted and enter the witnessed
record chain. This permanent attempt sequence makes a missed day or failed poll
auditable without duplicating an unchanged ZIP on every checkout.

The existing record-chain machinery then supplies the clock. A recorder digest
commits the verified custody root; [`witness_snapshot.py`](../../scripts/witness_snapshot.py)
obtains and pin-verifies RFC 3161 evidence for that digest; and
[`witnessed_timeline.py`](../../scripts/witnessed_timeline.py) exposes the
minimum verified TSA `genTime` as `earliestWitnessedAt`. A later available
witness may cover the capture transitively through the hash-linked record
chain. An unavailable witness marker supplies no time claim and makes the run
ineligible until an available successor covers it.

The capture's self-declared fetch time, server `Date`, Last-Modified, ETag, ZIP
timestamps, and PDF metadata must never substitute for the verified timeline
proof.

## First-print selection rule

For a requested series and fiscal year, the resolver must operate only on the
committed record corpus and must:

1. Verify the record chain and witnessed timeline.
2. Find dedicated SBA capture runs whose custody roots and complete inventories
   pass the current verifier and have an available direct or transitive timeline
   proof.
3. Determine coverage before parsing a value. A complete capture must expose a
   strict `WebsiteReports_FY<yy>Q<q>.zip` bundle identity and fiscal year from
   the archived page/link. For this ten-year product, a Q1-Q3 bundle's possible
   completed-year coverage is `bundleFiscalYear - 9 <= Y < bundleFiscalYear`;
   its current-year column is partial. A Q4 bundle's possible completed-year
   coverage includes `Y == bundleFiscalYear`, subject to the report's completed-
   year statement. An earlier complete capture in the applicable set may not be
   skipped merely because its internals later fail strict parsing. An
   unrecognized bundle identity is source drift and blocks selection pending
   review rather than being ignored.
4. Within the possible-coverage set, identify the minimum externally verified
   `earliestWitnessedAt` before parsing a value. Do not order captures by a
   claimed fetch time or HTTP/PDF metadata.
5. Replay every capture at that minimum witness time through the reviewed
   strict parser. A capture contains a completed period only when the requested
   report, table title, `Disaster` section and row, fiscal-year header, units,
   as-of statement, and completed-year status all validate and the exact cell
   parses. If any earliest capture fails, refuse; never fall forward to a later
   revision.
6. If distinct bundle hashes tie at the earliest witness time, accept only if
   every strictly parsed capture yields the same normalized value and unit;
   otherwise refuse as chronologically ambiguous.
7. Emit provenance containing the landing and asset URLs, ZIP and member
   hashes, custody-root hash, witness digest, TSA time, table/cell identity, and
   parser contract.

An earlier witnessed SBA capture in the deterministic possible-coverage set
that cannot pass the strict parser is a blocker, not permission to skip forward
to a later revisable bundle.

## Required resolver refusals

The resolver must fail closed, with stable literal-message prefixes suitable
for tests, for at least these states:

- `SBA CUSTODY ABSENT (refusing):` no witnessed capture establishes the period;
- `SBA CUSTODY UNWITNESSED (refusing):` matching bytes exist but have no
  available pinned-witness timeline proof;
- `SBA CUSTODY INVALID (refusing):` any archive, manifest, custody-root, URL,
  hash, size, inventory, or witness reference fails verification;
- `SBA EARLIEST CAPTURE AMBIGUOUS (refusing):` earliest externally witnessed
  candidates disagree;
- `SBA PDF LAYOUT DRIFT (refusing):` any required member, page/table identity,
  row, column, unit, completed-year marker, or unambiguous numeric cell fails
  the parser contract; and
- `SBA PERIOD PARTIAL (refusing):` the requested fiscal-year column is still
  described as quarter-to-date rather than completed.

It must never fall back to the current live ZIP, a later parseable revision,
the values copied into the request JSONs, parser fixtures, FRED, news, cached
search results, or HTTP/PDF timestamps. A period with no admissible witnessed
capture remains unresolved.

## Operational cadence and admission gate

The source has no exact-day release calendar, and the observed Q3 delay makes a
January/April/July-only job insufficient. The docket needs a daily capture
attempt, including weekends, against the exact landing page and its linked
asset. The job should run before the daily recorder and explicitly dispatch or
depend on the recorder after publishing a changed or bootstrap capture; the
current 13:40 UTC resolution job and 14:17 UTC recorder schedules are useful
backstops, not proof of ordering when hosted schedules are delayed.

That polling cadence is not evidence for `resolutionDate`. A target must not
infer a day from the nominal release months or from a previous bundle. It needs
either an official exact date under `release-calendar`, or a separately reviewed
`resolve-by-bound` registration with a lab-committed conservative
`expectedReleaseWindow` and outer deadline; in the latter case
`resolutionDate` is the window end. Without one of those registered bases, no
SBA target belongs in the forecast docket even if daily custody is operating.

Every new linked asset version must become a custody-rooted records run through
an allowlisted publisher, then receive an available record-chain witness. An
unchanged daily attempt records its fresh fetch event and prior-capture
reference but does not become another candidate. A new period or changed ZIP is
not eligible until its complete bytes are archived. Network failure, a 404, an
unlinked asset, or a missed recorder witness leaves a durable non-candidate
attempt. A recognized ZIP with layout drift is archived and, once witnessed,
advances the earliest covered-capture state as a blocking parse failure; it can
never be skipped in favor of later revised bytes.

The cadence minimizes the gap between SBA publication and Thesis custody but
does not erase it. If SBA publishes and revises between successful captures,
the intervening version is unknowable; the retained value is honestly labeled
the earliest witnessed capture, not the actual release-time first print.

As of this design note, no dedicated SBA capture exists in the witnessed
timeline. Unit 4 must therefore add no registry entries unless unit 3's
allowlisted daily capture has run, its custody inventory verifies, and an
available pinned witness covers it. Otherwise all three ingestion requests must
be left or set to `proposed` in unit 5 with this precise remaining step: **run
the official-page SBA capture through the records publisher and obtain an
available recorder-chain witness, then recheck admission**.
