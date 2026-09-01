"""
Token-budget-aware full-text compaction.

When ANY generator's request is rejected for being too large (HTTP 413,
or a rate_limit/tokens-per-minute error), the pipeline (see
comparison/runner.py) retries once with a much smaller version of the
same article's full text substituted in -- head + sampled middle + tail,
with long footnote/reference blocks stripped -- instead of the naive
head-truncated version normally used by generation/prompt.py.

This module only touches Article.full_text going INTO a prompt render.
It knows nothing about Groq, OpenRouter, or any other specific provider,
so the retry-with-compaction path in runner.py applies equally to
whichever --generators / --judge the user picked.
"""

import re


# Footnote/endnote lines in academic PDFs are typically: a bare number
# (the marker), then a long block of prose citing a source. Article body
# paragraphs don't start with a bare number, so this is a conservative,
# false-positive-resistant pattern -- it only strips lines that clearly
# look like footnotes, never ordinary body text.
_FOOTNOTE_LINE = re.compile(r"^\s*\d{1,3}\s+[A-Z].{40,}$", re.MULTILINE)

# Conservative default budget for the compacted fallback -- deliberately
# much smaller than generation/prompt.py's normal FULL_TEXT_CHAR_LIMIT
# (20,000), since the whole point of this path is recovering from a
# request that was already too large at that size. Tune per generator/
# model if needed; this is a starting value, not a measured optimum.
DEFAULT_COMPACT_CHAR_LIMIT = 6000


def strip_long_footnotes(text: str, min_len: int = 200) -> str:
    """
    Remove footnote/endnote-shaped lines (bare number + long prose) so a
    fixed character budget is spent on article body text rather than
    citation apparatus. Text with no such lines is returned unchanged.
    """
    if not text:
        return text
    kept = [
        line for line in text.split("\n")
        if not (_FOOTNOTE_LINE.match(line) and len(line) >= min_len)
    ]
    return "\n".join(kept)


def compact_full_text(
    full_text: str,
    budget_chars: int = DEFAULT_COMPACT_CHAR_LIMIT,
    head_ratio: float = 0.4,
    tail_ratio: float = 0.4,
) -> str:
    """
    Compact `full_text` to roughly `budget_chars` using a head/middle/
    tail sampling strategy instead of plain truncation:

    - head_ratio of the budget: the article's opening (abstract,
      introduction -- where core claims usually appear)
    - tail_ratio of the budget: the article's closing (conclusion,
      results -- where key findings usually appear)
    - the remainder: one evenly-centered slice from the middle

    Footnote-shaped lines are stripped first so the budget goes to body
    text. Never raises; a text already within budget is returned as-is
    (still footnote-stripped). Safe for any full_text/budget, including
    empty or very short input.
    """
    if not full_text:
        return full_text

    cleaned = strip_long_footnotes(full_text)

    if len(cleaned) <= budget_chars:
        return cleaned

    head_budget = int(budget_chars * head_ratio)
    tail_budget = int(budget_chars * tail_ratio)
    middle_budget = max(0, budget_chars - head_budget - tail_budget)

    head = cleaned[:head_budget]
    tail = cleaned[-tail_budget:] if tail_budget > 0 else ""

    middle_source = cleaned[head_budget: max(head_budget, len(cleaned) - tail_budget)]
    if middle_budget > 0 and len(middle_source) > middle_budget:
        mid_start = (len(middle_source) - middle_budget) // 2
        middle = middle_source[mid_start: mid_start + middle_budget]
    else:
        middle = middle_source[:middle_budget]

    parts = [head]
    if middle:
        parts.append(
            f"\n\n[... middle section condensed: {len(cleaned):,} original "
            f"chars reduced to fit a {budget_chars:,}-char budget ...]\n\n"
            + middle
        )
    if tail:
        parts.append(
            "\n\n[... skipping ahead to the article's closing section ...]\n\n"
            + tail
        )

    return "".join(parts)
