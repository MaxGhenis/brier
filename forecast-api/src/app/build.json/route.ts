// Immutable deployment identity for recorder pinning. The recorder reads this
// from the mutable API alias once, then captures every SSE stream from the
// returned deployment URL and verifies the alias did not move mid-snapshot.
export const dynamic = "force-static";

export function GET() {
  return Response.json({
    commit: process.env.VERCEL_GIT_COMMIT_SHA ?? "local-dev",
    ref: process.env.VERCEL_GIT_COMMIT_REF ?? null,
    deploymentUrl: process.env.VERCEL_URL ?? null,
    deploymentId: process.env.VERCEL_DEPLOYMENT_ID ?? null,
    branchUrl: process.env.VERCEL_BRANCH_URL ?? null,
    builtAt: new Date().toISOString(),
    service: "thesis-forecast-api",
  });
}
