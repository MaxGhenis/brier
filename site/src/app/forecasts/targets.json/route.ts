import { buildTargetArchitectureManifest } from "@/data/thesis-target-architecture-export";
import { loadTargetArchitectureProjection } from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

export async function GET() {
  const projection = await loadTargetArchitectureProjection();
  return Response.json(buildTargetArchitectureManifest(projection));
}
