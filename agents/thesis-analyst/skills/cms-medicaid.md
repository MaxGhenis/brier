# Skill: CMS Medicaid performance data

## The core dataset
"State Medicaid and CHIP Applications, Eligibility Determinations, and
Enrollment Data" — dataset id `6165f45b-ca93-5bb5-9d06-db29c692a360` on
data.medicaid.gov. Carries, monthly by state: call-center volume and average
wait, application volumes, determination timeliness, ex parte renewal
shares, procedural disenrollment shares.

- Datastore API:
  `https://data.medicaid.gov/api/1/datastore/query/6165f45b-ca93-5bb5-9d06-db29c692a360/0?limit=<n>&offset=<n>`
  (JSON; filterable). If the API resists, the dataset page lists downloadable
  distributions — use the latest and cite which.
- National figures are VOLUME-WEIGHTED across reporting jurisdictions
  (weight each state's average wait by its call volume, latest submission
  per jurisdiction) — say so in the rule and compute it that way.
- Reporting lags ~3-4 months; for release-calendar targets the resolutionDate
  is when CMS first publishes that period, not the period itself. A bounded
  target instead uses its registered outer bound.

## Reference classes for policy effects
- Arkansas 2018 work requirements: Sommers et al. (NEJM 2019/2020) —
  awareness/confusion findings, ~18k disenrolled in 2018. Use for
  calls-per-affected-enrollee and confusion-driven contact anchors.
- 2023-24 unwinding: KFF unwinding trackers + this same CMS dataset show the
  renewals→calls→wait propagation at scale; use as the elasticity anchor.
- Georgia Pathways: administrative-cost and verification-burden precedent.

## Modeling discipline
Policy effects on operational metrics decompose as:
people touched × touchpoints per period × contacts per touchpoint → Δvolume;
then a FITTED volume→wait relation from this dataset's own history (note
staffing confounds; prefer convex/queueing-shaped over linear), then an
offsetting staffing/deflection response anchored to the unwinding. Every
parameter gets a range and an anchor.
