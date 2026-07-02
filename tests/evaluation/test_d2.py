"""D2 LongitudinalCoherence proxy: tag/language coherence.

A [FACT] sentence with hedge words, or a [SPECULATION]/[HYPOTHESIS]
sentence with only overclaim words, counts as incoherent.
"""
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(title="Mark of a Criminal Record", abstract="Audit study of employer callbacks.")


def _analyzed(text):
    return AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=text))


def test_d2_all_coherent_tags_scores_one():
    text = (
        "[FACT] Callback rates were lower for applicants with a criminal record. "
        "[SPECULATION] It may be the case that this pattern generalizes to all cities."
    )
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d2 == 1.0


def test_d2_incoherent_fact_with_hedge_lowers_score():
    text = (
        "[FACT] Callback rates may possibly have been somewhat lower for applicants "
        "with a criminal record, it seems."
    )
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d2 == 0.0


def test_d2_no_tags_at_all_defaults_to_one():
    # No tagged sentences means nothing to be incoherent about; tag_coverage
    # (a separate diagnostic) will independently be 0.0 in this case.
    text = "This is a plain paragraph with no claim tags at all."
    score = BSIEvaluator().score_dimensions(_analyzed(text))
    assert score.d2 == 1.0
