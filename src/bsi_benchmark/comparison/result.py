"""
Result shapes for cross-model comparison runs.

A ComparisonCell represents one generator/mode combination.

Important validity rules:
- failed generations are never represented by a fake score;
- incomplete article inputs are invalid;
- a benchmark run is not publishable unless every required analysis
  and the independent judge result are present and valid.
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
    metadata: Dict[str, object]
    judge_result: Optional[dict] = None
    scores: dict = field(default_factory=dict)
    failed: bool = False

    @property
    def has_valid_analysis(self) -> bool:
        return self.analysis is not None

    @property
    def has_valid_judge(self) -> bool:
        if self.judge_result is None:
            return False

        if not isinstance(self.judge_result, dict):
            return False

        if self.judge_result.get("error"):
            return False

        return True


@dataclass
class ComparisonResult:
    article: Article
    cells: List[ComparisonCell] = field(default_factory=list)

    @property
    def article_input_valid(self) -> bool:
        title = getattr(self.article, "title", None)
        abstract = getattr(self.article, "abstract", None)

        return (
            isinstance(title, str)
            and bool(title.strip())
            and isinstance(abstract, str)
            and bool(abstract.strip())
        )

    @property
    def complete(self) -> bool:
        if not self.article_input_valid:
            return False

        if not self.cells:
            return False

        for cell in self.cells:
            if cell.failed:
                return False

            if not cell.has_valid_analysis:
                return False

            if cell.mode == "bsi" and not cell.has_valid_judge:
                return False

        return True


@dataclass
class ComparisonReport:
    dataset_name: str
    results: List[ComparisonResult] = field(default_factory=list)

    source_url: Optional[str] = None
    run_metadata: Optional[dict] = None

    @property
    def complete(self) -> bool:
        """
        A report is publishable only when every article/result is complete.

        This deliberately fails closed: missing judge output, missing
        analysis, failed generation, or incomplete article input makes
        the whole report non-publishable.
        """
        if not self.results:
            return False

        return all(result.complete for result in self.results)

    @property
    def incomplete_reasons(self) -> List[str]:
        reasons = []

        for index, result in enumerate(self.results, 1):
            if not result.article_input_valid:
                reasons.append(
                    f"article {index}: missing/invalid title or abstract"
                )

            if not result.cells:
                reasons.append(
                    f"article {index}: no comparison cells"
                )

            for cell in result.cells:
                if cell.failed:
                    error = cell.metadata.get("error")
                    if error:
                        reasons.append(
                            f"article {index}/{cell.generator}/{cell.mode}: "
                            f"generation failed: {error}"
                        )
                    else:
                        reasons.append(
                            f"article {index}/{cell.generator}/{cell.mode}: "
                            "generation failed"
                        )

                if cell.analysis is None:
                    reasons.append(
                        f"article {index}/{cell.generator}/{cell.mode}: "
                        "missing analysis"
                    )

                if cell.mode == "bsi" and not cell.has_valid_judge:
                    reasons.append(
                        f"article {index}/{cell.generator}/{cell.mode}: "
                        "missing or invalid independent judge result"
                    )

        return reasons
