from typing import Dict, Type
from .base import Evaluator
from .basic import BasicEvaluator
from .bsi import BSIEvaluator


class EvaluationRegistry:
    def __init__(self):
        self._evals: Dict[str, Type] = {}

        # default registrations
        # NOTE: previously "bsi" was mistakenly registered to BasicEvaluator
        # (a copy-paste error), which meant evaluate("basic", ds) and
        # evaluate("bsi", ds) silently ran identical logic. Fixed: "basic"
        # operates on a raw Dataset, "bsi" operates on an AnalyzedArticle.
        self.register("basic", BasicEvaluator)
        self.register("bsi", BSIEvaluator)

    def register(self, name: str, cls: Type):
        self._evals[name] = cls

    def get(self, name: str):
        return self._evals[name]

    def names(self):
        return sorted(self._evals.keys())


registry = EvaluationRegistry()
