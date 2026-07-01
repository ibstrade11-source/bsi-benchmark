class EvaluationRegistry:

    def __init__(self):
        self._evaluators = {}

    def register(self, evaluator):
        self._evaluators[evaluator.name] = evaluator

    def get(self, name):
        return self._evaluators[name]

    def available(self):
        return sorted(self._evaluators.keys())


registry = EvaluationRegistry()
