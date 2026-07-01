from .registry import registry


class EvaluationEngine:

    def evaluate(self, name, dataset):
        evaluator = registry.get(name)
        return evaluator().evaluate(dataset)
