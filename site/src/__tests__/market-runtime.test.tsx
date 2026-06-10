import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, render, screen } from "@testing-library/react";
import { MarketRuntime, STREAM_WATCHDOG_MS } from "@/components/MarketRuntime";
import { LIVE_FORECAST_SLUGS, MARKETS } from "@/data/markets";

type Listener = (event: MessageEvent) => void;

class FakeEventSource {
  static instances: FakeEventSource[] = [];
  static CONNECTING = 0;
  static OPEN = 1;
  static CLOSED = 2;
  url: string;
  closed = false;
  onerror: (() => void) | null = null;
  onopen: (() => void) | null = null;
  private listeners = new Map<string, Listener[]>();

  constructor(url: string) {
    this.url = url;
    FakeEventSource.instances.push(this);
  }

  addEventListener(type: string, listener: Listener) {
    this.listeners.set(type, [...(this.listeners.get(type) ?? []), listener]);
  }

  close() {
    this.closed = true;
  }

  emit(type: string, data: unknown) {
    for (const listener of this.listeners.get(type) ?? []) {
      listener({ data: JSON.stringify(data) } as MessageEvent);
    }
  }
}

const liveMarket = MARKETS.find((m) => LIVE_FORECAST_SLUGS.has(m.slug))!;

describe("MarketRuntime stream watchdog", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal("EventSource", FakeEventSource);
    FakeEventSource.instances = [];
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.useRealTimers();
  });

  it("falls back to the static trace when the stream stays silent", () => {
    render(<MarketRuntime market={liveMarket} />);
    expect(FakeEventSource.instances).toHaveLength(1);

    act(() => {
      vi.advanceTimersByTime(STREAM_WATCHDOG_MS + 50);
    });

    expect(FakeEventSource.instances[0].closed).toBe(true);
    expect(screen.getByText(/replaying the static mock trace/i)).toBeTruthy();
  });

  it("keeps the live stream once events arrive", () => {
    render(<MarketRuntime market={liveMarket} />);

    act(() => {
      FakeEventSource.instances[0].emit("step", {
        kind: "heading",
        text: "Identifying the question",
      });
    });
    act(() => {
      vi.advanceTimersByTime(STREAM_WATCHDOG_MS + 50);
    });

    expect(FakeEventSource.instances[0].closed).toBe(false);
    expect(screen.getByText("Identifying the question")).toBeTruthy();
  });

  it("still falls back immediately on connection errors", () => {
    render(<MarketRuntime market={liveMarket} />);

    act(() => {
      FakeEventSource.instances[0].onerror?.();
    });

    expect(FakeEventSource.instances[0].closed).toBe(true);
    expect(screen.getByText(/replaying the static mock trace/i)).toBeTruthy();
  });
});
