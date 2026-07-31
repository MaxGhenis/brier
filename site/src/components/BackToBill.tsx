"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";

/**
 * Context-aware return link: rendered only when the visitor arrived
 * from a bill page (the bill links carry ?from=/bills/<slug>). The
 * param is validated against a strict internal-path shape, so pasted
 * or crafted URLs can't inject arbitrary destinations.
 */
export function BackToBill() {
  const params = useSearchParams();
  const from = params.get("from") ?? "";
  if (!/^\/bills\/[a-z0-9][a-z0-9-]*$/.test(from)) return null;
  return (
    <>
      <span className="text-[var(--theme-text-dim)]"> · </span>
      <Link
        href={from}
        className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)] no-underline"
      >
        ← back to bill
      </Link>
    </>
  );
}
