import { sha256Hex } from "./canonical-json";
import type { ThesisTargetArchitectureProjection } from "./thesis-target-architecture";

export type TargetArchitectureTableKey =
  (typeof TARGET_ARCHITECTURE_TABLES)[number];

export const TARGET_ARCHITECTURE_CHUNK_SIZE = 10_000;
export const TARGET_ARCHITECTURE_BUILDER_VERSION =
  "thesis_target_architecture_builder_v2";

export const TARGET_ARCHITECTURE_TABLES = [
  "targets",
  "targetVersions",
  "sourceSeries",
  "observations",
  "observationVintages",
  "targetObservationBindings",
  "baselineCandidates",
  "forecastStrategies",
  "strategyVersions",
  "packs",
  "packVersions",
  "forecastRuns",
  "runPackVersions",
  "runArtifactRefs",
  "toolCalls",
  "forecastDistributions",
  "reasoningEvents",
  "reviewRuns",
  "judgeRuns",
  "resolutionEvents",
  "scores",
  "artifactRefs",
] as const;

export interface TargetArchitectureManifest {
  schemaVersion: "thesis_target_architecture_manifest_v2";
  projectionSchemaVersion: ThesisTargetArchitectureProjection["schemaVersion"];
  generatedAt: string;
  source: ThesisTargetArchitectureProjection["source"];
  sourceCommit: string;
  builderVersion: typeof TARGET_ARCHITECTURE_BUILDER_VERSION;
  hashAlgorithm: "sha256";
  hashCanonicalization: "canonical_json_v1";
  chunkHashSemantics: "canonical_chunk_without_projection_root_v1";
  projectionRootSha256: string;
  counts: ThesisTargetArchitectureProjection["counts"];
  chunkSize: number;
  tables: TargetArchitectureTableManifest[];
}

export interface TargetArchitectureTableManifest {
  table: TargetArchitectureTableKey;
  rowCount: number;
  url: string;
  chunkCount: number;
  sha256: string;
  chunks: TargetArchitectureChunkManifest[];
}

export interface TargetArchitectureChunkManifest {
  index: number;
  rowCount: number;
  url: string;
  sha256: string;
}

export interface TargetArchitectureTableExport {
  schemaVersion: "thesis_target_architecture_table_v2";
  projectionSchemaVersion: ThesisTargetArchitectureProjection["schemaVersion"];
  generatedAt: string;
  projectionRootSha256: string;
  table: TargetArchitectureTableKey;
  rowCount: number;
  chunkSize: number;
  chunkCount: number;
  sha256: string;
  chunks?: TargetArchitectureChunkManifest[];
  rows?: unknown[];
}

export interface TargetArchitectureChunkExport {
  schemaVersion: "thesis_target_architecture_chunk_v2";
  projectionSchemaVersion: ThesisTargetArchitectureProjection["schemaVersion"];
  generatedAt: string;
  projectionRootSha256: string;
  table: TargetArchitectureTableKey;
  chunkIndex: number;
  chunkSize: number;
  rowCount: number;
  rows: unknown[];
}

interface TargetArchitectureManifestOptions {
  sourceCommit?: string;
}

type RootPayload = Omit<TargetArchitectureManifest, "projectionRootSha256">;

export function buildTargetArchitectureManifest(
  projection: ThesisTargetArchitectureProjection,
  options: TargetArchitectureManifestOptions = {},
): TargetArchitectureManifest {
  const sourceCommit =
    options.sourceCommit ??
    process.env.VERCEL_GIT_COMMIT_SHA ??
    "source_commit_unavailable";
  const tables = TARGET_ARCHITECTURE_TABLES.map((table) =>
    buildTableManifest(projection, table),
  );
  const rootPayload: RootPayload = {
    schemaVersion: "thesis_target_architecture_manifest_v2",
    projectionSchemaVersion: projection.schemaVersion,
    generatedAt: projection.generatedAt,
    source: projection.source,
    sourceCommit,
    builderVersion: TARGET_ARCHITECTURE_BUILDER_VERSION,
    hashAlgorithm: "sha256",
    hashCanonicalization: "canonical_json_v1",
    chunkHashSemantics: "canonical_chunk_without_projection_root_v1",
    counts: projection.counts,
    chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
    tables,
  };
  return {
    ...rootPayload,
    projectionRootSha256: sha256Hex(rootPayload),
  };
}

export function buildTargetArchitectureTableExport(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
  manifest = buildTargetArchitectureManifest(projection),
): TargetArchitectureTableExport {
  const rows = getTargetArchitectureRows(projection, table);
  const tableManifest = requireTableManifest(manifest, table);
  if (tableManifest.chunkCount <= 1) {
    return {
      schemaVersion: "thesis_target_architecture_table_v2",
      projectionSchemaVersion: projection.schemaVersion,
      generatedAt: projection.generatedAt,
      projectionRootSha256: manifest.projectionRootSha256,
      table,
      rowCount: rows.length,
      chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
      chunkCount: tableManifest.chunkCount,
      sha256: tableManifest.sha256,
      rows,
    };
  }
  return {
    schemaVersion: "thesis_target_architecture_table_v2",
    projectionSchemaVersion: projection.schemaVersion,
    generatedAt: projection.generatedAt,
    projectionRootSha256: manifest.projectionRootSha256,
    table,
    rowCount: rows.length,
    chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
    chunkCount: tableManifest.chunkCount,
    sha256: tableManifest.sha256,
    chunks: tableManifest.chunks,
  };
}

export function buildTargetArchitectureChunkExport(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
  chunkIndex: number,
  manifest = buildTargetArchitectureManifest(projection),
): TargetArchitectureChunkExport {
  return {
    ...buildChunkHashPayload(projection, table, chunkIndex),
    projectionRootSha256: manifest.projectionRootSha256,
  };
}

export function buildTargetArchitectureRootPayload(
  manifest: TargetArchitectureManifest,
): RootPayload {
  const { projectionRootSha256: _projectionRootSha256, ...payload } = manifest;
  return payload;
}

export function buildTargetArchitectureChunkHashPayload(
  chunk: TargetArchitectureChunkExport,
): Omit<TargetArchitectureChunkExport, "projectionRootSha256"> {
  const { projectionRootSha256: _projectionRootSha256, ...payload } = chunk;
  return payload;
}

export function isTargetArchitectureTableKey(
  value: string,
): value is TargetArchitectureTableKey {
  return TARGET_ARCHITECTURE_TABLES.includes(
    value as TargetArchitectureTableKey,
  );
}

function buildTableManifest(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
): TargetArchitectureTableManifest {
  const rows = getTargetArchitectureRows(projection, table);
  const chunks = buildChunkManifests(projection, table, rows.length);
  const payload = {
    table,
    rowCount: rows.length,
    url: `/forecasts/targets/${table}/manifest.json`,
    chunkCount: getChunkCount(rows.length),
    chunks,
  };
  return { ...payload, sha256: sha256Hex(payload) };
}

function buildChunkManifests(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
  rowCount: number,
): TargetArchitectureChunkManifest[] {
  return Array.from({ length: getChunkCount(rowCount) }, (_, index) => {
    const payload = buildChunkHashPayload(projection, table, index);
    return {
      index,
      rowCount: payload.rowCount,
      url: `/forecasts/targets/${table}/${index}.json`,
      sha256: sha256Hex(payload),
    };
  });
}

function buildChunkHashPayload(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
  chunkIndex: number,
): Omit<TargetArchitectureChunkExport, "projectionRootSha256"> {
  const rows = getTargetArchitectureRows(projection, table);
  const start = chunkIndex * TARGET_ARCHITECTURE_CHUNK_SIZE;
  const chunkRows = rows.slice(start, start + TARGET_ARCHITECTURE_CHUNK_SIZE);
  return {
    schemaVersion: "thesis_target_architecture_chunk_v2",
    projectionSchemaVersion: projection.schemaVersion,
    generatedAt: projection.generatedAt,
    table,
    chunkIndex,
    chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
    rowCount: chunkRows.length,
    rows: chunkRows,
  };
}

function getChunkCount(rowCount: number) {
  return Math.max(1, Math.ceil(rowCount / TARGET_ARCHITECTURE_CHUNK_SIZE));
}

function getTargetArchitectureRows(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
): unknown[] {
  return projection[table] as unknown[];
}

function requireTableManifest(
  manifest: TargetArchitectureManifest,
  table: TargetArchitectureTableKey,
) {
  const tableManifest = manifest.tables.find(
    (candidate) => candidate.table === table,
  );
  if (!tableManifest) {
    throw new Error(`Missing target-architecture manifest table: ${table}`);
  }
  return tableManifest;
}
