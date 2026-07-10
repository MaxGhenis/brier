import type { ForecastCell } from "./forecast-cells";
import {
  buildTargetArchitectureProjection,
  type ThesisTargetArchitectureProjection,
} from "./thesis-target-architecture";
import type { PolicyEngineLedgerEntry } from "./thesis-log";

export interface TargetArchitectureBackfillSql {
  schemaVersion: "thesis_target_architecture_backfill_sql_v1";
  generatedAt: string;
  projection: ThesisTargetArchitectureProjection;
  counts: ThesisTargetArchitectureProjection["counts"];
  sql: string;
}

type SqlValue =
  | string
  | number
  | boolean
  | null
  | undefined
  | SqlRaw
  | SqlArray;

interface InsertStatement {
  table: string;
  columns: string[];
  rows: SqlValue[][];
}

class SqlRaw {
  constructor(readonly sql: string) {}
}

class SqlArray {
  constructor(readonly values: string[]) {}
}

const BACKFILL_GENERATED_AT = "2026-06-29T00:00:00+00:00";
const INSERT_CHUNK_SIZE = 500;

export function buildTargetArchitectureBackfillSql({
  forecasts,
  ledger,
}: {
  forecasts: ForecastCell[];
  ledger: PolicyEngineLedgerEntry[];
}): TargetArchitectureBackfillSql {
  const projection = buildTargetArchitectureProjection(forecasts, ledger);
  const statements = buildInsertStatements({ projection });

  return {
    schemaVersion: "thesis_target_architecture_backfill_sql_v1",
    generatedAt: BACKFILL_GENERATED_AT,
    projection,
    counts: projection.counts,
    sql: renderBackfillSql({ projection, statements }),
  };
}

function buildInsertStatements({
  projection,
}: {
  projection: ThesisTargetArchitectureProjection;
}): InsertStatement[] {
  const resolutionEventById = new Map(
    projection.resolutionEvents.map((event) => [
      event.resolutionEventId,
      event,
    ]),
  );

  return [
    insert(
      "artifact_refs",
      [
        "artifact_ref_id",
        "content_hash",
        "media_type",
        "storage_uri",
        "public_visibility",
        "metadata",
        "created_at",
      ],
      projection.artifactRefs.map((artifact) => [
        artifact.artifactRefId,
        artifact.contentHash,
        artifact.mediaType,
        artifact.storageUri,
        artifact.publicVisibility,
        json(artifact.metadata),
        timestamp(BACKFILL_GENERATED_AT),
      ]),
    ),
    insert(
      "targets",
      [
        "target_id",
        "slug",
        "data_point_id",
        "country",
        "agency",
        "source_family",
        "source_url",
        "tags",
        "created_at",
      ],
      projection.targets.map((target) => [
        target.targetId,
        target.slug,
        target.dataPointId,
        target.country,
        target.agency,
        target.sourceFamily,
        target.sourceUrl,
        textArray(target.tags),
        timestamp(target.createdAt),
      ]),
    ),
    insert(
      "target_versions",
      [
        "target_version_id",
        "target_id",
        "parent_target_version_id",
        "version_label",
        "question",
        "period_label",
        "target_period",
        "unit",
        "value_scale",
        "scoring_transform",
        "resolver_kind",
        "resolution_policy",
        "resolution_date_basis",
        "resolution_rule",
        "resolution_source",
        "resolution_source_url",
        "cdf_point_count",
        "published_at",
      ],
      projection.targetVersions.map((version) => [
        version.targetVersionId,
        version.targetId,
        null,
        version.versionLabel,
        version.question,
        version.periodLabel,
        version.targetPeriod,
        version.unit,
        version.valueScale,
        version.scoringTransform,
        version.resolverKind,
        version.resolutionPolicy,
        version.resolutionDateBasis,
        version.resolutionRule,
        version.resolutionSource,
        version.resolutionSourceUrl,
        version.cdfPointCount,
        timestamp(version.publishedAt),
      ]),
    ),
    insert(
      "source_series",
      [
        "source_series_id",
        "adapter_id",
        "source_family",
        "agency_series_id",
        "measure_key",
        "country",
        "agency",
        "source_url",
        "unit",
        "update_cadence",
        "default_vintage_policy",
        "metadata",
      ],
      projection.sourceSeries.map((series) => [
        series.sourceSeriesId,
        series.adapterId,
        series.sourceFamily,
        series.agencySeriesId ?? "",
        series.measureKey,
        series.country,
        series.agency,
        series.sourceUrl,
        series.unit,
        series.updateCadence,
        series.defaultVintagePolicy,
        json({ generatedFrom: "thesis_target_architecture_projection_v1" }),
      ]),
    ),
    insert(
      "observations",
      [
        "observation_id",
        "source_series_id",
        "data_point_id",
        "period_label",
        "value",
        "unit",
        "value_scale",
        "source_url",
        "retrieved_at",
        "payload_hash",
      ],
      projection.observations.map((observation) => [
        observation.observationId,
        observation.sourceSeriesId,
        observation.dataPointId,
        observation.periodLabel,
        observation.value,
        observation.unit,
        observation.valueScale,
        observation.sourceUrl,
        timestamp(observation.retrievedAt),
        observation.payloadHash,
      ]),
    ),
    insert(
      "observation_vintages",
      [
        "vintage_id",
        "observation_id",
        "vintage_kind",
        "published_at",
        "retrieved_at",
        "source_snapshot_artifact_ref_id",
        "normalized_payload_hash",
      ],
      projection.observationVintages.map((vintage) => [
        vintage.vintageId,
        vintage.observationId,
        vintage.vintageKind,
        timestamp(vintage.publishedAt),
        timestamp(vintage.retrievedAt),
        null,
        vintage.normalizedPayloadHash,
      ]),
    ),
    insert(
      "target_observation_bindings",
      [
        "binding_id",
        "target_version_id",
        "source_series_id",
        "observation_id",
        "binding_role",
        "transform_kind",
        "transform_expression",
        "adapter_method",
      ],
      projection.targetObservationBindings.map((binding) => [
        binding.bindingId,
        binding.targetVersionId,
        binding.sourceSeriesId,
        null,
        binding.bindingRole,
        binding.transformKind,
        null,
        binding.adapterMethod,
      ]),
    ),
    insert(
      "forecast_strategies",
      ["strategy_id", "name", "strategy_kind", "description"],
      projection.forecastStrategies.map((strategy) => [
        strategy.strategyId,
        strategy.name,
        strategy.strategyKind,
        strategy.description,
      ]),
    ),
    insert(
      "strategy_versions",
      [
        "strategy_version_id",
        "strategy_id",
        "version_label",
        "prompt_policy_hash",
        "tool_policy_hash",
        "required_inputs",
        "model_family_constraints",
      ],
      projection.strategyVersions.map((version) => [
        version.strategyVersionId,
        version.strategyId,
        version.versionLabel,
        version.promptPolicyHash,
        version.toolPolicyHash,
        json(version.requiredInputs),
        json(version.modelFamilyConstraints),
      ]),
    ),
    insert(
      "packs",
      [
        "pack_id",
        "slug",
        "name",
        "target_family_tags",
        "owner_id",
        "created_at",
      ],
      projection.packs.map((pack) => [
        pack.packId,
        pack.slug,
        pack.name,
        textArray(pack.targetFamilyTags),
        pack.ownerId,
        timestamp(pack.createdAt),
      ]),
    ),
    insert(
      "pack_versions",
      [
        "pack_version_id",
        "pack_id",
        "version_label",
        "evidence_requirements",
        "validator_rules",
        "prompt_content_hash",
        "examples",
        "ablation_plan",
      ],
      projection.packVersions.map((version) => [
        version.packVersionId,
        version.packId,
        version.versionLabel,
        json(version.evidenceRequirements),
        json(version.validatorRules),
        version.promptContentHash,
        json([]),
        version.ablationPlan,
      ]),
    ),
    insert(
      "forecast_runs",
      [
        "run_id",
        "target_version_id",
        "strategy_version_id",
        "agent_id",
        "model",
        "runtime",
        "prompt_hash",
        "tool_policy_hash",
        "input_bundle_hash",
        "status",
        "idempotency_key",
        "run_at",
      ],
      projection.forecastRuns.map((run) => [
        run.runId,
        run.targetVersionId,
        run.strategyVersionId,
        run.agentId,
        run.model,
        run.runtime,
        run.promptHash,
        run.toolPolicyHash,
        run.inputBundleHash,
        run.status,
        run.idempotencyKey,
        timestamp(run.runAt),
      ]),
    ),
    insert(
      "baseline_candidates",
      [
        "candidate_id",
        "target_version_id",
        "source_series_id",
        "model_adapter",
        "candidate_label",
        "training_cutoff",
        "point_estimate",
        "p10",
        "p50",
        "p90",
        "interval80_lower",
        "interval80_upper",
        "interval_method",
        "calibration_sample_size",
        "walk_forward_score",
        "assumptions",
        "failure_modes",
        "artifact_ref_id",
        "provenance",
      ],
      projection.baselineCandidates.map((candidate) => [
        candidate.candidateId,
        candidate.targetVersionId,
        candidate.sourceSeriesId,
        candidate.modelAdapter,
        candidate.candidateLabel,
        timestamp(candidate.trainingCutoff),
        candidate.pointEstimate,
        candidate.p10,
        candidate.p50,
        candidate.p90,
        candidate.interval80Lower,
        candidate.interval80Upper,
        candidate.intervalMethod,
        candidate.calibrationSampleSize,
        candidate.walkForwardScore,
        candidate.assumptions,
        textArray(candidate.failureModes),
        candidate.artifactRefId,
        json(candidate.provenance),
      ]),
    ),
    insert(
      "run_artifact_refs",
      [
        "run_artifact_ref_id",
        "run_id",
        "artifact_ref_id",
        "artifact_role",
        "sequence_index",
      ],
      projection.runArtifactRefs.map((ref) => [
        ref.runArtifactRefId,
        ref.runId,
        ref.artifactRefId,
        ref.artifactRole,
        ref.sequenceIndex,
      ]),
    ),
    insert(
      "run_pack_versions",
      ["run_pack_version_id", "run_id", "pack_version_id", "pack_role"],
      projection.runPackVersions.map((runPackVersion) => [
        runPackVersion.runPackVersionId,
        runPackVersion.runId,
        runPackVersion.packVersionId,
        runPackVersion.packRole,
      ]),
    ),
    insert(
      "forecast_distributions",
      [
        "run_id",
        "point_index",
        "value",
        "probability",
        "unit",
        "interval_mass",
        "distribution_provenance",
        "transform_version",
        "validation_status",
      ],
      projection.forecastDistributions.map((point) => [
        point.runId,
        point.pointIndex,
        point.value,
        point.probability,
        point.unit,
        point.intervalMass,
        point.distributionProvenance,
        point.transformVersion,
        point.validationStatus,
      ]),
    ),
    insert(
      "reasoning_events",
      [
        "reasoning_event_id",
        "run_id",
        "sequence_index",
        "event_kind",
        "public_text",
        "artifact_ref_id",
        "redaction_status",
      ],
      projection.reasoningEvents.map((event) => [
        event.reasoningEventId,
        event.runId,
        event.sequenceIndex,
        event.eventKind,
        event.publicText,
        event.artifactRefId,
        event.redactionStatus,
      ]),
    ),
    insert(
      "review_runs",
      [
        "review_run_id",
        "run_id",
        "reviewer_agent_id",
        "draft_artifact_ref_id",
        "findings",
        "revision_artifact_ref_id",
        "disposition",
      ],
      projection.reviewRuns.map((review) => [
        review.reviewRunId,
        review.runId,
        review.reviewerAgentId,
        review.draftArtifactRefId,
        json(review.findings),
        review.revisionArtifactRefId,
        review.disposition,
      ]),
    ),
    insert(
      "judge_runs",
      [
        "judge_run_id",
        "run_id",
        "batch_id",
        "left_run_id",
        "right_run_id",
        "judge_model",
        "prompt_version",
        "findings",
        "recommendations",
        "reward_eligible",
      ],
      projection.judgeRuns.map((judge) => [
        judge.judgeRunId,
        judge.runId,
        judge.batchId,
        judge.leftRunId,
        judge.rightRunId,
        judge.judgeModel,
        judge.promptVersion,
        json(judge.findings),
        json(judge.recommendations),
        judge.rewardEligible,
      ]),
    ),
    insert(
      "tool_calls",
      [
        "tool_call_id",
        "run_id",
        "allowed_tool_declaration",
        "tool_name",
        "request_hash",
        "response_hash",
        "provider",
        "status",
        "cost_usd",
        "influenced_final_forecast",
        "started_at",
        "completed_at",
        "sequence_index",
        "source_role",
      ],
      projection.toolCalls.map((toolCall) => [
        toolCall.toolCallId,
        toolCall.runId,
        toolCall.allowedToolDeclaration,
        toolCall.toolName,
        toolCall.requestHash,
        toolCall.responseHash,
        toolCall.provider,
        toolCall.status,
        toolCall.costUsd,
        toolCall.influencedFinalForecast,
        timestamp(BACKFILL_GENERATED_AT),
        timestamp(BACKFILL_GENERATED_AT),
        toolCall.sequenceIndex,
        toolCall.sourceRole,
      ]),
    ),
    insert(
      "resolution_events",
      [
        "resolution_event_id",
        "target_version_id",
        "observation_id",
        "vintage_id",
        "resolved_value",
        "source_url",
        "resolver_proof",
        "scoreable_status",
        "event_timestamp",
      ],
      projection.resolutionEvents.map((event) => [
        event.resolutionEventId,
        event.targetVersionId,
        event.observationId,
        event.vintageId,
        event.resolvedValue,
        event.sourceUrl,
        json(event.resolverProof),
        event.scoreableStatus,
        timestamp(event.eventTimestamp),
      ]),
    ),
    insert(
      "scores",
      [
        "score_id",
        "run_id",
        "resolution_event_id",
        "scoring_rule",
        "distribution_provenance",
        "transform_version",
        "crps",
        "normalization_scale",
        "normalization_scale_source",
        "probability_integral_transform",
        "interval80_covered",
        "signed_error",
        "absolute_error",
        "score_hash",
        "normalized_score",
        "normalized_crps",
        "normalized_absolute_error",
        "sharpness",
      ],
      projection.scores.map((score) => [
        score.scoreId,
        score.runId,
        score.resolutionEventId,
        score.scoringRule,
        score.distributionProvenance,
        score.transformVersion,
        score.crps,
        score.normalizationScale,
        score.normalizationScaleSource,
        score.probabilityIntegralTransform,
        score.interval80Covered,
        score.signedError,
        score.absoluteError,
        score.scoreHash,
        score.normalizedScore,
        score.normalizedCrps,
        score.normalizedAbsoluteError,
        score.sharpness,
      ]),
    ),
  ].filter((statement) => statement.rows.length > 0);
}

function insert(
  table: string,
  columns: string[],
  rows: SqlValue[][],
): InsertStatement {
  return { table, columns, rows };
}

function renderBackfillSql({
  projection,
  statements,
}: {
  projection: ThesisTargetArchitectureProjection;
  statements: InsertStatement[];
}) {
  const header = [
    "-- Thesis target architecture full backfill.",
    "-- Apply after:",
    "--   site/supabase/migrations/20260629_thesis_target_architecture.sql",
    "--   site/supabase/migrations/20260709_distribution_provenance.sql",
    "-- This file is generated from forecast cells, ledger records, and public artifacts.",
    `-- generated_at: ${BACKFILL_GENERATED_AT}`,
    `-- targets: ${projection.counts.targets}`,
    `-- target_versions: ${projection.counts.targetVersions}`,
    `-- forecast_runs: ${projection.counts.forecastRuns}`,
    "",
    "begin;",
    "",
  ].join("\n");
  const body = statements.map(renderInsertStatement).join("\n\n");
  return `${header}${body}\n\ncommit;\n`;
}

function renderInsertStatement(statement: InsertStatement) {
  const columnList = statement.columns.map(quoteIdentifier).join(", ");
  const chunks: string[] = [];
  for (
    let index = 0;
    index < statement.rows.length;
    index += INSERT_CHUNK_SIZE
  ) {
    const rows = statement.rows.slice(index, index + INSERT_CHUNK_SIZE);
    chunks.push(
      [
        `insert into ${quoteIdentifier(statement.table)} (${columnList})`,
        "values",
        rows.map(renderValuesRow).join(",\n"),
        "on conflict do nothing;",
      ].join("\n"),
    );
  }
  return chunks.join("\n\n");
}

function renderValuesRow(values: SqlValue[]) {
  return `  (${values.map(renderSqlValue).join(", ")})`;
}

function renderSqlValue(value: SqlValue): string {
  if (value instanceof SqlRaw) return value.sql;
  if (value instanceof SqlArray) {
    return `ARRAY[${value.values.map(quoteLiteral).join(", ")}]::text[]`;
  }
  if (value === null || value === undefined) return "null";
  if (typeof value === "number") {
    if (!Number.isFinite(value)) return "null";
    return String(value);
  }
  if (typeof value === "boolean") return value ? "true" : "false";
  return quoteLiteral(value);
}

function json(value: unknown) {
  return new SqlRaw(`${quoteLiteral(JSON.stringify(value ?? null))}::jsonb`);
}

function timestamp(value: string | undefined) {
  return value ? new SqlRaw(`${quoteLiteral(value)}::timestamptz`) : null;
}

function textArray(values: string[]) {
  return new SqlArray(values);
}

function quoteIdentifier(value: string) {
  return `"${value.replace(/"/g, '""')}"`;
}

function quoteLiteral(value: string) {
  return `'${value.replace(/'/g, "''")}'`;
}
