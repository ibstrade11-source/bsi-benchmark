from dataclasses import dataclass
from typing import Dict

@dataclass
class EvaluationResult:
    evaluator: str
    scores: Dict[str, float]
