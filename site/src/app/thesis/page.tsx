import Link from "next/link";
import { Cite } from "@/components/Cite";
import { Header } from "@/components/Header";

export default function ThesisPage() {
  return (
    <div>
      <Header activePage="thesis" />
      <article className="max-w-[680px] mx-auto px-8">
        <header className="text-center py-24 border-b border-[var(--theme-border)] mb-24 animate-[fade-up_0.6s_ease-out] max-[600px]:py-16">
          <p className="[font-family:var(--font-mono)] text-[0.65rem] tracking-[0.15em] uppercase text-accent mb-4">
            The Brier thesis
          </p>
          <h1 className="[font-family:var(--font-display)] text-[clamp(2rem,5vw,3rem)] font-light leading-[1.2] mb-8 tracking-[-0.02em]">
            Forecasting as a harness
          </h1>
          <p className="text-[1.15rem] text-[var(--theme-text-muted)] max-w-[480px] mx-auto leading-[1.6]">
            Why reframing decisions as predictions leads to better outcomes—and
            how to do it.
          </p>
        </header>

        <div className="prose-content">
          <section>
            <h2>The problem with advice</h2>
            <p>
              When we ask someone—a friend, a mentor, an AI—&quot;Should I do
              X?&quot;, we&apos;re asking the wrong question. The answer we get
              depends entirely on unstated assumptions: What do we value? What
              counts as success? How certain is the advisor? None of this is
              made explicit.
            </p>
            <p>
              Worse, we can never learn from these answers. A year later, we
              can&apos;t evaluate whether the advice was good because we never
              defined what &quot;good&quot; meant. The feedback loop is broken.
            </p>
            <p>
              This isn&apos;t just a problem with AI (though AI&apos;s tendency
              toward sycophancy makes it worse
              <Cite id="1">1</Cite>). It&apos;s a problem with how we structure
              decision-making conversations. Annie Duke calls this
              &quot;resulting&quot;—judging decisions by outcomes rather than
              process
              <Cite id="16">16</Cite>. When we ask for advice and get a good
              outcome, we credit the advice. Bad outcome, we blame it. But a
              single outcome tells us almost nothing about whether the decision
              was good.
            </p>
          </section>

          <section>
            <h2>The reframe</h2>
            <p>
              Instead of asking for advice, ask for{" "}
              <em>forecasts conditional on actions</em>.
            </p>
            <p>The shift is subtle but transformative:</p>
            <blockquote>
              <p>
                <strong>Before:</strong> &quot;Should I take this job?&quot;
              </p>
              <p>
                <strong>After:</strong> &quot;If I value income, growth, and
                work-life balance, what&apos;s the probability that each of
                these exceeds my threshold under Option A vs Option B? What
                assumptions drive those estimates?&quot;
              </p>
            </blockquote>
            <p>This forces several things to happen:</p>
            <ul>
              <li>
                <strong>Values become explicit.</strong> You must state what
                you&apos;re optimizing for before anyone can help you.
              </li>
              <li>
                <strong>Uncertainty becomes visible.</strong> A forecast
                requires a confidence interval. &quot;Probably fine&quot;
                becomes &quot;70% chance, with a range of 50-85%.&quot;
              </li>
              <li>
                <strong>Assumptions surface.</strong> To make a forecast, you
                must reason about mechanisms. What needs to be true for this
                outcome to occur?
              </li>
              <li>
                <strong>Accountability emerges.</strong> Predictions can be
                scored. Opinions cannot.
              </li>
            </ul>
          </section>

          <section>
            <h2>The superforecasting connection</h2>
            <p>
              This isn&apos;t a new idea. Philip Tetlock&apos;s research on
              superforecasting
              <Cite id="2">2</Cite> identified a set of techniques that reliably
              improve predictive accuracy. In the Good Judgment Project, a small
              group of forecasters consistently beat professional intelligence
              analysts with access to classified information
              <Cite id="3">3</Cite>.
            </p>
            <p>Their techniques include:</p>
            <ul>
              <li>
                <strong>Fermi decomposition:</strong> Break complex estimates
                into simpler, estimable components
                <Cite id="4">4</Cite>.
              </li>
              <li>
                <strong>Outside view first:</strong> Start with base rates
                before adjusting for specifics—what Kahneman calls
                &quot;reference class forecasting&quot;
                <Cite id="5">5</Cite>.
              </li>
              <li>
                <strong>Calibrated confidence:</strong> Your 80% predictions
                should come true 80% of the time.
              </li>
              <li>
                <strong>Continuous updating:</strong> Revise estimates as new
                information arrives, following Bayesian principles.
              </li>
            </ul>
            <p>
              Superforecasters don&apos;t have access to secret information.
              They&apos;re just more disciplined about structuring their
              thinking. Across nearly 100 comparative studies, Dawes, Faust, and
              Meehl found that structured &quot;mechanical&quot; prediction
              equaled or outperformed unstructured expert judgment in every
              domain tested
              <Cite id="17">17</Cite>. Brier applies this discipline to
              personal and professional decisions.
            </p>
          </section>

          <section>
            <h2>Why AI makes this better</h2>
            <p>
              Large language models are surprisingly good at forecasting. LLM
              ensembles can match human crowd accuracy on prediction tasks
              <Cite id="6">6</Cite>. Halawi et al. built a retrieval-augmented
              system that approaches competitive forecaster accuracy
              <Cite id="18">18</Cite>, and AI forecasting systems like AIA
              Forecaster have achieved superforecaster-level performance through
              structured pipelines of search, independent reasoning, and
              calibration
              <Cite id="7">7</Cite>. The CAIS forecasting bot has demonstrated
              superhuman accuracy on competitive forecasting platforms
              <Cite id="8">8</Cite>. On ForecastBench, LLMs now surpass the
              median public forecaster, with projected LLM-superforecaster
              parity by late 2026
              <Cite id="28">28</Cite>.
            </p>
            <p>
              But LLMs are also prone to sycophancy: telling you what you want
              to hear rather than what&apos;s true. Research has shown this
              tendency is robust across models and contexts
              <Cite id="1">1</Cite>.
            </p>
            <p>
              The forecasting frame is a <em>harness</em> that constrains this
              tendency. When you ask an AI for a probability with a confidence
              interval, it&apos;s harder for it to simply validate your existing
              beliefs. Numbers create accountability. Xiong et al. found that
              structured elicitation strategies—multi-step prompting, top-k
              sampling—can help mitigate LLM overconfidence, though no single
              technique consistently outperforms others
              <Cite id="19">19</Cite>. How you ask matters as much as what you
              ask.
            </p>
            <p>
              More importantly, the structure itself improves thinking. Research
              on LLM-augmented forecasting found that AI assistance
              significantly boosts human forecasting accuracy, with the largest
              gains for less experienced forecasters
              <Cite id="9">9</Cite>:
            </p>
            <ul>
              <li>
                <strong>KPI definition</strong> forces you to articulate what
                you actually care about.
              </li>
              <li>
                <strong>Option expansion</strong> surfaces alternatives you
                hadn&apos;t considered.
              </li>
              <li>
                <strong>Assumption surfacing</strong> reveals where your model
                might be wrong.
              </li>
              <li>
                <strong>Sensitivity analysis</strong> shows which uncertainties
                matter most.
              </li>
            </ul>
            <p>The AI becomes a structured thinking partner, not an oracle.</p>
            <p className="bg-[var(--theme-bg-surface)] border-l-[3px] border-l-accent p-8 my-16 rounded-r [&_a]:text-accent [&_a]:no-underline [&_a:hover]:underline">
              <strong>See the research:</strong> I&apos;ve developed a
              methodology called &quot;stability-under-probing&quot; to
              empirically test whether frameworks reduce sycophancy.{" "}
              <Link href="/paper">Read the paper →</Link>
            </p>
          </section>

          <section>
            <h2>The calibration loop</h2>
            <p>
              The most powerful part of this approach is what happens over time.
              By logging your forecasts and scoring them against reality, you
              build a calibration curve.
            </p>
            <p>
              Research on expert prediction shows that without feedback, even
              domain experts are poorly calibrated
              <Cite id="10">10</Cite>. Lichtenstein, Fischhoff, and Phillips
              found that when people said they were 98% confident, they were
              correct only 68% of the time
              <Cite id="20">20</Cite>. But with structured feedback, calibration
              improves dramatically. Weather forecasters and professional
              oddsmakers—who receive regular, structured feedback on their
              probabilistic predictions—exhibited little or no overconfidence.
              The Good Judgment Project confirmed this: regular accuracy
              feedback was one of the key interventions that improved
              performance
              <Cite id="3">3</Cite>.
            </p>
            <p>
              You learn that you&apos;re overconfident on career decisions. Or
              underconfident on technical estimates. Or systematically biased
              toward optimism about timelines.
            </p>
            <p>
              This meta-knowledge is invaluable. It&apos;s not just about making
              better individual decisions—it&apos;s about understanding your own
              decision-making patterns and compensating for systematic biases.
            </p>
          </section>

          <section>
            <h2>The decision quality chain</h2>
            <p>
              Ron Howard and the Strategic Decisions Group developed a framework
              for measuring decision quality at the time of decision,
              independent of outcome
              <Cite id="21">21</Cite>. A decision is only as good as its weakest
              link across six elements: appropriate frame, creative
              alternatives, reliable information, clear values, sound reasoning,
              and commitment to action
              <Cite id="22">22</Cite>.
            </p>
            <p>
              Brier maps directly onto this chain. Defining KPIs addresses{" "}
              <em>frame</em> and <em>values</em>. Option expansion addresses{" "}
              <em>creative alternatives</em>. Forecasting with base rates
              addresses <em>reliable information</em> and{" "}
              <em>sound reasoning</em>. The calibration loop addresses the
              feedback mechanism that strengthens every link over time.
            </p>
            <p>
              The key insight from decision analysis is that you can assess
              decision quality without waiting for outcomes. Howard&apos;s
              information value theory shows that when decisions are framed as
              forecasts, you can calculate exactly how much to invest in
              resolving each uncertainty
              <Cite id="23">23</Cite>. If the expected value of learning your
              probability of success is only $50, don&apos;t spend $5,000 on a
              feasibility study.
            </p>
            <p>
              This connects to what Kahneman and Lovallo call the &quot;inside
              view&quot; versus &quot;outside view&quot;
              <Cite id="24">24</Cite>. Decision makers naturally treat each
              problem as unique, anchoring on plans and scenarios rather than
              base rates from comparable situations. Reframing decisions as
              forecasts naturally invokes the outside view by forcing explicit
              probability assessment against a reference class.
            </p>
          </section>

          <section>
            <h2>Boosting, not nudging</h2>
            <p>
              Hertwig and Grune-Yanoff distinguish &quot;nudges&quot;
              (environmental changes that steer behavior) from
              &quot;boosts&quot; (interventions that build decision-making
              competence)
              <Cite id="25">25</Cite>. A nudge might default your retirement
              savings to 10%. A boost teaches you to think about compound
              interest so you choose the right rate yourself.
            </p>
            <p>
              Brier is a boost, not a nudge. It doesn&apos;t tell you what to
              decide. It teaches a way of thinking—probabilistic, structured,
              accountable—that transfers across domains. Julia Galef calls this
              the &quot;scout mindset&quot;: treating beliefs as provisional
              hypotheses to be stress-tested, not positions to defend
              <Cite id="26">26</Cite>. The forecasting frame cultivates this
              mindset by making accuracy the explicit goal.
            </p>
            <p>
              And critically, Koriat, Lichtenstein, and Fischhoff showed that
              simply asking people to generate reasons <em>against</em> their
              preferred option eliminates overconfidence almost entirely
              <Cite id="27">27</Cite>. Structured consideration of
              alternatives—a core forecasting discipline—is one of the most
              robust debiasing techniques known.
            </p>
          </section>

          <section>
            <h2>The framework</h2>
            <p>
              Brier implements a five-step process, drawing on structured
              analytic techniques from intelligence analysis
              <Cite id="11">11</Cite> and the superforecasting literature:
            </p>
            <ol>
              <li>
                <strong>Define KPIs.</strong> What outcomes matter? Pick 1-3
                metrics you&apos;d actually use to judge success in hindsight.
                This mirrors the &quot;AIMS&quot; technique (Audience, Issue,
                Message, Storyline) from intelligence analysis
                <Cite id="11">11</Cite>.
              </li>
              <li>
                <strong>Expand options.</strong> Don&apos;t just compare A vs B.
                What about C? Waiting? A hybrid? The best option is often one
                you didn&apos;t initially consider. This combats &quot;premature
                closure&quot;—a well-documented cognitive bias
                <Cite id="12">12</Cite>.
              </li>
              <li>
                <strong>Decompose and forecast.</strong> For each option x KPI,
                apply outside view, inside view, Fermi decomposition. Produce a
                point estimate with confidence interval. Decomposition is one of
                Heuer&apos;s core structured analytic techniques
                <Cite id="11">11</Cite>.
              </li>
              <li>
                <strong>Surface assumptions.</strong> What must be true for this
                forecast to hold? What would change it? This is the &quot;key
                assumptions check&quot; from intelligence tradecraft
                <Cite id="13">13</Cite>.
              </li>
              <li>
                <strong>Log and score.</strong> Record the decision. Return in
                3-6 months. Compare predictions to reality. Update your
                calibration. Brier scores provide a proper scoring rule that
                rewards both accuracy and calibration
                <Cite id="14">14</Cite>.
              </li>
            </ol>
          </section>

          <section>
            <h2>When to use it</h2>
            <p>Brier is valuable across a range of decisions:</p>
            <ul>
              <li>
                <strong>High-stakes decisions</strong> where the cost of being
                wrong is significant.
              </li>
              <li>
                <strong>Recurring decision types</strong> where you can build
                calibration over time.
              </li>
              <li>
                <strong>Decisions with delayed feedback</strong> where you
                won&apos;t know if you were right for months or years.
              </li>
              <li>
                <strong>Decisions where you suspect motivated reasoning</strong>
                —where you might be fooling yourself
                <Cite id="15">15</Cite>.
              </li>
              <li>
                <strong>Smaller decisions as practice</strong>—building the
                habit and calibration data that pays off when stakes are high.
              </li>
            </ul>
          </section>

          <section>
            <h2>The vision</h2>
            <p>Imagine a world where every significant decision comes with:</p>
            <ul>
              <li>Explicit success criteria</li>
              <li>A range of options, not just the obvious ones</li>
              <li>Quantified predictions with uncertainty ranges</li>
              <li>Surfaced assumptions that can be tested</li>
              <li>A record that can be scored and learned from</li>
            </ul>
            <p>
              This is possible today. The tools exist. The research supports it.
              What&apos;s missing is the habit—the muscle memory of reaching for
              forecasts instead of opinions.
            </p>
            <p>
              Brier is an attempt to build that habit. Use it as a Python
              library, a CLI tool, or a Claude Code plugin. Log your decisions.
              Score your predictions. Get better over time.
            </p>
            <p className="text-center mt-16">
              <Link
                href="/"
                className="inline-flex items-center gap-2 py-4 px-8 [font-family:var(--font-display)] text-[0.9rem] no-underline bg-[var(--theme-text)] text-[var(--theme-bg)] border border-[var(--theme-text)] rounded-lg transition-all duration-200 hover:bg-accent hover:border-accent hover:no-underline"
              >
                Get started →
              </Link>
            </p>
          </section>
        </div>

        <section className="mt-24 pt-24 border-t border-[var(--theme-border)]">
          <h2 className="[font-family:var(--font-display)] text-[1.25rem] font-normal mb-8 text-[var(--theme-text)]">
            References
          </h2>
          <ol className="list-none p-0 m-0 text-[0.85rem] text-[var(--theme-text-muted)] leading-[1.6] [&_li]:mb-4 [&_li]:pl-8 [&_li]:relative [&_li>a:first-child]:absolute [&_li>a:first-child]:left-0 [&_li>a:first-child]:text-[var(--theme-text-muted)] [&_li>a:first-child]:no-underline [&_li>a:first-child]:text-[0.8em] [&_li>a:first-child:hover]:text-accent [&_em]:italic [&_a]:text-accent [&_a]:no-underline [&_a:hover]:underline">
            <li id="ref-1">
              <a href="#cite-1">↑</a> Sharma, M., et al. (2024). &quot;Towards
              Understanding Sycophancy in Language Models.&quot;{" "}
              <em>ICLR 2024</em>.{" "}
              <a
                href="https://openreview.net/forum?id=tvhaxkMKAn"
                target="_blank"
                rel="noopener noreferrer"
              >
                openreview.net
              </a>
            </li>
            <li id="ref-2">
              <a href="#cite-2">↑</a> Tetlock, P. E., & Gardner, D. (2015).{" "}
              <em>Superforecasting: The Art and Science of Prediction</em>.
              Crown.{" "}
              <a
                href="https://www.amazon.com/Superforecasting-Science-Prediction-Philip-Tetlock/dp/0804136718"
                target="_blank"
                rel="noopener noreferrer"
              >
                Amazon
              </a>
            </li>
            <li id="ref-3">
              <a href="#cite-3">↑</a> Mellers, B., et al. (2014).
              &quot;Psychological Strategies for Winning a Geopolitical
              Forecasting Tournament.&quot; <em>Psychological Science</em>,
              25(5), 1106-1115.{" "}
              <a
                href="https://doi.org/10.1177/0956797614524255"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-4">
              <a href="#cite-4">↑</a> Good Judgment.
              &quot;Superforecasters&apos; Toolbox: Fermi-ization in
              Forecasting.&quot;{" "}
              <a
                href="https://goodjudgment.com/superforecasters-toolbox-fermi-ization-in-forecasting/"
                target="_blank"
                rel="noopener noreferrer"
              >
                goodjudgment.com
              </a>
            </li>
            <li id="ref-5">
              <a href="#cite-5">↑</a> Kahneman, D., & Tversky, A. (1979).
              &quot;Intuitive Prediction: Biases and Corrective
              Procedures.&quot; <em>TIMS Studies in Management Science</em>, 12,
              313-327.
            </li>
            <li id="ref-6">
              <a href="#cite-6">↑</a> Schoenegger, P., et al. (2024).
              &quot;Wisdom of the Silicon Crowd: LLM Ensemble Prediction
              Capabilities Rival Human Crowd Accuracy.&quot;{" "}
              <em>arXiv:2402.19379</em>.{" "}
              <a
                href="https://arxiv.org/abs/2402.19379"
                target="_blank"
                rel="noopener noreferrer"
              >
                arxiv.org/abs/2402.19379
              </a>
            </li>
            <li id="ref-7">
              <a href="#cite-7">↑</a> Alur, R., et al. (2025). &quot;AIA
              Forecaster: Technical Report.&quot; <em>arXiv:2511.07678</em>.{" "}
              <a
                href="https://arxiv.org/abs/2511.07678"
                target="_blank"
                rel="noopener noreferrer"
              >
                arxiv.org/abs/2511.07678
              </a>
            </li>
            <li id="ref-8">
              <a href="#cite-8">↑</a> Center for AI Safety. &quot;Superhuman
              Automated Forecasting.&quot;{" "}
              <a
                href="https://safe.ai/blog/forecasting"
                target="_blank"
                rel="noopener noreferrer"
              >
                safe.ai/blog/forecasting
              </a>
            </li>
            <li id="ref-9">
              <a href="#cite-9">↑</a> Schoenegger, P., et al. (2024).
              &quot;AI-Augmented Predictions: LLM Assistants Improve Human
              Forecasting Accuracy.&quot; <em>arXiv:2402.07862</em>.{" "}
              <a
                href="https://arxiv.org/abs/2402.07862"
                target="_blank"
                rel="noopener noreferrer"
              >
                arxiv.org/abs/2402.07862
              </a>
            </li>
            <li id="ref-10">
              <a href="#cite-10">↑</a> Tetlock, P. E. (2005).{" "}
              <em>
                Expert Political Judgment: How Good Is It? How Can We Know?
              </em>{" "}
              Princeton University Press.{" "}
              <a
                href="https://press.princeton.edu/books/paperback/9780691128719/expert-political-judgment"
                target="_blank"
                rel="noopener noreferrer"
              >
                Princeton University Press
              </a>
            </li>
            <li id="ref-11">
              <a href="#cite-11">↑</a> Heuer, R. J., & Pherson, R. H. (2015).{" "}
              <em>Structured Analytic Techniques for Intelligence Analysis</em>{" "}
              (2nd ed.). CQ Press.{" "}
              <a
                href="https://www.amazon.com/Structured-Analytic-Techniques-Intelligence-Analysis/dp/1608710181"
                target="_blank"
                rel="noopener noreferrer"
              >
                Amazon
              </a>
            </li>
            <li id="ref-12">
              <a href="#cite-12">↑</a> Kruglanski, A. W., & Webster, D. M.
              (1996). &quot;Motivated Closing of the Mind: &apos;Seizing&apos;
              and &apos;Freezing&apos;.&quot; <em>Psychological Review</em>,
              103(2), 263-283.{" "}
              <a
                href="https://doi.org/10.1037/0033-295X.103.2.263"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-13">
              <a href="#cite-13">↑</a> CIA. (2009). &quot;A Tradecraft Primer:
              Structured Analytic Techniques for Improving Intelligence
              Analysis.&quot;{" "}
              <a
                href="https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf"
                target="_blank"
                rel="noopener noreferrer"
              >
                cia.gov
              </a>
            </li>
            <li id="ref-14">
              <a href="#cite-14">↑</a> Brier, G. W. (1950). &quot;Verification
              of Forecasts Expressed in Terms of Probability.&quot;{" "}
              <em>Monthly Weather Review</em>, 78(1), 1-3.{" "}
              <a
                href="https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-15">
              <a href="#cite-15">↑</a> Kunda, Z. (1990). &quot;The Case for
              Motivated Reasoning.&quot; <em>Psychological Bulletin</em>,
              108(3), 480-498.{" "}
              <a
                href="https://doi.org/10.1037/0033-2909.108.3.480"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-16">
              <a href="#cite-16">↑</a> Duke, A. (2018).{" "}
              <em>
                Thinking in Bets: Making Smarter Decisions When You Don&apos;t
                Have All the Facts
              </em>
              . Portfolio/Penguin.
            </li>
            <li id="ref-17">
              <a href="#cite-17">↑</a> Dawes, R. M., Faust, D., & Meehl, P. E.
              (1989). &quot;Clinical Versus Actuarial Judgment.&quot;{" "}
              <em>Science</em>, 243(4899), 1668-1674.{" "}
              <a
                href="https://doi.org/10.1126/science.2648573"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-18">
              <a href="#cite-18">↑</a> Halawi, D., Zhang, F., Chen, Y.-H., &
              Steinhardt, J. (2024). &quot;Approaching Human-Level Forecasting
              with Language Models.&quot; <em>NeurIPS 2024</em>.{" "}
              <a
                href="https://arxiv.org/abs/2402.18563"
                target="_blank"
                rel="noopener noreferrer"
              >
                arxiv.org/abs/2402.18563
              </a>
            </li>
            <li id="ref-19">
              <a href="#cite-19">↑</a> Xiong, M., Hu, Z., Lu, X., et al. (2024).
              &quot;Can LLMs Express Their Uncertainty? An Empirical Evaluation
              of Confidence Elicitation in LLMs.&quot; <em>ICLR 2024</em>.{" "}
              <a
                href="https://arxiv.org/abs/2306.13063"
                target="_blank"
                rel="noopener noreferrer"
              >
                arxiv.org/abs/2306.13063
              </a>
            </li>
            <li id="ref-20">
              <a href="#cite-20">↑</a> Lichtenstein, S., Fischhoff, B., &
              Phillips, L. D. (1982). &quot;Calibration of Probabilities: The
              State of the Art to 1980.&quot; In D. Kahneman, P. Slovic, & A.
              Tversky (Eds.),{" "}
              <em>Judgment under Uncertainty: Heuristics and Biases</em> (pp.
              306-334). Cambridge University Press.
            </li>
            <li id="ref-21">
              <a href="#cite-21">↑</a> Howard, R. A. (1988). &quot;Decision
              Analysis: Practice and Promise.&quot; <em>Management Science</em>,
              34(6), 679-695.{" "}
              <a
                href="https://doi.org/10.1287/mnsc.34.6.679"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-22">
              <a href="#cite-22">↑</a> Spetzler, C., Winter, H., & Meyer, J.
              (2016).{" "}
              <em>
                Decision Quality: Value Creation from Better Business Decisions
              </em>
              . Wiley.
            </li>
            <li id="ref-23">
              <a href="#cite-23">↑</a> Howard, R. A. (1966). &quot;Information
              Value Theory.&quot;{" "}
              <em>IEEE Transactions on Systems Science and Cybernetics</em>,
              2(1), 22-26.{" "}
              <a
                href="https://doi.org/10.1109/TSSC.1966.300074"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-24">
              <a href="#cite-24">↑</a> Kahneman, D., & Lovallo, D. (1993).
              &quot;Timid Choices and Bold Forecasts: A Cognitive Perspective on
              Risk Taking.&quot; <em>Management Science</em>, 39(1), 17-31.{" "}
              <a
                href="https://doi.org/10.1287/mnsc.39.1.17"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-25">
              <a href="#cite-25">↑</a> Hertwig, R., & Grune-Yanoff, T. (2017).
              &quot;Nudging and Boosting: Steering or Empowering Good
              Decisions.&quot; <em>Perspectives on Psychological Science</em>,
              12(6), 973-986.{" "}
              <a
                href="https://doi.org/10.1177/1745691617702496"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-26">
              <a href="#cite-26">↑</a> Galef, J. (2021).{" "}
              <em>
                The Scout Mindset: Why Some People See Things Clearly and Others
                Don&apos;t
              </em>
              . Portfolio/Penguin.
            </li>
            <li id="ref-27">
              <a href="#cite-27">↑</a> Koriat, A., Lichtenstein, S., &
              Fischhoff, B. (1980). &quot;Reasons for Confidence.&quot;{" "}
              <em>
                Journal of Experimental Psychology: Human Learning and Memory
              </em>
              , 6(2), 107-118.{" "}
              <a
                href="https://doi.org/10.1037/0278-7393.6.2.107"
                target="_blank"
                rel="noopener noreferrer"
              >
                DOI
              </a>
            </li>
            <li id="ref-28">
              <a href="#cite-28">↑</a> Karger, E., et al. (2025).
              &quot;ForecastBench: A Dynamic Benchmark of AI Forecasting
              Capabilities.&quot; <em>ICLR 2025</em>.{" "}
              <a
                href="https://openreview.net/forum?id=lfPkGWXLLf"
                target="_blank"
                rel="noopener noreferrer"
              >
                openreview.net
              </a>
            </li>
          </ol>
        </section>

        <footer className="text-center py-24 mt-16 border-t border-[var(--theme-border)] text-[var(--theme-text-muted)] text-[0.85rem]">
          <p>
            Written by <a href="https://maxghenis.com">Max Ghenis</a>.
            Brier is{" "}
            <a href="https://github.com/MaxGhenis/brier">open source</a>.
          </p>
        </footer>
      </article>
    </div>
  );
}
