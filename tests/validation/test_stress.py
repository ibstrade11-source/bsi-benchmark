from bsi_benchmark.pipeline import PipelineRunner

QUERIES = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Large Language Models",
    "Computer Vision",
]

def test_crossref_stress():
    import os
    import pytest

    # Live provider stress tests are opt-in so the default suite
    # remains deterministic and independent of DNS/network state.
    if os.environ.get("BSI_LIVE_NETWORK_TESTS") != "1":
        pytest.skip(
            "Crossref live stress test disabled by default; "
            "set BSI_LIVE_NETWORK_TESTS=1 to run it."
        )


    runner = PipelineRunner()

    for query in QUERIES:
        result = runner.run("crossref", query)
        assert len(result.articles) > 0
