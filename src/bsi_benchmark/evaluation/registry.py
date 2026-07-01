from typing import Dict, Type
from .base import Evaluator
from .basic import BasicEvaluator
from .bsi import BSIAwareEvaluator
from .bsi import BSIAwareEvaluator


class EvaluationRegistry:
    def __init__(self):
        self._evals: Dict[str, Type[Evaluator]] = {}

        # default registrations
        self.register("basic", BasicEvaluator)
        self.register("bsi", BSIAwareEvaluator)

    def register(self, name: str, cls: Type[Evaluator]):
        self._evals[name] = cls

    def get(self, name: str):
        return self._evals[name]

    def names(self):
        return sorted(self._evals.keys())


registry = EvaluationRegistry()
