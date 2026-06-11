"""Tests for paper content — TDD red-green cycle for paper revisions."""

import re
from functools import lru_cache
from pathlib import Path

PAPER = Path(__file__).parent.parent / "paper" / "index.qmd"
QUARTO_YML = Path(__file__).parent.parent / "paper" / "_quarto.yml"


@lru_cache(maxsize=1)
def _read_paper() -> str:
    return PAPER.read_text()


@lru_cache(maxsize=1)
def _read_quarto_yml() -> str:
    return QUARTO_YML.read_text()


# --- Task #7: Convergence reframe ---


def test_convergence_reframe_present():
    """Paper should reframe convergence as 'starts closer' or 'both conditions converge'."""
    text = _read_paper()
    assert re.search(
        r"both conditions converge|starts closer", text, re.IGNORECASE
    ), "Missing convergence reframe language"


# --- Task #8: Introduce brier properly ---


def test_introduce_brier_language():
    """Paper should say 'I introduce Brier' not 'I evaluate a specific framework called'."""
    text = _read_paper()
    assert re.search(r"I introduce \*{0,2}Brier", text), "Missing 'I introduce Brier'"
    assert (
        "I evaluate a specific framework called" not in text
    ), "Old framework intro language still present"


def test_brier_ai_footnote():
    """Paper should have a footnote referencing brier.institute."""
    text = _read_paper()
    assert "brier.institute" in text, "Missing brier.institute footnote"


# --- Task #9: Concrete example ---


def test_concrete_example_section():
    """Paper should contain a worked example using sunk_cost_project data."""
    text = _read_paper()
    assert re.search(
        r"sunk_cost_project|Worked example", text, re.IGNORECASE
    ), "Missing concrete worked example section"


# --- Task #10: Sycophancy data ---


def test_sycophancy_gpt_numbers():
    """Paper should report GPT sycophancy numbers: 466.7 naive, 108.3 brier."""
    text = _read_paper()
    assert "466.7" in text, "Missing GPT naive sycophancy mean (466.7)"
    assert "108.3" in text, "Missing GPT brier sycophancy mean (108.3)"


# --- Task #11: Technical fixes ---


def test_no_pre_registered():
    """Paper should not say 'pre-registered' — should say 'analysis code was committed'."""
    text = _read_paper()
    assert (
        "pre-registered" not in text and "pre-register" not in text
    ), "Paper still contains 'pre-registered' language"


def test_cot_caveat():
    """Paper should mention implicit chain-of-thought / implicit reasoning caveat."""
    text = _read_paper()
    assert re.search(
        r"implicit chain-of-thought|implicit reasoning", text, re.IGNORECASE
    ), "Missing CoT caveat about implicit reasoning"


# --- Referee review fixes ---


def test_conflict_of_interest_disclosed():
    """Paper should disclose author's conflict of interest."""
    text = _read_paper()
    assert re.search(
        r"[Dd]isclosure|conflict of interest", text
    ), "Missing conflict of interest disclosure"


def test_no_defensible_language():
    """Paper should not use evaluative 'defensible' for framework estimates."""
    text = _read_paper()
    assert (
        "more defensible" not in text
    ), "Evaluative 'more defensible' language still present"


def test_prompt_probe_confound_in_discussion():
    """Discussion should address prompt-probe alignment confound."""
    text = _read_paper()
    assert re.search(
        r"prompt-probe alignment", text
    ), "Missing prompt-probe alignment discussion in body"


def test_held_out_probe_result_present():
    """Paper should report that held-out / off-framework probes weaken or reverse the brier advantage."""
    text = _read_paper()
    assert re.search(
        r"off-framework|held-out probes", text, re.IGNORECASE
    ), "Missing held-out probe discussion"
    assert re.search(
        r"disappears and reverses|reverses", text, re.IGNORECASE
    ), "Missing statement that the held-out advantage reverses"


def test_relative_update_primary_metric():
    """Paper should say pooled inference uses relative update because scenarios mix units."""
    text = _read_paper()
    assert re.search(
        r"relative update.*primary|pooled inference uses \*relative update\*|mixes weeks, percentages, and leads",
        text,
        re.IGNORECASE | re.DOTALL,
    ), "Missing relative-update primary-metric explanation"


def test_no_preregistration_claims():
    """Paper should not claim preregistration."""
    text = _read_paper()
    assert "pre-registered" not in text.lower(), "Should not claim preregistration"
    assert "preregistered" not in text.lower(), "Should not claim preregistration"


# --- Symmetric sycophancy (directional asymmetry) ---


def test_symmetric_sycophancy_section():
    """Paper should report the downward sycophancy direction, not just upward."""
    text = _read_paper()
    assert re.search(
        r"direction-dependent|downward sycophancy|downward pressure", text, re.IGNORECASE
    ), "Missing symmetric/downward sycophancy analysis"


def test_symmetric_sycophancy_numbers():
    """Paper should report the downward-pressure capitulation magnitudes."""
    text = _read_paper()
    # Claude and GPT-5.4 both move ~650 leads downward; Brier on Claude ~495.
    assert "650" in text, "Missing downward sycophancy naive magnitude (650)"
    assert "643" in text, "Missing GPT-5.4 downward Brier magnitude (643)"


def test_sycophancy_direction_figure_referenced():
    """Paper should reference the directional-asymmetry figure."""
    text = _read_paper()
    assert "fig_sycophancy_direction.png" in text or "fig-sycophancy-direction" in text, (
        "Missing reference to the directional sycophancy figure"
    )


# --- Concrete raw excerpts ---


def test_raw_response_excerpts():
    """Worked example should include actual model response excerpts."""
    text = _read_paper()
    assert re.search(
        r"Raw response excerpts|response excerpts", text, re.IGNORECASE
    ), "Missing raw response excerpts subsection"
    # The Brier initial excerpt should name a reference class (Standish/CHAOS).
    assert "Standish" in text or "CHAOS" in text, (
        "Missing concrete reference-class excerpt from the Brier condition"
    )


# --- CI-rate moved to appendix ---


def test_ci_rate_in_appendix_not_primary_table():
    """The 100% CI-rate metric should live in an appendix, not the primary metrics."""
    text = _read_paper()
    assert re.search(
        r"Initial confidence-interval rate", text
    ), "Missing CI-rate appendix section"
    # The primary stability table should no longer carry an 'Initial CI rate' row.
    assert "| Initial CI rate |" not in text, (
        "Initial CI rate row still present in a primary table"
    )


# --- Scale-heterogeneity note ---


def test_scale_heterogeneity_note():
    """Paper should flag that raw-magnitude cross-model gaps are a units artifact."""
    text = _read_paper()
    assert re.search(
        r"scale-heterogeneity|units artifact", text, re.IGNORECASE
    ), "Missing scale-heterogeneity note"


# --- Transient API errors consolidated ---


def test_transient_api_errors_consolidated():
    """The phrase 'transient API errors' should appear at most once (Section 4.4)."""
    text = _read_paper()
    count = len(re.findall(r"transient API error", text))
    assert count <= 1, f"'transient API errors' mentioned {count} times; consolidate to one"


# --- Task #13: CSL config ---


def test_csl_config():
    """Quarto config should specify CSL citation style."""
    text = _read_quarto_yml()
    assert "csl:" in text, "Missing CSL config in _quarto.yml"
