import {
  buildTargetArchitectureTableExport,
  isTargetArchitectureTableKey,
} from "@/data/thesis-target-architecture-export";
import { loadTargetArchitectureProjection } from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

interface TargetTableRouteContext {
  params: Promise<{ table: string }>;
}

export async function GET(_request: Request, context: TargetTableRouteContext) {
  // Use the resolved route param, not request.url — see [chunk].json/route.ts.
  const params = await context.params;
  const table = params.table.replace(/\.json$/, "");
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
