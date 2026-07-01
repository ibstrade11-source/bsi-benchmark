from bsi_benchmark.pipeline import PipelineRunner
from bsi_benchmark.evaluation import EvaluationEngine


def test_bsi():
    dataset = PipelineRunner().run(
        "crossref",
        "Artificial Intelligence",
    )

    result = EvaluationEngine().evaluate("bsi", dataset)

    assert "BSI" in result.scores

    for i in range(1, 8):
        assert f"D{i}" in result.scores

    assert 0 <= result.scores["BSI"] <= 1
