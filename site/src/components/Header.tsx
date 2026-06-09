import Link from "next/link";
import { BrierLogoMark } from "./BrierLogo";

export function Header({
  activePage,
}: {
  activePage?: "paper" | "forecasts" | "about";
}) {
  return (
    <header
      className="sticky top-0 z-100 w-full backdrop-blur-[16px] border-b"
      style={{
        backgroundColor: "var(--theme-header-bg)",
        borderColor: "var(--theme-border)",
      }}
    >
      <div className="w-full max-w-[1200px] mx-auto px-8 py-4 flex items-center justify-between max-md:px-4 max-md:py-3">
        <div className="flex items-center gap-3 min-w-0">
          <Link
            href="/"
            className="flex items-center gap-[0.35em] no-underline [font-family:var(--font-display)] text-[1.1rem] font-semibold hover:no-underline tracking-[-0.01em]"
            style={{ color: "var(--theme-text)" }}
          >
            <BrierLogoMark size={26} />
            <span>thesis</span>
          </Link>
          <span
            className="inline-flex h-6 items-center rounded-md border border-[#DFA85A] bg-[#FFF5E6] px-2 [font-family:var(--font-mono)] text-[0.62rem] font-medium uppercase tracking-[0.08em] text-[#7A4B12] max-[380px]:hidden"
            aria-label="Prototype build"
          >
            Prototype
          </span>
        </div>
        <nav className="flex gap-7 items-center max-md:gap-4">
          <Link
            href="/forecasts"
            className={`[font-family:var(--font-body)] text-[0.82rem] font-normal no-underline transition-colors duration-200 hover:no-underline ${
              activePage === "forecasts"
                ? "text-[#A94E80]"
                : "text-[var(--theme-text-muted)]"
            }`}
            style={
              activePage !== "forecasts"
                ? { color: "var(--theme-text-muted)" }
                : undefined
            }
          >
            Forecasts
          </Link>
          <Link
            href="/about"
            className={`[font-family:var(--font-body)] text-[0.82rem] font-normal no-underline transition-colors duration-200 hover:no-underline max-md:hidden ${
              activePage === "about"
                ? "text-[#A94E80]"
                : "text-[var(--theme-text-muted)]"
            }`}
            style={
              activePage !== "about"
                ? { color: "var(--theme-text-muted)" }
                : undefined
            }
          >
            About
          </Link>
          <a
            href="https://github.com/MaxGhenis/brier"
            className="no-underline transition-colors duration-200 hover:no-underline"
            style={{ color: "var(--theme-text-muted)" }}
            aria-label="GitHub"
          >
            <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
            </svg>
          </a>
        </nav>
      </div>
    </header>
  );
}
