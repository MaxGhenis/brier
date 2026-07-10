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
  },
});
