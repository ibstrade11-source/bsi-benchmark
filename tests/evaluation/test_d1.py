from bsi_benchmark.evaluation.bsi import BSIEvaluator


class Article:
    def __init__(self):
        self.title = "Artificial Intelligence"
        self.abstract = "Abstract"
        self.doi = "10.1000/test"


class Dataset:
    def __init__(self, n):
        self.articles = [Article() for _ in range(n)]


def test_d1_full_coverage():
    score = BSIEvaluator().evaluate(Dataset(5))
    assert score.d1 == 1.0


def test_d1_partial_coverage():
    score = BSIEvaluator().evaluate(Dataset(2))
    assert score.d1 == 0.4
