from .base import Evaluator
from .registry import registry
from .result import EvaluationResult


class BasicEvaluator(Evaluator):

    name = "basic"

    def evaluate(self, dataset):
        return EvaluationResult(
            evaluator=self.name,
            scores={
                "articles": len(dataset.articles)
            }
        )


registry.register(BasicEvaluator())
