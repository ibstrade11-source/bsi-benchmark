from types import SimpleNamespace

from bsi_benchmark.comparison.result import (
    ComparisonCell,
    ComparisonReport,
    ComparisonResult,
)


def _analysis():
    return SimpleNamespace(
        text="valid analysis",
    )


def _cell(judge_result):
    return ComparisonCell(
        generator="test",
        mode="bsi",
        analysis=_analysis(),
        metadata={},
        judge_result=judge_result,
        failed=False,
    )


def _result(judge_result):
    article = SimpleNamespace(
        title="Test Article",
        abstract="Test abstract",
        doi=None,
        url=None,
    )
    return ComparisonResult(
        article=article,
        cells=[_cell(judge_result)],
    )


def test_heuristic_fallback_is_not_a_valid_judge():
    cell = _cell(
        {
            "criteria_source": "heuristic_fallback",
            "total_scores": {"raw": 5.0, "bsi": 8.0},
        }
    )

    assert cell.has_valid_judge is False


def test_heuristic_fallback_makes_report_non_publishable():
    report = ComparisonReport(
        dataset_name="fallback-test",
        results=[
            _result(
                {
                    "criteria_source": "heuristic_fallback",
                    "total_scores": {"raw": 5.0, "bsi": 8.0},
                }
            )
        ],
    )

    assert report.complete is False
