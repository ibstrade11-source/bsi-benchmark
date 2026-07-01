import subprocess

def test_cli_run():

    p = subprocess.run(
        [
            "bsi-benchmark",
            "run",
            "--provider",
            "crossref",
            "--query",
            "Artificial Intelligence",
        ],
        capture_output=True,
        text=True,
    )

    assert p.returncode == 0
