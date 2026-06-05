"use client";

import { Header } from "@/components/Header";
import { MarketsBrowser } from "@/components/MarketsBrowser";

/* ── Almanac hero + live forecast cells ── */

function ForecastPrototype() {
  return (
    <main className="mx-auto max-w-[1200px] px-8 pb-24 pt-12 max-md:px-5">
      <section className="mb-12 grid grid-cols-[minmax(0,760px)_minmax(240px,1fr)] gap-10 max-lg:grid-cols-1">
        <div>
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--color-accent)] mb-3">
            Thesis · policy futures
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(2rem,4.5vw,3.1rem)] font-light leading-[1.08] tracking-[-0.02em] text-[var(--theme-text)] mb-5">
            Forecasts on every consequential cell of government data
          </h1>
          <p className="text-[1.05rem] leading-[1.65] text-[var(--theme-text-muted)]">
            Brier analyst agents forecast published government statistics,
            law-encoded policy parameters, and outcomes conditional on policy
            states. Each cell carries a calibrated interval and an audit trail
            of the reasoning behind it.
          </p>
        </div>
        <div
          className="self-start rounded-xl border bg-[var(--theme-bg-surface)] p-5"
          style={{ borderColor: "var(--theme-border)" }}
        >
          <p className="[font-family:var(--font-mono)] text-[0.62rem] uppercase tracking-[0.15em] text-[var(--theme-text-dim)] mb-3">
            Prototype status
          </p>
          <dl className="space-y-3 text-[0.85rem] leading-[1.5]">
            <div>
              <dt className="[font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.12em] text-[var(--color-horizon-700)]">
                Live product
              </dt>
              <dd className="text-[var(--theme-text)]">
                Catalog, filters, routes, forecast pages, resolution rules.
              </dd>
            </div>
            <div>
              <dt className="[font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.12em] text-[var(--color-horizon-700)]">
                Live API paths
              </dt>
              <dd className="text-[var(--theme-text)]">
                CPI-U and two CTC cells stream through api.thesisinstitute.org.
              </dd>
            </div>
            <div>
              <dt className="[font-family:var(--font-mono)] text-[0.58rem] uppercase tracking-[0.12em] text-[var(--theme-text-dim)]">
                Static mock traces
              </dt>
              <dd className="text-[var(--theme-text)]">
                Most analyst reasoning and seeded estimates are prewritten
                prototype content.
              </dd>
            </div>
          </dl>
        </div>
      </section>
      <MarketsBrowser />
    </main>
  );
}

/* ── Horizon Divider ── */

function HorizonDivider() {
  return (
    <div className="relative h-px my-0">
      <div
        className="absolute inset-0"
        style={{
          background:
            "linear-gradient(90deg, rgba(217,228,236,0) 0%, rgba(190,208,219,0.4) 30%, rgba(159,196,230,0.5) 50%, rgba(190,208,219,0.4) 70%, rgba(217,228,236,0) 100%)",
        }}
      />
    </div>
  );
}

/* ── How the Almanac works — 3 steps ── */

function HowItWorks() {
  const stages = [
    {
      num: "01",
      title: "The catalog",
      description:
        "Every consequential cell of government data — published statistics, law-encoded policy parameters, and outcomes conditional on policy states — gets its own forecast cell, with an explicit resolution source and date.",
    },
    {
      num: "02",
      title: "The forecast",
      description:
        "Brier analyst agents predict each cell with a point estimate, a calibrated interval, and a full audit trail of the reasoning, sources, and key drivers behind it — open by construction.",
    },
    {
      num: "03",
      title: "The score",
      description:
        "When the official number publishes, every forecast is scored against the record. Calibration is public, per cell and per agent, so the track record is the product.",
    },
  ];

  return (
    <section className="py-[clamp(88px,12vw,140px)] px-8 max-md:px-4 bg-[#F7FAFC]">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-16">
          <span className="[font-family:var(--font-mono)] text-[0.68rem] tracking-[0.12em] uppercase text-[#A94E80] block mb-4 font-medium">
            How the Almanac works
          </span>
          <h2 className="[font-family:var(--font-display)] text-[clamp(1.8rem,3.5vw,2.6rem)] font-medium leading-[1.08] tracking-[-0.03em] text-[#14202B]">
            Open forecasts, scored against reality
          </h2>
        </div>

        <div className="grid grid-cols-3 gap-6 max-md:grid-cols-1">
          {stages.map((stage) => (
            <div
              key={stage.num}
              className="bg-white rounded-2xl p-8 border border-[#D9E4EC] transition-all duration-200 hover:translate-y-[-2px] hover:shadow-[0_8px_24px_rgba(20,32,43,0.06)]"
            >
              <div className="[font-family:var(--font-mono)] text-[0.72rem] font-medium text-[#A94E80] mb-3">
                {stage.num}
              </div>
              <h3 className="[font-family:var(--font-display)] text-[1.2rem] font-semibold mb-3 tracking-[-0.01em] text-[#14202B]">
                {stage.title}
              </h3>
              <p className="text-[0.9rem] text-[#415463] leading-[1.6] m-0">
                {stage.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Footer ── */

function Footer() {
  return (
    <footer className="py-16 px-8 text-center bg-[#F7FAFC] border-t border-[#D9E4EC]">
      <div className="flex gap-6 justify-center text-[0.78rem] [font-family:var(--font-mono)]">
        <a
          href="/forecasts"
          className="text-[#6B7C89] no-underline hover:text-[#14202B] transition-colors"
        >
          Forecasts
        </a>
        <a
          href="https://github.com/MaxGhenis/brier"
          className="text-[#6B7C89] no-underline hover:text-[#14202B] transition-colors"
        >
          GitHub
        </a>
        <a
          href="https://thesisinstitute.org"
          className="text-[#6B7C89] no-underline hover:text-[#14202B] transition-colors"
        >
          Thesis Institute
        </a>
      </div>
      <p className="mt-6 text-[0.75rem] text-[#94A3AF]">
        A program of{" "}
        <a
          href="https://thesisinstitute.org"
          className="text-[#6B7C89] no-underline hover:text-[#14202B] transition-colors"
        >
          Thesis Institute
        </a>
      </p>
    </footer>
  );
}

/* ── App ── */

export default function HomePage() {
  return (
    <div className="bg-[#F7FAFC] text-[#14202B] min-h-screen grain-overlay">
      <Header activePage="forecasts" />
      <ForecastPrototype />
      <HorizonDivider />
      <HowItWorks />
      <Footer />
    </div>
  );
}
