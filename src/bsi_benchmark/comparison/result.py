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


# Execution status vocabulary, per METHODOLOGY.md section 35 ("Failure
# Handling"): every Run must carry one of these four statuses rather than
# a single failed/not-failed boolean, so a caller can distinguish "this
# generated fine but is still missing a required independent judge
# result" (INCOMPLETE) from "the generator call itself failed"
# (FAILED), and from the theoretically-unreachable data-integrity
# anomaly of a cell with no analysis that was never marked failed
# (INVALID). This is purely additive: `failed` and the existing
# has_valid_analysis/has_valid_judge properties are unchanged, and
# ComparisonResult.complete still uses the same logic it always did --
# `status` is a derived, read-only summary of that same logic, exposed
# as a real dataclass field so it round-trips through asdict()/JSON
# export (see comparison/json_export.py) instead of only existing as a
# property that dataclasses.asdict() would silently drop.
STATUS_VALID = "valid"
STATUS_FAILED = "failed"
STATUS_INCOMPLETE = "incomplete"
STATUS_INVALID = "invalid"


@dataclass
class ComparisonCell:
    generator: str
    mode: str
    analysis: Optional[Analysis]
    metadata: Dict[str, object]
    judge_result: Optional[dict] = None
    scores: dict = field(default_factory=dict)
    failed: bool = False
    status: str = field(init=False, default=STATUS_VALID)
    model_id: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.status = self._compute_status()
        # METHODOLOGY.md section 5 requires the exact model identifier to
        # be recorded per Run. Analysis.source_model already carries this
        # (e.g. "openai/gpt-oss-20b", set by each generator -- see
        # generation/groq.py, generation/openrouter.py, etc.) but was only
        # reachable by digging into the nested analysis object. Surfacing
        # it as a first-class cell field means it stays visible even when
        # inspecting/exporting cell-level status without needing to know
        # to look inside `analysis`, and it is still None -- never
        # fabricated -- for a failed cell with no analysis, per section 63.
        if self.analysis is not None:
            self.model_id = getattr(self.analysis, "source_model", None)

    def _compute_status(self) -> str:
        if self.failed:
            return STATUS_FAILED

        if self.analysis is None:
            # failed=False but no analysis is a data-integrity anomaly
            # that should not occur through the normal runner path --
            # flagged rather than silently treated as either valid or
            # a generation failure.
            return STATUS_INVALID

        if self.mode == "bsi" and not self.has_valid_judge:
            # Generation succeeded but the run is not yet
            # evidence-complete: no independent judge result (or an
            # invalid/heuristic one) is attached.
            return STATUS_INCOMPLETE

        return STATUS_VALID

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

        if self.judge_result.get("judge_error"):
            return False

        if self.judge_result.get("criteria_source") != "llm":
            return False

        return True


@dataclass
class ComparisonResult:
    article: Article
    cells: List[ComparisonCell] = field(default_factory=list)
    # METHODOLOGY.md section 4.1 requires a stable Artifact ID recorded
    # before output generation. This reuses the exact identity function
    # already used for checkpoint caching (comparison/checkpoint.py
    # article_key: DOI when present, otherwise a content hash of
    # title+abstract) rather than inventing a second, potentially
    # inconsistent identifier -- so a result's article_id always matches
    # the cache key that produced its cells. Empty string, not None, is
    # the "not supplied" default so this field round-trips cleanly
    # through JSON export even for results built outside the normal
    # runner path (e.g. in tests).
    article_id: str = ""

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
