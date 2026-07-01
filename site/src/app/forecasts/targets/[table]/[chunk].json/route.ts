import {
  buildTargetArchitectureChunkExport,
  buildTargetArchitectureManifest,
  isTargetArchitectureTableKey,
} from "@/data/thesis-target-architecture-export";
import { loadTargetArchitectureProjection } from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

interface TargetChunkRouteContext {
  params: Promise<{ table: string; chunk: string }>;
}

export async function GET(_request: Request, context: TargetChunkRouteContext) {
  // Use the resolved route params, not request.url: behind the app-host
  // rewrite Vercel hands the handler a URL whose shape differs from `next
  // start`, and string-parsing it 404'd every chunk in production.
  const params = await context.params;
  const table = params.table;
  const chunk = params.chunk.replace(/\.json$/, "");
  if (!isTargetArchitectureTableKey(table)) {
    return Response.json(
      {
        error: "unknown_target_architecture_table",
        table,
      },
      { status: 404 },
    );
  }

  const chunkIndex = Number(chunk);
  if (!Number.isInteger(chunkIndex) || chunkIndex < 0) {
    return Response.json(
      {
        error: "unknown_target_architecture_chunk",
        table,
        chunk,
      },
      { status: 404 },
    );
  }

  const projection = await loadTargetArchitectureProjection();
  const manifest = buildTargetArchitectureManifest(projection);
  const tableManifest = manifest.tables.find(
    (candidate) => candidate.table === table,
  );
  if (!tableManifest || chunkIndex >= tableManifest.chunkCount) {
    return Response.json(
      {
        error: "unknown_target_architecture_chunk",
        table,
        chunk,
      },
      { status: 404 },
    );
  }

  return Response.json(
    buildTargetArchitectureChunkExport(projection, table, chunkIndex),
  );
}
