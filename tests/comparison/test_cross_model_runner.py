"""
Offline end-to-end test of the actual benchmark goal: run multiple
generators under multiple prompt modes over a dataset, and score every
combination -- using MockGenerator so this runs with no network/API keys.
"""
from bsi_benchmark.comparison import ComparisonSpec, CrossModelRunner
from bsi_benchmark.datasets.dataset import Dataset
from bsi_benchmark.models import Article

DATASET = Dataset(
    provider="mock",
    query="test query",
    articles=[
        Article(title="Article One", abstract="First abstract."),
        Article(title="Article Two", abstract="Second abstract."),
    ],
)

SPEC = ComparisonSpec(
    generators=["mock"],
    prompt_modes={
        "raw": "Plain analysis.\n\nTitle: {title}\nAbstract: {abstract}",
        "bsi": "Follow the BSI master prompt.\n\nTitle: {title}\nAbstract: {abstract}",
    },
)


def test_cross_model_runner_produces_one_result_per_article():
    report = CrossModelRunner().run(DATASET, SPEC)
    assert len(report.results) == 2


def test_cross_model_runner_produces_one_cell_per_generator_mode_combo():
    report = CrossModelRunner().run(DATASET, SPEC)
    for result in report.results:
        assert len(result.cells) == 2  # 1 generator x 2 modes
        modes = {cell.mode for cell in result.cells}
        assert modes == {"raw", "bsi"}


def test_cross_model_runner_bsi_mode_scores_present_and_valid():
    report = CrossModelRunner().run(DATASET, SPEC)
    for result in report.results:
        for cell in result.cells:
            assert not cell.failed
            assert 0.0 <= cell.scores["BSI"] <= 1.0


def test_cross_model_runner_bsi_mode_uses_layered_analysis():
    # sanity check that "bsi" mode actually produced different (layered,
    # tagged) text from "raw" mode via MockGenerator, i.e. the two modes
    # are not accidentally identical.
    report = CrossModelRunner().run(DATASET, SPEC)
    result = report.results[0]
    raw_cell = next(c for c in result.cells if c.mode == "raw")
    bsi_cell = next(c for c in result.cells if c.mode == "bsi")
    assert raw_cell.analysis.text != bsi_cell.analysis.text
    assert "[FACT]" in bsi_cell.analysis.text
    assert "[FACT]" not in raw_cell.analysis.text
