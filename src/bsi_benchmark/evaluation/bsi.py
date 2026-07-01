from .base import Evaluator
from .result import EvaluationResult


class BSIawareEvaluator(Evaluator):
    """
    Simple BSI-aware scoring (v1):
    - completeness
    - article volume normalization
    """

    def __init__(self, metrics):
        self.metrics = metrics

    def evaluate(self, dataset):
        scores = {}

        for metric in self.metrics:
            scores[metric.name] = metric.compute(dataset)

        # aggregate BSI score (simple weighted mean placeholder)
        total = sum(scores.values()) if scores else 0
        normalized = total / max(len(scores), 1)

        scores["bsi_score"] = normalized

        return EvaluationResult(scores=scores)
