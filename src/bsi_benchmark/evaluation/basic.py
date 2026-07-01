from .bsi import BSIEvaluator


class BasicEvaluator:
    def __init__(self):
        self.impl = BSIEvaluator()

    def evaluate(self, dataset):
        return self.impl.evaluate(dataset)
