import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/Header";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import { cellsForTopic, TOPICS } from "@/data/topics";

export const metadata: Metadata = {
  title: "Forecast topics — Thesis Institute",
  description:
    "Standing topic views over the Thesis forecast catalog. Each topic collects every live forecast on its official data series and updates automatically as new cells are published.",
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

export default function TopicsIndexPage() {
  return (
    <div>
      <Header activePage="forecasts" />
      <main className="mx-auto max-w-[1200px] px-8 pb-32 pt-12 max-md:px-5">
        <section className="mb-12 max-w-[760px]">
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)] mb-3">
            Thesis Institute · topics
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(1.9rem,4vw,2.6rem)] font-light leading-[1.15] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            Topic views over the forecast catalog
          </h1>
          <p className="text-[1.05rem] leading-[1.65] text-[var(--theme-text-muted)]">
            A topic is a standing, rule-based view: it collects every forecast
            whose official data series belongs to the topic, and it updates
            automatically as the analyst pipeline publishes new cells. Nothing
            on these pages is curated by hand.
          </p>
        </section>
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
          {TOPICS.map((topic) => {
            const topicForecasts = cellsForTopic(topic, FORECAST_CELLS);
            return (
              <Link
                key={topic.slug}
                href={`/topics/${topic.slug}`}
                className="block rounded-xl border bg-[var(--theme-bg-surface)] p-6 no-underline transition-colors hover:border-[var(--color-accent)] hover:no-underline"
                style={{ borderColor: "var(--theme-border)" }}
              >
                <h2 className="mb-2 [font-family:var(--font-display)] text-[1.25rem] font-semibold tracking-[-0.01em] text-[var(--theme-text)]">
                  {topic.title}
                </h2>
                <p className="mb-4 text-[0.9rem] leading-[1.6] text-[var(--theme-text-muted)]">
                  {topic.description}
                </p>
                <p className="[font-family:var(--font-mono)] text-[0.7rem] uppercase tracking-[0.1em] text-[var(--theme-text-dim)]">
                  {topicForecasts.length} forecasts →
                </p>
              </Link>
            );
          })}
        </div>
      </main>
    </div>
  );
}
