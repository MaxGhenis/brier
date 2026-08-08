import { describe, expect, it } from "vitest";
import {
  CHALLENGE_SUBMISSIONS,
  listChallengeSubmissions,
} from "@/data/challenge";
import {
  FORECAST_CELLS,
  getForecastRunEntries,
} from "@/data/forecast-cells";
import {
  buildBrierAgentLeaderboard,
  type BrierRewardRow,
} from "@/data/brier-lab";

const externalRuns = FORECAST_CELLS.flatMap((cell) =>
  (cell.comparisonRuns ?? [])
    .filter((run) => run.externalSubmission)
    .map((run) => ({ cell, run })),
);

describe("challenge registry", () => {
  it("joins every registry row onto a real cell and run", () => {
    const views = listChallengeSubmissions();
    expect(views).toHaveLength(CHALLENGE_SUBMISSIONS.length);
    for (const view of views) {
      expect(view.cell.slug).toBe(view.cellSlug);
      expect(view.run.variantId).toBe(view.variantId);
    }
  });

  it("stays in lockstep with externally flagged comparison runs", () => {
    const registryVariantIds = new Set(
      CHALLENGE_SUBMISSIONS.map((record) => record.variantId),
    );
    const flaggedVariantIds = new Set(
      externalRuns.map(({ run }) => run.variantId),
    );
    expect(flaggedVariantIds).toEqual(registryVariantIds);
  });

  it("matches each cell's registered target and the run's claims", () => {
    for (const view of listChallengeSubmissions()) {
      expect(view.cell.dataPointId).toBe(view.dataPointId);
      expect(view.run.predictionRun.runAt).toBe(view.submittedAtUtc);
      expect(view.run.predictionRun.sourceContext ?? []).toContain(
        view.recordsDigest,
      );
      expect(view.run.externalSubmission).toEqual({
        challenger: view.challenger,
        systemType: view.systemType,
      });
    }
  });

  it("rejects registry rows that name unknown cells", () => {
    expect(() =>
      listChallengeSubmissions(
        FORECAST_CELLS.filter(
          (cell) => cell.slug !== CHALLENGE_SUBMISSIONS[0].cellSlug,
        ),
      ),
    ).toThrow(/unknown cell slug/);
  });
});

describe("external attribution propagation", () => {
  it("copies externalSubmission onto run entries", () => {
    for (const { cell, run } of externalRuns) {
      const entries = getForecastRunEntries(cell);
      const entry = entries.find(
        (candidate) => candidate.variantId === run.variantId,
      );
      expect(entry?.externalSubmission).toEqual(run.externalSubmission);
      const primary = entries.find((candidate) => candidate.isPrimary);
      expect(primary?.externalSubmission).toBeUndefined();
    }
  });

  it("marks leaderboard groups external only when every row is", () => {
    const base = (
      overrides: Partial<BrierRewardRow> & { runId: string },
    ): BrierRewardRow =>
      ({
        schemaVersion: "brier_reward_row_v1",
        predictionId: "p",
        specId: "s",
        split: "resolved",
        scoreEligibility: "scored_witness_verified",
        agent: "agent-a",
        runLabel: "run",
        runVariantId: "primary",
        distributionProvenance: "agent_reported",
        transformVersion: "v",
        resolutionDate: "2026-08-01",
        reward: {
          objective: "minimize_normalized_crps",
          value: null,
          components: {
            crps: null,
            normalizedCrps: null,
            absoluteError: null,
            normalizedAbsoluteError: null,
            sharpness: null,
            normalizationScale: null,
            normalizationScaleSource: null,
            interval80Covered: null,
          },
        },
        auxiliaryJudges: {
          rewardEligible: false,
          traceQualityScore: null,
          primaryFailureMode: undefined,
        },
        preSubmitReview: {
          status: "not_reviewed",
          reviewed: false,
          findingCount: 0,
          acceptedCount: 0,
          blockingFindingCount: 0,
        },
        provenance: {
          activityArtifactCount: 0,
        },
        ...overrides,
      }) as BrierRewardRow;

    const rows = [
      base({ runId: "r1", agent: "github:ext" }),
      base({
        runId: "r2",
        agent: "github:ext",
        externalSubmission: { challenger: "github:ext", systemType: "ai" },
      }),
      base({
        runId: "r3",
        agent: "github:pure-ext",
        externalSubmission: {
          challenger: "github:pure-ext",
          systemType: "ai",
        },
      }),
      base({ runId: "r4", agent: "thesis.analyst" }),
    ];
    const leaderboard = buildBrierAgentLeaderboard(rows);
    const byAgent = new Map(leaderboard.map((row) => [row.agent, row]));
    expect(byAgent.get("github:ext")?.external).toBe(false);
    expect(byAgent.get("github:pure-ext")?.external).toBe(true);
    expect(byAgent.get("thesis.analyst")?.external).toBe(false);
  });
});
