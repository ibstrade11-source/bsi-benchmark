"""D5 StrategicDepth proxy: density of implication/forward-looking statements."""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(title="Interpretation Drift", abstract="A framework for analytical governance.")


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d5_no_implication_language_scores_zero():
    text = "The paper defines drift and gives two examples."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d5 == 0.0


def test_d5_implication_language_raises_score():
    text = (
        "This suggests that going forward, future work should extend the "
        "framework; the implication is that downstream effects on governance "
        "follow-on into other domains, and this means that practitioners "
        "should reassess their pipelines."
    )
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d5 > 0.0
