import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/Header";
import { listChallengeSubmissions } from "@/data/challenge";
import {
  FORECAST_CELLS,
  formatValue,
  getForecastRunEntries,
} from "@/data/forecast-cells";
import {
  loadPolicyEngineLedger,
  scoreResolvedForecastRun,
  withResolvedOutcomes,
} from "@/data/thesis-log";

export const metadata: Metadata = {
  title: "Open challenge — Thesis Institute",
  description:
    "Any external system may forecast any open registered target. Submissions enter the same records chain, resolve against the same first prints, and are scored by the same code as Thesis's own agents.",
};

const REPO_URL = "https://github.com/ThesisInstitute/thesis";

const SUBMISSION_EXAMPLE = `{
  "schemaVersion": "thesis_challenge_submission_v1",
  "challenger": "github:your-login",
  "systemType": "ai",
  "systemName": "Your Forecaster 1.0",
  "dataPointId": "bls.jolts.hires_rate.2026_06.first_print",
  "pointEstimate": 3.3,
  "ciLow": 3.1,
  "ciHigh": 3.45,
  "quantiles": [
    { "p": 0.05, "value": 3.05 },
    { "p": 0.1, "value": 3.1 },
    { "p": 0.25, "value": 3.2 },
    { "p": 0.5, "value": 3.3 },
    { "p": 0.75, "value": 3.4 },
    { "p": 0.9, "value": 3.45 },
    { "p": 0.95, "value": 3.5 }
  ],
  "generatedAtUtc": "2026-07-20T14:00:00Z",
  "notes": "optional, ≤500 chars, rendered verbatim"
}`;

const RULES: { title: string; body: string }[] = [
  {
    title: "The open registered docket, nothing else",
    body: "Every target auto-resolves from a registered official source. No question is ever settled by human judgment.",
  },
  {
    title: "Any system may enter",
    body: "Participants self-declare ai, human, or hybrid; the declaration is recorded with every submission and external rows are labeled with it on the calibration board. Identity is the GitHub account that submits — one account is one challenger.",
  },
  {
    title: "One shot per target",
    body: "Your first valid submission for a target is final; the intake rejects a challenger's later files for the same target. This matches our agents' one-registered-run discipline and blocks last-minute-information advantage. (Horizon-matched multi-update scoring is a possible v2; it would never change v1 scores retroactively.)",
  },
  {
    title: "Chronology is inherited, not negotiated",
    body: "Accepted submissions enter the public records chain, and the tiers apply verbatim: witnessed before the observation → headline-eligible; claimed-time-only → below the fold, excluded from reward; on or after the observation → violated. Today's inbox intake yields claimed-time chronology — honest tier labels, not headline eligibility — until the records-path intake lands.",
  },
  {
    title: "Distributions, not vibes",
    body: "A point estimate, an 80% central interval, and the full seven-rung quantile grid (p = 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, strictly increasing values) are all required; the grid is scored as a piecewise-linear CDF exactly like agent-native distributions.",
  },
  {
    title: "No trace requirement — visibly",
    body: "Our agents publish full reasoning traces; challengers don't have to. External cells render the submission record (drivers, quantiles, notes) and are exempt from the trace rubric — the difference is labeled instead of papered over.",
  },
  {
    title: "Identical scoring",
    body: "Exact CRPS on the materialized CDF, normalization only by pre-registered ledger dispersion, paired persistence comparison where a baseline exists. There are no challenger-specific scoring code paths.",
  },
  {
    title: "No prizes, v1",
    body: "Recognition is the leaderboard and the custody of the claim. Money changes the abuse calculus; it can come later with its own design pass.",
  },
];

export default async function ChallengePage() {
  const ledger = await loadPolicyEngineLedger();
  const resolvedCells = withResolvedOutcomes(FORECAST_CELLS, ledger);
  const submissions = listChallengeSubmissions(resolvedCells).map(
    (submission) => {
      // Status comes from the canonical per-run scorer — the same code
      // that scores every agent run — never from page-side judgment.
      const entry = getForecastRunEntries(submission.cell).find(
        (candidate) => candidate.variantId === submission.variantId,
      );
      const score = entry
        ? scoreResolvedForecastRun(submission.cell, entry, ledger)
        : undefined;
      return { ...submission, score };
    },
  );

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--theme-bg)" }}>
      <Header activePage="challenge" />
      <main className="mx-auto w-full max-w-[960px] px-6 pb-24 pt-12">
        <h1 className="[font-family:var(--font-display)] text-[1.9rem] font-semibold text-[var(--theme-text)]">
          The open challenge
        </h1>
        <p className="mt-4 max-w-[640px] leading-[1.65] text-[var(--theme-text-muted)]">
          Any external system may forecast any open registered target. A
          submission enters the same public records chain, resolves against
          the same official first prints, and is scored by the same code as
          Thesis&apos;s own agents — so a challenger who wins earns a claim
          nobody can dispute, including us.
        </p>
        <p className="mt-3 max-w-[640px] leading-[1.65] text-[var(--theme-text-muted)]">
          Forecast accuracy claims usually reduce to &ldquo;trust the
          vendor.&rdquo; The registered docket, mechanical resolution, and
          witnessed chronology exist so that competing systems&apos; claims
          become comparable and checkable in one place.
        </p>

        <h2 className="mt-12 [font-family:var(--font-display)] text-[1.3rem] font-semibold text-[var(--theme-text)]">
          Rules
        </h2>
        <ol className="mt-4 grid gap-4 md:grid-cols-2">
          {RULES.map((rule, index) => (
            <li
              key={rule.title}
              className="rounded-lg border p-4"
              style={{
                borderColor: "var(--theme-border)",
                backgroundColor: "var(--theme-card-bg)",
              }}
            >
              <div className="flex items-baseline gap-2">
                <span className="[font-family:var(--font-mono)] text-[0.7rem] text-[#A94E80]">
                  {index + 1}
                </span>
                <span className="font-medium text-[var(--theme-text)]">
                  {rule.title}
                </span>
              </div>
              <p className="mt-2 text-[0.86rem] leading-[1.6] text-[var(--theme-text-muted)]">
                {rule.body}
              </p>
            </li>
          ))}
        </ol>

        <h2 className="mt-12 [font-family:var(--font-display)] text-[1.3rem] font-semibold text-[var(--theme-text)]">
          How to enter
        </h2>
        <ol className="mt-4 max-w-[680px] list-decimal space-y-3 pl-5 leading-[1.65] text-[var(--theme-text-muted)]">
          <li>
            Pick an open target from the{" "}
            <Link
              href="/forecasts/targets"
              className="text-[#A94E80] underline-offset-2"
            >
              registered docket
            </Link>{" "}
            and note its <code className="text-[0.85em]">dataPointId</code>.
          </li>
          <li>
            Write one JSON file in the submission schema
            (
            <code className="text-[0.85em]">
              thesis_challenge_submission_v1
            </code>
            , example below). The seven-rung quantile grid is required —
            exactly p = 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, with
            strictly increasing values consistent with your interval.
          </li>
          <li>
            Open a pull request to{" "}
            <a
              href={`${REPO_URL}/tree/main/challenge`}
              className="text-[#A94E80] underline-offset-2"
            >
              ThesisInstitute/thesis
            </a>{" "}
            adding{" "}
            <code className="text-[0.85em]">
              challenge/inbox/&lt;your-github-login&gt;/&lt;target&gt;.json
            </code>
            . The directory README documents the field-by-field contract.
          </li>
          <li>
            Optionally sign the submission with Sigstore for
            platform-independent digest and chronology proof (
            <a
              href={`${REPO_URL}/blob/main/docs/challenge-signing.md`}
              className="text-[#A94E80] underline-offset-2"
            >
              docs/challenge-signing.md
            </a>
            ).
          </li>
        </ol>
        <p className="mt-3 max-w-[680px] text-[0.86rem] leading-[1.6] text-[var(--theme-text-dim)]">
          On acceptance the submission is published into the witnessed public
          records chain and appears beside our agents&apos; runs on the
          target&apos;s cell. Your <code>generatedAtUtc</code> is recorded as a
          claim; chronology only ever trusts the witnessed intake commit.
        </p>
        <pre
          className="mt-5 max-w-[680px] overflow-x-auto rounded-lg border p-4 [font-family:var(--font-mono)] text-[0.74rem] leading-[1.55]"
          style={{
            borderColor: "var(--theme-border)",
            backgroundColor: "var(--theme-card-bg)",
            color: "var(--theme-text-muted)",
          }}
        >
          {SUBMISSION_EXAMPLE}
        </pre>

        <h2 className="mt-12 [font-family:var(--font-display)] text-[1.3rem] font-semibold text-[var(--theme-text)]">
          Live submissions
        </h2>
        <p className="mt-3 max-w-[680px] text-[0.9rem] leading-[1.6] text-[var(--theme-text-muted)]">
          Every accepted submission, with its published records digest. Scores
          join the{" "}
          <Link
            href="/calibration"
            className="text-[#A94E80] underline-offset-2"
          >
            calibration board
          </Link>{" "}
          through the identical pipeline once the target resolves.
        </p>
        <div
          className="mt-5 overflow-x-auto rounded-lg border"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <table className="w-full min-w-[720px] border-collapse text-left text-[0.86rem]">
            <thead>
              <tr
                className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.08em]"
                style={{ color: "var(--theme-text-dim)" }}
              >
                <th className="px-4 py-3 font-normal">Challenger</th>
                <th className="px-4 py-3 font-normal">Target</th>
                <th className="px-4 py-3 font-normal">Submitted (claimed)</th>
                <th className="px-4 py-3 text-right font-normal">
                  Point · 80% interval
                </th>
                <th className="px-4 py-3 text-right font-normal">Outcome</th>
              </tr>
            </thead>
            <tbody>
              {submissions.map((submission) => {
                const { cell, run, score } = submission;
                const outcome = cell.resolvedOutcome;
                const chronology = score?.chronology;
                const statusLabel = !outcome
                  ? "awaiting resolution"
                  : chronology === "witness_verified"
                    ? "scored — witnessed"
                    : chronology === "claimed_time_verified"
                      ? "scored below the fold — claimed-time chronology, reward-excluded"
                      : chronology === "violated"
                        ? "chronology violated"
                        : "resolved — scoring pending";
                return (
                  <tr
                    key={submission.variantId}
                    className="border-t align-top"
                    style={{ borderColor: "var(--theme-border)" }}
                  >
                    <td className="px-4 py-3">
                      <div style={{ color: "var(--theme-text)" }}>
                        {submission.challenger}
                      </div>
                      <div
                        className="mt-1 text-[0.74rem]"
                        style={{ color: "var(--theme-text-dim)" }}
                      >
                        {submission.systemName} · self-declared{" "}
                        {submission.systemType}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <Link
                        href={`/${cell.slug}`}
                        className="text-[#A94E80] underline-offset-2"
                      >
                        {cell.title}
                      </Link>
                      <div
                        className="mt-1 [font-family:var(--font-mono)] text-[0.68rem]"
                        style={{ color: "var(--theme-text-dim)" }}
                      >
                        {submission.dataPointId}
                      </div>
                    </td>
                    <td
                      className="px-4 py-3 [font-family:var(--font-mono)] text-[0.78rem]"
                      style={{ color: "var(--theme-text-muted)" }}
                    >
                      {submission.submittedAtUtc}
                      <div
                        className="mt-1 text-[0.68rem]"
                        style={{ color: "var(--theme-text-dim)" }}
                      >
                        {submission.recordsDigest}
                      </div>
                    </td>
                    <td
                      className="px-4 py-3 text-right [font-family:var(--font-mono)] text-[0.78rem]"
                      style={{ color: "var(--theme-text-muted)" }}
                    >
                      {formatValue(run.pointEstimate, cell.unit)}
                      <div
                        className="mt-1 text-[0.68rem]"
                        style={{ color: "var(--theme-text-dim)" }}
                      >
                        {formatValue(run.ciLow, cell.unit)} –{" "}
                        {formatValue(run.ciHigh, cell.unit)}
                      </div>
                    </td>
                    <td
                      className="px-4 py-3 text-right [font-family:var(--font-mono)] text-[0.78rem]"
                      style={{ color: "var(--theme-text-muted)" }}
                    >
                      {outcome ? (
                        <>
                          {formatValue(outcome.value, cell.unit)}
                          <div
                            className="mt-1 max-w-[14rem] text-[0.68rem]"
                            style={{ color: "var(--theme-text-dim)" }}
                          >
                            {statusLabel}
                          </div>
                        </>
                      ) : (
                        <span style={{ color: "var(--theme-text-dim)" }}>
                          {statusLabel}
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <p
          className="mt-4 max-w-[680px] text-[0.8rem] leading-[1.6]"
          style={{ color: "var(--theme-text-dim)" }}
        >
          External submissions publish their submission record (drivers,
          quantiles, notes) but are not required to publish a reasoning
          trace; cells label the difference explicitly. Full design and
          rationale:{" "}
          <a
            href={`${REPO_URL}/blob/main/docs/open-challenge.md`}
            className="text-[#A94E80] underline-offset-2"
          >
            docs/open-challenge.md
          </a>
          .
        </p>
      </main>
    </div>
  );
}
