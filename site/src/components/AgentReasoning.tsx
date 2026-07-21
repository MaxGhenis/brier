"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { ReasoningStep, Unit } from "@/data/forecast-cells";
import { formatValue } from "@/data/forecast-cells";
import type { TraceProvenance } from "@/data/trace-provenance";

interface AgentReasoningProps {
  steps: ReasoningStep[];
  unit: Unit;
  speed?: number; // 1.0 = normal; higher is faster
  provenance?: TraceProvenance;
}

interface StepState {
  step: ReasoningStep;
  // For text/heading/math: how many chars are revealed.
  // For tool: 0 = hidden, 1 = recorded check shown, 2 = recorded result shown.
  // For forecast: 0 = hidden, 1 = shown.
  progress: number;
  total: number;
}

export function AgentReasoning({
  steps,
  unit,
  speed = 1,
  provenance = "activity_backed",
}: AgentReasoningProps) {
  const initial: StepState[] = useMemo(
    () =>
      steps.map((s) => ({
        step: s,
        progress: 0,
        total: getStepTotal(s),
      })),
    [steps],
  );

  const [state, setState] = useState<StepState[]>(initial);
  const [activeIndex, setActiveIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  const [complete, setComplete] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const lastActiveRef = useRef(-1);

  useEffect(() => {
    setState(initial);
    setActiveIndex(0);
    setComplete(false);
    lastActiveRef.current = -1;
  }, [initial]);

  // Advance the active step until done, then move to next.
  useEffect(() => {
    if (paused || complete) return;
    if (activeIndex >= state.length) {
      setComplete(true);
      return;
    }
    const current = state[activeIndex];
    if (!current) {
      setComplete(true);
      return;
    }
    if (current.progress >= current.total) {
      const t = window.setTimeout(() => {
        setActiveIndex((i) => i + 1);
      }, getStepGap(current.step) / speed);
      return () => window.clearTimeout(t);
    }
    const delay = getStepStepDelay(current.step, current.progress) / speed;
    const t = window.setTimeout(() => {
      setState((prev) =>
        prev.map((s, i) =>
          i === activeIndex
            ? { ...s, progress: Math.min(s.progress + getProgressIncrement(s.step, s.progress), s.total) }
            : s,
        ),
      );
    }, delay);
    return () => window.clearTimeout(t);
  }, [state, activeIndex, paused, complete, speed]);

  // Auto-scroll only the inner container, never the page.
  useEffect(() => {
    if (activeIndex === lastActiveRef.current) return;
    lastActiveRef.current = activeIndex;
    const container = containerRef.current;
    if (!container) return;
    const active = container.querySelector(
      `[data-step-index="${activeIndex}"]`,
    ) as HTMLElement | null;
    if (!active) return;
    const containerRect = container.getBoundingClientRect();
    const activeRect = active.getBoundingClientRect();
    const relativeTop = activeRect.top - containerRect.top + container.scrollTop;
    const target = relativeTop - container.clientHeight + activeRect.height + 24;
    if (target > container.scrollTop) {
      container.scrollTo({ top: target, behavior: "smooth" });
    }
  }, [activeIndex]);

  const handleSkip = () => {
    setState((prev) => prev.map((s) => ({ ...s, progress: s.total })));
    setActiveIndex(state.length);
    setComplete(true);
  };

  const handleRestart = () => {
    setState(initial);
    setActiveIndex(0);
    setComplete(false);
    setPaused(false);
  };

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
            {!complete && !paused && (
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
            {complete
              ? "recorded trace complete"
              : paused
                ? "paused"
                : "recorded trace replay"}
          </span>
        </div>
        <div className="flex items-center gap-3 [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em]">
          {!complete && (
            <button
              onClick={() => setPaused((p) => !p)}
              className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)]"
            >
              {paused ? "resume" : "pause"}
            </button>
          )}
          {!complete && (
            <button
              onClick={handleSkip}
              className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)]"
            >
              skip
            </button>
          )}
          {complete && (
            <button
              onClick={handleRestart}
              className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)]"
            >
              replay
            </button>
          )}
        </div>
      </header>
      <div
        ref={containerRef}
        className="max-h-[640px] overflow-y-auto px-5 py-5"
      >
        {provenance === "illustrative" && (
          <div
            className="mb-4 rounded-md border px-4 py-3 text-[0.78rem] leading-[1.55]"
            style={{
              borderColor: "var(--theme-border-strong)",
              color: "var(--theme-text-muted)",
              backgroundColor: "var(--theme-bg-surface)",
            }}
          >
            <span
              className="mr-2 rounded-full border px-2 py-[1px] [font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.1em]"
              style={{ borderColor: "var(--theme-border-strong)" }}
            >
              illustrative trace
            </span>
            This trace was authored from source context when the cell was
            created; the tool calls shown were not executed. Runs from June
            28, 2026 onward replay archived activity from the public
            records.
          </div>
        )}
        {provenance === "recorded_run" && (
          <div
            className="mb-4 text-[0.72rem] leading-[1.5]"
            style={{ color: "var(--theme-text-dim)" }}
          >
            Recorded research run from before on-repo activity archives
            (June 28, 2026); steps reflect real activity without archived
            receipts.
          </div>
        )}
        {state.map((s, i) => (
          <div
            key={i}
            data-step-index={i}
            className={
              i > activeIndex && s.progress === 0
                ? "opacity-0 pointer-events-none"
                : ""
            }
          >
            <RenderedStep
              state={s}
              unit={unit}
              active={i === activeIndex && !complete}
              provenance={provenance}
            />
          </div>
        ))}
        {complete && (
          <div className="mt-6 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            — end of recorded trace —
          </div>
        )}
      </div>
    </div>
  );
}

function RenderedStep({
  state,
  unit,
  active,
  provenance,
}: {
  state: StepState;
  unit: Unit;
  active: boolean;
  provenance: TraceProvenance;
}) {
  const { step, progress, total } = state;
  switch (step.kind) {
    case "heading": {
      const text = step.text.slice(0, progress);
      return (
        <h4 className="mt-6 first:mt-0 mb-2 [font-family:var(--font-display)] text-[0.95rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
          <span className="mr-2 text-[var(--color-accent)]">§</span>
          {text}
          {active && progress < total && <Caret />}
        </h4>
      );
    }
    case "text": {
      const text = step.text.slice(0, progress);
      return (
        <p className="my-3 text-[0.93rem] leading-[1.65] text-[var(--theme-text)]">
          {text}
          {active && progress < total && <Caret />}
        </p>
      );
    }
    case "math": {
      const text = step.text.slice(0, progress);
      return (
        <p className="my-3 rounded-md border bg-[var(--theme-bg-surface)] px-4 py-2 [font-family:var(--font-mono)] text-[0.78rem] leading-[1.7] text-[var(--theme-text)]"
          style={{ borderColor: "var(--theme-border)" }}
        >
          {text}
          {active && progress < total && <Caret />}
        </p>
      );
    }
    case "tool": {
      const tool = step.tool ?? "policyengine.simulate";
      const illustrative = provenance === "illustrative";
      const label = illustrative
        ? "illustrative step"
        : tool === "agent.run"
          ? "recorded agent run"
          : "recorded source check";
      return (
        <div className="my-3">
          <div
            className="flex items-center justify-between rounded-t-md border-x border-t bg-[#0F1A24] px-4 py-2 text-[#9FB6C6] [font-family:var(--font-mono)] text-[0.7rem]"
            style={{ borderColor: "var(--color-ink-border)" }}
          >
            <span className="text-[#5E97C8]">
              ▸ {label}: {tool}
            </span>
            <span className="text-[#9DB1BF]">
              {illustrative
                ? "authored, not executed"
                : progress === 0
                  ? "hidden"
                  : progress === 1
                    ? "replaying"
                    : "recorded"}
            </span>
          </div>
          <pre className="overflow-x-auto border-x bg-[#0F1A24] px-4 py-3 text-[#E8F0F5] [font-family:var(--font-mono)] text-[0.78rem] leading-[1.55]"
            style={{ borderColor: "var(--color-ink-border)" }}
          >
            <code>{progress >= 1 ? step.call : ""}</code>
          </pre>
          {progress >= 2 ? (
            <pre className="overflow-x-auto rounded-b-md border-x border-b bg-[#172633] px-4 py-3 text-[#9FC4E6] [font-family:var(--font-mono)] text-[0.75rem] leading-[1.55]"
              style={{ borderColor: "var(--color-ink-border)" }}
            >
              <code>
                <span className="text-[#E7A6C8]">↳ </span>
                {step.result}
              </code>
            </pre>
          ) : progress === 1 ? (
            <div className="flex items-center gap-2 rounded-b-md border-x border-b bg-[#172633] px-4 py-3 [font-family:var(--font-mono)] text-[0.72rem] text-[#9DB1BF]"
              style={{ borderColor: "var(--color-ink-border)" }}
            >
              <Spinner />
              <span>
                {illustrative
                  ? "replaying authored step…"
                  : "replaying recorded step…"}
              </span>
            </div>
          ) : null}
        </div>
      );
    }
    case "forecast": {
      if (progress === 0) {
        return <div className="h-0" />;
      }
      return (
        <div className="mt-6 rounded-xl border border-[var(--color-accent)] bg-[var(--color-accent-subtle)] p-5">
          <div className="mb-2 [font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--color-rose-700)]">
            calibrated forecast · 80% CI
          </div>
          <div className="flex items-baseline gap-4">
            <span className="[font-family:var(--font-display)] text-[2rem] font-semibold leading-none text-[var(--color-rose-700)]">
              {formatValue(step.point, unit)}
            </span>
            <span className="[font-family:var(--font-mono)] text-[0.85rem] text-[var(--color-rose-700)]">
              [{formatValue(step.ciLow, unit)} · {formatValue(step.ciHigh, unit)}]
            </span>
          </div>
        </div>
      );
    }
  }
}

function Caret() {
  return (
    <span
      className="inline-block w-[7px] h-[1em] translate-y-[2px] bg-[var(--color-accent)] ml-[1px] animate-pulse align-middle"
      aria-hidden
    />
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
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}

function getStepTotal(step: ReasoningStep): number {
  switch (step.kind) {
    case "heading":
    case "text":
    case "math":
      return step.text.length;
    case "tool":
      return 2;
    case "forecast":
      return 1;
  }
}

function getProgressIncrement(step: ReasoningStep, progress: number): number {
  if (step.kind === "heading") return 2;
  if (step.kind === "text") return 4;
  if (step.kind === "math") return 2;
  if (step.kind === "tool") return 1;
  if (step.kind === "forecast") return 1;
  return 1;
}

function getStepStepDelay(step: ReasoningStep, progress: number): number {
  if (step.kind === "heading") return 18;
  if (step.kind === "text") return 14;
  if (step.kind === "math") return 18;
  if (step.kind === "tool") {
    // call shown -> wait while "running" -> result
    return progress === 0 ? 220 : 900;
  }
  if (step.kind === "forecast") return 250;
  return 50;
}

function getStepGap(step: ReasoningStep): number {
  if (step.kind === "heading") return 200;
  if (step.kind === "tool") return 380;
  if (step.kind === "forecast") return 0;
  return 160;
}
