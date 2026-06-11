import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/Header";
import {
  COUNTRY_LABEL,
  FORECAST_CELLS,
  formatValue,
  getForecastCountry,
  getResolutionResult,
  type ForecastCell,
} from "@/data/forecast-cells";
import {
  buildPredictionSpecs,
  buildRecordedPredictionRunRecords,
  type PredictionRunRecord,
  type PredictionSpec,
} from "@/data/prediction-specs";
import {
  buildThesisLog,
  buildResolutionQueue,
  isPredictionRecordedLogEntry,
  isPredictionResolvedLogEntry,
  loadPolicyEngineLedger,
  scoreResolvedForecasts,
  withResolvedOutcomes,
  type PredictionRecordedLogEntry,
  type PredictionResolvedLogEntry,
  type PredictionResolutionQueueEntry,
  type ResolvedForecastScore,
} from "@/data/thesis-log";

export const metadata: Metadata = {
  title: "Thesis Log — Thesis Institute",
  description: "Prediction records, distributions, traces, and scoring rows.",
  robots: {
    index: false,
    follow: false,
    nocache: true,
    googleBot: {
      index: false,
      follow: false,
      noimageindex: true,
    },
  },
};

export default async function ThesisLogPage() {
  const ledger = await loadPolicyEngineLedger();
  const forecasts = withResolvedOutcomes(FORECAST_CELLS, ledger);
  const specs = buildPredictionSpecs(forecasts);
  const runs = buildRecordedPredictionRunRecords(forecasts, specs);
  const logEntries = buildThesisLog(forecasts);
  const recordedPredictions = logEntries.filter(
    (entry): entry is PredictionRecordedLogEntry =>
      isPredictionRecordedLogEntry(entry),
  );
  const resolutions = logEntries.filter(
    (entry): entry is PredictionResolvedLogEntry =>
      isPredictionResolvedLogEntry(entry),
  );
  const scores = scoreResolvedForecasts(forecasts, ledger);
  const resolutionQueue = buildResolutionQueue(forecasts);
  const visibleResolutionQueue = resolutionQueue.slice(0, 12);

  const intervalCoverage =
    scores.length === 0
      ? null
      : scores.filter((score) => score.interval80Covered).length /
        scores.length;

  return (
    <div>
      <Header activePage="log" />
      <main className="mx-auto max-w-[1200px] px-8 pb-32 pt-12 max-md:px-5">
        <section className="mb-10 max-w-[780px]">
          <Link
            href="/"
            className="mb-5 inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
          >
            ← all forecasts
          </Link>
          <p className="mb-3 [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)]">
            Thesis Log · prediction records
          </p>
          <h1 className="mb-5 [font-family:var(--font-display)] text-[clamp(1.9rem,4vw,2.6rem)] font-light leading-[1.15] tracking-[-0.02em] text-[var(--theme-text)]">
            Thesis Log
          </h1>
          <p className="text-[1.02rem] leading-[1.65] text-[var(--theme-text-muted)]">
            Thesis Log records predictions, distributions, trace metadata,
            resolution links, and scores. Resolved predictions reference facts
            in the PolicyEngine Ledger.
          </p>
          <div className="mt-5 flex flex-wrap gap-4">
            <a
              href="/log.json"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--color-accent)] no-underline hover:no-underline"
            >
              Machine-readable log JSON →
            </a>
            <a
              href="/specs.json"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
            >
              Prediction specs JSON →
            </a>
            <a
              href="/ledger"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
            >
              View facts ledger →
            </a>
          </div>
        </section>

        <section className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-6">
          <MetricCard label="predictions" value={recordedPredictions.length} />
          <MetricCard label="specs" value={specs.length} />
          <MetricCard label="runs" value={runs.length} />
          <MetricCard label="resolved" value={resolutions.length} />
          <MetricCard label="pending" value={resolutionQueue.length} />
          <MetricCard
            label="scored / coverage"
            value={
              intervalCoverage === null
                ? "n/a"
                : `${scores.length} · ${Math.round(intervalCoverage * 100)}%`
            }
          />
        </section>

        <ProductionContractPanel specs={specs} runs={runs} />

        <section
          className="mb-8 rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <div className="mb-5 flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="[font-family:var(--font-display)] text-[1.05rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
              Resolution queue
            </h2>
            <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              {resolutionQueue.length} pending · next 12 shown
            </span>
          </div>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            {visibleResolutionQueue.map((entry) => (
              <ResolutionQueueRow entry={entry} key={entry.forecastSlug} />
            ))}
          </div>
        </section>

        <section
          className="rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <div className="mb-5 flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="[font-family:var(--font-display)] text-[1.05rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
              Recorded predictions
            </h2>
            <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              {recordedPredictions.length} rows · 201-point CDFs
            </span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[920px] border-collapse text-left [font-family:var(--font-body)] text-[0.84rem]">
              <thead>
                <tr className="border-b border-[var(--theme-border)] [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  <th className="py-3 pr-5 font-medium">prediction</th>
                  <th className="py-3 pr-5 font-medium">geo</th>
                  <th className="py-3 pr-5 font-medium">recorded</th>
                  <th className="py-3 pr-5 font-medium">agent</th>
                  <th className="py-3 pr-5 font-medium">estimate</th>
                  <th className="py-3 pr-5 font-medium">80% interval</th>
                  <th className="py-3 font-medium">cdf</th>
                </tr>
              </thead>
              <tbody>
                {recordedPredictions.map((entry) => (
                  <RecordedPredictionRow
                    entry={entry}
                    key={entry.forecastSlug}
                  />
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section
          className="mt-8 rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <div className="mb-5 flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="[font-family:var(--font-display)] text-[1.05rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
              Scored predictions
            </h2>
            <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              {scores.length} rows · facts from Ledger
            </span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[820px] border-collapse text-left [font-family:var(--font-body)] text-[0.84rem]">
              <thead>
                <tr className="border-b border-[var(--theme-border)] [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  <th className="py-3 pr-5 font-medium">prediction</th>
                  <th className="py-3 pr-5 font-medium">geo</th>
                  <th className="py-3 pr-5 font-medium">forecast</th>
                  <th className="py-3 pr-5 font-medium">actual</th>
                  <th className="py-3 pr-5 font-medium">error</th>
                  <th className="py-3 pr-5 font-medium">CRPS</th>
                  <th className="py-3 pr-5 font-medium">PIT</th>
                  <th className="py-3 font-medium">80%</th>
                </tr>
              </thead>
              <tbody>
                {scores.map((score) => {
                  const forecast = getForecastBySlug(
                    score.forecastSlug,
                    forecasts,
                  );
                  if (!forecast) return null;
                  return (
                    <ScoreRow
                      forecast={forecast}
                      key={score.forecastSlug}
                      score={score}
                    />
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

function ProductionContractPanel({
  runs,
  specs,
}: {
  runs: PredictionRunRecord[];
  specs: PredictionSpec[];
}) {
  const failedRuns = runs.filter((run) =>
    run.qualityGates.some((gate) => gate.status === "failed"),
  );
  const warningRuns = runs.filter((run) =>
    run.qualityGates.some((gate) => gate.status === "warning"),
  );
  const sampleRun = runs[0];

  return (
    <section
      className="mb-8 rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <div className="mb-5 flex flex-wrap items-baseline justify-between gap-3">
        <div>
          <p className="mb-2 [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--theme-text-dim)]">
            production contract
          </p>
          <h2 className="[font-family:var(--font-display)] text-[1.05rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
            Specs in, immutable runs out
          </h2>
        </div>
        <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          {failedRuns.length} failed · {warningRuns.length} warnings
        </span>
      </div>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <ContractStep
          label="spec"
          value={`${specs.length} prediction specs`}
          detail="Question, unit, Ledger target ref, allowed tools, CDF schema, and quality gates."
        />
        <ContractStep
          label="runner"
          value={sampleRun?.runner.id ?? "thesis.recorded-agent-runner"}
          detail="Turns a spec and tool context into a public trace, 201-point CDF, and run record."
        />
        <ContractStep
          label="store"
          value="Thesis Log"
          detail="Stores prediction runs and scores; observed facts stay in PolicyEngine Ledger."
        />
      </div>
    </section>
  );
}

function ContractStep({
  detail,
  label,
  value,
}: {
  detail: string;
  label: string;
  value: string;
}) {
  return (
    <div
      className="rounded-lg border bg-[var(--theme-bg-surface)] p-4"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <p className="[font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
        {label}
      </p>
      <p className="mt-2 text-[0.92rem] font-medium text-[var(--theme-text)]">
        {value}
      </p>
      <p className="mt-2 text-[0.78rem] leading-[1.55] text-[var(--theme-text-muted)]">
        {detail}
      </p>
    </div>
  );
}

function MetricCard({
  label,
  value,
}: {
  label: string;
  value: number | string;
}) {
  return (
    <div
      className="rounded-xl border bg-[var(--theme-bg-elevated)] p-5"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
        {label}
      </p>
      <p className="mt-3 [font-family:var(--font-display)] text-[2rem] font-semibold leading-none text-[var(--theme-text)]">
        {value}
      </p>
    </div>
  );
}

function ResolutionQueueRow({
  entry,
}: {
  entry: PredictionResolutionQueueEntry;
}) {
  return (
    <div
      className="rounded-lg border bg-[var(--theme-bg-surface)] p-4"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <Link
            href={`/${entry.forecastSlug}`}
            className="text-[0.92rem] font-medium leading-[1.45] text-[var(--theme-text)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
          >
            {entry.title}
          </Link>
          <p className="mt-2 break-all [font-family:var(--font-mono)] text-[0.66rem] text-[var(--theme-text-dim)]">
            {entry.dataPointId}
          </p>
          <p className="mt-2 text-[0.72rem] leading-[1.45] text-[var(--theme-text-muted)]">
            {entry.resolutionSourceUrl ? (
              <a
                className="text-[var(--theme-text-muted)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
                href={entry.resolutionSourceUrl}
              >
                {entry.resolutionSource}
              </a>
            ) : (
              entry.resolutionSource
            )}
          </p>
        </div>
        <span className="shrink-0 rounded-full border border-[var(--theme-border)] px-2 py-[2px] [font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
          {COUNTRY_LABEL[entry.country]}
        </span>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3 text-[0.78rem] text-[var(--theme-text-muted)]">
        <div>
          <p className="[font-family:var(--font-mono)] text-[0.56rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            resolves
          </p>
          <p className="mt-1 text-[var(--theme-text)]">
            {formatDisplayDate(entry.resolutionDate)}
          </p>
        </div>
        <div>
          <p className="[font-family:var(--font-mono)] text-[0.56rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            estimate
          </p>
          <p className="mt-1 text-[var(--theme-text)]">
            {formatValue(entry.pointEstimate, entry.unit)}
          </p>
        </div>
      </div>
    </div>
  );
}

function RecordedPredictionRow({
  entry,
}: {
  entry: PredictionRecordedLogEntry;
}) {
  const forecast = getForecastBySlug(entry.forecastSlug);
  if (!forecast) return null;

  const country = getForecastCountry(forecast);
  const summary = entry.distribution.summary;
  const interval = summary.interval80;

  return (
    <tr className="border-b border-[var(--theme-border)] last:border-b-0">
      <td className="max-w-[280px] py-4 pr-5 align-top">
        <Link
          href={`/${forecast.slug}`}
          className="text-[var(--theme-text)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
        >
          {forecast.title}
        </Link>
        <div className="mt-1 break-all [font-family:var(--font-mono)] text-[0.68rem] text-[var(--theme-text-dim)]">
          {entry.dataPointId}
        </div>
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text-muted)]">
        {COUNTRY_LABEL[country]}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {entry.recordedAt ? formatLedgerTimestamp(entry.recordedAt) : "seed"}
      </td>
      <td className="max-w-[180px] py-4 pr-5 align-top text-[var(--theme-text-muted)]">
        {entry.agent ?? "prototype seed"}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {formatValue(summary.pointEstimate, forecast.unit)}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {formatValue(interval.lower, forecast.unit)} to{" "}
        {formatValue(interval.upper, forecast.unit).replace(/^\+/, "")}
      </td>
      <td className="py-4 align-top [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
        {entry.distribution.pointCount} points
      </td>
    </tr>
  );
}

function ScoreRow({
  forecast,
  score,
}: {
  forecast: ForecastCell;
  score: ResolvedForecastScore;
}) {
  const country = getForecastCountry(forecast);
  const result = getResolutionResult(forecast);
  const observedValue = forecast.resolvedOutcome?.value;

  return (
    <tr className="border-b border-[var(--theme-border)] last:border-b-0">
      <td className="max-w-[260px] py-4 pr-5 align-top">
        <Link
          href={`/${forecast.slug}`}
          className="text-[var(--theme-text)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
        >
          {forecast.title}
        </Link>
        <div className="mt-1 break-all [font-family:var(--font-mono)] text-[0.68rem] text-[var(--theme-text-dim)]">
          {score.dataPointId}
        </div>
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text-muted)]">
        {COUNTRY_LABEL[country]}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {formatValue(score.pointEstimate, score.unit)}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {observedValue === undefined
          ? "pending"
          : formatValue(observedValue, score.unit)}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {formatSignedValue(score.signedError, score.unit)}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {formatCompactNumber(score.crps)}
      </td>
      <td className="py-4 pr-5 align-top text-[var(--theme-text)]">
        {formatCompactNumber(score.probabilityIntegralTransform)}
      </td>
      <td className="py-4 align-top">
        <span
          className={`rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] ${
            result === "inside"
              ? "border-[var(--color-horizon-300)] bg-[var(--color-horizon-50)] text-[var(--color-horizon-700)]"
              : "border-[#F2DCAF] bg-[#FFF4DD] text-[#7A5C20]"
          }`}
        >
          {result === "inside" ? "inside" : "outside"}
        </span>
      </td>
    </tr>
  );
}

function getForecastBySlug(
  slug: string,
  forecasts: ForecastCell[] = FORECAST_CELLS,
): ForecastCell | undefined {
  return forecasts.find((forecast) => forecast.slug === slug);
}

function formatSignedValue(value: number, unit: ForecastCell["unit"]): string {
  const formatted = formatValue(Math.abs(value), unit).replace(/^\+/, "");
  if (value === 0) return formatted;
  return `${value > 0 ? "+" : "-"}${formatted}`;
}

function formatCompactNumber(value: number): string {
  if (Math.abs(value) >= 100) return value.toFixed(0);
  if (Math.abs(value) >= 10) return value.toFixed(1);
  if (Math.abs(value) >= 1) return value.toFixed(2);
  return value.toPrecision(2);
}

function formatDisplayDate(value: string): string {
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

function formatLedgerTimestamp(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toISOString().slice(0, 10);
}
