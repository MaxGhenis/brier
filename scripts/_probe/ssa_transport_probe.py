"""TEMPORARY: probe whether an Actions runner can read ssa.gov pages.

Compares plain urllib against headless Chromium (playwright). Prints status
codes and the <title> of each fetch. Removed before merge.
"""

import json
import sys
import urllib.request

URLS = [
    "https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-06/table01.html",
    "https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table04.html",
    "https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2026-06.html",
    "https://www.ssa.gov/appeals/DataSets/02_HO_Workload_Data.xml",
]

for url in URLS:
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            body = response.read()
            print(
                json.dumps(
                    {
                        "transport": "urllib",
                        "url": url,
                        "status": response.status,
                        "bytes": len(body),
                    }
                )
            )
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"transport": "urllib", "url": url, "error": str(exc)[:200]}))

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:
    print(json.dumps({"transport": "playwright", "error": f"import failed: {exc}"}))
    sys.exit(0)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    for url in URLS:
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            body = response.body() if response else b""
            title = page.title()
            headers = dict(response.headers) if response else {}
            print(
                json.dumps(
                    {
                        "transport": "playwright",
                        "url": url,
                        "status": response.status if response else None,
                        "bytes": len(body),
                        "title": title[:120],
                        "server": headers.get("server"),
                        "content_type": headers.get("content-type"),
                    }
                )
            )
        except Exception as exc:  # noqa: BLE001
            print(
                json.dumps(
                    {"transport": "playwright", "url": url, "error": str(exc)[:300]}
                )
            )
    browser.close()
