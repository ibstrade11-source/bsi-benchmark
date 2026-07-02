"""
Model for a BSI-generated analysis of an article.

This benchmark runner has no model access of its own (no network / API
key), so `text` is expected to be produced elsewhere (e.g. a real BSI run
in Termux or claude.ai) and supplied to the benchmark as input, alongside
the raw `Article` it was generated from. See datasets/analyzed_dataset.py
for the paired container and its JSON schema.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Analysis:
    text: str
    source_model: str | None = None   # e.g. "claude-sonnet-5", "bsi-v3.4.2"
    generated_at: str | None = None   # ISO 8601 timestamp, caller-supplied
