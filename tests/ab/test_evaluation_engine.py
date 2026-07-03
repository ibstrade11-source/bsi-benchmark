from bsi_benchmark.ab.evaluation.engine import ABEvaluationEngine


def test_ab_engine():
    engine = ABEvaluationEngine()

    result = engine.run("What is artificial intelligence?")

    assert "baseline" in result
    assert "bsi_enhanced" in result
    assert "delta" in result
