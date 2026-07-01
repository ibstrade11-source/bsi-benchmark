from bsi_benchmark.evaluation.bsi import BSIEvaluator


class Article:
    def __init__(self, abstract=None, doi=None):
        self.abstract = abstract
        self.doi = doi
        self.title = "Artificial Intelligence"


class Dataset:
    def __init__(self, articles):
        self.articles = articles


def test_d2_full():
    score = BSIEvaluator().evaluate(
        Dataset([
            Article("a", "1"),
            Article("b", "2"),
            Article("c", "3"),
        ])
    )
    assert score.d2 == 1.0


def test_d2_partial():
    score = BSIEvaluator().evaluate(
        Dataset([
            Article("a", "1"),
            Article(None, "2"),
            Article("c", None),
        ])
    )
    assert abs(score.d2 - (1 / 3)) < 1e-9
