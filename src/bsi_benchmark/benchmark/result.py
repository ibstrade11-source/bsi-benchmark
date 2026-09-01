from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    dataset: object
    evaluation: object = None
    report: str = ""

    @property
    def provider(self):
        return self.dataset.provider

    @property
    def query(self):
        return self.dataset.query

    @property
    def articles(self):
        return self.dataset.articles

    @property
    def scores(self):
        if self.evaluation and hasattr(self.evaluation, "scores"):
            return self.evaluation.scores
        return {}
