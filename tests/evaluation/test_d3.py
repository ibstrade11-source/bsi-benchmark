from bsi_benchmark.evaluation.bsi import BSIEvaluator


class Article:
    def __init__(self, title):
        self.title = title
        self.abstract = "abstract"
        self.doi = "doi"


class Dataset:
    def __init__(self, articles):
        self.articles = articles


def test_d3_full():
    score = BSIEvaluator().evaluate(
        Dataset([
            Article("Artificial Intelligence"),
            Article("Machine Learning Research"),
            Article("Large Language Models"),
        ])
    )
    assert score.d3 == 1.0


def test_d3_partial():
    score = BSIEvaluator().evaluate(
        Dataset([
            Article("AI"),
            Article("Machine Learning Research"),
            Article("ML"),
        ])
    )
    assert abs(score.d3 - (1 / 3)) < 1e-9
