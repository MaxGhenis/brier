import {
  buildTargetArchitectureChunkExport,
  buildTargetArchitectureManifest,
  isTargetArchitectureTableKey,
} from "@/data/thesis-target-architecture-export";
import { loadTargetArchitectureProjection } from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

interface TargetChunkRouteContext {
  params: Promise<{}>;
}

export async function GET(request: Request, _context: TargetChunkRouteContext) {
  const { table, chunk } = getTableAndChunkFromPath(request.url);
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

function getTableAndChunkFromPath(url: string) {
  const segments = new URL(url).pathname.split("/").filter(Boolean);
  const chunk = segments.at(-1)?.replace(/\.json$/, "") ?? "";
  const table = segments.at(-2) ?? "";
  return { table, chunk };
}
