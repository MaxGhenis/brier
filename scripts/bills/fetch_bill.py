"""Fetch federal bill text into bills/raw/ — the ingest pipeline's mouth.

Three resolution paths, tried in order:

1. Axiom Supabase (TheAxiomFoundation/axiom-bills): the hosted store the
   hourly refresh-federal-bills workflow keeps current. Holds one
   preferred latest-stage text per bill with source_url + sha256
   provenance. Requires AXIOM_SUPABASE_ANON_KEY (the public anon key
   from the axiom-bills web app).
2. Congress.gov API: direct fetch when the bill is missing from the
   axiom store (or the store is unreachable). Requires CONGRESS_API_KEY
   (free key: https://api.congress.gov/sign-up/).
3. --url mode: any direct PDF/HTML/text URL — committee discussion
   drafts (e.g. Farm Bill 2.0) live on committee sites, not
   congress.gov, so this path skips resolution entirely.

Every fetch writes three artifacts under bills/raw/:
  <slug>.txt        flat text (the contract surface for ingest)
  <slug>.meta.json  provenance: source path, URL, version, sha256, times
  <slug>.<ext>      original document bytes (xml/html/pdf) when
                    available, so title-scoped chunking can use document
                    structure instead of re-deriving it from flat text

Version selection, format normalization, and text extraction are adapted
from TheAxiomFoundation/axiom-bills (packages/scrapers), which learned
the sharp edges first: stage-ranked version picking (alphabetical label
sort chose bill text by spelling luck) and Congress.gov rate budgeting.

Usage:
  uv run --extra bills scripts/bills/fetch_bill.py 119/hr/818
  uv run --extra bills scripts/bills/fetch_bill.py \
      https://www.congress.gov/bill/119th-congress/house-bill/818
  uv run --extra bills scripts/bills/fetch_bill.py \
      --url https://agriculture.house.gov/uploadedfiles/farm_bill.pdf \
      --slug farm-bill-2-0
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "bills" / "raw"

AXIOM_SUPABASE_URL = os.environ.get(
    "AXIOM_SUPABASE_URL", "https://tgohtgoqkjyrvwbvsspx.supabase.co"
)
AXIOM_ANON_KEY = os.environ.get("AXIOM_SUPABASE_ANON_KEY")
CONGRESS_API_KEY = os.environ.get("CONGRESS_API_KEY")
CONGRESS_API_ROOT = "https://api.congress.gov/v3"

# 'hr' + '818' → the display number the axiom store indexes by.
TYPE_DISPLAY = {
    "hr": "H.R.", "s": "S.",
    "hjres": "H.J.Res.", "sjres": "S.J.Res.",
    "hconres": "H.Con.Res.", "sconres": "S.Con.Res.",
    "hres": "H.Res.", "sres": "S.Res.",
}

# congress.gov bill-page URL path segment → type code.
URL_SLUG_TYPE = {
    "house-bill": "hr", "senate-bill": "s",
    "house-joint-resolution": "hjres", "senate-joint-resolution": "sjres",
    "house-concurrent-resolution": "hconres",
    "senate-concurrent-resolution": "sconres",
    "house-resolution": "hres", "senate-resolution": "sres",
}

# Later legislative stage beats earlier; unknown labels floor at 0.
_STAGE_KEYWORDS = [
    ("public law", 90), ("enacted", 85), ("enrolled", 80),
    ("engrossed", 60), ("passed", 55), ("reported", 40),
    ("placed on calendar", 30), ("amended", 25), ("referred", 20),
    ("introduced", 10),
]

_FORMAT_PREF = {"xml": 0, "html": 1, "txt": 2, "pdf": 3}


def stage_rank(label: str | None) -> int:
    if not label:
        return 0
    # Labels arrive both spaced ("Enrolled Bill") and slugified
    # ("enrolled-bill-html") — normalize separators before matching.
    lowered = label.lower().replace("-", " ").replace("_", " ")
    return max((r for k, r in _STAGE_KEYWORDS if k in lowered), default=0)


def normalize_format(raw: str) -> str:
    lower = (raw or "").strip().lower()
    if lower in ("formatted text", "html", "htm"):
        return "html"
    if lower in ("formatted xml", "xml", "united states legislative markup"):
        return "xml"
    if lower == "pdf":
        return "pdf"
    if lower in ("text", "txt", "plain text"):
        return "txt"
    return lower or "unknown"


def strip_line_gutters(text: str) -> str:
    """Drop the per-line number gutter congressional PDFs print (1–25).

    Only fires when a page's worth of lines actually start with small
    ascending integers, so ordinary numbers at line starts survive.
    """
    lines = text.splitlines()
    numbered = sum(
        1 for line in lines if re.match(r"^\s*([1-9]|1\d|2[0-5])\s+\S", line)
    )
    if not lines or numbered / len(lines) < 0.4:
        return text
    return "\n".join(
        re.sub(r"^\s*([1-9]|1\d|2[0-5])\s+", "", line) for line in lines
    )


def to_text(format_: str, body: bytes) -> str | None:
    fmt = normalize_format(format_)
    if fmt in ("html", "xml"):
        from selectolax.parser import HTMLParser

        try:
            tree = HTMLParser(body.decode("utf-8", errors="replace"))
        except Exception:
            return None
        text = tree.text(separator=" ").strip()
        return text or None
    if fmt == "txt":
        return body.decode("utf-8", errors="replace")
    if fmt == "pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(body))
            pages = [page.extract_text() or "" for page in reader.pages]
        except Exception:
            # Encrypted/corrupt/scanned-image PDFs — nothing to extract.
            return None
        text = "\n".join(pages).strip()
        if not text:
            return None
        return strip_line_gutters(text)
    return None


def parse_bill_ref(arg: str) -> tuple[int, str, int] | None:
    """'119/hr/818' or a congress.gov bill URL → (congress, type, number)."""
    m = re.fullmatch(r"(\d{2,3})/([a-z]+)/(\d+)", arg.strip().lower())
    if m and m.group(2) in TYPE_DISPLAY:
        return int(m.group(1)), m.group(2), int(m.group(3))
    m = re.search(
        r"congress\.gov/bill/(\d{2,3})\w*-congress/([a-z-]+)/(\d+)",
        arg.strip().lower(),
    )
    if m and m.group(2) in URL_SLUG_TYPE:
        return int(m.group(1)), URL_SLUG_TYPE[m.group(2)], int(m.group(3))
    return None


def fetch_from_axiom(
    client: httpx.Client, congress: int, bill_type: str, number: int
) -> dict | None:
    """Read the best stored text for a bill from the axiom Supabase."""
    if not AXIOM_ANON_KEY:
        print("  axiom: AXIOM_SUPABASE_ANON_KEY not set, skipping", file=sys.stderr)
        return None
    headers = {
        "apikey": AXIOM_ANON_KEY,
        "Authorization": f"Bearer {AXIOM_ANON_KEY}",
        "Accept-Profile": "bills",
    }
    display = f"{TYPE_DISPLAY[bill_type]}{number}"
    try:
        resp = client.get(
            f"{AXIOM_SUPABASE_URL}/rest/v1/bills",
            params={
                "jurisdiction": "eq.us",
                "number": f"eq.{display}",
                # Congress disambiguation lives on the sessions table
                # (bill numbers repeat across Congresses).
                "sessions.name": f"eq.{congress}th Congress",
                "select": "id,number,title,source_url,sessions!inner(name)",
            },
            headers=headers,
        )
        resp.raise_for_status()
        bills = resp.json()
        if not bills:
            print(f"  axiom: {display} not in store", file=sys.stderr)
            return None
        bill = bills[0]
        resp = client.get(
            f"{AXIOM_SUPABASE_URL}/rest/v1/bill_texts",
            params={
                "bill_id": f"eq.{bill['id']}",
                "select": "version_label,format,text,text_sha256,source_url,fetched_at",
            },
            headers=headers,
        )
        resp.raise_for_status()
        texts = resp.json()
    except httpx.HTTPError as exc:
        print(f"  axiom: request failed ({exc}), falling back", file=sys.stderr)
        return None
    if not texts:
        print(f"  axiom: {display} has no stored text", file=sys.stderr)
        return None
    best = min(
        texts,
        key=lambda t: (
            -stage_rank(t["version_label"]),
            _FORMAT_PREF.get(normalize_format(t["format"]), 9),
        ),
    )
    return {
        "resolved_via": "axiom-supabase",
        "title": bill.get("title"),
        "bill_number": bill["number"],
        "text": best["text"],
        "version_label": best["version_label"],
        "format": normalize_format(best["format"]),
        "source_url": best["source_url"],
        "source_fetched_at": best["fetched_at"],
        "text_sha256": best["text_sha256"],
        "source_bytes": None,  # axiom stores extracted text, not the doc
    }


def fetch_from_congress_api(
    client: httpx.Client, congress: int, bill_type: str, number: int
) -> dict | None:
    """Resolve text versions via the Congress.gov API and download the best."""
    if not CONGRESS_API_KEY:
        print("  congress.gov: CONGRESS_API_KEY not set, skipping", file=sys.stderr)
        return None
    params = {"api_key": CONGRESS_API_KEY, "format": "json"}
    base = f"{CONGRESS_API_ROOT}/bill/{congress}/{bill_type}/{number}"
    try:
        detail = client.get(base, params=params)
        detail.raise_for_status()
        title = detail.json().get("bill", {}).get("title")
        resp = client.get(f"{base}/text", params=params)
        resp.raise_for_status()
        versions = resp.json().get("textVersions", [])
    except httpx.HTTPError as exc:
        print(f"  congress.gov: request failed ({exc})", file=sys.stderr)
        return None
    candidates = [
        {
            "label": (v.get("type") or "Unknown").strip(),
            "format": normalize_format(f.get("type", "")),
            "url": f["url"],
        }
        for v in versions
        for f in v.get("formats", [])
        if f.get("url")
    ]
    candidates = [c for c in candidates if c["format"] in _FORMAT_PREF]
    if not candidates:
        print(f"  congress.gov: no fetchable text versions", file=sys.stderr)
        return None
    best = min(
        candidates,
        key=lambda c: (-stage_rank(c["label"]), _FORMAT_PREF[c["format"]]),
    )
    try:
        doc = client.get(best["url"])
        doc.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"  congress.gov: download failed ({exc})", file=sys.stderr)
        return None
    text = to_text(best["format"], doc.content)
    if not text:
        print(f"  congress.gov: text extraction failed", file=sys.stderr)
        return None
    return {
        "resolved_via": "congress.gov-api",
        "title": title,
        "bill_number": f"{TYPE_DISPLAY[bill_type]}{number}",
        "text": text,
        "version_label": best["label"],
        "format": best["format"],
        "source_url": best["url"],
        "source_fetched_at": None,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "source_bytes": doc.content,
    }


def fetch_from_url(client: httpx.Client, url: str) -> dict | None:
    """Direct fetch of an arbitrary document URL (committee drafts etc.)."""
    try:
        resp = client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"  url: download failed ({exc})", file=sys.stderr)
        return None
    content_type = resp.headers.get("content-type", "").lower()
    if "pdf" in content_type or url.lower().endswith(".pdf"):
        fmt = "pdf"
    elif "xml" in content_type or url.lower().endswith(".xml"):
        fmt = "xml"
    elif "html" in content_type or url.lower().endswith((".htm", ".html")):
        fmt = "html"
    else:
        fmt = "txt"
    text = to_text(fmt, resp.content)
    if not text:
        print(
            "  url: no text extracted (scanned/encrypted PDF? OCR is out of "
            "scope — fail loudly rather than analyze nothing)",
            file=sys.stderr,
        )
        return None
    return {
        "resolved_via": "direct-url",
        "title": None,
        "bill_number": None,
        "text": text,
        "version_label": None,
        "format": fmt,
        "source_url": url,
        "source_fetched_at": None,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "source_bytes": resp.content,
    }


def write_artifacts(slug: str, result: dict) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    txt_path = RAW_DIR / f"{slug}.txt"
    txt_path.write_text(result["text"], encoding="utf-8")
    doc_path = None
    if result["source_bytes"] and result["format"] in ("xml", "html", "pdf"):
        doc_path = RAW_DIR / f"{slug}.{result['format']}"
        doc_path.write_bytes(result["source_bytes"])
    meta = {
        "slug": slug,
        "bill_number": result["bill_number"],
        "title": result["title"],
        "resolved_via": result["resolved_via"],
        "source_url": result["source_url"],
        "version_label": result["version_label"],
        "format": result["format"],
        "text_sha256": result["text_sha256"],
        "source_fetched_at": result["source_fetched_at"],
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "text_file": txt_path.name,
        "source_file": doc_path.name if doc_path else None,
    }
    (RAW_DIR / f"{slug}.meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    return txt_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "ref",
        nargs="?",
        help="Bill reference: '119/hr/818' or a congress.gov bill URL",
    )
    parser.add_argument("--url", help="Direct document URL (committee PDFs etc.)")
    parser.add_argument("--slug", help="Artifact slug (default: hr818-119)")
    parser.add_argument(
        "--force", action="store_true", help="Refetch even if cached"
    )
    args = parser.parse_args()

    if not args.ref and not args.url:
        parser.error("give a bill reference or --url")
    if args.url and not args.slug:
        parser.error("--url mode requires --slug")

    with httpx.Client(
        timeout=60, follow_redirects=True, headers={"User-Agent": "thesis-bills/0.1"}
    ) as client:
        if args.url:
            slug = args.slug
            if (RAW_DIR / f"{slug}.txt").exists() and not args.force:
                print(f"cached: bills/raw/{slug}.txt (--force to refetch)")
                return 0
            result = fetch_from_url(client, args.url)
        else:
            ref = parse_bill_ref(args.ref)
            if not ref:
                parser.error(f"could not parse bill reference: {args.ref!r}")
            congress, bill_type, number = ref
            slug = args.slug or f"{bill_type}{number}-{congress}"
            if (RAW_DIR / f"{slug}.txt").exists() and not args.force:
                print(f"cached: bills/raw/{slug}.txt (--force to refetch)")
                return 0
            result = fetch_from_axiom(client, congress, bill_type, number)
            if result is None:
                result = fetch_from_congress_api(client, congress, bill_type, number)

    if result is None:
        print(f"error: could not resolve bill text for {args.ref or args.url}",
              file=sys.stderr)
        return 1
    txt_path = write_artifacts(slug, result)
    rel = txt_path.relative_to(REPO_ROOT)
    print(
        f"wrote {rel} ({len(result['text']):,} chars, "
        f"{result['version_label'] or 'unversioned'}, via {result['resolved_via']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
