"""End-to-end BSI evaluation, offline (no network): via the registry/engine
using an AnalyzedArticle, mirroring how the CLI/reporting layer would call it.
"""
from bsi_benchmark.evaluation import EvaluationEngine
from bsi_benchmark.evaluation.dimensions import WEIGHTS
from bsi_benchmark.models import Article, Analysis, AnalyzedArticle

ARTICLE = Article(
    title="The China Syndrome: Local Labor Market Effects of Import Competition",
    abstract="This paper studies how rising Chinese import competition affected local U.S. labor markets.",
    doi="10.1257/aer.103.6.2121",
)

ANALYSIS_TEXT = """
لایه Manifest (آشکار):
[FACT] Employment fell in manufacturing-exposed commuting zones between 1990 and 2007.

لایه Latent (پنهان):
[INFERENCE] If the shift-share instrument is valid, assuming regional labor immobility,
then the estimated employment effect can be interpreted causally, provided that
capital does not reallocate freely across regions.

لایه Meta (فرا):
[SPECULATION] It is possible, though not established by this study alone, that similar
dynamics could generalize to other advanced economies facing comparable trade shocks.
This suggests that going forward, future work on general-equilibrium spillovers and
regional retraining policy implications would be a natural extension, with downstream
effects for labor economics and trade policy debates more broadly.
""" * 2  # long enough to give the Meta-layer length bonus room to move


def test_bsi_via_engine_produces_all_expected_scores():
    dataset = AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=ANALYSIS_TEXT))

    result = EvaluationEngine().evaluate("bsi", dataset)

    assert result.evaluator == "bsi"
    for i in range(1, 8):
        assert f"D{i}" in result.scores
    assert "BSI" in result.scores
    assert "grounding_ratio" in result.scores
    assert "tag_coverage" in result.scores

    assert 0.0 <= result.scores["BSI"] <= 1.0


def test_bsi_total_matches_weighted_formula_not_plain_average():
    dataset = AnalyzedArticle(article=ARTICLE, analysis=Analysis(text=ANALYSIS_TEXT))
    result = EvaluationEngine().evaluate("bsi", dataset)

    manual_weighted = sum(
        result.scores[f"D{i}"] * WEIGHTS[f"d{i}"]
        for i in range(1, 8)
    )
    assert abs(result.scores["BSI"] - manual_weighted) < 1e-9

    plain_average = sum(result.scores[f"D{i}"] for i in range(1, 8)) / 7.0
    # Only equal by coincidence; assert the formula is actually weighted by
    # checking it against a case where weighted != unweighted (true here
    # since the seven scores are not all equal for this sample text).
    if len({round(result.scores[f"D{i}"], 6) for i in range(1, 8)}) > 1:
        assert abs(result.scores["BSI"] - plain_average) > 1e-9


def test_bsi_and_basic_are_no_longer_aliases():
    # Regression test for the fixed registry bug where both "basic" and
    # "bsi" pointed at the same class.
    from bsi_benchmark.evaluation.registry import registry
    assert registry.get("basic") is not registry.get("bsi")
