import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { sha256Hex } from "@/data/canonical-json";
import {
  FORECAST_CELLS,
  getForecastRunEntries,
  type ForecastCell,
  type PredictionRunActivityArtifact,
} from "@/data/forecast-cells";
import { THESIS_TARGET_LEDGER } from "@/data/ledger-targets";
import { buildRecordedPredictionRunId } from "@/data/prediction-specs";
import { buildTargetArchitectureProjection } from "@/data/thesis-target-architecture";
import {
  buildTargetArchitectureChunkExport,
  buildTargetArchitectureChunkHashPayload,
  buildTargetArchitectureManifest,
  buildTargetArchitectureRootPayload,
} from "@/data/thesis-target-architecture-export";
import {
  buildScoreId,
  buildPredictionResolutionEvents,
  scoreResolvedForecastRun,
  type ObservationRecordedLedgerEntry,
} from "@/data/thesis-log";

const FULL_DIGEST = /^[0-9a-f]{64}$/;

describe("target architecture hashing", () => {
  it("commits every canonical chunk and table manifest into one root", () => {
    const projection = buildTargetArchitectureProjection([FORECAST_CELLS[0]]);
    const manifest = buildTargetArchitectureManifest(projection, {
      sourceCommit: "0123456789abcdef0123456789abcdef01234567",
    });

    // Everything below is one claim: the single published root digest
    // commits to every table manifest, every chunk, and the source commit —
    // so a verifier who checks the root has checked the whole projection.
    const CHAIN =
      "The root is the ONLY digest published for the target-architecture\n" +
      "projection. If any link below stops holding, a reader who verifies the\n" +
      "root has verified nothing about the rows they actually downloaded.\n";
    expect(
      manifest.schemaVersion,
      "The target-architecture manifest schema version moved.\n" +
        'Verifiers pin "thesis_target_architecture_manifest_v2".\n' +
        "REMEDY: bump the readers (and scripts/ingest_target_architecture.py) in\n" +
        "the same commit. DO NOT edit only this expectation.",
    ).toBe("thesis_target_architecture_manifest_v2");
    expect(
      manifest.projectionRootSha256,
      "The published root digest is not the hash of its own root payload.\n" +
        `manifest.projectionRootSha256 = ${manifest.projectionRootSha256}\n` +
        `sha256Hex(buildTargetArchitectureRootPayload(manifest)) = ` +
        `${sha256Hex(buildTargetArchitectureRootPayload(manifest))}\n` +
        CHAIN +
        "Usual cause: a field was added to the manifest but not to the root\n" +
        "payload builder (or vice versa) in\n" +
        "site/src/data/thesis-target-architecture-export.ts.\n" +
        "REMEDY: make buildTargetArchitectureManifest compute the root FROM\n" +
        "buildTargetArchitectureRootPayload so they cannot drift.",
    ).toBe(sha256Hex(buildTargetArchitectureRootPayload(manifest)));
    for (const table of manifest.tables) {
      const { sha256, ...tablePayload } = table;
      expect(
        sha256,
        `Table manifest digest does not match its own payload.\n` +
          `Table: "${table.table}" (${table.chunkCount} chunk(s)).\n` +
          `manifest sha256 = ${sha256}\n` +
          `recomputed      = ${sha256Hex(tablePayload)}\n` +
          CHAIN +
          "The root commits to these table digests, so a stale one detaches the\n" +
          `whole "${table.table}" table from the root.\n` +
          "REMEDY: recompute table digests wherever the table manifest is built,\n" +
          "in site/src/data/thesis-target-architecture-export.ts.",
      ).toBe(sha256Hex(tablePayload));
      for (const reference of table.chunks) {
        const chunk = buildTargetArchitectureChunkExport(
          projection,
          table.table,
          reference.index,
          manifest,
        );
        const where = `table "${table.table}", chunk index ${reference.index}`;
        expect(
          chunk.projectionRootSha256,
          `A chunk does not carry the root it belongs to.\n` +
            `Location: ${where}.\n` +
            `chunk.projectionRootSha256 = ${chunk.projectionRootSha256}\n` +
            `manifest root              = ${manifest.projectionRootSha256}\n` +
            CHAIN +
            "Each chunk self-identifies its generation so a downloaded chunk can be\n" +
            "matched to the manifest it was published under; without it, chunks from\n" +
            "two generations are indistinguishable and can be silently mixed.\n" +
            "REMEDY: pass the manifest through to buildTargetArchitectureChunkExport.",
        ).toBe(manifest.projectionRootSha256);
        expect(
          reference.sha256,
          `Manifest chunk digest does not match the exported chunk.\n` +
            `Location: ${where}.\n` +
            `manifest reference sha256 = ${reference.sha256}\n` +
            `recomputed from export    = ` +
            `${sha256Hex(buildTargetArchitectureChunkHashPayload(chunk))}\n` +
            CHAIN +
            "Usual cause: buildTargetArchitectureChunkHashPayload and the manifest's\n" +
            "chunking disagree about which fields are covered, or about row order.\n" +
            "REMEDY: hash the chunk through the same payload builder on both paths.\n" +
            "DO NOT re-derive the manifest digest from the chunk at publish time —\n" +
            "that makes the check tautological and hides real drift.",
        ).toBe(sha256Hex(buildTargetArchitectureChunkHashPayload(chunk)));
      }
    }

    const otherCommit = buildTargetArchitectureManifest(projection, {
      sourceCommit: "ffffffffffffffffffffffffffffffffffffffff",
    });
    expect(
      otherCommit.projectionRootSha256,
      "Two different source commits produced the SAME projection root.\n" +
        "The root must commit to the sourceCommit it was generated from, so that\n" +
        "a published root identifies exactly one revision of the generator. If it\n" +
        "does not, two builds of different code are indistinguishable by digest\n" +
        "and the audit chain cannot say which produced a given row.\n" +
        "REMEDY: include sourceCommit in buildTargetArchitectureRootPayload\n" +
        "(site/src/data/thesis-target-architecture-export.ts).",
    ).not.toBe(manifest.projectionRootSha256);
  });

  it("hashes every chunk of a table larger than the chunk boundary", () => {
    const projection = buildTargetArchitectureProjection([FORECAST_CELLS[0]]);
    const template = projection.targets[0];
    projection.targets = Array.from({ length: 10_001 }, (_, index) => ({
      ...template,
      targetId: `target.synthetic.${index}`,
      slug: `synthetic-${index}`,
      dataPointId: `synthetic.${index}`,
    }));
    projection.counts.targets = projection.targets.length;

    const manifest = buildTargetArchitectureManifest(projection, {
      sourceCommit: "0123456789abcdef0123456789abcdef01234567",
    });
    const targets = manifest.tables.find((table) => table.table === "targets");

    expect(targets?.chunkCount).toBe(2);
    expect(targets?.chunks.map((chunk) => chunk.rowCount)).toEqual([10_000, 1]);
    expect(targets?.chunks[0].sha256).not.toBe(targets?.chunks[1].sha256);
  });

  it("uses the shared canonical row digest parity vector", () => {
    const row = {
      alpha: 1,
      items: [true, null, 1e-7],
      nested: { "😀": "astral", "\uffff": "bmp" },
      timestamp: "2026-07-09T12:34:56Z",
    };

    expect(sha256Hex(row)).toBe(
      "e199cead09a282ee400e6dc9c5ab8b4c12822b75d25bc2fc84bc1a6652528402",
    );
  });

  it("defines an atomic generation pointer and locked audit-chain head", () => {
    const sql = readFileSync(
      `${process.cwd()}/supabase/migrations/20260710_verifiable_projection_snapshots.sql`,
      "utf8",
    );

    expect(sql).toContain("create table if not exists thesis_audit_chain_head");
    expect(sql).toContain("chain_sequence bigint");
    expect(sql).toContain("where singleton\n    for update");
    expect(sql).toContain("last_sequence + 1");
    expect(sql).not.toContain("order by event_time desc");
    expect(sql).toContain(
      "create table if not exists thesis_projection_generations",
    );
    expect(sql).toContain(
      "create table if not exists thesis_projection_active_generation",
    );
    expect(sql).toContain("thesis_projection_generations_append_only");
  });

  it("builds a synthetic catalog at three times today's target count", () => {
    const template = FORECAST_CELLS[0];
    const syntheticCatalog = Array.from(
      { length: FORECAST_CELLS.length * 3 },
      (_, index): ForecastCell => ({
        ...template,
        slug: `synthetic-scale-${index}`,
        title: `Synthetic scale target ${index}`,
        question: `Synthetic projection scaling target ${index}`,
        dataPointId: undefined,
        policyParameter: undefined,
        conditionalOn: undefined,
        series: undefined,
        predictionRun: undefined,
        comparisonRuns: undefined,
        resolvedOutcome: undefined,
        resolutionSourceUrl: `https://example.gov/synthetic/${index}`,
        reasoning: [],
      }),
    );

    const projection = buildTargetArchitectureProjection(syntheticCatalog);

    expect(projection.counts.targets).toBe(FORECAST_CELLS.length * 3);
    expect(projection.counts.forecastRuns).toBe(projection.counts.targets);
    expect(projection.counts.forecastDistributionPoints).toBe(
      projection.counts.forecastRuns * 201,
    );
  }, 60_000);

  it("builds the real catalog without collisions and guards its ID projection", () => {
    // Pinned grand totals would break the publish gate on every legitimate
    // wave, so this asserts the invariants the snapshot stood for instead:
    // globally unique identifiers, counts that describe the projection
    // exactly, and a fully deterministic ID projection for identical input.
    const projection = buildTargetArchitectureProjection(
      FORECAST_CELLS,
      THESIS_TARGET_LEDGER,
    );
    const identifierProjection = (candidate: typeof projection) => ({
      targetIds: candidate.targets.map((row) => row.targetId),
      sourceSeriesIds: candidate.sourceSeries.map((row) => row.sourceSeriesId),
      runIds: candidate.forecastRuns.map((row) => row.runId),
      artifactRefIds: candidate.artifactRefs.map((row) => row.artifactRefId),
    });
    const identifiers = identifierProjection(projection);
    for (const [family, ids] of Object.entries(identifiers)) {
      expect(new Set(ids).size, `${family} must be collision-free`).toBe(
        ids.length,
      );
      expect(ids.length, `${family} must be non-empty`).toBeGreaterThan(0);
    }

    const countedTables: Record<string, number | undefined> = {
      targets: projection.targets.length,
      sourceSeries: projection.sourceSeries.length,
      forecastRuns: projection.forecastRuns.length,
      artifactRefs: projection.artifactRefs.length,
      observations: projection.observations.length,
      observationVintages: projection.observationVintages.length,
      forecastDistributionPoints: projection.forecastDistributions.length,
    };
    for (const [key, expected] of Object.entries(countedTables)) {
      expect(
        projection.counts[key as keyof typeof projection.counts],
        `counts.${key} must describe the projection exactly`,
      ).toBe(expected);
    }
    expect(projection.counts.targetVersions).toBe(projection.counts.targets);
    expect(projection.counts.observationVintages).toBe(
      projection.counts.observations,
    );

    const rebuilt = buildTargetArchitectureProjection(
      FORECAST_CELLS,
      THESIS_TARGET_LEDGER,
    );
    expect(sha256Hex(identifierProjection(rebuilt))).toBe(
      sha256Hex(identifiers),
    );

    expect(
      Array.from(
        new Set(
          projection.forecastDistributions
            .filter(
              (point) =>
                !["agent_reported", "interval_seeded"].includes(
                  point.distributionProvenance,
                ) || !point.transformVersion.endsWith("_v1"),
            )
            .map(
              (point) =>
                `provenance=${point.distributionProvenance}, ` +
                `transformVersion=${point.transformVersion}`,
            ),
        ),
      ),
      "Forecast distribution points carry an unrecognized provenance or\n" +
        "transform version (distinct offending combinations listed above; there\n" +
        `are ${projection.forecastDistributions.length} points in total).\n` +
        "Every published CDF point must say whether the agent reported the\n" +
        "distribution itself (agent_reported) or the site seeded it from the\n" +
        "stated interval (interval_seeded), and must name a _v1 transform.\n" +
        "Scores are only comparable across runs if that distinction is recorded:\n" +
        "an interval-seeded CDF is the site's construction, not the agent's, and\n" +
        "silently mixing the two attributes site-made sharpness to the agent.\n" +
        "REMEDY: set the provenance where the distribution is built in\n" +
        "site/src/data/prediction-distribution.ts. A genuinely new transform must\n" +
        "be versioned and added here AND to the score-ID payload, so old scores\n" +
        "do not silently change meaning. DO NOT just append the new string.",
    ).toEqual([]);
  });

  it("retains full payload digests while truncating public IDs to 16 hex", () => {
    const projection = buildTargetArchitectureProjection(
      FORECAST_CELLS,
      THESIS_TARGET_LEDGER,
    );

    // These were `.every(...)` booleans, which render as a bare
    // `expected false to be true`. Collect the offenders instead so the
    // failure names the row and the value that broke the rule.
    const TRUNCATION_RULE =
      "The split rule: public IDs may be truncated to 16 hex for readability,\n" +
      "but the digest a verifier recomputes must stay the FULL 64-hex sha256.\n" +
      "A truncated payload digest is not a collision-resistant commitment, so\n" +
      "silently shortening one turns a verifiable row into a decorative one.\n" +
      "REMEDY: truncate only when building the *Id fields in\n" +
      "site/src/data/thesis-target-architecture.ts. DO NOT loosen FULL_DIGEST.";
    expect(
      projection.observations.length,
      "The real catalog projected zero observations, so this digest gate\n" +
        "checked nothing. Either the ledger join broke or THESIS_TARGET_LEDGER\n" +
        "is empty — both would also empty the resolved/scored surfaces.",
    ).toBeGreaterThan(0);
    expect(
      projection.observations
        .filter((row) => !FULL_DIGEST.test(row.payloadHash))
        .map((row) => `${row.observationId} -> payloadHash=${row.payloadHash}`),
      `Observations whose payloadHash is not a full 64-hex digest.\n${TRUNCATION_RULE}`,
    ).toEqual([]);
    expect(
      projection.observationVintages
        .filter((row) => !FULL_DIGEST.test(row.normalizedPayloadHash))
        .map(
          (row) =>
            `${row.vintageId} -> normalizedPayloadHash=${row.normalizedPayloadHash}`,
        ),
      `Observation vintages whose normalizedPayloadHash is not a full 64-hex digest.\n` +
        "This digest is what proves a revision is the same bytes the resolver\n" +
        `fetched, so it must survive at full width.\n${TRUNCATION_RULE}`,
    ).toEqual([]);
    expect(
      projection.packVersions
        .filter((row) => !FULL_DIGEST.test(row.promptContentHash))
        .map(
          (row) =>
            `${row.packVersionId} -> promptContentHash=${row.promptContentHash}`,
        ),
      `Pack versions whose promptContentHash is not a full 64-hex digest.\n` +
        "Pack comparisons are only meaningful if each pack version is pinned to\n" +
        `the exact prompt content it shipped.\n${TRUNCATION_RULE}`,
    ).toEqual([]);
    expect(
      projection.strategyVersions
        .filter(
          (row) =>
            (row.promptPolicyHash && !FULL_DIGEST.test(row.promptPolicyHash)) ||
            (row.toolPolicyHash && !FULL_DIGEST.test(row.toolPolicyHash)),
        )
        .map(
          (row) =>
            `${row.strategyVersionId} -> promptPolicyHash=${String(row.promptPolicyHash)}, ` +
            `toolPolicyHash=${String(row.toolPolicyHash)}`,
        ),
      `Strategy versions carrying a policy hash that is present but not a full\n` +
        "64-hex digest. (Absent hashes are allowed — legacy strategy versions\n" +
        "predate policy pinning — but a present one must be complete.)\n" +
        "These hashes are what separate two prompt/tool lanes of the same agent,\n" +
        `so a mangled one silently pools them into a single lane.\n${TRUNCATION_RULE}`,
    ).toEqual([]);
    expect(
      projection.artifactRefs
        .filter((row) => !FULL_DIGEST.test(row.contentHash))
        .map((row) => `${row.artifactRefId} -> contentHash=${row.contentHash}`),
      `Artifact refs whose contentHash is not a full 64-hex digest.\n` +
        "contentHash is how an archived prompt/stdout artifact is proven to be\n" +
        `the bytes the run actually produced.\n${TRUNCATION_RULE}`,
    ).toEqual([]);
    expect(
      projection.artifactRefs
        .filter(
          (row) =>
            /^artifact\.[0-9a-f]+$/.test(row.artifactRefId) &&
            !/^artifact\.[0-9a-f]{16}$/.test(row.artifactRefId),
        )
        .map((row) => row.artifactRefId),
      "Digest-derived artifact ref IDs that are not exactly 16 hex chars.\n" +
        "Public artifact IDs are the truncated form (artifact.<16 hex>); an ID of\n" +
        "some other length means the truncation width drifted, which would\n" +
        "re-key every published artifact reference at once.\n" +
        "Note the filter: only IDs already shaped `artifact.<hex>` are checked,\n" +
        "so human-readable artifact IDs are deliberately exempt.\n" +
        "REMEDY: fix the truncation in site/src/data/thesis-target-architecture.ts.\n" +
        "DO NOT change the width to match — 16 hex is the published contract, and\n" +
        "the collision guard (see the colliding-artifact test in this file)\n" +
        "assumes it.",
    ).toEqual([]);
  });

  it("throws with both payload digests when truncated artifact IDs collide", () => {
    const base = FORECAST_CELLS.find((forecast) => forecast.predictionRun);
    if (!base?.predictionRun) throw new Error("Expected a recorded forecast");
    const prefix = "0123456789abcdef";
    const firstDigest = `${prefix}${"0".repeat(48)}`;
    const secondDigest = `${prefix}${"f".repeat(48)}`;
    const activityLog: PredictionRunActivityArtifact[] = [
      {
        artifactType: "prompt",
        path: "collision/first.txt",
        sha256: firstDigest,
        bytes: 1,
        createdAt: base.predictionRun.runAt,
      },
      {
        artifactType: "stdout",
        path: "collision/second.txt",
        sha256: secondDigest,
        bytes: 1,
        createdAt: base.predictionRun.runAt,
      },
    ];
    const collidingForecast: ForecastCell = {
      ...base,
      predictionRun: { ...base.predictionRun, activityLog },
    };

    expect(() =>
      buildTargetArchitectureProjection([collidingForecast]),
    ).toThrow(new RegExp(`${firstDigest} and ${secondDigest}`));
  });

  it("commits run IDs to the forecast output distribution summary", () => {
    const forecast = FORECAST_CELLS[0];
    const run = getForecastRunEntries(forecast)[0];
    const originalId = buildRecordedPredictionRunId(
      forecast,
      run.predictionRun?.runAt,
      run.variantId,
      run,
    );
    const changedId = buildRecordedPredictionRunId(
      forecast,
      run.predictionRun?.runAt,
      run.variantId,
      { ...run, pointEstimate: run.pointEstimate + 1 },
    );

    expect(originalId).toMatch(/\.[0-9a-f]{16}$/);
    expect(changedId).not.toBe(originalId);
  });

  it("commits resolution hashes and score IDs to the observed value", () => {
    const forecast = FORECAST_CELLS.find((row) => row.dataPointId);
    if (!forecast?.dataPointId) throw new Error("Expected a ledger target");
    const run = getForecastRunEntries(forecast)[0];
    const observation: ObservationRecordedLedgerEntry = {
      kind: "observation_recorded",
      observationId: `obs.${forecast.dataPointId}`,
      dataPointId: forecast.dataPointId,
      periodLabel: forecast.resolutionDate,
      value: run.pointEstimate,
      unit: forecast.unit,
      observedAt: forecast.resolutionDate,
      resolvedAt: forecast.resolutionDate,
      sourceKind: "official_release",
      source: forecast.resolutionSource,
      sourceUrl: forecast.resolutionSourceUrl,
    };
    const changedObservation = { ...observation, value: observation.value + 1 };
    const originalEvent = buildPredictionResolutionEvents(
      [forecast],
      [observation],
    )[0];
    const changedEvent = buildPredictionResolutionEvents(
      [forecast],
      [changedObservation],
    )[0];
    const originalScore = scoreResolvedForecastRun(forecast, run, [
      observation,
    ]);
    const changedScore = scoreResolvedForecastRun(forecast, run, [
      changedObservation,
    ]);
    const scoreProjection = buildTargetArchitectureProjection(
      [forecast],
      [observation],
    );

    expect(originalEvent.payloadHash).toMatch(FULL_DIGEST);
    expect(changedEvent.payloadHash).not.toBe(originalEvent.payloadHash);
    expect(originalScore?.scoreId).toContain(
      "numeric_cdf_crps_v3_ledger_scale",
    );
    expect(originalScore?.scoreId).toMatch(/\.[0-9a-f]{16}$/);
    expect(changedScore?.scoreId).not.toBe(originalScore?.scoreId);
    expect(scoreProjection.scores.length).toBeGreaterThan(0);
    expect(
      scoreProjection.scores.every(
        (score) =>
          ["agent_reported", "interval_seeded"].includes(
            score.distributionProvenance,
          ) && score.transformVersion.endsWith("_v1"),
      ),
    ).toBe(true);
    expect(
      scoreProjection.scores.every((score) =>
        FULL_DIGEST.test(score.scoreHash),
      ),
    ).toBe(true);
  });

  it("commits score IDs to the distribution transform version", () => {
    const payload = {
      runId: "run.test",
      resolutionEventId: "resolution_event.test",
      scoringRule: "numeric_cdf_crps_v3_ledger_scale" as const,
      forecastOutput: { pointEstimate: 1 },
      outcome: { observedValue: 1 },
      normalizationScale: 1,
      normalizationScaleSource: "ledger_dispersion",
      normalizationScaleCutoff: "2026-06-01T00:00:00Z",
      normalizationScaleObservationCount: 3,
      observedAt: "2026-07-01T00:00:00Z",
      chronology: "verified",
      chronologyPolicy: "test",
      contractBinding: "contract_bound",
      contractBindingPolicy: "test",
      conditionId: null,
      conditionStatus: null,
    };

    expect(
      buildScoreId({ ...payload, transformVersion: "interval_anchor_v1" }),
    ).not.toBe(
      buildScoreId({ ...payload, transformVersion: "interval_anchor_v2" }),
    );
  });
});
