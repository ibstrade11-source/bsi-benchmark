"""
Checkpoint/resume support for `bsi-benchmark compare`.

A benchmark run over many articles and generators can be interrupted
(network drop, Termux killed in background, rate limits, judge model
outage) partway through. Without checkpointing, a re-run would either
lose already-generated analyses (wasting the API calls that produced
them) or silently re-judge cells that already produced a valid,
independent judge result.

This module persists per-cell state to `<output>.checkpoint.json` as
the run progresses, so that re-running the *same* `compare` command
(same --output) resumes rather than restarts:

- A cell whose analysis was generated is never regenerated, even if
  judging for that cell failed or never ran.
- A cell whose judge result is missing, errored, or fell back to the
  keyword heuristic is retried; a successful retry overwrites the
  invalid entry.
- A cell whose judge result already came from a real LLM judge
  (criteria_source == "llm", no error) is left untouched.

Two independent *valid* runs are never silently merged into one: use
--fresh to start a new checkpoint. If a prior checkpoint (and its
report) already exist, --fresh archives them with a timestamp suffix
before starting over, so both results stay on disk rather than one
overwriting the other.

Article identity: articles have no stable ID field of their own, so a
DOI is used when present, otherwise a hash of title+abstract. This
degrades gracefully if a provider's result set changes between runs
(unmatched old entries just sit unused; new articles get fresh cache
entries) rather than corrupting anything.
"""

import hashlib
import json
import os
import shutil
import time
from dataclasses import asdict

from bsi_benchmark.models.analysis import Analysis


def article_key(article) -> str:
    if getattr(article, "doi", None):
        return f"doi:{article.doi}"
    basis = (article.title or "") + "|" + (article.abstract or "")
    return "hash:" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def cell_key(art_key: str, generator: str, mode: str) -> str:
    return f"{art_key}::{generator}::{mode}"


def judge_key(art_key: str, generator: str) -> str:
    return f"{art_key}::{generator}"


def is_valid_judge_result(judge_result) -> bool:
    """A judge result only counts as done-and-trustworthy if it actually
    came from an LLM judge with no error -- a heuristic fallback or an
    error dict is always eligible for retry on the next run."""
    if not isinstance(judge_result, dict):
        return False
    if judge_result.get("error"):
        return False
    if judge_result.get("judge_error"):
        return False
    if judge_result.get("criteria_source") != "llm":
        return False
    return True


def checkpoint_path(output: str) -> str:
    return f"{output}.checkpoint.json"


def load_checkpoint(path: str):
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # A corrupted/truncated checkpoint (e.g. process killed mid-write
        # before the atomic rename below existed) should not crash a
        # resume attempt -- fall back to starting fresh for this run.
        return None


def save_checkpoint(path: str, data: dict) -> None:
    """Atomic write: write to a temp file, then rename over the target,
    so a crash mid-write never corrupts a checkpoint that already had
    valid progress recorded in it."""
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)


def new_checkpoint() -> dict:
    return {"cells": {}, "judge_results": {}}


def cell_to_dict(analysis, metadata, failed) -> dict:
    return {
        "analysis": asdict(analysis) if analysis is not None else None,
        "metadata": metadata,
        "failed": failed,
    }


def cell_from_dict(d: dict):
    analysis = Analysis(**d["analysis"]) if d.get("analysis") else None
    return analysis, d.get("metadata", {}), d.get("failed", False)


def archive_existing_checkpoint(output: str) -> None:
    """Move any existing checkpoint + report aside with a timestamp
    suffix instead of overwriting them, so --fresh never destroys a
    previously completed, valid result set."""
    ckpt = checkpoint_path(output)
    if not os.path.exists(ckpt):
        return

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    for suffix in (".checkpoint.json", ".md", ".json"):
        src = f"{output}{suffix}"
        if os.path.exists(src):
            dst = f"{output}.archived_{stamp}{suffix}"
            shutil.move(src, dst)
            print(f"Archived existing {src} -> {dst}")
