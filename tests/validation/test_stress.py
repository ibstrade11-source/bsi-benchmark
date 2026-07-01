from bsi_benchmark.pipeline import PipelineRunner

QUERIES = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Large Language Models",
    "Computer Vision",
]

def test_crossref_stress():

    runner = PipelineRunner()

    for query in QUERIES:
        result = runner.run("crossref", query)
        assert len(result.articles) > 0
