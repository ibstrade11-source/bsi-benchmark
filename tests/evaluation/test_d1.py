"""D1 ConditionalDepth proxy: density of conditional-reasoning markers."""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(title="Import Competition and Labor Markets", abstract="A study of trade shocks.")


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d1_no_conditional_markers_scores_zero():
    text = "This paper shows that imports reduced employment. Wages fell in exposed regions."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d1 == 0.0


def test_d1_conditional_markers_raise_score():
    low = "This paper shows imports reduced employment."
    high = (
        "If the shift-share instrument is valid, then imports reduced "
        "employment, assuming labor is regionally immobile, provided that "
        "capital does not reallocate, and given that local demand elasticity "
        "is stable, if these conditions hold across regions."
    )
    low_score = BSIEvaluator().score_dimensions(_analyzed(low))
    high_score = BSIEvaluator().score_dimensions(_analyzed(high))
    assert high_score.d1 > low_score.d1


def test_d1_empty_analysis_scores_zero_everywhere():
    score = BSIEvaluator().score_dimensions(_analyzed(""))
    assert score.d1 == 0.0
    assert score.total == 0.0
