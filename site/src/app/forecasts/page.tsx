import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { MarketsBrowser } from "@/components/MarketsBrowser";

export const metadata: Metadata = {
  title: "Policy forecasts — Thesis",
  description:
    "Open forecasts on government statistics, law-encoded policy parameters, and outcomes conditional on policy states. A public preview of the Thesis, where analyst agents call public data and the PolicyEngine microsim.",
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

export default function MarketsPage() {
  return (
    <div>
      <Header activePage="forecasts" />
      <main className="mx-auto max-w-[1200px] px-8 pb-32 pt-12 max-md:px-5">
        <section className="mb-12 max-w-[760px]">
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)] mb-3">
            Thesis · policy futures
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(1.9rem,4vw,2.6rem)] font-light leading-[1.15] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            Forecasts on every consequential cell of government data
          </h1>
          <p className="text-[1.05rem] leading-[1.65] text-[var(--theme-text-muted)]">
            Three coupled forecast types fall out of the integrated stack:{" "}
            <strong>government data points</strong> on published statistics,{" "}
            <strong>policy state forecasts</strong> on law-encoded parameters,
            and <strong>conditional forecasts</strong> on outcomes given policy
            states. The Almanac shows the target agent workflow: call public
            data and the PolicyEngine microsim, then publish calibrated
            uncertainty with an audit trail behind it.
          </p>
        </section>
        <MarketsBrowser />
        <section
          className="mt-16 rounded-xl border bg-[var(--theme-bg-surface)] p-6"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--theme-text-dim)] mb-2">
            How forecasts are generated
          </p>
          <p className="text-[0.92rem] leading-[1.65] text-[var(--theme-text)]">
            Every forecast cell is opened by the Thesis analyst agent, which
            decomposes the question, calls the PolicyEngine microsim against
            scenarios drawn from law-encoded statutes and MICROPLEX synthetic
            populations, integrates external baselines (CBO, FOMC SEP, JCT, BLS,
            Census), and produces a calibrated distribution. Open each forecast
            to read the full streaming reasoning.
          </p>
        </section>
      </main>
    </div>
  );
}
