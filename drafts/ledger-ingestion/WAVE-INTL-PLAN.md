# International accountability wave — Ghana + Botswana (2026-08-08)

Max's directive: pipe the accountability-docket candidates end to end,
starting with ingestion requests. This wave = REQUESTS ONLY (drafts/
ledger-ingestion/*.json + this plan), wave-1 discipline: every claim in
a verification block comes from a REAL fetch performed this session
(sha256 + byteLength + printed values verbatim); honest outcomes
(these are all NEW adapter families / venues → outcome "proposed"
unless an existing family genuinely covers one); no records/**, no
docket edits, no adapter code, no site code in this wave.

Before item 1: read TWO existing drafts to mirror the schema exactly —
one verified (drafts/ledger-ingestion/irs-actc-total-credit-amount.json)
and one proposed (drafts/ledger-ingestion/
sba-disaster-physical-loans-approved-amount-14001-50000.json). Check
tests/ for any validator that sweeps drafts/ledger-ingestion/*.json
globs (wave-1's test parametrizes NAMED files only — confirm) so new
files don't break CI.

Work items (one per session; mark [x] when the request file is written
and self-consistent):

- [x] 1. gh-audit-service-total-irregularities.json —
  concept gh.audit_service.annual_report.total_irregularities, unit
  GHS (record the printed cedi total; note the site Unit union may need
  a GHS entry at registration time — that is a registration concern,
  not a blocker here), cadence annual. Venue: Ghana Audit Service
  published annual reports (https://ghaudit.org — find the latest
  Consolidated/MDAs annual report PDF actually fetchable; record the
  exact report title, fetch the PDF, sha256+bytes, extract the printed
  TOTAL irregularities figure for the most recent audited year
  verbatim, with page number). proposedFrom: gh-vfm-office-act-2026
  (slug reserved for a future bills/ entry — none exists yet; say so
  in the note). Adapter family: "gh-audit-annual-report-pdf" (new;
  one-shot annual PDFs — closer to irs-soi workbook custody than the
  rolling SBA family; requiredWork should say a reviewed PDF parser +
  capture custody are prerequisites, mirroring the original SBA
  proposed drafts).

- [x] 2. gh-parliament-women-share.json — concept
  gh.parliament.women_share, unit percent, cadence irregular
  (election-driven; treat as annual-with-election-resolution and note
  it). Venue: IPU Parline (https://data.ipu.org/parliament/GH — find
  the machine-readable endpoint; the IPU monthly ranking page also
  works). Fetch the CURRENT official IPU figure for Ghana (seats,
  women, %), record URL + sha256 of the fetched body + the printed
  values. proposedFrom: gh-act-1121-affirmative-action (reserved slug,
  no bills/ entry yet — say so). Statutory anchor: Act 1121's stepped
  quota targets — capture the most authoritative Act text you can
  actually fetch (try official/primary first: parliament.gh, mogcsp,
  ghanalegal; the ACEPA brochure
  https://acepa-africa.org/wp-content/uploads/2025/12/Afirmative-Action-Brochure-Final.pdf
  is an acceptable SECONDARY witness — label whatever you get honestly
  as primary/secondary) and record the exact quota schedule wording
  (public sources disagree 2030 vs 2034 — quote what the captured text
  actually says, flag the discrepancy if unresolved).

- [x] 3. gh-vfm-office-certificates.json — concept
  gh.vfm_office.certificates_issued (count, annual), the VfM Office's
  own reporting once it exists. This is a FUTURE-VENUE request: no
  print exists yet. Verify what CAN be verified today: the Act's
  passage/assent dates from an official or high-quality source; the
  operationalization commitment (2026 Mid-Year Fiscal Policy Review
  target of full operation by end-June 2027 — fetch the MoF mid-year
  review PDF from mofep.gov.gh if reachable and cite the page, else
  record the best secondary and label it). Note the implementation-
  milestone question ("operational by 2027-06-30") as a candidate
  policy-state target with the resolution-signal problem stated
  honestly (needs a defined official signal: commencement instrument
  or first certificate).

- [x] 4. bw-old-age-pension-monthly-amount.json — concept
  bw.gov.old_age_pension.monthly_amount, unit BWP, cadence annual
  (budget-driven). Venue: Botswana official prints — the DailyNews
  announcement (https://dailynews.gov.bw/news-detail/84506) and the
  gov.bw allowances page (https://www.gov.bw/allowances/old-age-pension-allowance);
  the 2025/26 Budget Speech PDF from finance.gov.bw if fetchable.
  Fetch what is reachable, record sha256+bytes+printed amounts (P830
  prior, P1,400 effective 2025-04-01), and the UDC P1,800 manifesto
  promise (dumaboko.com/social-advancement as the promise source —
  a party site, label it as such; the accountability target is
  "does a future budget print reach P1,800"). proposedFrom:
  bw-udc-pension-promise (reserved slug, no bills/ entry yet).

- [ ] 5. WAVE-INTL-REPORT.md — a short report in the same directory:
  table of the four requests, outcomes (all proposed expected),
  per-request the strongest verification artifact captured, open
  questions (GHS/BWP units in the site Unit union; bills/ entries for
  the three reserved slugs; adapter families needed:
  gh-audit-annual-report-pdf, ipu-parline, bw-budget-print;
  the VfM commencement-signal question). Honest counts; no
  overclaiming.

Print exactly "INTL-STEP-DONE: <item>" after completing one item, or
"INTL-ALL-DONE" when every box is checked.
