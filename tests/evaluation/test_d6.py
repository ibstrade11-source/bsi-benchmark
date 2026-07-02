"""D6 InterdisciplinaryBreadth proxy: distinct disciplinary keyword clusters touched."""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(title="Cross-disciplinary study", abstract="A broad analysis.")


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d6_single_domain_scores_low():
    text = "This is a purely economic analysis of market prices and inflation."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert 0.0 < score.d6 <= 0.25


def test_d6_multiple_domains_scores_higher():
    text = (
        "This touches economic market dynamics, sociological institution "
        "effects, philosophical epistemic questions, and computer science "
        "algorithm design, plus legal regulation constraints."
    )
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d6 >= 0.5
