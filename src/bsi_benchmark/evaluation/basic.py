from .result import EvaluationResult
from .bsi import BSIEvaluator

class BasicEvaluator:
    def evaluate(self, dataset):
        s = BSIEvaluator().evaluate(dataset)

        scores = {
            "D1": s.coverage,
            "D2": s.completeness,
            "D3": s.signal_quality,
            "D4": s.total,
            "D5": s.total,
            "D6": s.total,
            "D7": s.total,
            "coverage": s.coverage,
            "completeness": s.completeness,
            "signal_quality": s.signal_quality,
            "BSI": (
                s.coverage +
                s.completeness +
                s.signal_quality +
                s.total * 4
            ) / 7,
        }

        return EvaluationResult(
            evaluator="bsi",
            scores=scores,
        )
