from bsi_benchmark.benchmark import BenchmarkRunner
from bsi_benchmark.history import HistoryStore

def test_history_roundtrip():
    result = BenchmarkRunner().run(
        "crossref",
        "Artificial Intelligence",
    )

    path = HistoryStore().save(result)

    assert path.exists()
