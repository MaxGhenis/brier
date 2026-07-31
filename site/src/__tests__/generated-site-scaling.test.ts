import { describe, expect, it } from "vitest";
import { sha256Hex } from "@/data/canonical-json";
import { FORECAST_CELLS } from "@/data/forecast-cells";
import { buildForecastListing } from "@/data/forecast-listing";
import { THESIS_TARGET_LEDGER } from "@/data/ledger-targets";
import {
  buildThesisLogChunk,
  buildThesisLogData,
  buildThesisLogManifest,
  THESIS_LOG_CHUNK_COLLECTIONS,
} from "@/data/thesis-log";

describe("generated-site scaling surfaces", () => {
  it("projects the forecast catalog to compact listing-only fields", () => {
    const listing = buildForecastListing(FORECAST_CELLS);

    expect(
      listing,
      "buildForecastListing dropped or duplicated rows: the /forecasts browser\n" +
        `renders one row per catalog cell, so the listing must be exactly as long\n` +
        `as FORECAST_CELLS (${FORECAST_CELLS.length}).\n` +
        "REMEDY: fix the projection in site/src/data/forecast-listing.ts — a cell\n" +
        "silently missing here is a forecast nobody can find from the browser.\n" +
        "DO NOT relax the length check to match the projection.",
    ).toHaveLength(FORECAST_CELLS.length);
    const LISTING_FIELDS = [
      "country",
      "interval",
      "point",
      "publisher",
      "resolutionDate",
      "slug",
      "status",
      "title",
      "type",
    ].sort();
    expect(
      Object.keys(listing[0]).sort(),
      "The listing row shape changed. The listing is the payload every\n" +
        "/forecasts visitor downloads before clicking anything, so its field set\n" +
        "is deliberately frozen to the nine columns the browser and its filters\n" +
        "actually read (publisher/country/status/title are the only facets — see\n" +
        "site/src/data/forecast-publishers.ts; there is no topic/tag layer).\n" +
        `Sample row: ${listing[0]?.slug ?? "(none)"}.\n` +
        "REMEDY: if a field genuinely belongs on the browser, add it here AND to\n" +
        "buildForecastListing together. If it is only needed on a cell page, read\n" +
        "it from the full cell there instead of widening the listing. DO NOT just\n" +
        "append the new key to this expected list to get green — every added\n" +
        "field multiplies by the catalog size on every page load.",
    ).toEqual(LISTING_FIELDS);
    expect(
      JSON.stringify(listing),
      "A heavy per-cell field leaked into the listing payload.\n" +
        "Forbidden keys: activityLog, reasoning, historicalContext,\n" +
        "predictionDistribution — these are the multi-KB-per-cell structures the\n" +
        "chunked log exists to keep OUT of the initial browser payload.\n" +
        "REMEDY: strip the field in buildForecastListing\n" +
        "(site/src/data/forecast-listing.ts). DO NOT delete this assertion; it is\n" +
        "the only thing keeping the browser payload from growing with trace depth.",
    ).not.toMatch(/activityLog|reasoning|historicalContext|predictionDistribution/);
    const listingBytes = Buffer.byteLength(JSON.stringify(listing));
    expect(
      listingBytes,
      `The forecast listing payload is ${listingBytes} bytes across ` +
        `${listing.length} cells (~${Math.round(listingBytes / Math.max(listing.length, 1))} ` +
        "bytes/cell); the budget is 1 MiB.\n" +
        "REMEDY: shrink the per-row projection, or chunk the listing the way the\n" +
        "thesis log is chunked. DO NOT raise the budget: this payload is fetched\n" +
        "on every /forecasts page load, and the ceiling is what forces the\n" +
        "listing to stay a listing as the catalog grows.",
    ).toBeLessThan(1024 * 1024);
  });

  it("makes every v2 heavy row reachable through verified v3 chunks", () => {
    const data = buildThesisLogData(FORECAST_CELLS, THESIS_TARGET_LEDGER);
    const manifest = buildThesisLogManifest(data);

    expect(
      manifest.schemaVersion,
      "The thesis log manifest schema version moved. Consumers pin\n" +
        '"thesis_log_v3" (site/src/app/forecasts/log.json/route.ts and any\n' +
        "external reader of the published log).\n" +
        "REMEDY: if the change is intentional, bump the readers in the same\n" +
        "commit. DO NOT edit only this expectation — a manifest that claims a\n" +
        "version nobody serves silently breaks every chunk fetch.",
    ).toBe("thesis_log_v3");
    // Projection: name the offending key instead of four anonymous
    // `expected true to be false` failures.
    const HEAVY_KEYS = ["entries", "specs", "runs", "scores"] as const;
    expect(
      HEAVY_KEYS.filter((key) => key in manifest),
      "The v3 manifest inlined a heavy collection again. The manifest is an\n" +
        "index: it carries per-collection chunk references (index, count,\n" +
        "sha256) and nothing else, so that /forecasts/log.json stays small and\n" +
        "readers pull rows through /log/<collection>/<chunk>.json.\n" +
        "The keys listed above were found inlined.\n" +
        "REMEDY: move the collection into THESIS_LOG_CHUNK_COLLECTIONS in\n" +
        "site/src/data/thesis-log.ts and let buildThesisLogChunk serve it. DO NOT\n" +
        "delete this check — inlining is exactly the regression that made the\n" +
        "manifest unbounded before v3.",
    ).toEqual([]);
    const manifestBytes = Buffer.byteLength(JSON.stringify(manifest));
    expect(
      manifestBytes,
      `The thesis log manifest is ${manifestBytes} bytes; the budget is 4 MiB.\n` +
        "Chunk references are ~100 bytes each, so blowing this budget means a\n" +
        "collection is either inlined or chunked far too finely\n" +
        `(THESIS_LOG_CHUNK_SIZE is 100 rows).\n` +
        "REMEDY: find the collection that grew and chunk it. DO NOT raise the\n" +
        "budget; the manifest is fetched before any chunk is.",
    ).toBeLessThan(4 * 1024 * 1024);

    for (const collection of THESIS_LOG_CHUNK_COLLECTIONS) {
      const rows: unknown[] = [];
      for (const reference of manifest.collections[collection].chunks) {
        const chunk = buildThesisLogChunk(data, collection, reference.index);
        const where =
          `collection "${collection}", chunk index ${reference.index} ` +
          `(served at /log/${collection}/${reference.index}.json)`;
        expect(
          reference.sha256,
          `Manifest digest does not match the chunk the site would serve.\n` +
            `Location: ${where}.\n` +
            `manifest says sha256 = ${reference.sha256}\n` +
            `rebuilt chunk hashes to  ${sha256Hex(chunk)}\n` +
            "The manifest is what an external verifier checks a downloaded chunk\n" +
            "against, so a mismatch means every published verification of this\n" +
            "collection fails — the log stops being independently checkable.\n" +
            "Usual cause: buildThesisLogManifest and buildThesisLogChunk drifted\n" +
            "apart (different ordering, or a field added to one path only).\n" +
            "REMEDY: make both derive from the same buildThesisLogData rows in\n" +
            "site/src/data/thesis-log.ts. DO NOT recompute the manifest digest\n" +
            "from the chunk to silence this — that would make the check tautological.",
        ).toBe(sha256Hex(chunk));
        expect(
          reference.count,
          `Manifest row count does not match the chunk.\n` +
            `Location: ${where}.\n` +
            `manifest says count = ${reference.count}; chunk holds ${chunk.count}.\n` +
            "Readers use the manifest count to know when they have the whole\n" +
            "collection, so a wrong count truncates or over-reads the log.\n" +
            "REMEDY: as above — one source of truth for chunking in\n" +
            "site/src/data/thesis-log.ts.",
        ).toBe(chunk.count);
        rows.push(...chunk.rows);
      }
      // Projection: full row equality on thousands of objects renders as an
      // unreadable JSON wall, so lead with the shape and only then compare.
      expect(
        rows.length,
        `Reassembling collection "${collection}" from its chunks lost or ` +
          "duplicated rows.\n" +
          `chunks yielded ${rows.length} rows; buildThesisLogData produced ` +
          `${data[collection].length}; manifest advertises ` +
          `${manifest.collections[collection].count}.\n` +
          `Chunk boundaries: ${manifest.collections[collection].chunks
            .map((c) => `${c.index}:${c.count}`)
            .join(", ")}\n` +
          "Every heavy v2 row must remain reachable through v3 chunks; a row that\n" +
          "no chunk contains is data the site publishes in the manifest's counts\n" +
          "but can never actually serve.\n" +
          "REMEDY: check the slice arithmetic in buildThesisLogChunk\n" +
          "(site/src/data/thesis-log.ts) against THESIS_LOG_CHUNK_SIZE. DO NOT\n" +
          "adjust the manifest count to match the chunks.",
      ).toBe(data[collection].length);
      expect(
        rows,
        `Reassembled rows for collection "${collection}" are not the rows ` +
          "buildThesisLogData produced (counts match, contents differ — so this\n" +
          "is an ordering or mutation bug, not a slicing bug).\n" +
          "The chunked log must be a faithful re-serialization of the same rows;\n" +
          "if it is not, a verifier's digest check passes while the served data\n" +
          "is a different dataset.\n" +
          "REMEDY: look for a sort or in-place mutation applied on one path only\n" +
          "in site/src/data/thesis-log.ts.",
      ).toEqual(data[collection]);
      expect(
        rows,
        `Manifest count for collection "${collection}" contradicts the rows the ` +
          "chunks actually carry: manifest says " +
          `${manifest.collections[collection].count}, chunks carry ${rows.length}.`,
      ).toHaveLength(manifest.collections[collection].count);
    }
  });
});
