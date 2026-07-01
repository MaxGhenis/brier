import {
  buildTargetArchitectureTableExport,
  isTargetArchitectureTableKey,
} from "@/data/thesis-target-architecture-export";
import { loadTargetArchitectureProjection } from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

interface TargetTableRouteContext {
  params: Promise<{}>;
}

export async function GET(request: Request, _context: TargetTableRouteContext) {
  const table = getTableFromPath(request.url);
  if (!isTargetArchitectureTableKey(table)) {
    return Response.json(
      {
        error: "unknown_target_architecture_table",
        table,
      },
      { status: 404 },
    );
  }

  const projection = await loadTargetArchitectureProjection();
  return Response.json(buildTargetArchitectureTableExport(projection, table));
}

function getTableFromPath(url: string) {
  const pathname = new URL(url).pathname;
  const lastSegment = pathname.split("/").filter(Boolean).at(-1) ?? "";
  return lastSegment.replace(/\.json$/, "");
}
