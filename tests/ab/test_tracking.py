from bsi_benchmark.ab.runner import ABExperimentRunner
from bsi_benchmark.ab.tracking.logger import ABLogger
from bsi_benchmark.ab.tracking.store import ABStore


def test_tracking_system(tmp_path):

    runner = ABExperimentRunner()

    results = runner.run([
        "What is AI?",
    ])

    logger = ABLogger(log_dir=tmp_path / "logs")
    file_path = logger.log("test_experiment", results)

    store = ABStore(log_dir=tmp_path / "logs")

    experiments = store.list_experiments()

    assert len(experiments) == 1

    loaded = store.load(experiments[0])
    assert "results" in loaded
    assert loaded["experiment_name"] == "test_experiment"
