"""D7 AntiPerformativeDrift proxy: hedge markers vs. overclaim markers."""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(title="Some paper", abstract="Some findings.")


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d7_only_overclaiming_scores_zero():
    text = "This certainly always proves the effect definitely and undeniably."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d7 == 0.0


def test_d7_only_hedging_scores_one():
    text = "This may possibly suggest the effect, which could likely be the case."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d7 == 1.0


def test_d7_neither_marker_scores_neutral():
    text = "The paper presents a result about employment."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d7 == 0.5


def test_d7_mixed_markers_scores_between():
    text = "This certainly shows an effect, though it may not generalize."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert 0.0 < score.d7 < 1.0
