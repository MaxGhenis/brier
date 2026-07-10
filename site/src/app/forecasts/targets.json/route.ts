import { loadTargetArchitectureManifest } from "@/data/thesis-target-architecture-runtime";

export const dynamic = "force-static";

export async function GET() {
  return Response.json(await loadTargetArchitectureManifest());
}
