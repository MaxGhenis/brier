# Skill: Axiom — encoded-law references for policy conditionals

Axiom is a separate open project that encodes statutes as executable
rules-as-code. Thesis uses it as a tool: when a cell conditions on a policy
state, the conditioning event should reference the encoded provision so the
condition is checkable, not a vibe about "the policy."

## Current integration (interim)
Axiom's public query API is not yet wired into this pipeline. Until it is:
- Reference provisions by citation in `conditional_on` (e.g. "the 2025
  reconciliation law's Medicaid community-engagement compliance deadline,
  §71119; in effect = no enacted statutory delay and no nationwide stay by
  <date>").
- Verify the CURRENT state of the provision this run: enacted text
  (congress.gov / uscode.house.gov), implementing guidance (agency site),
  and litigation posture (CourtListener/ECF, KFF or Georgetown CCF trackers
  for health provisions). Cite what you fetched.
- Where the provision sets a numeric parameter (a deadline, a matching
  rate, an error-rate threshold), quote the enacted number with its
  citation — never from memory.

## When the API lands
`axiom.query(<provision-ref>)` will return the encoded parameter values and
effective dates; conditional cells should then carry the provision ref in
`conditional_on` verbatim so resolution can evaluate the condition
mechanically. Keep citations in the same format now so cells upgrade
cleanly.
