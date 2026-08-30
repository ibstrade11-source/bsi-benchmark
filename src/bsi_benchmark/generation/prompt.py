"""
Prompt-template rendering for AnalysisGenerator.

Only the four supported article placeholders are substituted:
{title}, {abstract}, {doi}, and {full_text}.

Other braces are preserved verbatim. This is important for prompts
containing JSON schemas, LaTeX, scientific notation, or other content
with braces that are not template variables.
"""

import re


_ALLOWED = {
    "title",
    "abstract",
    "doi",
    "full_text",
}

# Character cap applied to {full_text} substitution only. Real full text
# from --fetch-full-text/--full-text-file can be 100k+ chars; sending all
# of it uncapped risks blowing a generator's context window or cost, and
# was observed in practice to make a 20B model on Groq punt on the rest
# of the (already long) BSI master prompt instructions rather than
# attempt the full analysis. This is a pragmatic safety cap, not a
# measurement of how much text a given model could actually handle --
# raise it if your generator/model can take more.
FULL_TEXT_CHAR_LIMIT = 20000


def render(prompt_template: str, article) -> str:
    """Render supported article placeholders while preserving other braces."""

    full_text = getattr(article, "full_text", None) or ""
    original_len = len(full_text)
    if original_len > FULL_TEXT_CHAR_LIMIT:
        full_text = (
            full_text[:FULL_TEXT_CHAR_LIMIT]
            + f"\n\n[... full text truncated at {FULL_TEXT_CHAR_LIMIT:,} of "
              f"{original_len:,} characters to fit the generator's context "
              "budget ...]"
        )

    values = {
        "title": article.title or "",
        "abstract": article.abstract or "",
        "doi": article.doi or "",
        "full_text": full_text,
    }

    pattern = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

    def replace(match):
        key = match.group(1)
        if key in _ALLOWED:
            return values[key]
        return match.group(0)

    return pattern.sub(replace, prompt_template)
