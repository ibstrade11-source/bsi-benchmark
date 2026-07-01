from bsi_benchmark.benchmark import BenchmarkRunner
from bsi_benchmark.reporting.csv_reporter import CsvReporter


def test_csv_report(tmp_path):
    result = BenchmarkRunner().run(
        "crossref",
        "Artificial Intelligence",
    )

    out = tmp_path / "report.csv"

    CsvReporter().generate(result, out)

    assert out.exists()

    text = out.read_text(encoding="utf-8")

    assert "Metric" in text
    assert "BSI" in text
