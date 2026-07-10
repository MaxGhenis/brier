import {
  buildTargetArchitectureChunkExport,
  buildTargetArchitectureTableExport,
  isTargetArchitectureTableKey,
} from "@/data/thesis-target-architecture-export";
import {
  loadTargetArchitectureManifest,
  loadTargetArchitectureProjection,
} from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

interface TargetChunkRouteContext {
  params: Promise<{}>;
}

// Serves /forecasts/targets/{table}/{index}.json (a row chunk) and
// /forecasts/targets/{table}/manifest.json (the per-table manifest). One
// route for both: the suffixed dynamic segment [chunk].json outranks a
// literal manifest.json sibling in routing, and the previous [table].json
// shape never matched requests at all — locally or on Vercel.
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

  const [projection, manifest] = await Promise.all([
    loadTargetArchitectureProjection(),
    loadTargetArchitectureManifest(),
  ]);

  if (chunk === "manifest") {
    return Response.json(
      buildTargetArchitectureTableExport(projection, table, manifest),
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
    buildTargetArchitectureChunkExport(projection, table, chunkIndex, manifest),
  );
}

// Suffixed dynamic segments expose no route params, so the segments come
// from the URL. Strip .json repeatedly: behind the app-host rewrite Vercel
// reconstructs the handler URL with the suffix doubled (…/0.json.json)
// while next start passes it singly — stripping once 404'd every chunk in
// production.
function getTableAndChunkFromPath(url: string) {
  const segments = new URL(url).pathname.split("/").filter(Boolean);
  const chunk = segments.at(-1)?.replace(/(\.json)+$/, "") ?? "";
  const table = segments.at(-2) ?? "";
  return { table, chunk };
}
