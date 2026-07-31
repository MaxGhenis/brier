import { describe, expect, it } from "vitest";
import { loadBills } from "@/data/bills";

/**
 * Fail-closed gate for bill.json artifacts — the bills/ analog of the
 * trace-depth rubric. Motivated by the 2026-07-31 Farm Bill port: the
 * hand-assembled analysis shipped with mid-word truncations (an
 * authoring-time output limit) and four-newline holes where the retired
 * standalone site interleaved quotes into prose. Nothing gated the
 * artifact, so damaged analysis sat on a live page. Agent-generated
 * analyses (ingest_bill.py) will hit the same failure modes at higher
 * volume — this test rejects them at CI time.
 */

// Sentence-final punctuation, allowing trailing quotes/parens/markdown.
const COMPLETE = /[.!?]["”’)*`\]]*\s*$/;
const STANCES = new Set(["serves", "opposes", "orthogonal"]);

const bills = loadBills();

describe("bill artifacts", () => {
  it("at least one artifact loads", () => {
    expect(bills.length).toBeGreaterThan(0);
  });

  for (const entry of bills) {
    describe(entry.slug, () => {
      it("has complete bill metadata", () => {
        expect(entry.bill.name).toBeTruthy();
        expect(entry.bill.status).toBeTruthy();
        expect(entry.bill.sourceUrl).toMatch(/^https?:\/\//);
        expect(entry.bill.analysisDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
        expect(entry.provisions.length).toBeGreaterThan(0);
      });

      for (const [i, provision] of entry.provisions.entries()) {
        describe(`provision ${i}: ${provision.heading.slice(0, 50)}`, () => {
          it("has title, heading, and non-empty quote", () => {
            expect(provision.title).toBeTruthy();
            expect(provision.heading).toBeTruthy();
            expect(provision.quote?.trim()).toBeTruthy();
          });

          it("context has no interleave holes", () => {
            // Three-plus newlines mark the spot where the retired
            // standalone layout embedded the quote mid-prose.
            expect(provision.context ?? "").not.toMatch(/\n{3,}/);
          });

          it("prose fields end in complete sentences", () => {
            const prose: [string, string | undefined][] = [
              ["context", provision.context],
              ...provision.goals.map(
                (g, j) => [`goal ${j}`, g] as [string, string],
              ),
              ...provision.effects.map(
                (e, j) => [`effect ${j}`, e.text] as [string, string],
              ),
              ...provision.barriers.map(
                (b, j) => [`barrier ${j}`, b.text] as [string, string],
              ),
              ...provision.metrics.map(
                (m, j) => [`metric ${j}`, m.text] as [string, string],
              ),
              ...provision.metrics.map(
                (m, j) => [`metric ${j} rationale`, m.rationale] as [
                  string,
                  string | undefined,
                ],
              ),
            ];
            const incomplete = prose
              .filter(([, text]) => text !== undefined && text.trim() !== "")
              .filter(([, text]) => !COMPLETE.test((text as string).trim()))
              .map(([label, text]) => `${label}: …${(text as string).trim().slice(-60)}`);
            expect(incomplete).toEqual([]);
          });

          it("stances are well-formed when present", () => {
            for (const metric of provision.metrics) {
              for (const stance of metric.stances ?? []) {
                expect(STANCES.has(stance.stance)).toBe(true);
                expect(stance.goal).toBeGreaterThanOrEqual(0);
                expect(stance.goal).toBeLessThan(provision.goals.length);
              }
            }
          });
        });
      }
    });
  }
});
