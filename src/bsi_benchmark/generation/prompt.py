"""
Prompt-template rendering for AnalysisGenerator.

Only the three supported article placeholders are substituted:
{title}, {abstract}, and {doi}.

Other braces are preserved verbatim. This is important for prompts
containing JSON schemas, LaTeX, scientific notation, or other content
with braces that are not template variables.
"""

import re


_ALLOWED = {
    "title",
    "abstract",
    "doi",
}


def render(prompt_template: str, article) -> str:
    """Render supported article placeholders while preserving other braces."""

    values = {
        "title": article.title or "",
        "abstract": article.abstract or "",
        "doi": article.doi or "",
    }

    pattern = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

    def replace(match):
        key = match.group(1)
        if key in _ALLOWED:
            return values[key]
        return match.group(0)

    return pattern.sub(replace, prompt_template)
