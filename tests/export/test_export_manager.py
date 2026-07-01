from bsi_benchmark.benchmark import BenchmarkRunner
from bsi_benchmark.export import ExportManager

def test_export_manager(tmp_path):
    result = BenchmarkRunner().run(
        "crossref",
        "Artificial Intelligence",
    )

    out = tmp_path / "report.html"

    ExportManager().export(
        result,
        "html",
        out,
    )

    assert out.exists()
