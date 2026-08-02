"""
Data model for a self-comparison record.

Design intent (agreed in discussion, not an arbitrary schema choice):

- The ANALYST (an LLM, or a person) writes both a "raw" and a "bsi"
  analysis of the same article, then compares its own two outputs.
- The analyst chooses its OWN criteria -- this tool does not supply a
  fixed rubric. Forcing a fixed rubric would make the self-comparison
  no longer independent (see project discussion: imposing a lens
  collapses the value of self-judgement). Different analysts, or the
  same analyst on different articles, may use entirely different
  criteria lists. That heterogeneity is intentional and is preserved
  all the way to storage -- it is not normalized or forced into a
  common schema across records.
- For each criterion the analyst supplies a raw_score and a bsi_score
  (any consistent numeric scale the analyst chooses, e.g. 1-10). The
  winner for that criterion is DERIVED from the two scores, not
  separately asserted -- this keeps the "winner" column from silently
  disagreeing with the numbers next to it.
- This module has no opinion on which criteria are good. It only
  gives the self-comparison a consistent, storable, comparison-table
  shape so many heterogeneous records can be collected (the benchmark's
  actual goal: collection and recording, not standard-setting).
- Self-evidencing: raw_analysis_text / bsi_analysis_text hold the actual
  text each score was based on, so a record isn't just asserted numbers
  -- a reader can check a score against the real text. SHA-256 hashes
  are auto-derived from the text (never both supplied independently and
  possibly inconsistent), so the hash is always exactly what you'd get
  from re-hashing the stored text.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import List, Optional


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class CriterionScore:
    """One row of the analyst's own comparison table."""
    criterion: str
    raw_score: float
    bsi_score: float
    notes: Optional[str] = None

    @property
    def winner(self) -> str:
        """
        Derived, not analyst-asserted: 'raw', 'bsi', or 'tie'.

        Deriving this from the two scores (rather than letting the
        analyst state a winner independently of the numbers) prevents
        the table from containing a winner column that contradicts its
        own score columns.
        """
        if self.raw_score > self.bsi_score:
            return "raw"
        if self.bsi_score > self.raw_score:
            return "bsi"
        return "tie"


@dataclass
class SelfComparisonRecord:
    """
    A single analyst's self-comparison of their own raw-vs-bsi analysis
    of one article.
    """
    article_title: str
    analyst_model: str
    criteria: List[CriterionScore]
    overall_winner: str
    overall_reasoning: str
    article_doi: Optional[str] = None
    article_url: Optional[str] = None
    # Free-text list of the analyst's OWN criteria, in their own words,
    # kept separately from the table rows so the analyst's framing is
    # preserved verbatim even if the table above is later re-parsed.
    criteria_rationale: Optional[str] = None
    run_metadata: Optional[dict] = None

    # Self-evidencing: the actual text each score was based on. Without
    # this, a record is just asserted numbers -- no one can check that a
    # score of 8 actually matches what the "bsi" analysis said. Both are
    # optional (a record without them still loads/works, for backward
    # compatibility and for cases where full text can't be shared), but
    # including them is what makes a record checkable rather than merely
    # self-reported. The CLI warns (but does not refuse) when missing.
    raw_analysis_text: Optional[str] = None
    bsi_analysis_text: Optional[str] = None
    # Hashes are stored explicitly (not just computed on demand) so a
    # hash can be published/compared even in a context where the full
    # text is withheld later (e.g. copyright, length limits) -- but they
    # are always auto-derived FROM the text at construction time, never
    # accepted as an independent, possibly-inconsistent input.
    raw_analysis_sha256: Optional[str] = field(default=None, init=False)
    bsi_analysis_sha256: Optional[str] = field(default=None, init=False)

    def __post_init__(self):
        if self.raw_analysis_text is not None:
            self.raw_analysis_sha256 = _sha256(self.raw_analysis_text)
        if self.bsi_analysis_text is not None:
            self.bsi_analysis_sha256 = _sha256(self.bsi_analysis_text)

    def has_source_texts(self) -> bool:
        return bool(self.raw_analysis_text) and bool(self.bsi_analysis_text)

    def verify_hashes(self) -> dict:
        """
        Re-check stored hashes against stored text. Returns
        {'raw': True/False/None, 'bsi': True/False/None} -- None means
        there was no text+hash pair to check (e.g. text withheld).
        Only meaningful after loading a record from disk where the
        hash might have been tampered with independently of the text;
        for records built fresh in this process the two can never
        disagree, since __post_init__ always derives one from the other.
        """
        result = {"raw": None, "bsi": None}
        if self.raw_analysis_text is not None and self.raw_analysis_sha256:
            result["raw"] = _sha256(self.raw_analysis_text) == self.raw_analysis_sha256
        if self.bsi_analysis_text is not None and self.bsi_analysis_sha256:
            result["bsi"] = _sha256(self.bsi_analysis_text) == self.bsi_analysis_sha256
        return result

    def raw_wins(self) -> int:
        return sum(1 for c in self.criteria if c.winner == "raw")

    def bsi_wins(self) -> int:
        return sum(1 for c in self.criteria if c.winner == "bsi")

    def ties(self) -> int:
        return sum(1 for c in self.criteria if c.winner == "tie")
