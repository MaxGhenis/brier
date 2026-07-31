/**
 * Stance v1 fold (issue #43, stance micro-spec).
 *
 * Each metric may carry a stances matrix — one extraction-time
 * serves/opposes/orthogonal judgment per imputed goal, keyed by goal
 * index. The client folds the matrix over the countersign store's
 * currently-confirmed goals; judgments never change at view time.
 */

export type Stance = "serves" | "opposes" | "orthogonal";

export interface MetricStance {
  /** Index into provision.goals — stance follows goal identity, not wording. */
  goal: number;
  stance: Stance;
}

export type GoalState = "confirmed" | "struck";

export type StanceFold =
  | { kind: "serves" | "opposes" | "mixed" | "orthogonal" }
  | { kind: "counts"; serves: number; opposes: number; orthogonal: number };

/**
 * Fold a metric's stance matrix over the current goal states.
 *
 * - serves: ≥1 confirmed goal served and none opposed
 * - opposes: ≥1 confirmed goal opposed and none served
 * - mixed: both — a provision serving goal A while undercutting goal B
 * - orthogonal: otherwise
 * - zero confirmed goals → raw matrix counts, not a fake neutral
 *
 * Struck goals drop out entirely — from the confirmed fold and from the
 * zero-confirmed counts. Returns null when the metric has no matrix
 * (pre-stance artifacts render no badge).
 */
export function foldStances(
  stances: MetricStance[] | undefined,
  goalStates: Record<number, GoalState>,
): StanceFold | null {
  if (!stances || stances.length === 0) return null;

  const inForce = stances.filter((s) => goalStates[s.goal] !== "struck");
  const confirmed = inForce.filter((s) => goalStates[s.goal] === "confirmed");

  if (confirmed.length === 0) {
    return {
      kind: "counts",
      serves: inForce.filter((s) => s.stance === "serves").length,
      opposes: inForce.filter((s) => s.stance === "opposes").length,
      orthogonal: inForce.filter((s) => s.stance === "orthogonal").length,
    };
  }

  const served = confirmed.some((s) => s.stance === "serves");
  const opposed = confirmed.some((s) => s.stance === "opposes");
  if (served && opposed) return { kind: "mixed" };
  if (served) return { kind: "serves" };
  if (opposed) return { kind: "opposes" };
  return { kind: "orthogonal" };
}
