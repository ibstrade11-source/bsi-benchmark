"""
Run-level metadata for a ComparisonReport, so a report can stand on its
own as evidence: which exact code produced it, when, and with what known
methodological limitations -- rather than a bare score table with no
provenance.

This does NOT make BSI scores a validated psychometric instrument. It
makes the *report* an honest, checkable record of what was run.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from .version import __version__ as TOOL_VERSION

METHODOLOGY_NOTE = (
    "Scores are produced by BSIEvaluator, an offline lexical/keyword-based "
    "proxy for the seven BIO v1.0 dimensions (regex and keyword matching, "
    "not semantic understanding). They are first-pass triage signals, not "
    "a validated measurement of analytical quality, until checked against "
    "independent human judgement on a representative sample. Do not cite "
    "numeric BSI scores as a certified metric without that validation step."
)


def _git_commit(cwd: Optional[str] = None) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def _git_dirty(cwd: Optional[str] = None) -> Optional[bool]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return bool(result.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return None


@dataclass
class RunMetadata:
    tool_version: str
    git_commit: Optional[str]
    git_dirty: Optional[bool]
    run_timestamp_utc: str
    methodology_note: str = METHODOLOGY_NOTE

    @classmethod
    def capture(cls, repo_dir: Optional[str] = None) -> "RunMetadata":
        """
        Build a RunMetadata snapshot for 'right now'.

        git_commit / git_dirty are None (not False) if this isn't a git
        checkout or git isn't available -- callers should render that as
        an explicit "unknown", not silently treat it as clean/absent.
        """
        return cls(
            tool_version=TOOL_VERSION,
            git_commit=_git_commit(repo_dir),
            git_dirty=_git_dirty(repo_dir),
            run_timestamp_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
