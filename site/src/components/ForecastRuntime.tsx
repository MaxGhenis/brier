"use client";

import { useEffect, useRef, useState } from "react";
import { AgentReasoning } from "@/components/AgentReasoning";
import { ForecastTrend, ForecastViz } from "@/components/ForecastViz";
import {
  LIVE_FORECAST_SLUGS,
  formatValue,
  getForecastRuntimeKind,
  getResolutionResult,
  type ForecastCell,
  type PredictionDistribution,
  type ReasoningStep,
} from "@/data/forecast-cells";
import type { ResolvedForecastScore } from "@/data/thesis-log";

type RuntimeMode = "mock" | "connecting" | "live" | "complete" | "fallback";

interface RuntimeForecast {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  confidence: 0.8;
  distribution?: PredictionDistribution;
  source?:
    | "ai_gateway"
    | "deterministic_fallback"
    | "calibration_fallback"
    | "census_calibration_fallback";
  model?: string;
  generatedAt?: string;
  drivers?: string[];
}

interface ActiveTool {
  tool: string;
  call: string;
}

interface ForecastRuntimeProps {
  forecast: ForecastCell;
  resolvedScore?: ResolvedForecastScore;
}

export function ForecastRuntime({
  forecast: forecastCell,
  resolvedScore,
}: ForecastRuntimeProps) {
  const supportsLive = LIVE_FORECAST_SLUGS.has(forecastCell.slug);
  const runtimeKind = getForecastRuntimeKind(forecastCell);
  const [mode, setMode] = useState<RuntimeMode>(
    supportsLive ? "connecting" : "mock",
  );
  const [statusLabel, setStatusLabel] = useState(
    supportsLive
      ? "opening live stream"
      : runtimeKind === "agent-run"
        ? "recorded agent run"
        : "mock replay",
  );
  const [error, setError] = useState<string | null>(null);
  const [activeTool, setActiveTool] = useState<ActiveTool | null>(null);
  const [liveSteps, setLiveSteps] = useState<ReasoningStep[]>([]);
  const [liveForecast, setLiveForecast] = useState<RuntimeForecast | null>(
    null,
  );

  useEffect(() => {
    if (!supportsLive) return;
    if (new URLSearchParams(window.location.search).get("mock") === "1") {
      setMode("mock");
      setStatusLabel("mock replay");
      return;
    }

    let completed = false;
    const source = new EventSource(
      `${resolveApiBase()}/forecasts/${forecastCell.slug}/stream`,
    );

    setMode("connecting");
    setStatusLabel("connecting to live API");
    setError(null);
    setLiveSteps([]);
    setActiveTool(null);

    source.addEventListener("status", (event) => {
      const data = parseEventData<{ label?: string; state?: string }>(event);
      if (!data) return;
      setStatusLabel(data.label ?? "live stream running");
      if (data.state !== "complete") setMode("live");
    });

    source.addEventListener("step", (event) => {
      const step = parseEventData<ReasoningStep>(event);
      if (!step || !isReasoningStep(step)) return;
      setLiveSteps((prev) => [...prev, step]);
      setMode("live");
    });

    source.addEventListener("tool_start", (event) => {
      const data = parseEventData<ActiveTool>(event);
      if (!data) return;
      setActiveTool(data);
      setStatusLabel(`${data.tool} running`);
      setMode("live");
    });

    source.addEventListener("tool_result", (event) => {
      const data = parseEventData<ActiveTool & { result: string }>(event);
      if (!data) return;
      setActiveTool(null);
      setLiveSteps((prev) => [
        ...prev,
        {
          kind: "tool",
          tool: data.tool,
          call: data.call,
          result: data.result,
        },
      ]);
      setStatusLabel(`${data.tool} complete`);
      setMode("live");
    });

    source.addEventListener("forecast", (event) => {
      const forecast = parseEventData<RuntimeForecast>(event);
      if (!forecast) return;
      setLiveForecast(forecast);
      setLiveSteps((prev) => [
        ...prev,
        {
          kind: "forecast",
          point: forecast.pointEstimate,
          ciLow: forecast.ciLow,
          ciHigh: forecast.ciHigh,
        },
      ]);
      setStatusLabel(
        forecast.source === "ai_gateway"
          ? "AI Gateway forecast complete"
          : "fallback forecast complete",
      );
      setMode("complete");
    });

    source.addEventListener("failure", (event) => {
      const data = parseEventData<{ message?: string }>(event);
      setError(data?.message ?? "Live forecast failed.");
      setStatusLabel("live API failed");
      setMode("fallback");
      source.close();
    });

    source.addEventListener("done", () => {
      completed = true;
      setMode("complete");
      source.close();
    });

    source.onerror = () => {
      if (completed) return;
      setError("Could not connect to the live forecast API.");
      setStatusLabel("mock fallback");
      setMode("fallback");
      source.close();
    };

    return () => {
      completed = true;
      source.close();
    };
  }, [forecastCell.slug, supportsLive]);

  const displayedForecast = liveForecast ?? {
    pointEstimate: forecastCell.pointEstimate,
    ciLow: forecastCell.ciLow,
    ciHigh: forecastCell.ciHigh,
    confidence: 0.8 as const,
  };
  const drivers =
    liveForecast?.drivers && liveForecast.drivers.length > 0
      ? liveForecast.drivers
      : forecastCell.drivers;
  const isLiveForecast = Boolean(liveForecast);

  return (
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1.05fr_1fr]">
      <section className="min-w-0">
        <div
          className="rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <div className="mb-4 flex items-baseline justify-between gap-4">
            <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
              {isLiveForecast ? "live forecast" : "current forecast"} · 80% CI
            </span>
            <span className="[font-family:var(--font-display)] text-[2rem] font-semibold leading-none text-[var(--color-accent)]">
              {formatValue(displayedForecast.pointEstimate, forecastCell.unit)}
            </span>
          </div>
          <ForecastViz
            point={displayedForecast.pointEstimate}
            ciLow={displayedForecast.ciLow}
            ciHigh={displayedForecast.ciHigh}
            unit={forecastCell.unit}
            history={forecastCell.historicalContext}
            size="full"
          />
          {forecastCell.historicalContext.length > 0 && (
            <div
              className="mt-6 border-t pt-5"
              style={{ borderColor: "var(--theme-border)" }}
            >
              <div className="mb-3 flex items-baseline justify-between gap-4">
                <h2 className="[font-family:var(--font-display)] text-[0.95rem] font-semibold tracking-[-0.01em]">
                  Trend
                </h2>
                <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  history + forecast
                </span>
              </div>
              <ForecastTrend
                point={displayedForecast.pointEstimate}
                ciLow={displayedForecast.ciLow}
                ciHigh={displayedForecast.ciHigh}
                unit={forecastCell.unit}
                history={forecastCell.historicalContext}
                targetLabel={formatShortDate(
                  forecastCell.resolvedOutcome?.resolvedAt ??
                    forecastCell.resolutionDate,
                )}
                actual={
                  forecastCell.resolvedOutcome
                    ? {
                        label: "actual",
                        value: forecastCell.resolvedOutcome.value,
                      }
                    : undefined
                }
              />
            </div>
          )}
          <p className="mt-4 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            {forecastSourceLabel(
              forecastCell,
              supportsLive,
              mode,
              statusLabel,
              liveForecast,
            )}
          </p>
          {forecastCell.resolvedOutcome && (
            <ResolvedOutcomePanel
              forecast={forecastCell}
              score={resolvedScore}
            />
          )}
          <ThesisLogRecordPanel forecast={forecastCell} />
        </div>

        <div
          className="mt-6 rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <h2 className="mb-3 [font-family:var(--font-display)] text-[0.95rem] font-semibold tracking-[-0.01em]">
            Key drivers
          </h2>
          <ul className="grid grid-cols-1 gap-2 [font-family:var(--font-body)] text-[0.88rem] text-[var(--theme-text)] sm:grid-cols-2">
            {drivers.map((driver) => (
              <li key={driver} className="flex items-start gap-2 leading-[1.5]">
                <span className="mt-[6px] inline-block h-1 w-2 shrink-0 bg-[var(--color-accent)]" />
                <span>{driver}</span>
              </li>
            ))}
          </ul>
        </div>

        <div
          className="mt-6 rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <h2 className="mb-4 [font-family:var(--font-display)] text-[0.95rem] font-semibold tracking-[-0.01em]">
            Resolution
          </h2>
          <dl className="grid grid-cols-1 gap-x-5 gap-y-3 [font-family:var(--font-body)] text-[0.86rem] sm:grid-cols-[120px_minmax(0,1fr)]">
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              source
            </dt>
            <dd className="min-w-0 break-words text-[var(--theme-text)]">
              {forecastCell.resolutionSourceUrl ? (
                <a
                  className="text-[var(--theme-text)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
                  href={forecastCell.resolutionSourceUrl}
                >
                  {forecastCell.resolutionSource}
                </a>
              ) : (
                forecastCell.resolutionSource
              )}
            </dd>
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              {forecastCell.resolvedOutcome ? "resolved" : "expected"}
            </dt>
            <dd className="min-w-0 break-words text-[var(--theme-text)]">
              {formatFullDate(
                forecastCell.resolvedOutcome?.resolvedAt ??
                  forecastCell.resolutionDate,
              )}
            </dd>
            {forecastCell.resolvedOutcome && (
              <>
                <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  actual
                </dt>
                <dd className="min-w-0 break-words text-[var(--theme-text)]">
                  {formatValue(
                    forecastCell.resolvedOutcome.value,
                    forecastCell.unit,
                  )}
                </dd>
              </>
            )}
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              rule
            </dt>
            <dd className="min-w-0 break-words leading-[1.55] text-[var(--theme-text)]">
              {forecastCell.resolutionRule}
            </dd>
            {forecastCell.dataPointId && (
              <>
                <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  Data point
                </dt>
                <dd className="min-w-0 break-all [font-family:var(--font-mono)] text-[0.78rem] leading-[1.55] text-[var(--color-horizon-700)]">
                  {forecastCell.dataPointId}
                </dd>
              </>
            )}
            {forecastCell.policyParameter && (
              <>
                <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  Policy parameter
                </dt>
                <dd className="min-w-0 break-all [font-family:var(--font-mono)] text-[0.78rem] leading-[1.55] text-[var(--color-rose-700)]">
                  {forecastCell.policyParameter}
                </dd>
              </>
            )}
          </dl>
        </div>
        {forecastCell.series && <SeriesMetadataPanel forecast={forecastCell} />}
      </section>

      <section className="min-w-0">
        <div className="mb-3 flex items-center justify-between gap-4">
          <h2 className="[font-family:var(--font-display)] text-[1rem] font-semibold tracking-[-0.01em]">
            Analyst agent · reasoning trace
          </h2>
          <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            {reasoningStatusLabel(supportsLive, mode, liveSteps, forecastCell)}
          </span>
        </div>
        <TraceStatusBanner
          forecast={forecastCell}
          liveForecast={liveForecast}
          mode={mode}
          supportsLive={supportsLive}
        />
        <ReasoningSurface
          activeTool={activeTool}
          error={error}
          forecast={forecastCell}
          mode={mode}
          statusLabel={statusLabel}
          steps={liveSteps}
          supportsLive={supportsLive}
        />
        <p className="mt-3 text-[0.76rem] leading-[1.55] text-[var(--theme-text-dim)]">
          {supportsLive
            ? liveModeDescription(forecastCell.slug)
            : forecastCell.predictionRun
              ? "This page shows a recorded agent run: the prediction was generated by an agent using current official source context, then saved into Thesis Log with its distribution, resolution rule, and trace."
              : "The route, resolution rule, and catalog entry are live. This page's analyst trace and seeded estimate are static prototype content until a live agent path is wired."}
        </p>
      </section>
    </div>
  );
}

function ResolvedOutcomePanel({
  forecast,
  score,
}: {
  forecast: ForecastCell;
  score?: ResolvedForecastScore;
}) {
  const outcome = forecast.resolvedOutcome;
  if (!outcome) return null;
  const result = getResolutionResult(forecast);
  const resultLabel =
    result === "inside" ? "inside 80% interval" : "outside 80% interval";

  return (
    <div
      className="mt-5 rounded-lg border bg-[var(--theme-bg-surface)] p-4"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
          resolved outcome
        </span>
        <span
          className={`rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] ${
            result === "inside"
              ? "border-[var(--color-horizon-300)] bg-[var(--color-horizon-50)] text-[var(--color-horizon-700)]"
              : "border-[#F2DCAF] bg-[#FFF4DD] text-[#7A5C20]"
          }`}
        >
          {resultLabel}
        </span>
      </div>
      <dl className="grid grid-cols-1 gap-x-5 gap-y-2 [font-family:var(--font-body)] text-[0.84rem] sm:grid-cols-[120px_minmax(0,1fr)]">
        <dt className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          actual
        </dt>
        <dd className="text-[var(--theme-text)]">
          {formatValue(outcome.value, forecast.unit)}
        </dd>
        <dt className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          forecast
        </dt>
        <dd className="text-[var(--theme-text)]">
          {formatValue(forecast.pointEstimate, forecast.unit)} with 80% CI [
          {formatValue(forecast.ciLow, forecast.unit)},{" "}
          {formatValue(forecast.ciHigh, forecast.unit)}]
        </dd>
        {score && (
          <>
            <dt className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              error
            </dt>
            <dd className="text-[var(--theme-text)]">
              {formatSignedValue(score.signedError, forecast.unit)} · absolute{" "}
              {formatValue(score.absoluteError, forecast.unit)}
            </dd>
            <dt className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              cdf score
            </dt>
            <dd className="text-[var(--theme-text)]">
              CRPS {formatCompactNumber(score.crps)} · PIT{" "}
              {formatCompactNumber(score.probabilityIntegralTransform)}
            </dd>
          </>
        )}
        <dt className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          source
        </dt>
        <dd className="min-w-0 break-words text-[var(--theme-text)]">
          {outcome.sourceUrl ? (
            <a
              className="text-[var(--color-horizon-700)] no-underline hover:underline"
              href={outcome.sourceUrl}
            >
              {outcome.source}
            </a>
          ) : (
            outcome.source
          )}
        </dd>
      </dl>
      {outcome.note && (
        <p className="mt-3 text-[0.78rem] leading-[1.55] text-[var(--theme-text-muted)]">
          {outcome.note}
        </p>
      )}
    </div>
  );
}

function ThesisLogRecordPanel({ forecast }: { forecast: ForecastCell }) {
  const distribution = forecast.predictionDistribution;
  const run = forecast.predictionRun;
  if (!distribution && !run && !forecast.dataPointId) return null;

  return (
    <div
      className="mt-5 rounded-lg border bg-[var(--theme-bg-surface)] p-4"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
          recorded in Thesis Log
        </span>
        <a
          className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--color-accent)] no-underline hover:no-underline"
          href="/log"
        >
          Open log →
        </a>
      </div>
      <dl className="grid grid-cols-1 gap-x-5 gap-y-2 [font-family:var(--font-body)] text-[0.82rem] sm:grid-cols-[120px_minmax(0,1fr)]">
        <dt className="[font-family:var(--font-mono)] text-[0.66rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          record
        </dt>
        <dd className="text-[var(--theme-text)]">
          {run?.runAt ? formatFullDate(run.runAt) : "prototype seed"}
        </dd>
        <dt className="[font-family:var(--font-mono)] text-[0.66rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          agent
        </dt>
        <dd className="text-[var(--theme-text)]">
          {run?.agent ?? "prototype seed"}
        </dd>
        <dt className="[font-family:var(--font-mono)] text-[0.66rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          distribution
        </dt>
        <dd className="text-[var(--theme-text)]">
          {distribution
            ? `${distribution.pointCount} CDF points`
            : "not recorded"}
        </dd>
        {run?.model && (
          <>
            <dt className="[font-family:var(--font-mono)] text-[0.66rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              model
            </dt>
            <dd className="text-[var(--theme-text)]">{run.model}</dd>
          </>
        )}
        {forecast.dataPointId && (
          <>
            <dt className="[font-family:var(--font-mono)] text-[0.66rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              ledger fact
            </dt>
            <dd className="min-w-0 break-all [font-family:var(--font-mono)] text-[0.76rem] text-[var(--color-horizon-700)]">
              <a
                className="text-[var(--color-horizon-700)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
                href="/ledger"
              >
                {forecast.dataPointId}
              </a>
            </dd>
          </>
        )}
      </dl>
    </div>
  );
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

function TraceStatusBanner({
  forecast,
  liveForecast,
  mode,
  supportsLive,
}: {
  forecast: ForecastCell;
  liveForecast: RuntimeForecast | null;
  mode: RuntimeMode;
  supportsLive: boolean;
}) {
  const status = traceStatus(mode, supportsLive, liveForecast, forecast);

  return (
    <div
      className="mb-3 rounded-md border bg-[var(--theme-bg-surface)] px-4 py-3 text-[0.78rem] leading-[1.5]"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <span
        className={`mr-2 inline-block rounded-full border px-2 py-[1px] [font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.1em] ${
          status.tone === "live"
            ? "border-[var(--color-horizon-300)] bg-[var(--color-horizon-50)] text-[var(--color-horizon-700)]"
            : status.tone === "fallback"
              ? "border-[#F2DCAF] bg-[#FFF4DD] text-[#7A5C20]"
              : "border-[var(--theme-border)] bg-[var(--theme-bg-elevated)] text-[var(--theme-text-dim)]"
        }`}
      >
        {status.label}
      </span>
      <span className="text-[var(--theme-text-muted)]">{status.body}</span>
    </div>
  );
}

function SeriesMetadataPanel({ forecast }: { forecast: ForecastCell }) {
  const series = forecast.series;
  if (!series) return null;

  return (
    <div
      className="mt-6 rounded-xl border bg-[var(--theme-bg-elevated)] p-6"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <h2 className="mb-4 [font-family:var(--font-display)] text-[0.95rem] font-semibold tracking-[-0.01em]">
        Series design
      </h2>
      <dl className="grid grid-cols-1 gap-x-5 gap-y-3 [font-family:var(--font-body)] text-[0.86rem] sm:grid-cols-[120px_minmax(0,1fr)]">
        <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          series
        </dt>
        <dd className="min-w-0 break-all [font-family:var(--font-mono)] text-[0.78rem] leading-[1.55] text-[var(--color-horizon-700)]">
          {series.seriesId}
        </dd>
        <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          cadence
        </dt>
        <dd className="min-w-0 break-words text-[var(--theme-text)]">
          {series.cadence} · {series.resolutionLatency}
        </dd>
        <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          horizon
        </dt>
        <dd className="min-w-0 break-words text-[var(--theme-text)]">
          {series.horizonLabel} · {series.resolutionPolicy.replace("_", " ")}
        </dd>
        <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          priority
        </dt>
        <dd className="min-w-0 break-words text-[var(--theme-text)]">
          {series.priority}
        </dd>
        {series.benchmark && (
          <>
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              benchmark
            </dt>
            <dd className="min-w-0 break-words text-[var(--theme-text)]">
              {series.benchmark}
            </dd>
          </>
        )}
        <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
          chainable
        </dt>
        <dd className="min-w-0 break-words text-[var(--theme-text)]">
          {series.chainableQuestions.join(" · ")}
        </dd>
        {forecast.predictionRun && (
          <>
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              run
            </dt>
            <dd className="min-w-0 break-words text-[var(--theme-text)]">
              {forecast.predictionRun.agent} · {forecast.predictionRun.model} ·{" "}
              {formatFullDate(forecast.predictionRun.runAt)}
            </dd>
          </>
        )}
      </dl>
    </div>
  );
}

function ReasoningSurface({
  activeTool,
  error,
  forecast,
  mode,
  statusLabel,
  steps,
  supportsLive,
}: {
  activeTool: ActiveTool | null;
  error: string | null;
  forecast: ForecastCell;
  mode: RuntimeMode;
  statusLabel: string;
  steps: ReasoningStep[];
  supportsLive: boolean;
}) {
  const shouldReplayMock =
    !supportsLive ||
    mode === "mock" ||
    (mode === "fallback" && steps.length === 0);

  if (shouldReplayMock) {
    return (
      <>
        {error && (
          <div
            className="mb-3 rounded-md border bg-[var(--theme-bg-elevated)] px-4 py-3 text-[0.78rem] leading-[1.5] text-[var(--theme-text-muted)]"
            style={{ borderColor: "var(--theme-border)" }}
          >
            {error} Replaying the static reasoning trace.
          </div>
        )}
        <AgentReasoning steps={forecast.reasoning} unit={forecast.unit} />
      </>
    );
  }

  return (
    <LiveReasoningTimeline
      activeTool={activeTool}
      complete={mode === "complete"}
      error={error}
      statusLabel={statusLabel}
      steps={steps}
      unit={forecast.unit}
    />
  );
}

function LiveReasoningTimeline({
  activeTool,
  complete,
  error,
  statusLabel,
  steps,
  unit,
}: {
  activeTool: ActiveTool | null;
  complete: boolean;
  error: string | null;
  statusLabel: string;
  steps: ReasoningStep[];
  unit: ForecastCell["unit"];
}) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    container.scrollTo({ top: container.scrollHeight, behavior: "smooth" });
  }, [steps.length, activeTool]);

  return (
    <div
      className="rounded-xl border bg-[var(--theme-bg-elevated)]"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <header
        className="flex items-center justify-between gap-3 border-b px-5 py-3"
        style={{ borderColor: "var(--theme-border)" }}
      >
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            {!complete && !error && (
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[var(--color-accent)] opacity-60" />
            )}
            <span
              className="relative inline-flex h-2 w-2 rounded-full"
              style={{
                backgroundColor: complete
                  ? "var(--color-horizon-500)"
                  : "var(--color-accent)",
              }}
            />
          </span>
          <span className="[font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.12em] text-[var(--theme-text-muted)]">
            {complete ? "analysis complete" : statusLabel}
          </span>
        </div>
      </header>
      <div
        ref={containerRef}
        className="max-h-[640px] overflow-y-auto px-5 py-5"
      >
        {steps.length === 0 && !activeTool && (
          <p className="my-3 text-[0.93rem] leading-[1.65] text-[var(--theme-text-muted)]">
            Opening live analyst stream…
          </p>
        )}
        {steps.map((step, index) => (
          <LiveStep key={index} step={step} unit={unit} />
        ))}
        {activeTool && (
          <ToolBlock call={activeTool.call} running tool={activeTool.tool} />
        )}
        {error && (
          <p className="mt-4 text-[0.78rem] leading-[1.5] text-[var(--theme-text-muted)]">
            {error}
          </p>
        )}
        {complete && (
          <div className="mt-6 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            — end of analyst stream —
          </div>
        )}
      </div>
    </div>
  );
}

function LiveStep({
  step,
  unit,
}: {
  step: ReasoningStep;
  unit: ForecastCell["unit"];
}) {
  switch (step.kind) {
    case "heading":
      return (
        <h4 className="mt-6 first:mt-0 mb-2 [font-family:var(--font-display)] text-[0.95rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
          <span className="mr-2 text-[var(--color-accent)]">§</span>
          {step.text}
        </h4>
      );
    case "text":
      return (
        <p className="my-3 text-[0.93rem] leading-[1.65] text-[var(--theme-text)]">
          {step.text}
        </p>
      );
    case "math":
      return (
        <p
          className="my-3 rounded-md border bg-[var(--theme-bg-surface)] px-4 py-2 [font-family:var(--font-mono)] text-[0.78rem] leading-[1.7] text-[var(--theme-text)]"
          style={{ borderColor: "var(--theme-border)" }}
        >
          {step.text}
        </p>
      );
    case "tool":
      return (
        <ToolBlock
          call={step.call}
          result={step.result}
          tool={step.tool ?? "policyengine.simulate"}
        />
      );
    case "forecast":
      return (
        <div className="mt-6 rounded-xl border border-[var(--color-accent)] bg-[var(--color-accent-subtle)] p-5">
          <div className="mb-2 [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--color-rose-700)]">
            calibrated forecast · 80% CI
          </div>
          <div className="flex flex-wrap items-baseline gap-4">
            <span className="[font-family:var(--font-display)] text-[2rem] font-semibold leading-none text-[var(--color-rose-700)]">
              {formatValue(step.point, unit)}
            </span>
            <span className="[font-family:var(--font-mono)] text-[0.85rem] text-[var(--color-rose-700)]">
              [{formatValue(step.ciLow, unit)} ·{" "}
              {formatValue(step.ciHigh, unit)}]
            </span>
          </div>
        </div>
      );
  }
}

function ToolBlock({
  call,
  result,
  running = false,
  tool,
}: {
  call: string;
  result?: string;
  running?: boolean;
  tool: string;
}) {
  return (
    <div className="my-3">
      <div
        className="flex items-center justify-between rounded-t-md border-x border-t bg-[#0F1A24] px-4 py-2 text-[#9FB6C6] [font-family:var(--font-mono)] text-[0.7rem]"
        style={{ borderColor: "var(--color-ink-border)" }}
      >
        <span className="text-[#5E97C8]">▸ {tool}</span>
        <span className="text-[#9DB1BF]">
          {running ? "running…" : "complete"}
        </span>
      </div>
      <pre
        className="overflow-x-auto border-x bg-[#0F1A24] px-4 py-3 text-[#E8F0F5] [font-family:var(--font-mono)] text-[0.78rem] leading-[1.55]"
        style={{ borderColor: "var(--color-ink-border)" }}
      >
        <code>{call}</code>
      </pre>
      {running ? (
        <div
          className="flex items-center gap-2 rounded-b-md border-x border-b bg-[#172633] px-4 py-3 [font-family:var(--font-mono)] text-[0.72rem] text-[#9DB1BF]"
          style={{ borderColor: "var(--color-ink-border)" }}
        >
          <Spinner />
          <span>running live data lookup…</span>
        </div>
      ) : (
        <pre
          className="overflow-x-auto rounded-b-md border-x border-b bg-[#172633] px-4 py-3 text-[#9FC4E6] [font-family:var(--font-mono)] text-[0.75rem] leading-[1.55]"
          style={{ borderColor: "var(--color-ink-border)" }}
        >
          <code>
            <span className="text-[#E7A6C8]">↳ </span>
            {result}
          </code>
        </pre>
      )}
    </div>
  );
}

function Spinner() {
  return (
    <svg
      className="animate-spin"
      width="12"
      height="12"
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeOpacity="0.25"
        strokeWidth="3"
      />
      <path
        d="M12 2a10 10 0 0 1 10 10"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="3"
      />
    </svg>
  );
}

function resolveApiBase() {
  const configured = (
    process.env.NEXT_PUBLIC_THESIS_API_BASE_URL ??
    process.env.NEXT_PUBLIC_BRIER_API_BASE_URL
  )?.replace(/\/$/, "");
  if (configured) return configured;
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
  ) {
    return "http://127.0.0.1:3002";
  }
  return "https://api.thesisinstitute.org";
}

function parseEventData<T>(event: Event) {
  try {
    return JSON.parse((event as MessageEvent<string>).data) as T;
  } catch {
    return null;
  }
}

function isReasoningStep(step: ReasoningStep): step is ReasoningStep {
  return (
    step.kind === "heading" ||
    step.kind === "text" ||
    step.kind === "math" ||
    step.kind === "tool" ||
    step.kind === "forecast"
  );
}

function forecastSourceLabel(
  forecastCell: ForecastCell,
  supportsLive: boolean,
  mode: RuntimeMode,
  statusLabel: string,
  forecast: RuntimeForecast | null,
) {
  if (!supportsLive && forecastCell.predictionRun) {
    return `${forecastCell.predictionRun.agent} · ${forecastCell.predictionRun.runAt}`;
  }
  if (!supportsLive) return "static prototype estimate · seeded forecast value";
  if (forecast?.source === "ai_gateway") {
    return `generated by ${forecast.model ?? "AI Gateway"}`;
  }
  if (forecast?.source === "deterministic_fallback") {
    return "live BLS data · deterministic fallback";
  }
  if (forecast?.source === "calibration_fallback") {
    return "live PolicyEngine data · calibration fallback";
  }
  if (forecast?.source === "census_calibration_fallback") {
    return "live Census + PolicyEngine inputs · calibration fallback";
  }
  if (mode === "fallback") return "static mock · live API unavailable";
  return statusLabel;
}

function reasoningStatusLabel(
  supportsLive: boolean,
  mode: RuntimeMode,
  steps: ReasoningStep[],
  forecast: ForecastCell,
) {
  if (!supportsLive && forecast.predictionRun) return "recorded agent run";
  if (!supportsLive || mode === "mock") return "static mock";
  if (mode === "complete") return `${steps.length} live steps`;
  if (mode === "fallback") return "static fallback";
  return "streaming";
}

function traceStatus(
  mode: RuntimeMode,
  supportsLive: boolean,
  forecast: RuntimeForecast | null,
  forecastCell: ForecastCell,
) {
  if (!supportsLive && forecastCell.predictionRun) {
    return {
      label: "Recorded agent run",
      tone: "live" as const,
      body: "The reasoning below was generated by an agent using current official source context and saved in Thesis Log as this prediction's trace.",
    };
  }
  if (!supportsLive) {
    return {
      label: "Static mock trace",
      tone: "mock" as const,
      body: "The reasoning below is prewritten prototype content; the page, catalog entry, and resolution rule are live.",
    };
  }
  if (mode === "fallback") {
    return {
      label: "Fallback static trace",
      tone: "fallback" as const,
      body: "This cell has live API wiring, but the stream is unavailable, so the prototype is replaying the static mock trace.",
    };
  }
  if (mode === "mock") {
    return {
      label: "Static mock trace",
      tone: "mock" as const,
      body: "This cell can use the live API path, but this view is replaying the prewritten trace.",
    };
  }
  if (forecast) {
    return {
      label: "Live run",
      tone: "live" as const,
      body: "This run streamed through the live API and updated the forecast value on the page.",
    };
  }
  return {
    label: "Live API path",
    tone: "live" as const,
    body: "This cell is opening a server-sent reasoning stream. If the API is unavailable, the page falls back to the static mock trace.",
  };
}

function liveModeDescription(slug: string) {
  if (slug === "spm-child-poverty-2025") {
    return "Live mode checks public Census release/SPM pages, verifies the PolicyEngine current-law policy, applies an explicit child-poverty calibration prior, and calls the forecast model when AI Gateway credentials are available. If the API fails, the page replays the static trace.";
  }
  if (slug === "ctc-expansion-cost-ty2026") {
    return "Live mode queries the PolicyEngine policy and economy APIs, applies an explicit calibration prior, and calls the forecast model when AI Gateway credentials are available. If the API fails, the page replays the static trace.";
  }
  if (slug === "ctc-current-law-outlays-ty2026") {
    return "Live mode queries the PolicyEngine current-law policy, applies an explicit CTC outlay calibration prior, and streams the adjustment path. If the API fails, the page replays the static trace.";
  }
  return "Live mode queries BLS CPI-U data, computes an audit-ready data summary, and calls the forecast model when AI Gateway credentials are available. If the API fails, the page replays the static trace.";
}

function formatFullDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

function formatShortDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", {
    month: "short",
    year: "numeric",
  });
}
