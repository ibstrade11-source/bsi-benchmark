"""
Tests for prompt_loader.load_bsi_prompt.

Covers the three cases that matter for the permanent-fix behavior:
1. A raw master prompt with no placeholders -> auto-appended.
2. A prompt that already has both placeholders -> untouched.
3. A prompt with only one of the two placeholders -> raises ValueError
   instead of silently guessing.
"""
import pytest

from bsi_benchmark.prompt_loader import load_bsi_prompt


def test_raw_prompt_without_placeholders_gets_appended(tmp_path):
    p = tmp_path / "MASTER_PROMPT_BSI_v3.4.2.md"
    p.write_text(
        "You are the Behmanesh Structural Index evaluator...\n"
        "Follow Manifest/Latent/Meta layers.\n",
        encoding="utf-8",
    )

    result = load_bsi_prompt(str(p))

    assert "{title}" in result
    assert "{abstract}" in result
    # original content preserved verbatim, block only appended
    assert result.startswith("You are the Behmanesh Structural Index evaluator...")
    # file on disk untouched
    assert "{title}" not in p.read_text(encoding="utf-8")


def test_prompt_with_both_placeholders_is_unchanged(tmp_path):
    p = tmp_path / "already_templated.md"
    original = "Analyze.\nTitle: {title}\nAbstract: {abstract}\n"
    p.write_text(original, encoding="utf-8")

    result = load_bsi_prompt(str(p))

    assert result == original


def test_prompt_with_only_title_placeholder_raises(tmp_path):
    p = tmp_path / "half_templated.md"
    p.write_text("Title: {title}\nAbstract: TODO\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_bsi_prompt(str(p))


def test_prompt_with_only_abstract_placeholder_raises(tmp_path):
    p = tmp_path / "half_templated2.md"
    p.write_text("Title: TODO\nAbstract: {abstract}\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_bsi_prompt(str(p))


def test_result_formats_cleanly_with_real_article_data():
    """The whole point: format() must succeed after loading a raw prompt."""
    import tempfile
    import os

    fd, path = tempfile.mkstemp(suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("Raw BSI master prompt with no placeholders.\n")

        template = load_bsi_prompt(path)
        formatted = template.format(
            title="Sample Paper", abstract="Sample abstract text."
        )
        assert "Sample Paper" in formatted
        assert "Sample abstract text." in formatted
    finally:
        os.remove(path)
