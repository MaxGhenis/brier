import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/test-setup.ts",
    // Full-catalog integrity sweeps (stringify/project every cell) are
    // data-volume-bound, not latency tests; CI's shared runners in the
    // publish job miss the 5s default on cold caches.
    testTimeout: 30_000,
    // Suites that assert over the whole catalog build their projections
    // once in beforeAll rather than per test. That work is the same total
    // volume, just hoisted, so the hook needs the same budget as a test --
    // the 10s hook default would fail the setup instead of the assertions.
    hookTimeout: 60_000,
  },
});
