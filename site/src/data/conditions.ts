// Typed condition registry for conditional forecast cells (review
// finding F6). A conditional cell's branch is graded ONLY when its
// registered condition is "satisfied": the same official print resolves
// both branches of a pair, and grading an unmet branch would score the
// wrong hypothesis. Status transitions happen here, in normal commits,
// with evidence — auditable like everything else.

export type ConditionStatus = "open" | "satisfied" | "failed";

export interface ConditionDefinition {
  conditionId: string;
  description: string;
  // The exact conditionalOn strings recorded on published cells. Cells
  // bind to conditions through these recorded contracts, so generated
  // wave modules never need editing.
  matchStrings: string[];
  status: ConditionStatus;
  resolvesBy: string;
  complementOf?: string;
  evidenceUrl?: string;
  note?: string;
}

export const CONDITIONS: ConditionDefinition[] = [
  {
    conditionId: "cond.medicaid-work-req-deadline.holds",
    description:
      "The 2025 reconciliation law's Medicaid community-engagement " +
      "compliance deadline takes effect on its statutory schedule, with " +
      "no federal statutory or regulatory delay announced by 2027-03-31.",
    matchStrings: [
      "The 2025 reconciliation law's Medicaid community-engagement compliance deadline takes effect on its statutory schedule, with no federal statutory or regulatory delay announced by 2027-03-31.",
      "Medicaid community-engagement compliance deadline (2026-12-31) in effect — no statutory delay or nationwide stay as of 2027-03-31",
    ],
    status: "open",
    resolvesBy: "2027-03-31",
    complementOf: "cond.medicaid-work-req-deadline.delayed",
  },
  {
    conditionId: "cond.medicaid-work-req-deadline.delayed",
    description:
      "A federal statutory or regulatory delay of the Medicaid " +
      "community-engagement compliance deadline is announced on or " +
      "before 2027-03-31, pushing the effective date beyond April 2027.",
    matchStrings: [
      "A federal statutory or regulatory delay of the 2025 reconciliation law's Medicaid community-engagement compliance deadline is announced on or before 2027-03-31, pushing the effective date beyond April 2027.",
      "Medicaid community-engagement compliance deadline delayed beyond 2027 by statute or nationwide stay on or before 2027-03-31",
    ],
    status: "open",
    resolvesBy: "2027-03-31",
    complementOf: "cond.medicaid-work-req-deadline.holds",
  },
  {
    conditionId: "cond.ca-ex-parte-share-aug-2026.gte-80",
    description:
      "California ex parte renewal share at or above 80% in the August " +
      "2026 reporting period.",
    matchStrings: [
      "California ex parte renewal share at or above 80% in the August 2026 reporting period",
    ],
    status: "open",
    resolvesBy: "2026-12-31",
  },
  {
    conditionId: "cond.snap-cost-share.in-effect",
    description:
      "SNAP state cost-share provision in effect (no repeal or delay " +
      "enacted) through 2027-06-30.",
    matchStrings: [
      "SNAP state cost-share provision in effect (no repeal or delay enacted) through 2027-06-30",
    ],
    status: "open",
    resolvesBy: "2027-06-30",
    complementOf: "cond.snap-cost-share.repealed",
  },
  {
    conditionId: "cond.snap-cost-share.repealed",
    description:
      "SNAP state cost-share provision repealed or delayed by statute " +
      "enacted on or before 2027-06-30.",
    matchStrings: [
      "SNAP state cost-share provision repealed or delayed by statute enacted on or before 2027-06-30",
    ],
    status: "open",
    resolvesBy: "2027-06-30",
    complementOf: "cond.snap-cost-share.in-effect",
  },
  {
    conditionId: "cond.ctc-3000-refundable-ty2026.enacted",
    description:
      "A $3,000 fully refundable Child Tax Credit (or materially " +
      "equivalent) in effect for tax year 2026.",
    matchStrings: [
      "$3,000 fully refundable Child Tax Credit in effect for TY2026",
      "$3,000 fully refundable Child Tax Credit in effect for tax year 2026",
    ],
    status: "open",
    resolvesBy: "2026-12-31",
    complementOf: "cond.ctc-3000-refundable-ty2026.absent",
    note:
      "Enacted TY2026 law (OBBBA) sets a $2,200 CTC; retroactive change " +
      "remains possible until the tax year closes, so the window stays open.",
  },
  {
    conditionId: "cond.ctc-3000-refundable-ty2026.absent",
    description:
      "No materially equivalent $3,000 fully refundable Child Tax " +
      "Credit in effect for tax year 2026.",
    matchStrings: [
      "No materially equivalent $3,000 fully refundable Child Tax Credit in effect for TY2026",
    ],
    status: "open",
    resolvesBy: "2026-12-31",
    complementOf: "cond.ctc-3000-refundable-ty2026.enacted",
  },
  {
    conditionId: "cond.tcja-extension-house-framework.enacted",
    description:
      "TCJA extension package matching the House framework enacted by " +
      "2026-06-30.",
    matchStrings: [
      "TCJA extension package matching House framework enacted by 2026-06-30",
    ],
    status: "satisfied",
    resolvesBy: "2026-06-30",
    evidenceUrl: "https://www.congress.gov/bill/119th-congress/house-bill/1",
    note:
      "The 2025 reconciliation act extended the TCJA individual " +
      "provisions per the House framework, enacted well before the " +
      "2026-06-30 window closed.",
  },
  {
    conditionId: "cond.aca-enhanced-ptc.expired-through-2028",
    description:
      "Enhanced ACA premium tax credits remain expired through the end " +
      "of 2028.",
    matchStrings: [
      "Enhanced ACA premium tax credits remain expired through end of 2028",
    ],
    status: "open",
    resolvesBy: "2028-12-31",
  },
  {
    conditionId: "cond.salt-cap.eliminated-ty2026",
    description:
      "IRC §164(b)(6) SALT cap fully eliminated for TY2026 and later.",
    matchStrings: [
      "IRC §164(b)(6) SALT cap fully eliminated for TY2026 and later",
    ],
    status: "open",
    resolvesBy: "2026-12-31",
    note:
      "Enacted TY2026 law raises but does not eliminate the cap; the " +
      "window stays open until the tax year closes.",
  },
];

const BY_MATCH_STRING = new Map<string, ConditionDefinition>(
  CONDITIONS.flatMap((condition) =>
    condition.matchStrings.map((text) => [text, condition]),
  ),
);

// Two early published cells embed their contingency in the question text
// instead of a conditionalOn field; their generated modules are immutable,
// so they bind here by slug. New conditionals must carry conditionalOn.
const LEGACY_SLUG_BINDINGS: Record<string, string> = {
  "ca-medicaid-enrollment-50-64-april-2027-work-req-deadline-holds":
    "cond.medicaid-work-req-deadline.holds",
  "medicaid-enrollment-april-2027-work-req-deadline-delayed":
    "cond.medicaid-work-req-deadline.delayed",
};

const BY_ID = new Map(
  CONDITIONS.map((condition) => [condition.conditionId, condition]),
);

export function conditionForCell(cell: {
  slug: string;
  conditionalOn?: string;
}): ConditionDefinition | undefined {
  return (
    conditionForContract(cell.conditionalOn) ??
    BY_ID.get(LEGACY_SLUG_BINDINGS[cell.slug] ?? "")
  );
}

export function conditionForContract(
  conditionalOn: string | undefined,
): ConditionDefinition | undefined {
  if (!conditionalOn) return undefined;
  return BY_MATCH_STRING.get(conditionalOn.trim());
}

export function conditionStatusFor(
  cell: { slug: string; conditionalOn?: string },
  overrides?: Map<string, ConditionStatus>,
): ConditionStatus | "unregistered" {
  const condition = conditionForCell(cell);
  if (!condition) return "unregistered";
  return overrides?.get(condition.conditionId) ?? condition.status;
}
