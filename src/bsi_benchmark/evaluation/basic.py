from .result import EvaluationResult
from .bsi import BSIEvaluator


class BasicEvaluator:
    def evaluate(self, dataset):
        s = BSIEvaluator().evaluate(dataset)

        scores = {
            "D1": s.d1,
            "D2": s.d2,
            "D3": s.d3,
            "D4": s.d4,
            "D5": s.d5,
            "D6": s.d6,
            "D7": s.d7,
            "BSI": s.total,
        }

        return EvaluationResult(
            evaluator="bsi",
            scores=scores,
        )
