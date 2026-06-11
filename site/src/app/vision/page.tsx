import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/Header";

export const metadata: Metadata = {
  title: "Thesis Institute vision — working document",
  description:
    "Working synthesis of the Thesis Institute vision: we build open AI forecasters that publish, explain, and score predictions on consequential outcomes.",
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

export default function VisionPage() {
  return (
    <div>
      <Header />
      <article className="max-w-[680px] mx-auto px-8">
        <header className="text-center py-24 border-b border-[var(--theme-border)] mb-24 animate-[fade-up_0.6s_ease-out] max-[600px]:py-16">
          <p className="[font-family:var(--font-mono)] text-[0.65rem] tracking-[0.15em] uppercase text-accent mb-4">
            Working document · not for distribution
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(2rem,5vw,3rem)] font-light leading-[1.2] mb-8 tracking-[-0.02em]">
            Open predictions
          </h1>
          <p className="text-[1.15rem] text-[var(--theme-text-muted)] max-w-[520px] mx-auto leading-[1.6]">
            <span className="[font-family:var(--font-editorial)] italic">
              Thesis Institute
            </span>{" "}
            builds open AI forecasters. We make them predict consequential
            outcomes, show their work, call public tools, publish calibrated
            uncertainty, and score every forecast against reality.
          </p>
        </header>

        <div className="prose-content">
          <section>
            <h2>The bet</h2>
            <p>
              Open source software opened code. Open data opened the inputs.
              Open weights opened the reasoning machinery. We open the
              predictions: continuously-updated forecasts from AI systems whose
              tool calls, assumptions, uncertainty, calibration, and later
              outcomes are public.
            </p>
            <p>
              We use forecasting as an alignment pressure. A system that must
              predict public facts before they happen has to track reality,
              expose uncertainty, use evidence, and learn from misses. When the
              trace is open, the public can inspect the model's evidence and the
              model can learn from the public record of its own errors.
            </p>
            <p>
              The traces create a compounding loop. Aggregate them and
              systematic biases become visible. Score the forecasts and weak
              methods lose credibility. Publish the fixes and the next
              generation of forecasters starts from a better baseline. Applied
              to prediction, the open-source dynamic becomes epistemic
              infrastructure.
            </p>
          </section>

          <section>
            <h2>What we build</h2>
            <p>
              Thesis Institute builds four connected pieces of public-good
              forecasting infrastructure:
            </p>
            <h3>We run open forecasters on consequential questions</h3>
            <p>
              We run AI-agent ensembles across the structured grid of
              consequential questions: government statistics from BEA, BLS,
              Census, and IRS; law-encoded policy parameters; and counterfactual
              questions that drive policy and economic decisions. We publish the
              forecasts, the traces, the calibration history, and the running
              methodology notes openly. Funded compute scales the depth of the
              ensemble; the substrate stays free at the point of use.
            </p>
            <h3>We simulate policy with inspectable models</h3>
            <p>
              We maintain PolicyEngine as open-source microsimulation for US,
              UK, and Canadian tax-benefit systems. Governments, think tanks,
              advocacy organizations, and researchers use it for custom policy
              analysis. Thesis Institute forecasters call PolicyEngine when
              they need policy-conditional distributions, and PolicyEngine
              keeps serving the policy community through the brand and
              workflows people already know.
            </p>
            <h3>We build calibrated synthetic populations</h3>
            <p>
              We build Microplex as the synthetic micro-data substrate for
              PolicyEngine simulations and calibration-native AI research. We
              publish the population data, methodology, and synthesizer code
              openly. Microplex replaces PolicyEngine's Enhanced CPS substrate
              with data calibrated more tightly to administrative benchmarks and
              useful beyond tax-benefit microsimulation.
            </p>
            <h3>We make everyday agent advice forecastable</h3>
            <p>
              We maintain the open-source Brier Decisions package, CLI, MCP
              server, and agent skills. They turn advice-seeking into explicit
              forecasts with KPIs, options, confidence intervals, resolution
              rules, and calibration tracking. This keeps the same discipline
              available for individual decisions, team decisions, and public
              policy forecasts.
            </p>
          </section>

          <section>
            <h2>The transparency advantage is the durable moat</h2>
            <p>
              We make transparency the core mechanism. Every methodology
              improvement, newly-discovered bias, and successful tool
              integration becomes shared infrastructure. Researchers can inspect
              the trace, reproduce the forecast, challenge the assumptions, and
              contribute a better method. Each improvement raises the baseline
              for everyone who builds on the substrate.
            </p>
            <p>
              The same dynamic that made Linux durable protects Thesis
              Institute's position. The compounding work happens across the
              whole community of users and contributors. The foundation
              maintains the core infrastructure, integrates the best
              contributions, sets direction, and protects the public-good
              character. The community expands the surface area faster than any
              single organization could.
            </p>
          </section>

          <section>
            <h2>Built for the agents of tomorrow</h2>
            <p>
              The infrastructure that matters most gets built ahead of the
              capability that needs it. TCP/IP was designed for a few hundred
              nodes and scaled to billions because the design anticipated future
              use. Kubernetes solved orchestration problems most organizations
              had not yet reached when it shipped. Linux was built when
              computing was tiny and scaled with hardware nobody had imagined.
              Substrate-builders capture disproportionate value because they are
              already there when the demand shows up.
            </p>
            <p>
              Thesis Institute is built with this in mind. Every capability is
              reachable through a clean machine-callable API; future agents will
              call tools directly. Every agent trace is structured for
              downstream consumption by other agents and human readers. Every
              tool in the simulation engine is self-describing so that agents
              that have not been invented yet can discover what is available.
              Permissioning anticipates millions of automated participants
              through scoped automated access. Calibration scoring is queryable,
              so current agents can learn from history and future agents can
              preferentially route to tool configurations with proven track
              records.
            </p>
            <p>
              This costs a little more today and pays disproportionately when
              capability arrives. By the time agents are reliably orchestrating
              tools, composing pipelines, and proposing methodology
              improvements, the substrate they need will already be open,
              public, free, and continuously calibrated. Open substrate gives
              tomorrow's agents permission-less infrastructure the next decade
              of AI development can build on.
            </p>
          </section>

          <section>
            <h2>The stack</h2>
            <p>
              Two independent 501(c)(3) foundations, technically integrated as
              one open stack:
            </p>
            <blockquote>
              <p>
                <strong>Encoded-law substrate</strong> — computable statutes,
                regulations, holdings, and metadata linking published government
                statistics to the laws that mandate them. Separate organization,
                shared substrate.
              </p>
              <p>
                <strong>Thesis Institute</strong> — open-predictions platform,
                microsimulation engine and custom policy analysis
                (PolicyEngine), synthetic-population substrate (Microplex),
                personal decision tool (Brier Decisions), and the research
                program on calibration-native foundation models and value
                forecasting.
              </p>
            </blockquote>
            <p>
              The Thesis Institute platform consumes encoded law, government
              data architecture, and Microplex population substrate as inputs,
              runs ensembles through PolicyEngine and other computational
              engines, and publishes calibrated forecasts. Policy partners
              interact with PolicyEngine directly through its own brand and
              channels. New audiences — AI safety, agencies funding their own
              forecasts, prediction-market researchers, broader policy analysts
              — interact with Thesis Institute as the umbrella platform.
            </p>
          </section>

          <section>
            <h2>Open predictions as a movement</h2>
            <p>
              The category needs a name to anchor its identity. The lineage:
            </p>
            <ul>
              <li>
                <strong>Open source software</strong> opened the code. Linux,
                Apache, Mozilla. The free software movement and its successors
                made source available and rewrote the economics of software
                distribution.
              </li>
              <li>
                <strong>Open data</strong> opened the inputs. Wikipedia, Common
                Crawl, OpenStreetMap, government open-data portals. The raw
                material of analysis became public and citable.
              </li>
              <li>
                <strong>Open weights</strong> opened the reasoning machinery.
                Allen Institute's Olmo, Llama, Mistral, DeepSeek. The trained
                models themselves became available for inspection and reuse.
              </li>
              <li>
                <strong>Open predictions</strong> opens the reasoning
                <em>itself</em>, on consequential questions. Every prior, every
                tool call, every update is auditable. The output includes the
                forecast and the full chain of reasoning that produced it.
              </li>
            </ul>
            <p>
              Each step opens more of the epistemic process. Each step produces
              durable public goods and gives the next generation of builders
              more to start from. Open predictions is the natural next layer,
              and Thesis Institute is the foundation building it.
            </p>
          </section>

          <section>
            <h2>We align AI by making it predict</h2>
            <p>
              We give AI systems a narrow job with a hard feedback loop: predict
              consequential outcomes before they happen, explain the evidence
              behind the prediction, quantify uncertainty, and accept a public
              score when reality arrives. That objective pushes models toward
              truth-tracking behavior because calibration, evidence use, and
              humility become measurable product requirements.
            </p>
            <p>
              We use the strongest available models as forecasters today. We
              connect them to public data, encoded law, PolicyEngine
              simulations, Microplex populations, and explicit calibration
              records. We evaluate which model-tool-method combinations predict
              best. We publish the traces so other researchers can reproduce,
              criticize, and improve the methods.
            </p>
            <p>
              As the corpus grows, we train and evaluate prediction-native
              systems: agents that select tools, decompose questions, maintain
              uncertainty, update on evidence, and learn from scored outcomes.
              The lab advances by making forecasts useful in the world and by
              making the full learning loop open.
            </p>
          </section>

          <section>
            <h2>We train prediction-native agents</h2>
            <p>
              The long-run research program is not just prompting other
              companies' models. We build the data, tools, and evaluation loop
              needed to train our own forecasters. The training corpus is
              time-versioned so every backtest can ask what the agent could have
              known on a specific date, which tool versions were available, and
              which outcomes had not yet resolved. That leakage control turns
              forecasting into a real scientific benchmark instead of a vibes
              demo.
            </p>
            <p>
              We make tool use native. The agent learns that forecasting often
              means calling BLS, Census, IRS, CMS, CBO, BEA, PolicyEngine,
              Microplex, and other public or inspectable systems. Tool outputs
              carry provenance, vintage, and uncertainty. Forecast artifacts
              store the question, evidence, tool calls, assumptions, uncertainty
              decomposition, final distribution, resolution rule, and eventual
              score as first-class data.
            </p>
            <p>
              We train on scored predictions. Supervised learning starts from
              strong public forecast traces. Reinforcement learning and reward
              modeling optimize proper scoring rules, calibration, interval
              sharpness, and decision usefulness once enough forecasts resolve.
              The objective is not eloquence; it is measured accuracy under
              uncertainty with a visible audit trail.
            </p>
            <p>
              We let agents learn from other agents' public traces. Not private
              chain-of-thought, but durable artifacts: which evidence was used,
              which tools were called, which assumptions mattered, which
              forecaster configurations were overconfident, and which methods
              improved after resolution. Future agents can route to the tools,
              methods, and peer traces with the best calibration record.
            </p>
            <p>
              This is how Thesis Institute can become an AI lab without
              becoming a closed frontier company. Whether we train foundation
              models directly or specialize open models into forecasters, the
              purpose stays narrow and public: build systems whose job is to
              predict, explain, resolve, and improve against reality.
            </p>
          </section>

          <section>
            <h2>Funder fit</h2>
            <p>
              The funder base that matches the thesis is broader and more
              accessible than the funder base for any of the predecessor
              framings:
            </p>
            <ul>
              <li>
                <strong>Coefficient Giving</strong> (Open Philanthropy rebrand)
                — AI safety, forecasting infrastructure, consequence-visibility
                framing fits directly in their existing grant portfolios.
              </li>
              <li>
                <strong>Survival and Flourishing Fund</strong> — long-horizon AI
                safety and alignment-adjacent infrastructure.
              </li>
              <li>
                <strong>Astera Institute</strong>,{" "}
                <strong>Schmidt Sciences / Schmidt Futures</strong>,{" "}
                <strong>Mozilla Foundation</strong> — novel public-good
                scientific infrastructure and open-source AI ethos.
              </li>
              <li>
                <strong>
                  Anthropic alumni and AI-safety-aligned liquidity
                </strong>{" "}
                — tender-offer and IPO-event capital from Anthropic and similar
                frontier labs. Open-source-by-construction means current
                frontier-lab employees can publicly back the work without
                conflict of interest. The complement-not-compete frame is unique
                to this category.
              </li>
              <li>
                <strong>Arnold Ventures Mission Aligned Investments</strong> —
                fits the structure Andrew Moylan and team have already signaled
                interest in, particularly for the open policy-forecasting
                infrastructure angle.
              </li>
              <li>
                <strong>
                  Government agencies and international equivalents
                </strong>{" "}
                — Treasury, state revenue offices, Federal Reserve regional
                banks, HHS, Census, and international counterparts paying for
                marginal compute on the questions they care about. Sponsored
                runs are program-related revenue that fits 501(c)(3) structure
                cleanly.
              </li>
              <li>
                <strong>National research funding</strong> — NSF, DARPA, IARPA,
                ARIA UK, NIH for specific research directions.
              </li>
              <li>
                <strong>
                  Sponsorship capital from AI labs, Big Tech, and philanthropies
                </strong>
                , per the Fradkin/Jabarian/Koh
                well-capitalized-prediction-markets model, applied to specific
                question sets the sponsor wants better-calibrated forecasts on.
              </li>
            </ul>
            <p>
              Thesis Institute funds the work through multiple channels.
              Foundation grants fund the platform and research. Sponsored
              compute pays for specific question coverage. Custom analysis
              through PolicyEngine generates additional program revenue. The
              revenue mix keeps the foundation institutionally independent.
            </p>
          </section>

          <section>
            <h2>What success looks like in five years</h2>
            <p>
              At maturity, Thesis Institute produces continuously-updated
              calibrated forecasts on every consequential government statistic,
              every encoded policy parameter, and every counterfactual
              conditional question stakeholders care about. The platform runs
              hundreds to thousands of specialized agent configurations, each
              with published methodology and visible track record. Calibration
              history goes back years and is queryable per question, per
              configuration, per resolution period. Government agencies fund
              targeted compute on their projection questions. Researchers build
              on the open infrastructure for their own work. Frontier AI labs
              use the calibration corpus as a training and evaluation resource.
              Open-source forecaster configurations and tool integrations are
              contributed by people the foundation has never met.
            </p>
            <p>
              The forecasts feed into the decisions of governments, advocacy
              organizations, firms, and individuals because calibrated
              probability distributions with visible evidence improve the
              decisions those institutions already make. The substrate
              compounds: every new tool integration, every new methodology
              insight, and every new question coverage makes everything that was
              already there more useful.
            </p>
            <p>
              And when the AI agents of 2030 arrive — substantially more capable
              than today's, better at tool selection, better at composing
              methodology, better at reasoning over their own outputs — they
              find a substrate already built for them. Open, calibrated,
              audit-trail-native, and free at the point of use. The capability
              becomes immediately deployable on consequential questions because
              the infrastructure is already there.
            </p>
          </section>

          <section>
            <h2>Honest caveats and open questions</h2>
            <p>
              <strong>
                The autonomous-improvement language is aspirational.
              </strong>{" "}
              Today's AI systems can iterate variants, tune hyperparameters, and
              generate model code, but autonomous improvement of methodology
              without sustained human guidance is years out. Honest framing:
              open human-in-the-loop improvement of AI ensembles on a
              transparent substrate, with the substrate compounding the
              human-and-AI work over time. We build collaborative compounding
              before autonomous self-improvement.
            </p>
            <p>
              <strong>The one-year launch starts narrower.</strong> The platform
              launches with a smaller agent ensemble, fewer questions, a
              narrower research program, and a working but incomplete substrate.
              Building toward the mature state takes real research and
              engineering investment over years. The vision is the north star;
              the early stages look more like a focused shipping organization
              than a complete forecasting layer.
            </p>
            <p>
              <strong>Open infrastructure depends on adoption.</strong>{" "}
              Organizations need workflows that integrate open predictions into
              real decisions. Building that institutional muscle across policy
              shops, agencies, and other users takes years. Thesis Institute
              can lead the category and still has to earn adoption one workflow
              at a time.
            </p>
            <p>
              <strong>
                Regulatory ambiguity if forecasts become market-moving.
              </strong>{" "}
              Thesis Institute publishes forecasts rather than trades, which
              avoids most prediction-market regulatory complexity. If open
              forecasts become widely consumed by financial markets, the SEC or
              CFTC may still take interest in disclosure rules. Probably
              solvable through precedents like Federal Reserve forecast
              publication, but warrants real legal review.
            </p>
            <p>
              <strong>The PolicyEngine brand transition.</strong> PolicyEngine
              continues operationally unchanged, but funders, board, and
              partners need to be brought along on the umbrella structure.
              Existing grants are to PolicyEngine via PSL Foundation fiscal
              sponsorship; the cleanest path is incorporating Thesis Institute
              as the new 501(c)(3) and graduating PolicyEngine into it from
              PSL. Donor consent process is straightforward; the communications
              work requires care.
            </p>
            <p>
              <strong>
                The naming hierarchy still needs to be explicit.
              </strong>{" "}
              Thesis Institute is the organization and public forecasting
              surface. Brier Decisions is the personal decision tool.
              PolicyEngine, Microplex, and the shared law/data substrate keep
              their own names and interfaces.
            </p>
          </section>

          <section>
            <h2>The shape of the work, in priority order</h2>
            <ul>
              <li>
                <strong>Incorporate Thesis Institute</strong> as a 501(c)(3)
                upon graduating PolicyEngine from PSL fiscal sponsorship. Use
                fiscal sponsorship during the application period.
              </li>
              <li>
                <strong>Settle the naming hierarchy</strong> publicly and
                internally before any launch announcement: foundation, platform,
                PolicyEngine, Microplex, Decisions, and the shared law/data
                substrate.
              </li>
              <li>
                <strong>Compose the board</strong> with AI-safety, policy, and
                technical credibility — names that signal what the foundation is
                to the funder base it most needs to reach.
              </li>
              <li>
                <strong>Publish the manifesto</strong> in its public form (this
                document, rewritten for external audience) with accompanying
                funder one-pager and FAQ.
              </li>
              <li>
                <strong>Ship the first visible version of the platform</strong>—
                Manifold-hosted forecast experiments with full agent telemetry,
                a small set of government-data-anchored questions with published
                calibration, and the agent traces openly available.
              </li>
              <li>
                <strong>Move Microplex into PolicyEngine</strong> as the
                Enhanced CPS replacement, with the methodology and synthesizer
                code published openly.
              </li>
              <li>
                <strong>Pre-flight major funder conversations</strong> —
                Coefficient Giving, SFF, Schmidt, Anthropic-alumni outreach,
                Arnold Ventures MAI — with the manifesto and one-pager in hand.
              </li>
              <li>
                <strong>Coordinate the encoded-law substrate</strong> on shared
                roadmap for law access and government-data architecture.
              </li>
            </ul>
            <p className="text-center mt-16">
              <Link
                href="/thesis"
                className="inline-flex items-center gap-2 py-4 px-8 [font-family:var(--font-display)] text-[0.9rem] no-underline bg-[var(--theme-text)] text-[var(--theme-bg)] border border-[var(--theme-text)] rounded-lg transition-all duration-200 hover:bg-accent hover:border-accent hover:no-underline"
              >
                Read the thesis →
              </Link>
            </p>
          </section>
        </div>

        <footer className="text-center py-24 mt-16 border-t border-[var(--theme-border)] text-[var(--theme-text-muted)] text-[0.85rem]">
          <p>
            Working synthesis by <a href="https://maxghenis.com">Max Ghenis</a>.
            Living document. Not for distribution.
          </p>
        </footer>
      </article>
    </div>
  );
}
