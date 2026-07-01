from .bsi import BSIEvaluator
from .result import EvaluationResult

class BasicEvaluator:
    def evaluate(self, dataset):
        s = BSIEvaluator().evaluate(dataset)
        return EvaluationResult(
            evaluator="bsi",
            scores={
                "coverage": s.coverage,
                "completeness": s.completeness,
                "signal_quality": s.signal_quality,
                "BSI": s.total,
            },
        )
