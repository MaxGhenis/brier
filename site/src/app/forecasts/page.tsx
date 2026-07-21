import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/Header";
import { ForecastBrowser } from "@/components/ForecastBrowser";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import { buildForecastListing } from "@/data/forecast-listing";
import {
  loadPolicyEngineLedger,
  withResolvedOutcomes,
} from "@/data/thesis-log";

export const metadata: Metadata = {
  title: "Policy forecasts — Thesis Institute",
  description:
    "Open forecasts on government statistics, policy settings, encoded parameters, and outcomes conditional on policy states. A public preview of Thesis Institute, where analyst agents call public data and the PolicyEngine microsim.",
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

export default async function ForecastsPage() {
  const ledger = await loadPolicyEngineLedger();
  const forecasts = withResolvedOutcomes(FORECAST_CELLS, ledger);

  return (
    <div>
      <Header activePage="forecasts" />
      <main className="mx-auto max-w-[1200px] px-8 pb-32 pt-12 max-md:px-5">
        <section className="mb-12 max-w-[760px]">
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)] mb-3">
            Thesis Institute · policy futures
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(1.9rem,4vw,2.6rem)] font-light leading-[1.15] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            Forecasts on every consequential cell of government data
          </h1>
          <p className="text-[1.05rem] leading-[1.65] text-[var(--theme-text-muted)]">
            Three coupled forecast types fall out of the integrated stack:{" "}
            <strong>government data points</strong> on published statistics,{" "}
            <strong>policy state forecasts</strong> on formal settings and
            encoded parameters, and <strong>conditional forecasts</strong> on
            outcomes given policy states. Thesis shows the target agent
            workflow: call public data and the PolicyEngine microsim, then
            publish calibrated uncertainty with an audit trail behind it.
          </p>
          <div className="mt-5 flex flex-wrap gap-4">
            <Link
              href="/log"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--color-accent)] no-underline hover:no-underline"
            >
              View Thesis Log →
            </Link>
            <Link
              href="/topics"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
            >
              Browse by topic →
            </Link>
            <Link
              href="/ledger"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
            >
              View facts ledger →
            </Link>
            <Link
              href="/forecasts/targets"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
            >
              View target architecture →
            </Link>
            <Link
              href="/packs"
              className="inline-block [font-family:var(--font-mono)] text-[0.68rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)] no-underline hover:text-[var(--color-accent)] hover:no-underline"
            >
              View prediction packs →
            </Link>
          </div>
        </section>
        <ForecastBrowser forecasts={buildForecastListing(forecasts)} />
        <section
          className="mt-16 rounded-xl border bg-[var(--theme-bg-surface)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--theme-text-dim)] mb-2">
            How forecasts are generated
          </p>
          <p className="text-[0.92rem] leading-[1.65] text-[var(--theme-text)]">
            Every forecast cell is opened by the Thesis Institute analyst agent,
            which decomposes the question, calls the PolicyEngine microsim
            against scenarios drawn from encoded statutes and MICROPLEX
            synthetic populations, checks official public data sources,
            integrates external baselines (CBO, FOMC SEP, JCT, BLS, Census, ONS,
            ABS, Statistics Canada), and produces a calibrated distribution.
            Open each forecast to read the full streaming reasoning.
          </p>
        </section>
      </main>
    </div>
  );
}
