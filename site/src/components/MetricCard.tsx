"use client";

import { useState } from "react";
import { renderInline } from "@/lib/render-inline";

/**
 * Candidate-metric card with the long sourcing note clamped to a few
 * lines; the full text is a click away instead of a wall by default.
 */
export function MetricCard({
  kind,
  text,
  badgeLabel,
  badgeClass,
}: {
  kind: string;
  text: string;
  badgeLabel: string;
  badgeClass: string;
}) {
  const [expanded, setExpanded] = useState(false);
  const isLong = text.length > 220;

  return (
    <div className="rounded-lg border border-[var(--theme-border)] bg-[var(--theme-surface)] p-4">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <span
          className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] ${badgeClass}`}
        >
          {badgeLabel}
        </span>
        <span className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
          {kind}
        </span>
      </div>
      <p
        className={`m-0 text-[0.88rem] leading-[1.6] text-[var(--theme-text-muted)] ${
          isLong && !expanded ? "line-clamp-3" : ""
        }`}
      >
        {renderInline(text)}
      </p>
      {isLong && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mt-2 cursor-pointer border-0 bg-transparent p-0 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.1em] text-[var(--color-accent)] hover:underline"
        >
          {expanded ? "Less ↑" : "Full sourcing ↓"}
        </button>
      )}
    </div>
  );
}
