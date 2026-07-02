"""D3 AuthenticEthicalLayer proxy: presence and depth of a Meta layer."""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(title="Is Justified True Belief Knowledge?", abstract="Gettier counterexamples to JTB.")


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d3_no_meta_layer_scores_zero():
    text = "Manifest layer: the paper gives two counterexamples to JTB."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d3 == 0.0


def test_d3_meta_layer_present_scores_above_zero():
    text = "لایه Meta (فرا): این پرسش مبنایی است که آیا دانش اساساً شرط‌محور تعریف می‌شود یا نه، " * 5
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d3 > 0.0


def test_d3_longer_meta_bearing_text_scores_higher_than_bare_header():
    bare = "Meta layer."
    substantial = "Meta layer: " + ("this discusses the deeper epistemic stakes of the argument. " * 40)
    bare_score = BSIEvaluator().score_dimensions(_analyzed(bare))
    substantial_score = BSIEvaluator().score_dimensions(_analyzed(substantial))
    assert substantial_score.d3 > bare_score.d3
