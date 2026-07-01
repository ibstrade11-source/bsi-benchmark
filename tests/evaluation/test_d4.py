from bsi_benchmark.evaluation.bsi import BSIEvaluator


class Article:
    def __init__(self):
        self.title = "Artificial Intelligence"
        self.abstract = "abstract"
        self.doi = "doi"


class Dataset:
    def __init__(self, n):
        self.articles = [Article() for _ in range(n)]


def test_d4_full():
    score = BSIEvaluator().evaluate(Dataset(5))
    assert score.d4 == 1.0


def test_d4_partial():
    score = BSIEvaluator().evaluate(Dataset(2))
    assert score.d4 == 0.4
