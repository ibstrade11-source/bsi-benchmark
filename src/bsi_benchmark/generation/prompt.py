"""
Prompt-template rendering for AnalysisGenerator.

Kept deliberately trivial (str.format under the hood) rather than pulling
in a templating engine dependency -- the placeholder set is small and
fixed.
"""


def render(prompt_template: str, article) -> str:
    return prompt_template.format(
        title=article.title or "",
        abstract=article.abstract or "",
        doi=article.doi or "",
    )
