from bsi_benchmark.benchmark import BenchmarkRunner
from bsi_benchmark.reporting import HtmlReport


def test_html_report(tmp_path):
    result = BenchmarkRunner().run(
        "crossref",
        "Artificial Intelligence",
    )

    out = tmp_path / "report.html"

    HtmlReport().generate(result, out)

    assert out.exists()

    text = out.read_text(encoding="utf-8")

    assert "BSI Benchmark Report" in text
    assert "Artificial Intelligence" in text
