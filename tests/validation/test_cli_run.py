import subprocess


def test_cli_run(tmp_path):

    out = tmp_path / "report.html"

    p = subprocess.run(
        [
            "bsi-benchmark",
            "run",
            "--provider",
            "crossref",
            "--query",
            "Artificial Intelligence",
            "--format",
            "html",
            "--output",
            str(out),
        ],
        capture_output=True,
        text=True,
    )

    assert p.returncode == 0
    assert out.exists()
    assert "BSI Benchmark Report" in out.read_text(encoding="utf-8")
