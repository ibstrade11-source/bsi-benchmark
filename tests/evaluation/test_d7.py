from bsi_benchmark.evaluation.bsi import BSIEvaluator

class Article:
    def __init__(self, title=None, abstract=None, doi=None):
        self.title = title
        self.abstract = abstract
        self.doi = doi

class Dataset:
    def __init__(self, articles):
        self.articles = articles

def test_d7_full():
    score = BSIEvaluator().evaluate(
        Dataset([
            Article("Artificial Intelligence", "a", "1"),
            Article("Machine Learning Research", "b", "2"),
            Article("Large Language Models", "c", "3"),
            Article("Deep Learning", "d", "4"),
            Article("Neural Networks", "e", "5"),
        ])
    )
    assert score.d7 == 1.0

def test_d7_partial():
    score = BSIEvaluator().evaluate(
        Dataset([
            Article("AI", "a", "1"),
            Article("Machine Learning Research", None, "2"),
            Article("ML", "c", None),
        ])
    )
    expected = (0.6 + (1/3) + (1/3)) / 3
    assert abs(score.d7 - expected) < 1e-9
