from bsi_benchmark.ab.statistics.analyzer import StatisticalAnalyzer


def test_statistics():

    summary = StatisticalAnalyzer().summarize(
        [0.4, 0.6, 0.8]
    )

    assert summary["count"] == 3
    assert summary["min"] == 0.4
    assert summary["max"] == 0.8
    assert abs(summary["mean"] - 0.6) < 1e-6
