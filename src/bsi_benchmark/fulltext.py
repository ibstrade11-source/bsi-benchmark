"""
Provider-agnostic full-text orchestration.

The benchmark never branches on provider/generator names.
Providers expose an optional fetch_fulltext(article) capability.
The orchestrator asks the selected provider for that capability.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FullTextResult:
    text: str | None
    source: str | None
    error: str | None = None


def attach_full_text(dataset, provider, required: bool = False):
    """
    Attach full text to every article using the selected provider's
    capability.

    No provider name is inspected here.
    """

    for article in dataset.articles:
        try:
            text = provider.fetch_fulltext(article)
        except Exception as exc:
            article.input_quality = dict(article.input_quality or {})
            article.input_quality["has_full_text"] = False
            article.input_quality["full_text_fetch_error"] = str(exc)

            if required:
                raise RuntimeError(
                    f"Full-text fetch failed for article "
                    f"{article.title!r}: {exc}"
                ) from exc

            continue

        if text and text.strip():
            article.full_text = text

            quality = dict(article.input_quality or {})
            quality["has_full_text"] = True
            quality["full_text_chars"] = len(text)
            quality["full_text_source"] = getattr(
                provider, "full_text_source", provider.__class__.__name__
            )
            article.input_quality = quality
        else:
            article.input_quality = dict(article.input_quality or {})
            article.input_quality["has_full_text"] = False

    return dataset
