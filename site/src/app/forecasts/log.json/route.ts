import { buildThesisLogManifest } from "@/data/thesis-log";
import { loadThesisLogData } from "@/data/thesis-log-runtime";

export const dynamic = "force-static";

export async function GET() {
  return Response.json(buildThesisLogManifest(await loadThesisLogData()));
}
