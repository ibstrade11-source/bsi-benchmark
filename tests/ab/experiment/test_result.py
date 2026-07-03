from bsi_benchmark.ab.experiment.result import ExperimentResult


def test_result():

    r = ExperimentResult(
        prompt="AI",
        baseline="A",
        treatment="B",
    )

    assert r.prompt == "AI"
    assert r.baseline == "A"
    assert r.treatment == "B"
