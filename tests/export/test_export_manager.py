from bsi_benchmark.benchmark import BenchmarkRunner
from bsi_benchmark.export import ExportManager

import os
import pytest
def test_export_manager(tmp_path):
    if os.environ.get("BSI_LIVE_NETWORK_TESTS") != "1":
        pytest.skip(
            "Crossref export integration test disabled by default; "
            "set BSI_LIVE_NETWORK_TESTS=1 to run it."
        )
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
