"use client";

import { useEffect, useRef, useState } from "react";
import { AgentReasoning } from "@/components/AgentReasoning";
import { ForecastViz } from "@/components/ForecastViz";
import {
  LIVE_FORECAST_SLUGS,
  formatValue,
  type Market,
  type ReasoningStep,
} from "@/data/markets";

type RuntimeMode = "mock" | "connecting" | "live" | "complete" | "fallback";

// How long the stream may stay completely silent before the page gives up on
// the live API and replays the static trace. A hung connection never fires
// onerror, so without this a stuck socket pins the UI on "connecting" forever.
export const STREAM_WATCHDOG_MS = 10_000;

interface RuntimeForecast {
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  confidence: 0.8;
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

interface MarketRuntimeProps {
  market: Market;
}

export function MarketRuntime({ market }: MarketRuntimeProps) {
  const supportsLive = LIVE_FORECAST_SLUGS.has(market.slug);
  const [mode, setMode] = useState<RuntimeMode>(
    supportsLive ? "connecting" : "mock",
  );
  const [statusLabel, setStatusLabel] = useState(
    supportsLive ? "opening live stream" : "mock replay",
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
    let sawStream = false;
    const source = new EventSource(
      `${resolveApiBase()}/forecasts/${market.slug}/stream`,
    );

    setMode("connecting");
    setStatusLabel("connecting to live API");
    setError(null);
    setLiveSteps([]);
    setActiveTool(null);

    const watchdog = window.setTimeout(() => {
      if (sawStream || completed) return;
      source.close();
      setError(
        "The live forecast API did not respond in time. Replaying the static reasoning trace.",
      );
      setStatusLabel("mock fallback");
      setMode("fallback");
    }, STREAM_WATCHDOG_MS);

    source.addEventListener("status", (event) => {
      sawStream = true;
      const data = parseEventData<{ label?: string; state?: string }>(event);
      if (!data) return;
      setStatusLabel(data.label ?? "live stream running");
      if (data.state !== "complete") setMode("live");
    });

    source.addEventListener("step", (event) => {
      sawStream = true;
      const step = parseEventData<ReasoningStep>(event);
      if (!step || !isReasoningStep(step)) return;
      setLiveSteps((prev) => [...prev, step]);
      setMode("live");
    });

    source.addEventListener("tool_start", (event) => {
      sawStream = true;
      const data = parseEventData<ActiveTool>(event);
      if (!data) return;
      setActiveTool(data);
      setStatusLabel(`${data.tool} running`);
      setMode("live");
    });

    source.addEventListener("tool_result", (event) => {
      sawStream = true;
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
      sawStream = true;
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
      sawStream = true;
      const data = parseEventData<{ message?: string }>(event);
      setError(data?.message ?? "Live forecast failed.");
      setStatusLabel("live API failed");
      setMode("fallback");
      source.close();
    });

    source.addEventListener("done", () => {
      sawStream = true;
      completed = true;
      setMode("complete");
      source.close();
    });

    source.onerror = () => {
      if (completed) return;
      window.clearTimeout(watchdog);
      setError("Could not connect to the live forecast API.");
      setStatusLabel("mock fallback");
      setMode("fallback");
      source.close();
    };

    return () => {
      completed = true;
      window.clearTimeout(watchdog);
      source.close();
    };
  }, [market.slug, supportsLive]);

  const forecast = liveForecast ?? {
    pointEstimate: market.pointEstimate,
    ciLow: market.ciLow,
    ciHigh: market.ciHigh,
    confidence: 0.8 as const,
  };
  const drivers =
    liveForecast?.drivers && liveForecast.drivers.length > 0
      ? liveForecast.drivers
      : market.drivers;
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
              {formatValue(forecast.pointEstimate, market.unit)}
            </span>
          </div>
          <ForecastViz
            point={forecast.pointEstimate}
            ciLow={forecast.ciLow}
            ciHigh={forecast.ciHigh}
            unit={market.unit}
            history={market.historicalContext}
            size="full"
          />
          <p className="mt-4 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            {forecastSourceLabel(supportsLive, mode, statusLabel, liveForecast)}
          </p>
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
          <dl className="grid grid-cols-[120px_1fr] gap-y-3 [font-family:var(--font-body)] text-[0.86rem]">
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              source
            </dt>
            <dd className="text-[var(--theme-text)]">
              {market.resolutionSource}
            </dd>
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              expected
            </dt>
            <dd className="text-[var(--theme-text)]">
              {formatFullDate(market.resolutionDate)}
            </dd>
            <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
              rule
            </dt>
            <dd className="leading-[1.55] text-[var(--theme-text)]">
              {market.resolutionRule}
            </dd>
            {market.dataPointId && (
              <>
                <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  Data point
                </dt>
                <dd className="[font-family:var(--font-mono)] text-[0.78rem] text-[var(--color-horizon-700)]">
                  {market.dataPointId}
                </dd>
              </>
            )}
            {market.policyParameter && (
              <>
                <dt className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  Policy parameter
                </dt>
                <dd className="[font-family:var(--font-mono)] text-[0.78rem] text-[var(--color-rose-700)]">
                  {market.policyParameter}
                </dd>
              </>
            )}
          </dl>
        </div>
      </section>

      <section className="min-w-0">
        <div className="mb-3 flex items-center justify-between gap-4">
          <h2 className="[font-family:var(--font-display)] text-[1rem] font-semibold tracking-[-0.01em]">
            Analyst agent · reasoning trace
          </h2>
          <span className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            {reasoningStatusLabel(supportsLive, mode, liveSteps, market)}
          </span>
        </div>
        <TraceStatusBanner
          liveForecast={liveForecast}
          mode={mode}
          supportsLive={supportsLive}
        />
        <ReasoningSurface
          activeTool={activeTool}
          error={error}
          market={market}
          mode={mode}
          statusLabel={statusLabel}
          steps={liveSteps}
          supportsLive={supportsLive}
        />
        <p className="mt-3 text-[0.76rem] leading-[1.55] text-[var(--theme-text-dim)]">
          {supportsLive
            ? liveModeDescription(market.slug)
            : "The route, resolution rule, and catalog entry are live. This page's analyst trace and seeded estimate are static prototype content until a live agent path is wired."}
        </p>
      </section>
    </div>
  );
}

function TraceStatusBanner({
  liveForecast,
  mode,
  supportsLive,
}: {
  liveForecast: RuntimeForecast | null;
  mode: RuntimeMode;
  supportsLive: boolean;
}) {
  const status = traceStatus(mode, supportsLive, liveForecast);

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

function ReasoningSurface({
  activeTool,
  error,
  market,
  mode,
  statusLabel,
  steps,
  supportsLive,
}: {
  activeTool: ActiveTool | null;
  error: string | null;
  market: Market;
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
        <AgentReasoning steps={market.reasoning} unit={market.unit} />
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
      unit={market.unit}
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
  unit: Market["unit"];
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
  unit: Market["unit"];
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
  const configured = process.env.NEXT_PUBLIC_BRIER_API_BASE_URL?.replace(
    /\/$/,
    "",
  );
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
  supportsLive: boolean,
  mode: RuntimeMode,
  statusLabel: string,
  forecast: RuntimeForecast | null,
) {
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
  market: Market,
) {
  if (!supportsLive || mode === "mock") return "static mock";
  if (mode === "complete") return `${steps.length} live steps`;
  if (mode === "fallback") return "static fallback";
  return "streaming";
}

function traceStatus(
  mode: RuntimeMode,
  supportsLive: boolean,
  forecast: RuntimeForecast | null,
) {
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
