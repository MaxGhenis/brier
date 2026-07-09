import { describe, expect, it } from "vitest";
import type { BrierRewardRow } from "@/data/brier-lab";
import { summarizePairedComparison } from "@/data/brier-lab";
import { canonicalStringify, sha256Hex } from "@/data/canonical-json";
import type { ForecastCell } from "@/data/forecast-cells";
import { getForecastRunEntries } from "@/data/forecast-cells";
import {
  PERSISTENCE_BASELINE_ALGORITHM_VERSION,
  PERSISTENCE_BASELINE_AGENT,
  buildLedgerPersistenceBaseline,
} from "@/data/time-series-priors";
import {
  scoreResolvedForecasts,
  withResolvedOutcomes,
  type ObservationRecordedLedgerEntry,
  type PolicyEngineLedgerEntry,
} from "@/data/thesis-log";

const RUN_AT = "2026-04-10T12:00:00Z";

function forecast(agent = "agent.with.no.special.prefix"): ForecastCell {
  return {
    slug: "fixture-april",
    country: "US",
    type: "data",
    title: "Fixture series",
    question: "Fixture series April 2026 first print",
    unit: "percent",
    pointEstimate: 11,
    ciLow: 9,
    ciHigh: 13,
    confidence: 0.8,
    resolutionDate: "2026-05-01",
    resolutionSource: "Fixture agency",
    resolutionRule: "First print",
    dataPointId: "test.series.apr_2026.first_print",
    historicalContext: [
      { label: "agent-controlled latest", value: 999 },
      { label: "agent-controlled old", value: -999 },
    ],
    drivers: ["fixture"],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: RUN_AT,
      agent,
      model: "fixture-model",
      sourceContext: [],
    },
    reasoning: [{ kind: "forecast", point: 11, ciLow: 9, ciHigh: 13 }],
  };
}

function observation(
  period: string,
  value: number,
  observedAt: string,
): ObservationRecordedLedgerEntry {
  const dataPointId = `test.series.${period}_2026.first_print`;
  return {
    kind: "observation_recorded",
    observationId: `obs.${dataPointId}`,
    dataPointId,
    periodLabel: `${period} 2026`,
    unit: "percent",
    value,
    observedAt,
    resolvedAt: observedAt,
    sourceKind: "official_release",
    source: "Fixture agency",
    sourceUrl: `https://example.test/${period}`,
  };
}

function fixtureLedger(includeHistory = true): PolicyEngineLedgerEntry[] {
  const history = includeHistory
    ? [
        observation("mar", 12, "2026-04-01T12:00:00Z"),
        observation("jan", 10, "2026-02-01T12:00:00Z"),
        observation("feb", 14, "2026-03-01T12:00:00Z"),
      ]
    : [];
  return [...history, observation("apr", 13, "2026-05-01T12:00:00Z")];
}

describe("fair ledger-backed baselines", () => {
  it("uses the ledger's last print and realized history, never agent history", () => {
    const result = buildLedgerPersistenceBaseline(forecast(), fixtureLedger());
    const run = result.comparisonRun;

    expect(result.record.status).toBe("available");
    expect(run?.pointEstimate).toBe(12);
    expect(run?.ciLow).toBe(8.4);
    expect(run?.ciHigh).toBe(15.6);
    expect(result.record.observationRefs.map((ref) => ref.value)).toEqual([
      10, 14, 12,
    ]);
    expect(result.record.observationRefs.map((ref) => ref.observedAt)).toEqual([
      "2026-02-01T12:00:00Z",
      "2026-03-01T12:00:00Z",
      "2026-04-01T12:00:00Z",
    ]);
    expect(result.record.observationRefs.map((ref) => ref.value)).not.toContain(
      999,
    );

    const artifact = run?.predictionRun.activityLog?.[0];
    const payload = {
      schemaVersion: "thesis_persistence_baseline_inputs_v1",
      algorithmVersion: PERSISTENCE_BASELINE_ALGORITHM_VERSION,
      targetDataPointId: "test.series.apr_2026.first_print",
      seriesId: "test.series",
      cutoff: RUN_AT,
      observations: result.record.observationRefs,
    };
    expect(artifact?.artifactType).toBe("baseline_inputs");
    expect(artifact?.path).toMatch(/^ledger:\/\/persistence-baselines\//);
    expect(artifact?.sha256).toBe(sha256Hex(payload));
    expect(artifact?.bytes).toBe(
      new TextEncoder().encode(canonicalStringify(payload)).byteLength,
    );
    expect(artifact?.observationRefs).toEqual(result.record.observationRefs);
  });

  it("records an unavailable baseline when the ledger has no history", () => {
    const enriched = withResolvedOutcomes([forecast()], fixtureLedger(false));
    const target = enriched[0];

    expect(target.persistenceBaseline).toMatchObject({
      status: "unavailable",
      observationRefs: [],
      reason: "ledger has no pre-cutoff observations for the target series",
    });
    expect(
      getForecastRunEntries(target).some(
        (run) => run.predictionRun?.agent === PERSISTENCE_BASELINE_AGENT,
      ),
    ).toBe(false);
  });

  it("adds persistence coverage for every verified primary agent prefix", () => {
    const enriched = withResolvedOutcomes(
      [forecast("completely-unselected-agent")],
      fixtureLedger(),
    );
    const scores = scoreResolvedForecasts(enriched, fixtureLedger()).filter(
      (score) => score.chronology === "verified",
    );

    expect(enriched[0].persistenceBaseline?.status).toBe("available");
    expect(
      scores.some((score) => score.agent === PERSISTENCE_BASELINE_AGENT),
    ).toBe(true);
  });

  it("computes target-paired skill and win rate", () => {
    const row = (predictionId: string, normalizedCrps: number, agent: string) =>
      ({
        predictionId,
        agent,
        reward: {
          value: -normalizedCrps,
          components: { normalizedCrps },
        },
      }) as BrierRewardRow;
    const summary = summarizePairedComparison(
      [row("a", 0.3, "agent"), row("b", 0.5, "agent")],
      [
        row("a", 0.4, PERSISTENCE_BASELINE_AGENT),
        row("b", 0.2, PERSISTENCE_BASELINE_AGENT),
      ],
    );

    expect(summary.pairedTargets).toBe(2);
    expect(summary.meanAgentMinusBaselineNormalizedCrps).toBeCloseTo(0.1);
    expect(summary.agentWinRate).toBe(0.5);
  });
});
