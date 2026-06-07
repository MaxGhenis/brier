import { Header } from "@/components/Header";

export const metadata = {
  title: "About — The Thesis Institute",
  description:
    "Thesis builds open, calibrated forecasts of public outcomes — every prediction scored against reality, grounded in encoded law, and open all the way down.",
};

export default function AboutPage() {
  return (
    <div>
      <Header activePage="about" />
      <article className="max-w-[680px] mx-auto px-8">
        <header className="text-center py-24 border-b border-[var(--theme-border)] mb-24 animate-[fade-up_0.6s_ease-out] max-[600px]:py-16">
          <p className="[font-family:var(--font-mono)] text-[0.65rem] tracking-[0.15em] uppercase text-accent mb-4">
            About The Thesis Institute
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(2rem,5vw,3rem)] font-light leading-[1.2] mb-8 tracking-[-0.02em]">
            Forecasts, scored against reality.
          </h1>
          <p className="text-[1.15rem] text-[var(--theme-text-muted)] max-w-[520px] mx-auto leading-[1.6]">
            An open, neutral forecaster of the outcomes that shape public
            life — calibrated, grounded in encoded law, and open all the way
            down.
          </p>
        </header>

        <div className="prose-content">
          <section>
            <h2>The thesis</h2>
            <p>
              A forecast you can score is worth more than an opinion you
              can&apos;t. Thesis publishes calibrated forecasts on the outcomes
              that shape public life — tax and benefit statistics, poverty,
              government data, and the consequences of policy — and grades every
              one against reality when the official number arrives. Each forecast
              carries its full chain of reasoning. <strong>The track record is
              the product.</strong>
            </p>
            <p>
              Prediction markets aggregate information but can&apos;t show their
              work; official scores are single estimates filtered through
              judgment that isn&apos;t fully documented. A forecast that is open
              <em> and</em> scored is a different kind of object — auditable
              before the fact, accountable after it.
            </p>
          </section>

          <section>
            <h2>Why now</h2>
            <p>
              AI forecasters now beat most humans. In 2025 an AI system placed
              4th of 539 entrants in the Metaculus Cup, and the trend line is
              steep. For the first time, calibrated forecasting can be produced
              at the scale, speed, and transparency of a public good — instead of
              locked inside a trading desk or a private intelligence shop.
            </p>
          </section>

          <section>
            <h2>Rules-as-code in the loop</h2>
            <p>
              Not everything that shapes an outcome is uncertain — some of it is
              fixed by statute. <strong>Axiom</strong>, a separate open project,
              encodes law as executable rules-as-code and computes those parts
              exactly. Brier agents draw on it as a tool: where a forecast turns
              on a rule rather than a judgment call, Axiom supplies the exact
              figure, and once a policy is enacted its computed result can settle
              the forecast in the ledger. <strong>PolicyEngine</strong>, the
              microsimulation instrument in the Thesis stack, runs on the same
              encoded rules — two distinct projects, deliberately connected.
            </p>
          </section>

          <section>
            <h2>The instruments</h2>
            <p>
              Forecasting public outcomes takes more than a language model. Thesis
              runs on <strong>PolicyEngine</strong> — open-source microsimulation
              of encoded tax and benefit law — and <strong>Microplex</strong> —
              calibrated synthetic populations. So a forecast isn&apos;t a guess
              about a headline; it&apos;s grounded in the mechanics of the statute
              and the shape of the population it lands on.
            </p>
          </section>

          <section>
            <h2>The model line</h2>
            <p>
              The forecasting agents are a model lineage —{" "}
              <strong>Brier&#8209;N</strong>, named for the calibration score
              they&apos;re judged by. The arc is deliberate: prompt today&apos;s
              models, then fine-tune on scored forecast traces, then
              reinforcement-learn against open-weights models, and ultimately
              train a from-scratch, open forecast-native model with calibration
              itself as the reward. It is how Thesis becomes an AI lab without
              becoming a <em>closed</em> one — the open-model path that produced
              OLMo, pointed squarely at forecasting.
            </p>
          </section>

          <section>
            <h2>Open all the way down</h2>
            <p>
              Open source opened the code. Open data opened the inputs. Open
              weights opened the models.{" "}
              <strong>Open predictions opens the reasoning itself</strong> —
              every prior, every tool call, every calibration result, on the
              consequential questions where forecasts drive decisions. You
              cannot inspect a human forecaster&apos;s reasoning the way you can
              inspect an agent&apos;s; that transparency compounds, because every
              improvement is shared the moment it&apos;s found.
            </p>
          </section>

          <section>
            <h2>Why a nonprofit</h2>
            <p>
              A forecaster&apos;s only durable asset is being unconflicted. A
              for-profit selling foresight to the highest bidder is the
              credit-rating-agency trap — the conflict that helped detonate 2008,
              applied to the one product whose entire value is having no angle.
              Thesis is a public-benefit institute: no owners, no trades, no
              angle — funded by philanthropy and sponsored compute, the way the
              open public goods before it were built. Nonprofit status is not a
              constraint here; it is the structural proof of neutrality.
            </p>
          </section>

          <section>
            <h2>The flywheel</h2>
            <p>
              Publish a thesis. Reality scores it. The scored record becomes the
              training data for the next model, which writes better theses, which
              are scored in turn. The public showcase and the training ground are
              the same surface — which is why the forecasts and the models can
              never really be separated, and why all of it stays open.
            </p>
          </section>

          <section>
            <h2>Where this goes</h2>
            <p>
              A continuously-updated, openly-scored map of the outcomes that
              decisions depend on — a public good that closed forecasting
              infrastructure cannot match, built in the open by the people it
              describes. If you want to fund it, build on it, or sponsor a set of
              questions you want better-calibrated, get in touch:{" "}
              <a href="mailto:max@policyengine.org?subject=Thesis%20Institute">
                max@policyengine.org
              </a>
              .
            </p>
          </section>
        </div>

        <div className="h-24" />
      </article>
    </div>
  );
}
