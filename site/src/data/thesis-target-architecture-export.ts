import type { ThesisTargetArchitectureProjection } from "./thesis-target-architecture";

export type TargetArchitectureTableKey =
  (typeof TARGET_ARCHITECTURE_TABLES)[number];

export const TARGET_ARCHITECTURE_CHUNK_SIZE = 10_000;

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
  schemaVersion: "thesis_target_architecture_manifest_v1";
  projectionSchemaVersion: ThesisTargetArchitectureProjection["schemaVersion"];
  generatedAt: string;
  source: ThesisTargetArchitectureProjection["source"];
  counts: ThesisTargetArchitectureProjection["counts"];
  chunkSize: number;
  tables: TargetArchitectureTableManifest[];
}

export interface TargetArchitectureTableManifest {
  table: TargetArchitectureTableKey;
  rowCount: number;
  url: string;
  chunkCount: number;
  chunks: TargetArchitectureChunkManifest[];
}

export interface TargetArchitectureChunkManifest {
  index: number;
  rowCount: number;
  url: string;
}

export interface TargetArchitectureTableExport {
  schemaVersion: "thesis_target_architecture_table_v1";
  projectionSchemaVersion: ThesisTargetArchitectureProjection["schemaVersion"];
  generatedAt: string;
  table: TargetArchitectureTableKey;
  rowCount: number;
  chunkSize: number;
  chunkCount: number;
  chunks?: TargetArchitectureChunkManifest[];
  rows?: unknown[];
}

export interface TargetArchitectureChunkExport {
  schemaVersion: "thesis_target_architecture_chunk_v1";
  projectionSchemaVersion: ThesisTargetArchitectureProjection["schemaVersion"];
  generatedAt: string;
  table: TargetArchitectureTableKey;
  chunkIndex: number;
  chunkSize: number;
  rowCount: number;
  rows: unknown[];
}

export function buildTargetArchitectureManifest(
  projection: ThesisTargetArchitectureProjection,
): TargetArchitectureManifest {
  return {
    schemaVersion: "thesis_target_architecture_manifest_v1",
    projectionSchemaVersion: projection.schemaVersion,
    generatedAt: projection.generatedAt,
    source: projection.source,
    counts: projection.counts,
    chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
    tables: TARGET_ARCHITECTURE_TABLES.map((table) =>
      buildTableManifest(projection, table),
    ),
  };
}

export function buildTargetArchitectureTableExport(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
): TargetArchitectureTableExport {
  const rows = getTargetArchitectureRows(projection, table);
  const chunkCount = getChunkCount(rows.length);
  if (chunkCount <= 1) {
    return {
      schemaVersion: "thesis_target_architecture_table_v1",
      projectionSchemaVersion: projection.schemaVersion,
      generatedAt: projection.generatedAt,
      table,
      rowCount: rows.length,
      chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
      chunkCount,
      rows,
    };
  }
  return {
    schemaVersion: "thesis_target_architecture_table_v1",
    projectionSchemaVersion: projection.schemaVersion,
    generatedAt: projection.generatedAt,
    table,
    rowCount: rows.length,
    chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
    chunkCount,
    chunks: buildChunkManifests(table, rows.length),
  };
}

export function buildTargetArchitectureChunkExport(
  projection: ThesisTargetArchitectureProjection,
  table: TargetArchitectureTableKey,
  chunkIndex: number,
): TargetArchitectureChunkExport {
  const rows = getTargetArchitectureRows(projection, table);
  const start = chunkIndex * TARGET_ARCHITECTURE_CHUNK_SIZE;
  const chunkRows = rows.slice(start, start + TARGET_ARCHITECTURE_CHUNK_SIZE);
  return {
    schemaVersion: "thesis_target_architecture_chunk_v1",
    projectionSchemaVersion: projection.schemaVersion,
    generatedAt: projection.generatedAt,
    table,
    chunkIndex,
    chunkSize: TARGET_ARCHITECTURE_CHUNK_SIZE,
    rowCount: chunkRows.length,
    rows: chunkRows,
  };
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
  return {
    table,
    rowCount: rows.length,
    url: `/forecasts/targets/${table}/manifest.json`,
    chunkCount: getChunkCount(rows.length),
    chunks: buildChunkManifests(table, rows.length),
  };
}

function buildChunkManifests(
  table: TargetArchitectureTableKey,
  rowCount: number,
): TargetArchitectureChunkManifest[] {
  return Array.from({ length: getChunkCount(rowCount) }, (_, index) => ({
    index,
    rowCount: Math.min(
      TARGET_ARCHITECTURE_CHUNK_SIZE,
      Math.max(0, rowCount - index * TARGET_ARCHITECTURE_CHUNK_SIZE),
    ),
    url: `/forecasts/targets/${table}/${index}.json`,
  }));
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
