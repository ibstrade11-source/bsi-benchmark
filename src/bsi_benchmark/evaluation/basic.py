from .base import Evaluator
from .result import EvaluationResult


class BasicEvaluator(Evaluator):
    """
    legacy fallback evaluator
    """

    def evaluate(self, dataset):
        return EvaluationResult(
            scores={
                "articles": len(dataset.articles)
            }
        )
