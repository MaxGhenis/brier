"""Unit tests for scripts/bills/fetch_bill.py (the bill-ingestion mouth).

Covers the pure resolution/extraction logic; network paths are exercised
by hand (they hit the axiom Supabase store and Congress.gov).
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("httpx", reason="bills extra not installed")

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bills" / "fetch_bill.py"
_spec = importlib.util.spec_from_file_location("fetch_bill", _SCRIPT)
fetch_bill = importlib.util.module_from_spec(_spec)
sys.modules["fetch_bill"] = fetch_bill
_spec.loader.exec_module(fetch_bill)


class TestParseBillRef:
    def test_short_form(self):
        assert fetch_bill.parse_bill_ref("119/hr/818") == (119, "hr", 818)

    def test_short_form_joint_resolution(self):
        assert fetch_bill.parse_bill_ref("119/sjres/12") == (119, "sjres", 12)

    def test_congress_gov_url(self):
        url = "https://www.congress.gov/bill/119th-congress/senate-bill/3596"
        assert fetch_bill.parse_bill_ref(url) == (119, "s", 3596)

    def test_congress_gov_url_with_trailing_path(self):
        url = "https://www.congress.gov/bill/119th-congress/house-bill/818/text"
        assert fetch_bill.parse_bill_ref(url) == (119, "hr", 818)

    def test_unknown_bill_type_rejected(self):
        assert fetch_bill.parse_bill_ref("119/xx/1") is None

    def test_garbage_rejected(self):
        assert fetch_bill.parse_bill_ref("not a bill") is None


class TestStageRank:
    def test_later_stages_beat_earlier(self):
        ranks = [
            fetch_bill.stage_rank(label)
            for label in (
                "introduced-in-senate",
                "reported-to-senate",
                "engrossed-in-house",
                "enrolled-bill",
                "public-law",
            )
        ]
        assert ranks == sorted(ranks)
        assert len(set(ranks)) == len(ranks)

    def test_unknown_label_floors_at_zero(self):
        assert fetch_bill.stage_rank("mystery-version") == 0
        assert fetch_bill.stage_rank(None) == 0


class TestNormalizeFormat:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("Formatted Text", "html"),
            ("Formatted XML", "xml"),
            ("United States Legislative Markup", "xml"),
            ("PDF", "pdf"),
            ("Plain Text", "txt"),
            ("", "unknown"),
        ],
    )
    def test_congress_gov_labels(self, raw, expected):
        assert fetch_bill.normalize_format(raw) == expected


class TestStripLineGutters:
    def test_strips_gutter_heavy_text(self):
        text = "\n".join(f"{i} SECTION {i} words here" for i in range(1, 11))
        stripped = fetch_bill.strip_line_gutters(text)
        assert stripped.splitlines()[0] == "SECTION 1 words here"

    def test_leaves_normal_text_alone(self):
        text = "SECTION 1. SHORT TITLE.\nThis Act may be cited as follows.\n" * 10
        assert fetch_bill.strip_line_gutters(text) == text


class TestToText:
    def test_html_strips_tags(self):
        body = b"<html><body><h1>S. 3596</h1><p>A BILL</p></body></html>"
        text = fetch_bill.to_text("html", body)
        assert "S. 3596" in text and "A BILL" in text
        assert "<h1>" not in text

    def test_txt_passthrough(self):
        assert fetch_bill.to_text("txt", b"hello bill") == "hello bill"

    def test_corrupt_pdf_returns_none(self):
        assert fetch_bill.to_text("pdf", b"not a pdf at all") is None

    def test_unknown_format_returns_none(self):
        assert fetch_bill.to_text("docx", b"whatever") is None


class TestSlugContainment:
    @pytest.mark.parametrize(
        "slug",
        ["../escaped", "/etc/passwd", "a/b", "..", ".hidden", "UPPER", "", "a_b"],
    )
    def test_hostile_slugs_rejected(self, slug):
        with pytest.raises(SystemExit):
            fetch_bill.validate_slug(slug)

    @pytest.mark.parametrize("slug", ["hr818-119", "farm-bill-2-0", "s3596-119"])
    def test_real_slugs_accepted(self, slug):
        assert fetch_bill.validate_slug(slug) == slug

    def test_write_refuses_traversal_slug(self, tmp_path, monkeypatch):
        monkeypatch.setattr(fetch_bill, "RAW_DIR", tmp_path)
        result = {
            "resolved_via": "direct-url", "title": None, "bill_number": None,
            "text": "x", "version_label": None, "format": "txt",
            "source_url": "https://example.gov", "source_fetched_at": None,
            "text_sha256": "s", "source_bytes": None,
        }
        with pytest.raises(SystemExit):
            fetch_bill.write_artifacts("../escaped", result)
        assert not (tmp_path.parent / "escaped.txt").exists()

    def test_write_refuses_symlink_destination(self, tmp_path, monkeypatch):
        raw = tmp_path / "raw"
        raw.mkdir()
        outside = tmp_path / "outside.txt"
        outside.write_text("original")
        (raw / "sneaky.txt").symlink_to(outside)
        monkeypatch.setattr(fetch_bill, "RAW_DIR", raw)
        result = {
            "resolved_via": "direct-url", "title": None, "bill_number": None,
            "text": "overwritten", "version_label": None, "format": "txt",
            "source_url": "https://example.gov", "source_fetched_at": None,
            "text_sha256": "s", "source_bytes": None,
        }
        with pytest.raises(SystemExit):
            fetch_bill.write_artifacts("sneaky", result)
        assert outside.read_text() == "original"


class TestAxiomBackfill:
    def test_command_targets_axiom_bills_workflow(self):
        cmd = fetch_bill.backfill_command(119, "s", 3596)
        assert cmd[:3] == ["gh", "workflow", "run"]
        assert "TheAxiomFoundation/axiom-bills" in cmd
        assert "bills=s/3596" in cmd
        assert "congress=119" in cmd

    def test_trigger_reports_success(self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            fetch_bill.subprocess,
            "run",
            lambda cmd, **kw: calls.append(cmd),
        )
        assert fetch_bill.trigger_axiom_backfill(119, "hr", 818) is True
        assert calls and "bills=hr/818" in calls[0]

    def test_trigger_swallows_dispatch_failure(self, monkeypatch):
        def boom(cmd, **kw):
            raise RuntimeError("gh not authenticated")

        monkeypatch.setattr(fetch_bill.subprocess, "run", boom)
        assert fetch_bill.trigger_axiom_backfill(119, "hr", 818) is False


class TestWriteArtifacts:
    def test_writes_text_meta_and_source_doc(self, tmp_path, monkeypatch):
        monkeypatch.setattr(fetch_bill, "RAW_DIR", tmp_path)
        result = {
            "resolved_via": "direct-url",
            "title": "Test Bill",
            "bill_number": "S.3596",
            "text": "A BILL to test artifact writing.",
            "version_label": "introduced-in-senate",
            "format": "html",
            "source_url": "https://example.gov/bill.htm",
            "source_fetched_at": None,
            "text_sha256": "abc123",
            "source_bytes": b"<html>doc</html>",
        }
        txt_path = fetch_bill.write_artifacts("s3596-119", result)

        assert txt_path.read_text() == "A BILL to test artifact writing."
        assert (tmp_path / "s3596-119.html").read_bytes() == b"<html>doc</html>"
        meta = json.loads((tmp_path / "s3596-119.meta.json").read_text())
        assert meta["slug"] == "s3596-119"
        assert meta["source_url"] == "https://example.gov/bill.htm"
        assert meta["text_sha256"] == "abc123"
        assert meta["source_file"] == "s3596-119.html"
        assert meta["retrieved_at"]

    def test_no_source_doc_when_bytes_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(fetch_bill, "RAW_DIR", tmp_path)
        result = {
            "resolved_via": "axiom-supabase",
            "title": None,
            "bill_number": "H.R.818",
            "text": "text only",
            "version_label": "enrolled-bill",
            "format": "html",
            "source_url": "https://example.gov/x.htm",
            "source_fetched_at": "2026-07-17T00:00:00+00:00",
            "text_sha256": "def456",
            "source_bytes": None,
        }
        fetch_bill.write_artifacts("hr818-119", result)
        meta = json.loads((tmp_path / "hr818-119.meta.json").read_text())
        assert meta["source_file"] is None
        assert not (tmp_path / "hr818-119.html").exists()
