import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import { ForecastBrowser } from "@/components/ForecastBrowser";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import { buildForecastListing } from "@/data/forecast-listing";
import { cellsForTopic, getTopic, TOPICS } from "@/data/topics";
import {
  loadPolicyEngineLedger,
  withResolvedOutcomes,
} from "@/data/thesis-log";

export function generateStaticParams() {
  return TOPICS.map((topic) => ({ slug: topic.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const topic = getTopic(slug);
  if (!topic) return { title: "Topic not found — Thesis Institute" };
  return {
    title: `${topic.title} forecasts — Thesis Institute`,
    description: topic.description,
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

export default async function TopicPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const topic = getTopic(slug);
  if (!topic) notFound();

  const ledger = await loadPolicyEngineLedger();
  const forecasts = withResolvedOutcomes(FORECAST_CELLS, ledger);
  const topicForecasts = cellsForTopic(topic, forecasts);
  const resolvedCount = topicForecasts.filter(
    (forecast) => forecast.resolvedOutcome,
  ).length;

  return (
    <div>
      <Header activePage="forecasts" />
      <main className="mx-auto max-w-[1200px] px-8 pb-32 pt-12 max-md:px-5">
        <nav className="mb-6 [font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.12em] text-[var(--theme-text-muted)]">
          <Link
            href="/forecasts"
            className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)] no-underline"
          >
            ← all forecasts
          </Link>
          <span className="mx-2 text-[var(--theme-text-dim)]">/</span>
          <Link
            href="/topics"
            className="text-[var(--theme-text-muted)] hover:text-[var(--color-accent)] no-underline"
          >
            topics
          </Link>
        </nav>
        <section className="mb-12 max-w-[760px]">
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)] mb-3">
            Thesis Institute · topic view
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(1.9rem,4vw,2.6rem)] font-light leading-[1.15] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            {topic.title}
          </h1>
          <p className="text-[1.05rem] leading-[1.65] text-[var(--theme-text-muted)]">
            {topic.description}
          </p>
          <p className="mt-4 [font-family:var(--font-mono)] text-[0.72rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
            {topicForecasts.length} forecasts · {resolvedCount} resolved ·
            updates automatically as new cells land
          </p>
        </section>
        <ForecastBrowser forecasts={buildForecastListing(topicForecasts)} />
        <section
          className="mt-16 rounded-xl border bg-[var(--theme-bg-surface)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--theme-text-dim)] mb-2">
            How this page stays current
          </p>
          <p className="text-[0.92rem] leading-[1.65] text-[var(--theme-text)]">
            Topic membership is computed from each forecast&apos;s official
            data-point identifier, not from a hand-maintained list. When the
            analyst pipeline publishes new cells on these series — the next
            monthly print, a new conditional pair, a newly covered program —
            they appear here automatically, with the same public reasoning
            trace, resolution rule, and scoring as every other Thesis
            forecast.
          </p>
        </section>
      </main>
    </div>
  );
}
