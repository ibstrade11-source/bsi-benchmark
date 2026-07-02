"""
Result shapes for a cross-model comparison run.

A ComparisonCell holds either real scores (success) or an `error` key
(failure) -- a failed generation for one (article, generator, mode)
combination does not abort the whole run, it's just recorded as a gap in
the resulting table. This matters for real runs: if one provider rate-
limits or one API key is missing, you still get results for everything
else.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.models.article import Article


@dataclass
class ComparisonCell:
    generator: str
    mode: str
    analysis: Optional[Analysis]
    scores: Dict[str, float]

    @property
    def failed(self) -> bool:
        return "error" in self.scores


@dataclass
class ComparisonResult:
    article: Article
    cells: List[ComparisonCell] = field(default_factory=list)


@dataclass
class ComparisonReport:
    dataset_name: str
    results: List[ComparisonResult] = field(default_factory=list)
