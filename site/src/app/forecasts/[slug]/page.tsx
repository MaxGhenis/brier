import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import { MarketRuntime } from "@/components/MarketRuntime";
import {
  MARKETS,
  TYPE_LABEL,
  TYPE_DESCRIPTION,
  formatValue,
  getMarket,
  type Market,
} from "@/data/markets";

export function generateStaticParams() {
  return MARKETS.map((m) => ({ slug: m.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const m = getMarket(slug);
  if (!m) return { title: "Forecast not found — Thesis" };
  return {
    title: `${m.title} — Thesis forecasts`,
    description: m.question,
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

const typeBadgeClass: Record<Market["type"], string> = {
  data: "bg-[var(--color-mist-100)] text-[var(--color-horizon-700)] border-[var(--color-mist-200)]",
  policy:
    "bg-[var(--color-accent-subtle)] text-[var(--color-rose-700)] border-[var(--color-rose-100)]",
  conditional: "bg-[#FFF4DD] text-[#7A5C20] border-[#F2DCAF]",
};

export default async function MarketDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const market = getMarket(slug);
  if (!market) notFound();

  return (
    <div>
      <Header activePage="forecasts" />
      <main className="mx-auto max-w-[1100px] px-8 pb-32 pt-10 max-md:px-5">
        <nav className="mb-6 [font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.12em] text-[var(--theme-text-muted)]">
          <Link
            href="/forecasts"
            className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)] no-underline"
          >
            ← all forecasts
          </Link>
        </nav>

        {/* Hero */}
        <header className="mb-10">
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <span
              className={`inline-block rounded-full border px-2 py-[2px] [font-family:var(--font-mono)] text-[0.6rem] uppercase tracking-[0.1em] ${typeBadgeClass[market.type]}`}
            >
              {TYPE_LABEL[market.type]}
            </span>
            <span className="[font-family:var(--font-mono)] text-[0.65rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
              {TYPE_DESCRIPTION[market.type]}
            </span>
          </div>
          <h1 className="[font-family:var(--font-display)] text-[clamp(1.7rem,3.5vw,2.4rem)] font-light leading-[1.2] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            {market.title}
          </h1>
          <p className="max-w-[820px] text-[1rem] leading-[1.65] text-[var(--theme-text-muted)]">
            {market.question}
          </p>
          {market.conditionalOn && (
            <p className="mt-4 inline-block rounded-md border border-[#F2DCAF] bg-[#FFF4DD] px-3 py-2 [font-family:var(--font-mono)] text-[0.72rem] text-[#7A5C20]">
              conditional on:{" "}
              <span className="font-medium">{market.conditionalOn}</span>
            </p>
          )}
        </header>

        <MarketRuntime market={market} />

        {/* Related forecasts */}
        <RelatedMarkets currentSlug={market.slug} currentType={market.type} />
      </main>
    </div>
  );
}

function RelatedMarkets({
  currentSlug,
  currentType,
}: {
  currentSlug: string;
  currentType: Market["type"];
}) {
  const related = MARKETS.filter(
    (m) => m.slug !== currentSlug && m.type === currentType,
  ).slice(0, 3);
  if (related.length === 0) return null;
  return (
    <section
      className="mt-20 border-t pt-10"
      style={{ borderColor: "var(--theme-border)" }}
    >
      <h2 className="[font-family:var(--font-display)] text-[1.1rem] font-semibold tracking-[-0.01em] mb-5">
        More {TYPE_LABEL[currentType].toLowerCase()} forecasts
      </h2>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {related.map((m) => (
          <Link
            key={m.slug}
            href={`/forecasts/${m.slug}`}
            className="rounded-xl border bg-[var(--theme-bg-elevated)] p-5 no-underline transition-colors hover:no-underline"
            style={{ borderColor: "var(--theme-border)" }}
          >
            <div className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)] mb-2">
              resolves {formatShortDate(m.resolutionDate)}
            </div>
            <div className="[font-family:var(--font-display)] text-[0.95rem] font-semibold leading-[1.3] text-[var(--theme-text)] mb-3">
              {m.title}
            </div>
            <div className="[font-family:var(--font-display)] text-[1rem] font-semibold text-[var(--color-accent)]">
              {formatValue(m.pointEstimate, m.unit)}
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}

function formatShortDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", year: "numeric" });
}
