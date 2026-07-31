import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { Header } from "@/components/Header";
import {
  BillForecasts,
  type BillForecastView,
} from "@/components/BillForecasts";
import { getBillForecastGroups } from "@/data/bill-forecasts";
import {
  REGISTRY_LABEL,
  getBill,
  loadBills,
  metricRegistryStatus,
  type RegistryStatus,
} from "@/data/bills";
import { formatValue } from "@/data/forecast-cells";

export function generateStaticParams() {
  return loadBills().map((entry) => ({ slug: entry.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const entry = getBill(slug);
  if (!entry) return { title: "Bill not found — Thesis Institute" };
  return {
    title: `${entry.bill.name} — Thesis Institute bill analyses`,
    description: `Provisions, countersignable goals, likely effects, and candidate outcome metrics for ${entry.bill.name}.`,
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
}

/** Render the light markdown the analysis text uses: **bold** and `code`. */
function renderInline(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={i}
          className="[font-family:var(--font-mono)] text-[0.82em] text-[var(--theme-text)]"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
}

/** Server-side view models for the client selector — cells stay out of the bundle. */
function buildForecastViews(billSlug: string): BillForecastView[] {
  return getBillForecastGroups(billSlug).map(({ metricLabel, resolved }) => {
    const { group, trueArm, falseArm, probability, unconditional } = resolved;
    const pct = probability?.pointEstimate;
    const gap = Math.abs(trueArm.pointEstimate - falseArm.pointEstimate);
    return {
      metricLabel,
      groupSlug: group.slug,
      question: group.question,
      eventLabel: group.eventLabel,
      gapLabel: `${formatValue(trueArm.pointEstimate, trueArm.unit)} − ${formatValue(
        falseArm.pointEstimate,
        falseArm.unit,
      )} = ${formatValue(gap, trueArm.unit)}`,
      gapNote: group.gapNote,
      probability:
        probability && pct !== undefined
          ? { pct, slug: probability.slug }
          : undefined,
      enacted: {
        point: trueArm.pointEstimate,
        ciLow: trueArm.ciLow,
        ciHigh: trueArm.ciHigh,
        pointLabel: formatValue(trueArm.pointEstimate, trueArm.unit),
        ciLabel: `${formatValue(trueArm.ciLow, trueArm.unit)} – ${formatValue(
          trueArm.ciHigh,
          trueArm.unit,
        )}`,
        slug: trueArm.slug,
      },
      baseline: {
        point: falseArm.pointEstimate,
        ciLow: falseArm.ciLow,
        ciHigh: falseArm.ciHigh,
        pointLabel: formatValue(falseArm.pointEstimate, falseArm.unit),
        ciLabel: `${formatValue(falseArm.ciLow, falseArm.unit)} – ${formatValue(
          falseArm.ciHigh,
          falseArm.unit,
        )}`,
        slug: falseArm.slug,
      },
      unconditional:
        unconditional && pct !== undefined
          ? {
              valueLabel: formatValue(
                unconditional.pointEstimate,
                unconditional.unit,
              ),
              formula: `${Math.round(pct)}% × ${formatValue(
                trueArm.pointEstimate,
                trueArm.unit,
              )} + ${Math.round(100 - pct)}% × ${formatValue(
                falseArm.pointEstimate,
                falseArm.unit,
              )} = ${formatValue(unconditional.pointEstimate, unconditional.unit)}`,
              slug: unconditional.slug,
            }
          : undefined,
    };
  });
}

const registryBadgeClass: Record<RegistryStatus, string> = {
  reachable: "bg-[#E8F4EA] text-[#1F6B33] border-[#BFDEC7]",
  "not-yet": "bg-[#FFF4DD] text-[#7A5C20] border-[#F2DCAF]",
  "no-series": "bg-[var(--color-mist-100)] text-[var(--theme-text-muted)] border-[var(--color-mist-200)]",
  unknown: "bg-transparent text-[var(--theme-text-dim)] border-[var(--theme-border)]",
};

export default async function BillDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const entry = getBill(slug);
  if (!entry) notFound();
  const forecastViews = buildForecastViews(slug);

  return (
    <div>
      <Header />
      <main className="mx-auto max-w-[1100px] px-8 pb-32 pt-10 max-md:px-5">
        <nav className="mb-6 [font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.12em]">
          <Link
            href="/bills"
            className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)] no-underline"
          >
            ← all bills
          </Link>
        </nav>

        <header className="mb-12">
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)] mb-3">
            {entry.bill.status}
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(1.7rem,3.5vw,2.4rem)] font-light leading-[1.2] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            {entry.bill.name}
          </h1>
          <p className="max-w-[820px] text-[0.95rem] leading-[1.65] text-[var(--theme-text-muted)]">
            {entry.bill.analyzed} · {entry.bill.pages.toLocaleString()} pages ·
            analyzed {entry.bill.analysisDate} ·{" "}
            <a
              href={entry.bill.sourceUrl}
              className="text-[var(--color-accent)]"
              target="_blank"
              rel="noopener noreferrer"
            >
              bill text
            </a>
          </p>
        </header>

        <section className="mb-14">
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <span className="inline-block rounded-full border border-[#D8C7EE] bg-[#F4EDFC] px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] text-[#5B3E86]">
              Conditional forecasts
            </span>
            <span className="[font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
              Outcomes forecast both ways · enacted vs baseline · exactly one
              arm resolves
            </span>
          </div>
          {forecastViews.length > 0 ? (
            <BillForecasts views={forecastViews} />
          ) : (
            <div className="rounded-xl border border-dashed border-[var(--theme-border)] px-6 py-5 text-[0.9rem] leading-[1.6] text-[var(--theme-text-muted)]">
              No registered forecast pairs for this bill yet. The candidate
              metrics below are the demand: when a pair is registered through
              the privileged path, both arms — the outcome with the bill
              enacted and the baseline without it — appear here and are scored
              publicly either way.
            </div>
          )}
        </section>

        <div className="grid gap-14">
          {entry.provisions.map((provision, index) => (
            <section
              key={index}
              className="border-t border-[var(--theme-border)] pt-8"
            >
              <p className="[font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-2">
                {provision.title}
              </p>
              <h2 className="[font-family:var(--font-display)] text-[1.35rem] font-normal leading-[1.3] text-[var(--theme-text)] mb-4">
                {provision.heading}
              </h2>

              {provision.quote && (
                <blockquote className="mb-5 border-l-2 border-[var(--color-accent)] pl-4 text-[0.9rem] italic leading-[1.6] text-[var(--theme-text-muted)]">
                  {renderInline(provision.quote)}
                </blockquote>
              )}

              {provision.context && (
                <p className="mb-6 max-w-[820px] text-[0.92rem] leading-[1.65] text-[var(--theme-text-muted)]">
                  {renderInline(provision.context)}
                </p>
              )}

              {provision.goals.length > 0 && (
                <div className="mb-6">
                  <h3 className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-3">
                    Countersignable goals
                  </h3>
                  <div className="grid gap-3">
                    {provision.goals.map((goal, i) => (
                      <div
                        key={i}
                        className="rounded-lg border border-[var(--theme-border)] bg-[var(--theme-surface)] p-4 text-[0.92rem] leading-[1.6] text-[var(--theme-text)]"
                      >
                        {renderInline(goal)}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {provision.effects.length > 0 && (
                <div className="mb-6">
                  <h3 className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-3">
                    Likely effects — shown regardless of the goals
                  </h3>
                  <ul className="grid gap-3 list-none p-0 m-0">
                    {provision.effects.map((effect, i) => (
                      <li
                        key={i}
                        className="text-[0.92rem] leading-[1.6] text-[var(--theme-text-muted)]"
                      >
                        <span className="mr-2 inline-block rounded-full border border-[var(--theme-border)] px-2 py-[1px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
                          {effect.mechanism}
                        </span>
                        {renderInline(effect.text)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {provision.barriers.length > 0 && (
                <div className="mb-6">
                  <h3 className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-3">
                    Implementation barriers
                  </h3>
                  <ul className="grid gap-3 list-none p-0 m-0">
                    {provision.barriers.map((barrier, i) => (
                      <li
                        key={i}
                        className="text-[0.92rem] leading-[1.6] text-[var(--theme-text-muted)]"
                      >
                        <span className="mr-2 inline-block rounded-full border border-[var(--theme-border)] px-2 py-[1px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
                          {barrier.actor}
                        </span>
                        {renderInline(barrier.text)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {provision.metrics.length > 0 && (
                <div className="mb-6">
                  <h3 className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-3">
                    Candidate outcome metrics
                  </h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    {provision.metrics.map((metric, i) => {
                      const { status } = metricRegistryStatus(metric);
                      return (
                        <div
                          key={i}
                          className="rounded-lg border border-[var(--theme-border)] bg-[var(--theme-surface)] p-4"
                        >
                          <div className="mb-2 flex flex-wrap items-center gap-2">
                            <span
                              className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] ${registryBadgeClass[status]}`}
                            >
                              {REGISTRY_LABEL[status]}
                            </span>
                            <span className="[font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.08em] text-[var(--theme-text-dim)]">
                              {metric.kind}
                            </span>
                          </div>
                          <p className="m-0 text-[0.88rem] leading-[1.6] text-[var(--theme-text-muted)]">
                            {renderInline(metric.text)}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {provision.conditionals.length > 0 && (
                <div>
                  <h3 className="[font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-3">
                    Conditional forecast sketches
                  </h3>
                  <div className="grid gap-2">
                    {provision.conditionals.map((conditional, i) => (
                      <pre
                        key={i}
                        className="m-0 overflow-x-auto rounded-lg border border-[var(--theme-border)] bg-[var(--theme-surface)] p-3 [font-family:var(--font-mono)] text-[0.78rem] leading-[1.5] text-[var(--theme-text)] whitespace-pre-wrap"
                      >
                        {conditional.replaceAll("`", "")}
                      </pre>
                    ))}
                  </div>
                </div>
              )}
            </section>
          ))}
        </div>
      </main>
    </div>
  );
}
