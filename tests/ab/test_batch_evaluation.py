from bsi_benchmark.ab.evaluation.batch.runner import ABBatchRunner
from bsi_benchmark.ab.evaluation.batch.aggregator import ABBatchAggregator


def test_batch_ab_engine():
    dataset = [
        {"text": "Artificial intelligence is changing science."},
        {"text": "Machine learning improves prediction accuracy."},
    ]

    runner = ABBatchRunner()
    results = runner.run(dataset)

    assert len(results) == 2

    agg = ABBatchAggregator().aggregate(results)

    assert "avg_bsi" in agg
    assert "avg_eig" in agg
    assert agg["count"] == 2
