import { WITNESSED_CUSTODY_ROOTS } from "./witnessed-timeline.generated";

// Publication proof for the headline chronology tier (re-audit N1): a claimed
// runAt is testimony, not evidence. Proof is a custody root that the public
// record chain committed and an RFC 3161 TSA externally witnessed BEFORE the
// outcome was observable, with a custody inventory the verifier judged
// complete and headline eligible. The witnessed timeline
// (records/witnessed-timeline.json, extracted by scripts/witnessed_timeline.py
// from the verified chain) is the only source of that proof; absence from the
// timeline is unproven chronology, never a pass.

export interface WitnessedCustodyRootProof {
  coverage: "direct" | "transitive";
  custodyInventoryVersion: number;
  earliestWitnessedAt: string;
  headlineEligible: boolean;
  inventoryStatus: string;
  tsaGenTime: string;
  witnessDigest: string;
}

export type WitnessedCustodyRootMap = Record<string, WitnessedCustodyRootProof>;

export { WITNESSED_CUSTODY_ROOTS };

export type PublicationProofStatus =
  | "witnessed"
  | "witness_not_before_observation"
  | "root_not_headline_eligible"
  | "root_not_in_timeline"
  | "no_custody_root";

export interface ScoreChronologyProof {
  status: PublicationProofStatus;
  custodyRootSha256: string | null;
  earliestWitnessedAt: string | null;
  inventoryStatus: string | null;
  headlineEligible: boolean | null;
  witnessDigest: string | null;
}

const DAY_PREFIX = /^\d{4}-\d{2}-\d{2}/;
const EXPLICIT_TIMEZONE = /(?:Z|[+-]\d{2}:?\d{2})$/i;

export function dayOf(timestamp: string): string | null {
  const match = DAY_PREFIX.exec(timestamp.trim());
  return match ? match[0] : null;
}

// A timestamp supports sub-day ordering only when the string pins both a
// clock time and an explicit UTC offset. Anything looser is compared at
// day granularity on the written date itself, so a verdict can never
// depend on the build host's timezone (re-audit X4 residual: timezone-less
// strings parse as local time under Date.parse).
export function explicitInstantOf(timestamp: string): number | null {
  const trimmed = timestamp.trim();
  if (!trimmed.includes("T") || !EXPLICIT_TIMEZONE.test(trimmed)) return null;
  const parsed = Date.parse(trimmed);
  return Number.isFinite(parsed) ? parsed : null;
}

export type InstantPrecedence = "before" | "not_before" | "unknown";

// Strict precedence under the same conservatism as the claimed-time gate:
// sub-day ordering needs explicit instants on both sides; otherwise compare
// written UTC dates and treat a shared day as unknowable.
export function instantPrecedence(
  left: string,
  right: string,
): InstantPrecedence {
  const leftDay = dayOf(left);
  const rightDay = dayOf(right);
  if (!leftDay || !rightDay) return "unknown";
  const leftInstant = explicitInstantOf(left);
  const rightInstant = explicitInstantOf(right);
  if (leftInstant !== null && rightInstant !== null) {
    return leftInstant < rightInstant ? "before" : "not_before";
  }
  if (leftDay < rightDay) return "before";
  if (leftDay > rightDay) return "not_before";
  return "unknown";
}

export function classifyPublicationProof(
  custodyRootSha256: string | undefined,
  observedAt: string | undefined,
  custodyRoots: WitnessedCustodyRootMap = WITNESSED_CUSTODY_ROOTS,
): ScoreChronologyProof {
  if (!custodyRootSha256) {
    return {
      status: "no_custody_root",
      custodyRootSha256: null,
      earliestWitnessedAt: null,
      inventoryStatus: null,
      headlineEligible: null,
      witnessDigest: null,
    };
  }
  const entry = Object.hasOwn(custodyRoots, custodyRootSha256)
    ? custodyRoots[custodyRootSha256]
    : undefined;
  if (!entry) {
    return {
      status: "root_not_in_timeline",
      custodyRootSha256,
      earliestWitnessedAt: null,
      inventoryStatus: null,
      headlineEligible: null,
      witnessDigest: null,
    };
  }
  const evidence = {
    custodyRootSha256,
    earliestWitnessedAt: entry.earliestWitnessedAt,
    inventoryStatus: entry.inventoryStatus,
    headlineEligible: entry.headlineEligible,
    witnessDigest: entry.witnessDigest,
  };
  // Verifier-side custody verdicts travel with the timeline row: a witness
  // proves WHEN the bytes existed, never that their inventory is complete
  // (legacy-incomplete roots stay out of the headline forever).
  if (entry.inventoryStatus !== "complete" || entry.headlineEligible !== true) {
    return { status: "root_not_headline_eligible", ...evidence };
  }
  if (
    !observedAt ||
    instantPrecedence(entry.earliestWitnessedAt, observedAt) !== "before"
  ) {
    return { status: "witness_not_before_observation", ...evidence };
  }
  return { status: "witnessed", ...evidence };
}
