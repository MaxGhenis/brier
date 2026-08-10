# International accountability ingestion wave report

Status as of 2026-08-10 UTC: the request-only Ghana and Botswana wave is
complete. It produced four ingestion requests, all with outcome `proposed`;
zero are admitted or rejected. Three requests need new adapter families and
one describes a future venue that has not published a series observation.
This wave changes no docket, adapter, site, bill, or `records/**` artifact.

## Requests and strongest captured evidence

| Request | Outcome | Strongest verification artifact captured |
|---|---|---|
| `gh-audit-service-total-irregularities.json` | Proposed | The official Ghana Audit Service 2025 MDA report PDF (14,752,705 bytes; SHA-256 `d77e10c4ac3e121cf229122548a26dc256f5c80fab0f53a8cb596c4d8841b77c`) prints `GH¢5,266,315,079` on printed page 7 (PDF page 9), confirmed by Table 1A on printed page 8. This supports a parser proposal, not first-print custody. |
| `gh-parliament-women-share.json` | Proposed | The official IPU August 2026 ranking API response (125,041 bytes; SHA-256 `6027740af2a2051144c6d9fba107db43d68f2926e939d8739d6dbb98190573ab`) prints 276 filled seats, 40 women, and `14.5` percent for Ghana. The all-seat share is accountability context, not itself Act 1121's statutory compliance denominator. |
| `gh-vfm-office-certificates.json` | Proposed | The official 2026 Mid-Year Fiscal Policy Review PDF (39,059,132 bytes; SHA-256 `a2b649a817384e071b24daec4105736bcf8384e1320b0e6dd6170c3aa710e784`) prints `MoF will fully operationalise the Value for Money Office.` with target date `End-June 2027` in Table 6, item 19. It prints no certificate count and establishes no recurring VfM Office venue. |
| `bw-old-age-pension-monthly-amount.json` | Proposed | The official Botswana 2025 Budget Speech PDF (397,982 bytes; SHA-256 `a16fa9f07caf3048a6ecd4fd19ab0ef5f032cb381446e71f83624edd321090ed`) prints an increase from `P830.00` to `P1400.00` effective `1st April 2025` in paragraph 95. This supports a budget-print parser proposal, not authenticated first-print custody. |

## Counts and open questions

- Requests: 4. Outcomes: 4 proposed, 0 admitted, 0 rejected.
- Existing official venues needing reviewed adapters and release-time custody:
  `gh-audit-annual-report-pdf`, `ipu-parline`, and `bw-budget-print`.
- Future venues: 1. The Value for Money Office has no captured recurring
  reporting product or certificates-issued observation, so no adapter family
  is claimed for it.
- `GHS` and `BWP` are absent from the current site `Unit` union. Registration
  must address those units; this does not block the draft requests.
- The reserved bill slugs `gh-vfm-office-act-2026`,
  `gh-act-1121-affirmative-action`, and `bw-udc-pension-promise` have no
  `bills/` entries yet. The first slug is referenced by two requests.
- A future VfM implementation target cannot use “operational by 2027-06-30”
  until registration chooses one exact official resolution signal. A
  commencement instrument and a first issued certificate are distinct events;
  neither has been selected or observed here.

The captured current artifacts demonstrate parseable evidence only. They do
not authenticate release-time first prints, establish reviewed adapters, or
admit any series.
