import { describe, expect, it } from "vitest";
import { FORECAST_CELLS } from "@/data/forecast-cells";

// Quality bar for the thesis.analyst pipeline: any cell published as a
// recorded agent run must carry a trace deep enough to audit — real tool
// calls with data, an explicit reference class, a quantitative derivation,
// and a stated way the forecast could miss. Older hand-authored runs are
// exempt; everything the pipeline produces from v2 on is not.

const PIPELINE_CELLS = FORECAST_CELLS.filter((cell) =>
  cell.predictionRun?.agent?.startsWith("thesis.analyst"),
);

// Shared preamble for every trace-depth failure. The rubric is enforced in
// two places and the wrong fix (weakening the test) is always the easy one,
// so every message below repeats where the cell came from and what to do.
const RESPAWN =
  "REMEDY: re-spawn this cell through the thesis.analyst pipeline until the\n" +
  "run produces a trace that satisfies the rubric, then re-convert with\n" +
  "`python3 scripts/spawned_cells_to_ts.py site/src/data/forecast-examples/<name>.ts CONST_NAME in.json`.\n" +
  "DO NOT relax this assertion, and DO NOT hand-edit the trace in the .ts file:\n" +
  "this gate is the only thing standing between the published catalog and\n" +
  "cells whose 'agent run' was never actually run. scripts/spawned_cells_to_ts.py\n" +
  "enforces byte-identical rules — a change here that is not mirrored there\n" +
  "just moves the failure to the next spawn.";

const provenance = (cell: (typeof PIPELINE_CELLS)[number]): string =>
  [
    `cell slug:   ${cell.slug}`,
    `dataPointId: ${cell.dataPointId ?? "(none)"}`,
    `agent:       ${cell.predictionRun?.agent ?? "(none)"} @ ${cell.predictionRun?.agentVersion ?? "(no version)"}`,
    `promptMode:  ${cell.predictionRun?.promptMode ?? "(none)"}`,
    `runAt:       ${cell.predictionRun?.runAt ?? "(none)"}`,
    `source file: site/src/data/forecast-examples/ (grep for "${cell.slug}")`,
  ].join("\n");

describe("agent-run trace depth", () => {
  it("has pipeline cells to check once the spawn wave lands", () => {
    expect(Array.isArray(PIPELINE_CELLS)).toBe(true);
  });

  it.each(PIPELINE_CELLS.map((cell) => [cell.slug, cell] as const))(
    "%s meets the trace-depth rubric",
    (_slug, cell) => {
      const steps = cell.reasoning;
      expect(
        steps.length,
        `Trace is too shallow to audit.\n${provenance(cell)}\n\n` +
          `The rubric requires >=7 reasoning steps; this run emitted ${steps.length} ` +
          `(${steps.map((s) => s.kind).join(", ") || "none"}).\n` +
          "A short trace almost always means the run terminated early (tool\n" +
          "budget, sandbox denial, or a truncated model response) rather than\n" +
          "that the question was easy.\n\n" +
          RESPAWN,
      ).toBeGreaterThanOrEqual(7);

      const tools = steps.filter((s) => s.kind === "tool");
      expect(
        tools.length,
        `Trace has too few real tool calls.\n${provenance(cell)}\n\n` +
          `The rubric requires >=2 "tool" steps; this run has ${tools.length}.\n` +
          `Step kinds present: ${steps.map((s) => s.kind).join(", ") || "none"}.\n` +
          "Zero tool steps is the signature of a run that could not reach the\n" +
          "network and fabricated the series instead — the read-only Codex\n" +
          "sandbox blocks all sockets, so re-spawn with\n" +
          "`--codex-sandbox workspace-write --codex-network` for targets whose\n" +
          "official endpoint the hosted web tool cannot fetch (data.census.gov).\n\n" +
          RESPAWN,
      ).toBeGreaterThanOrEqual(2);
      for (const t of tools) {
        expect(
          t.call.length,
          `Tool step has a stub call signature.\n${provenance(cell)}\n\n` +
            `Offending call: ${JSON.stringify(t.call)} (${t.call.length} chars, needs >10).\n` +
            "A call this short is a placeholder, not something that was executed.\n\n" +
            RESPAWN,
        ).toBeGreaterThan(10);
        expect(
          t.result,
          `Tool step returned no numbers.\n${provenance(cell)}\n\n` +
            `Offending call:   ${JSON.stringify(t.call)}\n` +
            `Offending result: ${JSON.stringify(t.result)}\n` +
            "Every tool step must carry data — at least one digit — because a\n" +
            "result with no numbers cannot have supplied the base rate or the\n" +
            "release date the forecast claims to rest on.\n\n" +
            RESPAWN,
        ).toMatch(/\d/);
      }

      expect(
        steps.some((s) => s.kind === "math"),
        `Trace has no quantitative derivation.\n${provenance(cell)}\n\n` +
          `The rubric requires at least one step of kind "math"; this run has ` +
          `only: ${steps.map((s) => s.kind).join(", ") || "none"}.\n` +
          "Without a math step the point estimate and interval are asserted,\n" +
          "not derived, and the run is indistinguishable from a guess.\n\n" +
          RESPAWN,
      ).toBe(true);

      // Cells spawned on/after 2026-07-05 must SHOW the interval derivation
      // (sigma or the 1.28 z-multiplier) in a math step — width from realized
      // dispersion, not a hedged template. Byte-identical regex lives in
      // scripts/spawned_cells_to_ts.py; keep them in sync.
      const runAt = cell.predictionRun?.runAt ?? "";
      // Leakage gate: the resolution must postdate the run (same cutoff and
      // semantics as scripts/spawned_cells_to_ts.py).
      if (runAt >= "2026-07-07") {
        expect(
          cell.resolutionDate > runAt.slice(0, 10),
          `Leakage gate: the outcome may already have been public when the run happened.\n` +
            `${provenance(cell)}\n\n` +
            `resolutionDate ${cell.resolutionDate} is NOT strictly after the run day ` +
            `${runAt.slice(0, 10)}.\n` +
            "A forecast whose resolution date is on or before its own run date is\n" +
            "not a forecast — the first print may already have been observable.\n" +
            "Usual cause: resolutionDate was copied from the period label or from a\n" +
            "stale release calendar instead of the publisher's next scheduled release.\n\n" +
            "REMEDY: re-check the publisher's release calendar and re-spawn with the\n" +
            "correct resolutionDate, or drop the cell. DO NOT nudge resolutionDate\n" +
            "forward by hand and DO NOT move the 2026-07-07 cutoff — the cutoff is\n" +
            "the date this rule started applying, not a knob. The same check runs in\n" +
            "scripts/spawned_cells_to_ts.py with identical semantics.",
        ).toBe(true);
      }
      if (runAt >= "2026-07-05") {
        const mathText = steps
          .filter((s) => s.kind === "math")
          .map((s) => ("text" in s ? s.text : ""))
          .join(" ");
        // ladder_v2 (pre-registered 2026-07-10) uses a quantile-native
        // derivation contract: the ladder rungs plus the interpolated tail
        // percentiles stated literally, no parametric sigma disclosure.
        // Byte-identical semantics live in scripts/spawned_cells_to_ts.py.
        const promptMode = cell.predictionRun?.promptMode ?? "";
        const mathShown =
          mathText.length > 800 ? `${mathText.slice(0, 800)}…` : mathText;
        const DERIVATION_REMEDY =
          "REMEDY: re-spawn the cell so the agent states its derivation in the\n" +
          "math step. DO NOT weaken this pattern and DO NOT paste the missing\n" +
          "sentence into the trace by hand — the gate exists so a published\n" +
          "interval's width is traceable to realized dispersion rather than to a\n" +
          "hedged template, and an interval nobody derived is unfalsifiable\n" +
          "padding. scripts/spawned_cells_to_ts.py enforces the identical rule;\n" +
          "keep the two in sync if the derivation contract ever really changes.";
        if (promptMode === "ladder_v2") {
          const rungs = (mathText.match(/P\(X\s*<=/g) ?? []).length;
          expect(
            rungs,
            `ladder_v2 derivation contract: too few CDF rungs.\n${provenance(cell)}\n\n` +
              `Found ${rungs} "P(X <= …)" rungs in the math steps; the contract requires >=3.\n` +
              `Math steps as published:\n${mathShown || "(no math step text)"}\n\n` +
              "ladder_v2 is quantile-native: the run must state the ladder it\n" +
              "actually evaluated, not a summary of it.\n\n" +
              DERIVATION_REMEDY,
          ).toBeGreaterThanOrEqual(3);
          expect(
            /10th percentile/i.test(mathText),
            `ladder_v2 derivation contract: 10th percentile never stated.\n` +
              `${provenance(cell)}\n\n` +
              `Required literal: /10th percentile/i — absent from the math steps.\n` +
              `Math steps as published:\n${mathShown || "(no math step text)"}\n\n` +
              "ladder_v2 derives ciLow by interpolating the ladder to the 10th\n" +
              `percentile, so the published ciLow (${cell.ciLow}) has no stated origin ` +
              "without it.\n\n" +
              DERIVATION_REMEDY,
          ).toBe(true);
          expect(
            /90th percentile/i.test(mathText),
            `ladder_v2 derivation contract: 90th percentile never stated.\n` +
              `${provenance(cell)}\n\n` +
              `Required literal: /90th percentile/i — absent from the math steps.\n` +
              `Math steps as published:\n${mathShown || "(no math step text)"}\n\n` +
              "ladder_v2 derives ciHigh by interpolating the ladder to the 90th\n" +
              `percentile, so the published ciHigh (${cell.ciHigh}) has no stated origin ` +
              "without it.\n\n" +
              DERIVATION_REMEDY,
          ).toBe(true);
        } else {
          expect(
            /sigma\s*[=≈:]|1\.28/i.test(mathText),
            `Interval derivation is not shown in any math step.\n${provenance(cell)}\n\n` +
              "Required pattern: /sigma\\s*[=≈:]|1.28/i — i.e. the math step must\n" +
              "state the sigma it used or the 1.28 z-multiplier that turns sigma into\n" +
              `the 80% interval [${cell.ciLow}, ${cell.ciHigh}] around ${cell.pointEstimate}.\n` +
              `Math steps as published:\n${mathShown || "(no math step text)"}\n\n` +
              "Note: cells spawned under promptMode \"ladder_v2\" are held to the\n" +
              `quantile-native contract instead; this run's promptMode is ` +
              `"${promptMode || "(unset)"}", so the sigma contract applies. If the run\n` +
              "really was a ladder run, the promptMode field is what is wrong.\n\n" +
              DERIVATION_REMEDY,
          ).toBe(true);
        }
      }

      const text = steps
        .map((s) =>
          "text" in s ? s.text : "result" in s ? `${s.call} ${s.result}` : "",
        )
        .join(" ")
        .toLowerCase();
      const BASE_RATE_RE =
        /base rate|reference class|last \d+ (prints|releases|months|meetings|weeks|weekly|monthly|obs)|distribution of|(trailing|past|realized) \d+|\d+-(week|month) (range|distribution|history)|realized (volatility|distribution)|historical (range|distribution)|trailing-?\d+|month-to-month volatility|std_samp|modal outcome|market-implied|implied probabilit|p_hold/;
      const DISCONFIRM_RE =
        /outside (the|our|this) interval|outside \[|would (push|put|land|break)|upside risk|downside risk|miss(es)? (high|low)|surprise|tail (scenario|risk)|break (the|this) (model|forecast)|breach|lands? (above|below)|(above|below) the (interval|band|range)|forecast (high|low)|probability would (fall|rise)|would (fail|flip)|fails? (only )?if|wrong if|blow past|revert (into|to)|exceed (my|the) central|right-skewed|saturation tail/;
      // These two assert on a boolean rather than on `text` itself: the
      // concatenated trace runs to several KB and a toMatch diff would bury
      // the diagnosis under it.
      expect(
        BASE_RATE_RE.test(text),
        `Trace never states an outside view.\n${provenance(cell)}\n\n` +
          "No step mentions a base rate, reference class, or realized historical\n" +
          "dispersion (matched against BASE_RATE_RE in this file — an alternation\n" +
          "over the accepted phrasings, e.g. \"base rate\", \"reference class\",\n" +
          "\"last 12 prints\", \"trailing 24\", \"historical range\", \"market-implied\").\n" +
          `Trace is ${text.length} chars across ${steps.length} steps; first 500:\n` +
          `${text.slice(0, 500)}…\n\n` +
          "A run with no outside view produced a number without an anchor, which\n" +
          "is the failure mode this whole pipeline exists to prevent.\n\n" +
          "REMEDY: re-spawn so the agent actually fetches and cites the series\n" +
          "history. DO NOT add a new alternative to BASE_RATE_RE to make the\n" +
          "existing text match — widening the regex to fit a run is how the gate\n" +
          "stops meaning anything. Widen it only when a genuinely new but\n" +
          "legitimate phrasing appears, and mirror the change in\n" +
          "scripts/spawned_cells_to_ts.py.",
      ).toBe(true);
      expect(
        DISCONFIRM_RE.test(text),
        `Trace never says how the forecast could be wrong.\n${provenance(cell)}\n\n` +
          "No step contains a disconfirming consideration (matched against\n" +
          "DISCONFIRM_RE in this file — e.g. \"outside the interval\", \"upside\n" +
          "risk\", \"tail scenario\", \"would land above\", \"wrong if\", \"breach\").\n" +
          `Published interval: [${cell.ciLow}, ${cell.ciHigh}] around ${cell.pointEstimate}.\n` +
          `Trace is ${text.length} chars across ${steps.length} steps; first 500:\n` +
          `${text.slice(0, 500)}…\n\n` +
          "An 80% interval asserted with no stated way to fall outside it is a\n" +
          "confidence claim the run never tested.\n\n" +
          "REMEDY: re-spawn. DO NOT add an alternative to DISCONFIRM_RE to match\n" +
          "this particular trace — see the note on BASE_RATE_RE above; the same\n" +
          "rule lives in scripts/spawned_cells_to_ts.py.",
      ).toBe(true);

      const last = steps[steps.length - 1];
      expect(
        last.kind,
        `Trace does not end in a forecast step.\n${provenance(cell)}\n\n` +
          `Final step kind is "${last.kind}"; full sequence: ` +
          `${steps.map((s) => s.kind).join(" -> ")}.\n` +
          "The forecast step is where the published point and interval come from,\n" +
          "so a trace ending anywhere else means the run stopped before committing\n" +
          "to a number and the cell's numbers came from somewhere unaudited.\n\n" +
          RESPAWN,
      ).toBe("forecast");
      if (last.kind === "forecast") {
        // Projection: compare the whole triple at once so a mismatch shows
        // which of the three drifted instead of one anonymous number.
        expect(
          { point: last.point, ciLow: last.ciLow, ciHigh: last.ciHigh },
          `Published numbers disagree with the trace's own forecast step.\n` +
            `${provenance(cell)}\n\n` +
            "The cell's pointEstimate/ciLow/ciHigh must be exactly what the final\n" +
            "forecast step concluded. A mismatch means the cell fields were edited\n" +
            "after the run, so the published number is not the number the agent\n" +
            "produced and every score attached to it is misattributed.\n\n" +
            "REMEDY: re-run scripts/spawned_cells_to_ts.py from the source JSON,\n" +
            "which derives both from one place. DO NOT patch either side by hand to\n" +
            "make them agree — whichever you edit, you are choosing which record to\n" +
            "falsify.",
        ).toEqual({
          point: cell.pointEstimate,
          ciLow: cell.ciLow,
          ciHigh: cell.ciHigh,
        });
      }

      // Discrete-outcome cells (rate decisions) may sit at an interval edge.
      const INTERVAL_REMEDY =
        "REMEDY: re-spawn the cell. DO NOT reorder or swap the fields by hand —\n" +
        "an interval that does not bracket its own point estimate makes CRPS and\n" +
        "the coverage statistics meaningless for this target, and silently\n" +
        "'fixing' the ordering invents an interval the agent never stated.";
      const bracket =
        `ciLow=${cell.ciLow}, pointEstimate=${cell.pointEstimate}, ciHigh=${cell.ciHigh} ` +
        "— required order is ciLow <= pointEstimate <= ciHigh (equality is\n" +
        "allowed because discrete-outcome cells such as rate decisions may sit\n" +
        "on an interval edge).\n\n";
      expect(
        cell.ciLow,
        `Interval low bound sits above the point estimate.\n${provenance(cell)}\n\n` +
          bracket +
          INTERVAL_REMEDY,
      ).toBeLessThanOrEqual(cell.pointEstimate);
      expect(
        cell.pointEstimate,
        `Point estimate sits above the interval high bound.\n${provenance(cell)}\n\n` +
          bracket +
          INTERVAL_REMEDY,
      ).toBeLessThanOrEqual(cell.ciHigh);
      expect(
        cell.ciLow,
        `Interval has zero or negative width.\n${provenance(cell)}\n\n` +
          `ciLow=${cell.ciLow} is not strictly below ciHigh=${cell.ciHigh}.\n` +
          "A degenerate interval claims certainty and scores as a point mass.\n\n" +
          INTERVAL_REMEDY,
      ).toBeLessThan(cell.ciHigh);
      expect(
        cell.resolutionSourceUrl,
        `Resolution source is not an https URL.\n${provenance(cell)}\n\n` +
          `resolutionSourceUrl = ${JSON.stringify(cell.resolutionSourceUrl)}\n` +
          "Every cell must name the exact page the resolver will read the first\n" +
          "print from, over https. A missing or plain-http URL means the cell has\n" +
          "no automatic resolution path and will strand unresolved.\n\n" +
          "REMEDY: point it at the publisher's release page and re-spawn. DO NOT\n" +
          "substitute a generic agency homepage to satisfy the pattern.",
      ).toMatch(/^https:\/\//);

      const run = cell.predictionRun!;
      expect(
        Date.parse(run.runAt),
        `Run timestamp predates the pipeline.\n${provenance(cell)}\n\n` +
          `runAt = ${run.runAt} (parsed ${Date.parse(run.runAt)}), which is not after\n` +
          "2026-06-01, the date the thesis.analyst pipeline started producing\n" +
          "recorded runs. A NaN here means runAt is unparseable.\n" +
          "An impossible runAt breaks the chronology gate that proves a forecast\n" +
          "predates its outcome, so the cell can never be scored honestly.\n\n" +
          RESPAWN,
      ).toBeGreaterThan(Date.parse("2026-06-01"));
      expect(
        run.sourceContext.length,
        `Run cites too few sources.\n${provenance(cell)}\n\n` +
          `sourceContext has ${run.sourceContext.length} entr${run.sourceContext.length === 1 ? "y" : "ies"} ` +
          `(need >=2): ${JSON.stringify(run.sourceContext)}\n` +
          "Two sources is the minimum for a real run: the release calendar that\n" +
          "fixed resolutionDate and the series history that fixed the base rate.\n" +
          "Fewer means one of those was never fetched.\n\n" +
          RESPAWN,
      ).toBeGreaterThanOrEqual(2);
      for (const url of run.sourceContext) {
        expect(
          url,
          `sourceContext entry is not a URL.\n${provenance(cell)}\n\n` +
            `Offending entry: ${JSON.stringify(url)}\n` +
            `Full sourceContext: ${JSON.stringify(run.sourceContext)}\n` +
            "sourceContext records what the run actually fetched, so a prose\n" +
            "description in place of a URL means the citation is not checkable.\n\n" +
            RESPAWN,
        ).toMatch(/^https?:\/\//);
      }

      // Versioned-agent attribution: every pipeline run names the exact
      // agent definition (semver + content hashes) that produced it.
      const ATTRIBUTION_REMEDY =
        "REMEDY: re-spawn with the current agent definition so the runner stamps\n" +
        "these fields. DO NOT fill them in by hand and DO NOT drop the assertion:\n" +
        "the whole comparison surface (agent vs agent, prompt mode vs prompt mode)\n" +
        "is only meaningful if every run names the exact definition that produced\n" +
        "it, and an invented hash silently pools two different agents into one lane.";
      expect(
        run.agentVersion,
        `Run has no valid agent version.\n${provenance(cell)}\n\n` +
          `agentVersion = ${JSON.stringify(run.agentVersion)} (expected semver, e.g. "2.1.0").\n\n` +
          ATTRIBUTION_REMEDY,
      ).toMatch(/^\d+\.\d+\.\d+$/);
      expect(
        run.promptHash,
        `Run has no valid prompt hash.\n${provenance(cell)}\n\n` +
          `promptHash = ${JSON.stringify(run.promptHash)} (expected 64 lowercase hex chars).\n\n` +
          ATTRIBUTION_REMEDY,
      ).toMatch(/^[0-9a-f]{64}$/);
      expect(
        run.toolPolicyHash,
        `Run has no valid tool-policy hash.\n${provenance(cell)}\n\n` +
          `toolPolicyHash = ${JSON.stringify(run.toolPolicyHash)} (expected 64 lowercase hex chars).\n` +
          "This hash pins which tools the run was allowed to call, which is what\n" +
          "distinguishes a networked spawn from a sandboxed one.\n\n" +
          ATTRIBUTION_REMEDY,
      ).toMatch(/^[0-9a-f]{64}$/);
    },
  );
});

describe("ladder_v2 derivation contract", () => {
  // Byte-identical semantics to scripts/spawned_cells_to_ts.py: rungs plus
  // the interpolated tail percentiles stated literally, no sigma demanded.
  const gate = (mathText: string): boolean =>
    (mathText.match(/P\(X\s*<=/g) ?? []).length >= 3 &&
    /10th percentile/i.test(mathText) &&
    /90th percentile/i.test(mathText);

  it("accepts rungs plus interpolated tail percentiles", () => {
    expect(
      gate(
        "Ladder: P(X <= 3.0) = 0.05; P(X <= 3.4) = 0.30; P(X <= 3.8) = 0.60; " +
          "P(X <= 4.2) = 0.92. Linear interpolation gives the 10th percentile " +
          "at 3.1, median at 3.7, and 90th percentile at 4.15.",
      ),
    ).toBe(true);
  });

  it("rejects rungs without percentiles and percentiles without rungs", () => {
    expect(
      gate("Ladder: P(X <= 3.0) = 0.05; P(X <= 3.4) = 0.30; P(X <= 4.2) = 0.92."),
    ).toBe(false);
    expect(gate("10th percentile at 3.1, 90th percentile at 4.15.")).toBe(false);
  });
});
