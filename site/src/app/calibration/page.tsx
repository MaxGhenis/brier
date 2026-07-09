import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/Header";
import { FORECAST_CELLS, formatValue } from "@/data/forecast-cells";
import {
  buildPredictionSpecs,
  buildRecordedPredictionRunRecords,
} from "@/data/prediction-specs";
import { buildBrierRewardExport } from "@/data/brier-lab";
import {
  loadPolicyEngineLedger,
  scoreResolvedForecasts,
  withResolvedOutcomes,
} from "@/data/thesis-log";

export const metadata: Metadata = {
  title: "Calibration — Thesis Institute",
  description:
    "The public scoreboard: interval coverage, CRPS against persistence baselines, and per-agent calibration for every resolved Thesis forecast.",
};

const BASELINE_AGENT_PREFIX = "brier.time_series_prior";

function formatCrps(value: number | null): string {
  return value === null ? "—" : value.toFixed(3);
}

function formatCoverage(value: number | null): string {
  return value === null ? "—" : `${Math.round(value * 100)}%`;
}

export default async function CalibrationPage() {
  const ledger = await loadPolicyEngineLedger();
  const forecasts = withResolvedOutcomes(FORECAST_CELLS, ledger);
  const specs = buildPredictionSpecs(forecasts);
  const runs = buildRecordedPredictionRunRecords(forecasts, specs);
  const rewardExport = buildBrierRewardExport({
    forecasts,
    specs,
    runs,
    ledger,
  });
  const allScores = scoreResolvedForecasts(forecasts, ledger);
  // The headline track record is chronology-verified scores only: the run's
  // recorded time provably precedes the observation. Everything else stays
  // published below the fold, outside the official numbers.
  const scores = allScores.filter((score) => score.chronology === "verified");
  const provisionalCount = allScores.filter(
    (score) => score.chronology === "unverified",
  ).length;
  const violatedCount = allScores.filter(
    (score) => score.chronology === "violated",
  ).length;

  const covered = scores.filter((score) => score.interval80Covered).length;
  const coverage = scores.length > 0 ? covered / scores.length : null;
  const meanNormalizedCrps =
    scores.length > 0
      ? scores.reduce((total, score) => total + score.normalizedCrps, 0) /
        scores.length
      : null;
  const meanSharpness =
    scores.length > 0
      ? scores.reduce((total, score) => total + score.sharpness, 0) /
        scores.length
      : null;

  const leaderboard = [...rewardExport.leaderboard].sort((left, right) => {
    if (left.meanPairedSkill === null) return 1;
    if (right.meanPairedSkill === null) return -1;
    return left.meanPairedSkill - right.meanPairedSkill;
  });

  const cellBySlug = new Map(forecasts.map((cell) => [cell.slug, cell]));
  const recentScores = [...scores]
    .sort((left, right) => {
      const a = cellBySlug.get(left.forecastSlug)?.resolutionDate ?? "";
      const b = cellBySlug.get(right.forecastSlug)?.resolutionDate ?? "";
      return b.localeCompare(a);
    })
    .slice(0, 12);

  const splits = rewardExport.splits;

  return (
    <div>
      <Header activePage="calibration" />
      <main className="mx-auto max-w-[1200px] px-8 pb-32 pt-12 max-md:px-5">
        <p
          className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.14em]"
          style={{ color: "var(--theme-text-muted)" }}
        >
          The scoreboard
        </p>
        <h1
          className="mt-2 [font-family:var(--font-display)] text-[2rem] font-semibold tracking-[-0.01em]"
          style={{ color: "var(--theme-text)" }}
        >
          Calibration
        </h1>
        <p
          className="mt-3 max-w-[640px] text-[0.95rem] leading-[1.6]"
          style={{ color: "var(--theme-text-muted)" }}
        >
          Every forecast publishes an 80% interval before resolution and is
          graded against the official first print when it lands. This page is
          computed from the same records that back{" "}
          <a href="/log.json">log.json</a> and{" "}
          <a href="/brier/reward.json">reward.json</a>; the daily
          pre-registration chain lives in the{" "}
          <a href="https://github.com/MaxGhenis/brier/tree/main/records">
            public records repository
          </a>
          .
        </p>
        <p
          className="mt-3 max-w-[640px] text-[0.85rem] leading-[1.6]"
          style={{ color: "var(--theme-text-muted)" }}
        >
          Scoring methodology v2 (re-stated 2026-07-09): headline numbers count
          only chronology-verified scores — the run&rsquo;s recorded time
          provably precedes the observation — and CRPS is normalized by each
          target&rsquo;s pre-registered historical dispersion rather than the
          forecast&rsquo;s own interval width, so widening an interval can no
          longer improve a score. Legacy runs without verifiable timestamps stay
          published in <a href="/log.json">log.json</a>, flagged, outside the
          headline.
        </p>

        <section className="mt-10 grid grid-cols-4 gap-4 max-md:grid-cols-2">
          {[
            {
              label: "Scored forecasts",
              value: String(scores.length),
              detail: `chronology-verified; ${(
                provisionalCount + violatedCount
              ).toLocaleString()} legacy scores excluded, ${rewardExport.counts.unresolvedRuns.toLocaleString()} runs awaiting resolution`,
            },
            {
              label: "80% interval coverage",
              value: formatCoverage(coverage),
              detail: `${covered} of ${scores.length} observed inside the stated interval`,
            },
            {
              label: "Unpaired mean normalized CRPS",
              value: formatCrps(meanNormalizedCrps),
              detail: `Lower is better; scaled by each target's pre-registered historical dispersion, not the forecast's own width. Mean sharpness ${
                meanSharpness === null ? "—" : meanSharpness.toFixed(2)
              }× target scale.`,
            },
            {
              label: "Paired skill vs persistence",
              value: formatCrps(
                rewardExport.pairedComparison
                  .meanAgentMinusBaselineNormalizedCrps,
              ),
              detail:
                rewardExport.pairedComparison.pairedTargets > 0
                  ? `Agent nCRPS minus baseline nCRPS on ${rewardExport.pairedComparison.pairedTargets} matched targets; ${formatCoverage(rewardExport.pairedComparison.agentWinRate)} agent win rate`
                  : "No ledger-backed baseline pairs scored yet",
            },
          ].map((stat) => (
            <div
              key={stat.label}
              className="rounded-[14px] border p-5"
              style={{
                borderColor: "var(--theme-border)",
                backgroundColor: "var(--theme-card-bg)",
              }}
            >
              <div
                className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.12em]"
                style={{ color: "var(--theme-text-muted)" }}
              >
                {stat.label}
              </div>
              <div
                className="mt-2 [font-family:var(--font-display)] text-[1.7rem] font-semibold"
                style={{ color: "var(--theme-text)" }}
              >
                {stat.value}
              </div>
              <div
                className="mt-1 text-[0.74rem] leading-[1.5]"
                style={{ color: "var(--theme-text-muted)" }}
              >
                {stat.detail}
              </div>
            </div>
          ))}
        </section>

        <section className="mt-14">
          <h2
            className="[font-family:var(--font-display)] text-[1.3rem] font-semibold"
            style={{ color: "var(--theme-text)" }}
          >
            Agents against the baseline
          </h2>
          <p
            className="mt-2 max-w-[640px] text-[0.88rem] leading-[1.6]"
            style={{ color: "var(--theme-text-muted)" }}
          >
            Paired agent-minus-baseline normalized CRPS per target, lowest
            (best) first. Unpaired means remain visible for context. The
            persistence baseline forecasts every target as its last official
            print with a realized-volatility interval — an agent earns its place
            by beating it. Rows with few scored runs are noisy; read them
            accordingly.
          </p>
          <div
            className="mt-5 overflow-x-auto rounded-[14px] border"
            style={{ borderColor: "var(--theme-border)" }}
          >
            <table className="w-full border-collapse text-[0.84rem]">
              <thead>
                <tr
                  className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em]"
                  style={{ color: "var(--theme-text-muted)" }}
                >
                  <th className="px-4 py-3 text-left font-normal">Agent</th>
                  <th className="px-4 py-3 text-right font-normal">
                    Scored / total runs
                  </th>
                  <th className="px-4 py-3 text-right font-normal">
                    Mean paired skill
                  </th>
                  <th className="px-4 py-3 text-right font-normal">
                    Paired win rate
                  </th>
                  <th className="px-4 py-3 text-right font-normal">
                    Unpaired mean nCRPS
                  </th>
                  <th className="px-4 py-3 text-right font-normal">
                    80% coverage
                  </th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((row) => {
                  const isBaseline = row.agent.startsWith(
                    BASELINE_AGENT_PREFIX,
                  );
                  return (
                    <tr
                      key={`${row.agent}-${row.model ?? ""}`}
                      className="border-t"
                      style={{
                        borderColor: "var(--theme-border)",
                        backgroundColor: isBaseline
                          ? "var(--theme-card-bg)"
                          : undefined,
                      }}
                    >
                      <td
                        className="px-4 py-3"
                        style={{ color: "var(--theme-text)" }}
                      >
                        {row.agent}
                        {row.model ? (
                          <span
                            className="ml-2 text-[0.72rem]"
                            style={{ color: "var(--theme-text-muted)" }}
                          >
                            {row.model}
                          </span>
                        ) : null}
                        {isBaseline ? (
                          <span
                            className="ml-2 rounded-full border px-2 py-[1px] [font-family:var(--font-mono)] text-[0.56rem] uppercase tracking-[0.1em]"
                            style={{
                              borderColor: "var(--theme-border)",
                              color: "var(--theme-text-muted)",
                            }}
                          >
                            baseline
                          </span>
                        ) : null}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text-muted)" }}
                      >
                        {row.scoredRuns} / {row.totalRuns}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text)" }}
                      >
                        {formatCrps(row.meanPairedSkill)}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text-muted)" }}
                      >
                        {formatCoverage(row.pairedWinRate)}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text)" }}
                      >
                        {formatCrps(row.unpairedMeanNormalizedCrps)}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text-muted)" }}
                      >
                        {formatCoverage(row.unpairedInterval80Coverage)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mt-14">
          <h2
            className="[font-family:var(--font-display)] text-[1.3rem] font-semibold"
            style={{ color: "var(--theme-text)" }}
          >
            Evaluation splits
          </h2>
          <p
            className="mt-2 max-w-[640px] text-[0.88rem] leading-[1.6]"
            style={{ color: "var(--theme-text-muted)" }}
          >
            {rewardExport.noLeakagePolicy.rule}
          </p>
          <div className="mt-5 grid grid-cols-4 gap-4 max-md:grid-cols-2">
            {(
              Object.entries(splits) as [
                keyof typeof splits,
                (typeof splits)[keyof typeof splits],
              ][]
            ).map(([name, split]) => (
              <div
                key={name}
                className="rounded-[14px] border p-5"
                style={{
                  borderColor: "var(--theme-border)",
                  backgroundColor: "var(--theme-card-bg)",
                }}
              >
                <div
                  className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.12em]"
                  style={{ color: "var(--theme-text-muted)" }}
                >
                  {name}
                </div>
                <div
                  className="mt-2 [font-family:var(--font-display)] text-[1.35rem] font-semibold"
                  style={{ color: "var(--theme-text)" }}
                >
                  {split.scoredRuns}
                  <span
                    className="text-[0.85rem] font-normal"
                    style={{ color: "var(--theme-text-muted)" }}
                  >
                    {" "}
                    / {split.runs}
                  </span>
                </div>
                <div
                  className="mt-1 text-[0.72rem] leading-[1.5]"
                  style={{ color: "var(--theme-text-muted)" }}
                >
                  {split.rule}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-14">
          <h2
            className="[font-family:var(--font-display)] text-[1.3rem] font-semibold"
            style={{ color: "var(--theme-text)" }}
          >
            Latest resolutions
          </h2>
          <div
            className="mt-5 overflow-x-auto rounded-[14px] border"
            style={{ borderColor: "var(--theme-border)" }}
          >
            <table className="w-full border-collapse text-[0.84rem]">
              <thead>
                <tr
                  className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em]"
                  style={{ color: "var(--theme-text-muted)" }}
                >
                  <th className="px-4 py-3 text-left font-normal">Forecast</th>
                  <th className="px-4 py-3 text-right font-normal">
                    Predicted
                  </th>
                  <th className="px-4 py-3 text-right font-normal">Observed</th>
                  <th className="px-4 py-3 text-right font-normal">
                    In interval
                  </th>
                  <th className="px-4 py-3 text-right font-normal">
                    Elicitation
                  </th>
                  <th className="px-4 py-3 text-right font-normal">
                    Normalized CRPS
                  </th>
                </tr>
              </thead>
              <tbody>
                {recentScores.map((score) => {
                  const cell = cellBySlug.get(score.forecastSlug);
                  return (
                    <tr
                      key={score.scoreId}
                      className="border-t"
                      style={{ borderColor: "var(--theme-border)" }}
                    >
                      <td className="px-4 py-3">
                        <Link
                          href={`/${score.forecastSlug}`}
                          style={{ color: "var(--theme-text)" }}
                        >
                          {cell?.title ?? score.forecastSlug}
                        </Link>
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text-muted)" }}
                      >
                        {cell
                          ? formatValue(score.pointEstimate, cell.unit)
                          : score.pointEstimate}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text)" }}
                      >
                        {cell
                          ? formatValue(score.observedValue, cell.unit)
                          : score.observedValue}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{
                          color: score.interval80Covered
                            ? "var(--theme-text-muted)"
                            : "#A94E80",
                        }}
                      >
                        {score.interval80Covered ? "yes" : "no"}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)] text-[0.68rem] uppercase"
                        style={{ color: "var(--theme-text-muted)" }}
                      >
                        {score.distributionProvenance.replace("_", " ")}
                      </td>
                      <td
                        className="px-4 py-3 text-right [font-family:var(--font-mono)]"
                        style={{ color: "var(--theme-text)" }}
                      >
                        {formatCrps(score.normalizedCrps)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <p
            className="mt-4 text-[0.82rem]"
            style={{ color: "var(--theme-text-muted)" }}
          >
            Full history: <Link href="/log">the Thesis Log</Link> · method:{" "}
            <Link href="/thesis">why forecasting is the harness</Link>
          </p>
        </section>
      </main>
    </div>
  );
}
