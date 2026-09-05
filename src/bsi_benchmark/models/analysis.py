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
    usage: dict | None = None         # provider-reported token usage, when
                                       # available (e.g. {"prompt_tokens": n,
                                       # "completion_tokens": n, "total_tokens":
                                       # n} from an OpenAI-compatible API).
                                       # Never fabricated: None when the
                                       # provider's response did not include
                                       # a usage object, per METHODOLOGY.md
                                       # section 63 ("no data may be
                                       # fabricated merely to complete a
                                       # result table"). Feeds Execution
                                       # Burden reporting (section 32).
    finish_reason: str | None = None  # provider-reported stop reason for
                                       # the FINAL API call that produced
                                       # `text` (e.g. "stop", "length").
                                       # "length" means the model's own
                                       # response hit the max_tokens cap --
                                       # the analysis may be an incomplete/
                                       # truncated artifact even though
                                       # generation itself did not error.
                                       # Never fabricated: None when the
                                       # provider's response did not report
                                       # one.
    continuation_rounds: int = 0      # how many extra "continue where you
                                       # left off" API calls were made and
                                       # concatenated onto `text` because
                                       # earlier calls hit finish_reason ==
                                       # "length" (see generation/groq.py,
                                       # generation/openrouter.py). 0 means
                                       # the analysis is exactly one API
                                       # call's output.
