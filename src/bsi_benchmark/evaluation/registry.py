from typing import Dict, Type

from .basic import BasicEvaluator
from .bsi import BSIEvaluator


class EvaluationRegistry:

    def __init__(self):
        self._evals: Dict[str, Type] = {}
        self.register("basic", BasicEvaluator)
        self.register("bsi", BSIEvaluator)

    def register(self, name, cls):
        self._evals[name] = cls

    def get(self, name):
        return self._evals[name]

    def names(self):
        return sorted(self._evals)


registry = EvaluationRegistry()
