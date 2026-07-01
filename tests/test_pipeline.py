from bsi_benchmark.pipeline import PipelineRunner


def test_pipeline_crossref():

    runner = PipelineRunner()

    result = runner.run(
        "crossref",
        "Artificial Intelligence",
    )

    assert result.provider == "crossref"
    assert len(result.articles) > 0
