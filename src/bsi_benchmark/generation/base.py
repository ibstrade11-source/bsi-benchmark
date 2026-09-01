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

    def generate_with_judge_resource(
        self,
        article,
        system_prompt: str,
        user_prompt: str,
        judge_resource: str | None = None,
    ):
        """Judge-resource transport contract.

        Architectural separation:

        system_prompt:
            judging instructions only.

        user_prompt:
            article + RAW/BSI comparison task only.

        judge_resource:
            independent judge-side knowledge resource.

        The base class MUST NOT concatenate judge_resource into either
        prompt. Provider implementations that support an independent
        resource channel may override this method.
        """
        if judge_resource:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not implement the "
                "independent judge-resource transport API"
            )

        return self.generate_with_system(
            article,
            system_prompt,
            user_prompt,
        )

    def generate_with_system(self, article, system_prompt: str, user_prompt: str):
        """
        Like generate(), but with the prompt split into a system-level
        context (background/reference material, e.g. task rules and the
        BSI glossary) and a user-level task (the actual content being
        acted on, e.g. the RAW/BSI analyses to compare).

        Keeping this split matters for the judge specifically: the
        glossary is background context for interpreting BSI terminology,
        not part of the comparison task itself, and mixing it into the
        same turn as the RAW/BSI analyses blurs that distinction for the
        model. Subclasses whose backend supports a real system-role
        message (OpenRouterGenerator, GroqGenerator) override this to
        send system_prompt and user_prompt as separate messages.

        Default implementation (for generators that don't override this):
        falls back to a single combined prompt via generate(), so every
        generator keeps working without needing this method implemented.
        """
        combined = f"{system_prompt}\n\n{user_prompt}"
        return self.generate(article, combined)
