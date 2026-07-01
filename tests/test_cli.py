from bsi_benchmark.cli import main


def test_cli_exists():
    assert callable(main)
