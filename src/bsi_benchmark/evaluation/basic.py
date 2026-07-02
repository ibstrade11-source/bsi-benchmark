"""
BasicEvaluator: a trivial, non-BSI smoke-test evaluator over a raw
(fetched, not-yet-analyzed) Dataset. Useful for quickly checking that a
provider/query returned anything at all, without needing an analysis text.

This previously got overwritten to secretly delegate to BSIEvaluator,
which meant "basic" and "bsi" silently did the exact same thing. Restored
to its original, distinct purpose here.
"""

from .result import EvaluationResult


class BasicEvaluator:

    name = "basic"

    def evaluate(self, dataset) -> EvaluationResult:
        return EvaluationResult(
            evaluator=self.name,
            scores={"articles": len(dataset.articles)},
        )
