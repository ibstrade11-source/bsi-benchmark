"""D4 CreativeValueAdd proxy: lexical novelty of the analysis vs. the raw source."""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(
    title="The China Syndrome Local Labor Market Effects",
    abstract="Import competition reduced manufacturing employment in exposed regions.",
)


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d4_pure_restatement_scores_low():
    # Reuses almost exactly the source vocabulary -> low novelty.
    text = "Import competition reduced manufacturing employment in exposed regions."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d4 < 0.3


def test_d4_substantive_new_vocabulary_scores_higher():
    text = (
        "The instrumental variable strategy relies on shift-share exogeneity "
        "assumptions borrowed from general equilibrium migration literature, "
        "raising concerns about spatial spillovers and downstream retraining policy."
    )
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d4 > 0.5
