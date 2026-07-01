from typing import Dict, Type
from .base import Evaluator
from .basic import BasicEvaluator
from .bsi import BSIEvaluator
from .bsi import BSIEvaluator


class EvaluationRegistry:
    def __init__(self):
        self._evals: Dict[str, Type[Evaluator]] = {}

        # default registrations
        self.register("basic", BasicEvaluator)
        self.register("bsi", BSIEvaluator)

    def register(self, name: str, cls: Type[Evaluator]):
        self._evals[name] = cls

    def get(self, name: str):
        return self._evals[name]

    def names(self):
        return sorted(self._evals.keys())


registry = EvaluationRegistry()
