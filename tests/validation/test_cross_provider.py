from bsi_benchmark.pipeline import PipelineRunner

PROVIDERS = [
    "crossref",
    "arxiv",
]

def test_cross_provider():

    runner = PipelineRunner()

    for provider in PROVIDERS:
        result = runner.run(
            provider,
            "Artificial Intelligence",
        )

        assert len(result.articles) > 0
