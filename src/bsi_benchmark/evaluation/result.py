from dataclasses import dataclass


@dataclass
class EvaluationResult:
    evaluator: str
    scores: dict
