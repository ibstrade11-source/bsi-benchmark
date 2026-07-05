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
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


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

    def raw_wins(self) -> int:
        return sum(1 for c in self.criteria if c.winner == "raw")

    def bsi_wins(self) -> int:
        return sum(1 for c in self.criteria if c.winner == "bsi")

    def ties(self) -> int:
        return sum(1 for c in self.criteria if c.winner == "tie")
