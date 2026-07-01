from bsi_benchmark.pipeline import PipelineRunner


def test_reproducibility():
    runner = PipelineRunner()

    a = runner.run(
        "crossref",
        "Artificial Intelligence",
    )

    b = runner.run(
        "crossref",
        "Artificial Intelligence",
    )

    assert len(a.articles) > 0
    assert len(b.articles) > 0
