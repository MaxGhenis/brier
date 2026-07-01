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

// Suffixed dynamic segments ([table].json) expose no route params (Next types
// them Promise<{}>), so the segment comes from the URL. Strip .json
// repeatedly: behind the app-host rewrite Vercel reconstructs the handler URL
// with the suffix doubled (…/targets.json.json) while next start passes it
// singly — stripping once 404'd every table in production.
function getTableFromPath(url: string) {
  const pathname = new URL(url).pathname;
  const lastSegment = pathname.split("/").filter(Boolean).at(-1) ?? "";
  return lastSegment.replace(/(\.json)+$/, "");
}
