"""
Scientific article model.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Article:
    title: str
    abstract: str | None
    full_text: str | None = None
    doi: str | None = None
    url: str | None = None
    input_quality: dict | None = None
