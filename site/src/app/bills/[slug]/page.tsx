import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import {
  BillForecasts,
  type BillForecastView,
} from "@/components/BillForecasts";
import { ProvisionAnalysis } from "@/components/ProvisionAnalysis";
import { getBillForecastGroups } from "@/data/bill-forecasts";
import {
  REGISTRY_LABEL,
  getBill,
  loadBillMeta,
  loadBills,
  metricRegistryStatus,
  type RegistryStatus,
} from "@/data/bills";
import { formatValue } from "@/data/forecast-cells";
import { fullSectionText } from "@/lib/bill-text";
import { renderInline, stripRegistryNote } from "@/lib/render-inline";

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

/** Server-side view models for the client selector — cells stay out of the bundle. */
function buildForecastViews(billSlug: string): BillForecastView[] {
  return getBillForecastGroups(billSlug).map(
    ({ metricLabel, resolved, example }) => {
    const { group, trueArm, falseArm, probability, unconditional } = resolved;
    const pct = probability?.pointEstimate;
    const gap = Math.abs(trueArm.pointEstimate - falseArm.pointEstimate);
    return {
      metricLabel,
      example,
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
  const rawMeta = loadBillMeta(slug);

  return (
    <div>
      <Header activePage="bills" />
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
          <div className="flex flex-wrap items-center gap-2">
            <a
              href={entry.bill.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 rounded-full border border-[var(--theme-border)] bg-[var(--theme-surface)] px-3 py-[5px] [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.08em] text-[var(--theme-text-muted)] no-underline transition-colors hover:border-[var(--color-accent)] hover:text-[var(--color-accent)] hover:no-underline"
            >
              Bill text ↗
            </a>
            {rawMeta?.axiomDashboardUrl && (
              <a
                href={rawMeta.axiomDashboardUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 rounded-full border border-[var(--theme-border)] bg-[var(--theme-surface)] px-3 py-[5px] [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.08em] text-[var(--theme-text-muted)] no-underline transition-colors hover:border-[var(--color-accent)] hover:text-[var(--color-accent)] hover:no-underline"
              >
                Axiom bills ↗
              </a>
            )}
            <span className="ml-1 [font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
              analyzed {entry.bill.analysisDate}
            </span>
          </div>
        </header>

        <section className="mb-14">
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <span className="inline-block rounded-full border border-[#D8C7EE] bg-[#F4EDFC] px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] text-[#5B3E86]">
              Conditional forecasts
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

        <section>
          <h2 className="mb-5 [font-family:var(--font-mono)] text-[0.75rem] uppercase tracking-[0.14em] text-[var(--theme-text)]">
            Provisions
          </h2>

          <div className="grid gap-3">
            {entry.provisions.map((provision, index) => {
              const sectionText = fullSectionText(
                entry.slug,
                provision.heading,
                provision.title,
              );
              return (
              <details
                key={index}
                className="group rounded-xl border border-[var(--theme-border)] bg-[var(--theme-surface)]"
              >
                <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-5 py-4 [&::-webkit-details-marker]:hidden">
                  <div className="min-w-0">
                    <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] mb-1">
                      {provision.title}
                    </p>
                    <h3 className="[font-family:var(--font-display)] text-[1.05rem] font-normal leading-[1.35] text-[var(--theme-text)]">
                      {provision.heading}
                    </h3>
                  </div>
                  <span
                    aria-hidden
                    className="shrink-0 text-[var(--theme-text-dim)] transition-transform group-open:rotate-90"
                  >
                    ›
                  </span>
                </summary>

                <div className="border-t border-[var(--theme-border)] px-5 py-6">
                  {provision.context && (
                    <p className="mb-5 max-w-[820px] text-[0.92rem] leading-[1.65] text-[var(--theme-text-muted)]">
                      {renderInline(provision.context)}
                    </p>
                  )}

                  {provision.quote && (
                    <details className="mb-6">
                      <summary className="cursor-pointer list-none [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--color-accent)] [&::-webkit-details-marker]:hidden">
                        Quoted from the bill ▸
                      </summary>
                      <blockquote className="mt-3 border-l-2 border-[var(--color-accent)] pl-4 text-[0.9rem] italic leading-[1.6] text-[var(--theme-text-muted)]">
                        {renderInline(provision.quote)}
                      </blockquote>
                    </details>
                  )}

                  {sectionText && (
                    <details className="mb-6">
                      <summary className="cursor-pointer list-none [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.1em] text-[var(--color-accent)] [&::-webkit-details-marker]:hidden">
                        Full section text ▸
                      </summary>
                      <pre className="mt-3 max-h-[420px] overflow-auto whitespace-pre-wrap rounded-lg border border-[var(--theme-border)] bg-[var(--theme-bg)] p-4 [font-family:var(--font-mono)] text-[0.75rem] leading-[1.55] text-[var(--theme-text-muted)]">
                        {sectionText}
                      </pre>
                    </details>
                  )}

                  <ProvisionAnalysis
                    billSlug={slug}
                    provisionIndex={index}
                    goals={provision.goals}
                    effects={provision.effects}
                    barriers={provision.barriers}
                    metrics={provision.metrics.map((metric) => {
                      const { status } = metricRegistryStatus(metric);
                      return {
                        kind: metric.kind,
                        text: stripRegistryNote(metric.text),
                        badgeLabel: REGISTRY_LABEL[status],
                        badgeClass: registryBadgeClass[status],
                        rationale: metric.rationale,
                        stances: metric.stances,
                      };
                    })}
                    conditionals={provision.conditionals}
                  />
                </div>
              </details>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}
