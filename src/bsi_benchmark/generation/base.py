"""
AnalysisGenerator: produces an Analysis (BSI-generated or raw/baseline text)
for a given Article by calling an LLM.

This is the piece that lets the benchmark run *automatically* across
multiple models, rather than requiring a human to paste in pre-generated
analysis text every time (that manual path still exists via `evaluate`/
AnalyzedDatasetIO for one-off spot checks, but `compare` is the automated
entry point this class exists for).
"""

from abc import ABC, abstractmethod

from bsi_benchmark.models.article import Article
from bsi_benchmark.models.analysis import Analysis


class AnalysisGenerator(ABC):

    name: str

    @abstractmethod
    def generate(self, article: Article, prompt_template: str) -> Analysis:
        """
        Args:
            article: the raw article to analyze.
            prompt_template: a string containing `{title}` and `{abstract}`
                placeholders (see generation/prompt.py:render). Callers
                control what's in this template -- e.g. a bare instruction
                for a "raw" baseline run, or the full BSI master prompt for
                a "bsi" run -- which is exactly the axis this benchmark is
                meant to compare.

        Returns:
            An Analysis with `.text` set to the model's raw output and
            `.source_model` set to this generator's model identifier.

        Raises:
            bsi_benchmark.errors.ProviderError (or a subclass) on any
            request failure, mirroring how providers/ report fetch
            failures, so callers can handle both uniformly.
        """
        raise NotImplementedError
