import type {
  ForecastCell,
  PredictionPreSubmitReviewWorkflow,
} from "./forecast-cells";
import {
  buildForecastJudgeExport,
  type ForecastJudgeExport,
  type ForecastResolutionFailureMode,
} from "./forecast-judges";
import {
  buildRecordedPredictionRunId,
  buildRecordedPredictionRunRecords,
  type PredictionRunRecord,
  type PredictionSpec,
} from "./prediction-specs";
import type {
  PolicyEngineLedgerEntry,
  ResolvedForecastScore,
} from "./thesis-log";
import {
  buildPredictionRecordedLogEntries,
  buildResolvedPredictionLogEntries,
  scoreResolvedForecasts,
  withResolvedOutcomes,
} from "./thesis-log";
import { getForecastRunEntries } from "./forecast-cells";
import {
  getDistributionTransformVersion,
  type DistributionProvenance,
} from "./prediction-distribution";
import { PERSISTENCE_BASELINE_AGENT } from "./time-series-priors";

export type BrierEvalSplit = "train" | "validation" | "test" | "unresolved";

export interface BrierRewardRow {
  schemaVersion: "brier_reward_row_v1";
  runId: string;
  predictionId: string;
  specId: string;
  dataPointId?: string;
  split: BrierEvalSplit;
  agent?: string;
  model?: string;
  runLabel: string;
  runVariantId: string;
  runAt?: string;
  distributionProvenance: DistributionProvenance;
  transformVersion: string;
  resolutionDate: string;
  horizonDaysAtRun?: number;
  reward: {
    objective: "minimize_normalized_crps";
    value: number | null;
    components: {
      crps: number | null;
      normalizedCrps: number | null;
      absoluteError: number | null;
      normalizedAbsoluteError: number | null;
      sharpness: number | null;
      normalizationScale: number | null;
      normalizationScaleSource: "ledger_dispersion" | "target_primary_width" | "unavailable" | null;
      interval80Covered: boolean | null;
    };
  };
  auxiliaryJudges: {
    rewardEligible: false;
    traceJudgeId?: string;
    traceQualityScore: number | null;
    postResolutionJudgeId?: string;
    primaryFailureMode?: ForecastResolutionFailureMode;
  };
  preSubmitReview: {
    status: string;
    reviewed: boolean;
    findingCount: number;
    acceptedCount: number;
    blockingFindingCount: number;
  };
  provenance: {
    specVersionId: string;
    promptHash?: string;
    toolPolicyHash?: string;
    inputBundleHash?: string;
    scoreId?: string;
    resolutionEventId?: string;
    ledgerFactRef?: string;
    custodyRootSha256?: string;
    aggregationAlgorithmVersion?: string;
    constituentRuns?: PredictionRunRecord["constituentRuns"];
    activityArtifactCount: number;
  };
}

export interface BrierAgentLeaderboardRow {
  agent: string;
  model?: string;
  scoredRuns: number;
  totalRuns: number;
  unpairedMeanReward: number | null;
  unpairedMeanNormalizedCrps: number | null;
  unpairedMeanAbsoluteError: number | null;
  unpairedInterval80Coverage: number | null;
  pairedTargets: number;
  meanPairedSkill: number | null;
  pairedWinRate: number | null;
  activityArtifactCoverage: number;
}

export interface BrierBaselineCoverageRow {
  predictionId: string;
  primaryRunId: string;
  status: "available" | "unavailable";
  cutoff: string;
  targetDataPointId?: string;
  seriesId?: string;
  observationRefs: NonNullable<
    ForecastCell["persistenceBaseline"]
  >["observationRefs"];
  reason?: string;
}

export interface BrierPairedComparisonSummary {
  pairedTargets: number;
  meanAgentMinusBaselineNormalizedCrps: number | null;
  agentWinRate: number | null;
}

export interface BrierRewardExport {
  schemaVersion: "brier_reward_export_v1";
  generatedAt: string;
  mission: {
    agent: "Brier";
    objective: "maximize_forecast_accuracy";
    reward: "negative_normalized_crps";
    constraints: string[];
  };
  counts: {
    specs: number;
    runs: number;
    scoredRuns: number;
    unresolvedRuns: number;
    agents: number;
    traceJudgedRuns: number;
    postResolutionJudgeRows: number;
    preSubmitReviewedRuns: number;
    baselineTargets: number;
    availableBaselines: number;
    unavailableBaselines: number;
    pairedTargets: number;
  };
  splits: Record<
    BrierEvalSplit,
    {
      runs: number;
      scoredRuns: number;
      rule: string;
    }
  >;
  noLeakagePolicy: {
    rule: string;
    trainingEligibleSplits: BrierEvalSplit[];
    holdoutSplits: BrierEvalSplit[];
  };
  judgePolicy: {
    role: "auxiliary_process_eval";
    rewardEligible: false;
    calibrationRule: string;
  };
  leaderboard: BrierAgentLeaderboardRow[];
  pairedComparison: BrierPairedComparisonSummary;
  baselineCoverage: BrierBaselineCoverageRow[];
  rewardRows: BrierRewardRow[];
  judgeResults: ForecastJudgeExport;
}

export function buildBrierRewardExport({
  forecasts,
  specs,
  runs,
  ledger,
  generatedAt = "2026-06-16T00:00:00Z",
}: {
  forecasts: ForecastCell[];
  specs: PredictionSpec[];
  runs: PredictionRunRecord[];
  ledger: PolicyEngineLedgerEntry[];
  generatedAt?: string;
}): BrierRewardExport {
  const preparedForecasts = withResolvedOutcomes(forecasts, ledger);
  const suppliedRunsById = new Map(runs.map((run) => [run.runId, run]));
  for (const run of buildRecordedPredictionRunRecords(
    preparedForecasts,
    specs,
  )) {
    suppliedRunsById.set(run.runId, run);
  }
  const preparedRuns = [...suppliedRunsById.values()];
  // Rewards and leaderboards draw only on chronology-verified scores; a
  // run that cannot prove it predates the observation earns nothing.
  const scores = scoreResolvedForecasts(preparedForecasts, ledger).filter(
    (score) => score.chronology === "verified",
  );
  const judgeResults = buildForecastJudgeExport({
    forecasts: preparedForecasts,
    scores,
  });
  const traceJudgeByRunId = new Map(
    judgeResults.traceQuality.map((judge) => [judge.runId, judge]),
  );
  const postResolutionJudgeByRunId = new Map(
    judgeResults.postResolution.map((judge) => [judge.runId, judge]),
  );
  const scoreByRunId = new Map(scores.map((score) => [score.runId, score]));
  const specByPredictionId = new Map(
    specs.map((spec) => [spec.predictionId, spec]),
  );
  const runByRunId = new Map(preparedRuns.map((run) => [run.runId, run]));
  const rewardRows = preparedForecasts.flatMap((forecast) => {
    const spec = specByPredictionId.get(forecast.slug);
    return getForecastRunEntries(forecast).map((run) => {
      const runId = buildRecordedPredictionRunId(
        forecast,
        run.predictionRun?.runAt,
        run.variantId,
        run,
      );
      const score = scoreByRunId.get(runId);
      const runRecord = runByRunId.get(runId);
      const split = getBrierEvalSplit(forecast, score);
      return buildRewardRow({
        forecast,
        run,
        runId,
        spec,
        score,
        runRecord,
        split,
        traceJudge: traceJudgeByRunId.get(runId),
        postResolutionJudge: postResolutionJudgeByRunId.get(runId),
      });
    });
  });
  const leaderboard = buildBrierAgentLeaderboard(rewardRows);
  const pairedComparison = summarizePairedComparison(
    rewardRows.filter((row) => row.runVariantId === "primary"),
    rewardRows.filter((row) => row.agent === PERSISTENCE_BASELINE_AGENT),
  );
  const baselineCoverage = preparedForecasts.flatMap((forecast) => {
    const baseline = forecast.persistenceBaseline;
    if (!baseline) return [];
    const primary = getForecastRunEntries(forecast)[0];
    if (!primary) return [];
    return [
      {
        predictionId: forecast.slug,
        primaryRunId: buildRecordedPredictionRunId(
          forecast,
          primary.predictionRun?.runAt,
          primary.variantId,
          primary,
        ),
        ...baseline,
      },
    ];
  });

  return {
    schemaVersion: "brier_reward_export_v1",
    generatedAt,
    mission: {
      agent: "Brier",
      objective: "maximize_forecast_accuracy",
      reward: "negative_normalized_crps",
      constraints: [
        "agent-only forecasts",
        "public statistical series with predictable first-print resolution",
        "immutable run artifacts",
        "proper scoring rules",
        "holdout splits by resolution date",
      ],
    },
    counts: {
      specs: specs.length,
      runs: rewardRows.length,
      scoredRuns: rewardRows.filter((row) => row.reward.value !== null).length,
      unresolvedRuns: rewardRows.filter((row) => row.split === "unresolved")
        .length,
      agents: leaderboard.length,
      traceJudgedRuns: judgeResults.traceQuality.length,
      postResolutionJudgeRows: judgeResults.postResolution.length,
      preSubmitReviewedRuns: rewardRows.filter(
        (row) => row.preSubmitReview.reviewed,
      ).length,
      baselineTargets: baselineCoverage.length,
      availableBaselines: baselineCoverage.filter(
        (row) => row.status === "available",
      ).length,
      unavailableBaselines: baselineCoverage.filter(
        (row) => row.status === "unavailable",
      ).length,
      pairedTargets: pairedComparison.pairedTargets,
    },
    splits: buildSplitSummary(rewardRows),
    noLeakagePolicy: {
      rule: "Rows are split by resolutionDate, not run order. Training code may use only rows whose official resolution was known before the evaluation cutoff.",
      trainingEligibleSplits: ["train"],
      holdoutSplits: ["validation", "test"],
    },
    judgePolicy: {
      role: "auxiliary_process_eval",
      rewardEligible: false,
      calibrationRule:
        "Judge scores can be used as process diagnostics only after checking whether they predict held-out normalized CRPS. They must not replace the proper-score reward.",
    },
    leaderboard,
    pairedComparison,
    baselineCoverage,
    rewardRows,
    judgeResults,
  };
}

export function getBrierEvalSplit(
  forecast: ForecastCell,
  score?: ResolvedForecastScore,
): BrierEvalSplit {
  if (!score) return "unresolved";
  if (forecast.resolutionDate < "2026-07-01") return "train";
  if (forecast.resolutionDate < "2027-01-01") return "validation";
  return "test";
}

function buildRewardRow({
  forecast,
  run,
  runId,
  spec,
  score,
  runRecord,
  split,
  traceJudge,
  postResolutionJudge,
}: {
  forecast: ForecastCell;
  run: ReturnType<typeof getForecastRunEntries>[number];
  runId: string;
  spec?: PredictionSpec;
  score?: ResolvedForecastScore;
  runRecord?: PredictionRunRecord;
  split: BrierEvalSplit;
  traceJudge?: ForecastJudgeExport["traceQuality"][number];
  postResolutionJudge?: ForecastJudgeExport["postResolution"][number];
}): BrierRewardRow {
  return {
    schemaVersion: "brier_reward_row_v1",
    runId,
    predictionId: forecast.slug,
    specId: spec?.specId ?? `spec.${forecast.slug}`,
    dataPointId: forecast.dataPointId,
    split,
    agent: run.predictionRun?.agent,
    model: run.predictionRun?.model,
    runLabel: run.label,
    runVariantId: run.variantId,
    runAt: run.predictionRun?.runAt,
    distributionProvenance: run.predictionDistribution.provenance,
    transformVersion: getDistributionTransformVersion(
      run.predictionDistribution,
    ),
    resolutionDate: forecast.resolutionDate,
    horizonDaysAtRun: getHorizonDaysAtRun(run.predictionRun?.runAt, forecast),
    reward: {
      objective: "minimize_normalized_crps",
      value:
        score?.normalizedCrps === null || score?.normalizedCrps === undefined
          ? null
          : -score.normalizedCrps,
      components: {
        crps: score?.crps ?? null,
        normalizedCrps: score?.normalizedCrps ?? null,
        absoluteError: score?.absoluteError ?? null,
        normalizedAbsoluteError: score?.normalizedAbsoluteError ?? null,
        sharpness: score?.sharpness ?? null,
        normalizationScale: score?.normalizationScale ?? null,
        normalizationScaleSource: score?.normalizationScaleSource ?? null,
        interval80Covered: score?.interval80Covered ?? null,
      },
    },
    auxiliaryJudges: {
      rewardEligible: false,
      traceJudgeId: traceJudge?.judgeId,
      traceQualityScore: traceJudge?.overallScore ?? null,
      postResolutionJudgeId: postResolutionJudge?.judgeId,
      primaryFailureMode: postResolutionJudge?.primaryFailureMode,
    },
    preSubmitReview: summarizePreSubmitReview(
      run.predictionRun?.preSubmitReview,
    ),
    provenance: {
      specVersionId: spec?.specVersionId ?? `spec.${forecast.slug}.v1`,
      promptHash: runRecord?.promptHash,
      toolPolicyHash: runRecord?.toolPolicyHash,
      inputBundleHash: runRecord?.inputBundleHash,
      scoreId: score?.scoreId,
      resolutionEventId: score?.resolutionEventId,
      ledgerFactRef: score?.ledgerFactRef,
      custodyRootSha256: run.predictionRun?.custodyRootSha256,
      aggregationAlgorithmVersion:
        run.predictionRun?.aggregationAlgorithmVersion,
      constituentRuns: run.predictionRun?.constituentRuns,
      activityArtifactCount: run.predictionRun?.activityLog?.length ?? 0,
    },
  };
}

function summarizePreSubmitReview(
  review?: PredictionPreSubmitReviewWorkflow,
): BrierRewardRow["preSubmitReview"] {
  const findings = review?.findings ?? [];
  const dispositions = review?.dispositions ?? [];
  return {
    status: review?.status ?? "not_requested",
    reviewed: review?.status === "completed",
    findingCount: findings.length,
    acceptedCount: dispositions.filter((disposition) =>
      ["accepted", "partially_accepted"].includes(disposition.decision),
    ).length,
    blockingFindingCount: findings.filter(
      (finding) => finding.severity === "blocking",
    ).length,
  };
}

export function buildBrierAgentLeaderboard(
  rows: BrierRewardRow[],
): BrierAgentLeaderboardRow[] {
  const groups = new Map<string, BrierRewardRow[]>();
  for (const row of rows) {
    const key = `${row.agent ?? "prototype seed"}\u0000${row.model ?? ""}`;
    groups.set(key, [...(groups.get(key) ?? []), row]);
  }

  return [...groups.entries()]
    .map(([key, group]) => {
      const [agent, model] = key.split("\u0000");
      const rawScoredRows = group.filter(
        (row) => row.reward.components.crps !== null,
      );
      const scoredRows = group.filter(
        (row) => row.reward.components.normalizedCrps !== null,
      );
      const artifactRows = group.filter(
        (row) => row.provenance.activityArtifactCount > 0,
      );
      const paired =
        agent === PERSISTENCE_BASELINE_AGENT
          ? { pairedTargets: 0, meanPairedSkill: null, pairedWinRate: null }
          : pairedSkillForRows(scoredRows, rows);
      return {
        agent,
        model: model || undefined,
        scoredRuns: scoredRows.length,
        totalRuns: group.length,
        unpairedMeanReward: mean(
          scoredRows.map((row) => row.reward.value).filter(isNumber),
        ),
        unpairedMeanNormalizedCrps: mean(
          scoredRows
            .map((row) => row.reward.components.normalizedCrps)
            .filter(isNumber),
        ),
        unpairedMeanAbsoluteError: mean(
          rawScoredRows
            .map((row) => row.reward.components.absoluteError)
            .filter(isNumber),
        ),
        unpairedInterval80Coverage: mean(
          rawScoredRows
            .map((row) => row.reward.components.interval80Covered)
            .filter((value): value is boolean => typeof value === "boolean")
            .map((covered) => (covered ? 1 : 0)),
        ),
        ...paired,
        activityArtifactCoverage:
          group.length === 0 ? 0 : artifactRows.length / group.length,
      };
    })
    .sort((left, right) => {
      const leftSkill = left.meanPairedSkill ?? Number.POSITIVE_INFINITY;
      const rightSkill = right.meanPairedSkill ?? Number.POSITIVE_INFINITY;
      if (leftSkill !== rightSkill) return leftSkill - rightSkill;
      const leftReward = left.unpairedMeanReward ?? Number.NEGATIVE_INFINITY;
      const rightReward = right.unpairedMeanReward ?? Number.NEGATIVE_INFINITY;
      if (leftReward !== rightReward) return rightReward - leftReward;
      return right.scoredRuns - left.scoredRuns;
    });
}

function pairedSkillForRows(
  agentRows: BrierRewardRow[],
  allRows: BrierRewardRow[],
) {
  const baselineRows = allRows.filter(
    (row) =>
      row.agent === PERSISTENCE_BASELINE_AGENT && row.reward.value !== null,
  );
  const baselineByTarget = new Map(
    baselineRows.map((row) => [
      row.predictionId,
      row.reward.components.normalizedCrps,
    ]),
  );
  const agentScoresByTarget = new Map<string, number[]>();
  for (const row of agentRows) {
    const score = row.reward.components.normalizedCrps;
    if (score === null || !baselineByTarget.has(row.predictionId)) continue;
    agentScoresByTarget.set(row.predictionId, [
      ...(agentScoresByTarget.get(row.predictionId) ?? []),
      score,
    ]);
  }
  const deltas = [...agentScoresByTarget].flatMap(
    ([predictionId, agentScores]) => {
      const baselineScore = baselineByTarget.get(predictionId);
      const agentScore = mean(agentScores);
      return baselineScore === null ||
        baselineScore === undefined ||
        agentScore === null
        ? []
        : [agentScore - baselineScore];
    },
  );
  return {
    pairedTargets: deltas.length,
    meanPairedSkill: mean(deltas),
    pairedWinRate:
      deltas.length === 0
        ? null
        : deltas.filter((delta) => delta < 0).length / deltas.length,
  };
}

export function summarizePairedComparison(
  agentRows: BrierRewardRow[],
  baselineRows: BrierRewardRow[],
): BrierPairedComparisonSummary {
  const paired = pairedSkillForRows(agentRows, baselineRows);
  return {
    pairedTargets: paired.pairedTargets,
    meanAgentMinusBaselineNormalizedCrps: paired.meanPairedSkill,
    agentWinRate: paired.pairedWinRate,
  };
}

function buildSplitSummary(
  rows: BrierRewardRow[],
): BrierRewardExport["splits"] {
  return {
    train: summarizeSplit(rows, "train", "Resolved before 2026-07-01."),
    validation: summarizeSplit(
      rows,
      "validation",
      "Resolved from 2026-07-01 through 2026-12-31.",
    ),
    test: summarizeSplit(rows, "test", "Resolved on or after 2027-01-01."),
    unresolved: summarizeSplit(
      rows,
      "unresolved",
      "Not eligible for reward until the first-print resolver posts a fact.",
    ),
  };
}

function summarizeSplit(
  rows: BrierRewardRow[],
  split: BrierEvalSplit,
  rule: string,
) {
  const splitRows = rows.filter((row) => row.split === split);
  return {
    runs: splitRows.length,
    scoredRuns: splitRows.filter((row) => row.reward.value !== null).length,
    rule,
  };
}

function getHorizonDaysAtRun(
  runAt: string | undefined,
  forecast: ForecastCell,
): number | undefined {
  if (!runAt) return undefined;
  const runTime = Date.parse(runAt);
  const resolutionTime = Date.parse(`${forecast.resolutionDate}T00:00:00Z`);
  if (!Number.isFinite(runTime) || !Number.isFinite(resolutionTime)) {
    return undefined;
  }
  return Math.round((resolutionTime - runTime) / 86_400_000);
}

function mean(values: number[]) {
  if (values.length === 0) return null;
  return values.reduce((total, value) => total + value, 0) / values.length;
}

function isNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

export function summarizeBrierCoverage({
  forecasts,
  ledger,
}: {
  forecasts: ForecastCell[];
  ledger: PolicyEngineLedgerEntry[];
}) {
  const recorded = buildPredictionRecordedLogEntries(forecasts);
  const resolved = buildResolvedPredictionLogEntries(forecasts, ledger);
  const scored = scoreResolvedForecasts(forecasts, ledger).filter(
    (score) => score.chronology === "verified",
  );
  return {
    recordedRuns: recorded.length,
    resolvedEvents: resolved.length,
    scoredRuns: scored.length,
    activityLoggedRuns: recorded.filter((entry) => entry.activityLog?.length)
      .length,
  };
}
