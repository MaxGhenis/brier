// Deployment canary: which commit produced the running build. The recorder
// checks this against the commit it intends to attest, so a skipped or
// stale deployment can never be recorded as if it were live (finding F13).
export const dynamic = "force-static";

export function GET() {
  return Response.json({
    commit: process.env.VERCEL_GIT_COMMIT_SHA ?? "local-dev",
    ref: process.env.VERCEL_GIT_COMMIT_REF ?? null,
    builtAt: new Date().toISOString(),
  });
}
